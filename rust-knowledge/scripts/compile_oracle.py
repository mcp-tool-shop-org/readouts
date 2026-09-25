#!/usr/bin/env python3
"""compile_oracle.py — the non-model verifier for rust-knowledge.

A recipe's claim about CODE is checked by the pinned compiler, not by a model. A research
agent may run this oracle on its own lane while it works (that is a generator's self-check);
the authoritative run is `run`, made by the operator over a whole wave after the research
lanes close, and its result file is what the verdict ledger reads.

Every check compiles one self-contained Rust file with `rustc +1.98.1`. A check may link a
fixed dependency set (see ORACLE_DEPS), built once by `setup` under oracle/ with the same
rapier3d-f64 0.35.3 + enhanced-determinism that si-rpg-engine's solver links. Checks never
invoke cargo, so any number of them can run at once without contending for a build lock.

A check (one entry of a recipe's `checks` list):
  {
    "label": "what this check proves (<= 100 chars)",
    "edition": "2024",                  # 2015 | 2018 | 2021 | 2024
    "target": "host",                   # host | wasm32-unknown-unknown | wasm32v1-none
    "crate_type": "bin",                # lib | bin | cdylib | test   (test = rustc --test, then run)
    "oracle_set": "engine",             # dependency set: engine (default) | jam (si-jam-sessions)
    "deps": [],                         # subset of that set's deps; engine: host only; jam: host + wasm32
    "rustc_flags": [],                  # allowlisted, see FLAG_RULES
    "expect": "runs",                   # compiles | compile_fail | runs
    "error_codes": ["E0502"],           # compile_fail: each must appear as error[CODE]
    "lints": ["static_mut_refs"],       # each must appear in a #[warn|deny|forbid(lint)] note
    "stderr_contains": [],              # substrings rustc's stderr must contain
    "no_warnings": false,               # compiles/runs: rustc must print no warning
    "stdout": "4.5",                    # runs: exact stdout after normalising line ends
    "stdout_contains": [],              # runs: substrings stdout must contain
    "exit_code": 0,                     # runs: expected status (101 = a panic)
    "wasm_exports": ["memory", "step"], # wasm: exports that must exist
    "wasm_absent_exports": ["helper"],  # wasm: exports that must NOT exist
    "wasm_no_imports": false,           # wasm: the module must import nothing
    "wasm_imports": ["env.host_fn"],    # wasm: the exact set of imports ("module.name")
    "wasm_call": {"export": "f", "args": [1.5]},   # wasm: node calls it; its result is stdout
    "wasm_trap": false,                 # wasm: the wasm_call must throw WebAssembly.RuntimeError
                                        #       (its message becomes stdout; engines word it differently)
    "source": "fn main() { ... }"
  }

Usage:
  python scripts/compile_oracle.py setup [--set engine|jam]
  python scripts/compile_oracle.py check <lane.json> [--only SUBSTR] [--json OUT]
  python scripts/compile_oracle.py run <wave-dir> [--out FILE]
  python scripts/compile_oracle.py file <snippet.rs> --expect compiles [--edition 2024] ...

Exit 0 when every check matched its expectation, 1 when any did not, 2 when the oracle
itself is broken (wrong toolchain, setup missing). A mismatch is never softened.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
KB = os.path.dirname(HERE)
ORACLE = os.path.join(KB, "oracle")
EXTERNS = os.path.join(ORACLE, "target", "externs.json")

TOOLCHAIN = "1.98.1"
REQUIRED_VERSION_PREFIX = "rustc 1.98.1 "
EDITIONS = {"2015", "2018", "2021", "2024"}
TARGETS = {"host", "wasm32-unknown-unknown", "wasm32v1-none"}
CRATE_TYPES = {"lib", "rlib", "bin", "cdylib", "staticlib", "test"}
EXPECTS = {"compiles", "compile_fail", "runs"}
# Crate names as written in `use` paths -> package names in oracle/Cargo.toml.
ORACLE_DEPS = {
    "rapier3d_f64": "rapier3d-f64", "parry3d_f64": "parry3d-f64", "serde": "serde",
    "serde_json": "serde_json", "thiserror": "thiserror", "anyhow": "anyhow", "libm": "libm",
    "bytemuck": "bytemuck", "slotmap": "slotmap", "indexmap": "indexmap", "smallvec": "smallvec",
    "arrayvec": "arrayvec", "xxhash_rust": "xxhash-rust", "proptest": "proptest",
    "wasmparser": "wasmparser",
}
# A second, separate set for the si-jam-sessions tier (wave 4), built under oracle-jam/ for the host
# AND for wasm32-unknown-unknown, so a law check can link a parser into the wasm module. A check
# selects it with "oracle_set": "jam". It never changes the engine's set, which stays the default.
ORACLE_JAM = os.path.join(KB, "oracle-jam")
JAM_DEPS = {
    "midly": "midly", "quick_xml": "quick-xml", "roxmltree": "roxmltree", "abc_parser": "abc-parser",
    "musicxml": "musicxml", "cpal": "cpal", "midir": "midir", "rtrb": "rtrb", "ringbuf": "ringbuf",
    "assert_no_alloc": "assert_no_alloc",
}
# The law's own midly configuration (si-jam-sessions Phase 0 pins alloc + strict). It lives in
# its own crate because cargo unifies features across one build: adding "strict" to the jam
# set would silently change what every wave-4 midly check measured.
ORACLE_JAM_STRICT = os.path.join(KB, "oracle-jam-strict")
JAM_STRICT_DEPS = {"midly": "midly"}
ORACLE_SETS = {
    "engine": {"dir": ORACLE, "deps": ORACLE_DEPS, "targets": ["host"]},
    "jam": {"dir": ORACLE_JAM, "deps": JAM_DEPS, "targets": ["host", "wasm32-unknown-unknown"]},
    "jam-strict": {"dir": ORACLE_JAM_STRICT, "deps": JAM_STRICT_DEPS, "targets": ["host", "wasm32-unknown-unknown"]},
}
# rustc flags a check may pass. Anything else is refused: a check proves a claim about
# stable Rust under ordinary flags, not about whatever a clever flag can make true.
FLAG_RULES = [
    re.compile(r"^-O$"),
    re.compile(r"^-C(opt-level=[0-3sz]|panic=(abort|unwind)|overflow-checks=(on|off|yes|no|true|false)"
               r"|debug-assertions=(on|off|yes|no|true|false)|lto=(fat|thin|off|on|yes|no|true|false)"
               r"|codegen-units=\d+|target-feature=[+-][A-Za-z0-9_.-]+(,[+-][A-Za-z0-9_.-]+)*"
               r"|link-arg=[-A-Za-z0-9_=.,]+|strip=(none|debuginfo|symbols)|debuginfo=[0-2])$"),
    re.compile(r"^--cfg=[A-Za-z0-9_=\"]+$"),
    re.compile(r"^-[WADF][a-z0-9_:]+$"),
]
COMPILE_TIMEOUT = 300
RUN_TIMEOUT = 20
EXE = ".exe" if os.name == "nt" else ""


def slugify(s: str) -> str:  # byte-identical to load_db.py
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def tool(name: str) -> str:
    """The rustup proxy for `name`. `+1.98.1` then pins the toolchain on every call."""
    cand = os.path.join(os.path.expanduser("~"), ".cargo", "bin", name + EXE)
    if os.path.isfile(cand):
        return cand
    found = shutil.which(name)
    if not found:
        sys.exit(f"ORACLE BROKEN: {name} not found (install rustup, then `rustup toolchain install {TOOLCHAIN}`)")
    return found


def rustc_version() -> str:
    r = subprocess.run([tool("rustc"), f"+{TOOLCHAIN}", "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    v = (r.stdout or "").strip()
    if r.returncode != 0 or not v.startswith(REQUIRED_VERSION_PREFIX):
        print(f"ORACLE BROKEN: expected {REQUIRED_VERSION_PREFIX.strip()}..., got {v or r.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return v


# ----------------------------------------------------------------------------- setup

def setup() -> int:
    """Build the dependency set once and record where each rlib landed."""
    version = rustc_version()
    cargo = tool("cargo")
    meta = subprocess.run([cargo, f"+{TOOLCHAIN}", "metadata", "--format-version", "1"],
                          cwd=ORACLE, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if meta.returncode != 0:
        print(meta.stderr, file=sys.stderr)
        return 2
    md = json.loads(meta.stdout)
    root = md["resolve"]["root"]
    node = next(n for n in md["resolve"]["nodes"] if n["id"] == root)
    direct = {d["name"]: d["pkg"] for d in node["deps"]}  # crate name (underscored) -> package id
    versions = {p["id"]: p["version"] for p in md["packages"]}

    print(f"› cargo build (oracle dependency set, {len(direct)} direct deps) — first run downloads and compiles")
    b = subprocess.run([cargo, f"+{TOOLCHAIN}", "build", "--message-format=json-render-diagnostics"],
                       cwd=ORACLE, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if b.returncode != 0:
        print(b.stderr[-4000:], file=sys.stderr)
        return 2
    rlibs: dict[str, str] = {}
    for line in b.stdout.splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("reason") != "compiler-artifact":
            continue
        pid = msg.get("package_id")
        for crate, dpid in direct.items():
            if dpid == pid:
                for f in msg.get("filenames") or []:
                    if f.endswith(".rlib"):
                        rlibs[crate] = f
    missing = sorted(set(ORACLE_DEPS) - set(rlibs))
    if missing:
        print(f"ORACLE BROKEN: no rlib recorded for {missing}", file=sys.stderr)
        return 2
    deps_dir = os.path.join(ORACLE, "target", "debug", "deps")
    out = {
        "rustc": version,
        "deps_dir": deps_dir,
        "externs": {c: rlibs[c] for c in sorted(ORACLE_DEPS)},
        "versions": {c: versions[direct[c]] for c in sorted(ORACLE_DEPS)},
        "built": dt.date.today().isoformat(),
    }
    with open(EXTERNS, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print(f"oracle ready: {version}")
    for c in sorted(ORACLE_DEPS):
        print(f"  {c:14s} {out['versions'][c]}")
    return 0


def setup_jam(name: str = "jam") -> int:
    """Build a non-engine set (jam, jam-strict) for every target it serves; record each rlib per target."""
    version = rustc_version()
    cargo = tool("cargo")
    set_dir, set_deps = ORACLE_SETS[name]["dir"], ORACLE_SETS[name]["deps"]
    meta = subprocess.run([cargo, f"+{TOOLCHAIN}", "metadata", "--format-version", "1"],
                          cwd=set_dir, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if meta.returncode != 0:
        print(meta.stderr, file=sys.stderr)
        return 2
    md = json.loads(meta.stdout)
    root = md["resolve"]["root"]
    node = next(n for n in md["resolve"]["nodes"] if n["id"] == root)
    direct = {d["name"]: d["pkg"] for d in node["deps"]}
    versions = {p["id"]: p["version"] for p in md["packages"]}
    host_deps = os.path.join(set_dir, "target", "debug", "deps")
    out = {"rustc": version, "built": dt.date.today().isoformat(), "targets": {}}
    for target in ORACLE_SETS[name]["targets"]:
        cmd = [cargo, f"+{TOOLCHAIN}", "build", "--message-format=json-render-diagnostics"]
        if target != "host":
            cmd += ["--target", target]
        print(f"› cargo build ({name} set, {target})")
        b = subprocess.run(cmd, cwd=set_dir, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if b.returncode != 0:
            print(b.stderr[-4000:], file=sys.stderr)
            return 2
        rlibs: dict[str, str] = {}
        for line in b.stdout.splitlines():
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("reason") != "compiler-artifact":
                continue
            for crate, dpid in direct.items():
                if dpid == msg.get("package_id"):
                    for f in msg.get("filenames") or []:
                        if f.endswith(".rlib"):
                            rlibs[crate] = f
        # Proc-macro crates are host artifacts even in a cross build, so a wasm check searches both.
        if target == "host":
            dirs = [host_deps]
        else:
            dirs = [os.path.join(set_dir, "target", target, "debug", "deps"), host_deps]
        out["targets"][target] = {"deps_dirs": dirs, "externs": dict(sorted(rlibs.items())),
                                  "versions": {c: versions[direct[c]] for c in sorted(rlibs)}}
    missing = sorted(set(set_deps) - set(out["targets"]["host"]["externs"]))
    if missing:
        print(f"ORACLE BROKEN: no host rlib recorded for {missing}", file=sys.stderr)
        return 2
    path = os.path.join(set_dir, "target", "externs.json")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print(f"{name} set ready: {version}")
    for target, t in out["targets"].items():
        print(f"  {target}: " + ", ".join(f"{c} {v}" for c, v in t["versions"].items()))
    return 0


def load_externs() -> dict:
    """Every built set by name, each as {rustc, versions, targets: {target: {deps_dirs, externs}}}."""
    if not os.path.isfile(EXTERNS):
        print("ORACLE BROKEN: run `python scripts/compile_oracle.py setup` first", file=sys.stderr)
        sys.exit(2)
    with open(EXTERNS, encoding="utf-8") as fh:
        e = json.load(fh)
    sets = {"engine": {"rustc": e["rustc"], "versions": e.get("versions"),
                       "targets": {"host": {"deps_dirs": [e["deps_dir"]], "externs": e["externs"]}}}}
    for name, spec in ORACLE_SETS.items():
        if name == "engine":
            continue
        built = os.path.join(spec["dir"], "target", "externs.json")
        if os.path.isfile(built):
            with open(built, encoding="utf-8") as fh:
                j = json.load(fh)
            sets[name] = {"rustc": j["rustc"], "versions": j["targets"]["host"]["versions"], "targets": j["targets"]}
    return sets


# ----------------------------------------------------------------------------- one check

def norm_flags(flags: list) -> tuple[list[str], list[str]]:
    """Join `-C x` pairs, then allowlist. Returns (accepted, refused)."""
    out, bad, i = [], [], 0
    flags = [str(f) for f in (flags or [])]
    while i < len(flags):
        f = flags[i]
        if f in ("-C", "--cfg", "-W", "-A", "-D", "-F") and i + 1 < len(flags):
            f = (f + flags[i + 1]) if f in ("-C", "-W", "-A", "-D", "-F") else f"--cfg={flags[i + 1]}"
            i += 1
        i += 1
        (out if any(r.match(f) for r in FLAG_RULES) else bad).append(f)
    return out, bad


def norm_text(s: str) -> str:
    lines = (s or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "\n".join(l.rstrip() for l in lines).strip("\n")


def redact(text: str) -> str:
    """Replace machine-local paths in recorded compiler output with placeholders.

    rustc's diagnostics name the scratch source file, and the scratch directory
    sits under the user's temp directory, so every recorded error carried the home
    directory. The records ship with the public corpus. The per-check directory
    also has a random suffix, so `<work>` keeps records identical across runs.
    """
    if not isinstance(text, str) or not text:
        return text
    for real, mark in ((tempfile.gettempdir(), "<tmp>"), (os.path.expanduser("~"), "~")):
        # A linker error quotes its command line Debug-formatted, so the path also
        # appears with every backslash doubled.
        for form in {real, real.replace("\\", "/"), real.replace("\\", "\\\\")}:
            text = re.compile(re.escape(form), re.I).sub(lambda _m: mark, text)
    return re.sub(r"<tmp>(?:\\\\|\\|/)rk-oracle-[A-Za-z0-9_]+", "<work>", text)


def redact_result(res):
    """redact() over every string in a result, recursively."""
    if isinstance(res, dict):
        return {k: redact_result(v) for k, v in res.items()}
    if isinstance(res, list):
        return [redact_result(v) for v in res]
    return redact(res)


def wasm_probe(path: str, call: dict | None) -> dict:
    """Ask node what the module exports/imports and, optionally, call one export."""
    js = r"""
