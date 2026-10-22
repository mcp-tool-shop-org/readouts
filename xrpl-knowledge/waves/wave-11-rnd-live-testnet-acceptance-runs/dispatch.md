# Wave 11 — promoted from rnd: live testnet acceptance runs (xrpl-lab 2.6.0 AMM)

**KB** `xrpl-knowledge` · **dated** 2026-10-22 · **0** research agents (a promotion) · lanes `dex-amm`, `client-libraries`

**Source entry:** rnd `2026-10-20-live-testnet-runs-surface-defects-in-layers-each-fix-exposed` (all 5 claims `[verified]` by R&D
against xrpl-lab's receipts: `docs/receipts/2.6.0-amm-live-fire`, PR #19, issue #20).

## What was promoted (no new rows; gotchas appended to 4 existing rows)

| Row | Gotcha |
|---|---|
| `ammcreate` | Fee = owner reserve increment; a pool funded from one 100 XRP faucet grant fails `tecUNFUNDED_AMM` (about 98.6 XRP spendable); 25/25 works |
| `ammwithdraw` | After the sole LP's `tfWithdrawAll` the AMM is deleted; `amm_info` returns `actNotFound` |
| `xrpl-py` | `submit_and_wait` waits on a held result until `LastLedgerSequence` passes (about 80 s); a shorter client timeout loses the hash; sign first |
| `faucet-test-network-helpers` | A faucet reply is not proof of funding; wait for the validated balance (an unvalidated AccountSet led to `terNO_RIPPLE` / `terNO_AMM`) |

Sources (kind `repo`): the receipts folder on all four rows, for the outcomes; PR #19 on ammcreate, xrpl-py and the faucet row, for the code fixes it made (not the outcomes); issue #20 on the faucet row.

## Left out, and why

- The run-by-run narrative (what each of the four runs hid) and the studio lessons (budget several live acceptance runs; make the
  product's status honest first): process advice, not XRPL capability facts. They stay in the rnd entry.
- Run 4 and the 2.6.0 release facts: no capability row to attach them to.
- Anything not among the entry's five verified claims.

## Verification

Rig receipts read by R&D, 2026-10-20. No cloud seat, no second model family. The `verified` flags on the touched rows are unchanged.

## Provenance

Promoted from rnd entry `2026-10-20-live-testnet-runs-surface-defects-in-layers-each-fix-exposed`.
