#!/usr/bin/env python3
"""Generate the ai-loadout index at .claude/loadout/index.json over the catalog, from rust.db.

Progressive disclosure: one small `core` entry (the catalog index) + one `domain` entry per lane
(keyword-routed, loaded only when a task matches) + the engine-notes page + the wave dispatch and
verification docs (domain) + raw json (manual). Re-run after each wave (regen.py does).
QA: ai-loadout validate .claude/loadout/index.json
"""
import glob as _glob
import json
import os
import re
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "rust.db")
OUTDIR = os.path.join(ROOT, ".claude", "loadout")

KW = {
    "ownership-borrowing": ["ownership", "borrow", "borrowing", "borrowck", "move", "lifetime", "elision", "reborrow", "e0502", "e0499", "e0382", "e0505", "e0597", "split_at_mut", "mem::take"],
    "types-patterns": ["struct", "enum", "match", "pattern", "let-else", "let-chains", "newtype", "option", "result", "exhaustive", "tryfrom", "cast"],
    "traits-generics": ["trait", "generic", "generics", "impl", "dyn", "derive", "partialeq", "partialord", "total_cmp", "ops", "orphan", "iterator", "monomorphization"],
    "errors-panics": ["error", "errors", "result", "panic", "unwrap", "thiserror", "anyhow", "overflow", "checked", "wrapping", "saturating", "abort"],
    "collections-iterators": ["vec", "hashmap", "btreemap", "collection", "iterator", "iter", "closure", "sort", "sort_unstable", "fold", "sum", "vecdeque"],
    "cargo-modules": ["cargo", "crate", "module", "mod", "feature", "features", "profile", "edition", "cargo.lock", "toolchain", "rustflags", "workspace", "msrv", "resolver"],
    "testing-tooling": ["test", "tests", "testing", "clippy", "rustfmt", "proptest", "nextest", "doctest", "miri", "mutants", "cargo-deny", "lint", "lints"],
    "traits-advanced": ["associated", "gat", "dyn-compatible", "object-safety", "coherence", "blanket", "phantomdata", "variance", "hrtb", "upcasting", "rpitit", "use<>", "typestate", "sealed"],
    "memory-layout": ["box", "rc", "arc", "refcell", "cell", "lazylock", "oncelock", "layout", "repr", "repr(c)", "niche", "pin", "arena", "slotmap", "drop", "allocator"],
    "unsafe-ffi": ["unsafe", "ub", "undefined", "ffi", "extern", "static", "static_mut_refs", "raw", "no_mangle", "c-unwind", "miri", "aliasing", "provenance", "cbindgen"],
    "concurrency-async": ["thread", "threads", "send", "sync", "mutex", "atomic", "ordering", "rayon", "async", "await", "future", "tokio", "channel", "parallel"],
    "macros-const": ["macro", "macro_rules", "proc-macro", "derive", "build.rs", "cfg", "check-cfg", "const", "const-fn", "const-generics", "compile-time", "static-assert"],
    "performance": ["performance", "perf", "profile", "profiling", "benchmark", "criterion", "lto", "codegen-units", "inline", "bounds-check", "flamegraph", "simd", "allocation"],
    "rust-currency": ["edition", "2024", "release", "stabilized", "1.85", "1.88", "1.98", "migration", "cargo-fix", "new", "changed", "deprecated"],
    "wasm-raw-abi": ["wasm", "webassembly", "wasm32", "cdylib", "export", "no_mangle", "memory", "linear-memory", "trap", "wasm32v1-none", "bindgen", "float64array"],
    "float-determinism": ["float", "f64", "determinism", "deterministic", "ieee", "fma", "mul_add", "libm", "nan", "signed-zero", "subnormal", "total_cmp", "hash", "cross-platform"],
    "rapier-core": ["rapier", "rapier3d", "physics", "pipeline", "step", "integrationparameters", "island", "sleep", "rigidbody", "collider", "events", "enhanced-determinism"],
    "restore-internals": ["restore", "snapshot", "warmstart", "warm-start", "solver_restore", "t2", "manifold", "contact", "broad-phase", "bvh", "serde", "activation"],
    "rapier-shapes-kcc": ["parry", "shape", "trimesh", "mesh", "convex", "hull", "vhacd", "heightfield", "character", "controller", "kcc", "autostep", "raycast"],
    "binary-and-limits": ["lint", "memory.grow", "relaxed-simd", "opcode", "t3", "t4", "ccd", "tunnelling", "tunneling", "slope", "snap", "autostep", "allocator", "initial-memory"],
    "sim-architecture": ["simulation", "timestep", "replay", "rollback", "ggrs", "snapshot", "hash", "fnv", "xxh3", "canonical", "encoding", "handle", "ecs", "golden"],
    "host-embedding": ["host", "godot", "gdext", "gdextension", "unreal", "wasmtime", "wasmer", "wamr", "embed", "binding", "c-abi", "component-model", "wit"],
    "ci-reproducible-builds": ["ci", "reproducible", "digest", "remap-path-prefix", "trim-paths", "rust-cache", "locked", "arm64", "cargo-deny", "cargo-vet", "supply-chain", "bump"],
    "midi-notation-ingest": ["midi", "smf", "midly", "musicxml", "quick-xml", "roxmltree", "abc", "score", "notation", "ppq", "tempo", "si-jam-sessions"],
    "integer-time": ["tick", "ticks", "ppq", "tempo", "tempo-map", "sample", "samples", "microseconds", "u128", "rounding", "time-signature", "bar", "beat"],
    "host-audio-and-midi": ["audio", "cpal", "wasapi", "midir", "midi-input", "latency", "xrun", "callback", "rtrb", "ringbuf", "assert_no_alloc", "oscillator"],
    "crate-licences": ["licence", "license", "licenses", "cargo-deny", "cargo-about", "mpl", "copyleft", "attribution", "spdx", "mit", "apache", "notice"],
}
STOP = {"the", "and", "with", "for", "via", "from", "into", "use", "using", "that", "not", "are", "its", "your",
        "when", "than", "never", "every", "one", "two", "this", "what", "how"}


