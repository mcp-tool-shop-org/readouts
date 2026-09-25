"""Wave-6 — wire `offload` into the real workflows (verifier panel into roleos verify-citations,
study-swarm preread compress, ollama-intern companion). Idempotent on wave_number=6 + ids 162-164.
Hands-on + measured on the live RTX 5090 / llama-swap :9090 (2026-06-03)."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

# --- Wave 6 (hands-on wiring, no swarm) ---
c.execute("DELETE FROM waves WHERE wave_number=6")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (6,?,?,?,?,?,?,?,?)""", (
  "Wire offload into real workflows — verifier panel -> roleos verify-citations, study-swarm preread compress, ollama-intern companion",
  "2026-06-03",
  "llm-serving (verifier + token-economy wiring)",
  0,
  "HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090. The 0-false-confirm PANEL property "
  "was RE-PROVEN on a REAL 16-case arXiv citation set (not the rig's own measurements): mistral-nemo-12b "
  "solo false-confirmed a refuted claim (inverting arXiv:2404.13076's finding), the 3-seat conservative-"
  "majority panel held it at 'insufficient' (0 panel false-confirms). role-os wiring covered by 1196 "
  "passing tests; live end-to-end confirmed through role-os's own module against llama-swap.",
  "synthesized",
  "(hands-on session, no dispatch swarm)",
  "Closes the wave-5 #156 'NEXT' (wire the panel into roleos verify-citations). offload now SAVES Claude "
  "tokens in real pipelines, not on disk. Recipes #162-164."
))
wave6 = c.execute("SELECT id FROM waves WHERE wave_number=6").fetchone()[0]
print("wave6 id =", wave6)

# --- #162 — offload verify --panel wired into roleos verify-citations (--local-panel) ---
body162 = (
"WIRED (2026-06-03): offload's 3-seat entailment PANEL is now a SECOND verifier seat in role-os's "
"citation gate -- `roleos verify-citations --local-panel` (role-os v2.5.0 -- PUBLISHED to npm via OIDC Trusted "
"Publishing 2026-06-03: PRs #8 (feature) + #9 (release.yml) merged, tag + GitHub release v2.5.0, npm latest=2.5.0). "
"This realizes the wave-5 #156 'NEXT' and the EXTERNAL_VERIFIER (workflow-standard #6) "
"intent, runnable locally for free.\n\n"
"ARCHITECTURE: prism (the family-different verifier of record) RETRIEVES -- deterministic arXiv/Crossref "
"existence floor + its own groundedness lens, returning per-citation {source_title, supporting_span}. The new "
"seat (src/citation-panel.mjs: runOffloadPanel/applyLocalPanel/buildEvidence) re-judges each citation prism "
"marked `supported` by shelling `offload verify --panel` (qwen3-4b + qwen3-14b + mistral-nemo-12b) against "
"prism's OWN retrieved evidence. MONOTONE-TIGHTENING: it can only downgrade a passing gate to escalate "
"(local_panel_disagreement, exit 30) with a CONTRASTIVE message; never loosens, never overrides the existence "
"floor (blocking dominates), never runs on a non-passing gate; a requested-but-unreachable panel escalates "
"(closed-gate rule). Receipt gains a local_panel block (PIN_PER_STEP: the exact seat models) folded into the "
"hash chain via verdict + panel digest. +16 tests, 1196 total green. Decorrelated from BOTH the Claude "
"generator (no Anthropic model) AND prism's single groundedness model.\n\n"
"RE-PROVEN ON REAL CITATIONS (verifier/citations-real.json — 16 cases over 8 real arXiv papers role-os actually "
"verifies; abstracts fetched live from Semantic Scholar, content-pinned by sha256; planted traps = inversions, "
"plausible-but-unstated remedies, wrong numbers). citation_panel_eval.py result:\n"
"  qwen3-4b        13/16 = 81.2%, 0 false-confirms\n"
"  qwen3-14b       15/16 = 93.8%, 0 false-confirms\n"
"  mistral-nemo-12b 12/16 = 75.0%, *** 1 FALSE-CONFIRM *** (case #11: stamped a REFUTED claim that inverts "
"arXiv:2404.13076's self-recognition<->self-preference finding as 'supported')\n"
"  3-seat panel    13/16 = 81.2%, **0 false-confirms** -- it CAUGHT case #11 (4b=insufficient, 14b=refuted, "
"nemo=supported -> conservative majority = insufficient).\n"
"HONEST NUANCE: the panel's raw accuracy (81%) sits BELOW qwen3-14b solo (94%) because the conservative "
"majority pulls toward not-confirmed; but every panel miss is CONSERVATIVE (refuses to confirm a true claim -> "
"a human-review escalation), NEVER a false-confirm. For a GATE that is the correct trade: 0 false-confirms is "
"the safety property; over-escalation is recoverable, a false-confirm is not. Receipt: "
"verifier/citation-panel-receipt.json (property_holds=true; PIN: seats + verify_prompt_sha256 + per-source "
"abstract sha256). Live end-to-end re-confirmed through role-os's runOffloadPanel against llama-swap on case #11.\n\n"
"LIVE E2E (2026-06-03): ran `roleos verify-citations --local-panel` with PRISM_CMD set "
"(E:/AI/prism-verify/.venv/Scripts/prism.exe + PRISM_DEV=1) and ollama up (mistral-small:24b = prism's default "
"provider model). prism EXECUTED live (46.9 s, structured 3-citation response) -- but arXiv was THROTTLING this "
"host (ReadTimeout on all 3 ids; earlier 429s too), so prism's existence floor couldn't resolve them and the "
"gate correctly ESCALATED (exit 30, RETRIEVE MANUALLY) -- the closed-gate invariant, live (it also escalated "
"live on a prism signing-key misconfig). To exercise the panel-in-gate path that arXiv blocked, ran the REAL "
"runCitationGate + REAL offload panel against live llama-swap with ONLY prism's network RESPONSE stubbed from "
"the sha256-pinned abstract cache: the panel CAUGHT the planted inversion (arXiv:2404.13076 -> insufficient) "
"and confirmed the faithful claim (arXiv:2310.01798 -> supported), gate -> escalate (local_panel_disagreement) "
"with the contrastive message. So the full chain is proven: prism runs here + the gate's error-handling is "
"live + the panel decides accept/escalate in-gate live; the only un-live link (prism's OWN arXiv retrieval) is "
"an external outage, not the wiring. Continues #156; design: role-os design/citation-verification-runner.md (Local-panel seat)."
)

