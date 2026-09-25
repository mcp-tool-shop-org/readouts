#!/usr/bin/env python3
"""One definition of `verified`, shared by every KB's loader.

THE PROBLEM THIS SOLVES. `verified` meant a different thing in every KB, and in
four of them it meant nothing at all:

  sprites, sprite-motion  `verified = b(item["verified"])` — the RESEARCH AGENT'S
                          OWN field. No verifier consulted. 162 of 193 and 178 of
                          224 entries were flagged this way. sprite-motion is the
                          sharper case: its wave files carry a `cloud_verify` block
                          with three jurors, and the loader never opened it.
  godot, blender          `VERIFIED_VERDICTS = {"solid", "plausible"}`, where
                          "plausible" is by construction a NON-confirmation, plus an
                          `else b(item["verified"])` fallback that is pass-on-faith.
  training (datasets)     `verified = 1 if d.get("license") else 0` — verified for
                          having a licence STRING, checked by nobody.

A flag that a generator can set about its own output is not verification; it is a
restatement. Panickssery et al. (NeurIPS 2024) is the general form of the problem,
and this repo measured it: source-level "verification" correlated 100.0% with the
parent entity's own verdict across 934 rows in two KBs — a copy, not a check.

THE CONTRACT, and it is the same everywhere now:

  verified = 1  iff an EXTERNAL verdict says so — a verifier block in the wave
                file, or a durable verdict ledger. Never the author's self-report,
                never a proxy like "a licence string is present".
  verified = 0  whenever no external verdict exists. Absence of checking is not
                a pass, and it is not an error either: it is `directional`.

Two verdict sources, checked in order:

  1. `verification/verdicts.json` — the durable ledger (the vocology pattern).
     Keyed by entry slug. Survives a rebuild, which a DB write does not.
  2. The wave file's own verifier block — `cloud_verify` or `verify`, single-juror
     or multi-juror. Keyed by entry name.

Multi-juror aggregation is deliberately adversarial: a MAJORITY must confirm and
NO juror may refute. One credible refutation blocks, because the whole point of
seating three jurors is that any of them can stop a claim.
"""
from __future__ import annotations

import json
import os
import re

# Verdict vocabularies, lowercased. Anything unrecognised counts as no-confirmation.
CONFIRMING = {"confirmed", "confirmed-with-fixes", "corrected", "supported", "solid"}
REFUTING = {"refuted", "wrong", "not-supported", "not_supported", "avoid", "false"}
# Explicitly NOT confirming, and named so a reader can see the decision:
#   "plausible"  — the adversarial verdict for "could not falsify", not "checked out"
#   "unverified" — the juror could not reach it
#   "shaky", "*_stale" — flagged, not confirmed

NAME_KEYS = ("recipe", "capability", "model", "engine", "technique", "finding",
             "entry", "item", "name")
ITEM_LISTS = ("recipes", "findings", "models", "engines", "techniques",
              "capabilities", "entries")


def norm(s: str) -> str:
    """Match verdicts to entries by name, tolerating punctuation and case drift."""
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def lane_items(lane: dict) -> list[dict]:
    """A lane's entries, whichever shape the KB uses.

    Five KBs nest them under `lane["research"][<entity>]`; the rest put the list
    directly on the lane. A resolver that knows only one shape silently returns
    zero entries for half the corpus.
    """
    for key in ITEM_LISTS:
        if isinstance(lane.get(key), list):
            return [i for i in lane[key] if isinstance(i, dict)]
    research = lane.get("research")
    if isinstance(research, dict):
        for key in ITEM_LISTS:
            if isinstance(research.get(key), list):
                return [i for i in research[key] if isinstance(i, dict)]
    return []


def lane_verdicts(lane: dict) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """(by_name, by_slug) — every external verdict in a lane.

    Handles both block names and both juror shapes: `{verdicts: [...]}` (one seat)
    and `{jurors: {model: [...]}}` (several). It also has to handle both KEYS: most
    KBs identify the entry a verdict is about by name, training-knowledge does it by
    slug, and a resolver that knows only one silently matches nothing for the other.
    """
    by_name: dict[str, list[str]] = {}
    by_slug: dict[str, list[str]] = {}
    for block_key in ("cloud_verify", "verify"):
        block = lane.get(block_key)
        if not isinstance(block, dict):
            continue
        groups: list[list] = []
        if isinstance(block.get("verdicts"), list):
            groups.append(block["verdicts"])
        jurors = block.get("jurors")
        if isinstance(jurors, dict):
            groups.extend(v for v in jurors.values() if isinstance(v, list))
        for group in groups:
            for v in group:
                if not isinstance(v, dict):
                    continue
                overall = str(v.get("overall") or v.get("verdict") or "").strip().lower()
                if v.get("slug"):
                    by_slug.setdefault(str(v["slug"]).strip().lower(), []).append(overall)
                name = next((v[k] for k in NAME_KEYS if v.get(k)), None)
                if name:
                    by_name.setdefault(norm(str(name)), []).append(overall)
    return by_name, by_slug


def adjudicate(overalls: list[str]) -> tuple[int, str, str]:
    """(verified, status, note) from one or more jurors' verdicts.

    Majority must confirm and none may refute. Seating three jurors is pointless
    if a single refutation does not stop the claim.
    """
    if not overalls:
        return 0, "directional", "no external verdict — not checked"
    seats = len(overalls)
    confirms = sum(1 for o in overalls if o in CONFIRMING)
    refutes = sum(1 for o in overalls if o in REFUTING)
    tally = ", ".join(sorted(set(o or "(blank)" for o in overalls)))
    if refutes:
        return 0, "avoid", f"refuted by {refutes} of {seats} juror(s) [{tally}]"
    if confirms * 2 > seats:
        return 1, "recommended", f"confirmed by {confirms} of {seats} juror(s) [{tally}]"
    return 0, "directional", f"only {confirms} of {seats} juror(s) confirmed [{tally}]"


class Verdicts:
    """Resolver for one KB. Ledger first, then the wave file's verifier block."""

    def __init__(self, kb_root: str):
        self.ledger: dict[str, dict] = {}
        path = os.path.join(kb_root, "verification", "verdicts.json")
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                self.ledger = json.load(fh).get("verdicts", {})
        self._by_name: dict[str, list[str]] = {}
        self._by_slug: dict[str, list[str]] = {}

    def use_lane(self, lane: dict) -> None:
        self._by_name, self._by_slug = lane_verdicts(lane)

    def for_entry(self, slug: str, name: str) -> tuple[int, str, str, dict]:
        """(verified, status, note, corrections) — the loader writes these verbatim."""
        led = self.ledger.get(slug)
        if led:
            return (int(led.get("verified", 0)),
                    led.get("status") or "directional",
                    led.get("verify_note") or led.get("verdict") or "ledger verdict",
                    led.get("corrections") or {})
        overalls = (self._by_slug.get((slug or "").strip().lower())
                    or self._by_name.get(norm(name)) or [])
        verified, status, note = adjudicate(overalls)
        return verified, status, note, {}

    def covered(self) -> int:
        return len(self._by_name) + len(self._by_slug)
