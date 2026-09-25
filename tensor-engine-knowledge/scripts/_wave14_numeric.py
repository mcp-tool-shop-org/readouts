"""Wave-14 (the capstone) — a DETERMINISTIC numeric/unit verifier, the THIRD non-learned mechanism, catches
the wave-13 correlated false-confirms that fooled BOTH learned verifiers and restores 0-false-confirm across
domains. Idempotent on wave_number=14 + recipe id 177. Measured on 56 labeled cases (stdlib; no GPU). #177."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

c.execute("DELETE FROM waves WHERE wave_number=14")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (14,?,?,?,?,?,?,?,?)""", (
  "Deterministic numeric/unit floor — the third, non-learned mechanism catches the correlated failures both learned verifiers shared, restoring 0-false-confirm across domains (the capstone)",
  "2026-06-03",
  "llm-serving (verifier panel — deterministic numeric/unit floor)",
  0,
  "MEASURED on all 56 labeled cases (stdlib, no GPU). The wave-13 generality test found 2 correlated false-"
  "confirms (#48 numeric comparison, #55 unit) that fooled BOTH the LLM panel AND the orthogonal NLI seat. "
  "Wave-14 adds the fix the finding named: a DETERMINISTIC numeric/unit verifier (numeric_floor.py) — the "
  "quantity analog of prism's existence floor, a refute-or-abstain mechanism that can't be fooled by surface "
  "plausibility. It catches BOTH #48 (5.0<5.8 so not 'exceeded') and #55 (42 milli- vs micro-arcsec, the case "
  "that fooled all 4 learned verifiers) with 0 false-refutes across all 56 cases (100% precision). THE FULL "
  "STACK RESTORES 0-FALSE-CONFIRM ON PHYSICS: + the numeric floor takes nli_doc / NLI-veto-floor / consensus "
  "from 2 fc to 0 fc (the complete deterministic-floor + LLM-panel + NLI-floor stack = 0 fc on BOTH AI/ML and "
  "physics). Validates defense-in-depth: three mechanistically-DIFFERENT layers each catch what the others "
  "miss. Receipt: verifier/citation-panel-numeric-receipt.json.",
  "synthesized",
  "Wave-14 candidate (a deterministic numeric/unit checker) + verifier/numeric_floor.py + citation_panel_eval_numeric.py",
  "Recipe #177. The capstone of the verifier arc: deterministic floor (existence + numeric/unit) -> LLM panel -> NLI floor, 0-fc across domains. Honest residual: the comparison rule is targeted (shared-noun anchor) and abstains safely on structures it can't bind."
))
wave14 = c.execute("SELECT id FROM waves WHERE wave_number=14").fetchone()[0]
print("wave14 id =", wave14)

body177 = (
"DONE (2026-06-03, THE CAPSTONE): a DETERMINISTIC numeric/unit verifier — the THIRD, non-learned mechanism — "
"catches the wave-13 correlated false-confirms that fooled BOTH learned verifiers, restoring 0-false-confirm "
"across domains. `verifier/numeric_floor.py` is a REFUTE-OR-ABSTAIN floor (the quantity analog of prism's "
"existence floor): it returns 'refuted' ONLY on a PROVABLE quantitative contradiction, else abstains (falls "
"through to the learned verifiers), so it CANNOT add a false-confirm. Two rules: (1) UNIT-SCALE MISMATCH — "
"the claim states the same number as the evidence but a DIFFERENT metric prefix on the same base unit (42 "
"milli-arcsec vs 42 micro-arcsec); (2) COMPARISON-DIRECTION FALSEHOOD — the claim asserts A>B / A<B where A "
"and B each bind (via a discriminating modifier sitting ADJACENT to a shared quantity-noun — which "
"disambiguates 'expected background' from 'expected significance') to a DISTINCT explicit evidence number, "
"and the asserted relation is arithmetically false.\n\n"
"MEASURED (citation_panel_eval_numeric.py, ALL 56 labeled cases): catches BOTH wave-13 correlated misses — "
"#55 (42 milli vs micro arcsec — the case that fooled ALL FOUR learned verifiers) AND #48 ('observed 5.0σ "
"exceeded expected 5.8σ' -> 5.0<5.8) — with **0 FALSE-REFUTES ACROSS ALL 56 CASES (100% precision)**. THE "
"FULL STACK RESTORES 0-FALSE-CONFIRM ON PHYSICS: + the numeric floor takes nli_doc 2fc->0, the NLI-veto floor "
"2fc->0, and the consensus gate 2fc->0 (the llm_panel alone keeps #45, which the NLI floor catches -> the "
"complete deterministic-floor + LLM-panel + NLI-floor stack = 0 fc on BOTH AI/ML and physics).\n\n"
"This validates DEFENSE-IN-DEPTH: mechanistically-DIFFERENT layers (deterministic + decoder-LLM + encoder-"
"NLI) each catch what the others miss — the deterministic floor catches the quantitative-comparison + unit "
"failures the two LEARNED verifiers SHARE (and cannot catch), exactly as prism's existence floor catches "
"fabricated citations an LLM can't. HONEST RESIDUAL: the comparison rule is targeted (it needs a shared "
"quantity-noun to anchor + a discriminating modifier adjacent to it); it ABSTAINS safely on claims it can't "
"bind (0 false-refutes on the 56), so harder comparison structures fall through to the panel + the consensus "
"gate's human-review escalation — a high-precision floor, not a complete numeric reasoner. Receipt: "
"verifier/citation-panel-numeric-receipt.json (PIN: floor sha256, per-case rule+detail, the with/without-"
"floor physics metrics). The verifier arc now stands: deterministic floor (existence + numeric/unit) -> "
"3-family LLM panel (hardened + quantity-aware prompt) -> mechanistically-orthogonal NLI floor."
)

c.execute("DELETE FROM config_recipes WHERE id IN (177)")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (?,?,?,?,?,?,?,?,?)""", (
  177, "llm-serving-verifier-deterministic-numeric-unit-floor",
  "deterministic numeric/unit floor (the third, non-learned mechanism): catches the correlated false-confirms #48 (comparison 5.0<5.8) + #55 (unit milli/micro) that fooled BOTH learned verifiers, with 0 false-refutes on 56 cases (100% precision); restores 0-false-confirm across AI/ML + physics. The quantity analog of prism's existence floor",
  2, 15, "recipe", "file:///tensor-engine-knowledge/verifier/citation-panel-numeric-receipt.json", body177, wave14))

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0],
      "| waves:", c.execute("SELECT count(*) FROM waves").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id", (wave14,)):
    print(" ", r[0], r[1], "|", r[2][:84])
db.close()
