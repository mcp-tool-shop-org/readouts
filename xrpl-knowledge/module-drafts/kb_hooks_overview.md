---
id: kb_hooks_overview
title: "Hooks (WASM smart-contract layer)"
track: programmability
summary: "Hooks are small, efficient WebAssembly modules attached to a Xahau account that execute BEFORE and/or AFTER…"
time: 15-20 min
level: beginner
mode: testnet
requires: []
produces:
  - txid
  - report
checks:
  - "Understood: Hooks (WASM smart-contract layer)"
  - "Concept performed on testnet (txid produced)"
  - "Verified the key fields: ['WebAssembly (WASM) modules', 'hook() entrypoint + cbak() callback', 'weak vs…"
  - "Avoided the gotcha: ['Hooks live ONLY on Xahau, never on XRPL mainnet — a common misconception is…"
---
<!-- DRAFT auto-seeded from xrpl-knowledge capability `hooks-overview` (Programmability — Hooks (Xahau), mainnet-live, verified) · amendment `Hooks`.
     Edit forward: write the prose, wire the core action, set requires/checks. -->

Hooks are small, efficient WebAssembly modules attached to a Xahau account that execute BEFORE and/or AFTER transactions affect that account, letting the account accept, reject, or augment activity with custom logic. They are intentionally NOT Turing-complete — arbitrary unbounded loops are forbidden — which keeps worst-case execution predictable and priceable. Hooks are the native smart-contract…

## Step 1: Ensure your wallet is ready

You need a funded wallet. If you completed an earlier module it loads automatically.

<!-- action: ensure_wallet -->

## Step 2: Hooks (WASM smart-contract layer)

**Key fields / API to know:** ["WebAssembly (WASM) modules", "hook() entrypoint + cbak() callback", "weak vs strong execution", "hook chain (up to 4 strong hooks per account, sender + receiver)", "before/after transaction firing", "not Turing-complete by design", "guarded loops only"]

<!-- TODO: wire the core action for this module. The KB describes WHAT happens; pick the
     matching xrpl-lab action (see `xrpl-lab lint` for the registered action schema), e.g.:
       <!-- action: ensure_funded -->
       <!-- action: submit_payment destination=ADDRESS amount=10 -->
       <!-- action: set_trust_line currency=LAB limit=1000 -->
     Until wired, this module is dry-run/teaching-only. -->

## Step 3: Verify on-ledger

Inspect what happened on the explorer — turn the result into evidence you can read.

## Checkpoint: What you proved

You now understand **Hooks (WASM smart-contract layer)**.

**Watch out:** ["Hooks live ONLY on Xahau, never on XRPL mainnet — a common misconception is that XRPL gained smart contracts; it did not.", "A hook is account-scoped, not a global contract — there is no shared global address space like EVM; logic is bound to the account it is installed on.", "Execution is bounded and metered; you cannot run open-ended computation."]

**Learn more (verified sources):**
- [Hooks | Xahau Network (features/network-features/hooks)](https://xahau.network/docs/features/network-features/hooks/) — Hooks are small, efficient WebAssembly modules designed specifically for the XRPL that…
- [XRP Ledger Sidechain Xahau Now Live in Mainnet — U.Today](https://u.today/xrp-ledger-sidechain-xahau-now-live-in-mainnet) — The Hooks-enabled Xahau network launched its mainnet on October 31, 2023.

Run `xrpl-lab proof-pack` when you're ready to export your work.
