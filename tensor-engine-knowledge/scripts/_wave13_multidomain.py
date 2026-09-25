"""Wave-13 — test the orthogonal NLI seat's generality beyond AI/ML + a disagreement-gated consensus.
Idempotent on wave_number=13 + recipe id 176. Hands-on + measured on the live RTX 5090 / llama-swap :9090
(2026-06-03). THE GENERALITY TEST BROKE THE VERIFIER (the first false-confirms in the arc): numeric-
comparison + unit claims on physics abstracts false-confirm BOTH the LLM panel and the NLI seat. Recipe #176."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

c.execute("DELETE FROM waves WHERE wave_number=13")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (13,?,?,?,?,?,?,?,?)""", (
  "Generality test (physical-sciences abstracts) + a disagreement-gated consensus — the verifier's 0-false-confirm property is DOMAIN-DEPENDENT; numeric-comparison + unit claims break BOTH learned verifiers",
  "2026-06-03",
  "llm-serving (verifier panel — generality + consensus gate)",
  0,
  "HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090 (LLM panel ran LIVE on offload's PROMOTED "
  "wave-12 default). THE GENERALITY TEST BROKE THE VERIFIER — the first false-confirms in the whole arc, "
  "which is what a rigorous test should find. On 17 physics cases (LIGO/ATLAS/CMS/Planck/EHT, real sha-pinned "
  "abstracts): NLI doc-level drops to 76.5% with 2 FALSE-CONFIRMS (#48 'exceeded' missing 5.0<5.8; #55 "
  "milliarcseconds vs microarcseconds), and the CORRELATED-failure ceiling RE-EMERGES — #48/#55 false-confirm "
  "BOTH the LLM panel AND the orthogonal NLI seat (#55 fooled all 3 LLM seats + NLI). Mechanistic "
  "orthogonality REDUCES but does not ELIMINATE correlated error; quantitative-comparison + unit failure modes "
  "are shared by a decoder LLM and an encoder NLI alike. The combination's value is real but partial (#45 the "
  "NLI floor caught a panel false-confirm; #41 the panel did arithmetic the NLI couldn't). The consensus gate "
  "fixes the #26 residual on AI/ML (escalate instead of auto-refuting a true claim; 0 fc on the 39) but "
  "inherits the correlated blind spot. The durable fix = a mechanistically-THIRD, DETERMINISTIC numeric/unit "
  "verifier (wave-14). Receipt: verifier/citation-panel-multidomain-receipt.json.",
  "synthesized",
  "Wave-13 candidate (larger multi-domain set + the #26 residual) + verifier/_wave13_fetch.py + citations-multidomain.json + citation_panel_eval_multidomain.py",
  "Recipe #176. Honest negative finding: the 0-fc property is DOMAIN-DEPENDENT (AI/ML-validated, physics-broken). Wave-14 = a deterministic numeric/unit checker (the third, non-learned mechanism)."
))
wave13 = c.execute("SELECT id FROM waves WHERE wave_number=13").fetchone()[0]
print("wave13 id =", wave13)

