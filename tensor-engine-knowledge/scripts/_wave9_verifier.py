"""Wave-9 — harden the family-different verifier + prove the token economy at scale.
Idempotent on wave_number=9 + ids 169-172. Hands-on + measured on the live RTX 5090 / llama-swap
:9090 (2026-06-03). Three moves: (1) a 3rd verifier family (IBM Granite 3.3 8B) + the discovery that
family diversity does NOT fix correlated errors; (2) full-abstract evidence to the panel; (3) prompt
hardening that recovers the correlated false-confirms; plus a real study-swarm dogfood of both
offload paths. Updates #156 + #162 (their "3rd family" open item is now DONE)."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

c.execute("DELETE FROM waves WHERE wave_number=9")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (9,?,?,?,?,?,?,?,?)""", (
  "Harden the family-different verifier + prove the token economy at scale — 3rd family (IBM Granite), full-abstract evidence, prompt hardening, real-wave dogfood",
  "2026-06-03",
  "llm-serving (verifier panel hardening + token economy)",
  3,
  "HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090, PLUS a real 3-agent study-swarm whose "
  "citations were re-checked by the hardened panel. THE FINDING: adding a 3rd verifier FAMILY (IBM "
  "Granite 3.3 8B, Apache-2.0) improves accuracy and neutralizes UNCORRELATED single-seat slips, but "
  "an adversarial 24-case set BROKE the panel's 0-false-confirm property — #21/#22/#23 (a direction "
  "inversion + two plausible-but-unstated additions) fooled a MAJORITY of seats ACROSS ALL FAMILIES "
  "(#22 fooled all four), and conservative majority cannot catch a CORRELATED slip. The literature "
  "(Kim 2025 arXiv:2506.07962; Kuncheva-Whitaker 2003; PoLL arXiv:2404.18796) confirms family "
  "diversity fixes idiosyncratic bias, not correlated error. The FIX that worked is a different lever: "
  "a HARDENED verify prompt (explicit direction-check + added-specific-check) recovered ALL 3 "
  "correlated false-confirms (per-family panel 3 fc -> 0 fc, accuracy 79.2% -> 87.5%, no regressions) "
  "and is now the offload default. Move #2 (full-abstract evidence to the panel) and a real-wave "
  "dogfood (89.6% preread token saving + the panel catching a real agent mischaracterization) round "
  "it out. Receipts in verifier/: citation-panel-3family-receipt.json, prompt-hardening-receipt.json, "
  "e2e-full-abstract-receipt.json, wave9-dogfood-receipt.json.",
  "synthesized",
  "KICKOFF (Wave 7 verifier hardening; landed as wave 9 — waves 7/8 were the kohya/Chroma visual track) + verifier/wave-09 study-swarm",
  "Closes the standing '3rd family / multi-lens >=3' gap from #156/#162. Recipes #169-172."
))
wave9 = c.execute("SELECT id FROM waves WHERE wave_number=9").fetchone()[0]
print("wave9 id =", wave9)

