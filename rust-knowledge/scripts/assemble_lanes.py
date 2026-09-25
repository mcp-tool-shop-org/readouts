#!/usr/bin/env python3
"""assemble_lanes.py — the wave assembler for rust-knowledge.

Reads the per-lane research files a study-swarm wrote under
  waves/<wave-dir>/lanes/<laneSlug>.json
and works in two passes:

  --stage   lint every recipe against the wave contract (briefs/LANE-BRIEF.md) and, when clean,
            write verification/sweep-<date>/lanes/<laneSlug>.input.json for the verifiers: the
            recipes, their code checks and their citations — nothing of the research agent's packet.
            `--lane <slug>` stages one lane (lanes close at different times).
  --final   join three independent records per recipe and write waves/<wave-dir>/research-raw.json:
              - the verifier's verdict  verification/sweep-<date>/lanes/<laneSlug>.json
              - the compiler's verdict  verification/compile-<date>/<wave-dir>.json  (compile_oracle.py run)
              - the research lane itself (content + sources)
            HALT when any recipe lacks a verifier verdict, or carries checks the oracle has not run.

The research agent's own `currency` / `verify_note` are ignored on purpose: a flag a generator sets
about its own output is a restatement, not a check (shared/verdicts.py).

Slugs: every recipe's slug is slugify(name). The lint forbids two recipes anywhere in the KB whose names
normalise alike, which makes slugify collision-free, so the oracle, the verifier ledger and the loader
all key on the same string without a uniq suffix.

Usage:
  python scripts/assemble_lanes.py --wave 1 --dir wave-01-essentials --date 2026-09-25 --stage [--lane <slug>]
  python scripts/assemble_lanes.py --wave 1 --dir wave-01-essentials --date 2026-09-25 --final
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sqlite3
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "rust.db")
SCHEMA = os.path.join(ROOT, "schema.sql")
RECENCY_FLOOR = 2021
NAME_MAX = 110
CURRENCIES = {"solid", "plausible", "shaky", "stale", "wrong"}
VERDICTS = {"confirmed", "corrected", "refuted", "unfindable"}
PRIMARY_KINDS = {"docs", "reference", "book", "release-notes", "rfc", "issue", "pr", "repo", "spec"}
OLD_OK_KINDS = {"rfc", "spec"}
EXPECTS = {"compiles", "compile_fail", "runs"}
# Every key compile_oracle.run_check reads from a check (keep in step with its docstring).
CHECK_FIELDS = ("label", "edition", "target", "crate_type", "deps", "rustc_flags", "expect", "error_codes",
                "lints", "stderr_contains", "no_warnings", "stdout", "stdout_contains", "exit_code",
                "wasm_exports", "wasm_absent_exports", "wasm_no_imports", "wasm_imports", "wasm_call",
                "wasm_trap", "oracle_set", "source")


def check_view(c: dict) -> dict:
    """The keys of a check that assert something: CHECK_FIELDS minus absent, empty and false values.
    An empty wasm_imports stays, because it asserts "imports exactly nothing"."""
    return {k: c[k] for k in CHECK_FIELDS
            if c.get(k) is not None and c.get(k) is not False and c.get(k) != ""
            and (c.get(k) != [] or k == "wasm_imports")}


WAVE_TITLES = {
    1: "Essentials — the Rust a builder must never get wrong",
    2: "Advanced — the parts of the language that decide design",
    3: "si-rpg-engine — how Rust is and will be used in the engine",
    4: "si-jam-sessions — Rust for a deterministic music law (P1)",
    5: "si-jam-sessions — the signed lock's arithmetic, parser and callback, checked (P2)",
}


def slugify(s: str) -> str:  # byte-identical to compile_oracle.py
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def categories() -> dict[str, str]:
    """slug -> tier, read from schema.sql itself (the one list of lanes)."""
    con = sqlite3.connect(":memory:")
    with open(SCHEMA, encoding="utf-8") as fh:
        con.executescript(fh.read().replace("PRAGMA journal_mode = WAL;", ""))
    out = {s: t for s, t in con.execute("SELECT slug, tier FROM categories")}
    con.close()
    return out


def load_lane_files(pattern: str) -> list[dict]:
    lanes = []
    for p in sorted(glob.glob(pattern)):
        with open(p, encoding="utf-8") as fh:
            lane = json.load(fh)
        lane["_path"] = p
        lanes.append(lane)
    return lanes


def db_names(wave_no: int) -> dict[str, str]:
    """normalised name -> slug for recipes already in the DB, EXCLUDING this wave (load replaces it)."""
    if not os.path.isfile(DB):
        return {}
    con = sqlite3.connect(DB)
    try:
        rows = con.execute("SELECT r.slug, r.name FROM recipes r JOIN waves w ON w.id=r.wave_id "
                           "WHERE w.wave_number<>?", (wave_no,)).fetchall()
    except sqlite3.OperationalError:
        rows = []
    finally:
        con.close()
    return {norm(n): s for s, n in rows}


def lint(lanes: list[dict], wave_no: int, cats: dict[str, str]) -> tuple[list[str], list[str]]:
    errors, warns = [], []
    # Names must be unique across the whole KB: every wave's lane files plus the DB's other waves.
    seen: dict[str, str] = dict(db_names(wave_no))
    others = [l for l in load_lane_files(os.path.join(ROOT, "waves", "*", "lanes", "*.json"))
              if os.path.abspath(l["_path"]) not in {os.path.abspath(x["_path"]) for x in lanes}]
    for l in others:
        for r in l.get("recipes") or []:
            seen.setdefault(norm(r.get("name")), f"{l.get('laneSlug')}/{slugify(r.get('name'))}")
    for lane in lanes:
        ls = lane.get("laneSlug")
        if ls not in cats:
            errors.append(f"{lane['_path']}: unknown laneSlug {ls!r}")
            continue
        tier = cats[ls]
        recipes = lane.get("recipes") or []
        if not 6 <= len(recipes) <= 12:
            warns.append(f"{ls}: {len(recipes)} recipes (brief asks for 8-10)")
        with_checks = sum(1 for r in recipes if r.get("checks"))
        if tier in ("essentials", "advanced") and recipes and with_checks / len(recipes) < 0.7:
            warns.append(f"{ls}: {with_checks}/{len(recipes)} recipes carry checks (brief asks for >= 7 in 10)")
        for r in recipes:
            name = (r.get("name") or "").strip()
            tag = f"{ls}/{name[:60]!r}"
            if not name:
                errors.append(f"{ls}: recipe without a name")
                continue
            if len(name) > NAME_MAX:
                warns.append(f"{tag}: name is {len(name)} chars (> {NAME_MAX})")
            key = norm(name)
            if key in seen:
                errors.append(f"{tag}: name collides with {seen[key]}")
            seen[key] = f"{ls}/{slugify(name)}"
            for k in ("what", "how"):
                if not (r.get(k) or "").strip():
                    errors.append(f"{tag}: empty {k}")
            if tier in ("si-rpg-engine", "si-jam-sessions") and not (r.get("engine_note") or "").strip():
                errors.append(f"{tag}: {tier} tier requires an engine_note")
            srcs = [s for s in (r.get("sources") or []) if s.get("url")]
            distinct = {(s.get("url") or "").strip().split("#")[0].rstrip("/") for s in srcs}
            if len(distinct) < 2:
                errors.append(f"{tag}: {len(distinct)} distinct warrant source(s), need >= 2")
            if srcs and not any((s.get("kind") or "").lower() in PRIMARY_KINDS for s in srcs):
                errors.append(f"{tag}: no primary source (kinds {sorted(PRIMARY_KINDS)})")
            for s in srcs:
                y, kind = s.get("year"), (s.get("kind") or "").lower()
                if not isinstance(y, int):
                    errors.append(f"{tag}: source {s.get('url')} has no integer year")
                elif y < RECENCY_FLOOR and kind not in OLD_OK_KINDS:
                    errors.append(f"{tag}: warrant {s.get('url')} is {y} < {RECENCY_FLOOR} (move it to background_sources)")
                elif y < RECENCY_FLOOR:
                    warns.append(f"{tag}: pre-{RECENCY_FLOOR} {kind} {s.get('url')} — the verifier must see a current page confirm it")
                if s.get("retrieved") is not True:
                    errors.append(f"{tag}: source {s.get('url')} not marked retrieved")
            for i, c in enumerate(r.get("checks") or []):
                if not isinstance(c, dict) or not (c.get("source") or "").strip():
                    errors.append(f"{tag}: check #{i} has no source")
                elif c.get("expect") not in EXPECTS:
                    errors.append(f"{tag}: check #{i} expect {c.get('expect')!r} not in {sorted(EXPECTS)}")
                else:
                    # A label is a claim. When it promises silence or an import-free module, the
                    # check must carry the oracle gate that enforces it, or a regression in that
                    # half of the claim passes unseen (two verifiers found exactly this).
                    lab = (c.get("label") or "").lower()
                    if (re.search(r"\bsilent|no (diagnostic|warning|lint)|without (a |any )?(warning|diagnostic|lint)|warning-free|clean\b", lab)
                            and c.get("expect") in ("compiles", "runs") and not c.get("no_warnings")):
                        warns.append(f"{tag}: check #{i} label promises no warning but no_warnings is not set")
                    if (re.search(r"import(s)? nothing|no imports?\b|import-free|without imports", lab)
                            and (c.get("target") or "host") != "host" and not c.get("wasm_no_imports")):
                        warns.append(f"{tag}: check #{i} label promises no imports but wasm_no_imports is not set")
            r["slug"] = slugify(name)
    return errors, warns


def write_inputs(lanes: list[dict], sweep_dir: str) -> None:
    os.makedirs(sweep_dir, exist_ok=True)
    for lane in lanes:
        ls = lane["laneSlug"]
        out = {
            "bucket": ls,
            "title": lane.get("title"),
            "tier": lane.get("tier"),
            "count": len(lane.get("recipes") or []),
            "recipes": [{
                "slug": r["slug"], "name": r["name"], "what": r.get("what"), "how": r.get("how"),
                "rust_version": r.get("rust_version"), "gotchas": r.get("gotchas"),
                "engine_note": r.get("engine_note"),
                # EVERY field the oracle reads, so the verifier judges the check the oracle runs.
                # (Staging once omitted no_warnings / wasm_no_imports and two verifiers correctly
                # reported gates "missing" that the lane file had — see wave 1's verification.md.)
                "checks": [check_view(c) for c in (r.get("checks") or [])],
                "sources": [{k: s.get(k) for k in ("title", "url", "year", "kind", "identifier", "claim")}
                            for s in (r.get("sources") or []) if s.get("url")],
                "background_sources": r.get("background_sources") or [],
            } for r in (lane.get("recipes") or [])],
        }
        p = os.path.join(sweep_dir, f"{ls}.input.json")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(out, fh, indent=2, ensure_ascii=False)
        print(f"  verifier input  {os.path.relpath(p, ROOT)}  ({out['count']} recipes)")


def oracle_results(date: str, wave_dirname: str) -> tuple[dict, str | None]:
    """(slug, index) -> result, from the authoritative run; plus the rustc string."""
    p = os.path.join(ROOT, "verification", f"compile-{date}", f"{wave_dirname}.json")
    if not os.path.isfile(p):
        return {}, None
    with open(p, encoding="utf-8") as fh:
        payload = json.load(fh)
    return {(r["slug"], r["index"]): r for r in payload.get("results", [])}, payload.get("rustc")


def finalize(lanes: list[dict], sweep_dir: str, wave_no: int, date: str, wave_dir: str) -> int:
    orc, rustc = oracle_results(date, os.path.basename(wave_dir))
    missing_v, missing_o = [], []
    lanes_out = []
    tallies = {"confirmed": 0, "corrected": 0, "refuted": 0, "unfindable": 0}
    n_checks = n_fail = 0
    for lane in lanes:
        ls = lane["laneSlug"]
        vp = os.path.join(sweep_dir, f"{ls}.json")
        by_slug = {}
        lane_note = ""
        if os.path.isfile(vp):
            with open(vp, encoding="utf-8") as fh:
                vf = json.load(fh)
            lane_note = vf.get("verifier_note") or ""
            by_slug = {v["slug"]: v for v in vf.get("verdicts", []) if v.get("slug")}
        recipes_out = []
        for r in lane.get("recipes") or []:
            v = by_slug.get(r["slug"])
            if not v or v.get("verdict") not in VERDICTS:
                missing_v.append(f"{ls}/{r['slug']}")
                continue
            tallies[v["verdict"]] += 1
            cur = str(v.get("currency") or "").strip().lower()
            if cur not in CURRENCIES:
                cur = {"confirmed": "solid", "corrected": "plausible", "refuted": "wrong",
                       "unfindable": "shaky"}[v["verdict"]]
            per_src = {s.get("url"): s for s in (v.get("sources") or []) if isinstance(s, dict)}
            checks_out, ok_n = [], 0
            for i, c in enumerate(r.get("checks") or []):
                o = orc.get((r["slug"], i))
                if o is None:
                    missing_o.append(f"{ls}/{r['slug']}#{i}")
                    continue
                n_checks += 1
                ok_n += 1 if o.get("ok") else 0
                n_fail += 0 if o.get("ok") else 1
                cc = {k: c.get(k) for k in ("label", "edition", "target", "crate_type", "deps", "rustc_flags",
                                            "expect", "error_codes", "lints", "stdout", "source")}
                # Every other gate the oracle enforced travels too, so the record shows what a check
                # asserts. Until 2026-09-25 this copy stopped at `stdout`, and every no_warnings,
                # stderr_contains and wasm_* gate was enforced but invisible downstream.
                cc.update({k: v for k, v in check_view(c).items() if k not in cc})
                cc["oracle"] = {"ok": bool(o.get("ok")), "note": (o.get("note") or "")[:300], "rustc": rustc}
                checks_out.append(cc)
            n = len(r.get("checks") or [])
            if n == 0:
                cstatus, cnote = "none", "no code check (a claim code cannot show)"
            elif ok_n == n:
                cstatus, cnote = "pass", f"{n}/{n} checks pass under {rustc}"
            else:
                first = next((c["oracle"]["note"] for c in checks_out if not c["oracle"]["ok"]), "")
                cstatus, cnote = "fail", f"{ok_n}/{n} checks pass under {rustc}; first failure: {first[:200]}"
            recipes_out.append({
                "slug": r["slug"], "name": r["name"], "what": r.get("what"), "how": r.get("how"),
                "rust_version": r.get("rust_version"), "gotchas": r.get("gotchas"),
                "engine_note": r.get("engine_note") or "",
                "currency": cur, "verify_note": (v.get("verify_note") or "").strip()[:400],
                "verdict": v["verdict"], "corrections": v.get("corrections") or None,
                "compile_status": cstatus, "compile_note": cnote,
                "checks": checks_out,
                "sources": [{"title": s.get("title"), "url": s["url"], "claim": s.get("claim"),
                             "year": s.get("year"), "kind": s.get("kind"),
                             "identifier": s.get("identifier") or None,
                             "verified": (per_src.get(s["url"]) or {}).get("supported")}
                            for s in (r.get("sources") or []) if s.get("url")],
                "background_sources": r.get("background_sources") or [],
            })
        lanes_out.append({"laneSlug": ls, "title": lane.get("title") or ls, "tier": lane.get("tier"),
                          "verifier_note": lane_note, "recipes": recipes_out})
    if missing_v or missing_o:
        for m in missing_v:
            print(f"  ERROR no verifier verdict: {m}")
        for m in missing_o:
            print(f"  ERROR check not run by the oracle: {m}")
        print("HALT: every recipe needs a verifier verdict and every check an oracle result before loading")
        return 1
    n = sum(len(l["recipes"]) for l in lanes_out)
    out = {
        "wave": wave_no, "date": date,
        "title": f"Wave {wave_no} — {WAVE_TITLES.get(wave_no, '')}: {n} recipes across {len(lanes_out)} lanes",
        "domain_scope": ", ".join(l["laneSlug"] for l in lanes_out),
        "agent_count": 2 * len(lanes_out),
        "verifier_note": (f"Research: Claude Opus, one seat per lane (briefs/LANE-BRIEF.md + briefs/lanes.json). "
                          f"Verifier: Claude Sonnet, one reasoning-stripped seat per lane (briefs/VERIFIER-BRIEF.md): "
                          f"{tallies['confirmed']} confirmed, {tallies['corrected']} corrected, {tallies['refuted']} refuted, "
                          f"{tallies['unfindable']} unfindable. Compiler (non-model): {rustc} ran {n_checks} checks, "
                          f"{n_fail} failed. verified = ledger (external verdict AND compile gate)."),
        "lanes": lanes_out,
    }
    p = os.path.join(wave_dir, "research-raw.json")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {os.path.relpath(p, ROOT)} — {n} recipes; verdicts {tallies}; {n_checks} checks, {n_fail} failed")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wave", type=int, required=True)
    ap.add_argument("--dir", required=True, help="wave folder name under waves/")
    ap.add_argument("--date", required=True)
    ap.add_argument("--lane", help="stage only this lane")
    ap.add_argument("--stage", action="store_true")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--sweep", help="sweep folder under verification/ (default sweep-<date>). Two waves on one "
                                    "date that reuse lane slugs need their own, or the second overwrites the first")
    args = ap.parse_args()

    wave_dir = os.path.join(ROOT, "waves", args.dir)
    sweep_dir = os.path.join(ROOT, "verification", args.sweep or f"sweep-{args.date}", "lanes")
    pattern = os.path.join(wave_dir, "lanes", (args.lane or "*") + ".json")
    lanes = load_lane_files(pattern)
    if not lanes:
        sys.exit(f"no lane files match {pattern}")
    cats = categories()
    errors, warns = lint(lanes, args.wave, cats)
    for w in warns:
        print(f"  warn  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    n = sum(len(l.get("recipes") or []) for l in lanes)
    print(f"lanes {len(lanes)}  recipes {n}  errors {len(errors)}  warnings {len(warns)}")
    if errors:
        print("HALT: fix the lane files (or drop the offending recipes) first")
        return 1
    if args.stage:
        write_inputs(lanes, sweep_dir)
    if args.final:
        if args.lane:
            sys.exit("--final assembles the whole wave; drop --lane")
        return finalize(lanes, sweep_dir, args.wave, args.date, wave_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
