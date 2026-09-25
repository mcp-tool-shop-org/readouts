#!/usr/bin/env python3
"""Generate catalog/*.md from rust.db. Re-run after each wave (regen.py does it):
    python scripts/gen_catalog.py
DB-only. NEVER hand-edit catalog/*.md — every file here is regenerated from the DB.

  catalog/README.md   the index: three tiers, per-lane rollup, flagged list, legend
  catalog/<lane>.md   one page per lane: table + every recipe in full, code checks with the compiler's verdict
  catalog/engine.md   every recipe that names a place in si-rpg-engine, grouped by tier and lane
"""
import glob
import json
import os
import re
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "rust.db")
OUT = os.path.join(ROOT, "catalog")

CUR = {"solid": "✅ solid", "plausible": "▸ plausible", "shaky": "⚠ shaky", "stale": "⛔ stale", "wrong": "✗ wrong"}
COMPILE = {"pass": "✔ compiles as claimed", "fail": "✘ compiler disagrees", "none": "· no code check"}
TIERS = [("essentials", "Essentials — the Rust a builder must never get wrong"),
         ("advanced", "Advanced — the parts of the language that decide design"),
         ("si-rpg-engine", "si-rpg-engine — how Rust is and will be used in the engine"),
         ("si-jam-sessions", "si-jam-sessions — Rust for a deterministic music law (P1)")]
# Whose place an engine_note names, by tier: the music tier's notes point at si-jam-sessions' lock.
NOTE_TARGET = {"si-jam-sessions": "si-jam-sessions"}


def cell(s):
    return ("" if s is None else str(s)).replace("|", "/").replace("\n", " ").strip()


def fence_for(src: str) -> str:
    longest = max((len(m) for m in re.findall(r"`+", src or "")), default=0)
    return "`" * max(3, longest + 1)


def src_mark(v):
    return {1: "✓", 0: "✗"}.get(v, "·")


def gate_bits(raw) -> list[str]:
    """The rest of what the oracle asserted about a check (checks.gates), in words."""
    if not raw:
        return []
    g = json.loads(raw)
    out = []
    if g.get("oracle_set") and g["oracle_set"] != "engine":
        out.append(f"{g['oracle_set']} dependency set")
    if g.get("no_warnings"):
        out.append("no warnings")
    out += [f"stderr has “{s}”" for s in g.get("stderr_contains") or []]
    said = "the trap message has" if g.get("wasm_trap") else "output has"
    out += [f"{said} “{s}”" for s in g.get("stdout_contains") or []]
    if "exit_code" in g:
        out.append(f"exit code {g['exit_code']}")
    if g.get("wasm_exports"):
        out.append("exports " + ", ".join(g["wasm_exports"]))
    if g.get("wasm_absent_exports"):
        out.append("does not export " + ", ".join(g["wasm_absent_exports"]))
    if g.get("wasm_no_imports"):
        out.append("imports nothing")
    if "wasm_imports" in g:
        out.append("imports exactly " + (", ".join(g["wasm_imports"]) or "nothing"))
    call = g.get("wasm_call")
    if call:
        args = ", ".join(str(a) for a in call.get("args") or [])
        out.append(f"node calls {call.get('export')}({args})" + (", which must trap" if g.get("wasm_trap") else ""))
    return out


def check_caption(c) -> str:
    deps = json.loads(c["deps"] or "[]")
    codes = json.loads(c["error_codes"] or "[]")
    lints = json.loads(c["lints"] or "[]")
    bits = [f"`{c['expect']}`", f"edition {c['edition']}", c["target"]]
    if c["crate_type"]:
        bits.append(c["crate_type"])
    if deps:
        bits.append("deps: " + ", ".join(deps))
    if codes:
        bits.append("errors: " + ", ".join(codes))
    if lints:
        bits.append("lints: " + ", ".join(lints))
    bits += gate_bits(c["gates"] if "gates" in c.keys() else None)
    verdict = {1: "✔ oracle pass", 0: "✘ oracle FAIL"}.get(c["oracle_ok"], "· not run")
    note = f" — {cell(c['oracle_note'])}" if c["oracle_note"] and c["oracle_ok"] != 1 else ""
    return f"*Check {c['idx'] + 1}: {cell(c['label']) or 'untitled'}* · " + " · ".join(bits) + f" · **{verdict}**{note}"


