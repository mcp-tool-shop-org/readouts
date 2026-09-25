#!/usr/bin/env python3
"""Rewrite the root README's knowledge-base table from index.json.

The README already told the reader this table was copied from the generated index
("do not invent") - but copying was manual, so it drifted: vocology sat two waves and
48 findings behind while every other row was current. A table that claims to mirror a
generated artifact should be generated from it.

Rewrites only the rows between the table header and the blank line after it. Everything
else in the README is left byte-identical.

    python shared/sync_readme_table.py --check   # exit 1 if stale (CI gate)
    python shared/sync_readme_table.py           # rewrite in place
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
INDEX = os.path.join(ROOT, "index.json")
HEADER = "| KB | What | Status |"
RULE = "|----|------|--------|"


def build_rows() -> list[str]:
    with open(INDEX, encoding="utf-8") as fh:
        kbs = json.load(fh)["knowledge_bases"]
    rows = []
    for k in sorted(kbs, key=lambda x: x["kb"]):
        slug, noun = k["kb"], k.get("noun", "entries")
        status = (f"**{k['entries']} {noun} · {k['domains']} domains · "
                  f"{k['waves']} waves · {k['verified']}/{k['entries']} verified**")
        rows.append(f"| [{slug}]({slug}/) | {k['what']} | {status} |")
    return rows


def render(readme: str, rows: list[str]) -> str:
    lines = readme.split("\n")
    try:
        h = lines.index(HEADER)
    except ValueError:
        sys.exit(f"sync_readme_table: header row not found in {README}")
    if lines[h + 1].strip() != RULE:
        sys.exit("sync_readme_table: table rule row missing under the header")
    end = h + 2
    while end < len(lines) and lines[end].startswith("| ["):
        end += 1
    return "\n".join(lines[:h + 2] + rows + lines[end:])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the README table is stale; write nothing")
    args = ap.parse_args()

    with open(README, encoding="utf-8") as fh:
        current = fh.read()
    rows = build_rows()
    updated = render(current, rows)

    if updated == current:
        print(f"README table already current ({len(rows)} KBs).")
        return 0
    if args.check:
        print("::error:: README knowledge-base table is stale — run "
              "`python shared/sync_readme_table.py`")
        return 1
    with open(README, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(updated)
    print(f"README table re-synced from index.json ({len(rows)} KBs).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
