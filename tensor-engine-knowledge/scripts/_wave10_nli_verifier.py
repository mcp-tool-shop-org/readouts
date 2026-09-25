"""Wave-10 — a MECHANISTICALLY-ORTHOGONAL NLI verifier seat that breaks the correlated false-confirm
ceiling family diversity could not. Idempotent on wave_number=10 + recipe id 173. Hands-on + measured on
the live RTX 5090 (2026-06-03): an encoder NLI cross-encoder (DeBERTa-v3-large NLI, MIT) added as a
monotone-safe FLOOR under the offload LLM panel. Closes the wave-9 #171 NEXT."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

c.execute("DELETE FROM waves WHERE wave_number=10")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (10,?,?,?,?,?,?,?,?)""", (
  "Mechanistically-orthogonal NLI verifier seat — breaks the correlated false-confirm ceiling family diversity couldn't (encoder NLI cross-encoder as a monotone-safe floor)",
  "2026-06-03",
  "llm-serving (verifier panel — orthogonal NLI floor + calibrated abstention)",
  0,
  "HANDS-ON + MEASURED on the live RTX 5090 (no research swarm). THE FINDING: wave-9's 3-family LLM panel "
  "(all decoder-only instruct = SAME mechanism) shares a CORRELATED credulity blind spot (#21/#22/#23; #22 "
  "fooled all three families); conservative majority + a 3rd family cannot catch a CORRELATED slip "
  "(Kuncheva & Whitaker 2003 — majority-vote accuracy is bounded by member CORRELATION, not count). The "
  "durable fix is a member that FAILS DIFFERENTLY: an encoder NLI cross-encoder (DeBERTa-v3-large MNLI+FEVER"
  "+ANLI+LingNLI+WANLI, MIT; reasoning-stripped, no prompt). MEASURED on the 24-case adversarial set: NLI "
  "seat SOLO 100%/0fc (8/8 traps), catches ALL 3 correlated false-confirms; combined LLM-panel + NLI FLOOR "
  "(veto on 'supported', downgrade-only -> CANNOT add a false-confirm) holds 0fc under BOTH the legacy "
  "(79.2->91.7%) and the hardened (87.5%) prompt; the floor BEATS a 4th-seat majority (which still slips "
  "#22 — the correlated bloc out-votes the orthogonal seat). HONEST: n=24 small + the traps are NLI-"
  "canonical, so 100% is not a general claim; the durable value is the COMBINATION (LLM reasoning + NLI "
  "orthogonal floor), and the floor is monotone-safe. Receipt: verifier/citation-panel-nli-receipt.json.",
  "synthesized",
  "KICKOFF (wave-10 candidate: mechanistically-orthogonal verifier seat) + verifier/nli_verify.py + citation_panel_eval_nli.py",
  "Closes the wave-9 #171 NEXT (mechanistically-orthogonal verifier + calibrated abstention). Recipe #173. Companion: studio-local/nli_floor.py."
))
wave10 = c.execute("SELECT id FROM waves WHERE wave_number=10").fetchone()[0]
print("wave10 id =", wave10)

