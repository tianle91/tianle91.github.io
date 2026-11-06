#!/usr/bin/env python3
"""Regenerate interactive.md's project directory from StaticSites/sites.json.

Usage:
  scripts/sync_staticsites.py          # regenerate from the committed manifest
  scripts/sync_staticsites.py --check  # verify only; fail if stale or incomplete
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DIRECTORY = REPO / "interactive.md"
MANIFEST = REPO / "StaticSites" / "sites.json"
STATIC_SITES = REPO / "StaticSites"

STARTMARK = "<!-- staticsites:start — generated from StaticSites/sites.json by scripts/sync_staticsites.py; do not edit by hand -->"
ENDMARK = "<!-- staticsites:end -->"


def render(sites: list[dict]) -> str:
    """Build the generated block (between, not including, the markers)."""
    groups = {"Maps": [], "Economics & Finance": [], "Other projects": []}
    finance = {"canada-mortgage-stress", "fcf-macro-indicators",
               "margin-sp500-m2-visualization", "us-canada-yield-curves"}
    for site in sites:
        slug = site["output"].split("/", 1)[0]
        if slug in finance:
            group = "Economics & Finance"
        elif slug.endswith("-map") or slug == "union-station-transit-isochrone":
            group = "Maps"
        else:
            group = "Other projects"
        groups[group].append(site)
    lines = []
    for title, projects in groups.items():
        if not projects:
            continue
        lines.extend([f"## {title}", ""])
        for s in projects:
            lines.append(f"- [{s['title']}](/StaticSites/{s['output']})")
            lines.append(f"  — {s['description']}")
        lines.append("")
    n = len(sites)
    count = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
             6: "six", 7: "seven", 8: "eight", 9: "nine"}.get(n, str(n))
    lines.append("")
    lines.append(f"Source for all {count}: "
                 "[StaticSites source](https://github.com/tianle91/tianle91.github.io/tree/master/StaticSites)")
    return "\n".join(lines)


def splice(text: str, block: str) -> str:
    """Replace the content between the markers with `block`."""
    if STARTMARK not in text or ENDMARK not in text:
        sys.exit("interactive.md is missing the staticsites markers; add them once by hand.")
    pre, rest = text.split(STARTMARK, 1)
    _, post = rest.split(ENDMARK, 1)
    return f"{pre}{STARTMARK}\n{block}\n{ENDMARK}{post}"


def verify(sites: list[dict]) -> list[str]:
    """Cross-check the manifest against what's actually built. Return problems."""
    problems = []
    manifest_outputs = {s["output"] for s in sites}
    for s in sites:
        if not (STATIC_SITES / s["output"]).is_file():
            problems.append(f"manifest lists {s['output']} but the file is missing")
    # catch drift the other way: a built site absent from the manifest
    built = subprocess.run(
        ["git", "-C", str(STATIC_SITES), "ls-files", "*/output/*.html"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    for f in built:
        if f not in manifest_outputs:
            problems.append(f"built site {f} is not in sites.json")
    return problems


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit nonzero if interactive.md is stale or verification fails")
    args = ap.parse_args()

    sites = json.loads(MANIFEST.read_text())

    problems = verify(sites)
    if problems:
        print("Verification failed:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)

    current = DIRECTORY.read_text()
    updated = splice(current, render(sites))

    if args.check:
        if updated != current:
            sys.exit("interactive.md is out of date; run scripts/sync_staticsites.py")
        print(f"interactive.md is up to date ({len(sites)} sites).")
        return

    if updated == current:
        print(f"interactive.md already current ({len(sites)} sites); nothing to do.")
    else:
        DIRECTORY.write_text(updated)
        print(f"interactive.md regenerated with {len(sites)} sites.")


if __name__ == "__main__":
    main()
