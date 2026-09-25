#!/usr/bin/env python3
"""openrouter_lane.py — a non-Claude generator seat for one rust-knowledge lane.

Wave 4 (si-jam-sessions) is written by models outside the Claude family, reached through OpenRouter
or through Ollama Cloud (the local daemon), and checked by the same two verifiers as waves 1-3: the pinned compiler (compile_oracle.py, oracle set
"jam") and an independent Claude Sonnet retrieval verifier that sees only citations and checks.

A generator cannot browse or run tools, so this harness does both for it:

  1. GROUND   it hands the model pinned source excerpts read from the local cargo registry at the
              exact versions in oracle-jam/Cargo.lock, plus reference pages: on OpenRouter the web
              plugin searches on the first round; on Ollama, which has no search tool, the harness
              fetches a pinned list of pages (DOCS) and hashes them. Each excerpt names the URL the
              model cites.
  2. GENERATE the model returns one lane JSON (briefs/GENERATOR-BRIEF.md is the contract).
  3. ADMIT    a source tagged "opened" must be an excerpt URL or a web result the API returned;
              anything else is downgraded to "recall" and cannot be a warrant. A recipe left with
              fewer than two warrant sources is dropped (assemble_lanes' lint is the rule).
  4. COMPILE  every check runs through the oracle. Failures and lint errors go back to the model
              for a bounded number of revision rounds; a check that never passes is removed.
  5. RECEIPT  every call's model, generation id, tokens and cost, the prompt hashes and the pack
              manifest are written to waves/<wave>/receipts/<lane>.json.

The harness never verifies a claim itself: it only enforces the contract and records what happened.

Standards (0-3): PIN_PER_STEP 3 (dated model id, temperature 0, committed brief + scope + pack
manifest with SHA-256s, receipts per call); ANDON_AUTHORITY 2 (budget stop, parse failure, missing
pack file and missing key all halt; a lane that loses its checks is reported, not hidden);
NAMED_COMPENSATORS 2 (no irreversible call: it writes local files and spends metered credit, capped
by --budget); DECOMPOSE_BY_SECRETS 2 (the generator never sees verifier inputs); UNCERTAINTY_GATED
_HUMANS 2 (dropped recipes and checks are listed for the operator); EXTERNAL_VERIFIER 3 (compiler +
a different model family verify; the generator's conclusions are never inherited).

Usage:
  python scripts/openrouter_lane.py --lane midi-notation-ingest [--budget 2.0] [--rounds 3] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
KB = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import assemble_lanes  # noqa: E402  (the lane contract's lint, reused as the admission rule)

API = "https://openrouter.ai/api/v1/chat/completions"
WAVE = 4
WAVE_DIR = "wave-04-si-jam-sessions"
TIER = "si-jam-sessions"
# Requested ids and the dated snapshots they must resolve to (OpenRouter /models, 2026-09-25).
MODELS = {
    "google/gemini-3.1-pro-preview": {"dated": "google/gemini-3.1-pro-preview-20260219", "in": 2.0e-6, "out": 12.0e-6,
                                      "backend": "openrouter", "family": "google/gemini-3.1-pro-preview"},
    "x-ai/grok-4.7": {"dated": "x-ai/grok-4.7-20260916", "in": 1.6e-6, "out": 4.8e-6,
                      "backend": "openrouter", "family": "x-ai/grok-4.7"},
    # Ollama Cloud through the local daemon: billed by the plan, not per token; the digest is recorded.
    "ollama:kimi-k2.6:cloud": {"dated": "kimi-k2.6:cloud", "in": 0.0, "out": 0.0,
                               "backend": "ollama", "family": "kimi-k2.6"},
}
OLLAMA = "http://localhost:11434"
REGISTRY = sorted(glob.glob(os.path.join(os.path.expanduser("~"), ".cargo", "registry", "src", "index.crates.io-*")))
ORACLE_JAM = os.path.join(KB, "oracle-jam")

# The pinned grounding packs: (crate, version, path within the crate, max chars or None).
PACKS = {
    "midi-notation-ingest": [
        ("midly", "0.5.3", "Cargo.toml", None), ("midly", "0.5.3", "README.md", None),
        ("midly", "0.5.3", "src/lib.rs", None), ("midly", "0.5.3", "src/smf.rs", None),
        ("midly", "0.5.3", "src/primitive.rs", None), ("midly", "0.5.3", "src/event.rs", None),
        ("midly", "0.5.3", "src/error.rs", None),
        ("quick-xml", "0.42.0", "Cargo.toml", None), ("quick-xml", "0.42.0", "README.md", None),
        ("quick-xml", "0.42.0", "src/lib.rs", None), ("quick-xml", "0.42.0", "src/reader/slice_reader.rs", None),
        ("quick-xml", "0.42.0", "src/events/mod.rs", 24000),
        ("roxmltree", "0.21.1", "Cargo.toml", None), ("roxmltree", "0.21.1", "README.md", None),
        ("roxmltree", "0.21.1", "src/lib.rs", 30000),
        ("musicxml", "1.1.2", "Cargo.toml", None), ("musicxml", "1.1.2", "README.md", None),
        ("musicxml", "1.1.2", "src/lib.rs", None), ("musicxml", "1.1.2", "src/parser/mod.rs", None),
        ("musicxml", "1.1.2", "src/parser/xml_parser.rs", None),
        ("musicxml", "1.1.2", "src/elements/divisions.rs", None), ("musicxml", "1.1.2", "src/elements/time_modification.rs", None),
        ("musicxml", "1.1.2", "src/elements/backup.rs", None), ("musicxml", "1.1.2", "src/elements/forward.rs", None),
        ("musicxml", "1.1.2", "src/elements/tie.rs", None), ("musicxml", "1.1.2", "src/elements/grace.rs", None),
        ("musicxml", "1.1.2", "src/elements/repeat.rs", None), ("musicxml", "1.1.2", "src/elements/ending.rs", None),
        ("abc-parser", "0.4.0", "Cargo.toml", None), ("abc-parser", "0.4.0", "README.md", None),
        ("abc-parser", "0.4.0", "CHANGELOG.md", None), ("abc-parser", "0.4.0", "src/lib.rs", 30000),
        ("abc-parser", "0.4.0", "src/datatypes/mod.rs", None),
    ],
    "integer-time": [
        ("midly", "0.5.3", "Cargo.toml", None), ("midly", "0.5.3", "src/primitive.rs", None),
        ("midly", "0.5.3", "src/smf.rs", None), ("midly", "0.5.3", "src/event.rs", None),
    ],
    "host-audio-and-midi": [
        ("cpal", "0.18.2", "Cargo.toml", None), ("cpal", "0.18.2", "README.md", None),
        ("cpal", "0.18.2", "src/lib.rs", None), ("cpal", "0.18.2", "src/traits.rs", None),
        ("cpal", "0.18.2", "src/timestamp.rs", None), ("cpal", "0.18.2", "src/host/wasapi/mod.rs", None),
        ("cpal", "0.18.2", "src/host/wasapi/stream.rs", None), ("cpal", "0.18.2", "src/host/wasapi/device.rs", 30000),
        ("midir", "0.11.0", "Cargo.toml", None), ("midir", "0.11.0", "README.md", None),
        ("midir", "0.11.0", "src/lib.rs", None), ("midir", "0.11.0", "src/common.rs", None),
        ("midir", "0.11.0", "src/backend/winmm/mod.rs", None), ("midir", "0.11.0", "src/backend/winmm/handler.rs", None),
        ("rtrb", "0.4.0", "Cargo.toml", None), ("rtrb", "0.4.0", "README.md", None), ("rtrb", "0.4.0", "src/lib.rs", None),
        ("ringbuf", "0.5.2", "Cargo.toml", None), ("ringbuf", "0.5.2", "README.md", None),
        ("ringbuf", "0.5.2", "src/lib.rs", None), ("ringbuf", "0.5.2", "src/rb/shared.rs", None),
        ("assert_no_alloc", "1.1.2", "Cargo.toml", None), ("assert_no_alloc", "1.1.2", "README.md", None),
        ("assert_no_alloc", "1.1.2", "src/lib.rs", None),
    ],
    "crate-licences": [],  # built from the measured licence table (licence_pack) plus each crate's licence lines
}
# Reference pages the harness fetches for a backend with no search tool: (url, max chars, start marker).
DOCS = {
    "midi-notation-ingest": [],
    "integer-time": [
        ("https://doc.rust-lang.org/stable/cargo/reference/profiles.html", 5000, "overflow-checks"),
        ("https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html", 5000, "Overflow"),
        ("https://doc.rust-lang.org/stable/std/num/struct.Wrapping.html", 4000, None),
        ("https://doc.rust-lang.org/stable/std/primitive.u64.html", 5000, "pub const fn checked_mul"),
        ("https://doc.rust-lang.org/stable/std/primitive.u128.html", 3000, None),
        ("https://doc.rust-lang.org/stable/rustc/platform-support/wasm32-unknown-unknown.html", 7000, None),
    ],
    "host-audio-and-midi": [
        ("https://learn.microsoft.com/en-us/windows/win32/coreaudio/exclusive-mode-streams", 9000, None),
        ("https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-initialize", 9000, None),
        ("https://learn.microsoft.com/en-us/windows/win32/multimedia/mim-data", 4000, None),
        ("https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/nf-mmeapi-midiinopen", 6000, None),
    ],
    "crate-licences": [
        ("https://embarkstudios.github.io/cargo-deny/checks/licenses/cfg.html", 12000, None),
        ("https://embarkstudios.github.io/cargo-deny/checks/licenses/index.html", 6000, None),
        ("https://embarkstudios.github.io/cargo-about/", 6000, None),
        ("https://spdx.org/licenses/BSD-1-Clause.html", 4000, None),
        ("https://spdx.org/licenses/Unlicense.html", 4000, None),
        ("https://www.mozilla.org/en-US/MPL/2.0/FAQ/", 9000, None),
    ],
}
PACK_CHAR_CAP = 420_000


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def crate_dir(crate: str, version: str) -> str:
    for reg in REGISTRY:
        d = os.path.join(reg, f"{crate}-{version}")
        if os.path.isdir(d):
            return d
    sys.exit(f"HALT: {crate} {version} is not in the local cargo registry (run compile_oracle.py setup --set jam)")


def docs_url(crate: str, version: str, path: str) -> str:
    return f"https://docs.rs/crate/{crate}/{version}/source/{path}"


def file_pack(lane: str) -> tuple[str, list[dict]]:
    parts, manifest = [], []
    for crate, version, path, cap in PACKS[lane]:
        full = os.path.join(crate_dir(crate, version), *path.split("/"))
        if not os.path.isfile(full):
            sys.exit(f"HALT: pack file missing: {crate} {version} {path}")
        data = open(full, "rb").read()
        text = data.decode("utf-8", errors="replace")
        cut = cap is not None and len(text) > cap
        body = text[:cap] if cut else text
        url = docs_url(crate, version, path)
        head = f"=== SOURCE EXCERPT [opened] {crate} {version} {path}" + (f" (first {cap} of {len(text)} chars)" if cut else "")
        parts.append(f"{head} — cite as {url}\n{body}\n=== END {crate} {path}\n")
        manifest.append({"crate": crate, "version": version, "path": path, "url": url, "bytes": len(data),
                         "sha256": sha(data), "truncated_to": cap if cut else None})
    return "\n".join(parts), manifest


def licence_pack() -> tuple[str, list[dict]]:
    """The measured licence table of oracle-jam's graph, per target, plus each crate's licence lines."""
    cargo = os.path.join(os.path.expanduser("~"), ".cargo", "bin", "cargo")
    rows, manifest, parts = {}, [], []
    for label, triple in (("native host (x86_64-pc-windows-msvc)", "x86_64-pc-windows-msvc"),
                          ("wasm law (wasm32-unknown-unknown)", "wasm32-unknown-unknown")):
        r = subprocess.run([cargo, "+1.98.1", "metadata", "--format-version", "1", "--filter-platform", triple],
                           cwd=ORACLE_JAM, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            sys.exit(f"HALT: cargo metadata failed for {triple}: {r.stderr[-400:]}")
        md = json.loads(r.stdout)
        pk = {p["id"]: p for p in md["packages"]}
        nodes = {n["id"]: n for n in md["resolve"]["nodes"]}
        root = md["resolve"]["root"]
        # Walk from the root. A normal edge into a library reaches the shipped binary; a build edge,
        # or any edge into a proc-macro crate, is build-time only (it runs on the build machine).
        reach: dict[str, str] = {}
        stack = [(root, "binary")]
        while stack:
            nid, how = stack.pop()
            for dep in nodes[nid]["deps"]:
                kinds = {k.get("kind") for k in dep.get("dep_kinds") or []}
                if kinds <= {"dev"}:
                    continue
                pid = dep["pkg"]
                is_macro = any("proc-macro" in t.get("kind", []) for t in pk[pid].get("targets", []))
                edge = "binary" if (how == "binary" and (None in kinds) and not is_macro) else "build-time"
                if reach.get(pid) == "binary" or reach.get(pid) == edge:
                    continue
                reach[pid] = "binary" if "binary" in (reach.get(pid), edge) else edge
                stack.append((pid, reach[pid]))
        for pid, how in reach.items():
            p = pk[pid]
            key = (p["name"], p["version"])
            rows.setdefault(key, {"license": p.get("license") or f"(license-file: {p.get('license_file')})", "reach": {}})
            rows[key]["reach"][label] = how
    lines = ["=== MEASURED LICENCE TABLE [opened] — `cargo +1.98.1 metadata --filter-platform <target>` over this wave's",
             "dependency set (oracle-jam/Cargo.lock), walked from the root: 'binary' = reached through normal edges into",
             "libraries (linked into what ships); 'build-time' = only through build-dependencies or proc-macro crates.",
             "Cite each crate's own Cargo.toml URL (below) for its licence; cite this table as measured by the harness.",
             "| crate | version | licence (Cargo.toml) | native host | wasm law | licence files in the crate |",
             "|---|---|---|---|---|---|"]
    for (name, ver), row in sorted(rows.items()):
        d = crate_dir(name, ver)
        files = sorted(f for f in os.listdir(d) if re.match(r"(?i)^(licen[cs]e|copying|notice|unlicense|copyright)", f))
        lines.append(f"| {name} | {ver} | {row['license']} | {row['reach'].get('native host (x86_64-pc-windows-msvc)', '-')} | "
                     f"{row['reach'].get('wasm law (wasm32-unknown-unknown)', '-')} | {', '.join(files) or 'none'} |")
        manifest.append({"crate": name, "version": ver, "license": row["license"], "reach": row["reach"], "files": files})
    parts.append("\n".join(lines) + "\n=== END TABLE\n")
    # Each DIRECT dependency's licence lines, as an excerpt of its own Cargo.toml (the citable page).
    direct = {"midly": "0.5.3", "quick-xml": "0.42.0", "roxmltree": "0.21.1", "musicxml": "1.1.2", "abc-parser": "0.4.0",
              "cpal": "0.18.2", "midir": "0.11.0", "rtrb": "0.4.0", "ringbuf": "0.5.2", "assert_no_alloc": "1.1.2"}
    for crate, ver, fname in (("cpal", "0.18.2", "LICENSE"), ("assert_no_alloc", "1.1.2", "LICENSE"),
                              ("abc-parser", "0.4.0", "LICENSE"), ("midir", "0.11.0", "LICENSE")):
        path = os.path.join(crate_dir(crate, ver), fname)
        text = open(path, encoding="utf-8", errors="replace").read()
        url = docs_url(crate, ver, fname)
        parts.append(f"=== SOURCE EXCERPT [opened] {crate} {ver} {fname} (the licence text the crate ships) — cite as {url}\n"
                     f"{text}\n=== END {crate} {fname}\n")
        manifest.append({"crate": crate, "version": ver, "path": fname, "url": url, "sha256": sha(text.encode())})
    for crate, ver in direct.items():
        toml = open(os.path.join(crate_dir(crate, ver), "Cargo.toml"), encoding="utf-8").read()
        keep = [ln for ln in toml.splitlines() if re.match(r"^\s*(name|version|license|license-file|repository)\s*=", ln)]
        url = docs_url(crate, ver, "Cargo.toml")
        parts.append(f"=== SOURCE EXCERPT [opened] {crate} {ver} Cargo.toml (package lines) — cite as {url}\n"
                     + "\n".join(keep) + f"\n=== END {crate} Cargo.toml\n")
    return "\n".join(parts), manifest


def html_text(raw: bytes) -> str:
    s = raw.decode("utf-8", errors="replace")
    s = re.sub(r"(?is)<(script|style|nav|header|footer|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def docs_pack(lane: str) -> tuple[str, list[dict]]:
    """Fetch the lane's reference pages as text. A page that cannot be fetched is recorded, not cited."""
    parts, manifest = [], []
    for url, chars, marker in DOCS.get(lane, []):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "readouts-rust-knowledge (research lane)"})
            raw = urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:  # noqa: BLE001 — environmental; recorded in the manifest
            manifest.append({"url": url, "error": f"{type(e).__name__}: {e}"})
            continue
        text = html_text(raw)
        start = 0
        if marker:
            i = text.find(marker)
            if i < 0:
                manifest.append({"url": url, "error": f"marker {marker!r} not found"})
                continue
            start = max(0, i - 300)
        body = text[start:start + chars]
        parts.append(f"=== SOURCE EXCERPT [opened] {url} (fetched {dt.date.today().isoformat()}, {len(body)} of "
                     f"{len(text)} chars" + (f", from '{marker}'" if marker else "") + f") — cite as {url}\n"
                     f"{body}\n=== END {url}\n")
        manifest.append({"url": url, "bytes": len(raw), "sha256": sha(raw), "excerpt_sha256": sha(body.encode()),
                         "marker": marker})
    return "\n".join(parts), manifest