body169 = (
"DONE (2026-06-03): added a THIRD verifier family to the offload entailment panel — IBM Granite 3.3 "
"8B Instruct (Apache-2.0; granite-3.3-8b-instruct-Q4_K_M.gguf from ibm-granite/granite-3.3-8b-instruct-"
"GGUF; ~8B, well above the 4B 0-false-confirm floor). New llama-swap seat `granite-3.3-8b` "
"(config.yaml). offload PANEL_SEATS is now CONFIGURABLE (env OFFLOAD_PANEL_SEATS); the new default is "
"the per-family 3-seat qwen3-14b + mistral-nemo-12b + granite-3.3-8b (one strong seat per family — "
"the measured best, cleanest decorrelation, no same-family redundancy).\n\n"
"MEASURED (citation_panel_eval_3family.py). 16-case real-arXiv set, single seats: qwen3-4b 81.2%/0fc, "
"qwen3-14b 93.8%/0fc, mistral-nemo-12b 75.0%/1fc, granite-3.3-8b 75.0%/2fc (granite SOLO is "
"individually UNSAFE — 2 false-confirms). Panels, ALL 0 false-confirms on the 16: P2-baseline "
"(qwen4b+qwen14b+nemo, 2 families) 81.2%; P3-4seat 87.5%; P3-per-family (qwen14b+nemo+granite) 93.8% "
"(BEST); P3-cheap 81.2%. The 3-family panel ABSORBS granite's 2 solo false-confirms by conservative "
"majority — it held 3 single-seat slips (#11 nemo, #13/#16 granite) vs the 2-family panel's 1. "
"=> a 3rd family IMPROVES accuracy AND neutralizes more uncorrelated slips while holding 0 fc.\n\n"
"BUT THE CEILING (the load-bearing finding): on a HARDER 24-case set (8 adversarial traps grounded in "
"the SAME sha-pinned abstracts, citations-real-ext.json — subtle inversions + plausible-but-unstated "
"specifics), EVERY panel composition INCLUDING the 3-family ones shows 3 FALSE-CONFIRMS (#21/#22/#23). "
"#22 (a looser/stricter inversion of arXiv:2408.02442) fooled ALL FOUR seats; #21/#23 fooled the "
"majority. A 3rd family did NOT reduce the panel false-confirms because the failures are CORRELATED "
"across families — conservative majority only protects against UNCORRELATED error. The fix is a "
"different lever (prompt hardening, #171), not more seats. Receipt: citation-panel-3family-receipt.json "
"(PIN: seats incl. granite tag + gguf + hf repo, verify_prompt_sha256, per-source abstract sha256)."
)

body170 = (
"DONE (2026-06-03, Move #2): surface prism's FULL retrieved abstract to the local panel. Wave-6's "
"panel judged each citation against only prism's source_title + the single supporting_span its "
"groundedness lens surfaced; a faithful claim that the WHOLE abstract entails but no single span does "
"was wrongly escalated (the wave-6 e2e Kambhampati false-escalation).\n\n"
"FIX (both shipped products — branched, tested, CHANGELOG'd, NOT published; director release call):\n"
"- prism-verify (branch feat/citation-source-abstract): new CitationResult.source_abstract, populated "
"on the RESOLVED paths in engine.py (the abstract is already retrieved to ground the lens; prism "
"stopped discarding it) and flowing to the `verify --type citations` JSON via model_dump. +1 "
"integration test; 30 citation/engine tests green. Additive, non-breaking. Will be prism v0.6.\n"
"- role-os (branch feat/local-panel-full-abstract): buildEvidence now PREFERS source_abstract (falls "
"back to the span on older prism builds); gateCitations threads it through. +3 tests, 1199 total "
"green.\n\n"
"E2E (e2e_full_abstract.mjs — role-os's SHIPPED buildEvidence + runOffloadPanel against live "
"llama-swap; arXiv 429-throttled so prism's retrieved evidence stubbed from the sha-pinned cache, the "
"wave-6 workaround). The 3 e2e-dispatch.md citations under the wave-9 per-family panel: span_only "
"regime -> faithful c1(Kambhampati)=refuted, c2(Huang)=insufficient (the bug reproduced); "
"full_abstract regime -> c1=SUPPORTED, c2=SUPPORTED (FIXED), planted inversion c3(self-recognition "
"inversion of arXiv:2404.13076)=refuted under BOTH (still caught, the fix adds no false-confirm). "
"Receipt: verifier/e2e-full-abstract-receipt.json. Pairs with role-os's full-abstract change so the "
"panel re-checks against the whole abstract, not one span."
)

