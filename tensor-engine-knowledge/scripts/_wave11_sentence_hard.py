"""Wave-11 — stress the orthogonal NLI seat beyond NLI-canonical traps + sentence-level evidence selection.
Idempotent on wave_number=11 + recipe id 174. Hands-on + measured on the live RTX 5090 / llama-swap :9090
(2026-06-03). A partly counter-hypothesis result: the hard set did NOT break the NLI doc-level seat (100%),
sentence-level HURTS (negative result, not adopted), and the hardened LLM panel over-escalates numeric
paraphrases. Recipe #174."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

c.execute("DELETE FROM waves WHERE wave_number=11")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (11,?,?,?,?,?,?,?,?)""", (
  "Stress the orthogonal NLI seat beyond NLI-canonical traps + sentence-level evidence selection (a hard 15-case set; a negative result on sentence-level; the hardened LLM panel over-escalates numerics)",
  "2026-06-03",
  "llm-serving (verifier panel — hard-set stress + sentence-level FEVER selection)",
  0,
  "HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090 (LLM panel ran LIVE on 15 new cases). A "
  "DECONFIRMING wave: (1) the hard set (numeric/multi-hop/scope/paraphrase grounded in the same sha-pinned "
  "abstracts) did NOT break NLI doc-level (100%/0fc/0-over-escalation) — the wave-10 NLI-canonical caveat is "
  "weaker than feared; (2) sentence-level FEVER selection is a NEGATIVE result (80% hard, 70.8% on the "
  "24-case regression vs doc-level 100%/100% — loses document context the numeric cases need), so doc-level "
  "STAYS the default; (3) the hardened LLM panel is the WEAKEST verifier here (73.3%) — its added-specific-"
  "check over-escalates legitimate numeric paraphrases (#25/#26/#27) and over-refutes a scope claim (#34); "
  "on ALL 4 NLI-vs-LLM disagreements NLI doc-level was right. 0 false-confirms across EVERY method (the "
  "safety property is universal on this set). Receipt: verifier/citation-panel-hard-receipt.json.",
  "synthesized",
  "Wave-11 candidate (sentence-level FEVER selection + a harder/larger labeled set) + verifier/citations-hard.json + citation_panel_eval_hard.py",
  "Recipe #174. Negative result on sentence-level (kept behind verify_one_sentencewise(), not promoted). The LLM numeric over-escalation is a future prompt-refinement lever, NOT a floor change."
))
wave11 = c.execute("SELECT id FROM waves WHERE wave_number=11").fetchone()[0]
print("wave11 id =", wave11)

body174 = (
"DONE (2026-06-03): stress the orthogonal NLI seat BEYOND the wave-10 NLI-canonical traps + add sentence-"
"level FEVER evidence selection. Authored `citations-hard.json` (15 cases grounded in the SAME 8 sha-pinned "
"abstracts; every gold verified against the abstract text) spanning NUMERIC/arithmetic (23/36 -> 'fewer than "
"two-thirds' / 'more than half'; N=199 -> 'roughly two hundred'), MULTI-HOP, SCOPE/added-entity, subtle "
"PARAPHRASE-supported, and harder inversions — the reasoning an encoder NLI classifier is theoretically weak "
"at and where the LLM panel should earn its seat.\n\n"
"SURPRISES (measured, citation_panel_eval_hard.py; the LLM panel ran LIVE on the hard set, hardened prompt):"
"\n1. The hard set did NOT break NLI doc-level: 100% (15/15), 0 fc, 0 over-escalation — INCLUDING the numeric "
"paraphrases (#25 supported P(ent)=.998, #26 .77, #27 .998) and the multi-hop cases. The wave-10 'NLI-"
"canonical caveat' is WEAKER than feared: the seat generalizes to non-canonical hard cases (this set).\n"
"2. Sentence-level is a NEGATIVE result — it HURTS: 80% on the hard set, 70.8% on the 24-case regression "
"(vs doc-level 100%/100%). It loses the document context the numeric cases need (no single sentence carries "
"'23/36 -> fewer than two-thirds'; #25 max-sentence-entailment .53, #26 .15) and over-splits. DOCUMENT-LEVEL "
"STAYS THE DEFAULT; sentence-level kept behind `verify_one_sentencewise()` for long-document cases, NOT "
"promoted.\n"
"3. On this set the HARDENED LLM PANEL is the WEAKEST verifier (73.3%) and NLI doc-level the strongest "
"(100%). The added-specific-check OVER-escalates legitimate numeric paraphrases (#25/#26/#27 -> insufficient; "
"the three seats even disagree among themselves) and over-refutes a scope claim (#34 -> refuted). On ALL 4 "
"NLI-vs-LLM disagreements, NLI doc-level was RIGHT.\n\n"
"FLOOR behavior: 0 false-confirms EVERYWHERE (the safety property is universal on this set). But the "
"monotone-safe floor can't IMPROVE accuracy here — it only downgrades an LLM 'supported', and the LLM "
"already over-escalated (no false 'supported' to veto), so floor_doc = 73.3% = the LLM panel; both floor "
"variants (veto-on-not-supported vs veto-on-contradiction-only) are IDENTICAL here because there was no LLM "
"false-confirm to catch (the distinction only bites when the LLM slips a 'supported', as on the legacy-"
"prompt 24-case set). 24-case regression with the doc-level floor is still 87.5%/0fc (matches wave-10).\n\n"
"TAKEAWAY: NLI doc-level is a strong STANDALONE verifier (robust past canonical traps) AND the safety floor "
"(0-fc, wave-10). The LLM panel's numeric over-escalation is a PROMPT issue (the added-specific-check is too "
"aggressive on numeric paraphrases) — a future LLM-prompt-refinement lever, NOT a floor change (a symmetric "
"NLI 'upgrade' would break monotone-safety = could add a false-confirm). HONEST CAVEATS: still small (15 "
"hard + 24 canonical), single domain (AI/ML abstracts); the NLI's numeric success may be paraphrase-pattern, "
"not true arithmetic. Receipt: verifier/citation-panel-hard-receipt.json (PIN: hard-set sha256, per-abstract "
"sha256, verify-prompt sha256, the live LLM votes)."
)

c.execute("DELETE FROM config_recipes WHERE id IN (174)")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (?,?,?,?,?,?,?,?,?)""", (
  174, "llm-serving-verifier-nli-hard-set-and-sentence-level-negative",
  "stress the orthogonal NLI seat beyond canonical traps (15-case hard set) + sentence-level FEVER selection: NLI doc-level holds 100%, sentence-level HURTS (not adopted), and the hardened LLM panel over-escalates numeric paraphrases (NLI right on all disagreements); 0 false-confirms everywhere",
  2, 15, "recipe", "file:///tensor-engine-knowledge/verifier/citation-panel-hard-receipt.json", body174, wave11))

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0],
      "| waves:", c.execute("SELECT count(*) FROM waves").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id", (wave11,)):
    print(" ", r[0], r[1], "|", r[2][:84])
db.close()
