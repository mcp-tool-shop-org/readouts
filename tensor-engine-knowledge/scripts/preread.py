#!/usr/bin/env python3
"""preread — compress large sources to digests BEFORE they enter a Claude/agent context.

The study-swarm token-saver. A research/verify agent that ingests a raw log, doc, DB dump, or web
page burns Claude tokens on material a local model can digest for free. `preread` is the
ORCHESTRATOR-side step: compress each oversized source via `offload compress` (local, on llama-swap)
and emit the digest + a token-savings receipt, so only the small digest is embedded in the agent's
prompt — the raw never reaches Claude.

  python preread.py --file big.log --file dump.json --words 150
  python preread.py --url https://example.com/page --words 200 --json
  type big.log | python preread.py --words 120

Sources under --threshold-words pass through uncompressed (don't pay a model call to shrink something
already small). Reduction is measured with the model's OWN tokenizer (offload reports it). stdlib +
offload only; llama-swap must be up (:9090).
"""
import argparse, json, os, re, sys, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OFFLOAD = os.environ.get("OFFLOAD_SCRIPT", "E:/AI-Models/studio-local/offload.py")
PYTHON = os.environ.get("OFFLOAD_PYTHON", sys.executable)


def _strip_html(html):
    html = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", html)
    return re.sub(r"\s+", " ", re.sub(r"(?s)<[^>]+>", " ", html)).strip()


def read_source(spec):
    """spec = ('file', path) | ('url', url) | ('stdin', None) -> (label, text)."""
    kind, val = spec
    if kind == "file":
        return val, open(val, encoding="utf-8", errors="replace").read()
    if kind == "url":
        req = urllib.request.Request(val, headers={"User-Agent": "preread/1.0 (study-swarm)"})
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read().decode("utf-8", errors="replace")
        return val, _strip_html(raw) if "<" in raw[:2000] else raw
    return "(stdin)", sys.stdin.read()


def compress(text, words, model):
    """Shell offload compress (the canonical compressor) -> its --json dict."""
    p = subprocess.run(
        [PYTHON, OFFLOAD, "compress", "--words", str(words), "--model", model, "--json"],
        input=text, capture_output=True, text=True, encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
    )
    if p.returncode != 0:
        raise RuntimeError(f"offload compress failed: {p.stderr.strip()[:300]}")
    return json.loads(p.stdout)


def main():
    ap = argparse.ArgumentParser(prog="preread", description="Pre-read compressor for study-swarm sources.")
    ap.add_argument("--file", action="append", default=[], help="source file (repeatable)")
    ap.add_argument("--url", action="append", default=[], help="source URL (repeatable)")
    ap.add_argument("--words", type=int, default=150, help="digest word budget")
    ap.add_argument("--threshold-words", type=int, default=600,
                    help="sources under this many words pass through uncompressed")
    ap.add_argument("--model", default="qwen3-4b")
    ap.add_argument("--out", help="write the digests+receipt JSON here")
    ap.add_argument("--json", action="store_true", help="print the receipt JSON to stdout")
    a = ap.parse_args()

    specs = [("file", f) for f in a.file] + [("url", u) for u in a.url]
    if not specs:
        specs = [("stdin", None)]

    items, tin, tout = [], 0, 0
    for spec in specs:
        label, text = read_source(spec)
        nwords = len(text.split())
        if nwords < a.threshold_words:
            items.append({"source": label, "skipped": True, "reason": f"under threshold ({nwords} < {a.threshold_words} words)",
                          "in_tokens": None, "out_tokens": None, "digest": text})
            print(f"[preread] {label}: {nwords} words — passthrough (under threshold)", file=sys.stderr)
            continue
        r = compress(text, a.words, a.model)
        tin += r["in_tokens"]; tout += r["out_tokens"]
        items.append({"source": label, "skipped": False, "in_tokens": r["in_tokens"],
                      "out_tokens": r["out_tokens"], "reduction_pct": r["reduction_pct"],
                      "model": r["model"], "digest": r["summary"]})
        print(f"[preread] {label}: {r['in_tokens']} -> {r['out_tokens']} tok ({r['reduction_pct']}% smaller)", file=sys.stderr)

    compressed = [i for i in items if not i["skipped"]]
    receipt = {
        "kind": "study-swarm-preread",
        "model": a.model, "word_budget": a.words, "threshold_words": a.threshold_words,
        "sources": len(items), "compressed": len(compressed),
        "total_in_tokens": tin, "total_out_tokens": tout,
        "total_saved_tokens": tin - tout,
        "aggregate_reduction_pct": round(100 * (1 - tout / tin), 1) if tin else None,
        "items": items,
    }
    if a.out:
        json.dump(receipt, open(a.out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if a.json:
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
    else:
        print(f"\n[preread] {len(compressed)}/{len(items)} compressed | {tin} -> {tout} Claude-tokens "
              f"({receipt['aggregate_reduction_pct']}% smaller, {tin - tout} saved)", file=sys.stderr)


if __name__ == "__main__":
    main()
