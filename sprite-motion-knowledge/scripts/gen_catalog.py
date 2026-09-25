#!/usr/bin/env python3
"""Generate human-readable catalog/*.md from recipes.db. Re-run after each wave:
    python gen_catalog.py
DB-only (no dependency on raw swarm json) so it always reflects current DB state.
NEVER hand-edit catalog/*.md — they are regenerated from the DB.
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "recipes.db")
OUT = os.path.join(ROOT, "catalog")

COMM = {"yes": "✅ yes", "no": "⛔ no", "conditional": "⚠ cond", "unknown": "? unk"}
EV = {"measured-on-rig": "▣ measured", "reproduced-from-source": "▸ reproduced",
      "single-reported-run": "· single-run", "community-claim": "· community", "untested": "· untested"}


def cell(s):
    return ("" if s is None else str(s)).replace("|", "/").replace("\n", " ").strip()


def write_cat(c, cat, wave, date):
    rows = c.execute("SELECT * FROM recipes WHERE category_id=? ORDER BY download_priority, name", (cat["id"],)).fetchall()
    rec = sum(1 for t in rows if t["status"] == "recommended")
    meas = sum(1 for t in rows if t["evidence_strength"] == "measured-on-rig")
    L = [f"# {cat['name']}",
         f"_{cat['description']}_ · wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} recipes · {rec} recommended · {meas} measured-on-rig.\n",
         "| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |",
         "|---|--------|--------|---------|----------|------|-----|--------|---|"]
    for t in rows:
        L.append(f"| {t['download_priority'] or ''} | {cell(t['name'])} | {cell(t['engine_family'])} | "
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
        for label, key in [("Engine", "engine_family"), ("Applies to", "applicable_to"),
                           ("Base", "base_model_family"), ("Kind", "kind")]:
            if t[key]:
                meta.append(f"**{label}:** {t[key]}")
        if meta:
            L.append("- " + " · ".join(meta))
        repro = []
        for label, key in [("Seed", "seed"), ("Runs", "num_runs"), ("Tuning budget", "tuning_budget"),
                           ("VRAM", "vram_gb")]:
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
        if t["predecessor_recipe_id"] is not None:
            pre = c.execute("SELECT name FROM recipes WHERE id=?", (t["predecessor_recipe_id"],)).fetchone()
            if pre:
                L.append(f"- **Builds on (stage {t['stage_order'] or '?'}):** {cell(pre['name'])}")
        lic = f"- **Output license:** commercial **{t['commercial_use'] or '?'}**"
        if t["license"]:
            lic += f" (license: {t['license']})"
        if t["commercial_notes"]:
            lic += f" — {t['commercial_notes']}"
        L.append(lic)
        if t["license_correction"]:
            L.append(f"- **License correction (verifier):** {t['license_correction']}")
        L.append(f"- **Fit:** rig {t['rig_fit'] if t['rig_fit'] is not None else '-'}/5 · "
                 f"studio {t['studio_fit'] if t['studio_fit'] is not None else '-'}/5")

        hps = c.execute("SELECT name,value,unit,required,note FROM recipe_hparams WHERE recipe_id=? ORDER BY id",
                        (t["id"],)).fetchall()
        if hps:
            L += ["", "**Hyperparameters**", "", "| Param | Value | Req | Note |", "|---|---|---|---|"]
            L += [f"| {cell(h['name'])} | {cell(h['value'])}{(' ' + cell(h['unit'])) if h['unit'] else ''} | "
                  f"{'●' if h['required'] else '○'} | {cell(h['note'])} |" for h in hps] + [""]

        dss = c.execute("""SELECT d.name, d.license, rd.role FROM recipe_datasets rd
                           JOIN datasets d ON d.id=rd.dataset_id WHERE rd.recipe_id=? ORDER BY rd.role""",
                        (t["id"],)).fetchall()
        if dss:
            L.append("- **Datasets:** " + " ; ".join(
                f"{cell(d['name'])} ({cell(d['role'])}, license {cell(d['license']) or '?'})" for d in dss))

        fas = c.execute("SELECT symptom,cause,remediation,recipe_field FROM recipe_failures WHERE recipe_id=? ORDER BY id",
                        (t["id"],)).fetchall()
        if fas:
            L += ["", "**Failure modes**", "", "| Symptom | Cause | Fix | Field |", "|---|---|---|---|"]
            L += [f"| {cell(f['symptom'])} | {cell(f['cause'])} | {cell(f['remediation'])} | {cell(f['recipe_field'])} |"
                  for f in fas] + [""]

        evs = c.execute("""SELECT eval_kind,metric,result,threshold,accepted,harness FROM recipe_evals
                           WHERE recipe_id=? ORDER BY id""", (t["id"],)).fetchall()
        if evs:
            L += ["", "**Evaluation**", "", "| Kind | Metric | Result | Threshold | Pass | Harness |", "|---|---|---|---|---|---|"]
            L += [f"| {cell(e['eval_kind'])} | {cell(e['metric'])} | {cell(e['result'])} | {cell(e['threshold'])} | "
                  f"{'✓' if e['accepted']==1 else ('✗' if e['accepted']==0 else '—')} | {cell(e['harness'])} |"
                  for e in evs] + [""]

        bf = c.execute("""SELECT p.name pn, rp.fitness f, rp.use_tag u FROM recipe_purposes rp
                          JOIN purposes p ON p.id=rp.purpose_id WHERE rp.recipe_id=? ORDER BY rp.fitness DESC""",
                       (t["id"],)).fetchall()
        if bf:
            L.append("- **Best for:** " + " ; ".join(
                f"{cell(x['pn'])} ({x['u'] or '-'}, fit {x['f'] if x['f'] is not None else '-'})" for x in bf))
        if t["verify_note"]:
            L.append(f"- **Verify:** {t['verify_note']}")
        srcs = c.execute("SELECT title,url,claim,authors,year FROM sources WHERE recipe_id=? ORDER BY id", (t["id"],)).fetchall()
        if srcs:
            L.append("- **Sources:** " + " ; ".join(
                f"[{cell(s['title'] or 'source')}]({s['url']})"
                + (f" ({cell(s['authors'])}, {cell(s['year'])})" if s['authors'] else "")
                + (f" — {cell(s['claim'])}" if s["claim"] else "") for s in srcs))
        L.append("")

    with open(os.path.join(OUT, cat["slug"] + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    wr = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()
    wave = wr[0] if wr and wr[0] is not None else 0
    dr = c.execute("SELECT value FROM meta WHERE key='updated'").fetchone()
    date = dr[0] if dr else ""
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUT, exist_ok=True)

    idx = [f"# Catalog — sprite-motion recipes (architecture · rigging · AI-motion · inbetween · cloud · combat · verify)\n",
           f"Generated from `recipes.db` · wave {wave} · {date}. NEVER hand-edited — regenerated from the DB.\n",
           "The portable **animate-the-sprite** craft for this rig (RTX 5090 · Blackwell · 32 GB · Win 11 / WSL2) — "
           "the motion layer atop [sprites-knowledge](../../sprites-knowledge/catalog/README.md) (static 2.5D sprite "
           "generation). The spine is **motion truth (rig/mesh/proxy) -> AI polish -> sprite-sheet export -> verify**. "
           "Sibling KBs own the layers this one points at: "
           "[model-knowledge](../../model-knowledge/catalog/README.md) (the *weights*) · "
           "[tensor-engine-knowledge](../../tensor-engine-knowledge/catalog/README.md) (the *software* + rig-measured receipts) · "
           "[blender-knowledge](../../blender-knowledge/catalog/README.md) (Blender 4.x recipes) — "
           "linked via `engine_recipe_ref` / `base_model_slug`, never restated.\n"]

    # ---- Proven on-rig (v_proven) ----
    proven = c.execute("SELECT * FROM v_proven").fetchall()
    idx += ["## Proven on-rig\n",
            "Recipes whose `evidence_strength` is ▣ **measured-on-rig** — validated on this exact machine.\n"]
    if proven:
        idx += ["| Lane | Recipe | Engine | Applies | Comm | Validated under | ✓ |",
                "|---|---|---|---|---|---|---|"]
        for p in proven:
            idx.append(f"| {cell(p['category'])} | {cell(p['name'])} | {cell(p['engine_family'])} | "
                       f"{cell(p['applicable_to'])} | {COMM.get(p['commercial_use'], cell(p['commercial_use']))} | "
                       f"{cell(p['measured_conditions'])} | {'✓' if p['verified'] else '·'} |")
        idx.append("")
    else:
        idx += ["_No measured-on-rig recipes yet — the proven half fills as the rig measures the research recipes._\n"]

    # ---- Recommended shortlist (v_recommended) ----
    idx += ["## Recommended shortlist\n",
            "Top `recommended` / `runner-up` picks per lane, by try-first order. `Evidence` ▣ measured-on-rig is the strongest tier.\n"]
    recommended = c.execute("SELECT * FROM v_recommended").fetchall()
    if recommended:
        idx += ["| Lane | ↓ | Recipe | Engine | Applies | Evidence | Comm | ✓ |",
                "|---|---|---|---|---|---|---|---|"]
        cat_slug_by_name = {cat["name"]: cat["slug"] for cat in cats}
        for t in recommended:
            slug = cat_slug_by_name.get(t["category"], "")
            idx.append(f"| {cell(t['category'])} | {t['dl'] or ''} | [{cell(t['name'])}]({slug}.md) | "
                       f"{cell(t['engine_family'])} | {cell(t['applicable_to'])} | "
                       f"{EV.get(t['evidence_strength'], cell(t['evidence_strength']))} | "
                       f"{COMM.get(t['commercial_use'], cell(t['commercial_use']))} | {'✓' if t['verified'] else ''} |")
        idx.append("")
    else:
        idx += ["_No recommended recipes yet — load a wave to populate the shortlist._\n"]

    # ---- Lanes ----
    idx += ["## Lanes\n"]
    for cat in cats:
        n = c.execute("SELECT COUNT(*) FROM recipes WHERE category_id=?", (cat["id"],)).fetchone()[0]
        idx.append(f"- [{cell(cat['name'])}]({cat['slug']}.md) — {cell(cat['description'])} ({n} recipes)")

    # ---- Legend ----
    idx += ["",
            "## Legend\n",
            "- **↓** try-first order (lower = try first; derived from status + evidence strength).",
            "- **Evidence** ▣ measured-on-rig > ▸ reproduced-from-source > · single-run / community / untested. The "
            "ordinal disciplines a single-reported claim from wearing the authority of an on-rig measurement. Proven "
            "(▣ measured-on-rig) vs research (everything else) is the spine of this KB.",
            "- **Comm** commercial use of the OUTPUT: ✅ yes / ⚠ conditional / ⛔ no / ? unknown. A sprite inherits its "
            "base model's + recon model's license — the decisive axis (Zero123-lineage NVS is non-commercial).",
            "- **Rig** fit 0–5 for this exact rig (RTX 5090 · 32 GB · Win 11 / WSL2). **Studio** fit 0–5 for "
            "commercial 2.5D JRPG sprite production.",
            "- **✓** retrieval-verified this wave (existence + attribution + currency). Blank/· = unverified lead.",
            "- **Boundary:** rig-measured it/s & VRAM peaks live in tensor-engine-knowledge (linked via "
            "`engine_recipe_ref`); base weights live in model-knowledge (linked via `base_model_slug`); never restated here."]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    for cat in cats:
        write_cat(c, cat, wave, date)
    con.close()
    print("catalog/ regenerated:", ", ".join(cat["slug"] + ".md" for cat in cats), "+ README.md")


if __name__ == "__main__":
    main()
