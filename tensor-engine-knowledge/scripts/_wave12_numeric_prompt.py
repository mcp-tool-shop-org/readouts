"""Wave-12 — refine the verify prompt's added-specific-check with a QUANTITY EXCEPTION so the LLM panel
stops over-escalating legitimate numeric paraphrases (wave-11 #25/#26/#27). Idempotent on wave_number=12 +
recipe id 175. Hands-on + measured on the live RTX 5090 / llama-swap :9090 (2026-06-03). A CLEAN WIN,
adoptable via OFFLOAD_VERIFY_SYS_FILE and PROMOTED to offload's default with Mike's sign-off + verified.
Recipe #175."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

c.execute("DELETE FROM waves WHERE wave_number=12")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (12,?,?,?,?,?,?,?,?)""", (
  "Numeric-paraphrase prompt fix — a QUANTITY EXCEPTION in the verify prompt's added-specific-check (closes the wave-11 over-escalation; clean win, 0 new false-confirms)",
  "2026-06-03",
  "llm-serving (verifier panel — verify-prompt refinement)",
  0,
  "HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090 (refined panel ran LIVE on 39 cases). Closes "
  "the wave-11 finding that the hardened added-specific-check over-escalates legitimate numeric PARAPHRASES "
  "(it stamped 'fewer than two-thirds' of 23/36, 'more than half', 'roughly 200' of N=199 as insufficient). "
  "Surgical fix = a QUANTITY EXCEPTION: a number that is a restatement/rounding/one-step arithmetic "
  "consequence of a STATED quantity is NOT 'added' (evaluate under support/contradiction); a CONTRADICTORY "
  "number is still refuted; an ABSENT number is still insufficient. CLEAN WIN, 0 false-confirms everywhere, "
  "no trap regressions: 24-case 87.5->95.8% (also fixed #8 'over 100,000' + #20 'all 36' insufficient->"
  "refuted), hard-15 73.3->86.7% (#25/#27 fixed), combined 82.1->92.3%. Honest residual: #26 went "
  "insufficient->refuted (still a safe miss; NLI doc-level gets it right). Adoptable via "
  "OFFLOAD_VERIFY_SYS_FILE; PROMOTED to offload's DEFAULT with Mike's sign-off + verified (byte-identical to "
  "verify_sys_numeric.txt; the CLI returns supported on #25; _V_SYS_HARDENED_V1 preserved; role-os inherits "
  "it). Receipt: verifier/citation-panel-prompt-v2-receipt.json.",
  "synthesized",
  "Wave-12 candidate (LLM-prompt refinement for numeric over-escalation) + verifier/verify_sys_numeric.txt + citation_panel_eval_prompt_v2.py",
  "Recipe #175. PROMOTED to offload's default with Mike's sign-off + verified (byte-identical to verify_sys_numeric.txt; `offload verify --panel` returns supported on #25); _V_SYS_HARDENED_V1 preserved; role-os --local-panel inherits it via the shelled CLI."
))
wave12 = c.execute("SELECT id FROM waves WHERE wave_number=12").fetchone()[0]
print("wave12 id =", wave12)

body175 = (
"DONE (2026-06-03): refine the verify prompt's added-specific-check with a QUANTITY EXCEPTION so the LLM "
"panel stops over-escalating legitimate numeric PARAPHRASES (wave-11 #25/#26/#27). The wave-9 hardened "
"prompt's added-specific rule treated ANY number not literally in the evidence as 'added' -> insufficient, "
"so it stamped 'fewer than two-thirds' (of 23/36), 'more than half', and 'roughly 200' (of N=199) as "
"INSUFFICIENT where NLI doc-level correctly said SUPPORTED. The surgical fix (`verifier/verify_sys_numeric."
"txt`, sha 593a06d9…): a number that is a faithful restatement / rounding / one-step arithmetic consequence "
"of a STATED quantity is NOT 'added' (evaluate it under the contradiction/support rules); a CONTRADICTORY "
"number is still refuted; a genuinely-ABSENT number is still insufficient.\n\n"
"MEASURED (citation_panel_eval_prompt_v2.py; the refined panel ran LIVE on all 39 cases via the wave-9 "
"OFFLOAD_VERIFY_SYS_FILE override; reused the pinned hardened + NLI-doc verdicts). CLEAN WIN, 0 false-"
"confirms EVERYWHERE, no trap regressions:\n"
"- 24-case (canonical traps): 87.5% -> 95.8% — the contradictory-number clause ALSO fixed #8 'over 100,000' "
"and #20 'all 36' (insufficient -> refuted, the correct verdict)\n"
"- hard-15 (numeric paraphrases): 73.3% -> 86.7% — #25 and #27 (insufficient -> supported)\n"
"- combined-39: 82.1% -> 92.3%\n"
"Trap regression check: #8/#20 refuted, #21/#22/#23 still caught, #39 still insufficient — and 0 new false-"
"confirms anywhere. HONEST RESIDUAL: #26 ('more than half' of 23/36) went insufficient -> REFUTED (still a "
"miss vs gold=supported, but still SAFE — it escalates, never a false-confirm; NLI doc-level gets #26 right, "
"so the LLM+NLI combination still covers it).\n\n"
"ADOPTION: PROMOTED to offload's inline DEFAULT with Mike's sign-off (2026-06-03); the prior hardened prompt "
"is preserved as `_V_SYS_HARDENED_V1` (fallback) alongside `_V_SYS_LEGACY`, both still selectable via "
"OFFLOAD_VERIFY_SYS_FILE. VERIFIED: offload's default is byte-identical to the tested verify_sys_numeric.txt "
"(sha 593a06d9 = the receipt's refined sha) and the CLI role-os shells (`offload verify --panel`, no "
"override) returns SUPPORTED on #25 — role-os --local-panel inherits the win automatically (offload.py "
"edited in studio-local; the readouts repo is unchanged). EXTERNAL_VERIFIER: the labeled 24+15 "
"sets + the independent NLI doc seat confirmed the fix adds no false-confirm and breaks no trap. Receipt: "
"verifier/citation-panel-prompt-v2-receipt.json (PIN: refined-prompt sha256, hardened sha256, the live "
"refined votes, numeric-fix + trap-regression case lists)."
)

c.execute("DELETE FROM config_recipes WHERE id IN (175)")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (?,?,?,?,?,?,?,?,?)""", (
  175, "llm-serving-verifier-numeric-quantity-exception-prompt-fix",
  "QUANTITY EXCEPTION in the verify prompt's added-specific-check: stops over-escalating numeric paraphrases (23/36 -> 'fewer than two-thirds') while keeping contradictory/absent numbers refuted/insufficient — clean win (24-case 87.5->95.8%, hard 73.3->86.7%, 0 new false-confirms); PROMOTED to offload's default (role-os inherits it) with Mike's sign-off + verified",
  2, 15, "recipe", "file:///tensor-engine-knowledge/verifier/citation-panel-prompt-v2-receipt.json", body175, wave12))

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0],
      "| waves:", c.execute("SELECT count(*) FROM waves").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id", (wave12,)):
    print(" ", r[0], r[1], "|", r[2][:84])
db.close()
