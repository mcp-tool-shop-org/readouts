#!/usr/bin/env python3
"""gen_root_index.py (shared) — the MONOREPO front door for readouts, designed agent-first.

Parallel to gen_root_loadout.py: that emits the root ai-loadout index (routes a task to the right KB);
this emits the root READOUT — readouts/index.{html,md,json} — the agent-first home that links each KB's
own front door (<kb>/readout/index.html) with its stamp stats (domains / entries / verified / waves).

Counts derive fresh from each KB's DB; the descriptive copy (noun / what / decisive axis) comes from the KB's
profile, falling back to its own readout/index.json so a future profile-less KB still appears. Re-run after a
wave or after adding a KB (wired into every KB's scripts/regen.py AND the top-level regen.py):
    python shared/gen_root_index.py

Standards compliance (.claude/rules/workflow-standards.md), 0-3:
  PIN_PER_STEP 3 — every artifact derives from the DBs (counts) + pinned profiles; index.{html,md,json} carry
    the generated date + per-KB wave count, so the same DBs reproduce the same front door.
  EXTERNAL_VERIFIER 3 — this generator is NOT self-verified: the output is checked by a signal independent of
    the code (render headless + READ the PNG, the look-at-output rule) plus `ai-loadout validate` on the routing
    index it advertises. Counts shown here equal each KB's own DB-derived index.json (cross-checkable).
  ANDON_AUTHORITY 2 — a missing/locked DB or absent KB folder is skipped (not fabricated); a profile-less KB
    degrades to its readout/index.json rather than emitting wrong numbers.
  NAMED_COMPENSATORS N/A — read-only generator; writes only derived files at the repo root (index.{html,md,json}),
    each fully regenerated from source. Undo = re-run regen, or `git checkout -- index.*`.
  DECOMPOSE_BY_SECRETS 3 — KB-specific schema lives in readout_profiles.py; this file holds only root-level,
    KB-agnostic aggregation (the part that does NOT change when a KB's columns change).
  UNCERTAINTY_GATED_HUMANS 3 — the OUTWARD-FACING act (publishing this page) is gated to Mike's explicit
    sign-off (kickoff objective 2); the generator itself only writes inside the private repo.
"""
import glob, json, base64, io, os, sys, sqlite3, datetime
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from readout_profiles import PROFILES
ROOT = os.path.dirname(SCRIPT_DIR)  # shared/ -> readouts/
LOGO = os.path.join(SCRIPT_DIR, "readout", "assets", "readouts-logo.png")
try:  # py3.14 parent console is cp1252; keep our own prints UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

MONOREPO_WHAT = ("A monorepo of verified, ai-loadout-routed SQLite knowledge bases for the studio. Each KB grows in "
                 "waves of parallel research cross-checked by an adversarial retrieval verifier — full per-wave "
                 "provenance, every fact flagged verified, two-level progressive-disclosure routing so an agent reads "
                 "only the slice it needs, never the whole corpus.")


def logo_data_uri(h=80):
    try:
        from PIL import Image
        im = Image.open(LOGO).convert("RGBA"); w = int(im.width * h / im.height)
        im = im.resize((w, h), Image.LANCZOS); buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


def esc(s): return ("" if s is None else str(s)).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def clip(s, n=118):  # truncate at a word boundary so a table cell never cuts mid-word ("…/ Wind")
    s = "" if s is None else str(s)
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(" ,;:—-/") + "…"


def pick_db(kb_dir):
    """The KB's real DB — the largest file that actually holds tables.

    Not `glob(...)[0]`: a stray empty sibling sorts ahead of the real DB and silently
    zeroes that KB on the front door. training-knowledge/recipes.db (0 bytes, committed
    by accident) shadowed training.db exactly this way and reported 0 of 127 entries.
    """
    best = None
    for path in sorted(glob.glob(os.path.join(kb_dir, "*.db"))):
        if os.path.getsize(path) == 0:
            continue
        try:
            con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
            n = con.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
            con.close()
        except Exception:
            continue
        if n and (best is None or os.path.getsize(path) > os.path.getsize(best)):
            best = path
    return best


