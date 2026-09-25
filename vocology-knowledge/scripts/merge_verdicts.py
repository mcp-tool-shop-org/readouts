#!/usr/bin/env python3
"""Deprecated shim — the merger is shared now.

Ten near-identical copies of the same script is the duplication the audits kept
flagging, so this one moved to shared/merge_verdicts.py and takes --kb.

    python ../shared/merge_verdicts.py --kb vocology-knowledge
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHARED = os.path.join(os.path.dirname(os.path.dirname(HERE)), "shared", "merge_verdicts.py")
sys.exit(subprocess.run(
    [sys.executable, SHARED, "--kb", "vocology-knowledge", *sys.argv[1:]]).returncode)
