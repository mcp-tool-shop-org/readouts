#!/usr/bin/env python3
"""verify_cloud.py — the AUTHORITATIVE cross-family EXTERNAL_VERIFIER seat for sprite-motion-knowledge.

The study-swarm (Claude) does the web-grounded research; the `verified` flag that lands in the DB is set by a
PoLL JURY of the BIGGEST cross-family Ollama Cloud THINKING flagships (default deepseek-v4-pro:cloud 1.6T +
glm-5.2:cloud 756B + minimax-m3:cloud), because same-family judges over-rate their own family's work
(self-preference is mechanistic — Panickssery et al. 2024 arXiv:2404.13076; a disjoint-family jury is the
strongest mitigation — Verga et al. 2024 "PoLL" arXiv:2404.18796). Each juror reads each recipe's
REASONING-STRIPPED claims (name / kind / engine / claimed license + commercial_use / the one-line claim /
source urls+claims) and adjudicates REFUTE-BY-DEFAULT against a rubric declared separately from the claims.

For a sprite-MOTION KB the decisive traps are (1) FABRICATED tools/models/papers — a plausible but
non-existent 2025-2026 animation model or arXiv id (the #1 catch); (2) LICENSE over-claim — research /
academic-only weights waved through as commercial; (3) CLAIM not supported by the cited source.

Jury combination (refute-by-default, but a lone soundness-refute is down-weighted not honored — the seat
over-flags, so disambiguate against a second family):
  verified=1  : >=2 jurors confirm AND none refute
  refuted     : ANY juror finds existence=not-found, OR >=2 jurors refute -> verified=0, status='avoid' (kept visible)
  unverified  : everything else (incl. a lone refute) -> verified=0, the agent's web source stands as a lead
  license     : if any juror calls the license wrong, apply the MOST RESTRICTIVE corrected commercial_use
                (no < conditional < unknown < yes) + record license_correction — safe direction for a studio.
Writes a `cloud_verify` block per lane (provenance: served models + per-juror verdicts + tally) + a
waves/<wave>/verification.md receipt. Re-running SKIPS lanes already verified; SPRITEMOTION_VERIFY_FORCE=1 redoes.

    $env:PYTHONUTF8='1'; python scripts/verify_cloud.py waves/wave-01-foundation/research-raw.json
Env: SPRITEMOTION_VERIFY_MODELS (comma-sep jury) · OLLAMA_HOST (127.0.0.1:11434)
     SPRITEMOTION_VERIFY_TIMEOUT (per-call s, 360) · SPRITEMOTION_VERIFY_WORKERS (lanes, 3) · SPRITEMOTION_VERIFY_FORCE
"""
import json
import os
import re
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MODELS = [m.strip() for m in os.environ.get(
    "SPRITEMOTION_VERIFY_MODELS", "deepseek-v4-pro:cloud,glm-5.2:cloud,minimax-m3:cloud").split(",") if m.strip()]
HOST = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434").replace("http://", "").replace("https://", "").rstrip("/")
URL = f"http://{HOST}/api/chat"
TIMEOUT = int(os.environ.get("SPRITEMOTION_VERIFY_TIMEOUT", "360"))
WORKERS = int(os.environ.get("SPRITEMOTION_VERIFY_WORKERS", "3"))
FORCE = os.environ.get("SPRITEMOTION_VERIFY_FORCE", "") not in ("", "0", "false")
CU_RANK = {"no": 0, "conditional": 1, "unknown": 2, "yes": 3}  # lower = more restrictive (safe direction)

