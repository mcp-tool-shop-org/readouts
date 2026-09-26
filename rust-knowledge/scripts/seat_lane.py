#!/usr/bin/env python3
"""seat_lane.py — one rust-knowledge lane written by a chat seat, held to the harness's contract.

openrouter_lane.py reaches its generator over an API. A chat seat, such as a Grok chat in Cursor,
has no API the harness can call, so this adapter splits the harness's loop into commands the seat
(or the operator) runs by hand:

  prompt  Write the exact system and user text the harness sends for the lane: the same brief, the
          same scope from briefs/lanes.json and the same pinned pack (registry excerpts plus the
          fetched reference pages, as for Ollama, which has no search tool either). Output goes to
          waves/<wave>/seats/<seat>/<lane>.system.txt and .user.txt, plus a receipt holding their
          SHA-256s and the pack manifest. The two prompt files are git-ignored. The user text quotes
          crate source verbatim without its licence notice, so, like the harness, the repository
          keeps the hashes and never the pack. Plain .txt also keeps the markdown link check from
          reading rustdoc links inside the excerpts.
  check   Take the seat's reply (the lane JSON, in a file) through the harness's own gates:
          normalise, source admission, vacuous-check refusal, the lane lint and the compiler. Print
          the same ROUND N REVIEW the harness would send back. Each check is one round, copied to
          rounds/ and recorded in the seat receipt. The round cap matches the harness (--rounds 3:
          a first draft and three revisions).
  final   Apply the harness's final admission (drop checks the compiler never passed, then recipes
          the contract cannot admit). Write seats/<seat>/lanes/<lane>.json, the packet, and the
          receipt.

It never writes waves/<wave>/lanes/. Which draft enters the wave is the operator's decision, so a
generator already running on the same lane (the harness writes lanes/<lane>.json) cannot collide
with the seat. The seat folder also sits outside the waves/*/lanes/*.json glob that assembly and
lint read.

Every gate is imported from openrouter_lane.py, not copied, so a seat lane passes exactly the checks
a harness lane does. The seat must not open anything else in the wave folder: other lanes, their
receipts, or verification inputs. The generator never sees what its verifiers see.

Standards (0-3): PIN_PER_STEP 2 (brief, scope and pack are hashed at prompt time; the seat's model
is whatever its chat reports, recorded by `final --model`, and its sampling settings are not
pinned); ANDON_AUTHORITY 2 (a missing prompt, an unparseable reply, a round past the cap and a
pack failure all halt); NAMED_COMPENSATORS 2 (local files only: delete seats/<seat>/ to undo);
DECOMPOSE_BY_SECRETS 2 (the seat gets the prompt files and nothing else); UNCERTAINTY_GATED_HUMANS 2
(the operator picks which draft enters the wave); EXTERNAL_VERIFIER 3 (compiler, then a different
model family's retrieval verifier).

Usage (from rust-knowledge/):
  python scripts/seat_lane.py prompt --lane integer-time --wave 5 --wave-dir wave-05-si-jam-p2 \
         --brief GENERATOR-BRIEF-W5.md --seat grok-cursor
  python scripts/seat_lane.py check  --lane integer-time --wave 5 --wave-dir wave-05-si-jam-p2 \
         --seat grok-cursor --reply <file>
  python scripts/seat_lane.py final  --lane integer-time --wave 5 --wave-dir wave-05-si-jam-p2 \
         --seat grok-cursor --reply <file> --model "<model name the chat shows>"
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import openrouter_lane as ol  # noqa: E402  (the harness: its gates are the contract)
import assemble_lanes  # noqa: E402

KB = ol.KB


def seat_dir(args) -> str:
    return os.path.join(KB, "waves", args.wave_dir, "seats", args.seat)


def receipt_path(args) -> str:
    return os.path.join(seat_dir(args), f"{args.lane}.receipt.json")


def load_receipt(args) -> dict:
    p = receipt_path(args)
    if not os.path.isfile(p):
        sys.exit(f"HALT: no prompt for {args.lane} in {seat_dir(args)} (run `prompt` first)")
    return json.load(open(p, encoding="utf-8"))


def save(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        if isinstance(obj, str):
            fh.write(obj)
        else:
            json.dump(obj, fh, indent=2, ensure_ascii=False)
            fh.write("\n")


def cmd_prompt(args) -> int:
    brief = open(os.path.join(KB, "briefs", args.brief), encoding="utf-8").read()
    scope, _sc = ol.scope_text(args.lane)
    pack, manifest = ol.licence_pack() if args.lane == "crate-licences" else ol.file_pack(args.lane)
    dpack, dman = ol.docs_pack(args.lane)  # a chat seat has no search tool: same pages as the Ollama path
    pack, manifest = pack + "\n" + dpack, manifest + dman
    if len(pack) > ol.PACK_CHAR_CAP:
        sys.exit(f"HALT: pack is {len(pack)} chars, over the {ol.PACK_CHAR_CAP} cap")
    failed = [m for m in manifest if m.get("error")]
    if failed:
        sys.exit(f"HALT: {len(failed)} reference page(s) could not be fetched: {failed}")
    allowed = sorted({ol.norm_url(m["url"]) for m in manifest if m.get("url") and not m.get("error")})
    # Byte-for-byte the harness's user message (openrouter_lane.run).
    user = (f"YOUR LANE (from briefs/lanes.json):\n{scope}\n\n"
            f"SOURCE EXCERPTS (read from the local cargo registry at the pinned versions; each is an 'opened' "
            f"source you may cite by the URL in its header):\n\n{pack}")
    d = seat_dir(args)
    save(os.path.join(d, f"{args.lane}.system.txt"), brief)
    save(os.path.join(d, f"{args.lane}.user.txt"), user)
    rec = {"lane": args.lane, "wave": ol.WAVE, "seat": args.seat, "date": dt.date.today().isoformat(),
           "brief": args.brief, "brief_sha256": ol.sha(brief.encode()), "scope_sha256": ol.sha(scope.encode()),
           "user_prompt_sha256": ol.sha(user.encode()), "pack": manifest, "pack_chars": len(pack),
           "allowed_opened_urls": allowed, "rounds_cap": args.rounds, "rounds": [],
           "harness_sha256": ol.sha(open(ol.__file__, "rb").read()),
           "adapter_sha256": ol.sha(open(os.path.abspath(__file__), "rb").read())}
    save(receipt_path(args), rec)
    print(f"prompt for {args.lane} -> {os.path.relpath(d, KB)}: system {len(brief)} chars, user {len(user)} chars, "
          f"{len(manifest)} pack items, {len(allowed)} citable URLs")
    return 0


def gate(args, rec: dict, reply_text: str):
    """The harness's round, verbatim: returns (lane, results, lint_errors, downgraded, n_vacuous)."""
    try:
        lane = ol.parse_json(reply_text)
    except (json.JSONDecodeError, ValueError) as e:
        sys.exit(f"HALT: the reply is not one lane JSON object ({e})")
    ol.normalise(lane, args.lane)
    downgraded = ol.admit_sources(lane, set(rec["allowed_opened_urls"]))
    n_vac = 0
    for r in lane.get("recipes") or []:
        for c in r.get("checks") or []:
            if ol.vacuous(c):
                c["_vacuous"] = True
                n_vac += 1
    # Lint as the lane's own final file, like the harness: a draft of the same lane already in
    # lanes/ is treated as this lane, not as a name collision.
    out = os.path.join(KB, "waves", args.wave_dir, "lanes", f"{args.lane}.json")
    lint_errors = ol.lint(lane, out)
    clean = json.loads(json.dumps(lane))
    for r in clean.get("recipes") or []:
        for c in r.get("checks") or []:
            c.pop("_vacuous", None)
    work = tempfile.mkdtemp(prefix="rk-seat-")
    draft = os.path.join(work, f"{args.lane}.json")
    save(draft, clean)
    results = ol.oracle(draft)
    shutil.rmtree(work, ignore_errors=True)
    return lane, results, lint_errors, downgraded, n_vac


