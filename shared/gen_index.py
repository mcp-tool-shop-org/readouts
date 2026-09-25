#!/usr/bin/env python3
"""gen_index.py (shared) — the readouts HOME for whichever KB is in cwd, designed agent-first.

Emits readout/index.{md,json,html} from engines.db OR models.db (profile-driven). Run after gen_readout.py.
  index.md   : clean LLM-readable text map      index.json : programmatic map
  index.html : branded landing, content in semantic markup + a JSON island (so get_page_text yields the map)
"""
import sqlite3, json, base64, io, os, sys, datetime
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from readout_profiles import detect
LOGO = os.path.join(SCRIPT_DIR, "readout", "assets", "readouts-logo.png")

def logo_data_uri(h=80):
    try:
        from PIL import Image
        im = Image.open(LOGO).convert("RGBA"); w = int(im.width*h/im.height)
        im = im.resize((w, h), Image.LANCZOS); buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception: return ""

def esc(s): return ("" if s is None else str(s)).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def comm_label(v): return {"yes": "commercial", "conditional": "conditional", "no": "non-commercial"}.get(v, "—")

def main():
    db_path, prof = detect()
    T, FK, kb, noun = prof["table"], prof["fk"], prof["kb"], prof["noun"]
    db = sqlite3.connect(db_path); db.row_factory = sqlite3.Row; c = db.cursor()
    waves = c.execute("SELECT count(*) FROM waves").fetchone()[0]
    tot = c.execute(f"SELECT count(*) FROM {T}").fetchone()[0]
    tot_ver = c.execute(f"SELECT count(*) FROM {T} WHERE verified=1").fetchone()[0]
    tot_src = c.execute("SELECT count(*) FROM sources").fetchone()[0]
    generated = datetime.date.today().isoformat()

    domains = []
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    for cat in cats:
        n = c.execute(f"SELECT count(*) FROM {T} WHERE category_id=?", (cat["id"],)).fetchone()[0]
        if not n: continue
        ver = c.execute(f"SELECT count(*) FROM {T} WHERE category_id=? AND verified=1", (cat["id"],)).fetchone()[0]
        top = c.execute(f"""SELECT name, slug, commercial_use FROM {T} WHERE category_id=?
                ORDER BY (status!='recommended'),(download_priority IS NULL),download_priority,LOWER(name) LIMIT 1""", (cat["id"],)).fetchone()
        domains.append(dict(slug=cat["slug"], name=cat["name"], description=cat["description"] or "", count=n, verified=ver,
            top_pick=dict(name=top["name"], commercial_use=top["commercial_use"]) if top else None,
            readout=f"readout-{cat['slug']}.html"))

    shortlist = [dict(name=r["name"], domain=r["cat"], commercial_use=r["commercial_use"])
        for r in c.execute(f"""SELECT e.name, e.commercial_use, ct.name cat FROM {T} e JOIN categories ct ON ct.id=e.category_id
            WHERE e.status='recommended' ORDER BY (e.download_priority IS NULL), e.download_priority, LOWER(e.name) LIMIT 18""")]

    index = dict(kb=kb, noun=noun, what=prof["what"], decisive_axis=prof["axis"], waves=waves, generated=generated,
        totals=dict(**{noun: tot}, verified=tot_ver, sources=tot_src, domains=len(domains)),
        query=dict(db=f"{db_path} (views v_recommended, v_best_for; FTS {T}_fts)",
                   loadout=f"ai-loadout resolve --project ./{kb}", per_domain="readout-<slug>.html"),
        reports=dict(dispatches="waves.html", receipt="verification.html"),
        domains=domains, install_first=shortlist)
    os.makedirs("readout", exist_ok=True)
    open("readout/index.json", "w", encoding="utf-8").write(json.dumps(index, ensure_ascii=False, indent=2))

    # ---- index.md ----
    md = [f"# readouts — {kb}\n",
          f"> {index['what']}\n>\n> **{tot} {noun} · {tot_ver} verified · {tot_src} sources · {waves} waves · generated {generated}.**  ",
          f"> Decisive axis: {index['decisive_axis']}\n", "## Domains\n",
          f"| Domain | {noun.capitalize()} | Verified | Top pick | License | Readout |", "|---|--:|--:|---|---|---|"]
    for d in domains:
        tp = d["top_pick"]
        md.append(f"| {d['name']} | {d['count']} | {d['verified']}/{d['count']} | {tp['name'] if tp else '—'} | "
                  f"{comm_label(tp['commercial_use']) if tp else '—'} | [`{d['readout']}`]({d['readout']}) |")
    md.append("\n## Install-first shortlist (recommended, by KB download priority)\n")
    for i, s in enumerate(shortlist, 1):
        md.append(f"{i}. **{s['name']}** ({s['domain']}) — {comm_label(s['commercial_use'])}")
    md.append("\n## Go deeper\n")
    md.append(f"- **Per-domain readout:** `readout-<slug>.html` — filterable table + sources + verify trail\n"
              f"- **Wave dispatches** (research log): `waves.md` / `waves.html`\n"
              f"- **Verification receipt** (trust trail): `verification.md` / `verification.html`\n"
              f"- **Query the DB:** `{index['query']['db']}`\n- **Resolve via loadout:** `{index['query']['loadout']}`\n"
              f"- **Programmatic map:** `index.json`\n")
    md.append(f"## Provenance\n\nEvery fact carries a **wave id** and a **verified** flag; sources are retrieval-checked "
              f"by a different-family verifier. {waves} waves; {tot_ver}/{tot} {noun} verified.\n")
    open("readout/index.md", "w", encoding="utf-8").write("\n".join(md))

    # ---- index.html ----
    rows = "".join(
        f'<tr><td><a href="{d["readout"]}">{esc(d["name"])}</a><div class="d">{esc(d["description"])[:90]}</div></td>'
        f'<td class="n">{d["count"]}</td><td class="n"><span class="v">{d["verified"]}</span>/{d["count"]}</td>'
        f'<td>{esc(d["top_pick"]["name"]) if d["top_pick"] else "—"} <span class="chip c-{d["top_pick"]["commercial_use"] if d["top_pick"] else ""}">{comm_label(d["top_pick"]["commercial_use"]) if d["top_pick"] else ""}</span></td>'
        f'<td><a class="go" href="{d["readout"]}">open ↗</a></td></tr>' for d in domains)
    sl = "".join(f'<li><b>{esc(s["name"])}</b> <span class="dm">{esc(s["domain"])}</span> <span class="chip c-{s["commercial_use"]}">{comm_label(s["commercial_use"])}</span></li>' for s in shortlist)
    payload = json.dumps(index, ensure_ascii=False).replace("</", "<\\/")
    html = INDEX_HTML
    for k, v in {"__LOGO__": logo_data_uri(), "__KB__": kb, "__NOUN__": noun, "__WAVES__": str(waves), "__GEN__": generated,
                 "__TOT__": str(tot), "__VER__": str(tot_ver), "__SRC__": str(tot_src), "__NDOM__": str(len(domains)),
                 "__WHAT__": esc(index["what"]), "__AXIS__": esc(index["decisive_axis"]),
                 "__DBREF__": esc(f"{T}_fts"), "__ROWS__": rows, "__SHORTLIST__": sl, "__DATA__": payload}.items():
        html = html.replace(k, v)
    open("readout/index.html", "w", encoding="utf-8").write(html)
    print(f"  index.{{md,json,html}}  [{kb}]  {len(domains)} domains, {tot} {noun}, install-first {len(shortlist)}")

