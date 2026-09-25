#!/usr/bin/env python3
"""Generate human-readable catalog/*.md from godot.db. Re-run after each wave:
    python gen_catalog.py
DB-only (no dependency on the raw swarm json). NEVER hand-edit catalog/*.md — regenerated from the DB.
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "godot.db")
OUT = os.path.join(ROOT, "catalog")

CUR = {"solid": "✅ solid", "plausible": "▸ plausible", "shaky": "⚠ shaky",
       "godot3_stale": "⛔ godot-3 stale", "wrong": "✗ wrong"}


def cell(s):
    return ("" if s is None else str(s)).replace("|", "/").replace("\n", " ").strip()


def write_cat(c, cat, wave, date):
    rows = c.execute(
        "SELECT * FROM recipes WHERE category_id=? ORDER BY (currency='solid') DESC, (currency='plausible') DESC, name",
        (cat["id"],)).fetchall()
    solid = sum(1 for t in rows if t["currency"] == "solid")
    L = [f"# {cat['name']}",
         f"_{cat['description']}_ · wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} recipes · {solid} solid.\n",
         "| Recipe | Godot | Currency | ✓ | What |",
         "|--------|-------|----------|---|------|"]
    for t in rows:
        L.append(f"| {cell(t['name'])} | {cell(t['godot_version'])} | {CUR.get(t['currency'], cell(t['currency']))} | "
                 f"{'✓' if t['verified'] else '·'} | {cell(t['what'])[:80]} |")
    L.append("\n## Detail\n")
    for t in rows:
        L.append(f"### {t['name']} · `{CUR.get(t['currency'], t['currency'] or '?')}` · Godot {cell(t['godot_version'])}")
        if t["what"]:
            L.append(f"**{t['what']}**")
        if t["how"]:
            L.append(f"- **How:** {t['how']}")
        if t["gotchas"]:
            L.append(f"- **Gotchas:** {t['gotchas']}")
        if t["verify_note"]:
            L.append(f"- **Verify ({cell(t['currency'])}):** {t['verify_note']}")
        srcs = c.execute("SELECT title,url,claim FROM sources WHERE recipe_id=? ORDER BY id", (t["id"],)).fetchall()
        if srcs:
            L.append("- **Sources:** " + " ; ".join(
                f"[{cell(s['title'] or 'source')}]({s['url']})" + (f" — {cell(s['claim'])}" if s["claim"] else "")
                for s in srcs))
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

    total = c.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
    ver = c.execute("SELECT COALESCE(SUM(verified),0) FROM recipes").fetchone()[0]
    idx = [
        "# Catalog — Godot-4 dev knowledge (architecture · grid · combat · 2.5D render · UI · tooling)\n",
        f"Generated from `godot.db` · wave {wave} · {date}. NEVER hand-edited — regenerated from the DB.\n",
        f"Current, adversarially-verified **Godot 4** practice for building a 2.5D turn-based tactical "
        f"RPG). {total} recipes · {ver} verified. Decisive axis = **Godot-4 currency** (solid → wrong); the verifier "
        f"flags Godot-3 staleness. Sibling KBs in this monorepo cover the models / engines / training / sprites.\n"]

    idx += ["## By lane\n", "| Lane | Recipes | Solid | Verified |", "|---|---|---|---|"]
    for r in c.execute("SELECT * FROM v_by_lane"):
        slug = next((cat["slug"] for cat in cats if cat["name"] == r["category"]), "")
        idx.append(f"| [{cell(r['category'])}]({slug}.md) | {r['recipes']} | {r['solid']} | {r['verified']} |")
    idx.append("")

    flagged = c.execute("SELECT * FROM v_flagged").fetchall()
    idx += ["## Flagged — needs care (not silently trusted)\n"]
    if flagged:
        idx += ["| Lane | Recipe | Currency | Note |", "|---|---|---|---|"]
        for f in flagged:
            idx.append(f"| {cell(f['category'])} | {cell(f['name'])} | {CUR.get(f['currency'], cell(f['currency']))} | "
                       f"{cell(f['verify_note'])[:90]} |")
        idx.append("")
    else:
        idx += ["_None flagged this wave — every recipe verified solid/plausible against current Godot 4.x._\n"]

    idx += ["## Lanes\n"]
    for cat in cats:
        n = c.execute("SELECT COUNT(*) FROM recipes WHERE category_id=?", (cat["id"],)).fetchone()[0]
        idx.append(f"- [{cell(cat['name'])}]({cat['slug']}.md) — {cell(cat['description'])} ({n} recipes)")
    idx += ["", "## Legend\n",
            "- **Currency** (the decisive axis): ✅ solid > ▸ plausible > ⚠ shaky > ⛔ godot-3 stale > ✗ wrong. The "
            "verifier web-checked each recipe against current Godot 4.x and flags Godot-3-isms (deprecated nodes, "
            "renamed APIs).",
            "- **✓** verified (currency solid/plausible). **Godot** = the version the recipe targets (e.g. 4.x, 4.3+).",
            "- This is a CODE/practice KB — no license/VRAM/rig-fit axes (those live in the sprites/model/engine KBs)."]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    for cat in cats:
        write_cat(c, cat, wave, date)
    con.close()
    print("catalog/ regenerated:", ", ".join(cat["slug"] + ".md" for cat in cats), "+ README.md")


if __name__ == "__main__":
    main()
