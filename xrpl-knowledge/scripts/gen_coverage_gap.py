#!/usr/bin/env python3
"""gen_coverage_gap.py — cross-reference the xrpl-knowledge KB against xrpl-lab's modules to
produce a ranked module backlog (the depth the workbook is missing, sourced from the verified KB).

Reads:
  - xrpl.db (this KB) — capabilities + their domain, network_status, status, builder_fit, verified, tracks.
  - xrpl-lab modules/*.md frontmatter (id/title/track/summary) — current coverage.
Writes a markdown report to module-drafts/COVERAGE-GAP.md.

The KB is the curriculum source: a high-value capability (recommended, mainnet-live / testnet-runnable,
builder_fit>=4, cross-family verified) that no module teaches is a candidate module.

Usage:  $env:PYTHONUTF8='1'; python scripts/gen_coverage_gap.py [path-to-xrpl-lab/modules]
"""
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
DB = os.path.join(ROOT, "xrpl.db")
OUT = os.path.join(ROOT, "module-drafts", "COVERAGE-GAP.md")
DEFAULT_MODULES = r"E:\AI\xrpl-lab\modules"

# KB feature-domain -> the xrpl-lab track that currently covers it (or PROPOSED new track if none).
# Existing xrpl-lab tracks: foundations, dex, reserves, audit, amm.
DOMAIN_TRACK = {
    "protocol-consensus":        ("reserves/foundations", True),   # reserves_101 + receipts touch it
    "transactions":              ("foundations/audit", True),      # receipts, failures, audit
    "tokens":                    ("foundations", "partial"),       # trust_lines_101 covers IOUs only, not MPTs
    "stablecoins-institutional": ("payments (proposed)", False),
    "dex-amm":                   ("dex/amm", True),                 # well covered
    "nfts":                      ("nfts (proposed)", False),
    "programmability-hooks":     ("programmability (proposed)", False),
    "programmability-evm":       ("programmability (proposed)", False),
    "payments-advanced":         ("payments (proposed)", "partial"),  # receipts only; no escrow/channel/check/batch
    "identity-compliance":       ("identity (proposed)", "partial"),  # account_hygiene touches flags only
    "client-libraries":          ("foundations (reference)", False),
    "infrastructure-tooling":    ("ops (proposed)", False),
}


def load_modules(mod_dir):
    mods = []
    if not os.path.isdir(mod_dir):
        return mods
    for fn in sorted(os.listdir(mod_dir)):
        if not fn.endswith(".md"):
            continue
        txt = open(os.path.join(mod_dir, fn), encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---", txt, re.DOTALL)
        fm = m.group(1) if m else ""
        def field(k):
            r = re.search(rf"^{k}:\s*(.+)$", fm, re.MULTILINE)
            return r.group(1).strip().strip('"') if r else ""
        mods.append({"id": field("id") or fn[:-3], "title": field("title"),
                     "track": field("track"), "summary": field("summary"), "file": fn})
    return mods


def main(mod_dir):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    mods = load_modules(mod_dir)
    # keyword haystack from every module (id + title + summary), lowercased
    hay = " ".join((m["id"] + " " + m["title"] + " " + m["summary"]).lower() for m in mods)

    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    L = ["# xrpl-lab coverage gap — sourced from xrpl-knowledge",
         f"Generated from `xrpl.db` + `{mod_dir}`. The KB is the curriculum source; a high-value capability "
         "no module teaches is a candidate module.\n",
         f"**xrpl-lab today: {len(mods)} modules** across tracks "
         + ", ".join(sorted({m['track'] for m in mods if m['track']})) + ".\n"]

    # ── Domain coverage table ──
    L += ["## Domain coverage\n",
          "| KB domain | Caps | Recommended | Mainnet-live | xrpl-lab track | Covered? |",
          "|---|--:|--:|--:|---|---|"]
    gap_rows = []
    for cat in cats:
        caps = c.execute("SELECT * FROM capabilities WHERE category_id=?", (cat["id"],)).fetchall()
        n = len(caps)
        if not n:
            continue
        rec = sum(1 for x in caps if x["status"] == "recommended")
        live = sum(1 for x in caps if x["network_status"] == "mainnet-live")
        track, covered = DOMAIN_TRACK.get(cat["slug"], ("?", False))
        mark = {True: "✅ yes", "partial": "🟡 partial", False: "❌ none"}[covered]
        L.append(f"| {cat['name']} | {n} | {rec} | {live} | {track} | {mark} |")
        if covered is not True:
            gap_rows.append((cat, covered, track))

    # ── The backlog ──
    L += ["", "## Module backlog — top untaught capabilities per gap domain\n",
          "Ranked by builder_fit then verified. Each is a candidate `xrpl-lab` module "
          "(`scaffold --from-kb <slug>`). Capabilities already echoed in a module's title/summary are skipped.\n"]
    total_backlog = 0
    for cat, covered, track in gap_rows:
        caps = c.execute(
            """SELECT * FROM capabilities WHERE category_id=?
               AND status IN ('recommended','situational')
               AND network_status IN ('mainnet-live','testnet-devnet')
               AND builder_fit IS NOT NULL
               ORDER BY (status!='recommended'), builder_fit DESC, verified DESC, name""",
            (cat["id"],)).fetchall()
        # drop capabilities whose distinctive term already appears in a module
        backlog = []
        for x in caps:
            key = re.sub(r"[^a-z0-9 ]", " ", (x["name"] or "").lower())
            toks = [t for t in key.split() if len(t) > 4 and t not in
                    ("token", "tokens", "based", "their", "using", "value", "asset", "assets", "account")]
            if toks and any(t in hay for t in toks[:2]):
                continue  # plausibly already taught
            backlog.append(x)
        if not backlog:
            continue
        cover_note = f" _(currently {covered})_" if covered == "partial" else ""
        L.append(f"### {cat['name']} → track `{track}`{cover_note}  ·  {len(backlog)} candidates")
        for x in backlog[:8]:
            v = "✓" if x["verified"] else "·"
            xls = f" [{x['xls_standard']}]" if x["xls_standard"] else ""
            L.append(f"- **{x['name']}**{xls} `{x['slug']}` — fit {x['builder_fit']}/5 {v} · {x['kind']} · "
                     f"{(x['summary'] or '')[:140]}")
        total_backlog += len(backlog)
        L.append("")

    L += ["## Recommended new tracks\n",
          "xrpl-lab's tracks (foundations/dex/reserves/audit/amm) mirror today's coverage. The KB reveals "
          "whole-ecosystem depth that needs new tracks:\n",
          "- **nfts** — mint, collections, marketplaces, royalties, dynamic NFTs (game assets)",
          "- **payments** — escrow, payment channels, checks, batch payouts, cross-currency",
          "- **identity** — DID, Credentials, permissioned domains, deposit-auth (KYC-gated)",
          "- **programmability** — Hooks (Xahau) + EVM sidechain contracts",
          "- **tokens** (or extend foundations) — MPTs, clawback, freeze, issuance depth beyond IOU trust lines",
          "\nAdopting a track = add it to `xrpl_lab/curriculum.py::TRACKS`.\n",
          f"**Total auto-detected backlog: {total_backlog} candidate modules.**"]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    con.close()
    print(f"coverage gap report -> {os.path.relpath(OUT, ROOT)}  ({total_backlog} candidate modules, {len(mods)} existing)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODULES)
