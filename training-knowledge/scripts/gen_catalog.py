#!/usr/bin/env python3
"""Generate human-readable catalog/*.md from training.db. Re-run after each wave:
    python gen_catalog.py
DB-only (no dependency on raw swarm json) so it always reflects current DB state.
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "training.db")
OUT = os.path.join(ROOT, "catalog")

COMM = {"yes": "✅ yes", "no": "⛔ no", "conditional": "⚠ cond", "unknown": "? unk"}
EV = {"measured-on-rig": "▣ measured", "reproduced-from-source": "▸ reproduced",
      "single-reported-run": "· single-run", "community-claim": "· community", "untested": "· untested"}


def cell(s):
    return ("" if s is None else str(s)).replace("|", "/").replace("\n", " ").strip()


def write_cat(c, cat, wave, date):
    rows = c.execute("SELECT * FROM techniques WHERE category_id=? ORDER BY download_priority, name", (cat["id"],)).fetchall()
    rec = sum(1 for t in rows if t["status"] == "recommended")
    meas = sum(1 for t in rows if t["evidence_strength"] == "measured-on-rig")
    L = [f"# {cat['name']}",
         f"_{cat['description']}_ · wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} techniques · {rec} recommended · {meas} measured-on-rig. "
         f"Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).\n",
         "| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |",
         "|---|-----------|--------|---------|----------|------|-----|--------|---|"]
    for t in rows:
        L.append(f"| {t['download_priority'] or ''} | {cell(t['name'])} | {cell(t['method_family'])} | "
                 f"{cell(t['applicable_to'])} | {EV.get(t['evidence_strength'], cell(t['evidence_strength']))} | "
                 f"{COMM.get(t['commercial_use'], cell(t['commercial_use']))} | {cell(t['rig_fit'])} | "
                 f"{cell(t['studio_fit'])} | {'✓' if t['verified'] else '·'} |")
    L.append("\n## Detail\n")
    for t in rows:
        L.append(f"### {t['name']} · `{t['status']}` · {EV.get(t['evidence_strength'], t['evidence_strength'] or '')}")
        if t["claim"]:
            L.append(f"**{t['claim']}**")
        if t["summary"]:
            L.append(t["summary"])
        if t["design_implication"]:
            L.append(f"- **For the pipeline:** {t['design_implication']}")
        meta = []
        for label, key in [("Method", "method_family"), ("Applies to", "applicable_to"),
                           ("Base", "base_model_family"), ("Kind", "kind")]:
            if t[key]:
                meta.append(f"**{label}:** {t[key]}")
        if meta:
            L.append("- " + " · ".join(meta))
        repro = []
        for label, key in [("Seed", "seed"), ("Runs", "num_runs"), ("Tuning budget", "tuning_budget"),
                           ("Search", "search_method")]:
            if t[key]:
                repro.append(f"**{label}:** {t[key]}")
        if repro:
            L.append("- " + " · ".join(repro))
        if t["variance_note"]:
            L.append(f"- **Variance:** {t['variance_note']}")
        if t["measured_conditions"]:
            L.append(f"- **Validated under:** {t['measured_conditions']}")
        if t["engine_recipe_ref"]:
            L.append(f"- **Measured receipt (tensor-engine):** `{t['engine_recipe_ref']}` — the rig-measured it/s + VRAM peak live there, not here.")
        if t["base_model_slug"]:
            L.append(f"- **Base model (model-knowledge):** `{t['base_model_slug']}`")
        if t["predecessor_technique_id"] is not None:
            pre = c.execute("SELECT name FROM techniques WHERE id=?", (t["predecessor_technique_id"],)).fetchone()
            if pre:
                L.append(f"- **Builds on (stage {t['stage_order'] or '?'}):** {cell(pre['name'])}")
        lic = f"- **Output license:** commercial **{t['commercial_use'] or '?'}**"
        if t["commercial_notes"]:
            lic += f" — {t['commercial_notes']}"
        L.append(lic)
        L.append(f"- **Fit:** rig {t['rig_fit'] if t['rig_fit'] is not None else '-'}/5 · "
                 f"studio {t['studio_fit'] if t['studio_fit'] is not None else '-'}/5")

        hps = c.execute("SELECT name,value,unit,required,note FROM technique_hparams WHERE technique_id=? ORDER BY id",
                        (t["id"],)).fetchall()
        if hps:
            L += ["", "**Hyperparameters**", "", "| Param | Value | Req | Note |", "|---|---|---|---|"]
            L += [f"| {cell(h['name'])} | {cell(h['value'])}{(' ' + cell(h['unit'])) if h['unit'] else ''} | "
                  f"{'●' if h['required'] else '○'} | {cell(h['note'])} |" for h in hps] + [""]

        dss = c.execute("""SELECT d.name, d.license, td.role FROM technique_datasets td
                           JOIN datasets d ON d.id=td.dataset_id WHERE td.technique_id=? ORDER BY td.role""",
                        (t["id"],)).fetchall()
        if dss:
            L.append("- **Datasets:** " + " ; ".join(
                f"{cell(d['name'])} ({cell(d['role'])}, license {cell(d['license']) or '?'})" for d in dss))

        fas = c.execute("SELECT symptom,cause,remediation,recipe_field FROM technique_failures WHERE technique_id=? ORDER BY id",
                        (t["id"],)).fetchall()
        if fas:
            L += ["", "**Failure modes**", "", "| Symptom | Cause | Fix | Field |", "|---|---|---|---|"]
            L += [f"| {cell(f['symptom'])} | {cell(f['cause'])} | {cell(f['remediation'])} | {cell(f['recipe_field'])} |"
                  for f in fas] + [""]

        evs = c.execute("""SELECT eval_kind,metric,result,threshold,accepted,judge_model_family FROM technique_evals
                           WHERE technique_id=? ORDER BY id""", (t["id"],)).fetchall()
        if evs:
            L += ["", "**Evaluation**", "", "| Kind | Metric | Result | Threshold | Pass | Judge family |", "|---|---|---|---|---|---|"]
            L += [f"| {cell(e['eval_kind'])} | {cell(e['metric'])} | {cell(e['result'])} | {cell(e['threshold'])} | "
                  f"{'✓' if e['accepted']==1 else ('✗' if e['accepted']==0 else '—')} | {cell(e['judge_model_family'])} |"
                  for e in evs] + [""]

        bf = c.execute("""SELECT p.name pn, tp.fitness f, tp.use_tag u FROM technique_purposes tp
                          JOIN purposes p ON p.id=tp.purpose_id WHERE tp.technique_id=? ORDER BY tp.fitness DESC""",
                       (t["id"],)).fetchall()
        if bf:
            L.append("- **Best for:** " + " ; ".join(
                f"{cell(x['pn'])} ({x['u'] or '-'}, fit {x['f'] if x['f'] is not None else '-'})" for x in bf))
        if t["verify_note"]:
            L.append(f"- **Verify:** {t['verify_note']}")
        srcs = c.execute("SELECT title,url,claim,authors,year FROM sources WHERE technique_id=? ORDER BY id", (t["id"],)).fetchall()
        if srcs:
            L.append("- **Sources:** " + " ; ".join(
                f"[{cell(s['title'] or 'source')}]({s['url']})"
                + (f" ({cell(s['authors'])}, {cell(s['year'])})" if s['authors'] else "")
                + (f" — {cell(s['claim'])}" if s["claim"] else "") for s in srcs))
        L.append("")

    # cross-cutting failures pinned to this lane (technique_id NULL)
    xf = c.execute("""SELECT f.symptom,f.cause,f.remediation,f.recipe_field FROM technique_failures f
                      WHERE f.technique_id IS NULL AND f.wave_id IN (SELECT id FROM waves)
                      AND ?='debugging'""", (cat["slug"],)).fetchall()
    if xf:
        L += ["## Cross-cutting failure modes\n", "| Symptom | Cause | Fix | Field |", "|---|---|---|---|"]
        L += [f"| {cell(f['symptom'])} | {cell(f['cause'])} | {cell(f['remediation'])} | {cell(f['recipe_field'])} |"
              for f in xf] + [""]

    with open(os.path.join(OUT, cat["slug"] + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    wr = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()
    wave = wr[0] if wr else 0
    dr = c.execute("SELECT value FROM meta WHERE key='updated'").fetchone()
    date = dr[0] if dr else ""
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUT, exist_ok=True)

    idx = [f"# Catalog — training craft (methods · recipes · datasets · eval · debug)\n",
           f"Generated from `training.db` · wave {wave} · {date}. "
           f"Narrative + plan: [wave-01 dispatch](../waves/wave-01-foundation/dispatch.md). "
           f"Verification receipt: [verification.md](../waves/wave-01-foundation/verification.md).\n",
           "The portable **how-to-train** layer for this rig (RTX 5090 · Blackwell · 32 GB · Win 11 / WSL2). "
           "Sibling KBs: [model-knowledge](../../model-knowledge/catalog/README.md) (the *weights*) · "
           "[tensor-engine-knowledge](../../tensor-engine-knowledge/catalog/README.md) (the *software* + rig-measured receipts). "
           "This one owns the *methods, recipes, hyperparameter values, dataset & eval craft* — and points at the measured "
           "numbers via `engine_recipe_ref`, never restates them.\n",
           "## Try-first shortlist\n",
           "Top `recommended` picks per lane, by try-first order. `Evidence` ▣ measured-on-rig is the strongest tier.\n",
           "| Lane | ↓ | Technique | Method | Applies | Evidence | Comm | ✓ |",
           "|---|---|---|---|---|---|---|---|"]
    for cat in cats:
        for t in c.execute("""SELECT * FROM techniques WHERE category_id=? AND status='recommended'
                              ORDER BY download_priority, name LIMIT 3""", (cat["id"],)):
            idx.append(f"| {cell(cat['name'])} | {t['download_priority']} | [{cell(t['name'])}]({cat['slug']}.md) | "
                       f"{cell(t['method_family'])} | {cell(t['applicable_to'])} | "
                       f"{EV.get(t['evidence_strength'], cell(t['evidence_strength']))} | "
                       f"{COMM.get(t['commercial_use'], cell(t['commercial_use']))} | {'✓' if t['verified'] else ''} |")
    idx += ["", "## Lanes\n"]
    for cat in cats:
        n = c.execute("SELECT COUNT(*) FROM techniques WHERE category_id=?", (cat["id"],)).fetchone()[0]
        idx.append(f"- [{cell(cat['name'])}]({cat['slug']}.md) — {cell(cat['description'])} ({n} techniques)")
    idx += ["",
            "## Legend\n",
            "- **↓** try-first order (lower = try first; derived from status + evidence strength).",
            "- **Evidence** ▣ measured-on-rig > ▸ reproduced-from-source > · single-run / community / untested. The ordinal "
            "disciplines a single-reported claim from wearing the authority of an on-rig measurement.",
            "- **Comm** commercial use of the OUTPUT: ✅ yes / ⚠ conditional / ⛔ no / ? unknown. A LoRA/fine-tune inherits "
            "its base model's + dataset's license.",
            "- **Rig** fit 0–5 for this exact rig (RTX 5090 · 32 GB · Win 11 / WSL2). **Studio** fit 0–5 for the studio's "
            "actual training workloads.",
            "- **✓** retrieval-verified this wave (existence + attribution + currency). Blank/· = unverified lead.",
            "- **Boundary:** rig-measured it/s & VRAM peaks live in tensor-engine-knowledge (linked via `engine_recipe_ref`); "
            "base weights live in model-knowledge; inference placement in docker-knowledge."]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    for cat in cats:
        write_cat(c, cat, wave, date)
    con.close()
    print("catalog/ regenerated:", ", ".join(cat["slug"] + ".md" for cat in cats), "+ README.md")


if __name__ == "__main__":
    main()
