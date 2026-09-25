#!/usr/bin/env python3
"""Ingest a study-swarm wave's research-raw.json into training-knowledge/training.db.

Idempotent per wave: deletes any existing rows for the wave_number before inserting,
so re-running a wave (after a re-dispatch) cleanly replaces it.

research-raw.json shape (the contract the wave swarm produces):
{
  "wave": 1, "date": "YYYY-MM-DD",
  "lanes": [{
    "slug": "<category-slug>",
    "research": {
      "techniques": [{
        slug,name,kind,method_family,applicable_to,base_model_family,claim,summary,design_implication,
        evidence_strength,seed,num_runs,variance_note,tuning_budget,search_method,measured_conditions,
        engine_recipe_ref,base_model_slug,predecessor_slug,stage_order,commercial_use,commercial_notes,
        rig_fit,studio_fit,status,
        hparams:[{name,value,unit,required,note}],
        failures:[{symptom,cause,remediation,recipe_field,severity}],
        evals:[{eval_kind,metric,harness,task_version,prompt_template,n_shot,precision,seed,judge_model_family,result,threshold,accepted,note}],
        datasets:[{slug,role,note}],            # refs to datasets defined in this lane's research.datasets
        best_for:[{purpose,fitness,use_tag,note}],
        sources:[{kind,title,authors,year,identifier,url,claim,finding_supported}]
      }],
      "datasets":[{slug,name,base_model_target,modality,image_count,caption_format,caption_strategy,pruning_rule,
                   dedup_method,dedup_threshold,reg_image_count,reg_source,real_synthetic_ratio,motivation,
                   collection_process,preprocessing,intended_uses,license,redistribution,maintained,
                   train_eval_overlap_checked, sources:[...]}],
      "failures":[{symptom,cause,remediation,recipe_field,severity, sources:[...]}]   # cross-cutting (technique_id NULL)
    },
    "verify": {"verdicts": [{slug,overall,currency,note}]}   # overall: confirmed|confirmed-with-fixes|...
  }]
}

Run with UTF-8 forced on Windows (entries carry em-dashes):
    $env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; python scripts/load_db.py waves/wave-01-foundation/research-raw.json
"""
import json
import os
import re
import sqlite3
import sys

from refresh_meta import set_meta_currency  # currency pointer is derived from the DB, never the ingest wave
from migrate_s6 import migrate_s6  # apply schema.sql + S6 column ALTERs idempotently on every load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "training.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

WAVE_TITLES = {
    1: "Foundation — the SDXL spine + cross-cutting method/dataset/eval/debug craft (thin pass, prove the partition)",
    2: "Migration — rig-measured training-craft recipes re-homed from tensor-engine",
    3: "Diffusion depth — SDXL / Flux / dataset / eval (research)",
    4: "SDXL measurement — optimizer + network-type receipts (measured-on-rig)",
    5: "Eval measurement — CLIP-sim/CMMD style-fidelity panel on the wave-4 LoRAs (n=20 de-noised)",
    6: "Chroma measurement — rank/flow-shift/fp8-base receipts on Chroma1-HD (measured-on-rig, n=20 eval)",
    7: "SDXL research measurement — noise levers (noise_offset breaks #165) / checkpoint cadence / multi-concept repeat-balancing (measured-on-rig)",
    8: "Qwen-Image LoRA measurement — tallow_fen_style_v1/v2 recipe + style-descriptor noun literalization (measured-on-rig)",
    9: "Qwen-Image bestiary expansion — shape-anchored i2i for silhouette-hard classes, 3-run no-late-collapse, TRELLIS winged+headed mesh fragility (measured-on-rig)",
}

# used only when the wave file supplies neither
DEFAULT_DOMAIN_SCOPE = ("all (peft-methods, diffusion-sdxl-lora, diffusion-flux-lora, dataset-caption, llm-finetune, "
                        "efficiency, evaluation, debugging)")
DEFAULT_VERIFIER_NOTE = ("Reasoning-stripped adversarial verifier per lane (different model tier); WebFetch/WebSearch "
                         "retrieval oracle for paper/doc existence + attribution + currency. Family-different "
                         "local-panel deferred.")

