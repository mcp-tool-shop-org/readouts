#!/usr/bin/env python3
"""gen_readout.py (shared) — engines.db OR models.db -> standalone, brand-correct, JSON-driven catalog readouts.

Profile-driven (readout_profiles.detect picks the KB by the DB in cwd). Run FROM a KB directory; writes
to <kb>/readout/readout-<domain>.html, reading the shared template + logo from this script's dir.

Usage (from a KB dir):  python ../shared/gen_readout.py            -> all domains
                        python ../shared/gen_readout.py <domain>   -> one domain
"""
import sqlite3, json, base64, io, os, sys, datetime
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from readout_profiles import detect

TEMPLATE = os.path.join(SCRIPT_DIR, "readout", "readout_template.html")
LOGO = os.path.join(SCRIPT_DIR, "readout", "assets", "readouts-logo.png")
STATUS_ORDER = {"recommended": 0, "runner-up": 1, "situational": 2, "legacy": 3, "avoid": 4}

def logo_data_uri(h=84):
    try:
        from PIL import Image
        im = Image.open(LOGO).convert("RGBA"); w = int(im.width * h / im.height)
        im = im.resize((w, h), Image.LANCZOS); buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        print("  (logo embed skipped:", e, ")"); return ""

def build_one(domain, db_path, prof):
    T, FK = prof["table"], prof["fk"]
    PT = FK.replace("_id", "_purposes")
    db = sqlite3.connect(db_path); db.row_factory = sqlite3.Row; c = db.cursor()
    cat = c.execute("SELECT * FROM categories WHERE slug=?", (domain,)).fetchone()
    if not cat:
        sys.exit(f"unknown domain '{domain}' in {prof['kb']}")
    waves = c.execute("SELECT count(*) FROM waves").fetchone()[0]
    tot = c.execute(f"SELECT count(*) FROM {T}").fetchone()[0]
    totv = c.execute(f"SELECT count(*) FROM {T} WHERE verified=1").fetchone()[0]
    items = []
    for e in c.execute(f"SELECT * FROM {T} WHERE category_id=?", (cat["id"],)).fetchall():
        x = dict(e)
        x["best_for"] = [dict(purpose=p["name"], rank=p["rank"], fitness=p["fitness"], note=p["note"])
            for p in c.execute(f"""SELECT pu.name, ep.rank, ep.fitness, ep.note FROM {PT} ep
                JOIN purposes pu ON pu.id=ep.purpose_id WHERE ep.{FK}=?
                ORDER BY (ep.rank IS NULL), ep.rank, ep.fitness DESC""", (e["id"],))]
        x["sources"] = [dict(kind=s["kind"], title=s["title"], url=s["url"], claim=s["claim"],
                             verified=s["verified"], finding_supported=s["finding_supported"])
            for s in c.execute(f"SELECT * FROM sources WHERE {FK}=? ORDER BY (verified IS NULL), verified DESC", (e["id"],))]
        items.append(x)
    items.sort(key=lambda x: (STATUS_ORDER.get(x["status"], 9),
                              x["download_priority"] if x["download_priority"] is not None else 999,
                              (x["name"] or "").lower()))
    for i, x in enumerate(items, 1):
        x["rank"] = i
    gen = datetime.date.today().isoformat()
    data = dict(readout_type="catalog", kb=prof["kb"], noun=prof["noun"], waves=waves, generated=gen,
                domain=dict(slug=cat["slug"], name=cat["name"], description=cat["description"] or ""),
                totals=dict(items=tot, verified=totv), columns=prof["columns"], detail_spec=prof["detail_spec"],
                items=items)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = open(TEMPLATE, encoding="utf-8").read()
    for k, v in {"__DOMAIN_NAME__": cat["name"], "__DOMAIN_DESC__": cat["description"] or "",
                 "__KB_NAME__": prof["kb"], "__KB_WAVES__": str(waves), "__GENERATED__": gen,
                 "__LOGO_URI__": logo_data_uri(), "__READOUT_DATA__": payload}.items():
        html = html.replace(k, v)
    os.makedirs("readout", exist_ok=True)
    out = f"readout/readout-{domain}.html"
    open(out, "w", encoding="utf-8").write(html)
    print(f"  {out}  ({round(len(html.encode())/1024,1)} KB, {len(items)} {prof['noun']}, "
          f"{sum(1 for x in items if x['verified'])} verified, {sum(len(x['sources']) for x in items)} sources)")
    db.close()

def all_domains(db_path, prof):
    db = sqlite3.connect(db_path)
    doms = [r[0] for r in db.execute(
        f"SELECT c.slug FROM categories c WHERE EXISTS(SELECT 1 FROM {prof['table']} e WHERE e.category_id=c.id) ORDER BY c.sort")]
    db.close(); return doms

if __name__ == "__main__":
    db_path, prof = detect()
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    doms = [arg] if arg != "all" else all_domains(db_path, prof)
    print(f"[{prof['kb']}] {len(doms)} domain readout(s) from {db_path}:")
    for d in doms:
        build_one(d, db_path, prof)
