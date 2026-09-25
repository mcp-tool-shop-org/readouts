#!/usr/bin/env python3
"""Generate human-readable catalog/*.md from engines.db. Re-run after each wave:
    python gen_catalog.py
DB-only (no dependency on raw swarm json) so it always reflects current DB state.
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "engines.db")
OUT = os.path.join(ROOT, "catalog")

COMM = {"yes": "✅ yes", "no": "⛔ no", "conditional": "⚠ cond", "unknown": "? unk"}
BW = {1: "✓", 0: "✗", None: "?"}


def cell(s):
    return ("" if s is None else str(s)).replace("|", "/").replace("\n", " ").strip()


def write_cat(c, cat, wave, date):
    rows = c.execute("SELECT * FROM engines WHERE category_id=? ORDER BY download_priority, name", (cat["id"],)).fetchall()
    rec = sum(1 for e in rows if e["status"] == "recommended")
    bw = sum(1 for e in rows if e["blackwell_ready"] == 1)
    L = [f"# {cat['name']}",
         f"_{cat['description']}_ · wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} engines · {rec} recommended · {bw} confirmed Blackwell/Windows-ready. "
         f"Narrative + install plan: [dispatch](../waves/wave-01-foundation/dispatch.md).\n",
         "| ↓ | Engine | Type | License | Comm | BW | Rig | Studio | ✓ |",
         "|---|--------|------|---------|------|----|-----|--------|---|"]
    for e in rows:
        L.append(f"| {e['download_priority'] or ''} | {cell(e['name'])} | {cell(e['engine_type'])} | "
                 f"{cell(e['license'])} | {COMM.get(e['commercial_use'], cell(e['commercial_use']))} | "
                 f"{BW.get(e['blackwell_ready'], '?')} | {cell(e['rig_fit'])} | {cell(e['studio_fit'])} | "
                 f"{'✓' if e['verified'] else '·'} |")
    L.append("\n## Detail\n")
    for e in rows:
        bf = c.execute("""SELECT p.name pn, ep.fitness f, ep.use_tag u FROM engine_purposes ep
                          JOIN purposes p ON p.id=ep.purpose_id WHERE ep.engine_id=? ORDER BY ep.fitness DESC""",
                       (e["id"],)).fetchall()
        srcs = c.execute("SELECT title, url, claim FROM sources WHERE engine_id=? ORDER BY id", (e["id"],)).fetchall()
        L.append(f"### {e['name']} · `{e['status']}` · {e['maturity_tier'] or ''}")
        if e["summary"]:
            L.append(e["summary"])
        meta = []
        for label, key in [("Dev", "developer"), ("Type", "engine_type"), ("Lang", "language"),
                           ("Version", "latest_version"), ("Released", "release_date")]:
            if e[key]:
                meta.append(f"**{label}:** {e[key]}")
        if meta:
            L.append("- " + " · ".join(meta))
        plat = []
        for label, key in [("Platforms", "platforms"), ("Accelerators", "accelerators"), ("Formats", "model_formats")]:
            if e[key]:
                plat.append(f"**{label}:** {e[key]}")
        if plat:
            L.append("- " + " · ".join(plat))
        run = [f"**Blackwell/Win-ready:** {'yes' if e['blackwell_ready']==1 else ('no' if e['blackwell_ready']==0 else 'unknown')}"]
        if e["optimization_for"]:
            run.append(f"**Optimizes for:** {e['optimization_for']}")
        if e["multi_gpu"]:
            run.append(f"**Multi-GPU:** {e['multi_gpu']}")
        run.append(f"**Fit:** rig {e['rig_fit'] if e['rig_fit'] is not None else '-'}/5 · studio {e['studio_fit'] if e['studio_fit'] is not None else '-'}/5")
        L.append("- " + " · ".join(run))
        lic = f"- **License:** {e['license'] or '?'} — commercial: **{e['commercial_use'] or '?'}**"
        if e["commercial_notes"]:
            lic += f". {e['commercial_notes']}"
        L.append(lic)
        if bf:
            L.append("- **Best for:** " + " ; ".join(
                f"{cell(b['pn'])} ({b['u'] or '-'}, fit {b['f'] if b['f'] is not None else '-'})" for b in bf))
        if e["speed_note"]:
            L.append(f"- **Speed/notes:** {e['speed_note']}")
        if e["verify_note"]:
            L.append(f"- **Verify:** {e['verify_note']}")
        if srcs:
            L.append("- **Sources:** " + " ; ".join(
                f"[{cell(s['title'] or 'source')}]({s['url']})" + (f" — {cell(s['claim'])}" if s["claim"] else "")
                for s in srcs))
        if e["repo_url"]:
            L.append(f"- **Repo:** {e['repo_url']}")
        L.append("")
    recs = c.execute("SELECT name, kind, url, body FROM config_recipes WHERE category_id=? ORDER BY kind DESC, name",
                     (cat["id"],)).fetchall()
    if recs:
        L += ["## Config recipes, tools & resources\n",
              "_The how-to-configure-and-optimize-properly layer for this lane._\n",
              "| Kind | Name | Note | URL |", "|---|---|---|---|"]
        L += [f"| {cell(r['kind'])} | {cell(r['name'])} | {cell(r['body'])} | {cell(r['url'])} |" for r in recs] + [""]
    with open(os.path.join(OUT, cat["slug"] + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    wave = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()[0]
    dr = c.execute("SELECT value FROM meta WHERE key='updated'").fetchone()
    date = dr[0] if dr else ""
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUT, exist_ok=True)

    idx = [f"# Catalog — tensor / inference / training engines\n",
           f"Generated from `engines.db` · wave {wave} · {date}. "
           f"Narrative + install plan: [wave-01 dispatch](../waves/wave-01-foundation/dispatch.md). "
           f"Verification receipt: [verification.md](../waves/wave-01-foundation/verification.md).\n",
           "The engines that **run and train** models on this rig (RTX 5090 · Blackwell · 32 GB VRAM · 64 GB RAM · Win 11). "
           "Sibling KB [model-knowledge](../../model-knowledge/catalog/README.md) catalogs the *models*; this one catalogs the *engines*.\n",
           "## Fastest install shortlist\n",
           "Top `recommended` picks per lane, install-priority order. `BW` = confirmed Blackwell/Windows-ready; `✓` = retrieval-verified this wave.\n",
           "| Lane | ↓ | Engine | License | BW | Rig | Studio | ✓ |",
           "|---|---|---|---|----|-----|--------|---|"]
    for cat in cats:
        for e in c.execute("""SELECT * FROM engines WHERE category_id=? AND status='recommended'
                              ORDER BY download_priority, name LIMIT 3""", (cat["id"],)):
            idx.append(f"| {cell(cat['name'])} | {e['download_priority']} | [{cell(e['name'])}]({cat['slug']}.md) | "
                       f"{cell(e['license'])} | {BW.get(e['blackwell_ready'], '?')} | {cell(e['rig_fit'])} | "
                       f"{cell(e['studio_fit'])} | {'✓' if e['verified'] else ''} |")
    idx += ["", "## Lanes\n"]
    for cat in cats:
        n = c.execute("SELECT COUNT(*) FROM engines WHERE category_id=?", (cat["id"],)).fetchone()[0]
        idx.append(f"- [{cell(cat['name'])}]({cat['slug']}.md) — {cell(cat['description'])} ({n} engines)")
    idx += ["",
            "## Legend\n",
            "- **↓** install priority (lower = set up first; derived from status + maturity tier).",
            "- **Comm** commercial use: ✅ yes / ⚠ conditional (read notes) / ⛔ no / ? unknown. (A permissive engine can still load a restrictively-licensed model — license is decided per-model too.)",
            "- **BW** Blackwell/Windows-ready: ✓ runs on RTX 5090 / sm_120 / CUDA 12.8+ on Windows today / ✗ no / ? unconfirmed.",
            "- **Rig** fit 0–5 for this exact rig (RTX 5090 · 32 GB VRAM · 64 GB RAM · Win 11). **Studio** fit 0–5 for the local single-user studio workload (vs datacenter-only tooling).",
            "- **✓** retrieval-verified this wave (existence + license + specs). Blank/· = unverified lead."]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    for cat in cats:
        write_cat(c, cat, wave, date)
    con.close()
    print("catalog/ regenerated:", ", ".join(cat["slug"] + ".md" for cat in cats), "+ README.md")


if __name__ == "__main__":
    main()
