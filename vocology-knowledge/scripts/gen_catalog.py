#!/usr/bin/env python3
"""Generate catalog/*.md from findings.db. NEVER hand-edit catalog/."""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "findings.db")
OUT = os.path.join(ROOT, "catalog")


def cell(s):
    return ("" if s is None else str(s)).replace("|", "/").replace("\n", " ").strip()


def write_cat(c, cat, wave, date):
    rows = c.execute(
        "SELECT * FROM findings WHERE category_id=? ORDER BY verified DESC, name",
        (cat["id"],)).fetchall()
    ver = sum(1 for f in rows if f["verified"])
    L = [f"# {cat['name']}",
         f"_{cat['description']}_ · wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} findings · {ver} verified (abstract-supported accept).\n",
         "| Finding | Authors · year | Claim | ✓ |",
         "|---------|----------------|-------|---|"]
    for f in rows:
        by = cell(f"{f['authors'] or ''} · {f['year'] or ''}").strip(" ·")
        L.append(f"| {cell(f['name'])} | {by} | {cell(f['claim'])} | "
                 f"{'✓' if f['verified'] else '·'} |")
    L.append("\n## Detail\n")
    for f in rows:
        srcs = c.execute(
            "SELECT title,authors,year,identifier,url,claim "
            "FROM finding_sources WHERE finding_id=? ORDER BY id", (f["id"],)).fetchall()
        L.append(f"### {f['name']} · `{f['status']}`")
        if f["claim"]:
            L.append(f"**{f['claim']}**")
        if f["design_implication"]:
            L.append(f"- **Implication:** {f['design_implication']}")
        if f["citation_id"]:
            L.append(f"- **Identifier:** `{f['citation_id']}`")
        if f["verify_note"]:
            L.append(f"- **Verify:** {f['verify_note']}")
        if srcs:
            bits = []
            for s in srcs:
                label = cell(s["title"] or s["identifier"] or "source")
                bits.append(f"[{label}]({s['url']})")
            L.append("- **Sources:** " + " ; ".join(bits))
        L.append("")
    with open(os.path.join(OUT, cat["slug"] + ".md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    wave = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()[0]
    dr = c.execute("SELECT value FROM meta WHERE key='updated'").fetchone()
    date = dr[0] if dr else ""
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUT, exist_ok=True)

    n_all = c.execute("SELECT COUNT(*) FROM findings").fetchone()[0]
    n_ver = c.execute("SELECT COUNT(*) FROM findings WHERE verified=1").fetchone()[0]

    idx = [
        "# Catalog — vocology-knowledge (sung-voice craft)\n",
        f"Generated from `findings.db` · wave {wave} · {date}. NEVER hand-edited — regenerated from the DB.\n",
        "Sung-voice craft for **score-lock** SVS vs lyrics-to-song generators. "
        "Not a models table — weights live in [model-knowledge](../../model-knowledge/catalog/audio.md).\n",
        f"**{n_all} findings · {n_ver}/{n_all} verified** (nine abstract-supported accepts from wave-1 verification).\n",
        "## Verified shortlist\n",
        "| Lane | Finding | Claim | ✓ |",
        "|---|---|---|---|",
    ]
    for cat in cats:
        for f in c.execute(
            "SELECT * FROM findings WHERE category_id=? AND verified=1 ORDER BY name",
            (cat["id"],)):
            idx.append(
                f"| {cell(cat['name'])} | [{cell(f['name'])}]({cat['slug']}.md) | "
                f"{cell(f['claim'])} | ✓ |")
    idx += ["", "## Lanes\n"]
    for cat in cats:
        n = c.execute("SELECT COUNT(*) FROM findings WHERE category_id=?", (cat["id"],)).fetchone()[0]
        idx.append(f"- [{cell(cat['name'])}]({cat['slug']}.md) — {cell(cat['description'])} ({n} findings)")
    idx += ["", "## Legend\n",
            "- **✓** abstract-supported accept on wave-1 verification receipt. · = directional / unverified lead.",
            "- Decisive axis: **score-lock** (MIDI + lyrics as hard constraint vs song generator)."]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(idx) + "\n")

    for cat in cats:
        write_cat(c, cat, wave, date)
    con.close()
    print("catalog/ regenerated:", ", ".join(cat["slug"] + ".md" for cat in cats), "+ README.md")


if __name__ == "__main__":
    main()