def ollama_digest(model: str) -> str | None:
    try:
        d = json.load(urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=30))
        return next((m.get("digest") for m in d.get("models", []) if m.get("name") == model), None)
    except Exception:  # noqa: BLE001
        return None


def call_ollama(model: str, messages: list) -> dict:
    """One chat call through the local Ollama daemon, reshaped like an OpenRouter response."""
    body = {"model": model, "messages": messages, "stream": False, "format": "json",
            "options": {"temperature": 0, "num_predict": 32000, "num_ctx": 262144}}
    data = json.dumps(body).encode("utf-8")
    last = None
    for attempt in range(3):
        req = urllib.request.Request(f"{OLLAMA}/api/chat", data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=3600) as r:
                d = json.load(r)
            if d.get("error"):
                raise RuntimeError(d["error"])
            return {"id": None, "model": d.get("model"), "provider": "ollama-cloud",
                    "choices": [{"message": {"content": (d.get("message") or {}).get("content") or "", "annotations": []}}],
                    "usage": {"prompt_tokens": d.get("prompt_eval_count"), "completion_tokens": d.get("eval_count"),
                              "cost": 0.0, "total_duration_ns": d.get("total_duration")}}
        except (urllib.error.URLError, TimeoutError, RuntimeError) as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(20 * (attempt + 1))
    raise RuntimeError(f"Ollama call failed: {last}")