def cmd_check(args) -> int:
    rec = load_receipt(args)
    rnd = len(rec["rounds"])
    if rnd > rec["rounds_cap"]:
        sys.exit(f"HALT: {rnd} rounds already checked; the cap is a first draft plus {rec['rounds_cap']} revisions. "
                 f"Run `final`.")
    text = open(args.reply, encoding="utf-8").read()
    lane, results, lint_errors, downgraded, n_vac = gate(args, rec, text)
    kept = os.path.join(seat_dir(args), "rounds", f"{args.lane}.r{rnd}.json")
    save(kept, text if text.endswith("\n") else text + "\n")
    n_fail = sum(1 for r in results if not r.get("ok")) + n_vac
    rec["rounds"].append({"round": rnd, "reply": os.path.relpath(kept, KB).replace(os.sep, "/"),
                          "reply_sha256": ol.sha(text.encode()), "recipes": len(lane.get("recipes") or []),
                          "checks": len(results), "failing_checks": n_fail, "lint_errors": len(lint_errors),
                          "downgraded_sources": len(downgraded),
                          "at": dt.datetime.now().isoformat(timespec="seconds")})
    save(receipt_path(args), rec)
    print(f"round {rnd}: {len(lane.get('recipes') or [])} recipes, {len(results)} checks, {n_fail} failing "
          f"({n_vac} vacuous), {len(lint_errors)} lint errors, {len(downgraded)} sources downgraded")
    if not n_fail and not lint_errors and not downgraded:
        print("CLEAN: every check passes and the contract admits every recipe. Run `final`.")
    elif rnd >= rec["rounds_cap"]:
        print("Round cap reached. Run `final`: failing checks and inadmissible recipes will be dropped.")
    else:
        print()
        print(ol.feedback(rnd + 1, results, lint_errors, downgraded, lane))
    return 0


