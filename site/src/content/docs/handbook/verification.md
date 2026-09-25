---
title: Verification
description: How an entry earns the verified flag, what the flag promises, what it does not, and the checks that keep the corpus honest.
sidebar:
  order: 4
---

## How an entry earns `verified`

1. **Research, in waves.** A wave sends one research lane per domain. Each lane writes entries, and each entry cites its sources as `{url, claim}` pairs: the page, and the sentence the page is supposed to support.
2. **A separate verifier.** A second agent checks each entry against the pages it cites. It sees only the claims and the citations, never the researcher's reasoning, so it cannot be argued into agreeing. It returns a verdict per entry.
3. **One definition of `verified`.** [`shared/verdicts.py`](https://github.com/mcp-tool-shop-org/readouts/blob/main/shared/verdicts.py) sets `verified = 1` only when an external verdict confirms the entry. That verdict comes from the verifier block in the wave file or from a durable ledger (`verification/verdicts.json`). The author's own field never counts, and neither does a proxy such as "a licence string is present".
4. **The compiler, where there is code.** In rust-knowledge every code check is a complete Rust file with an expectation: it compiles, fails with a named error, or runs and prints an exact output. `rustc 1.98.1` runs every check. A recipe whose own example fails the compiler is never verified, whatever the verifier said.

Verdict scales differ between KBs, because each KB measures a different thing:

- **Currency scales** (godot-knowledge, blender-knowledge): solid, plausible, shaky, stale or wrong. Only `solid` confirms; `plausible` is, by construction, not a confirmation.
- **Retrieval verdicts** (rust-knowledge, vocology-knowledge and others): confirmed, corrected, refuted or unfindable. `corrected` confirms the entry as corrected, and the correction is kept in its record.
- **Cloud verifiers** (some waves in blender-knowledge, sprite-motion-knowledge and xrpl-knowledge): a verifier run on a model outside the researcher's family, sometimes several at once. With several, a majority must confirm and none may refute, so one credible refutation blocks the entry.

## What `verified` promises, and what it does not

It promises that a verifier other than the author opened the cited pages and found that they support the claim, as of the wave's date.

It does not promise:

- **Independence of model family.** In most waves the verifier comes from the same model family as the researcher. The live page is the decorrelating check. Some waves add a seat from a different family; rust-knowledge's fourth wave was written by other families and verified by Claude. Each wave's `verifier_note` says which.
- **That the fact is still current.** Tools move. A verdict is a snapshot at the wave's date, which the catalog pages show.
- **That the advice suits you.** Many KBs were measured on one workstation with one 32 GB NVIDIA GPU under Windows, and say so.
- **Legal clearance.** A licence note is a research note, not legal advice.

An unverified entry is not a wrong one. It is a lead that nobody has confirmed yet.

## Corrections and annotations

When the verifier corrects an entry, the correction is what gets loaded, and the wave's `verification.md` lists what changed. rust-knowledge also keeps operator notes (`verification/operator-notes.json`). A note annotates a verdict and never changes it. It records a pipeline defect the verifier could not have seen, the commit a citation was checked against, or a later measurement that narrows a verified claim.

## The floor: verify.py

`python verify.py` checks that the generated files are true about the databases. It runs on every push that changes the corpus.

| Check | Level | What it proves |
|---|---|---|
| no shadow DB | FAIL | No empty `.db` file sits beside a real one. An empty one once zeroed a whole KB on the front door. |
| sqlite integrity | FAIL | Every database passes `integrity_check` and `foreign_key_check`. |
| FTS rowid alignment | FAIL | Every full-text rowid joins to its own entry, checked by slug, not by count. |
| verified implies a source | FAIL | No verified entry lacks a source. |
| verified is external | FAIL | The database's verified count equals what `shared/verdicts.py` derives from the external verdicts. |
| meta.latest_wave current | FAIL | Each database's recorded latest wave matches its waves table. |
| front door matches DBs | FAIL | `index.json` reports the counts the databases actually hold. |
| README table current | FAIL | The README's table matches `index.json`. |
| no dead relative links | FAIL | Every relative markdown link resolves. |
| source flag is independent | WARN | Whether each source's own `verified` flag was checked separately, or copied from its entry. |
| every entry has a source | WARN | A few entries have no source rows. They are known, recorded, and never verified. |
| no collision-forked slugs | WARN | Colliding slugs were suffixed `-2` on load. They are known pairs to review before re-ingesting a wave. |

The warnings are real, known defects. They do not block, and `--strict` turns them into failures. Every failure and warning prints a stable code and a hint, listed in the [Reference](../reference/).

## Why the checks look like this

Each one exists because the corpus once failed that way, silently:

- Every loader once built its full-text index without the entry ids. In three KBs search-then-join returned nothing. In a fourth, deleted rows shifted the index, and dozens of searches returned a confident answer about a different engine. Row counts matched the whole time, so count parity never caught it.
- In five KBs, `verified` once meant something weaker than a verdict: the research agent's own field, a `plausible` rating, or the mere presence of a licence string. The count went down when the definition was fixed, because a lower number that means something beats a higher one that does not.
- A README table that claimed to mirror a generated file was maintained by hand, and drifted.
