#!/usr/bin/env python3
"""Write S6.3 measured results into training.db — the write-back that closes the S6 loop.

Measurements land here → flow to curriculum.json (gen_curriculum.py) → role-os flips `unverified`
prerequisite edges to `confirmed` and fills the recipe preview (`roleos crew --programs` / `--preview`).
Idempotent (re-runnable; upserts edges, updates technique preview fields). Two payloads:

  - EDGE transfer delta: the measured cheaper-after-foundation saving for a (predecessor, successor)
    prerequisite — the thing that makes an edge `confirmed` (findings 15,16).
  - TECHNIQUE preview fit: the mixing-law fit + calibration scale + replay/forgetting + task fingerprints
    that the recipe preview surfaces (findings 6,9,10,11,19,21).

Contract: role-os/design/specialist-training-programs.md (study-swarm wf_9b6208e9-b97).

measurement.json shape:
{
  "wave": <N>, "date": "YYYY-MM-DD",            # provenance (optional; tags the rows to a wave)
  "edges": [
    {"predecessor": "<slug>", "successor": "<slug>",
     "per_seed_steps_saved_frac": [0.31, 0.28, 0.35],   # REQUIRED for a verified delta — the RAW per-seed values
     "magnitude_floor": 0.20,                            # preregistered noise floor; |median| must clear it
     "edge_kind": "cheaper|prerequisite-required", "validated_as": "sequence|merge",
     "witness_score": 0.9, "witness_signals": {...}, "note": "..."}
    # VERDICT is COMPUTED here, never trusted: steps_saved_frac=median is written ONLY when
    #   len(per_seed) >= 3 AND all deltas agree in sign AND |median| >= magnitude_floor; else NULL (unverified).
    #   A consistent all-<=0 result is a real `confirmed-negative` (warm-start measured NOT to help).
  ],
  "techniques": [
    {"slug": "<slug>", "mixing_law": {"tier": "law-predicted", "predicted_loss": 1.2,
       "predicted_steps_to_cert": 600, "coefficients": {...}},
     "calibration_params": 4000000000, "calibration_tokens": 100000000,
     "replay_fraction": 0.01, "measured_forgetting": 0.05,
     "difficulty_signal": "exam-flip-consistency", "task_embedding_ref": "...", "task_vector_ref": "..."}
  ]
}

Run (UTF-8 on Windows):  $env:PYTHONUTF8='1'; python scripts/record_measurement.py <measurement.json>
"""
import json
import os
import sqlite3
import statistics
import sys

from migrate_s6 import migrate_s6  # ensure the S6 schema exists before writing

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.environ.get("TRAINING_DB") or os.path.join(ROOT, "training.db")

# Mirror role-os MIN_OUTCOME_RECEIPTS: a consistent-sign directional claim needs n>=3 (at n=2 the null
# sign-agreement rate is a coin flip). The producer is the gatekeeper; the consumer (role-os) re-checks.
MIN_OUTCOME_RECEIPTS = 3


def _edge_verdict(e):
    """Compute the honest edge verdict from the RAW per-seed deltas — never a hand-authored scalar.
    Returns (steps_saved_frac_or_None, n_receipts, consistent_sign_0_1_or_None, reason).
    A non-NULL steps_saved_frac (the median) is returned ONLY when n>=MIN_OUTCOME_RECEIPTS receipts agree
    in sign AND |median| clears the preregistered magnitude floor; otherwise None (the edge stays unverified)."""
    per_seed = e.get("per_seed_steps_saved_frac")
    if not isinstance(per_seed, list) or not per_seed:
        return None, int(e.get("n_receipts", 0) or 0), None, \
            "no per_seed_steps_saved_frac (required for a verified delta)"
    deltas = [float(x) for x in per_seed]
    n = len(deltas)
    consistent = all(d > 0 for d in deltas) or all(d <= 0 for d in deltas)
    median = statistics.median(deltas)
    floor = e.get("magnitude_floor")
    reasons = []
    if n < MIN_OUTCOME_RECEIPTS:
        reasons.append(f"n={n} < {MIN_OUTCOME_RECEIPTS}")
    if not consistent:
        reasons.append("mixed-sign per-seed deltas (transfer-neutral)")
    if floor is None:
        reasons.append("no magnitude_floor (preregister the noise floor)")
    elif abs(median) < float(floor):
        reasons.append(f"|median|={abs(median):.3f} < magnitude_floor={float(floor):.3f}")
    passes = not reasons
    return (round(median, 4) if passes else None), n, (1 if consistent else 0), \
        ("OK" if passes else "; ".join(reasons))