body176 = (
"DONE (2026-06-03): test the orthogonal NLI seat's GENERALITY beyond AI/ML + a disagreement-gated consensus. "
"THE GENERALITY TEST BROKE THE VERIFIER (the first false-confirms in the whole arc — exactly what a rigorous "
"test should find). Fetched 5 real physical-sciences abstracts (LIGO GW150914, ATLAS + CMS Higgs, Planck "
"2015, EHT M87; Semantic Scholar, sha-pinned, separate cache) + authored 17 gold-verified cases "
"(`citations-multidomain.json`) spanning numeric / inversion / scope / UNIT / paraphrase.\n\n"
"MEASURED (citation_panel_eval_multidomain.py; the LLM panel ran LIVE on offload's PROMOTED wave-12 default):\n"
"- NLI doc-level GENERALITY DROPS: 76.5% (vs 100% on AI/ML), with 2 FALSE-CONFIRMS — #48 (it read '5.0σ "
"exceeded 5.8σ' as supported, missing 5.0<5.8) and #55 (matched '42' + 'diameter', missing milliarcseconds "
"vs MICROarcseconds), plus #41 wrong-refuted a 36+29=65 sum (P=0.74 contradiction). The wave-10/11 'NLI is "
"robust / handles numerics' finding was AI/ML-SPECIFIC; the seat has real blind spots (quantitative "
"comparison, units) on a numeric-heavy domain.\n"
"- THE CORRELATED-FAILURE CEILING RE-EMERGES ACROSS MECHANISMS: #48 (comparison 'exceeded') and #55 (unit "
"milli/micro) FALSE-CONFIRMED BOTH the LLM panel AND the orthogonal NLI seat (#55 fooled all 3 LLM seats + "
"the NLI). Mechanistic orthogonality REDUCES correlated error but does NOT eliminate it — some quantitative "
"failure modes are shared by a decoder LLM and an encoder NLI alike.\n"
"- THE COMBINATION'S VALUE IS REAL BUT PARTIAL: on #45 ('5.0σ' vs the stated 5.9σ) the NLI floor CAUGHT a "
"panel false-confirm (uncorrelated — NLI refuted P=0.99, panel slipped); on #41 the LLM panel did the "
"arithmetic the NLI couldn't (then the floor over-escalated it). Each covers SOME of the other's blind spots; "
"neither covers the CORRELATED ones.\n\n"
"CONSENSUS GATE (the #26 residual fix — 'supported' only if BOTH mechanisms agree, a disagreement on the "
"supported axis -> escalate/REVIEW): cleanly fixes #26 on the 39 AI/ML cases (panel=refuted + NLI=supported "
"-> consensus=insufficient/review instead of confidently auto-refuting a TRUE claim; 0 fc preserved on the "
"39) and escalates uncorrelated disagreements (#41/#45 on physics). But it INHERITS the correlated blind spot "
"(#48/#55 both-supported -> consensus supported), so consensus is NOT 0-fc on physics either — no two-"
"verifier combination can catch a case both verifiers fail.\n\n"
"HONEST TAKEAWAY (KB INTEGRITY): the verifier's 0-false-confirm property is DOMAIN-DEPENDENT — validated for "
"AI/ML citation traps (waves 6-12), but numeric-COMPARISON ('exceeded') and UNIT (milli vs micro) claims on "
"physics abstracts break it across BOTH learned verifiers. The durable fix is a mechanistically-THIRD "
"verifier that is DETERMINISTIC, not learned: a numeric/unit extractor-comparator (parse quantities + units "
"from claim vs evidence and compare arithmetically) — the quantity analog of prism's existence floor, which "
"neither an LLM nor an NLI provides. That is the wave-14 candidate. Receipt: verifier/citation-panel-"
"multidomain-receipt.json (PIN: multidomain sha256, per-abstract sha256, NLI scores, the live LLM votes)."
)

c.execute("DELETE FROM config_recipes WHERE id IN (176)")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (?,?,?,?,?,?,?,?,?)""", (
  176, "llm-serving-verifier-generality-limit-and-consensus-gate",
  "generality test breaks the verifier: on physics abstracts the 0-false-confirm property FAILS — numeric-comparison (#48 'exceeded') + unit (#55 milli/micro) claims false-confirm BOTH the LLM panel and the orthogonal NLI seat (correlated); a consensus gate fixes the #26 residual on AI/ML but inherits the blind spot; the fix is a deterministic numeric/unit checker (wave-14)",
  2, 15, "recipe", "file:///tensor-engine-knowledge/verifier/citation-panel-multidomain-receipt.json", body176, wave13))

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0],
      "| waves:", c.execute("SELECT count(*) FROM waves").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id", (wave13,)):
    print(" ", r[0], r[1], "|", r[2][:84])
db.close()