def _front_door(name, kb_dir):
    """Links to the KB's readout, or to the folder when it has no readout profile.

    Only KBs with a profile in readout_profiles.py get readout/index.{html,md,json};
    the rest are lean catalog+loadout KBs and gen_readout.py skips them by design.
    Emitting the links unconditionally put six dead entries on the front door.
    """
    have = os.path.isfile(os.path.join(kb_dir, "readout", "index.html"))
    if have:
        return dict(index_html=f"{name}/readout/index.html",
                    index_md=f"{name}/readout/index.md",
                    index_json=f"{name}/readout/index.json")
    return dict(index_html=f"{name}/",
                index_md=f"{name}/catalog/README.md",
                index_json=f"{name}/.claude/loadout/index.json")


def kb_stats(name, kb_dir):
    """One KB's front-door stats — counts FRESH from its DB, copy from its profile (fallback: readout/index.json)."""
    db_path = pick_db(kb_dir)
    if not db_path:
        return None
    db_name = os.path.basename(db_path)
    prof = PROFILES.get(db_name) or {}
    side = {}
    sidecar = os.path.join(kb_dir, "readout", "index.json")  # the KB's own front-door json (DB-derived by gen_index.py)
    if os.path.exists(sidecar):
        try:
            side = json.load(open(sidecar, encoding="utf-8"))
        except Exception:
            side = {}
    noun = prof.get("noun") or side.get("noun") or "entries"
    what = prof.get("what") or side.get("what") or ""
    axis = prof.get("axis") or side.get("decisive_axis") or ""
    kb_label = prof.get("kb") or name
    T = prof.get("table")

    waves = entries = verified = sources = domains = 0
    try:
        con = sqlite3.connect(db_path); cur = con.cursor()
        if not T:  # profile-less KB: discover the primary table the way gen_root_loadout.py does
            for cand in ("engines", "models", "techniques", "recipes", "findings", "capabilities"):
                try:
                    cur.execute(f"SELECT 1 FROM {cand} LIMIT 1"); T = cand; break
                except Exception:
                    pass
        if T:
            entries = cur.execute(f"SELECT count(*) FROM {T}").fetchone()[0]
            verified = cur.execute(f"SELECT count(*) FROM {T} WHERE verified=1").fetchone()[0]
            domains = cur.execute(f"SELECT count(DISTINCT category_id) FROM {T}").fetchone()[0]
        try:
            waves = cur.execute("SELECT count(*) FROM waves").fetchone()[0]
        except Exception:
            pass
        # Two KBs name this table `finding_sources`; querying only `sources` threw,
        # the bare except swallowed it, and both published "0 sources" on the front
        # door — understating the corpus by 318 citations.
        for tbl in ("sources", "finding_sources"):
            try:
                sources = cur.execute(f"SELECT count(*) FROM {tbl}").fetchone()[0]
                break
            except Exception:
                continue
        con.close()
    except Exception:  # DB unreadable/locked → fall back to the KB's own front-door totals rather than fabricate
        tot = side.get("totals", {})
        entries = tot.get(noun) or tot.get("engines") or tot.get("models") or 0
        verified = tot.get("verified", 0); sources = tot.get("sources", 0)
        domains = tot.get("domains", 0); waves = side.get("waves", 0)

    return dict(name=name, kb=kb_label, noun=noun, what=what, axis=axis,
                domains=domains, entries=entries, verified=verified, sources=sources, waves=waves,
                fts=f"{T}_fts" if T else None, db=f"{name}/{db_name}",
                **_front_door(name, kb_dir))