# --- #163 — offload compress as the study-swarm pre-read token-saver ---
body163 = (
"WIRED (2026-06-03): `offload compress` is the study-swarm PRE-READ step -- shrink a large source to a digest "
"BEFORE it enters a Claude/agent context, so the raw never costs Claude tokens. Tool: scripts/preread.py "
"(--file/--url/stdin, --words budget, --threshold-words passthrough, batch + token receipt; shells offload "
"compress). \n\n"
"WHERE IT FITS (honest): Workflow-tool scripts run sandboxed with NO subprocess/FS access, so the compress "
"step CANNOT live inside wave-swarm.workflow.js. The correct home is ORCHESTRATOR-SIDE: pre-compress large "
"sources, then embed only the DIGEST in agent prompts. The pre-read is for SOURCE-INGESTING waves (an agent "
"must read a long log/doc/dump/prior-wave prose); the engine-research wave's own inputs are already compact "
"(lane instructions + structured claims), so it needs no pre-read -- the convention is documented in "
"wave-swarm.workflow.js as the template for the next such wave. Per-source only: a source must fit the local "
"model's ~16K context (the 440 KB wave-01 research-raw.json must be chunked).\n\n"
"MEASURED on this KB's OWN real wave-1 artifacts (receipt: verifier/preread-wave-receipt.json): "
"verification.md 2767->286 tok (89.7%), dispatch.md 4475->286 tok (93.6%); AGGREGATE 7242 -> 572 Claude-tokens, "
"**92.1% smaller, 6670 tokens saved**, faithful digests (qwen3-4b, word budget 150). Continues the wave-5 "
"token-economy work (#157 baseline, #158 the offload tool)."
)