def readmit(slug: str) -> int:
    """Re-apply the current admission rules to the lane file on disk (no model call), with a receipt entry."""
    wdir = os.path.join(KB, "waves", WAVE_DIR)
    out = os.path.join(wdir, "lanes", f"{slug}.json")
    lane = json.load(open(out, encoding="utf-8"))
    dropped_checks, dropped_recipes = [], []
    for r in lane.get("recipes") or []:
        kept = []
        for c in r.get("checks") or []:
            if vacuous(c):
                dropped_checks.append({"recipe": r.get("name"), "label": c.get("label"), "why": "asserts nothing"})
            else:
                kept.append(c)
        r["checks"] = kept
    admitted = []
    for r in lane.get("recipes") or []:
        errs = lint(dict(lane, recipes=[r]), out)
        if errs:
            dropped_recipes.append({"recipe": r.get("name"), "why": errs[:3]})
        else:
            admitted.append(r)
    lane["recipes"] = admitted
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(lane, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    rpath = os.path.join(wdir, "receipts", f"{slug}.json")
    rec = json.load(open(rpath, encoding="utf-8")) if os.path.isfile(rpath) else {"lane": slug}
    rec["readmitted"] = {"date": dt.date.today().isoformat(),
                         "harness_sha256": sha(open(os.path.abspath(__file__), "rb").read()),
                         "dropped_checks": dropped_checks, "dropped_recipes": dropped_recipes,
                         "final_recipes": len(admitted), "final_checks": sum(len(r.get("checks") or []) for r in admitted)}
    with open(rpath, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"readmitted {slug}: {len(admitted)} recipes kept; dropped {len(dropped_checks)} checks, "
          f"{len(dropped_recipes)} recipes")
    return 0


def scope_text(lane: str) -> tuple[str, dict]:
    d = json.load(open(os.path.join(KB, "briefs", "lanes.json"), encoding="utf-8"))
    sc = next((l for l in d["lanes"] if l["slug"] == lane), None)
    if not sc:
        sys.exit(f"HALT: lane {lane!r} has no scope in briefs/lanes.json")
    return json.dumps(sc, indent=2, ensure_ascii=False), sc


def norm_url(u: str) -> str:
    u = (u or "").strip().split("#")[0]
    return u[:-1] if u.endswith("/") else u


def parse_json(content: str) -> dict:
    """The first top-level JSON object in the reply that holds "recipes"."""
    dec, s, i, first_err = json.JSONDecoder(), content, 0, None
    while True:
        i = s.find("{", i)
        if i < 0:
            break
        try:
            obj, end = dec.raw_decode(s, i)
        except json.JSONDecodeError as e:
            first_err = first_err or e
            i += 1
            continue
        if isinstance(obj, dict) and "recipes" in obj:
            return obj
        i = end
    raise ValueError(f"no JSON object with 'recipes' in the reply ({first_err or 'none found'})")


def call(model: str, messages: list, web: bool, key: str, backend: str = "openrouter") -> dict:
    if backend == "ollama":
        return call_ollama(model, messages)
    body = {"model": model, "messages": messages, "temperature": 0, "max_tokens": 40000,
            "reasoning": {"effort": "medium"},
            "response_format": {"type": "json_object"}, "usage": {"include": True}}
    if web:
        # Pinned engine: with the default, Gemini's search never ran (prompt 27 tokens, no citations);
        # "exa" injected results and citations for both generators (probed 2026-09-25).
        body["plugins"] = [{"id": "web", "engine": "exa", "max_results": 6}]
    data = json.dumps(body).encode("utf-8")
    last = None
    for attempt in range(3):
        req = urllib.request.Request(API, data=data, headers={
            "Authorization": f"Bearer {key}", "Content-Type": "application/json",
            "X-Title": "readouts rust-knowledge (research lane)"})
        try:
            with urllib.request.urlopen(req, timeout=1200) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:400]!r}"
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(20 * (attempt + 1))
                continue
            break
        except (urllib.error.URLError, TimeoutError) as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(20 * (attempt + 1))
    raise RuntimeError(f"OpenRouter call failed: {last}")


