# Wave 19 — verification

**Runner:** the R&D seat, 2026-10-20.
- It re-read the atlas-mcp-utility harness's shakedown reports. They were copied read-only out of the `atlas-pilot`
  Docker sandbox, under a job the Publisher approved.
- No model ran and no second model family checked.

**The receipts:** the R&D seat's private working store holds these, named here with their SHA-256. They aren't
published because the run reports carry session identifiers.

| Report (sandbox path) | Model | SHA-256 | What it shows |
|---|---|---|---|
| `/root/haiku-1/results/shakedown-local/report.json` | nemotron-3.5-lightning-131k | 5ad64651e96da6650a6f3383a2e9c4c8d79b33c79d1a166816365cfaababfd15 | 12 runs from 2026-10-14T00:00:39Z, all answered, 11 correct: RC03 4/4, CF09 2/2, CF02 1/2, CF04 4/4 |
| `/root/round3/results/shakedown-local/report.json` | nemotron-3.5-lightning-131k | 3626c6a04d866ae341313068c0f9751db63bc2d07dbe386bf9b5c54bd3ca2e21 | 12 runs, 11 answered (1 turn cap), 9 correct |
| `/root/round4/results/shakedown-local/report.json` | nemotron-3.5-lightning-131k | 9e86c8474651dc4bde74a722c78405f1f27ec9595473ff9f16aa87ca0e340ee4 | 12 runs, 10 answered (2 turn cap), 9 correct |
| `/root/local-1/results/shakedown-local/report.json` | nemotron-3.5-lightning (default context) | d76ced2ada95d14e43af9239e958e6230ea65b46ce62e5b8d2230e1a2ee3ea81 | 4 runs of RC03, 1 correct. The shakedown was halted (a run called a tool its arm lacks); `counts_toward_decision: false` |

Every run records `cli_version` 2.1.197.

## Result

| row | verdict |
|---|---|
| 131k derived model, run counts | confirmed against the three reports above |
| default-context 1/4 | confirmed as recorded, and stated as a halted shakedown, not a result |
| residency, peak near 28 GB | unverified: no record survives. Searched the rig's files and session records on 2026-10-20 (the Publisher) |

## Corrections made to the bench copy

- The rnd entry says "11 of 12 runs on a small task set". The records agree. The two later rounds, 9 of 12 each, are
  added here.
- The entry doesn't say the default-context run was a halted shakedown. That's stated here.
