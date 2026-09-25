#!/usr/bin/env python3
"""Export the curriculum graph (roleos-curriculum/v1) from training.db for role-os S6.

role-os reads this PUBLISHED JSON, never the .db — the Parnas seam (like engine_recipe_ref): the KB
owns its schema and exports raw SIGNALS; role-os COMPUTES the prerequisite graph (witness, DAG,
recipe previews). See role-os/design/specialist-training-programs.md (study-swarm wf_9b6208e9-b97)
and role-os src/specialist/training-programs.mjs.

Emits ACTIVE techniques (status not superseded/avoid) + explicit prerequisite edges (from
predecessor_technique_id) with the corroborating signals role-os fuses into a directional witness
(stage_chain, shared_datasets, shared_sources), plus any MEASURED outcome delta from technique_edges
(empty until S6.3, so role-os classifies every edge `unverified` for now — honest by construction).

Run (UTF-8 forced on Windows):
    $env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; python scripts/gen_curriculum.py [out.json]
Default out: <root>/curriculum.json
"""
import datetime
import json
import os
import sqlite3
import sys

from migrate_s6 import migrate_s6  # ensure technique_edges + S6 columns exist before reading

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.environ.get("TRAINING_DB") or os.path.join(ROOT, "training.db")


def main(out):
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    migrate_s6(con)  # idempotent
    cur = con.cursor()

    active = "(status IS NULL OR status NOT IN ('superseded', 'avoid'))"
    techs, ids = [], set()
    for r in cur.execute(
        f"""SELECT id, slug, name, applicable_to, evidence_strength, engine_recipe_ref,
                   rig_fit, studio_fit, status,
                   difficulty_signal, mixing_law_coefficients, calibration_params, calibration_tokens,
                   replay_fraction, measured_forgetting, task_embedding_ref, task_vector_ref
            FROM techniques WHERE {active} ORDER BY id"""):
        techs.append({
            "id": r[0], "slug": r[1], "name": r[2], "lane": r[3],
            "evidence_strength": r[4], "engine_recipe_ref": r[5],
            "rig_fit": r[6], "studio_fit": r[7], "status": r[8],
            # S6.2 recipe-preview inputs (per-technique); empty until S6.3 measures them.
            "preview": {
                "difficulty_signal": r[9],
                "mixing_law": json.loads(r[10]) if r[10] else None,  # fitted-prediction object (form/predicted_*/coeffs)
                "calibration_params": r[11],
                "calibration_tokens": r[12],
                "replay_fraction": r[13],
                "measured_forgetting": r[14],
                "task_embedding_ref": r[15],
                "task_vector_ref": r[16],
            },
        })
        ids.add(r[0])

    # signal sources role-os fuses into a directional witness
    ds = {}   # technique_id -> {dataset_id}
    for tid, did in cur.execute("SELECT technique_id, dataset_id FROM technique_datasets"):
        ds.setdefault(tid, set()).add(did)
    src = {}  # technique_id -> {identifier}  (shared citation backing)
    for tid, ident in cur.execute(
            "SELECT technique_id, identifier FROM sources WHERE identifier IS NOT NULL AND technique_id IS NOT NULL"):
        src.setdefault(tid, set()).add(ident)

    # measured outcome deltas (S6.3; empty now) keyed (predecessor, successor). Only a verdict-passing
    # edge has a non-NULL steps_saved_frac (record_measurement.py gates it); we also export the
    # sign-consistency flag + raw per-seed deltas so role-os can re-derive the verdict, not just trust it.
    deltas = {}
    measured = {}  # (pred,succ) -> measured-evidence for ANY row record_measurement wrote (the verdict lives in the
                   # note), so a MEASURED-but-unverified edge (e.g. a censored steps-to-cert) is visibly distinct from
                   # a never-measured one. role-os still re-derives the verdict from outcome_delta; `measured` is display.
    for pid, sid, ssf, n, cs, psd, note in cur.execute(
            "SELECT predecessor_id, successor_id, steps_saved_frac, outcome_n_receipts, "
            "consistent_sign, per_seed_deltas, verifier_note FROM technique_edges"):
        if ssf is not None:
            d = {"steps_saved_frac": ssf, "n_receipts": n or 0}
            if cs is not None:
                d["consistent_sign"] = bool(cs)
            if psd:
                try:
                    d["per_seed"] = json.loads(psd)
                except (ValueError, TypeError):
                    pass
            deltas[(pid, sid)] = d
        if note:
            measured[(pid, sid)] = {"n_receipts": n or 0, "has_delta": ssf is not None, "note": note}

    # explicit prerequisite edges: B.predecessor_technique_id = A  =>  edge A -> B
    edges = []
    for sid, pid, stage in cur.execute(
            "SELECT id, predecessor_technique_id, stage_order FROM techniques WHERE predecessor_technique_id IS NOT NULL"):
        if pid not in ids or sid not in ids:
            continue  # an edge into a superseded/avoid technique is not part of the active curriculum
        e = {
            "from": pid, "to": sid,
            "signals": {
                "explicit_predecessor": True,
                "stage_chain": stage is not None,
                "shared_datasets": len(ds.get(pid, set()) & ds.get(sid, set())),
                "shared_sources": len(src.get(pid, set()) & src.get(sid, set())),
            },
        }
        if (pid, sid) in deltas:
            e["outcome_delta"] = deltas[(pid, sid)]
        if (pid, sid) in measured:
            e["measured"] = measured[(pid, sid)]
        edges.append(e)

    doc = {
        "schema": "roleos-curriculum/v1",
        "generated": datetime.date.today().isoformat(),
        "source": "training-knowledge/training.db",
        "techniques": techs,
        "edges": edges,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    con.close()
    print(f"curriculum.json: {len(techs)} active techniques, {len(edges)} prerequisite edges -> {out}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "curriculum.json")
    main(out)
