# Scorecard

> Score a repo before remediation. Fill this out first, then use SHIP_GATE.md to fix.

**Repo:** mcp-tool-shop-org/readouts
**Date:** 2026-09-25 (assessed at `1adb487`, the 2026-09-14 publication)
**Type tags:** `[all]` (data corpus with maintenance scripts and a static site)

## Pre-Remediation Assessment

| Category | Score | Notes |
|----------|-------|-------|
| A. Security | 3/10 | No SECURITY.md and no threat model. A home-directory path had been public in two logs since 2026-09-10, and two third-party email addresses since 2026-09-14. |
| B. Error Handling | 5/10 | `verify.py` separated FAIL from WARN, but gave no codes or hints, and a crashing check exited 1 instead of the documented 2. |
| C. Operator Docs | 5/10 | The README's hand-maintained table was stale, routing examples named a deprecated package, and there was no CHANGELOG. |
| D. Shipping Hygiene | 4/10 | `verify.py` existed, but nothing ran it in CI, and no dependency scanning ran. |
| E. Identity (soft) | 1/10 | No logo, translations, landing page or topics. The description was stale. |
| **Overall** | **18/50** | |

## Key Gaps

1. Exposed personal data on a public repo, missed by a scanner whose pattern allowed only one separator.
2. No security policy and no threat model for readers or for the research tooling.
3. No CI: the corpus's floor ran only when someone remembered.
4. A README written for the studio rather than for readers, with a table maintained by hand.
5. No landing page, handbook or translations.

## Remediation Priority

| Priority | Item | Estimated effort |
|----------|------|-----------------|
| 1 | Scrub the exposed data; add a home-path gate that covers every spelling; redact recorded compiler output | 1 hour |
| 2 | SECURITY.md, threat model, codes and hints in `verify.py`, CI | 1 hour |
| 3 | README, landing page, handbook, translations, metadata | 3 hours |

## Post-Remediation

| Category | Before | After |
|----------|--------|-------|
| A. Security | 3/10 | 9/10 |
| B. Error Handling | 5/10 | 9/10 |
| C. Operator Docs | 5/10 | 10/10 |
| D. Shipping Hygiene | 4/10 | 10/10 |
| E. Identity (soft) | 1/10 | 10/10 |
| **Overall** | 18/50 | 48/50 |

Re-scored 2026-09-25 after the history rewrite and with Dependabot alerts on; `shipcheck audit` passes every item.

Not yet 50:

- **Security (9).** The rewrite took the exposed data off every ref: `main` is a single commit, and there is no other branch, tag or pull ref. GitHub still serves the two pre-rewrite commits to anyone holding their SHA, until it garbage-collects them. Asking GitHub Support to purge them is the owner's step.
- **Error handling (9).** `verify.py` reports a code and a hint for every finding. The loaders and generators still end in a raw traceback on bad input; a missing wave file, for one, raises `FileNotFoundError`.