def admit_sources(lane: dict, allowed: set[str]) -> list[dict]:
    """Downgrade an 'opened' tag the conversation cannot back; set retrieved from the tag."""
    downgraded = []
    for r in lane.get("recipes") or []:
        for s in r.get("sources") or []:
            tag = (s.get("tag") or "recall").strip().lower().strip("[]")
            if tag == "opened" and norm_url(s.get("url")) not in allowed:
                downgraded.append({"recipe": r.get("name"), "url": s.get("url")})
                tag = "recall"
            s["tag"] = tag
            s["retrieved"] = tag == "opened"
        # Only opened sources are warrants; the rest move to background.
        keep, back = [], list(r.get("background_sources") or [])
        for s in r.get("sources") or []:
            (keep if s["retrieved"] else back).append(s)
        r["sources"], r["background_sources"] = keep, back
    return downgraded


GATES = ("error_codes", "lints", "stderr_contains", "no_warnings", "stdout", "stdout_contains", "exit_code",
         "wasm_exports", "wasm_absent_exports", "wasm_no_imports", "wasm_imports", "wasm_call", "wasm_trap")


def vacuous(c: dict) -> bool:
    """A `compiles` check with no gate whose program only imports crates and defines empty functions
    proves nothing about a claim (seen in wave 4's first licence draft: `fn main() {}`)."""
    if c.get("expect") != "compiles" or any(c.get(g) not in (None, [], "", False) for g in GATES):
        return False
    src = re.sub(r"//[^\n]*", "", c.get("source") or "")
    src = re.sub(r"use\s+[\w:]+\s+as\s+_\s*;", "", src)
    src = re.sub(r"#!?\[[^\]]*\]", "", src)
    bodies = re.findall(r"\{([^{}]*)\}", src)
    return "::" not in src and all(not b.strip() for b in bodies)