body171 = (
"DONE (2026-06-03, the headline): the verifier HARDENING that closes the correlated-failure ceiling "
"#169 surfaced. The 24-case adversarial set broke the panel's 0-false-confirm property (#21/#22/#23 — "
"a direction inversion + two plausible-but-unstated additions — fooled a MAJORITY of seats across all "
"families). A 3rd family didn't help (correlated error). The lever that DID: a HARDENED verify system "
"prompt with two explicit decompositional rules — (1) DIRECTION CHECK (a claim that reverses a "
"comparison/effect direction -> refuted) and (2) ADDED-SPECIFIC CHECK (a claim asserting an entity/"
"number/ranking not in the evidence -> insufficient, even if the rest is supported).\n\n"
"MEASURED (prompt_hardening_probe.py, per-family panel, 24 cases): default prompt 79.2% / 3 fc "
"(#21,#22,#23) -> HARDENED 87.5% / 0 fc. Recovered ALL 3; NO regressions. Per-seat: qwen3-14b 1->0 fc, "
"mistral-nemo-12b 4->0 fc, granite-3.3-8b 8->2 fc (accuracy up on both). The hardened prompt is now the "
"offload `_V_SYS` DEFAULT (sha256 c7ea81d5...; the legacy wave-5/6 prompt preserved as _V_SYS_LEGACY; "
"OFFLOAD_VERIFY_SYS_FILE overrides). role-os --local-panel inherits it automatically (it shells "
"offload). Receipt: verifier/prompt-hardening-receipt.json.\n\n"
"LITERATURE-GROUNDED (the wave-9 study-swarm, research-raw.md). The ceiling is known: Kim et al. 2025 "
"(arXiv:2506.07962, capability convergence drives correlated errors even across providers); Kuncheva & "
"Whitaker 2003 (majority-vote accuracy is bounded by member correlation); Verga et al. 2024 PoLL "
"(arXiv:2404.18796, diverse panels fix idiosyncratic bias, NOT shared reasoning error). The fix is "
"predicted: Li et al. 2022 (arXiv:2210.04695, LMs are poor at DIRECTIONAL inference — exactly the #22 "
"failure); Zheng et al. 2025 (arXiv:2506.07446, atomic decomposition raises precision). HONEST "
"CEILING: prompt-only is PARTIAL (granite still 2 fc; directional/sycophantic biases are training-"
"baked) -> the durable fix pairs the hardened prompt with a mechanistically-orthogonal verifier "
"(a dedicated NLI/entailment + deterministic floor — which prism's existence floor + numeric guard "
"already partially provide, sitting UNDER the panel) and calibrated abstention. Carried as the wave-9 "
"NEXT."
)

body172 = (
"DONE (2026-06-03, Move #3): ONE real study-swarm wave run through BOTH offload paths, measured end-to-"
"end (wave9_dogfood.py) — proves the wiring in anger, not on fixtures. The wave: 3 parallel research "
"agents (research-grounded-advisor protocol) grounding the wave-9 correlated-failure finding "
"(research-raw.md; the same findings cited in #171).\n\n"
"PREREAD (token economy across a real wave): `offload compress` on the 3 agent outputs -> agent-A "
"1046->78, agent-B 992->112, agent-C 1095->135 Claude-tokens; AGGREGATE 3133 -> 325 = **89.6% saved "
"(2808 tokens)** across 3 sources, faithful digests (qwen3-4b, 90-word budget). The 'before/after "
"across a real wave' the offload kickoff asked for (cf. the wave-6 fixtures-only 92.1%).\n\n"
"VERIFY (the swarm's citations through the wave-9 hardened panel, against the cited papers' REAL "
"Semantic-Scholar abstracts): 17 citations submitted, all 17 resolved (0 fabricated / existence-floor "
"catches), 16 SUPPORTED, 1 FLAGGED -> escalate. The catch is REAL: [B2] arXiv:2508.17536 'Debate or "
"Vote' — the agent claimed 'agent diversity is the key factor', but the abstract's actual finding is "
"'Majority Voting alone accounts for most of the performance gains'; the hardened panel (qwen14b="
"refuted, nemo=insufficient, granite=refuted -> conservative majority REFUTED) CAUGHT the "
"mischaracterization. The EXTERNAL_VERIFIER earning its keep on a real study-swarm's output. Receipt: "
"verifier/wave9-dogfood-receipt.json (PIN: panel seats + verify_prompt_sha256 + per-source abstract "
"sha256)."
)

