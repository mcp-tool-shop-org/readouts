#!/usr/bin/env python3
"""verify_cloud.py — cross-family EXTERNAL_VERIFIER hardening pass for blender-knowledge.

The study-swarm (Claude/Sonnet) did the web-grounded research; this pass re-adjudicates each recipe's
Blender-4.x CURRENCY with a DIFFERENT model family — a large Ollama Cloud model (default
deepseek-v3.1:671b-cloud) — because same-family judges over-rate their own family's work (self-preference
is mechanistic; mitigated by a cross-family juror). Reasoning-stripped claims in, refute-by-default out.

Currency-KB nuance: for a fast-moving tool, the verifier's OWN parametric Blender knowledge is cutoff-limited,
so the rubric tells it to return 'unverified' (a down-weight, NOT a refute) for recent 4.3/4.4 features it
can't confirm, and to 'refuted' only with a SPECIFIC reason (invented API, clear 3.x-ism stated as 4.x). The
fetched live-docs sources remain the currency authority.

Mutates each recipe in the wave's research-raw.json:
  confirmed            -> currency unchanged
  confirmed-with-fixes -> solid demoted to plausible; fix appended to verify_note
  unverified           -> solid demoted to plausible (cross-family couldn't confirm; live source stands)
  refuted              -> currency -> shaky (or blender3_stale if currency_check=='stale'); shows in v_flagged
Also writes a cloud_verify block per lane (provenance) + waves/<wave>/verification.md, then re-run load_db.

    $env:PYTHONUTF8='1'; python scripts/verify_cloud.py waves/wave-01-pipeline-core/research-raw.json
Env: BLENDER_VERIFY_MODEL (deepseek-v3.1:671b-cloud) · OLLAMA_HOST (127.0.0.1:11434)
     BLENDER_VERIFY_TIMEOUT (per-lane s, 360) · BLENDER_VERIFY_WORKERS (3)
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
MODEL = os.environ.get("BLENDER_VERIFY_MODEL", "deepseek-v3.1:671b-cloud")
HOST = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434").replace("http://", "").replace("https://", "").rstrip("/")
URL = f"http://{HOST}/api/chat"
TIMEOUT = int(os.environ.get("BLENDER_VERIFY_TIMEOUT", "360"))
WORKERS = int(os.environ.get("BLENDER_VERIFY_WORKERS", "3"))

SYSTEM = (
    "You are an adversarial, cross-family verifier for a Blender knowledge base. You are NOT the author of "
    "these recipes and share no model family with them. Each recipe claims a CURRENT Blender 4.x practice / "
    "API / setting. Judge each REFUTE-BY-DEFAULT against this rubric:\n"
    "  1. EXISTENCE — does this Blender feature / operator / bpy attribute-path / setting actually exist as "
    "described? Flag invented operators, wrong bpy paths, or non-existent settings.\n"
    "  2. CURRENCY — is this CURRENT Blender 4.x, or a stale 2.8/2.9/3.x-ism stated as current? Known shifts: "
    "render-engine id 'BLENDER_EEVEE' -> 'BLENDER_EEVEE_NEXT' (4.2); the removed 'Auto Smooth' checkbox -> the "
    "4.1 Smooth-by-Angle modifier; bone layers -> 4.0 Bone Collections; Filmic -> the 4.0 AgX default view "
    "transform; legacy add-on install -> the 4.2 Extensions platform; the 4.0 Principled BSDF v2 input renames. "
    "Flag 3.x-isms presented as 4.x.\n"
    "  3. CONSISTENCY — is the 'how' internally consistent and correct for the stated blender_version?\n"
    "Use your own Blender knowledge PLUS the provided source urls+claims as evidence. Do NOT accept a claim "
    "just because a url is present. IMPORTANT: if you cannot confirm a claim AND have no specific reason to "
    "doubt it (e.g. a very recent 4.3/4.4 feature beyond your training), return overall='unverified' — NOT a "
    "pass and NOT a refute. Use 'refuted' ONLY when you have a SPECIFIC reason it is wrong or stale. Reply with "
    "ONLY a JSON object:\n"
    '{"verdicts":[{"recipe":"<exact name>","overall":"confirmed|confirmed-with-fixes|unverified|refuted",'
    '"currency_check":"current|stale|unknown","fixes":"<correction if any>","note":"<one sentence>"}]}'
)

_io_lock = threading.Lock()


def _norm_model(m):
    # strip BOTH cloud tag forms — ':cloud' (glm-5.2:cloud) AND '-cloud' (qwen3-coder:480b-cloud).
    # stripping only one false-flags the other form as a local fallback and drops its votes.
    return re.sub(r"[-:]cloud$", "", (m or "").strip()).replace(":latest", "")


def strip_claims(lane):
    out = []
    for r in (lane.get("recipes") or []):
        how = (r.get("how") or "")
        if len(how) > 700:
            how = how[:700] + " …"
        srcs = [f"{(s.get('url') or '').strip()} :: {(s.get('claim') or '').strip()}"
                for s in (r.get("sources") or []) if s.get("url")]
        out.append({"recipe": r.get("name"), "what": r.get("what"), "how": how,
                    "blender_version": r.get("blender_version"), "claimed_currency": r.get("currency"),
                    "evidence": srcs[:4]})
    return out


def call_model(claims, lane_name):
    user = (f"Lane: {lane_name}\nVerify every recipe below. Return one verdict per recipe, matching the recipe "
            f"name exactly.\n\nRECIPES:\n{json.dumps(claims, ensure_ascii=False, indent=1)}")
    body = json.dumps({"model": MODEL,
                       "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                       "stream": False, "format": "json", "options": {"temperature": 0}}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        resp = json.loads(r.read().decode("utf-8"))
    served = resp.get("model", "")
    if served and _norm_model(served) != _norm_model(MODEL):  # real fallback (e.g. to local hermes) caught
        raise RuntimeError(f"model mismatch: requested {MODEL}, daemon served {served}")
    content = ((resp.get("message") or {}).get("content", "") or "").strip()
    if content.startswith("```"):
        content = content.strip("`")
        content = content[content.find("{"):content.rfind("}") + 1]
    return served or MODEL, json.loads(content).get("verdicts", [])


def _norm(s):
    return "".join((s or "").lower().split())


def apply_verdicts(lane, verdicts):
    """Mutate recipe currency/verify_note per cross-family verdict. Returns a tally."""
    vmap = {_norm(v.get("recipe")): v for v in verdicts}
    tally = {"confirmed": 0, "confirmed-with-fixes": 0, "unverified": 0, "refuted": 0, "no-verdict": 0}
    for r in (lane.get("recipes") or []):
        v = vmap.get(_norm(r.get("name")))
        orig = (r.get("currency") or "").lower()
        r["research_currency"] = orig
        base_note = (r.get("verify_note") or "").rstrip()
        if not v:
            r["verify_note"] = (base_note + " | cross-family (deepseek): no verdict returned.").strip(" |")
            tally["no-verdict"] += 1
            continue
        ov = (v.get("overall") or "unverified").strip().lower()
        cc = (v.get("currency_check") or "").strip().lower()
        note = f"cross-family (deepseek-v3.1): {ov}"
        if v.get("note"):
            note += f" — {v['note']}"
        if ov == "refuted":
            r["currency"] = "blender3_stale" if cc == "stale" else "shaky"
            tally["refuted"] += 1
        elif ov == "confirmed-with-fixes":
            if orig == "solid":
                r["currency"] = "plausible"
            if v.get("fixes"):
                note += f" [fix: {v['fixes']}]"
            tally["confirmed-with-fixes"] += 1
        elif ov == "unverified":
            if orig == "solid":
                r["currency"] = "plausible"
            tally["unverified"] += 1
        else:  # confirmed
            tally["confirmed"] += 1
        r["verify_note"] = (base_note + " | " + note).strip(" |")
    return tally


def process_lane(lane):
    name = lane.get("laneSlug") or lane.get("title")
    claims = strip_claims(lane)
    if not claims:
        lane["cloud_verify"] = {"model": MODEL, "verdicts": [], "tally": {}}
        return name, "no recipes — skipped", True
    err = None
    for attempt in (1, 2):
        try:
            served, verdicts = call_model(claims, name)
            tally = apply_verdicts(lane, verdicts)
            lane["cloud_verify"] = {"model": served, "verdicts": verdicts, "tally": tally}
            return name, " ".join(f"{k}={v}" for k, v in tally.items() if v), True
        except Exception as e:
            err = e
            if attempt == 1:
                time.sleep(3)
    lane["cloud_verify"] = {"model": MODEL, "error": str(err), "verdicts": []}
    return name, f"FAILED: {err}", False


def write_receipt(path, data):
    wdir = os.path.dirname(path)
    L = [f"# Cross-family verification — {data.get('title', '')}",
         f"\nModel: **{MODEL}** (cross-family, off-box via the local Ollama Cloud daemon) · {data.get('date','')}",
         "\nReasoning-stripped, refute-by-default re-adjudication of each recipe's Blender-4.x currency. "
         "`unverified` = the cross-family juror could not independently confirm (often a recent 4.3/4.4 feature "
         "beyond its training) — a down-weight, not a refute; the fetched live-docs source remains the authority.\n",
         "| Lane | confirmed | w/fixes | unverified | refuted | no-verdict |",
         "|---|---|---|---|---|---|"]
    grand = {}
    for lane in data.get("lanes", []):
        t = (lane.get("cloud_verify") or {}).get("tally") or {}
        for k, v in t.items():
            grand[k] = grand.get(k, 0) + v
        L.append(f"| {lane.get('laneSlug')} | {t.get('confirmed',0)} | {t.get('confirmed-with-fixes',0)} | "
                 f"{t.get('unverified',0)} | {t.get('refuted',0)} | {t.get('no-verdict',0)} |")
    L.append(f"| **total** | {grand.get('confirmed',0)} | {grand.get('confirmed-with-fixes',0)} | "
             f"{grand.get('unverified',0)} | {grand.get('refuted',0)} | {grand.get('no-verdict',0)} |")
    refuted = [(l.get('laneSlug'), r.get('name'), r.get('currency'), r.get('verify_note'))
               for l in data.get("lanes", []) for r in (l.get("recipes") or [])
               if (r.get("currency") or "") in ("shaky", "blender3_stale", "wrong")]
    if refuted:
        L += ["\n## Demoted by the cross-family pass\n", "| Lane | Recipe | New currency | Note |", "|---|---|---|---|"]
        for ln, nm, cu, nt in refuted:
            L.append(f"| {ln} | {nm} | {cu} | {(nt or '')[-160:]} |")
    else:
        L.append("\n_No recipe refuted — every recipe survived the cross-family pass (confirmed / down-weighted to plausible)._")
    open(os.path.join(wdir, "verification.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    lanes = data.get("lanes", [])
    print(f"cross-family verify: {MODEL} via {URL}  ({len(lanes)} lanes, {WORKERS} workers)")

    def save():
        with _io_lock:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    failed = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(process_lane, lane): lane for lane in lanes}
        for fut in as_completed(futs):
            name, msg, ok = fut.result()
            save()
            print(("  OK  " if ok else "  XX  ") + f"{name:20s} {msg}")
            if not ok:
                failed.append(name)

    # stamp the wave verifier_note + write the receipt
    data["verifier_note"] = (data.get("verifier_note", "") +
                             f"  CROSS-FAMILY HARDENING: re-adjudicated by {MODEL} (different model family), "
                             "reasoning-stripped, refute-by-default; solid recipes the juror couldn't confirm "
                             "were down-weighted to plausible, refuted ones moved to shaky/blender3_stale.")
    save()
    write_receipt(path, data)
    print(f"\nverified -> {os.path.relpath(path, ROOT)} (+ verification.md)")
    if failed:
        print(f"  WARN {len(failed)} lane(s) failed (re-run to retry): " + ", ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-pipeline-core", "research-raw.json"))
