#!/usr/bin/env python3
"""gen_reports.py (shared) — the narrative readout types: wave-dispatch + verification-receipt.

Profile-driven, generic over (waves, <item>, sources) so it serves both KBs. Run from a KB dir; writes
readout/waves.{html,md} (the research-log timeline) and readout/verification.{html,md} (the trust trail).
Both carry .md companions (agent-first) and the single-logo branded header.
"""
import sqlite3, json, base64, io, os, sys, re, datetime
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
def parse_vn(vn):
    if not vn: return None, None
    m = re.search(r"verdict=([^|]+)", vn); v = m.group(1).strip() if m else None
    f = re.search(r"fixe?s?:(.*)$", vn, re.I | re.S); fx = f.group(1).strip() if f else None
    return v, fx

BRAND_CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0f1f;--panel:#111a30;--panel2:#0d1526;--border:#22304f;--fg:#e8edf6;--muted:#93a1bd;--faint:#62719455;
--blue:#5aa6e8;--sky:#8fc4e8;--accent:#5aa6e8;--grad:linear-gradient(90deg,#2f6fb0,#8fc4e8);--ok:#46c98b;--warn:#e6b450;--bad:#ef6b6b;--cond:#7da6d9;
--mono:ui-monospace,"Cascadia Mono",Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
[data-theme=light]{--bg:#f7f8fb;--panel:#fff;--panel2:#eef2f8;--border:#dbe2ee;--fg:#13203a;--muted:#56648a;--faint:#8492ad55;--accent:#2f6fb0;--grad:linear-gradient(90deg,#1f4f86,#5aa6e8)}
body{background:var(--bg);color:var(--fg);font-family:var(--sans);line-height:1.55}.wrap{max-width:900px;margin:0 auto;padding:0 24px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
header{border-bottom:1px solid var(--border);background:linear-gradient(180deg,var(--panel),transparent)}
.head{display:flex;align-items:center;gap:12px;padding:20px 0}.brand{display:flex;align-items:center;gap:12px}.head img{height:40px}.sweep{height:3px;width:60px;border-radius:2px;background:var(--grad)}.spacer{flex:1}
.pill{font:600 12px var(--sans);padding:7px 11px;border:1px solid var(--border);border-radius:999px;color:var(--muted);background:var(--panel);cursor:pointer}
.eyebrow{font:700 11px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:18px 0 4px}
h1{font-size:28px;font-weight:750;letter-spacing:-.02em;margin:0 0 8px;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.stamps{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}.stamp{font:600 11px var(--mono);padding:6px 9px;border-radius:7px;background:var(--panel);border:1px solid var(--border);color:var(--muted)}.stamp b{color:var(--fg)}.stamp .v{color:var(--ok)}
h2{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:28px 0 12px;display:flex;align-items:center;gap:10px}h2::after{content:"";flex:1;height:1px;background:var(--border)}
.wave{border:1px solid var(--border);border-left:3px solid var(--accent);background:var(--panel);border-radius:10px;padding:16px 18px;margin-bottom:14px}
.whead{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}.wnum{font:700 11px var(--mono);color:var(--accent);text-transform:uppercase;letter-spacing:.08em}
.wave h3{font-size:17px;font-weight:700;margin:0}.wdate{font:600 11px var(--mono);color:var(--faint);margin-left:auto}
.wmeta{font:600 11px var(--mono);color:var(--muted);margin:6px 0 10px;display:flex;gap:8px;flex-wrap:wrap}
.tag{padding:2px 7px;border:1px solid var(--border);border-radius:5px}.tag.add{color:var(--sky);border-color:#8fc4e844;background:#8fc4e814}
.wbody{font-size:14px;color:var(--fg)}.wbody.method{color:var(--muted);font-size:13px;margin-bottom:8px}.wbody.method b{color:var(--ok)}
.vsum{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px}
.metric{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px 16px;min-width:120px}.metric .big{font:750 24px var(--sans);color:var(--fg)}.metric .lbl{font:600 11px var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.metric .big.ok{color:var(--ok)}.metric .big.fix{color:var(--warn)}.metric .big.bad{color:var(--bad)}
.note{border-top:1px solid var(--border);padding:10px 0;font-size:13.5px}.note:first-child{border:0}.note b{color:var(--fg)}
.vd{font:700 10px var(--mono);text-transform:uppercase;padding:2px 7px;border-radius:5px;margin-right:8px}
.vd-confirmed{color:var(--ok);background:#46c98b14;border:1px solid #46c98b44}.vd-fix{color:var(--warn);background:#e6b45014;border:1px solid #e6b45044}.vd-no{color:var(--bad);background:#ef6b6b14;border:1px solid #ef6b6b44}
.fixtext{color:var(--muted);font-size:12.5px;margin-top:3px}
ul.plain{list-style:none}ul.plain li{padding:5px 0;font-size:13.5px;border-bottom:1px solid var(--border)}
footer{border-top:1px solid var(--border);margin-top:30px;padding:20px 0 44px;color:var(--muted);font-size:13px}.prov{display:flex;gap:9px;align-items:center}
.lead{color:var(--muted);font-size:14.5px;max-width:680px;margin-bottom:6px}"""

def doc(title, eyebrow, body, logo, kb, waves, generated):
    return (f'<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1"><title>readouts — {esc(kb)} · {esc(title)}</title>'
        f'<style>{BRAND_CSS}</style></head><body>'
        f'<header><div class="wrap"><div class="head"><a class="brand" href="index.html" title="all readouts"><img src="{logo}" alt="readouts"><span class="sweep"></span></a><span class="spacer"></span>'
        f'<button class="pill" onclick="var h=document.documentElement;h.dataset.theme=h.dataset.theme===\'dark\'?\'light\':\'dark\'">◐ theme</button></div>'
        f'<div class="eyebrow">{esc(eyebrow)}</div><h1>{esc(title)}</h1>'
        f'<div class="stamps"><span class="stamp">KB <b>{esc(kb)}</b></span><span class="stamp">waves <b>{waves}</b></span><span class="stamp">generated <b>{generated}</b></span></div></div></header>'
        f'<div class="wrap">{body}</div>'
        f'<footer><div class="wrap"><div class="prov"><span class="sweep"></span><span>Every fact carries a <b>wave id</b> and a <b>verified</b> flag; sources retrieval-checked by a different-family verifier.</span></div></div></footer>'
        f'</body></html>')

def main():
    db_path, prof = detect()
    T, FK, kb, noun = prof["table"], prof["fk"], prof["kb"], prof["noun"]
    db = sqlite3.connect(db_path); db.row_factory = sqlite3.Row; c = db.cursor()
    gen = datetime.date.today().isoformat()
    logo = logo_data_uri()
    waves = c.execute("SELECT * FROM waves ORDER BY wave_number").fetchall()
    nwaves = len(waves)
    items_per = {r[0]: r[1] for r in c.execute(f"SELECT wave_id, count(*) FROM {T} GROUP BY wave_id")}
    src_per = {r[0]: r[1] for r in c.execute("SELECT wave_id, count(*) FROM sources GROUP BY wave_id")}
    has_recipes = c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='config_recipes'").fetchone()[0]
    rec_per = {r[0]: r[1] for r in c.execute("SELECT wave_id, count(*) FROM config_recipes GROUP BY wave_id")} if has_recipes else {}
    os.makedirs("readout", exist_ok=True)

    # ---------- DISPATCH (waves) ----------
    cards, mdw = [], [f"# readouts — {kb} · wave dispatches\n", f"> The research log: how this KB was built, wave by wave. {nwaves} waves · generated {gen}.\n"]
    for w in waves:
        wid, num = w["id"], w["wave_number"]
        adds = [f'+{items_per.get(wid,0)} {noun}', f'+{src_per.get(wid,0)} sources'] + ([f'+{rec_per.get(wid,0)} recipes'] if has_recipes else [])
        agents = f'{w["agent_count"]} agents' if w["agent_count"] else 'hands-on'
        meta = " · ".join(filter(None, [esc(w["domain_scope"]), agents, esc(w["status"])]))
        cards.append(f'<article class="wave"><div class="whead"><span class="wnum">Wave {num}</span><h3>{esc(w["title"])}</h3><span class="wdate">{esc(w["dispatched_date"])}</span></div>'
            f'<div class="wmeta">{meta} <span class="tag add">{" · ".join(adds)}</span></div>'
            + (f'<div class="wbody method"><b>Verifier:</b> {esc(w["verifier_note"])}</div>' if w["verifier_note"] else '')
            + (f'<div class="wbody">{esc(w["notes"])}</div>' if w["notes"] else '') + '</article>')
        mdw.append(f"## Wave {num} — {w['title']} ({w['dispatched_date']})\n")
        mdw.append(f"_{meta} · {' · '.join(adds)}_\n")
        if w["verifier_note"]: mdw.append(f"**Verifier:** {w['verifier_note']}\n")
        if w["notes"]: mdw.append(f"{w['notes']}\n")
    body = f'<p class="lead">The research log — each wave\'s scope, what it added, how it was verified, and the synthesis.</p>' + "".join(cards)
    open("readout/waves.html", "w", encoding="utf-8").write(doc("Wave dispatches", "research log", body, logo, kb, nwaves, gen))
    open("readout/waves.md", "w", encoding="utf-8").write("\n".join(mdw))

    # ---------- RECEIPT (verification) ----------
    tot = c.execute(f"SELECT count(*) FROM {T}").fetchone()[0]
    ver = c.execute(f"SELECT count(*) FROM {T} WHERE verified=1").fetchone()[0]
    nsrc = c.execute("SELECT count(*) FROM sources").fetchone()[0]
    src_ok = c.execute("SELECT count(*) FROM sources WHERE verified=1").fetchone()[0]
    # Three buckets, and they must sum to the whole. verified=1 / verified=0 were
    # presented as complementary while NULL rows — sources nobody checked — fell
    # out of both and vanished from a page titled "the trust trail".
    src_unchecked = c.execute("SELECT count(*) FROM sources WHERE verified IS NULL").fetchone()[0]
    rows = c.execute(f"SELECT name, status, verified, verify_note FROM {T} ORDER BY LOWER(name)").fetchall()
    fixed, clean, unver = [], 0, []
    for r in rows:
        v, fx = parse_vn(r["verify_note"])
        if not r["verified"]: unver.append(r["name"])
        if v and "fix" in v.lower() and fx: fixed.append((r["name"], fx))
        elif v and "confirm" in v.lower(): clean += 1
    nonresolve = c.execute("SELECT subject, title, url FROM sources WHERE verified=0 ORDER BY (title IS NULL), title").fetchall()

    metrics = (f'<div class="metric"><div class="big ok">{ver}/{tot}</div><div class="lbl">{noun} verified</div></div>'
        f'<div class="metric"><div class="big">{nsrc}</div><div class="lbl">sources ({src_ok} resolve · {src_unchecked} unchecked)</div></div>'
        f'<div class="metric"><div class="big ok">{clean}</div><div class="lbl">confirmed clean</div></div>'
        f'<div class="metric"><div class="big fix">{len(fixed)}</div><div class="lbl">confirmed w/ fixes</div></div>'
        f'<div class="metric"><div class="big bad">{len(unver)}</div><div class="lbl">unverified</div></div>')
    method = "".join(f'<div class="note"><b>Wave {w["wave_number"]}</b> · {esc(w["title"])}<div class="fixtext">{esc(w["verifier_note"])}</div></div>' for w in waves if w["verifier_note"])
    corr = "".join(f'<div class="note"><span class="vd vd-fix">confirmed w/ fixes</span><b>{esc(n)}</b><div class="fixtext">{esc(fx)}</div></div>' for n, fx in fixed) or '<div class="note">None.</div>'
    unv = ("".join(f'<li><span class="vd vd-no">unverified</span>{esc(n)}</li>' for n in unver) or '<li>None — every item verified.</li>')
    # Link only what a reader can actually follow. Some source rows record internal
    # provenance (a path to a working record) in the url column rather than a URL;
    # rendering those as <a href> published a page of 404s on the public mirror.
    # They stay visible as text — the provenance is real, it is just not a link.
    def _src_ref(s):
        u = s["url"] or ""
        label = esc(s["title"] or s["subject"] or u)
        if u.startswith(("http://", "https://")):
            return f'{label} — <a href="{esc(u)}" target=_blank rel=noopener>link</a>'
        return f'{label}{" — <code>" + esc(u) + "</code>" if u else ""}'

    nonres_n = c.execute("SELECT count(*) FROM sources WHERE verified=0").fetchone()[0]
    if src_ok + nonres_n + src_unchecked != nsrc:
        raise SystemExit(f"::error:: source buckets do not sum: {src_ok}+{nonres_n}+"
                         f"{src_unchecked} != {nsrc} — a verdict value is unaccounted for")
    nrz = ("".join(f"<li>{_src_ref(s)}</li>" for s in nonresolve) or "<li>None.</li>")
    body = (f'<p class="lead">The trust trail: what the different-family verifier confirmed, corrected, and flagged. '
        f'Verdicts are parsed from each item\'s verify-note; sources are checked for resolution.</p>'
        f'<div class="vsum">{metrics}</div>'
        f'<h2>Verification method, by wave</h2>{method}'
        f'<h2>Corrections — confirmed with fixes ({len(fixed)})</h2>{corr}'
        f'<h2>Unverified ({len(unver)})</h2><ul class="plain">{unv}</ul>'
        f'<h2>Sources that don\'t resolve ({len(nonresolve)})</h2><ul class="plain">{nrz}</ul>')
    open("readout/verification.html", "w", encoding="utf-8").write(doc("Verification receipt", "trust trail", body, logo, kb, nwaves, gen))
    mdv = [f"# readouts — {kb} · verification receipt\n",
        f"> **{ver}/{tot} {noun} verified · {nsrc} sources ({src_ok} resolve) · {nwaves} waves · generated {gen}.**  ",
        f"> Verdicts: {clean} confirmed clean · {len(fixed)} confirmed-with-fixes · {len(unver)} unverified.\n",
        "## Verification method, by wave\n"]
    mdv += [f"- **Wave {w['wave_number']}** ({w['title']}): {w['verifier_note']}" for w in waves if w["verifier_note"]]
    mdv.append(f"\n## Corrections — confirmed with fixes ({len(fixed)})\n")
    mdv += [f"- **{n}** — {fx}" for n, fx in fixed] or ["- None."]
    mdv.append(f"\n## Unverified ({len(unver)})\n"); mdv += [f"- {n}" for n in unver] or ["- None."]
    open("readout/verification.md", "w", encoding="utf-8").write("\n".join(mdv))

    print(f"  reports [{kb}]: waves.{{html,md}} ({nwaves} waves), verification.{{html,md}} ({ver}/{tot} verified, {len(fixed)} fixes, {len(unver)} unverified)")

if __name__ == "__main__":
    main()