const fs = require('fs');
const [p, callJson] = process.argv.slice(1);
const mod = new WebAssembly.Module(fs.readFileSync(p));
const out = { exports: WebAssembly.Module.exports(mod).map(e => e.name),
              imports: WebAssembly.Module.imports(mod).map(i => i.module + '.' + i.name) };
if (callJson && callJson !== 'null') {
  const c = JSON.parse(callJson);
  const inst = new WebAssembly.Instance(mod, {});
  const f = inst.exports[c.export];
  if (typeof f !== 'function') { out.call_error = 'no exported function ' + c.export; }
  else {
    try {
      const r = f(...(c.args || []).map(a => (typeof a === 'string' && /^-?\d+n$/.test(a)) ? BigInt(a.slice(0, -1)) : a));
      out.result = (typeof r === 'number' && Object.is(r, -0)) ? '-0' : String(r);
    } catch (e) {
      out.trap = (e instanceof WebAssembly.RuntimeError) ? ('RuntimeError: ' + e.message) : ('non-trap error: ' + e);
    }
  }
}
process.stdout.write(JSON.stringify(out));
"""
    node = shutil.which("node")
    if not node:
        return {"error": "node not found"}
    r = subprocess.run([node, "-e", js, path, json.dumps(call) if call else "null"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=RUN_TIMEOUT)
    if r.returncode != 0:
        return {"error": (r.stderr or "node failed").strip()[:400]}
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"error": "node printed no JSON"}


def run_check(chk: dict, ext: dict) -> dict:
    res = {"ok": False, "expect": chk.get("expect"), "note": ""}
    expect = chk.get("expect")
    edition = str(chk.get("edition") or "2024")
    target = chk.get("target") or "host"
    ctype = chk.get("crate_type") or ("bin" if expect == "runs" else "lib")
    deps = list(chk.get("deps") or [])
    src = chk.get("source") or ""
    res.update(edition=edition, target=target, crate_type=ctype, deps=deps)
    if chk.get("oracle_set"):
        res["oracle_set"] = chk["oracle_set"]

    problems = []
    if expect not in EXPECTS:
        problems.append(f"expect must be one of {sorted(EXPECTS)}")
    if edition not in EDITIONS:
        problems.append(f"edition {edition!r} unknown")
    if target not in TARGETS:
        problems.append(f"target {target!r} not in {sorted(TARGETS)}")
    if ctype not in CRATE_TYPES:
        problems.append(f"crate_type {ctype!r} not in {sorted(CRATE_TYPES)}")
    if not src.strip():
        problems.append("empty source")
    set_name = chk.get("oracle_set") or "engine"
    oset = ORACLE_SETS.get(set_name)
    if oset is None:
        problems.append(f"oracle set {set_name!r} unknown (sets: {sorted(ORACLE_SETS)})")
    else:
        unknown = [d for d in deps if d not in oset["deps"]]
        if unknown:
            problems.append(f"deps not in the {set_name} oracle set: {unknown} (allowed: {sorted(oset['deps'])})")
        elif deps and target not in oset["targets"]:
            problems.append(f"deps are available for {' and '.join(oset['targets'])} only")
        elif deps and set_name not in ext:
            problems.append(f"the {set_name} oracle set is not built (run `setup --set {set_name}`)")
        elif deps:
            built = ext[set_name]["targets"].get(target, {}).get("externs", {})
            absent = [d for d in deps if d not in built]
            if absent:
                problems.append(f"deps not built for {target} in the {set_name} set: {absent}")
    if expect == "runs" and target != "host" and not chk.get("wasm_call"):
        problems.append("a wasm check can only `run` through wasm_call")
    # An expected output on a check that never runs is never compared, so it would read as proof it is not.
    if expect != "runs" and any(chk.get(k) not in (None, "", []) for k in ("stdout", "stdout_contains", "exit_code")):
        problems.append("stdout, stdout_contains and exit_code are compared only when expect is `runs`")
    if "#![feature" in src and expect != "compile_fail":
        problems.append("#![feature] is nightly-only; a stable claim cannot use it (expect compile_fail E0554 to show that)")
    flags, refused = norm_flags(chk.get("rustc_flags"))
    if refused:
        problems.append(f"rustc flags outside the allowlist: {refused}")
    if problems:
        res["note"] = "MALFORMED CHECK: " + "; ".join(problems)
        return res

    work = tempfile.mkdtemp(prefix="rk-oracle-")
    try:
        src_path = os.path.join(work, "main.rs")
        with open(src_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(src)
        cmd = [tool("rustc"), f"+{TOOLCHAIN}", "--edition", edition, "--crate-name", "snippet",
               "--color", "never"]
        if ctype == "test":
            cmd.append("--test")
        else:
            cmd += ["--crate-type", ctype]
        wasm = target != "host"
        if wasm:
            cmd += ["--target", target]
        if ctype in ("bin", "test"):
            out = os.path.join(work, "snippet" + ("" if wasm else EXE))
            cmd += ["-o", out]
        else:
            out = None
            cmd += ["--out-dir", work]
        if deps:
            built = ext[set_name]["targets"][target]
            for ddir in built["deps_dirs"]:
                cmd += ["-L", f"dependency={ddir}"]
            for d in deps:
                cmd += ["--extern", f"{d}={built['externs'][d]}"]
        cmd += flags + [src_path]
        res["rustc_flags"] = flags
        try:
            r = subprocess.run(cmd, cwd=work, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=COMPILE_TIMEOUT)
        except subprocess.TimeoutExpired:
            res["note"] = f"rustc timed out after {COMPILE_TIMEOUT}s"
            return res
        stderr = r.stderr or ""
        res["returncode"] = r.returncode
        res["error_codes"] = sorted(set(re.findall(r"error\[(E\d{4})\]", stderr)))
        res["lints"] = sorted(set(re.findall(r"#!?\[(?:warn|deny|forbid)\(([A-Za-z0-9_:]+)\)\]", stderr)))
        res["stderr_head"] = stderr[:1500]
        warned = bool(re.search(r"^warning: (?!\d+ warnings? emitted)", stderr, re.M))

        misses = []
        for lint in chk.get("lints") or []:
            if lint not in res["lints"]:
                misses.append(f"lint {lint} not reported")
        for s in chk.get("stderr_contains") or []:
            if s not in stderr:
                misses.append(f"stderr lacks {s!r}")

        if expect == "compile_fail":
            if r.returncode == 0:
                misses.insert(0, "compiled, but the recipe says it must fail")
            for code in chk.get("error_codes") or []:
                if code not in res["error_codes"]:
                    misses.append(f"{code} not reported (got {res['error_codes'] or 'none'})")
            res["ok"] = not misses
            res["note"] = "; ".join(misses) or "failed as expected"
            return res

        if r.returncode != 0:
            first = next((l for l in stderr.splitlines() if l.startswith("error")), "rustc failed")
            res["note"] = f"did not compile: {first[:200]}"
            return res
        if chk.get("no_warnings") and warned:
            misses.append("rustc printed a warning")

        if wasm:
            wasm_file = out or next(iter(glob.glob(os.path.join(work, "*.wasm"))), None)
            if not wasm_file or not os.path.isfile(wasm_file):
                misses.append("no .wasm produced")
            else:
                res["wasm_bytes"] = os.path.getsize(wasm_file)
                probe = wasm_probe(wasm_file, chk.get("wasm_call"))
                if probe.get("error"):
                    misses.append(f"node: {probe['error']}")
                else:
                    res["wasm_exports"] = probe.get("exports")
                    res["wasm_imports"] = probe.get("imports")
                    for e in chk.get("wasm_exports") or []:
                        if e not in (probe.get("exports") or []):
                            misses.append(f"export {e!r} missing")
                    for e in chk.get("wasm_absent_exports") or []:
                        if e in (probe.get("exports") or []):
                            misses.append(f"export {e!r} present but must be absent")
                    if chk.get("wasm_no_imports") and probe.get("imports"):
                        misses.append(f"module imports {probe['imports']}")
                    if chk.get("wasm_imports") is not None and \
                            sorted(chk["wasm_imports"]) != sorted(probe.get("imports") or []):
                        misses.append(f"imports {probe.get('imports')} != expected {chk['wasm_imports']}")
                    if chk.get("wasm_call"):
                        if probe.get("call_error"):
                            misses.append(probe["call_error"])
                        elif chk.get("wasm_trap"):
                            trap = probe.get("trap")
                            res["stdout"] = trap or ""
                            if not trap or not trap.startswith("RuntimeError"):
                                misses.append(f"expected a WebAssembly trap, got {trap or 'a normal return ' + repr(probe.get('result'))}")
                            for s in chk.get("stdout_contains") or []:
                                if s not in (trap or ""):
                                    misses.append(f"trap message lacks {s!r}")
                        elif probe.get("trap"):
                            misses.append(f"call trapped: {probe['trap']}")
                        else:
                            got = probe.get("result", "")
                            res["stdout"] = got
                            if expect == "runs" and "stdout" in chk and norm_text(got) != norm_text(str(chk["stdout"])):
                                misses.append(f"wasm_call returned {got!r}, expected {chk['stdout']!r}")
            res["ok"] = not misses
            res["note"] = "; ".join(misses) or ("compiled" if expect == "compiles" else "ran as expected")
            return res

        if expect == "runs":
            try:
                p = subprocess.run([out], cwd=work, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=RUN_TIMEOUT)
            except subprocess.TimeoutExpired:
                res["note"] = f"binary timed out after {RUN_TIMEOUT}s"
                return res
            res["stdout"] = (p.stdout or "")[:2000]
            res["run_stderr_head"] = (p.stderr or "")[:600]
            res["exit_code"] = p.returncode
            want_code = int(chk.get("exit_code", 0))
            if p.returncode != want_code:
                misses.append(f"exit {p.returncode}, expected {want_code}")
            if "stdout" in chk and chk["stdout"] is not None and norm_text(p.stdout) != norm_text(str(chk["stdout"])):
                misses.append(f"stdout {norm_text(p.stdout)[:160]!r} != expected {norm_text(str(chk['stdout']))[:160]!r}")
            for s in chk.get("stdout_contains") or []:
                if s not in (p.stdout or ""):
                    misses.append(f"stdout lacks {s!r}")
        res["ok"] = not misses
        res["note"] = "; ".join(misses) or ("compiled" if expect == "compiles" else "ran as expected")
        return res
    finally:
        shutil.rmtree(work, ignore_errors=True)


# ----------------------------------------------------------------------------- lanes

def lane_checks(lane: dict) -> list[tuple[str, str, int, dict]]:
    items = []
    for rec in lane.get("recipes") or []:
        name = rec.get("name") or ""
        slug = rec.get("slug") or slugify(name)
        for i, chk in enumerate(rec.get("checks") or []):
            if isinstance(chk, dict):
                items.append((slug, name, i, chk))
    return items


def check_lane_file(path: str, only: str | None, ext: dict, workers: int) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        lane = json.load(fh)
    lslug = lane.get("laneSlug") or os.path.splitext(os.path.basename(path))[0]
    items = [t for t in lane_checks(lane)
             if not only or only.lower() in (t[0] + " " + t[1]).lower()]
    results = []
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(run_check, chk, ext): (slug, name, i, chk) for slug, name, i, chk in items}
        for fut in cf.as_completed(futs):
            slug, name, i, chk = futs[fut]
            try:
                r = fut.result()
            except Exception as exc:  # a crashed check is a failed check, never a pass
                r = {"ok": False, "note": f"oracle error: {type(exc).__name__}: {exc}"}
            r = redact_result(r)
            r.update(lane=lslug, slug=slug, name=name, index=i, label=chk.get("label"))
            results.append(r)
    results.sort(key=lambda r: (r["slug"], r["index"]))
    return results


def print_results(results: list[dict]) -> int:
    fails = 0
    for r in results:
        mark = "PASS" if r.get("ok") else "FAIL"
        fails += 0 if r.get("ok") else 1
        print(f"  {mark}  {r['slug'][:70]}#{r['index']}  [{r.get('expect')}, ed{r.get('edition', '?')}, "
              f"{r.get('target', '?')}]  {r.get('note', '')[:220]}")
    n_rec = len({r["slug"] for r in results})
    print(f"{len(results)} checks over {n_rec} recipes — {len(results) - fails} pass, {fails} fail")
    return fails


def cmd_check(args) -> int:
    rustc_version()
    ext = load_externs()
    results = check_lane_file(args.lane, args.only, ext, args.workers)
    fails = print_results(results)
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(results, fh, indent=2, ensure_ascii=False)
    return 1 if fails else 0


def cmd_run(args) -> int:
    version = rustc_version()
    ext = load_externs()
    wave_dir = os.path.abspath(args.wave_dir)
    lanes = sorted(glob.glob(os.path.join(wave_dir, "lanes", "*.json")))
    if not lanes:
        print(f"no lane files under {wave_dir}/lanes", file=sys.stderr)
        return 2
    all_results = []
    for p in lanes:
        print(f"› {os.path.basename(p)}")
        res = check_lane_file(p, None, ext, args.workers)
        print_results(res)
        all_results.extend(res)
    date = args.date or dt.date.today().isoformat()
    out = args.out or os.path.join(KB, "verification", f"compile-{date}", os.path.basename(wave_dir) + ".json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    payload = {
        "oracle": "rustc (non-model verifier)", "rustc": version, "toolchain": TOOLCHAIN,
        "deps": ext["engine"].get("versions"),
        "deps_by_set": {k: v.get("versions") for k, v in ext.items()}, "date": date, "wave_dir": os.path.relpath(wave_dir, KB).replace("\\", "/"),
        "checks": len(all_results), "failed": sum(1 for r in all_results if not r.get("ok")),
        "results": all_results,
    }
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    try:
        shown = os.path.relpath(out, KB)
    except ValueError:  # --out on another drive (Windows): relpath cannot span drives
        shown = out
    print(f"\nwrote {shown} — {payload['checks']} checks, {payload['failed']} failed")
    return 1 if payload["failed"] else 0


def cmd_file(args) -> int:
    rustc_version()
    ext = load_externs()
    with open(args.snippet, encoding="utf-8") as fh:
        src = fh.read()
    chk = {"source": src, "expect": args.expect, "edition": args.edition, "target": args.target,
           "crate_type": args.crate_type, "deps": [d for d in (args.deps or "").split(",") if d],
           "error_codes": [c for c in (args.error_codes or "").split(",") if c],
           "lints": [c for c in (args.lints or "").split(",") if c],
           "rustc_flags": args.flag or []}
    if args.oracle:
        chk["oracle_set"] = args.oracle
    if args.stdout is not None:
        chk["stdout"] = args.stdout
    r = redact_result(run_check(chk, ext))
    print(json.dumps({k: v for k, v in r.items() if k != "stderr_head"}, indent=2))
    if not r["ok"] and r.get("stderr_head"):
        print(r["stderr_head"])
    return 0 if r["ok"] else 1


def cmd_redact(args) -> int:
    """Apply redact() to result records written before the oracle redacted them."""
    changed = 0
    for path in args.files:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        clean = redact_result(data)
        if clean != data:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(clean, fh, indent=2, ensure_ascii=False)
            changed += 1
            print(f"redacted {path}")
    print(f"{changed} of {len(args.files)} file(s) changed")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    st = sub.add_parser("setup")
    st.add_argument("--set", default="engine", choices=sorted(ORACLE_SETS))
    c = sub.add_parser("check")
    c.add_argument("lane")
    c.add_argument("--only")
    c.add_argument("--json")
    c.add_argument("--workers", type=int, default=4)
    r = sub.add_parser("run")
    r.add_argument("wave_dir")
    r.add_argument("--out")
    r.add_argument("--date")
    r.add_argument("--workers", type=int, default=6)
    f = sub.add_parser("file")
    f.add_argument("snippet")
    f.add_argument("--expect", required=True, choices=sorted(EXPECTS))
    f.add_argument("--edition", default="2024")
    f.add_argument("--target", default="host")
    f.add_argument("--crate-type", dest="crate_type", default=None)
    f.add_argument("--deps")
    f.add_argument("--error-codes", dest="error_codes")
    f.add_argument("--lints")
    f.add_argument("--stdout")
    f.add_argument("--flag", action="append")
    f.add_argument("--oracle", default=None, choices=sorted(ORACLE_SETS))
    rd = sub.add_parser("redact", help="strip machine-local paths from existing result files")
    rd.add_argument("files", nargs="+")
    args = ap.parse_args()
    if args.cmd == "redact":
        return cmd_redact(args)
    if args.cmd == "setup":
        name = getattr(args, "set", "engine")
        return setup() if name == "engine" else setup_jam(name)
    if args.cmd == "check":
        return cmd_check(args)
    if args.cmd == "run":
        return cmd_run(args)
    return cmd_file(args)


if __name__ == "__main__":
    sys.exit(main())
