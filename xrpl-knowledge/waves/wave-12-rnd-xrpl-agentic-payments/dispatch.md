# Wave 12 — promoted from rnd: XRPL agentic payments (x402 exact scheme, AI Starter Kit, MPP SDK)

**KB** `xrpl-knowledge` · **dated** 2026-10-22 · **0** research agents (a promotion) · lanes `payments-advanced`, `infrastructure-tooling`, `client-libraries`

**Source entry:** rnd `2026-10-20-xrpl-agentic-payments-x402-the-ai-starter-kit-and-mpp`. Only its `[verified]` claims were used (read at
source by the Editor, 2026-10-20, and R&D's research agent, 2026-10-22). The KB held no row on x402, MCP/AI tools or MPP before this wave.

## What was promoted (3 new rows, all `verified=0`)

| Row | Category / kind | Network, maturity | What it records |
|---|---|---|---|
| `x402-exact-scheme-xrpl` | payments-advanced / standard | n/a, new | The `exact` scheme for XRPL in x402-foundation/x402 (Apache-2.0), added 2026-07-03: the payer signs an XRPL Payment, a facilitator submits it; it cannot sponsor fees. The x402 Foundation (Linux Foundation) was announced 2026-04-02 and operational 2026-07-14. |
| `xrpl-ai-starter-kit-mcp-skills` | infrastructure-tooling / service | n/a, new | Ripple's 2026-06-09 post (docs MCP server, two Claude skills in XRPLF/xrpl-dev-portal, two xrpl.org pages, x402 in XRP or RLUSD, t54 credited) and xrpl.org's AI-tools page now (Docs MCP at mcp.xrpledger.ai, xrpl.org MCP at xrpl.org/mcp, wallet/payments/trading skills). |
| `xrpl-mpp-sdk` | client-libraries / library | n/a, experimental | Ripple's xrpl-mpp-sdk (Apache-2.0, created 2026-08-14, 0.1.0-beta.4); MPP is Stripe and Tempo's protocol (announced 2026-03-18, specs CC0 1.0) and that announcement does not mention XRPL. |

All three are linked to the `track-payments` purpose. Sources: the x402 repo and both Linux Foundation releases; Ripple's post, xrpl.org's AI-tools page and
XRPLF/xrpl-dev-portal; the xrpl-mpp-sdk repo, Stripe's MPP post and tempoxyz/mpp-specs. Source `verified` is NULL (unchecked by a seat).

`network_status` is `n/a` on all three: they are off-ledger specs, services and libraries, not amendments or transaction types. `scripts/apply_promotion.py`
gained an idempotent `new_capabilities[]` path to insert these (no verifier call, no cloud seat).

## Left out, and why

- **Every adoption count**, including The Block's 2026-07-21 quote from RippleX (verified as a quote, but it names no counter or method), the 1M and
  13.9M figures, and "millions of agentic transactions". No source defines an agentic transaction, so the numbers are not decision-grade. Adoption figures stay out of the KB.
- **Every `[unverified]` claim** in the entry (the Foundation's 2026-07-08 announcement, the 13.9M hub count, the marketing guide's "millions").
- The entry's own reading of the claims (studio relevance, the xrpl-lab module idea, the "watch for" list) and t54's hosted facilitator: not among the verified claims, or not an XRPL capability fact.
- `xrpl.org/docs/agents/agentic-payments-x402`: listed in the entry but marked "not re-read", so not cited.

## Verification

Entry claims verified at source by the Editor (2026-10-20) and R&D's research agent (2026-10-22). No cloud seat, no second model family; the new rows' `verified` flag stays 0.

## Provenance

Promoted from rnd entry `2026-10-20-xrpl-agentic-payments-x402-the-ai-starter-kit-and-mpp`.
