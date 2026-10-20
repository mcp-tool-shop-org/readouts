#!/usr/bin/env python3
"""Generate an ai-loadout index at .claude/loadout/index.json over the catalog, from the DB.

Progressive disclosure (so all the data isn't dumped on the agent at once):
  - ONE tiny `core` entry (the catalog index + load-bearing shortlist) — always loaded.
  - one `domain` entry per catalog file — keyword-routed, loaded only when the task matches.
  - the wave dispatch/verification docs as `domain` entries.
  - the raw swarm json as `manual` — never auto-loaded.

Re-run after each wave. QA with:  ai-loadout validate|overlaps|budget .claude/loadout/index.json
"""
import glob as _glob
import json
import os
import re
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "findings.db")
OUTDIR = os.path.join(ROOT, ".claude", "loadout")
DATE_FALLBACK = "2026-10-20"

# curated single-token keywords per lane (single tokens = best match recall)
KW = {
    'claude-code-headless': ['claude', 'claude-code', 'headless', 'print', 'stream-json', 'init', 'mcp', 'mcp-server',
                             'pending', 'connected', 'hold', 'first-turn', 'kickoff', 'version'],
    'permissions-containment': ['permission', 'permissions', 'deny', 'allow', 'read', 'grep', 'glob', 'containment',
                                'isolation', 'sandbox', 'leak', 'path', 'rule', 'best-effort', 'unprivileged'],
    'agent-sandboxes': ['sbx', 'docker', 'sandbox', 'sandboxes', 'kit', 'policy', 'network', 'balanced', 'oauth',
                        'credentials', 'ollama', 'host', 'daemon', 'socket'],
    'agent-tracing': ['relay', 'nemo-relay', 'tracing', 'trace', 'atof', 'atif', 'opentelemetry', 'telemetry',
                      'gateway', 'privacy', 'identity'],
}
PAT = {
    'claude-code-headless': ['claude_code', 'mcp', 'headless'],
    'permissions-containment': ['permissions', 'containment', 'deny_rule'],
    'agent-sandboxes': ['sandbox', 'sbx', 'network_policy'],
    'agent-tracing': ['tracing', 'relay', 'privacy'],
}


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
    wr = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()
    wave = wr[0] if wr and wr[0] is not None else 1
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUTDIR, exist_ok=True)
    entries = []

    # core — tiny always-on orientation
    t, l = est(os.path.join(ROOT, "catalog", "README.md"))
    entries.append({"id": "catalog-index", "path": "catalog/README.md",
                    "keywords": ["agent", "harness", "claude-code", "sandbox", "permissions", "loadout", "catalog"],
                    "patterns": [], "priority": "core",
                    "summary": "agent-tooling-knowledge catalog index + load-bearing shortlist; drill into per-lane entries.",
                    "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # one domain entry per catalog file
    for cat in cats:
        full = os.path.join(ROOT, "catalog", cat["slug"] + ".md")
        if not os.path.exists(full):
            continue
        nfind = c.execute("SELECT COUNT(*) FROM findings WHERE category_id=?", (cat["id"],)).fetchone()[0]
        t, l = est(full)
        summ = f"{cat['name']}: {nfind} findings. {cat['description']}"[:120]
        entries.append({"id": cat["slug"], "path": f"catalog/{cat['slug']}.md", "keywords": list(KW.get(cat["slug"], [])),
                        "patterns": PAT.get(cat["slug"], []), "priority": "domain", "summary": summ,
                        "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # wave docs — every wave's dispatch + verification (domain) and raw json (manual)
    DISP_KW = ["agent", "harness", "claude-code", "mcp", "permissions", "sandbox", "relay", "probe",
               "design", "implication"]
    VER_KW = ["verify", "verification", "citation", "source", "fabricated", "groundedness", "oracle", "trust"]
    for wdir in sorted(_glob.glob(os.path.join(ROOT, "waves", "wave-*"))):
        if not os.path.isdir(wdir):
            continue
        wname = os.path.basename(wdir)
        disp = os.path.join(wdir, "dispatch.md")
        if os.path.exists(disp):
            t, l = est(disp)
            entries.append({"id": f"{wname}-dispatch", "path": f"waves/{wname}/dispatch.md", "keywords": DISP_KW,
                            "patterns": ["claude_code", "sandbox", "permissions"], "priority": "domain",
                            "summary": f"{wname} narrative: findings -> design implications per lane."[:120],
                            "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})
        ver = os.path.join(wdir, "verification.md")
        if os.path.exists(ver):
            t, l = est(ver)
            entries.append({"id": f"{wname}-verification", "path": f"waves/{wname}/verification.md", "keywords": VER_KW,
                            "patterns": ["verification"], "priority": "domain",
                            "summary": f"{wname} verification: receipts, verdicts, corrections."[:120],
                            "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})
        rawj = os.path.join(wdir, "research-raw.json")
        if os.path.exists(rawj):
            t, l = est(rawj)
            entries.append({"id": f"{wname}-raw", "path": f"waves/{wname}/research-raw.json", "keywords": ["raw", "json"],
                            "patterns": [], "priority": "manual",
                            "summary": f"Raw {wname} wave file — manual lookup only.",
                            "triggers": {"task": False, "plan": False, "edit": False}, "tokens_est": t, "lines": l})

    core = sum(e["tokens_est"] for e in entries if e["priority"] == "core")
    ondemand = sum(e["tokens_est"] for e in entries if e["priority"] != "core")
    domain_toks = sorted((e["tokens_est"] for e in entries if e["priority"] == "domain"), reverse=True)
    avg = core + sum(domain_toks[:2])  # orientation + ~2 matched domain entries
    index = {"version": "1.0.0", "generated": date + "T00:00:00Z",
             "source": f"findings.db (wave {wave})", "lazyLoad": True,
             "budget": {"always_loaded_est": core, "on_demand_total_est": ondemand,
                        "avg_task_load_est": avg, "avg_task_load_observed": None},
             "entries": entries}
    with open(os.path.join(OUTDIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    con.close()
    print(f"loadout index: {len(entries)} entries — core {core} tok always-on, "
          f"{ondemand} tok on-demand, ~{avg} tok/typical task. -> .claude/loadout/index.json")


if __name__ == "__main__":
    main()