# status + evidence ordinals -> try-first ordering (lower = try first)
STATUS_RANK = {"recommended": 0, "runner-up": 2, "situational": 4, "legacy": 7, "superseded": 8, "avoid": 9}
EV_RANK = {"measured-on-rig": 0, "reproduced-from-source": 1, "single-reported-run": 3,
           "community-claim": 5, "untested": 7}


def wave_file_title(raw, wave_no):
    """The wave file's title, minus the redundant "Wave <n> -" every one of them repeats."""
    t = (raw or "").strip()
    if not t:
        return None
    t = re.sub(rf"^wave\s*{wave_no}\s*[—–:-]\s*", "", t, flags=re.I)
    return t.strip() or None


def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def priority(status, evidence):
    return 1 + STATUS_RANK.get(status, 5) + EV_RANK.get(evidence, 4)


def uniq_slug(cur, table, base):
    s, k = base, 2
    while cur.execute(f"SELECT 1 FROM {table} WHERE slug=?", (s,)).fetchone():
        s, k = f"{base}-{k}", k + 1
    return s


def i(v):
    """int-or-None."""
    try:
        return int(v) if v is not None and str(v).strip() != "" else None
    except (ValueError, TypeError):
        return None


def b(v):
    """bool-ish -> 1/0/None."""
    if v in (True, 1):
        return 1
    if v in (False, 0):
        return 0
    if isinstance(v, str):
        t = v.strip().lower()
        if t in ("yes", "true", "1"):
            return 1
        if t in ("no", "false", "0"):
            return 0
    return None


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "lanes" not in data and isinstance(data.get("result"), dict):  # tolerate harness envelope
        data = data["result"]
    wave_no = int(data.get("wave", 1))
    date = data.get("date", "")
    lanes = data.get("lanes", [])
    # the wave file's own verification record and scope win over the generic defaults;
    # both are refreshed on reload so a re-ingest produces the same row as a first ingest
    verifier_note = data.get("verifier_note") or DEFAULT_VERIFIER_NOTE
    domain_scope = data.get("domain_scope") or DEFAULT_DOMAIN_SCOPE
    # curated titles win; otherwise use the wave file's own, minus the "Wave N —" it repeats
    title = WAVE_TITLES.get(wave_no) or wave_file_title(data.get("title"), wave_no) or f"Wave {wave_no}"

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    migrate_s6(con)  # schema.sql + S6 column ALTERs (idempotent); supersedes a bare executescript
    cur = con.cursor()

    # wave row (insert or refresh) ------------------------------------------------
    row = cur.execute("SELECT id FROM waves WHERE wave_number=?", (wave_no,)).fetchone()
    if row:
        wave_id = row[0]
        # clean replace: cascade clears technique-linked rows; explicitly clear wave-scoped orphans
        cur.execute("DELETE FROM techniques WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM datasets WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM technique_failures WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM sources WHERE wave_id=?", (wave_id,))
        cur.execute("UPDATE waves SET title=?, dispatched_date=?, status='synthesized', domain_scope=?, "
                    "verifier_note=? WHERE id=?", (title, date, domain_scope, verifier_note, wave_id))
    else:
        cur.execute(
            """INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path)
               VALUES(?,?,?,?,?,?,?,?)""",
            (wave_no, title, date,
             domain_scope, len(lanes), verifier_note,
             "synthesized", f"waves/{os.path.basename(os.path.dirname(os.path.abspath(path)))}/dispatch.md"))
        wave_id = cur.lastrowid

    cat = {s: i_ for s, i_ in cur.execute("SELECT slug,id FROM categories")}

    def purpose_id(name, category_id):
        sl = slugify(name)
        r = cur.execute("SELECT id FROM purposes WHERE slug=?", (sl,)).fetchone()
        if r:
            return r[0]
        cur.execute("INSERT INTO purposes(slug,name,category_id) VALUES(?,?,?)", (sl, name, category_id))
        return cur.lastrowid

    def add_sources(rows, technique_id, subject=None, target_table=None, target_id=None):
        n = 0
        for s in (rows or []):
            if not s.get("url"):
                continue
            cur.execute(
                """INSERT INTO sources(technique_id,subject,kind,title,authors,year,identifier,url,claim,
                   retrieved_date,verified,finding_supported,target_table,target_id,wave_id)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (technique_id, subject, s.get("kind"), s.get("title"), s.get("authors"), str(s.get("year") or "") or None,
                 s.get("identifier"), s.get("url"), s.get("claim"), date,
                 1 if s.get("finding_supported") in ("SUPPORTED", "PARTIAL") else 0,
                 s.get("finding_supported"), target_table, target_id, wave_id))
            n += 1
        return n

    n_tech = n_ds = n_src = n_hp = n_fail = n_eval = n_refuted = 0
    refuted = []       # (slug, note) — ANDON: a refuted core claim is a defect; it does NOT enter the KB
    pending_pred = []       # (technique_id, predecessor_slug) resolved after all techniques exist
    pending_supersede = []  # (new_technique_id, superseded_slug) — measurement waves retire research versions
    tech_ids = {}      # slug -> id

    for lane in lanes:
        lslug = lane.get("slug")
        category_id = cat.get(lslug)
        if category_id is None and lslug:  # safety net for a brand-new lane slug
            cur.execute("INSERT OR IGNORE INTO categories(slug,name,description,sort) VALUES(?,?,?,?)",
                        (lslug, lslug.replace("-", " ").title(), "auto-created from wave lane", 99))
            category_id = cur.execute("SELECT id FROM categories WHERE slug=?", (lslug,)).fetchone()[0]
            cat[lslug] = category_id
        research = lane.get("research") or {}
        verify = lane.get("verify") or {}
        verdicts = {}
        for v in (verify.get("verdicts") or []):
            key = (v.get("slug") or v.get("name") or "").strip().lower()
            if key:
                verdicts[key] = v

        # datasets first (so technique_datasets can resolve slug -> id) -----------
        ds_ids = {}
        for d in (research.get("datasets") or []):
            dslug = uniq_slug(cur, "datasets", slugify(d.get("slug") or d.get("name")))
            cur.execute(
                """INSERT INTO datasets(slug,name,base_model_target,modality,image_count,caption_format,caption_strategy,
                   pruning_rule,dedup_method,dedup_threshold,reg_image_count,reg_source,real_synthetic_ratio,motivation,
                   collection_process,preprocessing,intended_uses,license,redistribution,maintained,
                   train_eval_overlap_checked,verified,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (dslug, d.get("name"), d.get("base_model_target"), d.get("modality"), i(d.get("image_count")),
                 d.get("caption_format"), d.get("caption_strategy"), d.get("pruning_rule"), d.get("dedup_method"),
                 d.get("dedup_threshold"), i(d.get("reg_image_count")), d.get("reg_source"), d.get("real_synthetic_ratio"),
                 d.get("motivation"), d.get("collection_process"), d.get("preprocessing"), d.get("intended_uses"),
                 d.get("license"), d.get("redistribution"), d.get("maintained"), b(d.get("train_eval_overlap_checked")),
                 # A licence string is a field, not a check. Verified only when a
                 # verifier says so; presence of a licence is recorded separately.
                 0, wave_id, date))
            did = cur.lastrowid
            ds_ids[d.get("slug") or dslug] = did
            n_ds += 1
            n_src += add_sources(d.get("sources"), None, subject=d.get("name"), target_table="datasets", target_id=did)

        # techniques -------------------------------------------------------------
        for t in (research.get("techniques") or []):
            name = t.get("name")
            tslug = uniq_slug(cur, "techniques", slugify(t.get("slug") or name))
            status = t.get("status")
            ev = t.get("evidence_strength")
            v = verdicts.get((t.get("slug") or name or "").strip().lower(), {})
            overall = v.get("overall")
            if overall == "refuted":  # ANDON: external verifier contradicted a core claim — halt it at the gate
                n_refuted += 1
                refuted.append((t.get("slug") or name, v.get("note")))
                continue
            verified = 1 if overall in ("confirmed", "confirmed-with-fixes") else 0
            parts = []
            if overall:
                parts.append(f"verdict={overall}")
            if v.get("currency"):
                parts.append(f"currency={v['currency']}")
            if v.get("note"):
                parts.append(v["note"])
            vnote = " | ".join(parts) or None

            cur.execute(
                """INSERT INTO techniques(slug,name,category_id,kind,method_family,applicable_to,base_model_family,
                   claim,summary,design_implication,evidence_strength,seed,num_runs,variance_note,tuning_budget,
                   search_method,measured_conditions,engine_recipe_ref,base_model_slug,stage_order,commercial_use,
                   commercial_notes,rig_fit,studio_fit,download_priority,status,verified,verify_note,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (tslug, name, category_id, t.get("kind"), t.get("method_family"), t.get("applicable_to"),
                 t.get("base_model_family"), t.get("claim"), t.get("summary"), t.get("design_implication"), ev,
                 t.get("seed"), i(t.get("num_runs")), t.get("variance_note"), t.get("tuning_budget"),
                 t.get("search_method"), t.get("measured_conditions"), t.get("engine_recipe_ref"), t.get("base_model_slug"),
                 i(t.get("stage_order")), t.get("commercial_use"), t.get("commercial_notes"), i(t.get("rig_fit")),
                 i(t.get("studio_fit")), priority(status, ev), status, verified, vnote, wave_id, date))
            tid = cur.lastrowid
            tech_ids[t.get("slug") or tslug] = tid
            n_tech += 1
            if t.get("predecessor_slug"):
                pending_pred.append((tid, t["predecessor_slug"]))
            if t.get("supersedes"):
                pending_supersede.append((tid, t["supersedes"]))

            for hp in (t.get("hparams") or []):
                cur.execute("INSERT INTO technique_hparams(technique_id,name,value,unit,required,note) VALUES(?,?,?,?,?,?)",
                            (tid, hp.get("name"), str(hp.get("value")) if hp.get("value") is not None else None,
                             hp.get("unit"), b(hp.get("required")) or 0, hp.get("note")))
                n_hp += 1
            for fa in (t.get("failures") or []):
                cur.execute(
                    "INSERT INTO technique_failures(technique_id,symptom,cause,remediation,recipe_field,severity,wave_id) "
                    "VALUES(?,?,?,?,?,?,?)",
                    (tid, fa.get("symptom"), fa.get("cause"), fa.get("remediation"), fa.get("recipe_field"),
                     fa.get("severity"), wave_id))
                n_fail += 1
            for ev_row in (t.get("evals") or []):
                cur.execute(
                    """INSERT INTO technique_evals(technique_id,eval_kind,metric,harness,task_version,prompt_template,
                       n_shot,precision,seed,judge_model_family,result,threshold,accepted,note)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (tid, ev_row.get("eval_kind"), ev_row.get("metric"), ev_row.get("harness"), ev_row.get("task_version"),
                     ev_row.get("prompt_template"), i(ev_row.get("n_shot")), ev_row.get("precision"), ev_row.get("seed"),
                     ev_row.get("judge_model_family"), ev_row.get("result"), ev_row.get("threshold"),
                     b(ev_row.get("accepted")), ev_row.get("note")))
                n_eval += 1
            for dref in (t.get("datasets") or []):
                did = ds_ids.get(dref.get("slug"))
                if did is None:
                    r = cur.execute("SELECT id FROM datasets WHERE slug=?", (slugify(dref.get("slug")),)).fetchone()
                    did = r[0] if r else None
                if did is not None:
                    cur.execute("INSERT OR IGNORE INTO technique_datasets(technique_id,dataset_id,role,note) VALUES(?,?,?,?)",
                                (tid, did, dref.get("role") or "training", dref.get("note")))
            for bf in (t.get("best_for") or []):
                pn = bf.get("purpose")
                if not pn:
                    continue
                cur.execute(
                    "INSERT OR REPLACE INTO technique_purposes(technique_id,purpose_id,fitness,rank,use_tag,note) "
                    "VALUES(?,?,?,?,?,?)",
                    (tid, purpose_id(pn, category_id), i(bf.get("fitness")), i(bf.get("rank")), bf.get("use_tag"),
                     bf.get("note")))
            n_src += add_sources(t.get("sources"), tid)

        # lane-level cross-cutting failures (technique_id NULL) ------------------
        for fa in (research.get("failures") or []):
            cur.execute(
                "INSERT INTO technique_failures(technique_id,symptom,cause,remediation,recipe_field,severity,wave_id) "
                "VALUES(NULL,?,?,?,?,?,?)",
                (fa.get("symptom"), fa.get("cause"), fa.get("remediation"), fa.get("recipe_field"),
                 fa.get("severity"), wave_id))
            n_fail += 1
            n_src += add_sources(fa.get("sources"), None, subject=fa.get("symptom"))

    # resolve predecessor links now that every technique exists -------------------
    for tid, pred_slug in pending_pred:
        pid = tech_ids.get(pred_slug) or (
            lambda r: r[0] if r else None)(cur.execute("SELECT id FROM techniques WHERE slug=?", (slugify(pred_slug),)).fetchone())
        if pid:
            cur.execute("UPDATE techniques SET predecessor_technique_id=? WHERE id=?", (pid, tid))

    # a measurement-wave technique retires the research version it corrects (provenance kept, not deleted)
    n_superseded = 0
    for new_tid, old_slug in pending_supersede:
        r = cur.execute("SELECT id FROM techniques WHERE slug=?", (old_slug,)).fetchone()
        if r and r[0] != new_tid:
            cur.execute("UPDATE techniques SET status='superseded', superseded_by=? WHERE id=?", (new_tid, r[0]))
            n_superseded += 1
    if n_superseded:
        print(f"  superseded {n_superseded} prior-wave technique(s) (status='superseded' + superseded_by set).")

    # rebuild FTS ----------------------------------------------------------------
    cur.execute("DELETE FROM techniques_fts")
    cur.execute(
        """INSERT INTO techniques_fts(rowid,slug,name,method_family,applicable_to,base_model_family,summary,claim,best_for,category)
           SELECT t.id, t.slug, t.name, COALESCE(t.method_family,''), COALESCE(t.applicable_to,''),
                  COALESCE(t.base_model_family,''), COALESCE(t.summary,''), COALESCE(t.claim,''),
                  COALESCE((SELECT group_concat(p.name,' ') FROM technique_purposes tp
                            JOIN purposes p ON p.id=tp.purpose_id WHERE tp.technique_id=t.id),''),
                  COALESCE((SELECT name FROM categories c WHERE c.id=t.category_id),'')
           FROM techniques t""")

    # meta: static identity + DB-derived currency pointer ------------------------
    meta = {
        "kb_name": "training-knowledge",
        "rig": "OMEN 45L · RTX 5090 · Blackwell sm_120 · 32 GB VRAM · Core Ultra 9 · 64 GB RAM · Windows 11 / WSL2 (the only machine)",
        "scope": "Portable TRAINING CRAFT — methods, recipes, hyperparameter values, dataset/eval/debug know-how — for "
                 "the single-RTX-5090 pipeline. The how-to-train layer between the weights (model-knowledge) and the "
                 "software (tensor-engine-knowledge). Rig-measured engine receipts stay in tensor-engine, referenced via "
                 "engine_recipe_ref, never restated.",
    }
    for k, vv in meta.items():
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, vv))
    set_meta_currency(cur)  # latest_wave = MAX(wave_number), updated = that wave's date

    con.commit()
    print(f"wave {wave_no}: {n_tech} techniques, {n_ds} datasets, {n_hp} hparams, {n_fail} failures, "
          f"{n_eval} evals, {n_src} sources.")
    if n_refuted:
        print(f"  ⚠ {n_refuted} technique(s) EXCLUDED by the verifier (refuted core claim):")
        for sl, note in refuted:
            print(f"    - {sl}: {(note or '')[:100]}")
    for r in cur.execute(
        """SELECT c.name, COUNT(*), COALESCE(SUM(t.verified),0)
           FROM techniques t JOIN categories c ON c.id=t.category_id
           WHERE t.wave_id=? GROUP BY c.name ORDER BY c.sort""", (wave_id,)):
        print(f"  {r[0]:42s} {r[1]:2d} techniques  ({r[2]} verified)")
    con.close()


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-foundation", "research-raw.json")
    main(p)