# --- #164 — ollama-intern <-> offload companion (no MCP change) ---
body164 = (
"WIRED (2026-06-03) as a COMPANION, deliberately NOT an MCP primitive. ollama-intern-mcp is v2.6.0 (42 tools, "
"968 tests): the atom freeze lifted at v2.1.0 WITH DISCIPLINE (new atom needs an audit-justified gap + tests + "
"handbook + CHANGELOG), packs/artifacts stay frozen, and the audit/calibration/VERIFIER surface STAYS REVERTED "
"('the MCP does the work, it does not grade itself'). offload-as-primitive fails that 3 ways: (1) no gap for "
"compress -- summarize_fast/deep already compress on the intern's own model; (2) a self-hosted verifier is the "
"reverted surface AND same-stack self-grading is what EXTERNAL_VERIFIER forbids; (3) cross-stack -- offload is "
"llama-swap/Qwen+Mistral, the MCP is Ollama/hermes3. So offload sits ALONGSIDE the intern, which is exactly "
"where it adds value: as the family-different EXTERNAL_VERIFIER the intern is forbidden to be for itself "
"(different FAMILY -- Qwen+Mistral vs hermes3/Llama -- AND different STACK -- llama-swap vs Ollama -> "
"decorrelated from both the intern and the Claude generator).\n\n"
"BRIDGE: E:/AI-Models/studio-local/intern_offload.py (two seams, both shell offload, no freeze touched): "
"`digest` = pre-shrink an oversized input before the intern/Claude reads it; `check` = panel-verify an intern "
"OUTPUT against its source (default 3-seat panel, 0 false-confirms). Playbook: intern_offload.md. "
"DEMONSTRATED on arXiv:2310.01798 ('LLMs Cannot Self-Correct Reasoning Yet'): a faithful intern summary -> "
"SUPPORTED; an intern OVERCLAIM ('LLMs reliably self-correct via iterative prompting alone') -> REFUTED -- the "
"family-different panel catches the intern's hallucination. Continues #158."
)

recipes = [
  (162, "llm-serving-offload-panel-wired-into-roleos-verify-citations-local-seat",
   "offload verify --panel wired into roleos verify-citations (--local-panel): family-different local seat, 0-false-confirm re-proven on real arXiv citations",
   "https://github.com/mcp-tool-shop-org/role-os", body162),
  (163, "llm-serving-offload-compress-study-swarm-preread-token-saver",
   "offload compress as study-swarm pre-read (preread.py): measured 92.1% Claude-token reduction on real wave artifacts",
   "file:///tensor-engine-knowledge/scripts/preread.py", body163),
  (164, "llm-serving-offload-ollama-intern-companion-external-verifier",
   "offload <-> ollama-intern companion (intern_offload.py): offload verify --panel as the intern's family-different EXTERNAL_VERIFIER (no MCP change)",
   "file:///E:/AI-Models/studio-local/intern_offload.py", body164),
]
c.execute("DELETE FROM config_recipes WHERE id IN (162,163,164)")
for rid, slug, name, url, body in recipes:
    c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
    VALUES (?,?,?,?,?,?,?,?,?)""", (rid, slug, name, 2, 15, "recipe", url, body, wave6))

# --- mark #156's "NEXT" as done (continuity, like _wave5_record updated #149) ---
row = c.execute("SELECT body FROM config_recipes WHERE id=156").fetchone()
if row and "[UPDATE 2026-06-03 wave-6]" not in row[0]:
    upd = ("\n\n[UPDATE 2026-06-03 wave-6]: the 'NEXT' items are DONE -- the 3-seat panel is WIRED into "
           "roleos verify-citations as `--local-panel` (#162, role-os v2.5.0), the labeled set was EXPANDED to a "
           "real 16-case arXiv set (citations-real.json), and the 0-false-confirm property was RE-PROVEN on it "
           "(mistral-nemo's single slip on case #11 rescued by the panel). Still open: a 3rd family (Phi/Granite/"
           "Gemma) seat for deeper decorrelation.")
    c.execute("UPDATE config_recipes SET body=? WHERE id=156", (row[0] + upd,))
    print("updated #156 (NEXT -> done)")

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0], "| waves:", c.execute("SELECT count(*) FROM waves").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id", (wave6,)):
    print(" ", r[0], r[1], "|", r[2][:72])
db.close()