def cmd_final(args) -> int:
    rec = load_receipt(args)
    if not rec["rounds"]:
        sys.exit("HALT: no checked round (run `check` on the reply first)")
    text = open(args.reply, encoding="utf-8").read()
    if ol.sha(text.encode()) != rec["rounds"][-1]["reply_sha256"]:
        sys.exit("HALT: this reply is not the last checked round; run `check` on it first")
    lane, results, _lint, downgraded, _nv = gate(args, rec, text)
    # The harness's final admission (openrouter_lane.run), verbatim.
    failing = {(r["slug"], r["index"]) for r in results if not r.get("ok")}
    dropped_checks, dropped_recipes = [], []
    out = os.path.join(KB, "waves", args.wave_dir, "lanes", f"{args.lane}.json")
    for r in lane.get("recipes") or []:
        slug = assemble_lanes.slugify(r.get("name"))
        kept = []
        for i, c in enumerate(r.get("checks") or []):
            if (slug, i) in failing or c.pop("_vacuous", False):
                dropped_checks.append({"recipe": r.get("name"), "label": c.get("label")})
            else:
                kept.append(c)
        r["checks"] = kept
    admitted = []
    for r in lane.get("recipes") or []:
        errs = ol.lint(dict(lane, recipes=[r]), out)
        if errs:
            dropped_recipes.append({"recipe": r.get("name"), "why": errs[:3]})
        else:
            admitted.append(r)
    lane["recipes"] = admitted
    packet = lane.pop("packet", "") or ""
    d = seat_dir(args)
    save(os.path.join(d, "lanes", f"{args.lane}.json"), lane)
    save(os.path.join(d, f"{args.lane}.md"),
         f"# {lane.get('title') or args.lane} — generator packet\n\n"
         f"Written by the `{args.seat}` seat (`{args.model}`) through `scripts/seat_lane.py`; unverified until the "
         f"wave's verification record says otherwise.\n\n{packet}\n")
    rec.update(model_reported=args.model, finalised=dt.datetime.now().isoformat(timespec="seconds"),
               dropped_checks=dropped_checks, dropped_recipes=dropped_recipes, downgraded_sources=downgraded,
               final_recipes=len(admitted), final_checks=sum(len(r.get("checks") or []) for r in admitted),
               status="complete")
    save(receipt_path(args), rec)
    print(f"wrote {os.path.relpath(os.path.join(d, 'lanes', args.lane + '.json'), KB)}: {len(admitted)} recipes, "
          f"{rec['final_checks']} checks; dropped {len(dropped_checks)} checks, {len(dropped_recipes)} recipes")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("prompt", "check", "final"):
        p = sub.add_parser(name)
        p.add_argument("--lane", required=True)
        p.add_argument("--wave", type=int, required=True)
        p.add_argument("--wave-dir", required=True)
        p.add_argument("--seat", required=True, help="a short name for the seat, e.g. grok-cursor")
        if name == "prompt":
            p.add_argument("--brief", required=True, help="the brief under briefs/, as the harness takes it")
            p.add_argument("--rounds", type=int, default=3, help="revision rounds after the first draft")
        else:
            p.add_argument("--reply", required=True, help="a file holding the seat's lane JSON")
        if name == "final":
            p.add_argument("--model", required=True, help="the model name the seat's chat reports")
    args = ap.parse_args()
    ol.WAVE, ol.WAVE_DIR = args.wave, args.wave_dir  # the harness's globals pick scope, pack and lint
    return {"prompt": cmd_prompt, "check": cmd_check, "final": cmd_final}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
