#!/usr/bin/env python3
"""tighten_checks.py — apply verifier-requested gate tightenings to lane check files.

A check's label is a claim. Where a verifier (or assemble_lanes.py's label lint) found a label that
promises more than the check asserts — "compiles silently" without `no_warnings`, "imports nothing"
without `wasm_no_imports` — this sets the missing gate on exactly the named check, and nothing else.
The research content is untouched; the check only gains the assertion its own label already made.
ADD appends a check where a verifier confirmed a recipe's claim by its own counter-example but no
check asserted it; a check can only lower a recipe's standing (a failure gates it to unverified).
Every tightening here was dry-run first and passed, beside a planted wrong value that failed; the
authoritative oracle run after it is the proof.

Usage:  python scripts/tighten_checks.py            # apply TIGHTEN below
        python scripts/tighten_checks.py --dry-run  # report only
"""
import argparse
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# (wave dir, lane slug, recipe slug prefix, check index, gate, value, who asked)
# The four checks two verifiers named (cargo-modules x2, memory-layout x2) ALREADY carried their
# gates in the lane files; the staged verifier input had dropped those two keys. Nothing to tighten
# there — see verification/operator-notes.json. The entries below are the label lint's real finds.
TIGHTEN = [
    ("wave-01-essentials", "types-patterns", "list-every-variant-in-a-match", 1, "no_warnings", True, "label lint"),
    ("wave-01-essentials", "types-patterns", "keep-patterns-edition-2024-clean", 0, "no_warnings", True, "label lint"),
    ("wave-01-essentials", "types-patterns", "wrap-units-and-ids-in-tuple-struct-newtypes", 1, "no_warnings", True, "label lint"),
    ("wave-02-advanced", "concurrency-async", "serialize-native-calls-into-the-law", 7, "no_warnings", True, "label lint"),
    # wasm-raw-abi's verifier confirmed both by its own counter-examples and corrected the recipe
    # because no check asserted them; the oracle gained these gates during the wave.
    ("wave-03-si-rpg-engine", "wasm-raw-abi", "export-the-law-with-unsafe-no-mangle", 1, "wasm_absent_exports",
     ["public_but_not_exported", "step_impl"], "wasm-raw-abi verifier"),
    ("wave-03-si-rpg-engine", "wasm-raw-abi", "export-the-law-with-unsafe-no-mangle", 5, "wasm_imports",
     ["host.host_log"], "wasm-raw-abi verifier"),
]

# (wave dir, lane slug, recipe slug prefix, check, who asked) — appended once, matched by label.
ADD = [
    ("wave-03-si-rpg-engine", "wasm-raw-abi", "return-a-status-code-from-every-export", {
        "label": "an unchecked export that indexes out of range panics, and under panic=abort the panic "
                 "is a WebAssembly trap (RuntimeError: unreachable)",
        "edition": "2024", "target": "wasm32-unknown-unknown", "crate_type": "cdylib", "expect": "runs",
        "source": "static mut SLOTS: [f64; 4] = [0.0; 4];\n"
                  "/// No range check: an index of 4 or more panics.\n"
                  "#[unsafe(no_mangle)]\n"
                  "pub extern \"C\" fn write_slot_unchecked(i: u32, v: f64) -> u32 {\n"
                  "    let slots = unsafe { &mut *(&raw mut SLOTS) };\n"
                  "    slots[i as usize] = v;\n"
                  "    1\n"
                  "}\n",
        "wasm_call": {"export": "write_slot_unchecked", "args": [9, 1.5]},
        "wasm_trap": True,
        "stdout_contains": ["unreachable"],
    }, "wasm-raw-abi verifier"),
    # host-audio-and-midi's verifier corrected the recipe because its check never registered
    # AllocDisabler as the global allocator, so nothing showed an allocation being caught. This
    # check does, in the oracle's debug build (the crate's default `disable_release` makes it a
    # no-op in release). The exit status is Windows' abort status, as in two wave-1 checks.
    ("wave-04-si-jam-sessions", "host-audio-and-midi", "wrap-oscillator-callback-in-assert-no-alloc", {
        "label": "with AllocDisabler as #[global_allocator], an allocation inside assert_no_alloc aborts "
                 "(debug build); one outside it is allowed",
        "oracle_set": "jam", "edition": "2024", "target": "host", "crate_type": "bin",
        "deps": ["assert_no_alloc"], "expect": "runs",
        "source": "use assert_no_alloc::{assert_no_alloc, AllocDisabler};\n\n"
                  "#[global_allocator]\n"
                  "static ALLOC: AllocDisabler = AllocDisabler;\n\n"
                  "fn main() {\n"
                  "    println!(\"before\");\n"
                  "    // Allowed: outside assert_no_alloc.\n"
                  "    let ok: Vec<u8> = Vec::with_capacity(8);\n"
                  "    std::hint::black_box(&ok);\n"
                  "    // Forbidden: an allocation inside the closure reaches AllocDisabler, which calls handle_alloc_error.\n"
                  "    assert_no_alloc(|| {\n"
                  "        let v: Vec<u8> = Vec::with_capacity(16);\n"
                  "        std::hint::black_box(&v);\n"
                  "    });\n"
                  "    println!(\"unreachable\");\n"
                  "}\n",
        "stdout": "before",
        "exit_code": 3221226505,
    }, "host-audio-and-midi verifier"),
]


def slugify(s):
    s = (s or "").strip().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "x"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    touched = {}

    def recipe(wave, lane, prefix):
        path = os.path.join(ROOT, "waves", wave, "lanes", f"{lane}.json")
        data = touched.get(path) or json.load(open(path, encoding="utf-8"))
        matches = [r for r in data["recipes"] if slugify(r["name"]).startswith(prefix)]
        if len(matches) != 1:
            raise SystemExit(f"HALT: {lane}/{prefix}* matched {len(matches)} recipes")
        touched[path] = data
        return matches[0]

    dry = "(dry) " if args.dry_run else ""
    for wave, lane, prefix, idx, gate, value, who in TIGHTEN:
        checks = recipe(wave, lane, prefix).get("checks") or []
        if idx >= len(checks):
            raise SystemExit(f"HALT: {lane}/{prefix}* has no check #{idx}")
        before = checks[idx].get(gate)
        checks[idx][gate] = value
        print(f"{dry}{lane}/{prefix}#{idx}: {gate} {before!r} -> {value!r}   [{who}]")
    for wave, lane, prefix, check, who in ADD:
        checks = recipe(wave, lane, prefix).setdefault("checks", [])
        if any(c.get("label") == check["label"] for c in checks):
            print(f"{dry}{lane}/{prefix}: check already present — {check['label'][:60]}")
            continue
        checks.append(dict(check))
        print(f"{dry}{lane}/{prefix}#{len(checks) - 1}: added — {check['label'][:60]}   [{who}]")
    if not args.dry_run:
        for path, data in touched.items():
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
        print(f"wrote {len(touched)} lane file(s)")


if __name__ == "__main__":
    main()
