"""Wave-5 #157 — token-economy findings + verifier size-floor appended to #156. Idempotent."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()
wave5 = c.execute("SELECT id FROM waves WHERE wave_number=5").fetchone()[0]

# append the verifier size-floor to #156
row = c.execute("SELECT body FROM config_recipes WHERE id=156").fetchone()
if row and "SIZE-FLOOR" not in row[0]:
    add = ("\n\nSIZE-FLOOR (swept smaller 2026-06-03): qwen3-1.7b = 64.3% (0 false-confirms; safe but weak), "
           "qwen3-0.6b = 50.0% with 3 FALSE-CONFIRMS (refuted 0/5 — confirms false claims, DANGEROUS). "
           "=> the verifier role has a HARD FLOOR at ~4B: below it accuracy collapses AND the safety property breaks. "
           "4B is the cheapest SAFE verifier; do not shrink it further.")
    c.execute("UPDATE config_recipes SET body=? WHERE id=156", (row[0]+add,))
    print("appended size-floor to #156")

body = (
"TOKEN-ECONOMY findings — small LOCAL models to cut Claude token usage (the ollama-intern philosophy, pushed further). Measured 2026-06-03 via llama-swap; scored by llama-server's completion_tokens (the model's own tokenizer = exact, deterministic ruler).\n\n"
"(A) BUDGET-ADHERENCE BASELINE — can a small model compress text to <= N tokens by SELF-REGULATING (no hard cap)? Models qwen3-0.6b/1.7b/4b/14b; budgets 60 & 120; 3 sources. "
"RESULT: small models do NOT self-regulate to a token budget — they emit a roughly FIXED-LENGTH summary driven by the SOURCE, not the requested N. At budget 60 (tight) every model overshoots a dense source (~140 tok REGARDLESS of size; fit 1/3); at budget 120 they undershoot (~0.7-0.9x). "
"CRITICAL: SIZE-INDEPENDENT — 14b is no better than 0.6b at hitting budgets => budget-adherence is a behavioral/skill gap, not a capability/scale gap (mirrors the verifier finding). A good LoRA target; scale does nothing.\n\n"
"(B) PROMPTING FIX (measure-before-training): models can't count TOKENS but have a rough sense of WORDS. Tested token- vs word- vs sentence-budget on the hard dense source at ~60 tok. "
"RESULT: WORD budgets beat token budgets. Best NON-TRAINED config = qwen3-4b + 'AT MOST 45 words' (fit 2/2; the token-budget prompt only 1/2; sentence-budget 1/2). qwen3-1.7b could not reliably compress dense text even with word budgets. "
"=> CHEAPEST FIX (free, no training): instruct a WORD budget (~0.75x the token target) on a >=4B model, plus a hard max_tokens cap as a deterministic backstop. The residual gap (reliability on dense text, sub-4B models, very tight budgets) is what a budget-adherence LoRA (Unsloth #155) would close.\n\n"
"NET GUIDANCE for a local 'context economizer' that pre-digests inputs so Claude reads less: (1) >=4B base; (2) WORD budget instruction, not token; (3) hard max_tokens backstop; (4) a budget-adherence LoRA only if you need sub-4B economizers or tight/reliable budgets. "
"Companion: the verifier size-floor (see #156) — verifier role floors at ~4B (0.6b false-confirms). "
"Artifacts: verifier/budget_bench.py, prompt_variant_bench.py, budget-results.json, variant-results.json. "
"NEXT (optional, user-gated): dogfood Unsloth #155 — train a budget-adherence LoRA on a tiny base (0.6b/1.7b) so the CHEAPEST model becomes budget-reliable; eval = before/after on budget_bench."
)
c.execute("DELETE FROM config_recipes WHERE id=157")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (157,?,?,?,?,?,?,?,?)""", (
  "token-economy-small-model-budget-adherence-baseline-and-word-budget-fix",
  "Token-economy: small models don't self-regulate to token budgets (size-independent); word-budget prompting is the free fix; LoRA is the residual",
  2, 15, "baseline",
  "https://github.com/mostlygeek/llama-swap",
  body, wave5))
db.commit()
print("inserted #157; recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
db.close()
