"""Collect a Comfy Cloud batch-output JSON into Grounded run-artifact folders.

Usage: python collect_wave.py <batch_output.json>
- Downloads every output whose job_id is in MAP into its cue folder with
  canonical fixture-style names (<short>-track_mix.flac etc.).
- Instrumented job: downloads only .txt telemetry; audio filenames go to the
  determinism comparison instead of disk.
- Prints per-folder inventory, every LUFS/BPM manifest line, sha256 table,
  and the instrumented-vs-production content-address comparison.
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

BASE = Path(r"model-knowledge/generated/grounded")

MAP = {
    "bfde6090": ("cue-ardent-ready-s101", "ardent-ready-s101"),
    "af5983d5": ("cue-ardent-ready-s102", "ardent-ready-s102"),
    "41639142": ("cue-ardent-sweep-s103", "ardent-sweep-s103"),
    "e1080f7a": ("cue-ardent-sweep-s104", "ardent-sweep-s104"),
    "ba9fdcfd": ("cue-court-martial-s105", "court-martial-s105"),
    "e58cd3b6": ("cue-court-martial-s106", "court-martial-s106"),
    "71c004dc": ("cue-ambush-s201", "ambush-s201"),
    "ba8ed7b8": ("cue-derelict-s202", "derelict-s202"),
    "8b12e374": ("cue-freeport-s301", "freeport-s301"),
    "a2450dd0": ("cue-contracts-s302", "contracts-s302"),
    "8e79d1ba": ("cue-communion-s401", "communion-s401"),   # failed run; remap replaces
    "b1d49f9b": ("cue-investigation-s501", "investigation-s501"),
    "92bd0ee0": ("cue-crew-s601", "crew-s601"),
    "ca6dd409": ("_instrumented-ardent-ready-s101", "instr-ardent-ready-s101"),
    # remap batch
    "318d8252": ("cue-communion-s401", "communion-s401"),
    "bf663bac": ("cue-investigation-s501", "investigation-s501"),
    "68a54a21": ("cue-crew-s601", "crew-s601"),
}

PRODUCTION_S101 = "bfde6090"
INSTRUMENTED = "ca6dd409"


def main(path: str) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    outputs = data["outputs"]
    by_job: dict[str, dict[str, str]] = {}
    downloaded = []
    for out in outputs:
        jid8 = out["job_id"][:8]
        if jid8 not in MAP:
            continue
        folder, short = MAP[jid8]
        prefix = out["filename_prefix"].split("/")[-1]
        by_job.setdefault(jid8, {})[prefix] = out["filename"]
        ext = ".flac" if out["class_type"] == "SaveAudioAdvanced" else ".txt"
        if jid8 == INSTRUMENTED and ext == ".flac":
            continue  # determinism check uses content-addresses, not bytes
        dest = BASE / folder / f"{short}-{prefix}{ext}"
        if dest.exists() and dest.stat().st_size > 0:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(out["url"]) as r, open(dest, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)
        downloaded.append(dest)

    print(f"downloaded {len(downloaded)} new files")
    for folder in sorted({m[0] for m in MAP.values()}):
        d = BASE / folder
        if not d.exists():
            continue
        files = sorted(p for p in d.iterdir() if p.is_file())
        if not files:
            continue
        print(f"\n== {folder} ({len(files)} files)")
        for p in files:
            digest = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
            line = f"  {p.name}  {p.stat().st_size}  sha256:{digest}"
            if p.suffix == ".txt":
                line += "  | " + p.read_text(encoding="utf-8", errors="replace").strip()[:120]
            print(line)

    prod = by_job.get(PRODUCTION_S101, {})
    instr = by_job.get(INSTRUMENTED, {})
    if prod and instr:
        print("\n== determinism: instrumented vs production s101 (cloud content-addresses)")
        for key in sorted(prod):
            a, b = prod.get(key), instr.get(key)
            verdict = "MATCH" if a == b else "DIFFER"
            print(f"  {key}: {verdict}  prod={str(a)[:12]}  instr={str(b)[:12]}")


if __name__ == "__main__":
    main(sys.argv[1])
