#!/usr/bin/env python3
"""Generate human-readable catalog/*.md from findings.db. Re-run after each wave:
    python gen_catalog.py
DB-only (no dependency on raw swarm json) so it always reflects current DB state.
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "findings.db")
OUT = os.path.join(ROOT, "catalog")

CONF = {"high": "●●●", "medium": "●●·", "low": "●··"}


def cell(s):
    return ("" if s is None else str(s)).replace("|", "/").replace("\n", " ").strip()


def write_cat(c, cat, wave, date):
    rows = c.execute("SELECT * FROM findings WHERE category_id=? ORDER BY status, name", (cat["id"],)).fetchall()
    lb = sum(1 for f in rows if f["status"] == "load-bearing")
    ver = sum(1 for f in rows if f["verified"])
    L = [f"# {cat['name']}",
         f"_{cat['description']}_ · wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} findings · {lb} load-bearing · {ver} verified.\n",
         "| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |",
         "|------|---------|-------|--------|------------|------|---|"]
    for f in rows:
        L.append(f"| {cell(f['kind'])} | {cell(f['name'])} | {cell(f['claim'])} | {cell(f['metric'])} | "
                 f"{cell(f['applies_to'])} | {CONF.get(f['confidence'], cell(f['confidence']))} | "
                 f"{'✓' if f['verified'] else '·'} |")
    L.append("\n## Detail\n")
    for f in rows:
        srcs = c.execute(
            "SELECT title,authors,year,identifier,url,claim,quant,finding_supported "
            "FROM finding_sources WHERE finding_id=? ORDER BY id", (f["id"],)).fetchall()
        L.append(f"### {f['name']} · `{f['status']}` · {f['kind'] or ''}")
        if f["claim"]:
            L.append(f"**{f['claim']}**")
        if f["detail"]:
            L.append(f["detail"])
        meta = []
        if f["applies_to"]:
            meta.append(f"**Applies to:** {f['applies_to']}")
        if f["metric"]:
            meta.append(f"**Metric:** {f['metric']}")
        if f["confidence"]:
            meta.append(f"**Confidence:** {f['confidence']}")
        if f["rig_relevance"] is not None:
            meta.append(f"**Rig relevance:** {f['rig_relevance']}/5")
        if meta:
            L.append("- " + " · ".join(meta))
        if f["design_implication"]:
            L.append(f"- **Design implication:** {f['design_implication']}")
        if f["verify_note"]:
            L.append(f"- **Verify:** {f['verify_note']}")
        if srcs:
            def srcfmt(s):
                label = cell(s["title"] or s["identifier"] or "source")
                tail = []
                byline = cell(f"{s['authors'] or ''} {s['year'] or ''}").strip()
                if byline:
                    tail.append(byline)
                if s["quant"]:
                    tail.append(cell(s["quant"]))
                if s["finding_supported"]:
                    tail.append(cell(s["finding_supported"]))
                extra = (" — " + "; ".join(tail)) if tail else ""
                return f"[{label}]({s['url']}){extra}"
            L.append("- **Sources:** " + " ; ".join(srcfmt(s) for s in srcs))
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

    idx = [f"# Catalog — docker-knowledge (placement + runtime-measurement)\n",
           f"Generated from `findings.db` · wave {wave} · {date}. The knowledge base behind the "
           f"**gpu-container** product — how to package, measure, and place models honestly on one GPU. "
           f"Siblings: [model-knowledge](../../model-knowledge) (the models), "
           f"[tensor-engine-knowledge](../../tensor-engine-knowledge) (the engines).\n",
           "## Load-bearing shortlist\n",
           "The findings that drive a design decision. `✓` = retrieval oracle + family-different verified.\n",
           "| Lane | Finding | Claim | Metric | ✓ |",
           "|---|---|---|---|---|"]
    for cat in cats:
        for f in c.execute("SELECT * FROM findings WHERE category_id=? AND status='load-bearing' ORDER BY name", (cat["id"],)):
            idx.append(f"| {cell(cat['name'])} | [{cell(f['name'])}]({cat['slug']}.md) | {cell(f['claim'])} | "
                       f"{cell(f['metric'])} | {'✓' if f['verified'] else ''} |")
    idx += ["", "## Lanes\n"]
    for cat in cats:
        n = c.execute("SELECT COUNT(*) FROM findings WHERE category_id=?", (cat["id"],)).fetchone()[0]
        idx.append(f"- [{cell(cat['name'])}]({cat['slug']}.md) — {cell(cat['description'])} ({n} findings)")
    idx += ["", "## Legend\n",
            "- **Kind** technique | gotcha | constraint | benchmark | method | policy.",
            "- **Conf** confidence ●●● high / ●●· medium / ●·· low.",
            "- **✓** verified this wave (retrieval-oracle existence + family-different groundedness). · = unverified lead."]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(idx) + "\n")

    for cat in cats:
        write_cat(c, cat, wave, date)
    con.close()
    print("catalog/ regenerated:", ", ".join(cat["slug"] + ".md" for cat in cats), "+ README.md")


if __name__ == "__main__":
    main()
