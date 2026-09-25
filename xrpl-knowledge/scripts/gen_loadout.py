#!/usr/bin/env python3
"""Generate the KB ai-loadout index at .claude/loadout/index.json over the catalog, from xrpl.db.

Progressive disclosure (so the corpus isn't dumped on the agent at once):
  - ONE tiny `core` entry (the catalog index) — always loaded for orientation.
  - one `domain` entry per FEATURE domain (keyword-routed).
  - one `domain` entry per BUILD-FOCUS track folder (keyword-routed) — game-economies / nft-assets / payments / identity.
  - the wave dispatch/verification docs as `domain` entries.
  - the raw swarm json as `manual` — never auto-loaded.

Re-run after each wave. QA:  ai-loadout validate|overlaps|budget .claude/loadout/index.json
"""
import json
import os
import re
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "xrpl.db")
OUTDIR = os.path.join(ROOT, ".claude", "loadout")
DATE_FALLBACK = "2026-06-14"

KW = {
    'protocol-consensus': ['xrpl', 'xrp', 'ledger', 'consensus', 'validator', 'unl', 'rippled', 'reserve', 'fee',
                           'amendment', 'protocol'],
    'transactions': ['transaction', 'tx', 'sign', 'submit', 'sequence', 'autofill', 'multisign', 'ticket', 'batch',
                     'memo', 'flags', 'delegate'],
    'tokens': ['token', 'iou', 'trustline', 'trust', 'issue', 'currency', 'mpt', 'freeze', 'clawback', 'rippling',
               'issued'],
    'stablecoins-institutional': ['stablecoin', 'rlusd', 'institutional', 'rwa', 'tokenized', 'compliance', 'issuer'],
    'dex-amm': ['dex', 'amm', 'offer', 'orderbook', 'liquidity', 'pool', 'swap', 'pathfinding', 'exchange', 'trade',
                'autobridge'],
    'nfts': ['nft', 'nftoken', 'mint', 'xls20', 'collection', 'royalty', 'brokered', 'taxon'],
    'programmability-hooks': ['hook', 'hooks', 'xahau', 'sethook', 'smartcontract', 'programmable'],
    'programmability-evm': ['evm', 'sidechain', 'solidity', 'contract', 'bridge', 'axelar', 'hardhat', 'foundry',
                            'metamask', 'wxrp'],
    'payments-advanced': ['payment', 'escrow', 'paychan', 'channel', 'check', 'micropayment', 'streaming', 'crosscurrency',
                          'destinationtag'],
    'identity-compliance': ['did', 'credential', 'identity', 'kyc', 'permissioned', 'domain', 'depositauth', 'flags',
                            'compliance', 'verify'],
    'client-libraries': ['library', 'sdk', 'xrpljs', 'xrplpy', 'xrpl4j', 'codec', 'keypair', 'wallet', 'faucet',
                         'javascript', 'python', 'java'],
    'infrastructure-tooling': ['rippled', 'clio', 'node', 'explorer', 'oracle', 'indexer', 'infrastructure', 'devnet',
                               'testnet', 'api', 'xrpscan', 'bithomp', 'xaman', 'gemwallet'],
}
TRACK_KW = {
    'game-economies': ['game', 'economy', 'economies', 'currency', 'token', 'sink', 'faucet', 'ingame', 'mpt', 'rlusd',
                       'softcurrency'],
    'nft-assets': ['nft', 'asset', 'marketplace', 'mint', 'collectible', 'item', 'gameasset', 'royalty', 'trade'],
    'payments': ['payment', 'micropayment', 'payout', 'channel', 'escrow', 'tip', 'transfer', 'streaming'],
    'identity-compliance': ['identity', 'did', 'credential', 'kyc', 'compliance', 'player', 'account', 'permissioned',
                            'region', 'gate'],
}
TRACK_LABEL = {'game-economies': 'Game token economies', 'nft-assets': 'NFT game assets & marketplaces',
               'payments': 'Payments & micropayments', 'identity-compliance': 'Identity & compliance'}


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
    date = dr[0] if dr else DATE_FALLBACK
    wave = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()[0]
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUTDIR, exist_ok=True)
    entries = []

    t, l = est(os.path.join(ROOT, "catalog", "README.md"))
    entries.append({"id": "catalog-index", "path": "catalog/README.md",
                    "keywords": ["xrpl", "xrp", "ledger", "ripple", "catalog", "loadout"], "patterns": [],
                    "priority": "core",
                    "summary": "XRPL catalog index: decisive-axis (what's mainnet-live), the feature domains + the four build-focus folders.",
                    "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    for cat in cats:
        full = os.path.join(ROOT, "catalog", cat["slug"] + ".md")
        if not os.path.exists(full):
            continue
        n = c.execute("SELECT COUNT(*) FROM capabilities WHERE category_id=?", (cat["id"],)).fetchone()[0]
        t, l = est(full)
        kw = list(KW.get(cat["slug"], []))
        for (nm,) in c.execute("SELECT name FROM capabilities WHERE category_id=? AND status='recommended' "
                               "ORDER BY download_priority LIMIT 4", (cat["id"],)):
            for w in re.split(r"[^a-z0-9]+", (nm or "").lower()):
                if len(w) > 3 and w not in kw:
                    kw.append(w)
        summ = f"{cat['name']}: {n} capabilities. {cat['description']}"[:120]
        entries.append({"id": cat["slug"], "path": f"catalog/{cat['slug']}.md", "keywords": kw, "patterns": [],
                        "priority": "domain", "summary": summ,
                        "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # the four build-focus track folders
    for track, kw in TRACK_KW.items():
        full = os.path.join(ROOT, "catalog", f"track-{track}.md")
        if not os.path.exists(full):
            continue
        n = c.execute("""SELECT COUNT(DISTINCT cap.id) FROM capability_purposes cp JOIN purposes p ON p.id=cp.purpose_id
                         JOIN capabilities cap ON cap.id=cp.capability_id WHERE p.track=?""", (track,)).fetchone()[0]
        t, l = est(full)
        entries.append({"id": f"track-{track}", "path": f"catalog/track-{track}.md", "keywords": kw, "patterns": [],
                        "priority": "domain",
                        "summary": f"Build-focus: {TRACK_LABEL[track]} — {n} capabilities across feature domains."[:120],
                        "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # wave docs
    for wid, wpath, kws, summ in [
        (f"wave-{wave:02d}-dispatch", "readout/waves.md",
         ["wave", "dispatch", "research", "log", "how", "built", "swarm"],
         "Wave dispatches: how this KB was built, wave by wave."),
        (f"wave-{wave:02d}-verification", "readout/verification.md",
         ["verify", "verification", "verifier", "trust", "source", "citation", "crossfamily", "confirmed"],
         "Verification receipt: the cross-family + retrieval-oracle trust trail."),
    ]:
        full = os.path.join(ROOT, wpath.replace("/", os.sep))
        if not os.path.exists(full):
            continue
        t, l = est(full)
        entries.append({"id": wid, "path": wpath, "keywords": kws, "patterns": [], "priority": "domain",
                        "summary": summ[:120], "triggers": {"task": True, "plan": True, "edit": False},
                        "tokens_est": t, "lines": l})

    # manual — raw json, never auto-loaded
    full = os.path.join(ROOT, "waves", f"wave-{wave:02d}-foundation", "research-raw.json")
    if os.path.exists(full):
        t, l = est(full)
        entries.append({"id": f"wave-{wave:02d}-raw", "path": f"waves/wave-{wave:02d}-foundation/research-raw.json",
                        "keywords": ["raw", "json"], "patterns": [], "priority": "manual",
                        "summary": "Raw verified wave swarm output (large) — manual lookup only.",
                        "triggers": {"task": False, "plan": False, "edit": False}, "tokens_est": t, "lines": l})

    core = sum(e["tokens_est"] for e in entries if e["priority"] == "core")
    ondemand = sum(e["tokens_est"] for e in entries if e["priority"] != "core")
    domain_toks = sorted((e["tokens_est"] for e in entries if e["priority"] == "domain"), reverse=True)
    avg = core + sum(domain_toks[:2])
    index = {"version": "1.0.0", "generated": date + "T00:00:00Z",
             "source": f"xrpl.db (wave {wave})", "lazyLoad": True,
             "budget": {"always_loaded_est": core, "on_demand_total_est": ondemand,
                        "avg_task_load_est": avg, "avg_task_load_observed": None},
             "entries": entries}
    with open(os.path.join(OUTDIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    con.close()
    print(f"loadout index: {len(entries)} entries — core {core} tok always-on, {ondemand} tok on-demand, "
          f"~{avg} tok/typical task. -> .claude/loadout/index.json")


if __name__ == "__main__":
    main()