INDEX_HTML = """<!doctype html><html lang="en" data-theme="dark"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>readouts — __KB__</title>
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
.what{color:var(--muted);font-size:15px;max-width:720px;margin-bottom:14px}
.stamps{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}.stamp{font:600 11px var(--mono);padding:6px 9px;border-radius:7px;background:var(--panel);border:1px solid var(--border);color:var(--muted)}.stamp b{color:var(--fg)}.stamp .v{color:var(--ok)}
.agent{border:1px solid var(--border);border-left:3px solid var(--accent);background:var(--panel2);border-radius:8px;padding:13px 15px;margin-bottom:24px;font-size:13.5px;color:var(--muted)}
.agent b{color:var(--fg)}.agent code{font:600 12px var(--mono);color:var(--sky);background:#8fc4e814;padding:1px 6px;border-radius:5px}
h2{font-size:13px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin:26px 0 12px;display:flex;align-items:center;gap:10px}h2::after{content:"";flex:1;height:1px;background:var(--border)}
table{width:100%;border-collapse:collapse}th{text-align:left;font:700 11px var(--sans);letter-spacing:.05em;text-transform:uppercase;color:var(--muted);padding:9px 12px;border-bottom:1px solid var(--border)}
td{padding:13px 12px;border-bottom:1px solid var(--border);font-size:14px;vertical-align:top}td.n{font:700 13px var(--mono);text-align:right;color:var(--fg)}td .v{color:var(--ok)}td .d{color:var(--faint);font-size:12px;margin-top:3px}.go{font:700 12px var(--sans)}
.chip{display:inline-block;font:700 10px var(--mono);padding:2px 7px;border-radius:5px;border:1px solid var(--border);vertical-align:middle}
.c-yes{color:var(--ok);border-color:#46c98b44;background:#46c98b14}.c-conditional{color:var(--cond);border-color:#7da6d944;background:#7da6d914}.c-no{color:var(--bad);border-color:#ef6b6b44;background:#ef6b6b14}
ol.sl{columns:2;column-gap:30px;list-style:decimal;padding-left:22px}ol.sl li{font-size:14px;padding:4px 0;break-inside:avoid}ol.sl .dm{color:var(--faint);font-size:12px}
footer{border-top:1px solid var(--border);margin-top:34px;padding:20px 0 44px;color:var(--muted);font-size:13px}.prov{display:flex;gap:9px;align-items:center;margin-bottom:8px}
@media(max-width:680px){ol.sl{columns:1}}
</style></head><body>
<header><div class="wrap"><div class="head"><span class="brand"><img src="__LOGO__" alt="readouts"><span class="sweep"></span></span><span class="spacer"></span><button class="pill" onclick="var h=document.documentElement;h.dataset.theme=h.dataset.theme==='dark'?'light':'dark'">◐ theme</button></div></div></header>
<div class="wrap">
<div class="eyebrow">index</div>
<h1>__KB__</h1>
<p class="what">__WHAT__</p>
<div class="stamps"><span class="stamp">domains <b>__NDOM__</b></span><span class="stamp">__NOUN__ <b>__TOT__</b></span><span class="stamp">verified <span class="v">__VER__</span></span><span class="stamp">sources <b>__SRC__</b></span><span class="stamp">waves <b>__WAVES__</b></span><span class="stamp">generated <b>__GEN__</b></span></div>
<div class="agent">▣ <b>For agents:</b> the full map is structured data in the <code>#readouts-index</code> JSON island at the foot of this file; a plain-text version is <a href="index.md"><code>index.md</code></a>; query the corpus at <code>__DBREF__</code> (views <code>v_recommended</code>, <code>v_best_for</code>). Decisive axis: __AXIS__</div>
<h2>Domains</h2>
<table><thead><tr><th>Domain</th><th style="text-align:right">__NOUN__</th><th style="text-align:right">Verified</th><th>Top pick</th><th></th></tr></thead><tbody>__ROWS__</tbody></table>
<h2>Install-first shortlist <span style="color:var(--faint);text-transform:none;letter-spacing:0;font-weight:400">— recommended, by KB download priority</span></h2>
<ol class="sl">__SHORTLIST__</ol>
<h2>More readouts</h2>
<p style="font-size:14px;color:var(--muted)"><a href="waves.html">Wave dispatches</a> — the research log, wave by wave · <a href="verification.html">Verification receipt</a> — the trust trail (confirmed / corrected / flagged). Agent text: <a href="waves.md">waves.md</a>, <a href="verification.md">verification.md</a>.</p>
</div>
<footer><div class="wrap"><div class="prov"><span class="sweep"></span><span>Every fact carries a <b>wave id</b> and a <b>verified</b> flag; sources retrieval-checked by a different-family verifier.</span></div><div>__KB__ · __WAVES__ waves · __TOT__ __NOUN__ (__VER__ verified) · generated __GEN__ · one map, three views: index.html · index.md · index.json.</div></div></footer>
<script id="readouts-index" type="application/json">__DATA__</script>
</body></html>"""

if __name__ == "__main__":
    main()
