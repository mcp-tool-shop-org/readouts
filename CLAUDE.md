# Standing rules for Claude sessions in readouts

Set by the maintainer on 2026-09-29. They apply to every session and every wave.

## Model verification: local only, no Ollama Cloud

- Do not spend on Ollama Cloud. Don't call cloud-routed Ollama models (`*-cloud` tags or ollama.com endpoints), and don't add them as a verifier lane.
- Verify with local models only, through the local Ollama daemon.
- When a check needs a stronger model than the local ones, stop and flag it. The maintainer runs those checks by hand on Grok or Gemini and brings back the results. Record where the verdict came from.
- Existing `verify_cloud.py` scripts and Ollama Cloud verdicts in earlier waves stay as the historical record. Don't re-run them.

## Subagents

- Run subagents on Sonnet 5.5 (`claude-sonnet-5-5`). `.claude/settings.json` sets `CLAUDE_CODE_SUBAGENT_MODEL` to it, and Agent calls should pass `model: "sonnet"` too.
