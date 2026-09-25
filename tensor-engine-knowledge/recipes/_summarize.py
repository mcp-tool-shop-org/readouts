#!/usr/bin/env python3
"""Goal 3 (part 1): one-line summaries for each recipe, generated on the LOCAL model.

Runs entirely on Ollama (qwen3.6:35b-a3b) — zero Claude tokens. Idempotent: only fills
recipes.summary where it's NULL/empty (re-runnable). Thinking disabled + <think> stripped.

Usage:  $env:PYTHONUTF8='1'; python recipes/_summarize.py [--limit N] [--all]
  --limit N : only process N rows (pilot)
  --all     : re-summarize even rows that already have a summary
"""
import os, sys, re, json, sqlite3, urllib.request

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen3.6:35b-a3b"

PROMPT = (
    "You label tensor-engine setup recipes for a catalog. In ONE concise line "
    "(max 16 words, no period, no preamble, no quotes, no markdown), state what this recipe "
    "does plus its single most important RTX-5090 / Blackwell / Windows constraint if any.\n\n"
    "Recipe name: {name}\nKind: {kind}\nBody:\n{body}\n\nOne-line summary:")

def summarize(name, kind, body):
    payload = {
        "model": MODEL,
        "prompt": PROMPT.format(name=name, kind=kind, body=(body or "")[:2000]),
        "stream": False, "think": False,
        "options": {"temperature": 0.2, "num_predict": 60},
    }
    req = urllib.request.Request(OLLAMA, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.loads(r.read())["response"]
    out = re.sub(r"<think>.*?</think>", "", out, flags=re.S).strip()
    line = next((l.strip().strip('"').strip("-•* ").strip() for l in out.splitlines() if l.strip()), "")
    return line[:160]

def main():
    limit = None; do_all = "--all" in sys.argv
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    con = sqlite3.connect(DB); cur = con.cursor()
    where = "" if do_all else "where summary is null or summary=''"
    q = f"select id, name, recipe_kind, body from recipes {where} order by id"
    if limit: q += f" limit {limit}"
    rows = cur.execute(q).fetchall()
    print(f"summarizing {len(rows)} recipes on {MODEL} ...")
    done = 0
    for rid, name, kind, body in rows:
        try:
            s = summarize(name, kind, body)
        except Exception as e:
            print(f"  [{rid}] ERROR {e}"); continue
        cur.execute("update recipes set summary=? where id=?", (s, rid))
        done += 1
        if limit or done % 20 == 0:
            print(f"  [{done}/{len(rows)}] {name[:40]:40s} -> {s}")
        if done % 20 == 0:
            con.commit()
    con.commit()
    print(f"done: {done} summaries written")
    con.close()

if __name__ == "__main__":
    main()
