#!/usr/bin/env python3
"""Duskline Out of Office — make.fun bounty u-hamsyh-funniest-one-line-out-of-office-reply-5490c1c8.

Writes one funny one-line out-of-office reply (1-160 chars) to
$MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic, Python 3.13 standard
library only, no network, no randomness.

Safety rules:
- Never writes into the repository directory: if the resolved output
  directory is the repo dir or inside it, refuse and exit 0.
- If MAKEFUN_OUTPUT_DIR is unset or empty, fall back to a fresh
  temporary directory outside the repo.
- Never raises: any failure exits 0 without writing anything.
"""

import os
import sys
import tempfile

ENTRY = "I\u2019m out of the office, and my autoresponder has officially filed for a promotion \u2014 it does more work than I do."
# Joke idea: the auto-reply itself — the thing doing the talking — has
# filed for a promotion, because it does more work than its owner. The
# line stays a real away message (it opens "I'm out of the office"),
# the laugh lands on the first read, and the turn is fresh: no beach,
# no inbox, no "limited email access". Every word earns its place.

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def _is_in_repo(path):
    """True if path resolves to the repo dir or anywhere inside it."""
    try:
        resolved = os.path.realpath(path)
    except Exception:
        return True
    repo = os.path.realpath(REPO_DIR)
    return resolved == repo or resolved.startswith(repo + os.sep)


def main():
    try:
        if not 1 <= len(ENTRY) <= 160:
            return 0
        if not ENTRY.strip():
            return 0
        if "\n" in ENTRY or "\r" in ENTRY:
            return 0
        ENTRY.encode("utf-8")

        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
        if not out_dir:
            out_dir = tempfile.mkdtemp(prefix="duskline-out-of-office-")
        if _is_in_repo(out_dir):
            return 0

        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        if _is_in_repo(target):
            return 0
        with open(target, "w", encoding="utf-8", newline="") as handle:
            handle.write(ENTRY)
        with open(target, "r", encoding="utf-8") as handle:
            back = handle.read()
        if back != ENTRY:
            try:
                os.remove(target)
            except Exception:
                pass
            return 0
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