def main():
    kbs = []
    for name in sorted(os.listdir(ROOT)):  # alphabetical, deterministic — matches gen_root_loadout.py + the README
        kb_dir = os.path.join(ROOT, name)
        if not os.path.isdir(kb_dir) or name.startswith(".") or name == "shared":
            continue
        # a KB = any subfolder with its own loadout index + at least one .db file (same gate as gen_root_loadout.py)
        if not os.path.exists(os.path.join(kb_dir, ".claude", "loadout", "index.json")):
            continue
        s = kb_stats(name, kb_dir)
        if s:
            kbs.append(s)
    generated = datetime.date.today().isoformat()
    totals = dict(knowledge_bases=len(kbs), entries=sum(k["entries"] for k in kbs),
                  verified=sum(k["verified"] for k in kbs), sources=sum(k["sources"] for k in kbs),
                  domains=sum(k["domains"] for k in kbs), waves=sum(k["waves"] for k in kbs))
    index = dict(what=MONOREPO_WHAT, generated=generated, totals=totals, knowledge_bases=kbs,
                 route=dict(loadout="ai-loadout resolve --project .",
                            root_loadout=".claude/loadout/index.json",
                            per_kb="<kb>/readout/index.{html,md,json}"))

    # ---- index.json (programmatic monorepo map) ----
    open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8").write(json.dumps(index, ensure_ascii=False, indent=2))

    # ---- index.md (agent-first text map) ----
    md = ["# readouts\n",
          f"> {MONOREPO_WHAT}\n>\n> **{totals['knowledge_bases']} knowledge bases · {totals['entries']} entries · "
          f"{totals['verified']} verified · {totals['domains']} domains · {totals['waves']} waves · "
          f"generated {generated}.**\n",
          "## Knowledge bases\n",
          "| Knowledge base | What | Domains | Entries | Verified | Waves | Front door |",
          "|---|---|--:|--:|--:|--:|---|"]
    for k in kbs:
        md.append(f"| [{k['kb']}]({k['index_html']}) | {k['what']} | {k['domains']} | {k['entries']} {k['noun']} | "
                  f"{k['verified']}/{k['entries']} | {k['waves']} | [index.md]({k['index_md']}) · "
                  f"[json]({k['index_json']}) |")
    md.append("\n## For agents\n")
    md.append("- **Route to the right KB:** `ai-loadout resolve --project .` — the root loadout picks "
              "the KB, then the KB's own loadout picks the domain slice (two-level progressive disclosure; the corpus "
              "is never dumped whole).")
    md.append("- **Each KB's front door:** `<kb>/readout/index.md` (text map) · `index.json` (programmatic) · "
              "`index.html` (branded landing).")
    md.append("- **Query a KB directly** — open its SQLite DB (views `v_recommended`, `v_best_for`; FTS `<table>_fts`):")
    for k in kbs:
        md.append(f"  - `{k['db']}` — FTS `{k['fts']}`")
    md.append("- **Programmatic monorepo map:** `index.json` (the data backing this page).\n")
    md.append("## How each KB decides\n")
    for k in kbs:
        md.append(f"- **{k['kb']}** — decisive axis: {k['axis']}")
    md.append("\n## Provenance\n")
    md.append(f"Every fact in every KB carries a **wave id** and a **verified** flag. Sources are retrieval-checked "
              f"against the live page; some waves add a cross-family seat, and each wave's own receipt says "
              f"which — see `waves.verifier_note`. Family-different verification across every wave is the "
              f"planned upgrade, not the current state. {totals['waves']} research waves "
              f"across {totals['knowledge_bases']} knowledge bases; {totals['verified']}/{totals['entries']} entries "
              f"verified.\n")
    open(os.path.join(ROOT, "index.md"), "w", encoding="utf-8").write("\n".join(md))

    # ---- index.html (branded landing — same navy+blue brand as the per-KB index, single logo) ----
    rows = "".join(
        f'<tr><td><a href="{k["index_html"]}" title="{esc(k["axis"])}">{esc(k["kb"])}</a>'
        f'<div class="d">{esc(clip(k["what"]))}</div></td>'
        f'<td class="n">{k["domains"]}</td>'
        f'<td class="n">{k["entries"]}<div class="d" style="text-align:right">{esc(k["noun"])}</div></td>'
        f'<td class="n"><span class="v">{k["verified"]}</span>/{k["entries"]}</td>'
        f'<td class="n">{k["waves"]}</td>'
        f'<td><a class="go" href="{k["index_html"]}">open ↗</a></td></tr>' for k in kbs)
    axes = "".join(f'<li><b>{esc(k["kb"])}</b> — {esc(k["axis"])}</li>' for k in kbs)
    payload = json.dumps(index, ensure_ascii=False).replace("</", "<\\/")
    html = ROOT_HTML
    for key, val in {"__LOGO__": logo_data_uri(), "__WHAT__": esc(MONOREPO_WHAT), "__GEN__": generated,
                     "__KBN__": str(totals["knowledge_bases"]), "__ENT__": str(totals["entries"]),
                     "__VER__": str(totals["verified"]), "__NDOM__": str(totals["domains"]),
                     "__WAVES__": str(totals["waves"]), "__ROWS__": rows, "__AXES__": axes,
                     "__DATA__": payload}.items():
        html = html.replace(key, val)
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)

    print(f"root index: {len(kbs)} KB(s), {totals['entries']} entries ({totals['verified']} verified), "
          f"{totals['domains']} domains, {totals['waves']} waves -> index.{{html,md,json}}")