SYSTEM = (
    "You are an adversarial, cross-family verifier for a game SPRITE-MOTION / character-animation knowledge "
    "base. You are NOT the author of these recipes and you share no model family with them. Each recipe claims "
    "a tool, model, technique, or pipeline for animating 2.5D JRPG sprites (rigging, AI motion, inbetweening, "
    "cloud workers, combat-animation craft, motion QA). Judge each REFUTE-BY-DEFAULT against this rubric:\n"
    "  1. EXISTENCE — does this tool / model / repo / paper / technique actually exist as described? Flag "
    "invented model names, fabricated arXiv ids or repos, and capabilities attributed to a tool it does not "
    "have. A plausible-sounding but non-existent recent (2025-2026) animation model is the #1 thing to catch.\n"
    "  2. LICENSE — is the claimed commercial_use (yes/conditional/no) correct for a COMMERCIAL studio? "
    "Research / academic-only weights, non-commercial CC clauses, and base-model-inherited licenses are common "
    "traps; a permissive CODE license does NOT make the WEIGHTS commercial. Flag any over-permissive claim.\n"
    "  3. CLAIM-SUPPORT — does the one-line claim match what the cited sources actually say? Do not accept a "
    "claim merely because a url is present.\n"
    "  4. CURRENCY — is this the current state of the art, or superseded / deprecated?\n"
    "Use your own knowledge PLUS the provided source urls+claims as evidence. When you cannot confirm AND have "
    "no specific reason to doubt, return overall='unverified' (NOT a pass, NOT a refute). Use 'refuted' ONLY "
    "with a SPECIFIC reason (does not exist, invented capability, clearly wrong license). Reply with ONLY a "
    "JSON object:\n"
    '{"verdicts":[{"recipe":"<exact name>","overall":"confirmed|confirmed-with-fixes|unverified|refuted",'
    '"existence":"exists|not-found|unsure","license_check":"correct|wrong|unknown",'
    '"corrected_commercial_use":"yes|conditional|no|unknown|","fixes":"<correction if any>",'
    '"note":"<one sentence>"}]}'
)

_io_lock = threading.Lock()


def _norm_model(m):
    # strip BOTH cloud tag forms — ':cloud' (glm-5.2:cloud) AND '-cloud' (qwen3-coder:480b-cloud).
    # stripping only one false-flags the other form as a local fallback and drops its votes.
    return re.sub(r"[-:]cloud$", "", (m or "").strip()).replace(":latest", "")


def _short(m):
    return _norm_model(m).split(":")[0]


def strip_claims(lane):
    out = []
    for r in (lane.get("recipes") or []):
        summ = (r.get("summary") or "")
        if len(summ) > 600:
            summ = summ[:600] + " …"
        srcs = [f"{(s.get('url') or '').strip()} :: {(s.get('claim') or '').strip()}"
                for s in (r.get("sources") or []) if s.get("url")]
        out.append({"recipe": r.get("name"), "kind": r.get("kind"), "engine": r.get("engine_family"),
                    "claimed_license": r.get("license"), "claimed_commercial_use": r.get("commercial_use"),
                    "claim": r.get("claim"), "summary": summ, "evidence": srcs[:5]})
    return out


