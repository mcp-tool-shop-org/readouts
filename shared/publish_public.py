#!/usr/bin/env python3
"""Publish readouts-internal's main to the public mirror, end to end, or stop at a gate.

The daily publish (Director, 2026-10-13): readouts is updated in the private repo
first and reaches the public repo only through export_public.py's allow-list. This
wraps the whole flow so a scheduled run cannot skip a step:

  1. the public clone must be a clean checkout of mcp-tool-shop-org/readouts (never
     -internal: a rename once left origin pointing at the wrong repository), at its
     origin/main, committing as the noreply identity;
  2. this tree must be clean, because the export copies files from disk;
  3. if origin/main's last publish names this internal commit, there is nothing to do;
  4. export_public.py --out <clone>, with all of its gates;
  5. no file may be deleted from the public repo except Atlas's generated map files,
     which step 6 rebuilds (an export once tried to delete verify.py);
  6. one commit, then `atlas map` with the pin the public verify workflow uses, the map
     amended into the same commit, then `atlas check`. The public repo keeps a map
     under the org rule; its boundaries and workflow live in the public/ overlay;
  7. the identity scan on the final tree must return RESULT CLEAN;
  8. with --push, a plain push to main (never a force push).

Exit 0: published, ready (without --push) or nothing to publish. Exit 2: a gate
stopped it, with the reason. Nothing is pushed unless every step passed.

    python shared/publish_public.py --clone <public clone>            # build and check, no push
    python shared/publish_public.py --clone <public clone> --push     # publish
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_REMOTE = re.compile(r"github\.com[:/]mcp-tool-shop-org/readouts(\.git)?/?$")
ATLAS_GENERATED = {"atlas/README.md", "atlas/page.json", "atlas/statistics.json", "atlas/structure.json"}
TRAILER = "Internal-Commit"


class Halt(Exception):
    pass


def run(args, cwd, check=True):
    got = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and got.returncode != 0:
        said = (got.stderr or got.stdout or "").strip().splitlines()
        raise Halt(f"{' '.join(args[:3])} failed: {said[-1] if said else got.returncode}")
    return got


def git(cwd, *args, check=True):
    return run(["git", *args], cwd, check).stdout.strip()


def preflight(clone):
    url = git(clone, "remote", "get-url", "origin")
    if not PUBLIC_REMOTE.search(url):
        raise Halt(f"the clone's origin is {url}, not mcp-tool-shop-org/readouts")
    email = git(clone, "config", "user.email", check=False)
    if not email.endswith("@users.noreply.github.com"):
        raise Halt(f"the clone commits as {email or 'nobody'}; set the noreply identity first")
    if git(clone, "status", "--porcelain"):
        raise Halt("the public clone has uncommitted changes")
    if git(ROOT, "status", "--porcelain"):
        raise Halt("this internal tree has uncommitted changes; the export copies from disk")
    git(clone, "fetch", "origin")
    git(clone, "merge", "--ff-only", "origin/main")


def last_published(clone):
    body = git(clone, "log", "-1", f"--grep=^{TRAILER}:", "--format=%B", "origin/main")
    found = re.search(rf"^{TRAILER}:\s*([0-9a-f]{{40}})\s*$", body, re.M)
    return found.group(1) if found else None


def subjects_since(since, head):
    """The internal commits this publish carries. Before the first trailer there is no
    starting point, so none are listed rather than a misleading recent history."""
    if not since:
        return []
    return git(ROOT, "log", "--format=%h %s", f"{since}..{head}", "-n", "30").splitlines()


def atlas_pin(clone):
    path = os.path.join(clone, ".github", "workflows", "verify.yml")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        raise Halt("the public verify workflow is missing, so there is no Atlas pin")
    found = re.search(r"@dogfood-lab/atlas@(\d+\.\d+\.\d+)", text)
    if not found:
        raise Halt("the public verify workflow names no pinned Atlas version")
    return found.group(1)


def npx():
    found = shutil.which("npx") or shutil.which("npx.cmd")
    if not found:
        raise Halt("npx is not on PATH; Atlas cannot run")
    return found


def porcelain_deletions(text):
    """Deleted paths from `git status --porcelain` output, read raw: each line is two status
    columns, a space, then the path. Stripping the whole output first would eat the first
    line's leading space and cut a character off its path (the 2026-10-13 halt on 'tlas/')."""
    out = []
    for line in text.splitlines():
        if len(line) > 3 and "D" in line[:2]:
            out.append(line[3:].strip().strip('"'))
    return out


def deleted(clone):
    return porcelain_deletions(run(["git", "status", "--porcelain"], clone).stdout)


def identity_clean(clone):
    scanner = os.path.join(os.path.expanduser("~"), ".grok", "bin", "identity-scan.py")
    if not os.path.isfile(scanner):
        raise Halt("identity-scan.py is missing; the identity gate could not run")
    got = run([sys.executable, scanner, "."], clone, check=False)
    last = (got.stdout or "").strip().splitlines()
    return bool(last) and last[-1].strip() == "RESULT CLEAN"


def lock_path(clone):
    return os.path.join(git(clone, "rev-parse", "--absolute-git-dir"), "publish_public.lock")


