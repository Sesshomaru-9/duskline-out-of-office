#!/usr/bin/env python3
"""Duskline Out of Office — make.fun bounty
u-hamsyh-funniest-one-line-out-of-office-reply-5490c1c8.

Writes one funny one-line out-of-office reply (1-160 chars) to
$MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic, Python 3.13 standard
library only, no network, no randomness, no arguments.

Safety rules:
- Never writes into the repository directory: if the resolved output
  directory is the repo dir or inside it, refuse silently and exit 0.
- If MAKEFUN_OUTPUT_DIR is unset or empty, fall back to a fresh
  temporary directory outside the repo.
- Never raises: any failure exits 0 without writing anything.
"""

import os
import sys
import tempfile

# The entry, exactly 111 characters. The apostrophe is U+2019 and the
# dash is U+2014, written as escapes so the source stays plain ASCII.
# Joke idea: the auto-reply itself — the thing doing the talking — has
# filed for a promotion, because it does more work than its owner. The
# line stays a real away message (it opens "I'm out of the office"),
# the laugh lands on the first read, and the turn is fresh: no beach,
# no inbox, no "limited email access". Every word earns its place.
ENTRY = (
    "I\u2019m out of the office, and my autoresponder has officially "
    "filed for a promotion \u2014 it does more work than I do."
)

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def _inside_repo(path):
    """True if path resolves to the repo dir or anywhere inside it."""
    try:
        resolved = os.path.realpath(path)
    except Exception:
        return True
    repo = os.path.realpath(REPO_DIR)
    return resolved == repo or resolved.startswith(repo + os.sep)


def _valid(text):
    """Gate: 1-160 chars, not only whitespace, a single line, UTF-8.

    The bounds come from the bounty spec: the reply must be a single
    line of 1-160 characters, so a stray newline or an over-long draft
    is rejected before anything is written.
    """
    if not 1 <= len(text) <= 160:
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _output_dir():
    """$MAKEFUN_OUTPUT_DIR, or a fresh temp dir outside the repo."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    if not out_dir:
        out_dir = tempfile.mkdtemp(prefix="duskline-out-of-office-")
    return out_dir


def _write_and_verify(target, text):
    """Write text with no trailing newline, then read it back and
    confirm it matches byte-for-byte; remove it again on mismatch."""
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(target, "r", encoding="utf-8") as handle:
        back = handle.read()
    if back != text:
        try:
            os.remove(target)
        except Exception:
            pass
        return False
    return True


def main():
    try:
        if not _valid(ENTRY):
            return 0
        out_dir = _output_dir()
        if _inside_repo(out_dir):
            return 0
        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        if _inside_repo(target):
            return 0
        _write_and_verify(target, ENTRY)
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