ROOT_HTML = """<!doctype html><html lang="en" data-theme="dark"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>readouts — knowledge bases</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0f1f;--panel:#111a30;--panel2:#0d1526;--border:#22304f;--fg:#e8edf6;--muted:#93a1bd;--faint:#62719455;
--blue:#5aa6e8;--sky:#8fc4e8;--accent:#5aa6e8;--grad:linear-gradient(90deg,#2f6fb0,#8fc4e8);--ok:#46c98b;--bad:#ef6b6b;--cond:#7da6d9;
--mono:ui-monospace,"Cascadia Mono",Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
[data-theme="light"]{--bg:#f7f8fb;--panel:#fff;--panel2:#eef2f8;--border:#dbe2ee;--fg:#13203a;--muted:#56648a;--faint:#8492ad55;--accent:#2f6fb0;--grad:linear-gradient(90deg,#1f4f86,#5aa6e8)}
body{background:var(--bg);color:var(--fg);font-family:var(--sans);line-height:1.55}
.wrap{max-width:980px;margin:0 auto;padding:0 24px}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
header{border-bottom:1px solid var(--border);background:linear-gradient(180deg,var(--panel),transparent)}
.head{display:flex;align-items:center;gap:12px;padding:22px 0}.brand{display:flex;align-items:center;gap:12px}.head img{height:40px}
.sweep{height:3px;width:60px;border-radius:2px;background:var(--grad)}.spacer{flex:1}
.pill{font:600 12px var(--sans);padding:7px 11px;border:1px solid var(--border);border-radius:999px;color:var(--muted);background:var(--panel);cursor:pointer}
.eyebrow{font:700 11px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:22px 0 4px}
h1{font-size:30px;font-weight:750;letter-spacing:-.02em;margin:0 0 6px;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.what{color:var(--muted);font-size:15px;max-width:760px;margin-bottom:14px}
.stamps{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}.stamp{font:600 11px var(--mono);padding:6px 9px;border-radius:7px;background:var(--panel);border:1px solid var(--border);color:var(--muted)}.stamp b{color:var(--fg)}.stamp .v{color:var(--ok)}
.agent{border:1px solid var(--border);border-left:3px solid var(--accent);background:var(--panel2);border-radius:8px;padding:13px 15px;margin-bottom:24px;font-size:13.5px;color:var(--muted)}
.agent b{color:var(--fg)}.agent code{font:600 12px var(--mono);color:var(--sky);background:#8fc4e814;padding:1px 6px;border-radius:5px}
h2{font-size:13px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin:26px 0 12px;display:flex;align-items:center;gap:10px}h2::after{content:"";flex:1;height:1px;background:var(--border)}
table{width:100%;border-collapse:collapse}th{text-align:left;font:700 11px var(--sans);letter-spacing:.05em;text-transform:uppercase;color:var(--muted);padding:9px 12px;border-bottom:1px solid var(--border)}
td{padding:13px 12px;border-bottom:1px solid var(--border);font-size:14px;vertical-align:top}td.n{font:700 13px var(--mono);text-align:right;color:var(--fg)}td .v{color:var(--ok)}td .d{color:var(--faint);font-size:12px;margin-top:3px;font-family:var(--sans);font-weight:400}.go{font:700 12px var(--sans);white-space:nowrap}
ul.axes{list-style:none}ul.axes li{font-size:13.5px;padding:9px 0;border-bottom:1px solid var(--border);color:var(--muted)}ul.axes li:last-child{border-bottom:0}ul.axes b{color:var(--fg);font:700 12px var(--mono)}
footer{border-top:1px solid var(--border);margin-top:34px;padding:20px 0 44px;color:var(--muted);font-size:13px}.prov{display:flex;gap:9px;align-items:center;margin-bottom:8px}
</style></head><body>
<header><div class="wrap"><div class="head"><span class="brand"><img src="__LOGO__" alt="readouts"><span class="sweep"></span></span><span class="spacer"></span><button class="pill" onclick="var h=document.documentElement;h.dataset.theme=h.dataset.theme==='dark'?'light':'dark'">◐ theme</button></div></div></header>
<div class="wrap">
<div class="eyebrow">monorepo</div>
<h1>Knowledge bases</h1>
<p class="what">__WHAT__</p>
<div class="stamps"><span class="stamp">knowledge bases <b>__KBN__</b></span><span class="stamp">entries <b>__ENT__</b></span><span class="stamp">verified <span class="v">__VER__</span></span><span class="stamp">domains <b>__NDOM__</b></span><span class="stamp">waves <b>__WAVES__</b></span><span class="stamp">generated <b>__GEN__</b></span></div>
<div class="agent">▣ <b>For agents:</b> this is the monorepo front door. The machine-readable map is the <code>#readouts-root</code> JSON island at the foot of this page; a plain-text version is <a href="index.md"><code>index.md</code></a>. Route a task with <code>ai-loadout resolve --project .</code> — the root loadout picks the KB, then each KB's own loadout picks the domain. Per-KB front doors: <code>&lt;kb&gt;/readout/index.md</code>.</div>
<h2>Knowledge bases</h2>
<table><thead><tr><th>Knowledge base</th><th style="text-align:right">Domains</th><th style="text-align:right">Entries</th><th style="text-align:right">Verified</th><th style="text-align:right">Waves</th><th></th></tr></thead><tbody>__ROWS__</tbody></table>
<h2>How each KB decides <span style="color:var(--faint);text-transform:none;letter-spacing:0;font-weight:400">— the decisive axis per knowledge base</span></h2>
<ul class="axes">__AXES__</ul>
</div>
<footer><div class="wrap"><div class="prov"><span class="sweep"></span><span>Every fact in every KB carries a <b>wave id</b> and a <b>verified</b> flag; sources retrieval-checked against the live page. Cross-family seats are per-wave — see each wave's receipt.</span></div><div>readouts · __KBN__ knowledge bases · __ENT__ entries (__VER__ verified) · __NDOM__ domains · __WAVES__ waves · generated __GEN__ · one map, three views: index.html · index.md · index.json.</div></div></footer>
<script id="readouts-root" type="application/json">__DATA__</script>
</body></html>"""

if __name__ == "__main__":
    main()