def normalise(lane: dict, slug: str) -> None:
    lane["laneSlug"], lane["tier"] = slug, TIER
    for r in lane.get("recipes") or []:
        r["currency"], r["verify_note"] = None, None
        for c in r.get("checks") or []:
            c["oracle_set"] = "jam"
            c.setdefault("edition", "2024")


def lint(lane: dict, path: str) -> list[str]:
    lane = dict(lane, _path=path)
    errors, _warns = assemble_lanes.lint([lane], WAVE, assemble_lanes.categories())
    return errors


def oracle(path: str) -> list[dict]:
    out = path + ".oracle.json"
    subprocess.run([sys.executable, os.path.join(HERE, "compile_oracle.py"), "check", path, "--json", out, "--workers", "4"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
    return json.load(open(out, encoding="utf-8")) if os.path.isfile(out) else []


def feedback(rnd: int, results: list[dict], lint_errors: list[str], downgraded: list[dict], lane: dict) -> str:
    fails = [r for r in results if not r.get("ok")]
    empty = [(r.get("name"), i, c.get("label")) for r in lane.get("recipes") or []
             for i, c in enumerate(r.get("checks") or []) if c.get("_vacuous")]
    L = [f"ROUND {rnd} REVIEW. Revise only what is listed below, keep everything else as it is, and return the "
         f"complete lane JSON again (one JSON object).",
         f"Compiler (rustc 1.98.1): {len(results) - len(fails)} checks pass, {len(fails)} fail."]
    for r in fails:
        L.append(f"- Recipe \"{r.get('name')}\", check {r.get('index')} \"{r.get('label')}\": {r.get('note', '')[:500]}")
        head = (r.get("stderr_head") or "").strip()
        if head:
            L.append("  compiler stderr: " + head[:900].replace("\n", "\n  "))
        if r.get("stdout") not in (None, ""):
            L.append(f"  actual stdout: {str(r.get('stdout'))[:300]!r}")
    if empty:
        L.append("Checks that assert nothing (an empty program with no expectation), refused:")
        L += [f"- \"{n}\", check {i} \"{lab}\": remove it, or make it prove the claim" for n, i, lab in empty]
    if lint_errors:
        L.append("Contract (lint) errors:")
        L += [f"- {e}" for e in lint_errors[:40]]
    if downgraded:
        L.append("Sources you tagged opened whose URL is not among the excerpts or search results you were given "
                 "(now recall, not warrants):")
        L += [f"- \"{d['recipe']}\": {d['url']}" for d in downgraded[:40]]
    L.append("If the compiler disagrees with your claim, the claim is wrong: fix the claim or remove it. Never bend a "
             "check to match whatever happened. A recipe needs two DIFFERENT opened URLs that each state its "
             "claim. Never cite a page that does not state the claim to meet that rule: remove the recipe instead. "
             "Where code cannot show a claim (a licence, device behaviour), carry no check at all.")
    return "\n".join(L)


RECEIPT: dict = {}


def write_receipt(status: str) -> None:
    """Called on every exit, so a halted or failed lane still leaves its calls and costs on disk."""
    if not RECEIPT.get("lane"):
        return
    RECEIPT["status"] = status
    d = os.path.join(KB, "waves", WAVE_DIR, "receipts")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{RECEIPT['lane']}.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(RECEIPT, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def main() -> int:
    try:
        rc = run()
    except SystemExit as e:
        write_receipt(f"halted: {e.code}")
        raise
    except Exception as e:
        write_receipt(f"failed: {type(e).__name__}: {e}")
        raise
    return rc


def run() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--budget", type=float, default=2.0, help="USD cap for this lane")
    ap.add_argument("--rounds", type=int, default=3, help="revision rounds after the first draft")
    ap.add_argument("--dry-run", action="store_true", help="build the prompt and manifest; call nothing")
    ap.add_argument("--probe", action="store_true", help="one tiny call to confirm the pinned model id resolves")
    ap.add_argument("--readmit", action="store_true", help="re-apply admission to the lane file on disk; no model call")
    ap.add_argument("--revise", action="store_true",
                    help="start from the lane on disk plus the compiler's current objections, not a fresh draft")
    args = ap.parse_args()
    if args.readmit:
        return readmit(args.lane)

    brief = open(os.path.join(KB, "briefs", "GENERATOR-BRIEF.md"), encoding="utf-8").read()
    scope, sc = scope_text(args.lane)
    requested = sc["generator"]
    model = MODELS[requested]["dated"]
    backend = MODELS[requested]["backend"]
    pack, manifest = licence_pack() if args.lane == "crate-licences" else file_pack(args.lane)
    if backend == "ollama":
        dpack, dman = docs_pack(args.lane)
        pack, manifest = pack + "\n" + dpack, manifest + dman
    if len(pack) > PACK_CHAR_CAP:
        sys.exit(f"HALT: pack is {len(pack)} chars, over the {PACK_CHAR_CAP} cap")
    allowed = {norm_url(m["url"]) for m in manifest if m.get("url") and not m.get("error")}
    if args.lane == "crate-licences":
        allowed |= {norm_url(docs_url(m["crate"], m["version"], "Cargo.toml")) for m in manifest if m.get("crate")}
    user = (f"YOUR LANE (from briefs/lanes.json):\n{scope}\n\n"
            f"SOURCE EXCERPTS (read from the local cargo registry at the pinned versions; each is an 'opened' "
            f"source you may cite by the URL in its header):\n\n{pack}")
    messages = [{"role": "system", "content": brief}, {"role": "user", "content": user}]
    wdir = os.path.join(KB, "waves", WAVE_DIR)
    receipt = RECEIPT
    receipt.update({"lane": args.lane, "wave": WAVE, "date": dt.date.today().isoformat(), "model_requested": requested,
               "model_pinned": model, "backend": backend, "temperature": 0,
               "web_search_round_1": backend == "openrouter", "fetched_docs": backend == "ollama",
               "ollama_digest": ollama_digest(model) if backend == "ollama" else None,
               "brief_sha256": sha(brief.encode()), "scope_sha256": sha(scope.encode()),
               "user_prompt_sha256": sha(user.encode()), "pack": manifest, "pack_chars": len(pack),
               "calls": [], "rounds": [], "budget_usd": args.budget,
               "harness_sha256": sha(open(os.path.abspath(__file__), "rb").read())})
    print(f"› {args.lane}: {model}, pack {len(pack)} chars ({len(manifest)} items), budget ${args.budget}")
    if args.dry_run:
        print(user[:1500])
        RECEIPT.clear()
        return 0
    key = os.environ.get("OPENROUTER_API_KEY") if backend == "openrouter" else None
    if backend == "openrouter" and not key:
        sys.exit("HALT: OPENROUTER_API_KEY is not set")
    if args.probe:
        r = call(model, [{"role": "user", "content": 'Reply with the JSON object {"ok": true} and nothing else.'}], False, key, backend)
        print("probe:", r.get("model"), (r["choices"][0]["message"].get("content") or "")[:80], r.get("usage", {}).get("cost"))
        RECEIPT.clear()
        return 0

    spent, lane, results, downgraded, lint_errors = 0.0, None, [], [], []
    work = tempfile.mkdtemp(prefix="rk-gen-")
    draft = os.path.join(work, f"{args.lane}.json")
    # Lint as the lane's own final file, so a re-run is not a name collision with its last output.
    out = os.path.join(wdir, "lanes", f"{args.lane}.json")
    start, old_packet = 0, ""
    if args.revise:
        prior = json.load(open(out, encoding="utf-8"))
        pkt = os.path.join(wdir, f"{args.lane}.md")
        if os.path.isfile(pkt):
            old_packet = open(pkt, encoding="utf-8").read().split("\n\n", 2)[-1].strip()
        with open(draft, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(prior, fh, indent=2, ensure_ascii=False)
        prior_results = oracle(draft)
        prior_lint = lint(prior, out)
        messages.append({"role": "assistant", "content": json.dumps(prior, ensure_ascii=False)})
        messages.append({"role": "user", "content": feedback(1, prior_results, prior_lint, [], prior)})
        receipt["revised_from"] = {"lane_sha256": sha(json.dumps(prior, sort_keys=True).encode()),
                                   "failing_checks": sum(1 for r in prior_results if not r.get("ok")),
                                   "lint_errors": len(prior_lint)}
        start = 1
        print(f"  revising the lane on disk: {receipt['revised_from']['failing_checks']} failing checks, "
              f"{len(prior_lint)} lint errors")
    for rnd in range(start, args.rounds + 1):
        est_next = (len(json.dumps(messages)) / 4) * MODELS[requested]["in"] + 40000 * MODELS[requested]["out"]
        if spent + est_next > args.budget:
            print(f"  budget stop before round {rnd}: spent ${spent:.3f}, next call up to ${est_next:.3f}")
            receipt["stopped"] = f"budget before round {rnd}"
            break
        t0 = time.time()
        resp = call(model, messages, web=(rnd == 0), key=key, backend=backend)
        msg = resp["choices"][0]["message"]
        usage = resp.get("usage") or {}
        cost = usage.get("cost")
        if cost is None:
            cost = usage.get("prompt_tokens", 0) * MODELS[requested]["in"] + usage.get("completion_tokens", 0) * MODELS[requested]["out"]
        spent += float(cost)
        for a in msg.get("annotations") or []:
            u = (a.get("url_citation") or {}).get("url")
            if u:
                allowed.add(norm_url(u))
        receipt["calls"].append({"round": rnd, "id": resp.get("id"), "model": resp.get("model"),
                                 "provider": resp.get("provider"), "usage": usage, "cost_usd": cost,
                                 "seconds": round(time.time() - t0, 1),
                                 "web_citations": [(a.get("url_citation") or {}).get("url") for a in msg.get("annotations") or []]})
        if spent > args.budget:
            print(f"  budget exceeded by one call: spent ${spent:.3f} of ${args.budget}")
            receipt["stopped"] = f"budget exceeded in round {rnd}"
        family = MODELS[requested]["family"]
        if resp.get("model") and not resp["model"].startswith(family):
            sys.exit(f"HALT: asked for {model}, got {resp['model']}")
        content = msg.get("content") or ""
        messages.append({"role": "assistant", "content": content})
        try:
            lane = parse_json(content)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"  round {rnd}: output is not JSON ({e}); asking again")
            messages.append({"role": "user", "content": "Your reply was not a single valid JSON object. Return the complete lane JSON only."})
            receipt["rounds"].append({"round": rnd, "parse_error": str(e)})
            continue
        normalise(lane, args.lane)
        downgraded = admit_sources(lane, allowed)
        n_vac = 0
        for r in lane.get("recipes") or []:
            for c in r.get("checks") or []:
                if vacuous(c):
                    c["_vacuous"] = True
                    n_vac += 1
        with open(draft, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(lane, fh, indent=2, ensure_ascii=False)
        lint_errors = lint(lane, out)
        clean = json.loads(json.dumps(lane))
        for r in clean.get("recipes") or []:
            for c in r.get("checks") or []:
                c.pop("_vacuous", None)
        with open(draft, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(clean, fh, indent=2, ensure_ascii=False)
        results = oracle(draft)
        n_fail = sum(1 for r in results if not r.get("ok")) + n_vac
        receipt["rounds"].append({"round": rnd, "recipes": len(lane.get("recipes") or []), "checks": len(results),
                                  "failing_checks": n_fail, "lint_errors": len(lint_errors),
                                  "downgraded_sources": len(downgraded), "spent_usd": round(spent, 4)})
        print(f"  round {rnd}: {len(lane.get('recipes') or [])} recipes, {len(results)} checks, {n_fail} failing "
              f"({n_vac} vacuous), "
              f"{len(lint_errors)} lint errors, {len(downgraded)} sources downgraded, spent ${spent:.3f}")
        if not n_fail and not lint_errors:
            break
        if receipt.get("stopped"):
            break
        if rnd < args.rounds:
            messages.append({"role": "user", "content": feedback(rnd + 1, results, lint_errors, downgraded, lane)})

    if lane is None:
        sys.exit("HALT: no parseable lane after every round")
    # Final admission: drop checks the compiler never passed, then recipes the contract cannot admit.
    failing = {(r["slug"], r["index"]) for r in results if not r.get("ok")}
    dropped_checks, dropped_recipes = [], []
    for r in lane.get("recipes") or []:
        slug = assemble_lanes.slugify(r.get("name"))
        kept = []
        for i, c in enumerate(r.get("checks") or []):
            if (slug, i) in failing or c.pop("_vacuous", False):
                dropped_checks.append({"recipe": r.get("name"), "label": c.get("label")})
            else:
                kept.append(c)
        r["checks"] = kept
    admitted = []
    for r in lane.get("recipes") or []:
        errs = lint(dict(lane, recipes=[r]), out)
        if errs:
            dropped_recipes.append({"recipe": r.get("name"), "why": errs[:3]})
        else:
            admitted.append(r)
    lane["recipes"] = admitted
    packet = lane.pop("packet", "") or old_packet
    os.makedirs(os.path.join(wdir, "lanes"), exist_ok=True)
    os.makedirs(os.path.join(wdir, "receipts"), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(lane, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    with open(os.path.join(wdir, f"{args.lane}.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"# {lane.get('title') or args.lane} — generator packet\n\n"
                 f"Written by `{model}` through `scripts/openrouter_lane.py`; unverified until the wave's "
                 f"verification record says otherwise.\n\n{packet}\n")
    receipt.update(spent_usd=round(spent, 4), dropped_checks=dropped_checks, dropped_recipes=dropped_recipes,
                   downgraded_sources=downgraded, final_recipes=len(admitted),
                   final_checks=sum(len(r.get("checks") or []) for r in admitted))
    write_receipt("complete")
    print(f"wrote {os.path.relpath(out, KB)}: {len(admitted)} recipes, {receipt['final_checks']} checks; "
          f"dropped {len(dropped_checks)} checks, {len(dropped_recipes)} recipes; spent ${spent:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
