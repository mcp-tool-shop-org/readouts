#!/usr/bin/env python3
"""verify_cloud.py — the AUTHORITATIVE cross-family EXTERNAL_VERIFIER seat for xrpl-knowledge.

The study-swarm (Claude) does the research; the flag that ends up in the DB is set by a DIFFERENT model
family — a LARGE Ollama Cloud model (default deepseek-v3.1:671b-cloud, ~671B). Same-family judges over-rate
their own family's work (self-preference is mechanistic — Panickssery et al. 2024 arXiv:2404.13076; mitigated
by a cross-family jury, Verga et al. 2024 "PoLL" arXiv:2404.18796). The verifier reads each lane's
REASONING-STRIPPED claims (name / kind / network_status / chain / XLS / amendment + source urls+claims) and
adjudicates refute-by-default against an external rubric declared separately from the claims.

Writes `cloud_verify` back into the wave's research-raw.json; load_db.py reads it as the authoritative
`verified` source. Cloud routing: the local Ollama daemon (signed into Ollama Cloud) serves `*-cloud` tags via
POST /api/chat. The daemon reports the served model WITHOUT the `-cloud` suffix, so the fallback guard compares
modulo that suffix (a real fallback to the local tier model is still caught).

Robust: lanes run concurrently, results write incrementally (crash-safe), and a re-run SKIPS lanes already
verified — so re-running only retries the failures. Exits non-zero if any lane is still unverified.

Usage:  $env:PYTHONUTF8='1'; python scripts/verify_cloud.py [waves/wave-NN/research-raw.json]
Env:    XRPL_VERIFY_MODEL (deepseek-v3.1:671b-cloud) · OLLAMA_HOST (127.0.0.1:11434)
        XRPL_VERIFY_TIMEOUT (per-lane seconds, 360) · XRPL_VERIFY_WORKERS (3) · XRPL_VERIFY_FORCE (1 = redo all)
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
MODEL = os.environ.get("XRPL_VERIFY_MODEL", "deepseek-v3.1:671b-cloud")
HOST = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434").replace("http://", "").replace("https://", "").rstrip("/")
URL = f"http://{HOST}/api/chat"
TIMEOUT = int(os.environ.get("XRPL_VERIFY_TIMEOUT", "360"))
WORKERS = int(os.environ.get("XRPL_VERIFY_WORKERS", "3"))
FORCE = os.environ.get("XRPL_VERIFY_FORCE", "") not in ("", "0", "false")

SYSTEM = (
    "You are an adversarial, cross-family citation verifier for an XRP Ledger (XRPL) knowledge base. "
    "You are NOT the author of these claims and you share no model family with them. Judge each claim "
    "REFUTE-BY-DEFAULT against this external rubric:\n"
    "  1. EXISTENCE — does this capability exist on XRPL (or Xahau / the XRPL EVM sidechain) as described?\n"
    "  2. NETWORK_STATUS — is the claimed status correct? The decisive check: if it claims 'mainnet-live', "
    "is the underlying amendment ACTUALLY enabled on XRPL MAINNET as of mid-2026 (not merely proposed, "
    "voting, or devnet/testnet-only)? Flag anything stated as live that is only pending.\n"
    "  3. IDENTIFIERS — is the XLS number and amendment name correct?\n"
    "  4. CURRENCY — is this the current mechanism, or has it been superseded/deprecated?\n"
    "Use your own parametric knowledge of XRPL plus the provided source urls+claims as evidence. Do NOT "
    "accept a claim just because a url is present. When you cannot confirm, return overall='unverified' "
    "(NOT a pass). Reply with ONLY a JSON object: "
    '{"verdicts":[{"capability":"<exact name>","overall":"confirmed|confirmed-with-fixes|unverified|refuted",'
    '"network_status_check":"<what the status really is>","currency":"current|stale|unknown",'
    '"fixes":"<correction if any>","note":"<one sentence>"}]}'
)

_io_lock = threading.Lock()


def _norm_model(m):
    # strip BOTH cloud tag forms — ':cloud' (glm-5.2:cloud) AND '-cloud' (qwen3-coder:480b-cloud).
    # stripping only one false-flags the other form as a local fallback and drops its votes.
    return re.sub(r"[-:]cloud$", "", (m or "").strip()).replace(":latest", "")


def strip_claims(lane):
    caps = (lane.get("research") or {}).get("capabilities") or []
    out = []
    for c in caps:
        srcs = [f"{(s.get('url') or '').strip()} :: {(s.get('claim') or '').strip()}"
                for s in (c.get("sources") or []) if s.get("url")]
        out.append({"capability": c.get("name"), "kind": c.get("kind"),
                    "claimed_network_status": c.get("network_status"), "chain": c.get("chain"),
                    "xls_standard": c.get("xls_standard"), "amendment_name": c.get("amendment_name"),
                    "evidence": srcs[:6]})
    return out


def call_model(claims, lane_name):
    user = (f"Lane: {lane_name}\nVerify every capability below. Return one verdict per capability, matching "
            f"the capability name exactly.\n\nCLAIMS:\n{json.dumps(claims, ensure_ascii=False, indent=1)}")
    body = json.dumps({"model": MODEL,
                       "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                       "stream": False, "format": "json", "options": {"temperature": 0}}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        resp = json.loads(r.read().decode("utf-8"))
    served = resp.get("model", "")
    if served and _norm_model(served) != _norm_model(MODEL):  # real fallback (e.g. to local hermes) still caught
        raise RuntimeError(f"model mismatch: requested {MODEL}, daemon served {served}")
    content = (resp.get("message") or {}).get("content", "").strip()
    if content.startswith("```"):
        content = content.strip("`")
        content = content[content.find("{"):content.rfind("}") + 1]
    return served or MODEL, json.loads(content).get("verdicts", [])


def already_done(lane):
    cv = lane.get("cloud_verify") or {}
    return bool(cv.get("verdicts")) and not cv.get("error")


def process_lane(lane):
    name = lane.get("name") or lane.get("slug")
    claims = strip_claims(lane)
    if not claims:
        lane["cloud_verify"] = {"model": MODEL, "verdicts": []}
        return name, "no capabilities — skipped", True
    err = None
    for attempt in (1, 2):
        try:
            served, verdicts = call_model(claims, name)
            lane["cloud_verify"] = {"model": served, "verdicts": verdicts}
            tally = {}
            for v in verdicts:
                ov = (v.get("overall") or "unverified").strip()
                tally[ov] = tally.get(ov, 0) + 1
            return name, f"{len(verdicts)} verdicts  " + " ".join(f"{k}={v}" for k, v in sorted(tally.items())), True
        except Exception as e:
            err = e
            if attempt == 1:
                time.sleep(3)
    lane["cloud_verify"] = {"model": MODEL, "error": str(err), "verdicts": []}
    return name, f"FAILED: {err}", False


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    lanes = data.get("lanes", [])

    def save():
        with _io_lock:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)

    todo = [l for l in lanes if FORCE or not already_done(l)]
    skipped = len(lanes) - len(todo)
    print(f"cross-family verify: {MODEL} via {URL}  ({len(todo)} lanes, {skipped} already done, {WORKERS} workers)")
    failed = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(process_lane, lane): lane for lane in todo}
        for fut in as_completed(futs):
            name, msg, ok = fut.result()
            save()  # incremental — crash-safe, and a re-run resumes from here
            print(("  ✓ " if ok else "  ✗ ") + f"{name:34s} {msg}")
            if not ok:
                failed.append(name)

    totals = {}
    for lane in lanes:
        for v in (lane.get("cloud_verify") or {}).get("verdicts", []):
            ov = (v.get("overall") or "unverified").strip()
            totals[ov] = totals.get(ov, 0) + 1
    print(f"\n{MODEL} verdicts -> {os.path.relpath(path, ROOT)}")
    print("  totals: " + (" · ".join(f"{k} {v}" for k, v in sorted(totals.items())) or "none"))
    if failed:
        print(f"  ⚠ {len(failed)} lane(s) failed (re-run to retry just these): " + ", ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-foundation", "research-raw.json")
    main(p)
