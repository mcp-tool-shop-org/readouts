#!/usr/bin/env python3
"""ingest_proofs.py — record xrpl-lab on-ledger receipts (txids) into xrpl.db as the v_proven tier.

The proof-by-artifact loop: a capability the KB says is "mainnet-live / cross-family verified" becomes
"proven-on-ledger" once an xrpl-lab module executes it and produces a real txid. This reads an xrpl-lab
proof-pack JSON (xrpl_lab_proof_pack.json) OR a single manual receipt, maps the xrpl-lab module -> the KB
capability it proves, and upserts into the `proofs` table. NOT wave-scoped — load_db never touches proofs,
so on-ledger proofs survive every re-ingestion.

Verification tiers, weakest to strongest: research-verified < retrieval-confirmed < PROVEN-ON-LEDGER.

Usage:
  $env:PYTHONUTF8='1'; python scripts/ingest_proofs.py <proof_pack.json>
  python scripts/ingest_proofs.py --capability <slug> --txid <hash> [--network testnet] [--module <id>] \
                                  [--explorer <url>] [--date <iso>]
"""
import json
import os
import sqlite3
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "xrpl.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

# xrpl-lab module id -> KB capability slug (the capability the module proves). Ideally each module
# carries `kb_source: <slug>` in its frontmatter; this map covers the shipped KB-sourced modules.
MODULE_CAPABILITY = {
    "nft_minting_101": "nftokenmint",
    "mpt_issuance_101": "mpt-issuance-create-config",
    "escrow_101": "escrow-xrp",
    "did_101": "did-transactions",
}


def _con():
    con = sqlite3.connect(DB)
    with open(SCHEMA, encoding="utf-8") as f:
        con.executescript(f.read())  # idempotent — ensures proofs table + v_proven exist
    con.row_factory = sqlite3.Row
    return con


def record(cur, slug, txid, network, explorer_url, module_id, date):
    if not slug or not txid:
        return 0
    if not cur.execute("SELECT 1 FROM capabilities WHERE slug=?", (slug,)).fetchone():
        print(f"  ! no capability '{slug}' in xrpl.db — skipping txid {txid[:12]}")
        return 0
    cur.execute(
        """INSERT OR IGNORE INTO proofs(capability_slug,txid,network,explorer_url,module_id,proved_date)
           VALUES(?,?,?,?,?,?)""",
        (slug, txid, network, explorer_url, module_id, date),
    )
    return cur.rowcount


def from_proof_pack(cur, path):
    pack = json.load(open(path, encoding="utf-8"))
    network = pack.get("network", "")
    date = pack.get("generated") or pack.get("date") or ""
    n = 0
    for m in pack.get("modules", []):
        mid = m.get("module_id", "")
        slug = MODULE_CAPABILITY.get(mid)
        if not slug:
            print(f"  ! no capability mapping for module '{mid}' — skipping")
            continue
        urls = m.get("explorer_urls", []) or []
        for i, txid in enumerate(m.get("txids", []) or []):
            url = urls[i] if i < len(urls) else ""
            n += record(cur, slug, txid, network, url, mid, date)
    return n


def main(argv):
    con = _con()
    cur = con.cursor()
    if "--capability" in argv:
        def g(k, d=""):
            return argv[argv.index(k) + 1] if k in argv else d
        n = record(cur, g("--capability"), g("--txid"), g("--network", "testnet"),
                   g("--explorer"), g("--module"), g("--date"))
    elif argv and not argv[0].startswith("--"):
        n = from_proof_pack(cur, argv[0])
    else:
        con.close()
        sys.exit("usage: ingest_proofs.py <proof_pack.json> | --capability <slug> --txid <hash> [...]")
    con.commit()
    print(f"recorded {n} new proof(s).")
    rows = cur.execute("SELECT name, network_status, txid, network FROM v_proven").fetchall()
    print(f"v_proven ({len(rows)}):")
    for r in rows:
        print(f"  ● {r['name']}  [{r['network_status']}]  proven on {r['network']}  txid {r['txid'][:24]}...")
    con.close()


if __name__ == "__main__":
    main(sys.argv[1:])
