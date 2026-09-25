#!/usr/bin/env python3
"""Generate human-readable catalog/*.md from models.db. Re-run after each wave:
    python gen_catalog.py
DB-only (no dependency on raw swarm json) so it always reflects current DB state.
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "models.db")
OUT = os.path.join(ROOT, "catalog")

COMM = {"yes": "✅ yes", "no": "⛔ no", "conditional": "⚠ cond", "unknown": "? unk"}


def cell(s):
    return ("" if s is None else str(s)).replace("|", "/").replace("\n", " ").strip()


def write_cat(c, cat, wave, date):
    rows = c.execute("SELECT * FROM models WHERE category_id=? ORDER BY download_priority, name", (cat["id"],)).fetchall()
    rec = sum(1 for m in rows if m["status"] == "recommended")
    safe = sum(1 for m in rows if m["commercial_use"] == "yes")
    L = [f"# {cat['name']}",
         f"_{cat['description']}_ · wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} models · {rec} recommended · {safe} commercial-safe (license=yes). "
         f"Narrative + re-download plan: [dispatch](../waves/wave-01-foundation/dispatch.md).\n",
         "| ↓ | Model | Arch | License | Comm | VRAM | Game | Mkt | ✓ |",
         "|---|-------|------|---------|------|------|------|-----|---|"]
    for m in rows:
        L.append(f"| {m['download_priority'] or ''} | {cell(m['name'])} | {cell(m['base_arch'])} | "
                 f"{cell(m['license'])} | {COMM.get(m['commercial_use'], cell(m['commercial_use']))} | "
                 f"{cell(m['min_vram_gb'])} | {cell(m['game_asset_fit'])} | {cell(m['marketing_fit'])} | "
                 f"{'✓' if m['verified'] else '·'} |")
    L.append("\n## Detail\n")
    for m in rows:
        bf = c.execute("""SELECT p.name pn, mp.fitness f, mp.use_tag u FROM model_purposes mp
                          JOIN purposes p ON p.id=mp.purpose_id WHERE mp.model_id=? ORDER BY mp.fitness DESC""",
                       (m["id"],)).fetchall()
        srcs = c.execute("SELECT title, url, claim FROM sources WHERE model_id=? ORDER BY id", (m["id"],)).fetchall()
        L.append(f"### {m['name']} · `{m['status']}` · {m['quality_tier'] or ''}")
        if m["summary"]:
            L.append(m["summary"])
        meta = []
        for label, key, suf in [("Dev", "developer", ""), ("Arch", "base_arch", ""), ("Params", "params", ""),
                                ("Released", "release_date", ""), ("Disk", "disk_size_gb", " GB")]:
            if m[key]:
                meta.append(f"**{label}:** {m[key]}{suf}")
        vram = []
        if m["min_vram_gb"]:
            vram.append(f"min {m['min_vram_gb']} GB")
        if m["recommended_vram_gb"]:
            vram.append(f"rec {m['recommended_vram_gb']} GB")
        if vram:
            meta.append("**VRAM:** " + " / ".join(vram))
        if meta:
            L.append("- " + " · ".join(meta))
        lic = f"- **License:** {m['license'] or '?'} — commercial: **{m['commercial_use'] or '?'}**"
        if m["commercial_notes"]:
            lic += f". {m['commercial_notes']}"
        L.append(lic)
        if "cloud_feasible" in m.keys() and m["cloud_feasible"]:
            cl = f"- **Cloud:** {m['cloud_feasible']}"
            if m["cloud_note"]:
                cl += f" — {m['cloud_note']}"
            L.append(cl)
        if bf:
            L.append("- **Best for:** " + " ; ".join(
                f"{cell(b['pn'])} ({b['u'] or '-'}, fit {b['f'] if b['f'] is not None else '-'})" for b in bf))
        if m["speed_note"]:
            L.append(f"- **Speed/notes:** {m['speed_note']}")
        if m["verify_note"]:
            L.append(f"- **Verify:** {m['verify_note']}")
        if srcs:
            L.append("- **Sources:** " + " ; ".join(
                f"[{cell(s['title'] or 'source')}]({s['url']})" + (f" — {cell(s['claim'])}" if s["claim"] else "")
                for s in srcs))
        if m["repo_url"]:
            L.append(f"- **Repo:** {m['repo_url']}")
        L.append("")
    if cat["slug"] == "comfy":
        nodes = c.execute("SELECT name, url, note FROM custom_nodes ORDER BY id").fetchall()
        if nodes:
            L += ["## Essential custom nodes\n", "| Node | Note | URL |", "|---|---|---|"]
            L += [f"| {cell(n['name'])} | {cell(n['note'])} | {cell(n['url'])} |" for n in nodes] + [""]
    wfs = c.execute("SELECT name, kind, url, description FROM workflows WHERE category_id=? ORDER BY kind, name",
                    (cat["id"],)).fetchall()
    if wfs:
        L += ["## Workflows & sources\n", "| Kind | Name | URL | Note |", "|---|---|---|---|"]
        L += [f"| {cell(w['kind'])} | {cell(w['name'])} | {cell(w['url'])} | {cell(w['description'])} |" for w in wfs] + [""]
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

    idx = [f"# Catalog — local generative-AI models\n",
           f"Generated from `models.db` · wave {wave} · {date}. "
           f"Narrative + re-download plan: [wave-01 dispatch](../waves/wave-01-foundation/dispatch.md). "
           f"Verification receipt: [verification.md](../waves/wave-01-foundation/verification.md).\n",
           "## Fastest commercial-safe re-download shortlist\n",
           "Top `recommended`, commercial-`yes` picks per domain, priority order. `✓` = retrieval-verified this wave.\n",
           "| Domain | ↓ | Model | License | VRAM | Game | Mkt | ✓ |",
           "|---|---|---|---|---|---|---|---|"]
    for cat in cats:
        for m in c.execute("""SELECT * FROM models WHERE category_id=? AND status='recommended'
                              AND commercial_use='yes' ORDER BY download_priority, name LIMIT 3""", (cat["id"],)):
            idx.append(f"| {cell(cat['name'])} | {m['download_priority']} | [{cell(m['name'])}]({cat['slug']}.md) | "
                       f"{cell(m['license'])} | {cell(m['min_vram_gb'])} | {cell(m['game_asset_fit'])} | "
                       f"{cell(m['marketing_fit'])} | {'✓' if m['verified'] else ''} |")
    idx += ["", "## Domains\n"]
    for cat in cats:
        n = c.execute("SELECT COUNT(*) FROM models WHERE category_id=?", (cat["id"],)).fetchone()[0]
        idx.append(f"- [{cell(cat['name'])}]({cat['slug']}.md) — {cell(cat['description'])} ({n} models)")
    idx += ["",
            "## Legend\n",
            "- **↓** download priority (lower = grab first; derived from status + quality tier).",
            "- **Cloud** (detail pages): Comfy Cloud feasibility — yes / partial / local / unknown (wave-6 axis; wave-7 entries are measured on-account).",
            "- **Comm** commercial use: ✅ yes / ⚠ conditional (revenue or regional caps — read notes) / ⛔ no (non-commercial weights) / ? unknown.",
            "- **Game / Mkt** fit 0–5 for game-asset production vs marketing/creative.",
            "- **✓** retrieval-verified this wave (existence + license + specs). Blank/· = unverified lead.",
            "- **VRAM** practical minimum in GB (quantized where noted); all picks target a 32 GB RTX 5090."]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    for cat in cats:
        write_cat(c, cat, wave, date)
    con.close()
    print("catalog/ regenerated:", ", ".join(cat["slug"] + ".md" for cat in cats), "+ README.md")


if __name__ == "__main__":
    main()