def call_model(model, claims, lane_name):
    user = (f"Lane: {lane_name}\nVerify every recipe below. Return one verdict per recipe, matching the recipe "
            f"name exactly.\n\nRECIPES:\n{json.dumps(claims, ensure_ascii=False, indent=1)}")
    body = json.dumps({"model": model,
                       "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                       "stream": False, "format": "json", "options": {"temperature": 0}}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        resp = json.loads(r.read().decode("utf-8"))
    served = resp.get("model", "")
    if served and _norm_model(served) != _norm_model(model):  # real fallback (e.g. local hermes) caught
        raise RuntimeError(f"model mismatch: requested {model}, daemon served {served}")
    content = ((resp.get("message") or {}).get("content", "") or "").strip()
    if content.startswith("```"):
        content = content.strip("`")
        content = content[content.find("{"):content.rfind("}") + 1]
    return served or model, json.loads(content).get("verdicts", [])


def _norm(s):
    return "".join((s or "").lower().split())


def apply_jury(lane, per_model):
    """Combine the jurors' per-recipe verdicts and mutate each recipe's verified / status / license / verify_note.

    Decision ladder. The jury OVER-FLAGS recent / studio-internal artifacts with a lone existence=not-found
    (documented in cross-family-cloud-verification.md — a juror can't web-verify a 2026 model variant or a
    studio's own internal script), so a SINGLE dissent never decides:
      - measured-on-rig  -> verified=1 ALWAYS. The rig is the authority for an on-rig measurement; a web juror
        cannot see the rig. Jury view is still recorded in verify_note.
      - refuted (verified=0, status=avoid): the wrongness is CORROBORATED — >=2 jurors not-found OR >=2 refute.
      - confirmed (verified=1): a clear majority confirms with at most one dissent — n_conf>=2 & n_ref<=1 & n_notfound<=1.
      - unverified (verified=0, kept as a lead): the murky middle (e.g. 1 confirm + 2 unverified).
    """
    by_recipe = {}
    for model, verdicts in per_model.items():
        for v in (verdicts or []):
            by_recipe.setdefault(_norm(v.get("recipe")), {})[model] = v
    tally = {"confirmed": 0, "unverified": 0, "refuted": 0, "no-verdict": 0}
    for r in (lane.get("recipes") or []):
        jurors = by_recipe.get(_norm(r.get("name")), {})
        base = (r.get("verify_note") or "").rstrip()
        measured = (r.get("evidence_strength") or "").lower() == "measured-on-rig"
        if not jurors:
            r["verified"] = 1 if measured else 0
            tag = "; kept (measured-on-rig is rig-authoritative)" if measured else ""
            r["verify_note"] = (base + " | cross-family jury: no verdict returned" + tag).strip(" |")
            tally["confirmed" if measured else "no-verdict"] += 1
            continue
        overalls = {m: (v.get("overall") or "unverified").strip().lower() for m, v in jurors.items()}
        n_conf = sum(1 for o in overalls.values() if o in ("confirmed", "confirmed-with-fixes"))
        n_ref = sum(1 for o in overalls.values() if o == "refuted")
        n_notfound = sum(1 for v in jurors.values() if (v.get("existence") or "").lower() == "not-found")

        # license — apply a juror correction ONLY when it moves toward MORE restrictive (safe direction).
        # Over-claiming commercial is the decisive risk; a juror's looser read (e.g. conditional->yes) is
        # recorded but NEVER auto-applied — only the director upgrades a commercial_use toward 'yes'.
        lic_wrong = [v for v in jurors.values() if (v.get("license_check") or "").lower() == "wrong"]
        if lic_wrong:
            fixes = "; ".join(sorted({(v.get("fixes") or "").strip() for v in lic_wrong if v.get("fixes")}))
            r["license_correction"] = fixes or "cross-family jury flagged the commercial_use claim as wrong"
            cands = [c for c in ((v.get("corrected_commercial_use") or "").strip().lower() for v in lic_wrong)
                     if c in CU_RANK]
            if cands:
                worst = min(cands, key=lambda c: CU_RANK[c])
                cur = CU_RANK.get((r.get("commercial_use") or "unknown").strip().lower(), 2)
                if CU_RANK[worst] < cur:                 # downgrade toward safe -> apply
                    r["commercial_use"] = worst
                # else: keep the more-careful current value; the looser juror read stays in license_correction

        if measured:
            r["verified"] = 1
            decision = "confirmed (measured-on-rig — rig is authoritative)"
            tally["confirmed"] += 1
        elif n_ref >= 2 or n_notfound >= 2:
            r["verified"] = 0
            r["status"] = "avoid"
            decision = "refuted"
            tally["refuted"] += 1
        elif n_conf >= 2 and n_ref <= 1 and n_notfound <= 1:
            r["verified"] = 1
            decision = "confirmed"
            tally["confirmed"] += 1
        else:
            r["verified"] = 0
            decision = "unverified"
            tally["unverified"] += 1

        votes = " ".join(f"{_short(m)}={o}" for m, o in overalls.items())
        note = f"cross-family jury [{votes}] -> {decision}"
        if n_notfound:
            note += f"; not-found x{n_notfound}"
        if r.get("license_correction"):
            note += f" [license -> commercial_use={r.get('commercial_use')}]"
        r["verify_note"] = (base + " | " + note).strip(" |")
    return tally


def already_done(lane):
    cv = lane.get("cloud_verify") or {}
    return bool(cv.get("jurors")) and not cv.get("error")


def process_lane(lane):
    name = lane.get("laneSlug") or lane.get("title")
    claims = strip_claims(lane)
    if not claims:
        lane["cloud_verify"] = {"models": MODELS, "jurors": {}, "tally": {}}
        return name, "no recipes — skipped", True
    per_model, served_list, errs = {}, [], []
    for model in MODELS:
        for attempt in (1, 2):
            try:
                served, verdicts = call_model(model, claims, name)
                per_model[model] = verdicts
                served_list.append(served)
                break
            except Exception as e:
                if attempt == 2:
                    errs.append(f"{_short(model)}: {e}")
                else:
                    time.sleep(3)
    if not per_model:
        lane["cloud_verify"] = {"models": MODELS, "error": "; ".join(errs), "jurors": {}}
        return name, f"FAILED: {errs[-1] if errs else 'no jurors'}", False
    tally = apply_jury(lane, per_model)
    lane["cloud_verify"] = {"models": served_list, "jurors": per_model, "tally": tally, "errors": errs or None}
    msg = " ".join(f"{k}={v}" for k, v in tally.items() if v)
    if errs:
        msg += f"  (jurors down: {len(errs)})"
    return name, msg, True


def write_receipt(path, data):
    wdir = os.path.dirname(path)
    L = [f"# Cross-family verification — {data.get('title', '')}",
         f"\nJury: **{' + '.join(MODELS)}** (disjoint families, off-box via the local Ollama Cloud daemon) · "
         f"{data.get('date', '')}",
         "\nReasoning-stripped, refute-by-default PoLL re-adjudication of each recipe (existence / license / "
         "claim-support / currency). `verified=1` when the recipe is **measured-on-rig** (rig-authoritative — a "
         "web juror cannot see the rig, so it false-flags recent variants) OR a **clear majority confirms** "
         "(>=2 jurors, <=1 dissent). `refuted` (status `avoid`, kept visible) only when CORROBORATED — >=2 jurors "
         "not-found OR >=2 refute; a LONE dissent -> `unverified` lead (the agent's web source stands). A license "
         "flagged wrong is applied only toward MORE restrictive; a juror's looser read is recorded, never "
         "auto-upgrades commercial_use.\n",
         "| Lane | confirmed | unverified | refuted | no-verdict |",
         "|---|---|---|---|---|"]
    grand = {}
    for lane in data.get("lanes", []):
        t = (lane.get("cloud_verify") or {}).get("tally") or {}
        for k, val in t.items():
            grand[k] = grand.get(k, 0) + val
        L.append(f"| {lane.get('laneSlug')} | {t.get('confirmed', 0)} | {t.get('unverified', 0)} | "
                 f"{t.get('refuted', 0)} | {t.get('no-verdict', 0)} |")
    L.append(f"| **total** | {grand.get('confirmed', 0)} | {grand.get('unverified', 0)} | "
             f"{grand.get('refuted', 0)} | {grand.get('no-verdict', 0)} |")
    refuted = [(l.get('laneSlug'), r.get('name'), r.get('verify_note'))
               for l in data.get("lanes", []) for r in (l.get("recipes") or [])
               if (r.get("status") or "") == "avoid" and not r.get("verified")]
    if refuted:
        L += ["\n## Refuted / flagged `avoid` by the jury\n", "| Lane | Recipe | Note |", "|---|---|---|"]
        for ln, nm, nt in refuted:
            L.append(f"| {ln} | {nm} | {(nt or '')[-200:]} |")
    else:
        L.append("\n_No recipe refuted — every recipe either confirmed (>=2 jurors) or held as an unverified lead._")
    lic = [(l.get('laneSlug'), r.get('name'), r.get('commercial_use'), r.get('license_correction'))
           for l in data.get("lanes", []) for r in (l.get("recipes") or []) if r.get("license_correction")]
    if lic:
        L += ["\n## License corrections (the decisive axis)\n", "| Lane | Recipe | commercial_use | Correction |",
              "|---|---|---|---|"]
        for ln, nm, cu, lc in lic:
            L.append(f"| {ln} | {nm} | {cu} | {(lc or '')[:180]} |")
    open(os.path.join(wdir, "verification.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    lanes = data.get("lanes", [])

    def save():
        with _io_lock:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    todo = [l for l in lanes if FORCE or not already_done(l)]
    skipped = len(lanes) - len(todo)
    print(f"cross-family jury: {', '.join(MODELS)} via {URL}  ({len(todo)} lanes, {skipped} done, {WORKERS} workers)")
    failed = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(process_lane, lane): lane for lane in todo}
        for fut in as_completed(futs):
            name, msg, ok = fut.result()
            save()  # incremental — crash-safe, and a re-run resumes from here
            print(("  OK  " if ok else "  XX  ") + f"{name:16s} {msg}")
            if not ok:
                failed.append(name)

    data["verifier_note"] = (data.get("verifier_note", "") +
                             f"  CROSS-FAMILY POLL JURY: {', '.join(MODELS)} (disjoint families), reasoning-"
                             "stripped, refute-by-default; verified=1 only on >=2-juror confirm & no refute; "
                             "any existence=not-found or >=2 refutes -> status avoid (kept visible).")
    save()
    write_receipt(path, data)
    print(f"\nverified -> {os.path.relpath(path, ROOT)} (+ verification.md)")
    if failed:
        print(f"  WARN {len(failed)} lane(s) failed (re-run to retry): " + ", ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-foundation", "research-raw.json"))
