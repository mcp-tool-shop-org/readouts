# Verification sweep — 2026-09-09

A retrieval sweep over **all 147 findings that no verifier had ever reached**, run as
six parallel adversarial lanes. This is not a wave: it adds no findings. It settles
the `verified` flag on findings waves 1–7 already carried.

## Why it was needed

`verified` came from `ACCEPT_IDS` — nine citation IDs hardcoded in `load_db.py` from
wave-01's abstract-NLI pass. Every other finding defaulted to
`verified=0, status=directional, "existence may be gated; claim not abstract-NLI-supported"`.
So the KB read **12/159 verified**, which understated it badly: the findings were not
wrong, they were *unchecked*. 8% is not a quality signal, it is an absence of one.

## Result

| | |
|---|---|
| findings swept | 147 |
| confirmed | 106 |
| corrected | 38 |
| refuted | 1 |
| unfindable | 2 |
| **outright fabrications** | **0** |

**12/159 → 153/159 verified** (144 from the sweep, plus the 9 wave-01 accepts the
sweep did not cover). Every citation resolved to a real artifact — including every
forward-dated identifier, which each lane was told to attack first as the usual
fabrication tell.

## What the corrections were actually about

Almost none were invention. Three patterns account for nearly all 38:

**Scope-stripping — a real number quoted without the qualifier that gives it meaning.**
CREPE's 0.967/0.909 holds only on MDB-stem-synth (on RWC-synth it is 0.999/0.995);
AST's 0.485 mAP is the Ensemble-M config, not a single model; a chirp-group-delay F1
of 0.88 was measured on guitar and piano with **zero vocal material** and then routed
to "the singing route".

**Compound claims where a verified half carries an unchecked half across an "and".**
A library is correctly described as MIT with MFCC and chroma, *and* said to lack raw
mel bands — but `melBands` ships in the package. A paper's beat-grid rationale holds,
*and* it is credited with saying something about singing voice that it never mentions.

**Attribution.** Eight entries credited a hosting organisation or journal where a named
person is the author; two named the wrong people entirely.

One claim was **refuted**: the load-bearing half of a progressive-disclosure entry is
not in the cited source, and the slug 404s. Two are **unfindable** — Khronos GLSL pages
that return 403 to every route including the archive.

## Provenance

- `lanes/<bucket>.input.json` — the findings each lane was given
- `lanes/<bucket>.json` — its verdicts, one per input slug, with evidence URLs
- `../verdicts.json` — the merged ledger, **read by `load_db.py`**, so a rebuild
  reproduces this state instead of reverting to the ACCEPT_IDS default

Regenerate the ledger after a future sweep:

```bash
python scripts/merge_verdicts.py 'verification/sweep-*/lanes/*.json'
```

## Two things a reader should carry forward

**The verifier is separate from the author, and it caught things.** 38 corrections and
one refutation out of 147 is a ~26% touch rate on material that had been sitting in a
knowledge base presented as findings. Any KB whose `verified` column is mostly zeros is
making a claim about its process, not about its content.

**Contested pedagogy is recorded as contested.** Two register entries cite an
organisation whose own published position argues the opposite of the claim. They are
kept, with the dispute written into `verify_note`, rather than silently resolved in
either direction.