body173 = (
"DONE (2026-06-03, the wave-10 headline — closes the wave-9 #171 NEXT). Stood up a MECHANISTICALLY-"
"ORTHOGONAL verifier seat and MEASURED that it breaks the correlated-failure ceiling that family diversity "
"could not. Wave-9 proved the 3-family LLM panel (qwen3-14b + mistral-nemo-12b + granite-3.3-8b, all "
"decoder-only instruct models = the SAME mechanism) shares a CORRELATED credulity blind spot: on the "
"24-case adversarial set it false-confirmed #21/#22/#23 (a stricter/looser inversion + two plausible-but-"
"unstated additions); #22 fooled all three families. Conservative majority + a 3rd family can't catch a "
"CORRELATED slip (Kuncheva & Whitaker 2003: majority-vote accuracy is bounded by member CORRELATION, not "
"count). The hardened prompt (#171) recovered them, but that is a patch on the SAME mechanism.\n\n"
"THE SEAT: an encoder NLI cross-encoder — MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli "
"(DeBERTa-v3-large base, MIT; ~435M; FEVER in the mix = fact-verification, the exact shape of a citation "
"check). A DIFFERENT mechanism (bidirectional encoder, discriminative 3-way classifier, NO chain-of-"
"thought, NO prompt) so its errors decorrelate from the LLM bloc. Mapping (NLI premise = evidence title+"
"abstract, hypothesis = claim): entailment->supported, contradiction->refuted, neutral->insufficient. "
"ASYMMETRIC calibrated abstention: return 'supported' ONLY if argmax==entailment AND P(ent)>=TAU_SUPPORT "
"(default 0.55), else downgrade a would-be 'supported' to 'insufficient' — refuted/insufficient are NOT "
"thresholded (only a false-CONFIRM is dangerous; over-escalation is the safe failure). Runs on the rig's "
"unsloth-env (torch 2.12 cu130 sm_120), 435M loads on CUDA, ~sub-second/case; NOT on llama-swap — that's "
"the point, it is OFF the LLM serving stack. id2label confirmed at load {0:entailment,1:neutral,2:"
"contradiction} (not hard-coded).\n\n"
"MEASURED (citation_panel_eval_nli.py; the LLM votes are REUSED sha-pinned from prompt-hardening-receipt."
"json — the LLMs ran in wave-9 against the SAME sha-pinned abstracts, so the core property needs no live "
"llama-swap). NLI seat SOLO on the 24-case set: 100% (24/24), 0 false-confirms, 8/8 on the traps — catches "
"ALL THREE correlated false-confirms (#21 insufficient P(neutral)=0.95, #22 refuted P(contradiction)=0.999, "
"#23 insufficient) that every LLM family slipped. COMBINED LLM-panel + NLI FLOOR (NLI as a veto on "
"'supported' — downgrade only, never upgrade, so it CANNOT add a false-confirm): legacy prompt 79.2%/3fc "
"-> +floor 91.7%/0fc (orthogonality breaks the ceiling WITHOUT the prompt patch); hardened prompt 87.5%/0fc "
"-> +floor 87.5%/0fc (no regression — an INDEPENDENT backstop). The FLOOR BEATS a 4th-seat MAJORITY: "
"majority still false-confirms #22 (the correlated LLM bloc out-votes the orthogonal seat 3-1) — validating "
"the asymmetric VETO over naive voting. TAU robust (0fc across 0.50-0.90 on this set). Live e2e (studio-"
"local/nli_floor.py --demo vs llama-swap UP): with the hardened default both the panel AND the NLI seat "
"refute #22 (belt-and-suspenders).\n\n"
"WIRING: verifier/nli_verify.py (the seat + CLI/smoke) + studio-local/nli_floor.py (the COMPANION — the "
"wave-6 #164 pattern: composes `offload`'s LLM panel + the NLI floor WITHOUT editing offload.py/stdlib or "
"any MCP; --nli-only runs the seat alone when llama-swap is down). role-os's citation gate can call "
"nli_floor for the orthogonal backstop under the existing panel.\n\n"
"HONEST CAVEATS: n=24 is small and the traps are NLI-CANONICAL patterns (inversions->contradiction, "
"unstated->neutral) — the model's home turf, so 100% here is NOT a general accuracy claim. The durable "
"value is the COMBINATION, not NLI-alone: the LLM panel handles reasoning the NLI lacks (multi-hop, "
"numeric, world knowledge), the NLI floor vetoes the LLM's credulity slips, and the floor is MONOTONE-SAFE "
"so NLI errors on other distributions degrade to over-escalation (safe), never a false-confirm. Document-"
"level NLI (claim vs whole abstract); sentence-level FEVER-style evidence selection is the next refinement. "
"Receipt: verifier/citation-panel-nli-receipt.json (PIN: model+license+tau+mapping, the reused LLM-vote "
"receipt sha256, per-source abstract sha256)."
)

c.execute("DELETE FROM config_recipes WHERE id IN (173)")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (?,?,?,?,?,?,?,?,?)""", (
  173, "llm-serving-verifier-orthogonal-nli-floor-correlated-failure-fix",
  "mechanistically-orthogonal NLI floor (DeBERTa-v3 NLI, MIT) under the LLM panel: catches the correlated false-confirms a 3rd family + prompt-hardening can't fully fix — SOLO 100%/0fc on the 24-case set, combined floor holds 0fc (legacy + hardened), monotone-safe, beats a 4th-seat majority",
  2, 15, "recipe", "file:///tensor-engine-knowledge/verifier/citation-panel-nli-receipt.json", body173, wave10))

# --- mark #171 (wave-9) "mechanistically-orthogonal verifier" NEXT as DONE ---
upd171 = ("\n\n[UPDATE 2026-06-03 wave-10]: the 'mechanistically-orthogonal verifier (a dedicated NLI/"
          "entailment + calibrated abstention)' NEXT is DONE (#173). An encoder NLI cross-encoder "
          "(DeBERTa-v3-large NLI, MIT) added as a MONOTONE-SAFE floor under the LLM panel: SOLO 100%/0fc on "
          "the 24-case set, catches all 3 correlated false-confirms (#21/#22/#23); the combined panel holds "
          "0fc under BOTH the legacy (79.2->91.7%) and the hardened prompt; the floor beats a 4th-seat "
          "majority (which still slips #22). Companion: studio-local/nli_floor.py.")
row = c.execute("SELECT body FROM config_recipes WHERE id=171").fetchone()
if row and "[UPDATE 2026-06-03 wave-10]" not in row[0]:
    c.execute("UPDATE config_recipes SET body=? WHERE id=171", (row[0] + upd171,))
    print("updated #171 (mechanistically-orthogonal verifier NEXT -> done)")

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0],
      "| waves:", c.execute("SELECT count(*) FROM waves").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id", (wave10,)):
    print(" ", r[0], r[1], "|", r[2][:84])
db.close()
