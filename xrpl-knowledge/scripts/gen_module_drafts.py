#!/usr/bin/env python3
"""gen_module_drafts.py — draft xrpl-lab modules from verified xrpl-knowledge capabilities.

The KB-seeded scaffolder behind the proposed `xrpl-lab scaffold --from-kb <slug>`. For each capability it
emits an xrpl-lab-format module markdown draft: frontmatter (id/title/track/summary/time/level/mode + checks)
+ a body whose intro/steps/checkpoint are seeded from the KB's summary / key_fields / gotchas, and whose
"Learn more" links are the KB's verified sources. The CORE operation is left as a TODO action hint (the action
wiring is xrpl-lab's domain); only `ensure_wallet` is emitted as a real action, so the draft passes
`xrpl-lab lint` out of the box (same discipline as xrpl-lab's own render_module_skeleton).

Usage:  $env:PYTHONUTF8='1'; python scripts/gen_module_drafts.py [slug ...]
        (no args -> a demo set spanning the new tracks)  ·  --out <dir> to target xrpl-lab/modules directly
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
OUTDIR = os.path.join(ROOT, "module-drafts")

DOMAIN_TRACK = {
    "nfts": "nfts", "payments-advanced": "payments", "identity-compliance": "identity",
    "programmability-hooks": "programmability", "programmability-evm": "programmability",
    "tokens": "tokens", "stablecoins-institutional": "tokens", "dex-amm": "dex",
    "protocol-consensus": "foundations", "transactions": "foundations",
    "client-libraries": "ops", "infrastructure-tooling": "ops",
}
DEMO = ["nftokenmint", "payment-channel-create", "did-transactions", "mpt-issuance-create-config", "hooks-overview"]


def level_for(kind):
    return "intermediate" if (kind or "") in ("pattern", "standard", "amendment", "service", "library") else "beginner"


def runnable(net):
    # testnet modules execute; pending/devnet-only/deprecated -> dry-run (teach without a live tx)
    return net in ("mainnet-live", "testnet-devnet")


def sentence(s, n=200):
    s = (s or "").strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def yaml_safe(s):
    """Make a string safe inside a double-quoted YAML scalar (capability text can carry quotes/JSON/newlines)."""
    return re.sub(r"\s+", " ", str(s or "").replace('"', "'").replace("\n", " ")).strip()


def draft(cur, slug):
    cap = cur.execute("SELECT cap.*, c.slug AS cat_slug, c.name AS cat_name FROM capabilities cap "
                      "JOIN categories c ON c.id=cap.category_id WHERE cap.slug=?", (slug,)).fetchone()
    if not cap:
        return None, f"no capability '{slug}'"
    cap = dict(cap)
    track = DOMAIN_TRACK.get(cap["cat_slug"], "foundations")
    mode = "testnet" if runnable(cap["network_status"]) else "dry-run"
    title = cap["name"] if len(cap["name"]) < 60 else cap["name"][:57] + "…"
    sources = cur.execute("SELECT title,url,claim FROM sources WHERE capability_id=? ORDER BY id LIMIT 5",
                          (cap["id"],)).fetchall()

    checks = [f"Understood: {sentence(cap['name'], 60)}"]
    if mode == "testnet":
        checks.append(f"{cap['kind'].capitalize() if cap['kind'] else 'Operation'} performed on testnet (txid produced)")
    if cap["key_fields"]:
        checks.append(f"Verified the key fields: {sentence(cap['key_fields'], 80)}")
    if cap["gotchas"]:
        checks.append(f"Avoided the gotcha: {sentence(cap['gotchas'], 80)}")

    xls = f" ({cap['xls_standard']})" if cap["xls_standard"] else ""
    amend = f" · amendment `{cap['amendment_name']}`" if cap["amendment_name"] else ""
    net = cap["network_status"]
    fm = [
        "---",
        f"id: kb_{re.sub(r'[^a-z0-9_]', '_', slug.lower())}",
        f'title: "{yaml_safe(title + xls)}"',
        f"track: {track}",
        f'summary: "{yaml_safe(sentence(cap["summary"] or cap["name"], 110))}"',
        "time: 15-20 min",
        f"level: {level_for(cap['kind'])}",
        f"mode: {mode}",
        "requires: []",
        "produces:",
        "  - report" if mode == "dry-run" else "  - txid\n  - report",
        "checks:",
    ] + [f'  - "{yaml_safe(c)}"' for c in checks] + ["---", ""]

    body = [
        f"<!-- DRAFT auto-seeded from xrpl-knowledge capability `{slug}` "
        f"({cap['cat_name']}, {net}{', verified' if cap['verified'] else ', UNVERIFIED — re-check'}){amend}.",
        "     Edit forward: write the prose, wire the core action, set requires/checks. -->",
        "",
        sentence(cap["summary"] or "", 400) or f"This module teaches **{cap['name']}** on the XRP Ledger.",
        "",
        "## Step 1: Ensure your wallet is ready",
        "",
        "You need a funded wallet. If you completed an earlier module it loads automatically.",
        "",
        "<!-- action: ensure_wallet -->",
        "",
        f"## Step 2: {cap['name']}",
        "",
    ]
    if cap["key_fields"]:
        body += [f"**Key fields / API to know:** {cap['key_fields']}", ""]
    body += [
        "<!-- TODO: wire the core action for this module. The KB describes WHAT happens; pick the",
        "     matching xrpl-lab action (see `xrpl-lab lint` for the registered action schema), e.g.:",
        "       <!-- action: ensure_funded -->",
        "       <!-- action: submit_payment destination=ADDRESS amount=10 -->",
        "       <!-- action: set_trust_line currency=LAB limit=1000 -->",
        "     Until wired, this module is dry-run/teaching-only. -->",
        "",
        "## Step 3: Verify on-ledger",
        "",
        "Inspect what happened on the explorer — turn the result into evidence you can read.",
        "",
        "## Checkpoint: What you proved",
        "",
        f"You now understand **{cap['name']}**.",
        "",
    ]
    if cap["gotchas"]:
        body += [f"**Watch out:** {cap['gotchas']}", ""]
    if net != "mainnet-live":
        body += [f"> ⚠ Network status: **{net}**. Confirm current mainnet availability before relying on this in production.", ""]
    if sources:
        body += ["**Learn more (verified sources):**"]
        body += [f"- [{(s['title'] or 'source').strip()}]({s['url']})" + (f" — {sentence(s['claim'], 90)}" if s["claim"] else "")
                 for s in sources]
        body += [""]
    body += ["Run `xrpl-lab proof-pack` when you're ready to export your work."]

    return "\n".join(fm) + "\n".join(body) + "\n", None


def main(slugs, outdir):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for slug in slugs:
        md, err = draft(cur, slug)
        if err:
            print(f"  ✗ {slug}: {err}")
            continue
        dest = os.path.join(outdir, f"kb_{re.sub(r'[^a-z0-9_]', '_', slug.lower())}.md")
        open(dest, "w", encoding="utf-8").write(md)
        print(f"  ✓ {slug} -> {os.path.relpath(dest, ROOT)}")
        n += 1
    con.close()
    print(f"{n} module draft(s) written to {os.path.relpath(outdir, ROOT)}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    outdir = OUTDIR
    if "--out" in sys.argv:
        outdir = sys.argv[sys.argv.index("--out") + 1]
    main(args or DEMO, outdir)