def take_lock(clone):
    """One publish at a time per clone. The first scheduled run met a manual publish mid-export
    and halted on the clone's half-written tree; a lock names that case instead."""
    path = lock_path(clone)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise Halt(f"another publish holds {path}; if no publish is running, remove it and re-run")
    with os.fdopen(fd, "w") as fh:
        fh.write(str(os.getpid()))
    return path


def publish(clone, push, allow_delete):
    report = {"clone": os.path.basename(os.path.normpath(clone)), "pushed": False}
    lock = take_lock(clone)
    try:
        return _publish(clone, push, allow_delete, report)
    finally:
        try:
            os.remove(lock)
        except OSError:
            pass


def site_audit():
    """The public Pages workflow runs `npm audit --audit-level=high` before it builds, so a new
    advisory against a site dependency fails the deploy whatever the content (2026-10-13:
    sharp and source-map-js). Read the same audit from the lockfile here and report it; a
    failing audit doesn't stop the content publish, but the report says Pages will fail."""
    site = os.path.join(ROOT, "public", "site")
    if not os.path.isfile(os.path.join(site, "package-lock.json")):
        return "no site lockfile"
    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        return "unknown: npm is not on PATH"
    try:
        got = run([npm, "audit", "--audit-level=high", "--json"], site, check=False)
        data = json.loads(got.stdout or "{}")
    except (Halt, ValueError):
        return "unknown: npm audit did not run"
    counts = (data.get("metadata") or {}).get("vulnerabilities") or {}
    high = int(counts.get("high", 0)) + int(counts.get("critical", 0))
    return "ok" if high == 0 else f"failing: {high} high or critical advisories; run npm audit fix in public/site"


def _publish(clone, push, allow_delete, report):
    preflight(clone)
    report["site_audit"] = site_audit()
    head = git(ROOT, "rev-parse", "HEAD")
    since = last_published(clone)
    report.update(internal=head, last_published=since)
    if since == head:
        report["result"] = "nothing to publish: the public repo already carries this internal commit"
        return report

    got = run([sys.executable, os.path.join(ROOT, "shared", "export_public.py"), "--out", clone], ROOT, check=False)
    tail = (got.stdout or "").strip().splitlines()[-12:]
    if got.returncode != 0 or not tail or tail[-1].strip() != "all gates passed":
        raise Halt("export_public.py stopped: " + " | ".join(tail[-4:]))

    gone = sorted(set(deleted(clone)) - ATLAS_GENERATED - set(allow_delete))
    if gone:
        raise Halt(f"the export would delete {len(gone)} path(s) from the public repo: " + ", ".join(gone[:10]))

    git(clone, "add", "-A")
    if not git(clone, "status", "--porcelain"):
        report["result"] = "nothing to publish: the export matches the public repo"
        return report
    subjects = subjects_since(since, head)
    carried = ("\n".join(f"- {s}" for s in subjects) + "\n\n" if subjects else
               "The first publish through publish_public.py; earlier publications carry no trailer.\n\n" if not since else "")
    message = f"readouts: publish internal {head[:7]}\n\n{carried}{TRAILER}: {head}\n"
    git(clone, "commit", "-q", "-m", message)

    pin = atlas_pin(clone)
    tool = npx()
    run([tool, "--yes", f"@dogfood-lab/atlas@{pin}", "map"], clone)
    if git(clone, "status", "--porcelain"):
        git(clone, "add", "atlas")
        git(clone, "commit", "-q", "--amend", "--no-edit")
    checked = run([tool, "--yes", f"@dogfood-lab/atlas@{pin}", "check"], clone, check=False)
    if checked.returncode != 0:
        raise Halt("atlas check failed on the published tree: " + (checked.stdout or checked.stderr).strip()[-300:])

    if not identity_clean(clone):
        raise Halt("the identity scan did not return RESULT CLEAN on the published tree")

    files = git(clone, "diff", "--name-only", "origin/main", "HEAD").splitlines()
    report.update(commit=git(clone, "rev-parse", "HEAD"), files_changed=len(files), atlas=pin,
                  internal_commits=subjects)
    if not files:
        git(clone, "reset", "-q", "--hard", "origin/main")
        report["result"] = "nothing to publish: no file differs from the public repo"
        return report
    if push:
        git(clone, "push", "origin", "HEAD:main")
        report["pushed"] = True
        report["result"] = "published"
    else:
        report["result"] = "ready: committed in the clone, not pushed (run again with --push)"
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clone", required=True, help="a clean clone of mcp-tool-shop-org/readouts")
    ap.add_argument("--push", action="store_true", help="push to main when every step passes")
    ap.add_argument("--allow-delete", action="append", default=[], metavar="PATH",
                    help="a public path the export may delete (repeat); anything else halts")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    args = ap.parse_args(argv)
    try:
        report = publish(os.path.abspath(args.clone), args.push, args.allow_delete)
    except Halt as exc:
        report = {"result": "halted", "reason": str(exc), "pushed": False}
        print(json.dumps(report, indent=1) if args.json else f"HALT: {exc}")
        return 2
    if args.json:
        print(json.dumps(report, indent=1))
    else:
        print(report["result"])
        for k in ("internal", "last_published", "commit", "files_changed", "atlas"):
            if report.get(k) is not None:
                print(f"  {k}: {report[k]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
