"""Wave-5 #158 — the shipped `offload` local CLI. Idempotent on id 158."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()
wave5 = c.execute("SELECT id FROM waves WHERE wave_number=5").fetchone()[0]

body = (
"SHIPPED: `offload` — a single-file stdlib-only CLI that delegates BOUNDED tasks to local models (via llama-swap) to cut Claude token usage (ollama-intern philosophy, distilled). "
"Location: E:\\AI-Models\\studio-local\\offload.py (+ README.md). Talks to llama-swap at $LLAMASWAP_BASE (default :9090). Defaults are the wave-5-validated configs (#156/#157). Smoke-tested live 2026-06-03.\n\n"
"COMMANDS:\n"
"  offload verify --claim X --evidence Y [--panel] [--model qwen3-4b] [--json]  -> grounded entailment: supported|refuted|insufficient. "
"Evidence-only, grammar-constrained JSON. Default qwen3-4b (cheapest 0-false-confirm verifier; #156). --panel = 3-seat conservative majority over >=2 families (qwen3-4b+qwen3-14b+mistral-nemo-12b) — catches a single model's false-confirm. SMOKE: true->SUPPORTED, false->REFUTED, panel aggregates 3 seats. OK.\n"
"  offload compress --words N [--file f] [--json] [--quiet]  -> shrink text to a WORD budget (models hit word targets, not token targets; #157) + hard max_tokens backstop. Summary on stdout (pipeable), reduction stats on stderr. Default qwen3-4b. SMOKE: an 838-token recipe -> 70 tokens (91.6% smaller), faithful digest. OK.\n\n"
"This is the 'ship the prompting recipe' outcome of the wave-5 token-economy work (user chose ship-over-train, the measure-first data showing word-budget prompting + hard cap on a 4B is sufficient). A budget-adherence LoRA (Unsloth #155) remains the deferred option for sub-4B economizers. "
"USE IT: pre-digest large logs/docs/DB-dumps through `offload compress` before handing to Claude; route citation/claim checks through `offload verify --panel` as the family-different EXTERNAL_VERIFIER seat. Prereq: llama-swap running with the wave-5 config."
)
c.execute("DELETE FROM config_recipes WHERE id=158")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (158,?,?,?,?,?,?,?,?)""", (
  "tool-offload-local-verify-compress-cut-claude-tokens",
  "offload CLI (SHIPPED): local verify + compress via llama-swap to cut Claude tokens — validated defaults, smoke-tested",
  2, 15, "tool",
  "file:///E:/AI-Models/studio-local/offload.py",
  body, wave5))
db.commit()
print("inserted #158; recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id",(wave5,)):
    print(" ", r[0], r[1], "|", r[2][:58])
db.close()
