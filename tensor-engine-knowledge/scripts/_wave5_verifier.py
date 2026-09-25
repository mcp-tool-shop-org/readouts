"""Wave-5 #156 — local family-different verifier on llama-swap, validated. Idempotent on id 156."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()
wave5 = c.execute("SELECT id FROM waves WHERE wave_number=5").fetchone()[0]

body = (
"LOCAL FAMILY-DIFFERENT VERIFIER stood up + validated on llama-swap (2026-06-03) — the EXTERNAL_VERIFIER that workflow-standards #6 + the study-swarm protocol + this KB's own 'verifier maturity (honest)' notes have wanted. "
"FIRST real consumer of wave-5's llama-swap. Generator = Claude (Anthropic); verifier = a LOCAL non-Claude model (Qwen / Mistral, Apache-2.0) served NATIVELY via llama-swap :9090. "
"Task = GROUNDED ENTAILMENT: given CLAIM + EVIDENCE only (the generator's reasoning is HIDDEN = the protocol's reasoning-stripped requirement), return constrained JSON {verdict: supported|refuted|insufficient, confidence, rationale}. Output grammar-constrained via llama.cpp json_schema response_format (GBNF under the hood -> also exercises the structured-output lane).\n\n"
"VALIDATED on a 14-case labeled set (5 supported / 5 refuted / 4 insufficient, incl. adversarial 'sounds-true-but-refuted' + 'don't-extrapolate' cases; verifier/claims.json). Per single model:\n"
"  qwen3-4b      (Qwen 4B dense):  13/14 = 92.9%, 0 false-confirms, 0.91 s/verdict\n"
"  qwen3-14b     (Qwen 14B dense): 13/14 = 92.9%, 0 false-confirms, 1.26 s/verdict\n"
"  qwen3-30b-a3b (Qwen MoE):       11/14 = 78.6%, 0 false-confirms, 0.60 s/verdict (over-conservative)\n"
"  mistral-nemo-12b (Mistral 12B): 13/14 = 92.9%, *** 1 FALSE-CONFIRM ***, 1.02 s/verdict\n\n"
"KEY FINDINGS (counterintuitive — the value of measuring rather than assuming):\n"
"1. SIZE DOESN'T HELP for grounded entailment: the dense 4B TIES the 14B and BEATS the 30B-A3B MoE (78.6%). Verification is a bounded task; a small DENSE model follows strict-grounding instructions better than a big reasoning-MoE. => the external-verifier role is CHEAP (2.5 GB, ~0.9 s/verdict, runs alongside other work / co-resident via llama-swap groups).\n"
"2. THE RIGHT METRIC IS FALSE-CONFIRM RATE, NOT ACCURACY. A false-confirm = stamping a non-supported claim 'supported' = letting bad output through (the exact failure an external verifier exists to prevent). Mistral-Nemo TIED on accuracy (92.9%) but produced 1 false-confirm (#6: it READ 'pip install unsloth downgraded torch to a CPU build' and STILL called the claim 'torch left untouched' supported). Every Qwen size held 0 false-confirms. => choose the verifier on false-confirm rate; raw accuracy hides the one dangerous error.\n"
"3. A 3-SEAT CONSERVATIVE-MAJORITY PANEL restores safety: panel says 'supported' ONLY if a strict majority of seats agree, else not-confirmed. The 3-seat 2-family panel (qwen3-4b + qwen3-14b + mistral-nemo-12b) = 92.9% with **0 false-confirms** — it CATCHES Nemo's #6 slip (2 Qwen refute, 1 Mistral confirms -> majority refutes). Empirically validates the workflow-standards 'multi-lens >= 3' EXTERNAL_VERIFIER design.\n\n"
"RECOMMENDED CONFIG:\n"
"- Quick/cheap: single qwen3-4b verifier (92.9%, 0 fc, 2.5 GB).\n"
"- Safety-critical: 3-seat conservative-majority panel mixing >= 2 families (e.g. qwen3-4b + qwen3-14b + a non-Qwen seat) — 0 fc, catches single-model false-confirms.\n"
"- ALL seats family-different from the Claude generator (decorrelation); evidence-only prompt (reasoning hidden); '/no_think' + json_schema grammar for clean fast JSON (Qwen3 is a thinking model — WITHOUT /no_think its <think> block exhausts the token cap before the JSON => empty content).\n\n"
"WIRING: served via llama-swap :9090 (wave-5 #152/#153); POST /v1/chat/completions with response_format json_schema. Reusable artifacts under tensor-engine-knowledge/verifier/: verify_local.py (verifier; argv = model [base] [think]), claims.json (labeled set), panel_analysis.py (panel), results-*.json (raw per-model). "
"CAVEAT: 14-case set is small => accuracy is INDICATIVE, not definitive; the false-confirm + panel findings are the load-bearing conclusions. NEXT: expand the labeled set; wire the panel as the family-different seat in roleos verify-citations / prism-verify; add a 3rd family (Phi/Granite/Gemma) for deeper decorrelation."
)
c.execute("DELETE FROM config_recipes WHERE id=156")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (156,?,?,?,?,?,?,?,?)""", (
  "llm-serving-local-family-different-verifier-on-llama-swap-validated",
  "Local family-different verifier on llama-swap (VALIDATED): grounded entailment, 0-false-confirm safety, small-dense-wins, 3-seat panel",
  2, 15, "recipe",
  "https://github.com/mostlygeek/llama-swap",
  body, wave5))
db.commit()
print("inserted #156; recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id",(wave5,)):
    print(" ", r[0], r[1], "|", r[2][:60])
db.close()