def _tid(cur, slug):
    r = cur.execute("SELECT id FROM techniques WHERE slug=?", (slug,)).fetchone()
    return r[0] if r else None


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        m = json.load(f)

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    migrate_s6(con)
    cur = con.cursor()

    wave_id = None
    if m.get("wave") is not None:
        r = cur.execute("SELECT id FROM waves WHERE wave_number=?", (int(m["wave"]),)).fetchone()
        wave_id = r[0] if r else None

    n_edges = n_tech = 0
    unresolved = []
    edge_reports = []

    for e in m.get("edges", []):
        pid, sid = _tid(cur, e.get("predecessor")), _tid(cur, e.get("successor"))
        if pid is None or sid is None:
            unresolved.append(("edge", e.get("predecessor"), e.get("successor")))
            continue
        ssf, n, cs, reason = _edge_verdict(e)
        verdict = "unverified" if ssf is None else ("confirmed-negative" if ssf <= 0 else "confirmed")
        per_seed_json = json.dumps(e["per_seed_steps_saved_frac"]) \
            if isinstance(e.get("per_seed_steps_saved_frac"), list) else None
        note_full = ((e.get("note") or "").strip()
                     + f" · S6.3 verdict={verdict} (n={n}; {reason})").strip()
        cur.execute(
            """INSERT INTO technique_edges
                 (predecessor_id, successor_id, witness_score, witness_signals, steps_saved_frac,
                  outcome_n_receipts, consistent_sign, per_seed_deltas, edge_kind, validated_as,
                  verifier_note, wave_id)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(predecessor_id, successor_id) DO UPDATE SET
                 witness_score=excluded.witness_score, witness_signals=excluded.witness_signals,
                 steps_saved_frac=excluded.steps_saved_frac, outcome_n_receipts=excluded.outcome_n_receipts,
                 consistent_sign=excluded.consistent_sign, per_seed_deltas=excluded.per_seed_deltas,
                 edge_kind=excluded.edge_kind, validated_as=excluded.validated_as,
                 verifier_note=excluded.verifier_note, wave_id=excluded.wave_id""",
            (pid, sid, e.get("witness_score"),
             json.dumps(e["witness_signals"]) if e.get("witness_signals") else None,
             ssf, n, cs, per_seed_json, e.get("edge_kind"),
             e.get("validated_as"), note_full, wave_id))
        n_edges += 1
        edge_reports.append(f"  {e.get('predecessor')} -> {e.get('successor')}: {verdict} (n={n}; {reason})")

    for t in m.get("techniques", []):
        tid = _tid(cur, t.get("slug"))
        if tid is None:
            unresolved.append(("technique", t.get("slug"), None))
            continue
        # COALESCE on the fingerprint/signal fields so a partial measurement doesn't wipe prior values.
        cur.execute(
            """UPDATE techniques SET
                 mixing_law_coefficients=?, calibration_params=?, calibration_tokens=?,
                 replay_fraction=?, measured_forgetting=?,
                 difficulty_signal=COALESCE(?, difficulty_signal),
                 task_embedding_ref=COALESCE(?, task_embedding_ref),
                 task_vector_ref=COALESCE(?, task_vector_ref)
               WHERE id=?""",
            (json.dumps(t["mixing_law"]) if t.get("mixing_law") else None,
             t.get("calibration_params"), t.get("calibration_tokens"), t.get("replay_fraction"),
             t.get("measured_forgetting"), t.get("difficulty_signal"),
             t.get("task_embedding_ref"), t.get("task_vector_ref"), tid))
        n_tech += 1

    con.commit()
    con.close()
    print(f"recorded {n_edges} edge delta(s), {n_tech} technique preview fit(s).")
    for r in edge_reports:
        print(r)
    if unresolved:
        print("  WARNING unresolved slugs (skipped — fix the slug or load the technique first):")
        for kind, a, bb in unresolved:
            print(f"    {kind}: {a}{(' -> ' + bb) if bb else ''}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: record_measurement.py <measurement.json>")
    main(sys.argv[1])