def write_lane(c, cat, wave, date):
    rows = c.execute(
        "SELECT * FROM recipes WHERE category_id=? ORDER BY verified DESC, (currency='solid') DESC, name",
        (cat["id"],)).fetchall()
    ver = sum(1 for t in rows if t["verified"])
    L = [f"# {cat['name']}",
         f"_{cat['description']}_ · tier **{cat['tier']}** · wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} recipes · {ver} verified · "
         f"{sum(1 for t in rows if t['compile_status'] == 'pass')} compiler-checked.\n",
         "| Recipe | Rust | Currency | ✓ | Code | What |",
         "|--------|------|----------|---|------|------|"]
    for t in rows:
        code = {"pass": "✔", "fail": "✘"}.get(t["compile_status"], "·")
        L.append(f"| {cell(t['name'])} | {cell(t['rust_version'])} | {CUR.get(t['currency'], cell(t['currency']))} | "
                 f"{'✓' if t['verified'] else '·'} | {code} | {cell(t['what'])[:90]} |")
    L.append("\n## Detail\n")
    for t in rows:
        L.append(f"### {t['name']}")
        L.append(f"`{CUR.get(t['currency'], t['currency'] or '?')}` · {'✓ verified' if t['verified'] else '· not verified'}"
                 f" · {COMPILE.get(t['compile_status'], t['compile_status'])} · Rust {cell(t['rust_version'])}\n")
        if t["what"]:
            L.append(f"**{t['what']}**\n")
        if t["how"]:
            L.append(f"- **How:** {t['how']}")
        if t["gotchas"]:
            L.append(f"- **Gotchas:** {t['gotchas']}")
        if t["engine_note"]:
            L.append(f"- **In {NOTE_TARGET.get(cat['tier'], 'si-rpg-engine')}:** {t['engine_note']}")
        checks = c.execute("SELECT * FROM checks WHERE recipe_id=? ORDER BY idx", (t["id"],)).fetchall()
        if checks:
            # The lane page stays lean for the loadout router: one line per check. The full source of
            # every check lives on the lane's code page, loaded only when someone needs the code.
            L.append(f"- **Code checks** ([source]({cat['slug']}.code.md#{anchor(t['name'])})):")
            for ch in checks:
                L.append(f"  - {check_caption(ch)}")
        L.append("")
        if t["verify_note"]:
            L.append(f"- **Verifier ({cell(t['currency'])}):** {t['verify_note']}")
        if t["compile_note"]:
            L.append(f"- **Compiler:** {t['compile_note']}")
        srcs = c.execute("SELECT title,url,claim,year,verified FROM sources WHERE recipe_id=? ORDER BY id",
                         (t["id"],)).fetchall()
        if srcs:
            L.append("- **Sources** (✓ supported · ✗ not supported · · unchecked):")
            for s in srcs:
                year = f" ({s['year']})" if s["year"] else ""
                claim = f" — {cell(s['claim'])}" if s["claim"] else ""
                L.append(f"  - {src_mark(s['verified'])} [{cell(s['title'] or 'source')}]({s['url']}){year}{claim}")
        L.append("")
    with open(os.path.join(OUT, cat["slug"] + ".md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")


def anchor(name: str) -> str:
    """GitHub-style heading anchor for a recipe name (lowercase, punctuation dropped, spaces -> '-')."""
    a = re.sub(r"[^\w\- ]", "", (name or "").lower())
    return a.replace(" ", "-")


def write_code(c, cat, wave, date):
    """<lane>.code.md — every check's full source, grouped by recipe, with the oracle's verdict."""
    rows = c.execute("SELECT * FROM recipes WHERE category_id=? ORDER BY verified DESC, (currency='solid') DESC, name",
                     (cat["id"],)).fetchall()
    L = [f"# {cat['name']} — code checks",
         f"Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; "
         f"its verdict is on the caption. Wave {wave} · {date} · [‹ lane page]({cat['slug']}.md) · "
         f"[catalog index](README.md)\n"]
    for t in rows:
        checks = c.execute("SELECT * FROM checks WHERE recipe_id=? ORDER BY idx", (t["id"],)).fetchall()
        if not checks:
            continue
        L.append(f"## {t['name']}")
        L.append(f"**{t['what']}**\n" if t["what"] else "")
        for ch in checks:
            L.append(check_caption(ch))
            f = fence_for(ch["source"])
            L.append(f"{f}rust\n{ch['source'].rstrip()}\n{f}")
            if ch["expected_stdout"]:
                L.append(f"Expected output: `{cell(ch['expected_stdout'])[:200]}`")
            L.append("")
    with open(os.path.join(OUT, cat["slug"] + ".code.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")


def write_engine(c, cats):
    """engine.md is a small index; each tier's engine notes live on engine-<tier>.md (router-sized pages)."""
    idx = ["# si-rpg-engine notes — every recipe that names a place in the engine",
           "Generated from `rust.db`. NEVER hand-edited. [‹ catalog index](README.md)\n",
           "Each note is a recipe's `engine_note`: the file, function, pin or slice of si-rpg-engine it bears on, "
           "as of the commit its lane cites. Engine notes are the perishable part of this KB: the repository moves, "
           "so re-check a note against `main` before acting on it. Follow the lane link for evidence and code.\n",
           "| Tier | Notes | Page |", "|---|---|---|"]
    written = []
    for tier, title in TIERS:
        tier_cats = [k for k in cats if k["tier"] == tier]
        L = [f"# {NOTE_TARGET.get(tier, 'si-rpg-engine')} notes — {title}",
             f"Generated from `rust.db`. NEVER hand-edited. [‹ engine notes index](engine.md) · [catalog index](README.md)\n"]
        n = 0
        for cat in tier_cats:
            rows = c.execute("SELECT name, engine_note, verified FROM recipes WHERE category_id=? AND "
                             "COALESCE(TRIM(engine_note),'')<>'' ORDER BY name", (cat["id"],)).fetchall()
            if not rows:
                continue
            L.append(f"## [{cat['name']}]({cat['slug']}.md)\n")
            for r in rows:
                L.append(f"- {'✓' if r['verified'] else '·'} **{cell(r['name'])}** — {cell(r['engine_note'])}")
                n += 1
            L.append("")
        if not n:
            continue
        page = f"engine-{tier}.md"
        with open(os.path.join(OUT, page), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(L) + "\n")
        idx.append(f"| {title} | {n} | [{page}]({page}) |")
        written.append(page)
    with open(os.path.join(OUT, "engine.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(idx) + "\n")
    return written


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    wave = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()[0] or 0
    dr = c.execute("SELECT value FROM meta WHERE key='updated'").fetchone()
    date = dr[0] if dr else ""
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUT, exist_ok=True)

    total = c.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
    ver = c.execute("SELECT COALESCE(SUM(verified),0) FROM recipes").fetchone()[0]
    n_checks = c.execute("SELECT COUNT(*) FROM checks").fetchone()[0]
    n_pass = c.execute("SELECT COUNT(*) FROM checks WHERE oracle_ok=1").fetchone()[0]
    idx = ["# Catalog — Rust for building si-rpg-engine\n",
           f"Generated from `rust.db` · wave {wave} · {date}. NEVER hand-edited — regenerated from the DB.\n",
           f"{total} recipes · {ver} verified · {n_checks} code checks, {n_pass} passing under the pinned compiler "
           f"(rustc 1.98.1). Two independent verdicts per recipe: **currency** from an adversarial retrieval verifier "
           f"(a different model than the author, reasoning-stripped) and **compile** from the compiler itself. "
           f"`verified` needs both. The engine-facing index is [engine.md](engine.md).\n"]
    by_lane = {r["slug"]: r for r in c.execute("SELECT * FROM v_by_lane")}
    for tier, title in TIERS:
        idx += [f"## {title}\n", "| Lane | Recipes | Solid | Verified | Code ✔ | Code ✘ |", "|---|---|---|---|---|---|"]
        for cat in [k for k in cats if k["tier"] == tier]:
            r = by_lane.get(cat["slug"])
            if not r or not r["recipes"]:
                idx.append(f"| {cell(cat['name'])} | 0 | — | — | — | — |")
                continue
            idx.append(f"| [{cell(cat['name'])}]({cat['slug']}.md) | {r['recipes']} | {r['solid']} | {r['verified']} | "
                       f"{r['compiled']} | {r['compile_failed']} |")
        idx.append("")
    flagged = c.execute("SELECT * FROM v_flagged").fetchall()
    idx += ["## Flagged — needs care (never silently trusted)\n"]
    if flagged:
        idx += ["| Tier | Lane | Recipe | Currency | Code | Status | Note |", "|---|---|---|---|---|---|---|"]
        for f in flagged:
            note = f["compile_note"] if f["compile_status"] == "fail" else f["verify_note"]
            idx.append(f"| {cell(f['tier'])} | {cell(f['category'])} | {cell(f['name'])} | "
                       f"{CUR.get(f['currency'], cell(f['currency']))} | {cell(f['compile_status'])} | "
                       f"{cell(f['status'])} | {cell(note)[:110]} |")
        idx.append("")
    else:
        idx += ["_None flagged._\n"]
    idx += ["## Legend\n",
            "- **Currency** (retrieval verifier, against Rust 1.98.1 stable / edition 2024 / the pinned crates): "
            "✅ solid > ▸ plausible > ⚠ shaky > ⛔ stale > ✗ wrong.",
            "- **Code**: ✔ every check the recipe carries did what the recipe says under rustc 1.98.1 · ✘ at least one "
            "did not · · the claim is not one code can show.",
            "- **✓ verified**: the ledger (`verification/verdicts.json`) holds a confirming external verdict AND no failing "
            "code check. Never the author's own flag.",
            "- Pinned: rustc 1.98.1 (48a229cea 2026-09-01), rapier3d-f64 0.35.3 + enhanced-determinism, parry3d-f64 0.30.2. "
            "The oracle is `scripts/compile_oracle.py`."]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(idx) + "\n")

    keep = {"README.md", "engine.md"}
    lanes = codes = 0
    for cat in cats:
        if c.execute("SELECT 1 FROM recipes WHERE category_id=? LIMIT 1", (cat["id"],)).fetchone():
            write_lane(c, cat, wave, date)
            keep.add(cat["slug"] + ".md")
            lanes += 1
            if c.execute("SELECT 1 FROM checks k JOIN recipes r ON r.id=k.recipe_id WHERE r.category_id=? LIMIT 1",
                         (cat["id"],)).fetchone():
                write_code(c, cat, wave, date)
                keep.add(cat["slug"] + ".code.md")
                codes += 1
    engine_pages = write_engine(c, cats)
    keep.update(engine_pages)
    for path in glob.glob(os.path.join(OUT, "*.md")):
        if os.path.basename(path) not in keep:
            os.remove(path)
    con.close()
    print(f"catalog/ regenerated: {lanes} lane pages + {codes} code pages + engine.md with "
          f"{len(engine_pages)} tier page(s) + README.md")


if __name__ == "__main__":
    main()
