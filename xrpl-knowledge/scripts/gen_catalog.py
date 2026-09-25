#!/usr/bin/env python3
"""Generate human-readable catalog/*.md from xrpl.db. Re-run after each wave (regen.py calls it):
    $env:PYTHONUTF8='1'; python scripts/gen_catalog.py
DB-only (no dependency on the raw swarm json) so it always reflects current DB state.
NEVER hand-edit catalog/*.md — they are regenerated from the DB.

Two folder families, both first-class:
  catalog/<feature-domain>.md  — the FEATURE domains (ingest backbone): protocol, tx, tokens, ...
  catalog/track-<folder>.md    — the four BUILD-FOCUS folders (cross-cutting): game-economies,
                                 nft-assets, payments, identity-compliance.
catalog/README.md leads with the decisive axis (what's actually mainnet-live) then both folder families.
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "xrpl.db")
OUT = os.path.join(ROOT, "catalog")

NET = {"mainnet-live": "● live", "amendment-pending": "◐ pending", "testnet-devnet": "○ devnet",
       "deprecated": "× deprecated", "n/a": "· n/a"}
STATUS_ORDER = {"recommended": 0, "situational": 1, "legacy": 2, "avoid": 3}
TRACKS = [("game-economies", "Game token economies"), ("nft-assets", "NFT game assets & marketplaces"),
          ("payments", "Payments & micropayments"), ("identity-compliance", "Identity & compliance")]


def cell(s):
    return ("" if s is None else str(s)).replace("|", "/").replace("\n", " ").strip()


def netlbl(s):
    return NET.get(s, cell(s) or "· ?")


def caps_in_category(c, cat_id):
    rows = c.execute("SELECT * FROM capabilities WHERE category_id=? ORDER BY download_priority, name", (cat_id,)).fetchall()
    return sorted(rows, key=lambda x: (STATUS_ORDER.get(x["status"], 9),
                                       x["download_priority"] if x["download_priority"] is not None else 999,
                                       (x["name"] or "").lower()))


def detail_block(c, t):
    L = [f"### {t['name']} · `{t['kind'] or '?'}` · {netlbl(t['network_status'])}{' ✓' if t['verified'] else ''}"]
    if t["summary"]:
        L.append(t["summary"])
    meta = []
    for label, key in [("Chain", "chain"), ("XLS", "xls_standard"), ("Amendment", "amendment_name"),
                       ("Enabled", "enabled_date"), ("Maturity", "maturity_tier"), ("Use", "status")]:
        if t[key]:
            meta.append(f"**{label}:** {t[key]}")
    if meta:
        L.append("- " + " · ".join(meta))
    if t["key_fields"]:
        L.append(f"- **Key fields / API:** {t['key_fields']}")
    if t["gotchas"]:
        L.append(f"- **Gotchas:** {t['gotchas']}")
    # Link only tracks that actually get a page. purposes.track holds 28 distinct
    # values because category slugs and ad-hoc strings leaked into it during ingest
    # (dex-amm, transactions, devops, defi-liquidity...), while TRACKS - the four
    # curated build-focus folders - is the authoritative list and the only one
    # write_track() emits pages for. Linking the raw column produced dead links to
    # track-defi-liquidity.md and friends. The stray values are an ingest defect
    # worth normalising separately; this keeps the artifact honest meanwhile.
    known = {slug for slug, _ in TRACKS}
    tracks = [r[0] for r in c.execute(
        """SELECT DISTINCT p.track FROM capability_purposes cp JOIN purposes p ON p.id=cp.purpose_id
           WHERE cp.capability_id=? AND p.track IS NOT NULL ORDER BY p.track""", (t["id"],))
        if r[0] in known]
    if tracks:
        L.append("- **Build-focus tracks:** " + ", ".join(f"[{tr}](track-{tr}.md)" for tr in tracks))
    bf = c.execute(
        """SELECT p.name pn, p.track tr, cp.fitness f FROM capability_purposes cp JOIN purposes p ON p.id=cp.purpose_id
           WHERE cp.capability_id=? AND p.track IS NULL ORDER BY (cp.fitness IS NULL), cp.fitness DESC""", (t["id"],)).fetchall()
    if bf:
        L.append("- **Best for:** " + " ; ".join(
            f"{cell(x['pn'])}{(' (' + x['tr'] + ')') if x['tr'] else ''}{(', fit ' + str(x['f'])) if x['f'] is not None else ''}" for x in bf))
    if t["verify_note"]:
        L.append(f"- **Verify:** {t['verify_note']}")
    srcs = c.execute("SELECT title,url,claim FROM sources WHERE capability_id=? ORDER BY id", (t["id"],)).fetchall()
    if srcs:
        L.append("- **Sources:** " + " ; ".join(
            f"[{cell(s['title'] or 'source')}]({s['url']})" + (f" — {cell(s['claim'])}" if s["claim"] else "") for s in srcs))
    L.append("")
    return L


def write_cat(c, cat, wave, date):
    rows = caps_in_category(c, cat["id"])
    ver = sum(1 for t in rows if t["verified"])
    live = sum(1 for t in rows if t["network_status"] == "mainnet-live")
    L = [f"# {cat['name']}",
         f"_{cat['description']}_ · wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} capabilities · {live} mainnet-live · {ver} cross-family verified.\n",
         "| ↓ | Capability | Kind | Network | Chain | XLS | Fit | Use | ✓ |",
         "|---|------------|------|---------|-------|-----|-----|-----|---|"]
    for t in rows:
        L.append(f"| {t['download_priority'] or ''} | {cell(t['name'])} | {cell(t['kind'])} | {netlbl(t['network_status'])} | "
                 f"{cell(t['chain'])} | {cell(t['xls_standard'])} | {t['builder_fit'] if t['builder_fit'] is not None else '-'} | "
                 f"{cell(t['status'])} | {'✓' if t['verified'] else '·'} |")
    L.append("\n## Detail\n")
    for t in rows:
        L += detail_block(c, t)
    with open(os.path.join(OUT, cat["slug"] + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def _track_table(rows):
    L = ["| Capability | Feature domain | Kind | Network | Fit | ✓ |",
         "|------------|----------------|------|---------|-----|---|"]
    for t in rows:
        L.append(f"| [{cell(t['name'])}]({cell(t['catslug'])}.md) | {cell(t['catname'])} | {cell(t['kind'])} | "
                 f"{netlbl(t['network_status'])} | {t['fit'] if t['fit'] is not None else '-'} | {'✓' if t['verified'] else '·'} |")
    return L


def write_track(c, track, label, wave, date):
    # MAX(fitness) per capability; a capability is "curated" if a DEPTH wave (wave_id >= 2) tagged it for this
    # track, vs "broader" if only the foundation wave (1) did. Depth waves OWN folder curation; the foundation
    # wave is generous context. Curated rides on top; broader follows.
    rows = c.execute(
        """SELECT cap.*, ct.name catname, ct.slug catslug, MAX(cp.fitness) fit
           FROM capability_purposes cp
           JOIN purposes p       ON p.id=cp.purpose_id
           JOIN capabilities cap ON cap.id=cp.capability_id
           JOIN categories ct    ON ct.id=cap.category_id
           WHERE p.track=? GROUP BY cap.id
           ORDER BY (fit IS NULL), fit DESC, cap.name""", (track,)).fetchall()
    curated = [t for t in rows if (t["wave_id"] or 0) >= 2]
    broader = [t for t in rows if (t["wave_id"] or 0) < 2]
    ver = sum(1 for t in rows if t["verified"])
    live = sum(1 for t in rows if t["network_status"] == "mainnet-live")
    L = [f"# Build-focus: {label}",
         f"_The XRPL capabilities you assemble for **{label.lower()}** — across every feature domain._ · "
         f"wave {wave} · {date} · [‹ catalog index](README.md)\n",
         f"{len(rows)} capabilities ({len(curated)} depth-curated) · {live} mainnet-live · {ver} cross-family verified.\n"]
    if curated:
        L += ["## Curated — the building blocks",
              "_From the focused depth wave for this folder, ranked by builder fitness._\n"]
        L += _track_table(curated)
        L.append("")
    L += ["## Broader — also relevant",
          "_Tagged by the foundation wave (wide net). Curation happens in this folder's depth wave._\n"] if broader else []
    if broader:
        L += _track_table(broader)
    L.append("\n_Each capability's full detail (key fields, gotchas, sources) lives in its feature-domain readout, linked above._\n")
    with open(os.path.join(OUT, f"track-{track}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    wr = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()
    wave = wr[0] if wr and wr[0] is not None else 0
    dr = c.execute("SELECT value FROM meta WHERE key='updated'").fetchone()
    date = dr[0] if dr else ""
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    tot = c.execute("SELECT COUNT(*) FROM capabilities").fetchone()[0]
    totv = c.execute("SELECT COUNT(*) FROM capabilities WHERE verified=1").fetchone()[0]
    tots = c.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    os.makedirs(OUT, exist_ok=True)

    idx = [f"# Catalog — xrpl-knowledge\n",
           f"Generated from `xrpl.db` · wave {wave} · {date}. NEVER hand-edited — regenerated from the DB.\n",
           "The **XRP Ledger ecosystem for a builder** — protocol features, transaction types, XLS standards, client "
           "libraries and tooling — each tagged with its **current mainnet/amendment status** (the decisive axis). "
           "Whole-ecosystem: XRPL mainnet + Xahau/Hooks + the XRPL EVM sidechain + the institutional layer "
           "(RLUSD, compliance). Sibling KBs live in the same [readouts](../../index.md) monorepo.\n",
           f"**{tot} capabilities · {totv} cross-family verified · {tots} sources · wave {wave}.**\n"]

    # ---- Decisive axis: what's actually mainnet-live ----
    idx += ["## Decisive axis — what's live\n",
            "XRPL moves by amendment. The first question for any feature is whether it is **enabled on mainnet right "
            "now** vs amendment-pending vs devnet-only vs deprecated. Counts by `network_status`:\n",
            "| network_status | capabilities |", "|---|--:|"]
    for s, n in c.execute("SELECT network_status, COUNT(*) n FROM capabilities GROUP BY network_status ORDER BY (network_status<>'mainnet-live'), n DESC"):
        idx.append(f"| {netlbl(s)} | {n} |")
    idx.append("")

    # ---- Feature domains ----
    idx += ["## Feature domains\n", "The ingest backbone — every capability lives in exactly one.\n",
            "| Domain | Capabilities | Live | Verified |", "|---|--:|--:|--:|"]
    for cat in cats:
        rows = c.execute("SELECT verified, network_status FROM capabilities WHERE category_id=?", (cat["id"],)).fetchall()
        n = len(rows)
        if not n:
            continue
        live = sum(1 for r in rows if r["network_status"] == "mainnet-live")
        ver = sum(1 for r in rows if r["verified"])
        idx.append(f"| [{cell(cat['name'])}]({cat['slug']}.md) | {n} | {live} | {ver}/{n} |")
    idx.append("")

    # ---- Build-focus tracks (the four folders) ----
    idx += ["## Build-focus folders\n",
            "The four builder lenses — cross-cutting views that assemble the relevant capabilities from across the "
            "feature domains. **Curated** = tagged by that folder's focused depth wave (the building blocks); "
            "**total** also includes the foundation wave's wider net. A capability appears in every folder it serves.\n",
            "| Folder | Curated | Total | Live | Verified |", "|---|--:|--:|--:|--:|"]
    for track, label in TRACKS:
        rows = c.execute(
            """SELECT cap.verified, cap.network_status, cap.wave_id FROM capabilities cap
               WHERE cap.id IN (SELECT cp.capability_id FROM capability_purposes cp
                                JOIN purposes p ON p.id=cp.purpose_id WHERE p.track=?)""", (track,)).fetchall()
        n = len(rows)
        cur = sum(1 for r in rows if (r["wave_id"] or 0) >= 2)
        live = sum(1 for r in rows if r["network_status"] == "mainnet-live")
        ver = sum(1 for r in rows if r["verified"])
        idx.append(f"| [{label}](track-{track}.md) | {cur} | {n} | {live} | {ver}/{n} |")

    try:
        proven = c.execute(
            "SELECT name, category, network_status, txid, network, explorer_url FROM v_proven"
        ).fetchall()
    except sqlite3.OperationalError:
        proven = []
    if proven:
        idx += ["## Proven on-ledger\n",
                "Capabilities an [xrpl-lab](https://github.com/mcp-tool-shop-org/xrpl-lab) module has executed "
                "LIVE, with a real txid — the strongest verification tier "
                "(research-verified < retrieval-confirmed < proven-on-ledger).\n",
                "| Capability | Domain | Network | txid |", "|---|---|---|---|"]
        for p in proven:
            tx = cell(p["txid"])
            disp = f"[{tx[:18]}…]({p['explorer_url']})" if p["explorer_url"] else f"{tx[:18]}…"
            idx.append(f"| {cell(p['name'])} | {cell(p['category'])} | {cell(p['network'])} | {disp} |")
        idx.append("")

    idx += ["",
            "## Legend\n",
            "- **Network:** ● mainnet-live (amendment enabled) · ◐ amendment-pending · ○ testnet/devnet · × deprecated. "
            "The decisive axis — a builder ships against what's live.",
            "- **Kind:** concept · transaction · standard (XLS) · amendment · library · service · pattern.",
            "- **Fit:** builder usefulness 0–5. **Use:** recommended / situational / legacy / avoid.",
            "- **✓** cross-family verified: the AUTHORITATIVE seat is a large Ollama Cloud model (different family from "
            "the Claude researcher — no self-preference); a Claude+WebFetch retrieval oracle checks the live docs as "
            "seat 1. Blank/· = pending or unconfirmed.",
            "- **Chains:** xrpl-mainnet · xahau (Hooks) · xrpl-evm-sidechain · all."]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    for cat in cats:
        if c.execute("SELECT COUNT(*) FROM capabilities WHERE category_id=?", (cat["id"],)).fetchone()[0]:
            write_cat(c, cat, wave, date)
    for track, label in TRACKS:
        write_track(c, track, label, wave, date)
    con.close()
    print("catalog/ regenerated: README.md + "
          + ", ".join(cat["slug"] + ".md" for cat in cats
                      if True) + " + " + ", ".join(f"track-{t}.md" for t, _ in TRACKS))


if __name__ == "__main__":
    main()