def est(path):
    if not os.path.exists(path):
        return 0, 0
    txt = open(path, encoding="utf-8").read()
    return max(0, len(txt) // 4), txt.count("\n") + 1


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    dr = c.execute("SELECT value FROM meta WHERE key='updated'").fetchone()
    date = dr[0] if dr else "2026-09-25"
    wave = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()[0] or 0
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUTDIR, exist_ok=True)
    entries = []

    t, l = est(os.path.join(ROOT, "catalog", "README.md"))
    entries.append({"id": "catalog-index", "path": "catalog/README.md",
                    "keywords": ["rust", "cargo", "rustc", "si-rpg-engine", "solver", "catalog", "wasm", "rapier"],
                    "patterns": [], "priority": "core",
                    "summary": "Rust KB index: three tiers, per-lane rollup, flagged list; drill into a lane for recipes.",
                    "triggers": {"task": True, "plan": True, "edit": True}, "tokens_est": t, "lines": l})

    for cat in cats:
        full = os.path.join(ROOT, "catalog", cat["slug"] + ".md")
        if not os.path.exists(full):
            continue
        n = c.execute("SELECT COUNT(*) FROM recipes WHERE category_id=?", (cat["id"],)).fetchone()[0]
        t, l = est(full)
        kw = list(KW.get(cat["slug"], []))
        for sl, wh in c.execute("SELECT slug, COALESCE(what,'') FROM recipes WHERE category_id=?", (cat["id"],)):
            for src in (sl, wh):
                for w in re.split(r"[^a-z0-9_.]+", (src or "").lower()):
                    w = w.strip(".")
                    if len(w) > 2 and w not in kw and w not in STOP:
                        kw.append(w)
        entries.append({"id": cat["slug"], "path": f"catalog/{cat['slug']}.md", "keywords": kw[:60],
                        "patterns": KW.get(cat["slug"], [])[:4], "priority": "domain",
                        "summary": f"[{cat['tier']}] {cat['name']}: {n} recipes. {cat['description']}"[:120],
                        "triggers": {"task": True, "plan": True, "edit": True}, "tokens_est": t, "lines": l})

    # Code pages: the full source of every compiler check, one page per lane. Manual on purpose —
    # an agent drills in from the lane page's "source" link when it needs the code, never by default.
    for cat in cats:
        code = os.path.join(ROOT, "catalog", cat["slug"] + ".code.md")
        if not os.path.exists(code):
            continue
        t, l = est(code)
        entries.append({"id": f"{cat['slug']}-code", "path": f"catalog/{cat['slug']}.code.md",
                        "keywords": KW.get(cat["slug"], [])[:8] + ["code", "example", "check", "source", "snippet"],
                        "patterns": [], "priority": "manual",
                        "summary": f"{cat['name']}: full source of every compiler check (rustc 1.98.1 verdict on each)."[:120],
                        "triggers": {"task": False, "plan": False, "edit": False}, "tokens_est": t, "lines": l})

    eng_kw = ["si-rpg-engine", "solver", "rapier_law", "lib.rs", "build.mjs", "flags.md",
              "t1", "t2", "t3", "t4", "t5", "restore", "lint", "golden", "digest", "host"]
    eng = os.path.join(ROOT, "catalog", "engine.md")
    if os.path.exists(eng):
        t, l = est(eng)
        entries.append({"id": "engine-notes", "path": "catalog/engine.md", "keywords": eng_kw,
                        "patterns": ["si-rpg-engine", "solver/"], "priority": "domain",
                        "summary": "Index of engine notes by tier: which recipes name a file, function, pin or slice.",
                        "triggers": {"task": True, "plan": True, "edit": True}, "tokens_est": t, "lines": l})
    for tier in ("essentials", "advanced", "si-rpg-engine", "si-jam-sessions"):
        page = os.path.join(ROOT, "catalog", f"engine-{tier}.md")
        if not os.path.exists(page):
            continue
        t, l = est(page)
        # The music tier's notes point at si-jam-sessions' lock, not at si-rpg-engine.
        owner = "si-jam-sessions" if tier == "si-jam-sessions" else "si-rpg-engine"
        own_tier = tier in ("si-rpg-engine", "si-jam-sessions")
        kw = (["si-jam-sessions", "jam", "music", "law", "lock", "ppq", "midi", "audio"] if owner == "si-jam-sessions"
              else eng_kw) + [tier]
        entries.append({"id": f"engine-notes-{tier}", "path": f"catalog/engine-{tier}.md",
                        "keywords": kw, "patterns": [owner],
                        "priority": "domain" if own_tier else "manual",
                        "summary": f"Notes from the {tier} tier: where each recipe touches {owner}."[:120],
                        "triggers": {"task": own_tier, "plan": own_tier, "edit": False},
                        "tokens_est": t, "lines": l})

    disp_kw = ["rust", "wave", "dispatch", "lane", "research", "findings", "si-rpg-engine"]
    ver_kw = ["verify", "verification", "currency", "stale", "compile", "oracle", "trust", "source", "receipt"]
    for wdir in sorted(_glob.glob(os.path.join(ROOT, "waves", "wave-*"))):
        if not os.path.isdir(wdir):
            continue
        wname = os.path.basename(wdir)
        for fname, sid, kw, pri, summ, pat in [
            ("dispatch.md", f"{wname}-dispatch", disp_kw, "domain", f"{wname}: lane findings and what they mean for the engine.", ["rust"]),
            ("verification.md", f"{wname}-verification", ver_kw, "domain", f"{wname} receipts: verifier verdicts, compiler results, gates.", ["verification"]),
            ("research-raw.json", f"{wname}-raw", ["raw", "json"], "manual", f"Raw verified {wname} output (large) — manual lookup only.", []),
        ]:
            fp = os.path.join(wdir, fname)
            if not os.path.exists(fp):
                continue
            t, l = est(fp)
            entries.append({"id": sid, "path": f"waves/{wname}/{fname}", "keywords": kw, "patterns": pat,
                            "priority": pri, "summary": summ[:120],
                            "triggers": {"task": pri != "manual", "plan": pri != "manual", "edit": False},
                            "tokens_est": t, "lines": l})

    core = sum(e["tokens_est"] for e in entries if e["priority"] == "core")
    ondemand = sum(e["tokens_est"] for e in entries if e["priority"] != "core")
    domain_toks = sorted((e["tokens_est"] for e in entries if e["priority"] == "domain"), reverse=True)
    avg = core + sum(domain_toks[:2])
    index = {"version": "1.0.0", "generated": date + "T00:00:00Z", "source": f"rust.db (wave {wave})",
             "lazyLoad": True,
             "budget": {"always_loaded_est": core, "on_demand_total_est": ondemand, "avg_task_load_est": avg,
                        "avg_task_load_observed": None},
             "entries": entries}
    with open(os.path.join(OUTDIR, "index.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)
    con.close()
    print(f"loadout index: {len(entries)} entries — core {core} tok always-on, {ondemand} tok on-demand, "
          f"~{avg} tok/typical task. -> .claude/loadout/index.json")


if __name__ == "__main__":
    main()
