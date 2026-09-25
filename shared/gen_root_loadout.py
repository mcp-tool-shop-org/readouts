#!/usr/bin/env python3
"""Generate the ROOT readouts loadout (.claude/loadout/index.json) that routes a task to the right
KNOWLEDGE BASE first. ai-loadout is layered (global -> org -> project -> session); this is the
org/project layer over the KBs. Each KB then has its own .claude/loadout/index.json that routes to a
domain slice. Re-run after adding a KB or after a KB's loadout changes:
    python shared/gen_root_loadout.py
QA: ai-loadout validate .claude/loadout/index.json
"""
import glob
import json
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # shared/ -> readouts/
OUT = os.path.join(ROOT, ".claude", "loadout")


def est(path):
    if not os.path.exists(path):
        return 0, 0
    t = open(path, encoding="utf-8").read()
    return max(0, len(t) // 4), t.count("\n") + 1


def kb_keywords(kb_dir):
    """Union the KB's own loadout entry keywords, so the root entry stays in sync with the KB."""
    idx = os.path.join(kb_dir, ".claude", "loadout", "index.json")
    kws = set()
    if os.path.exists(idx):
        d = json.load(open(idx, encoding="utf-8"))
        for e in d.get("entries", []):
            for k in e.get("keywords", []):
                kws.add(k)
    return sorted(kws)


def main():
    entries = []
    t, l = est(os.path.join(ROOT, "README.md"))
    entries.append({"id": "readouts-index", "path": "README.md",
                    "keywords": ["readouts", "knowledge", "base", "catalog"], "patterns": [], "priority": "core",
                    "summary": "readouts monorepo overview + the knowledge bases it holds.",
                    "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    kbs = 0
    for name in sorted(os.listdir(ROOT)):
        kb = os.path.join(ROOT, name)
        if not os.path.isdir(kb) or name.startswith(".") or name == "shared":
            continue
        # a KB is any subfolder with its own loadout index + at least one .db file
        # (so KBs are free to name their DB models.db, engines.db, etc.)
        if not os.path.exists(os.path.join(kb, ".claude", "loadout", "index.json")):
            continue
        # Largest non-empty DB, not glob()[0]: a stray 0-byte sibling sorts first and
        # silently zeroes the KB's count (training-knowledge/recipes.db did exactly that).
        dbs = [p for p in sorted(glob.glob(os.path.join(kb, "*.db"))) if os.path.getsize(p)]
        if not dbs:
            continue
        dbs.sort(key=os.path.getsize, reverse=True)
        t, l = est(os.path.join(kb, "catalog", "README.md"))
        cnt = "?"
        try:
            con = sqlite3.connect(dbs[0])
            for tbl in ("models", "engines", "findings", "techniques", "recipes", "capabilities"):  # primary-entity table name varies by KB
                try:
                    cnt = con.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
                    break
                except Exception:
                    pass
            con.close()
        except Exception:
            pass
        entries.append({"id": name, "path": f"{name}/catalog/README.md", "keywords": kb_keywords(kb) or [name],
                        "patterns": [], "priority": "domain",
                        "summary": f"{name}: {cnt}-entry knowledge base; routes to its own per-domain loadout."[:120],
                        "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})
        kbs += 1

    core = sum(e["tokens_est"] for e in entries if e["priority"] == "core")
    ondemand = sum(e["tokens_est"] for e in entries if e["priority"] != "core")
    index = {"version": "1.0.0", "generated": "2026-06-02T00:00:00Z", "source": "readouts monorepo (root)",
             "lazyLoad": True,
             "budget": {"always_loaded_est": core, "on_demand_total_est": ondemand,
                        "avg_task_load_est": core + ondemand, "avg_task_load_observed": None},
             "entries": entries}
    os.makedirs(OUT, exist_ok=True)
    json.dump(index, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"root loadout: {len(entries)} entries ({kbs} knowledge base(s)). -> .claude/loadout/index.json")


if __name__ == "__main__":
    main()