recipes = [
  (169, "llm-serving-verifier-3rd-family-granite-correlated-failure-ceiling",
   "3rd verifier family (IBM Granite 3.3 8B) added to the offload panel: improves accuracy + absorbs uncorrelated slips, but family diversity does NOT fix correlated false-confirms (measured)",
   "file:///tensor-engine-knowledge/verifier/citation-panel-3family-receipt.json", body169),
  (170, "llm-serving-verifier-full-abstract-evidence-prism-roleos",
   "full-abstract evidence to the local panel: prism-verify CitationResult.source_abstract + role-os buildEvidence prefers it; e2e flips faithful claims insufficient->supported, inversion still caught",
   "file:///tensor-engine-knowledge/verifier/e2e-full-abstract-receipt.json", body170),
  (171, "llm-serving-verifier-prompt-hardening-correlated-false-confirm-fix",
   "hardened verify prompt (direction-check + added-specific-check) recovers the correlated false-confirms a 3rd family can't: per-family panel 3fc->0fc, 79.2%->87.5%, no regressions; now the offload default",
   "file:///tensor-engine-knowledge/verifier/prompt-hardening-receipt.json", body171),
  (172, "llm-serving-offload-real-wave-dogfood-preread-and-panel",
   "real study-swarm dogfood of both offload paths: 89.6% preread token saving across 3 agent outputs + the hardened panel catching a real agent mischaracterization (16/17 supported, 1 flagged)",
   "file:///tensor-engine-knowledge/verifier/wave9-dogfood-receipt.json", body172),
]
c.execute("DELETE FROM config_recipes WHERE id IN (169,170,171,172)")
for rid, slug, name, url, body in recipes:
    c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
    VALUES (?,?,?,?,?,?,?,?,?)""", (rid, slug, name, 2, 15, "recipe", url, body, wave9))

# --- mark #156 (wave-5) + #162 (wave-6) "3rd family" open item DONE ---
upd156 = ("\n\n[UPDATE 2026-06-03 wave-9]: the 'Still open: a 3rd family' item is DONE — IBM Granite "
          "3.3 8B (Apache-2.0) is now the 3rd panel family (#169). Measured finding: a 3rd family improves "
          "accuracy + absorbs UNCORRELATED slips but does NOT fix CORRELATED false-confirms; the hardened "
          "prompt (#171) does. Default panel is now qwen3-14b + mistral-nemo-12b + granite-3.3-8b.")
upd162 = ("\n\n[UPDATE 2026-06-03 wave-9]: the '3rd family (Phi/Granite/Gemma)' NEXT is DONE — IBM Granite "
          "3.3 8B added (#169); the panel default is now the per-family 3-seat (qwen3-14b + mistral-nemo-12b "
          "+ granite-3.3-8b) with the HARDENED verify prompt (#171). The full abstract is now surfaced to the "
          "panel (#170, prism source_abstract + role-os buildEvidence), fixing the truncated-span false-"
          "escalation. role-os --local-panel inherits all three automatically (it shells offload).")
for rid, upd, tag in [(156, upd156, "wave-9"), (162, upd162, "wave-9")]:
    row = c.execute("SELECT body FROM config_recipes WHERE id=?", (rid,)).fetchone()
    if row and "[UPDATE 2026-06-03 wave-9]" not in row[0]:
        c.execute("UPDATE config_recipes SET body=? WHERE id=?", (row[0] + upd, rid))
        print(f"updated #{rid} (3rd-family open item -> done)")

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0], "| waves:", c.execute("SELECT count(*) FROM waves").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id", (wave9,)):
    print(" ", r[0], r[1], "|", r[2][:78])
db.close()
