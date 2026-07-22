#!/usr/bin/env python3
"""Regenerate index.md's Interactive list from the StaticSites submodule.

StaticSites publishes a machine-readable manifest at StaticSites/sites.json
(slug, title, description, output) — see tianle91/StaticSites#2. This script is
the deterministic replacement for the old hand-driven "link every site" skill:
it rewrites the block between the STARTMARK/ENDMARK comments in index.md so the
homepage always matches whatever sites the pinned submodule builds.

Usage:
  scripts/sync_staticsites.py                     # regenerate from current submodule
  scripts/sync_staticsites.py --update-submodule  # bump submodule to latest main, then regenerate
  scripts/sync_staticsites.py --check             # verify only; nonzero exit if stale (for CI)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "index.md"
MANIFEST = REPO / "StaticSites" / "sites.json"
SUBMODULE = REPO / "StaticSites"

STARTMARK = "<!-- staticsites:start — generated from StaticSites/sites.json by scripts/sync_staticsites.py; do not edit by hand -->"
ENDMARK = "<!-- staticsites:end -->"


def render(sites: list[dict]) -> str:
    """Build the generated block (between, not including, the markers)."""
    lines = []
    for s in sites:
        lines.append(f"- [{s['title']}](/StaticSites/{s['output']})")
        lines.append(f"  — {s['description']}")
    n = len(sites)
    count = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
             6: "six", 7: "seven", 8: "eight", 9: "nine"}.get(n, str(n))
    lines.append("")
    lines.append(f"Source for all {count}: "
                 "[github.com/tianle91/StaticSites](https://github.com/tianle91/StaticSites)")
    return "\n".join(lines)


def splice(text: str, block: str) -> str:
    """Replace the content between the markers with `block`."""
    if STARTMARK not in text or ENDMARK not in text:
        sys.exit("index.md is missing the staticsites markers; add them once by hand.")
    pre, rest = text.split(STARTMARK, 1)
    _, post = rest.split(ENDMARK, 1)
    return f"{pre}{STARTMARK}\n{block}\n{ENDMARK}{post}"


def verify(sites: list[dict]) -> list[str]:
    """Cross-check the manifest against what's actually built. Return problems."""
    problems = []
    manifest_outputs = {s["output"] for s in sites}
    for s in sites:
        if not (SUBMODULE / s["output"]).is_file():
            problems.append(f"manifest lists {s['output']} but the file is missing")
    # catch drift the other way: a built site absent from the manifest
    built = subprocess.run(
        ["git", "-C", str(SUBMODULE), "ls-files", "*/output/*.html"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    for f in built:
        if f not in manifest_outputs:
            problems.append(f"built site {f} is not in sites.json")
    return problems


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--update-submodule", action="store_true",
                    help="bump the StaticSites submodule to latest main before regenerating")
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit nonzero if index.md is stale or verification fails")
    args = ap.parse_args()

    if args.update_submodule:
        if args.check:
            sys.exit("--update-submodule and --check are mutually exclusive")
        subprocess.run(["git", "submodule", "update", "--remote", str(SUBMODULE)], check=True)

    sites = json.loads(MANIFEST.read_text())

    problems = verify(sites)
    if problems:
        print("Verification failed:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)

    current = INDEX.read_text()
    updated = splice(current, render(sites))

    if args.check:
        if updated != current:
            sys.exit("index.md is out of date; run scripts/sync_staticsites.py")
        print(f"index.md is up to date ({len(sites)} sites).")
        return

    if updated == current:
        print(f"index.md already current ({len(sites)} sites); nothing to do.")
    else:
        INDEX.write_text(updated)
        print(f"index.md regenerated with {len(sites)} sites.")


if __name__ == "__main__":
    main()
