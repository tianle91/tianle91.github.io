---
name: sync-staticsites
description: Bump the StaticSites submodule to the latest main and ensure index.md links every built site. Use when asked to "pull the latest StaticSites", update the maps, refresh the submodule, or make sure all interactive sites are linked on tianle91.github.io.
---

# Sync StaticSites and link every site

Keep the `StaticSites/` submodule current and guarantee that the **Interactive**
section of [index.md](../../index.md) links to every site StaticSites builds.
StaticSites gains new sites over time; this skill catches ones that were added
upstream but never linked here.

Background on the submodule and the legacy Pages constraints is in
[AGENTS.md](../../AGENTS.md) — read it if anything below is surprising.

## Steps

1. **Pull the latest submodule pointer.** From the repo root:

   ```bash
   git submodule update --remote StaticSites
   git submodule status   # note the new commit; leading '+' means the pointer moved
   ```

2. **Enumerate every built site.** Each project commits `output/<project>.html`:

   ```bash
   git -C StaticSites ls-files '*/output/*.html'
   ```

3. **Make index.md link all of them.** Each link in the Interactive list uses the
   submodule's real path, `/StaticSites/<project>/output/<project>.html` (see the
   AGENTS.md note on why these aren't prettier permalinks). For any built site not
   yet present, add a bullet with a one-line description — pull the wording from
   that project's `StaticSites/<project>/README.md` or the StaticSites root
   `README.md` table. Keep the "Source for all N" line's count in sync.

4. **Verify — every link resolves, and nothing is unlinked:**

   ```bash
   # linked paths point at real files
   grep -oE '/StaticSites/[^)]*\.html' index.md | while read p; do
     [ -f ".$p" ] && echo "OK   $p" || echo "MISS $p"; done
   # no built site is missing from index.md
   for f in $(git -C StaticSites ls-files '*/output/*.html'); do
     grep -q "$f" index.md || echo "UNLINKED: $f"; done
   ```

   Expect all `OK` and zero `UNLINKED`. Also update any stale site-count
   references in AGENTS.md (the "builds N sites" line and the verify loop's map
   list) if the number changed.

5. **Commit and open a PR** on a feature branch (not `master`), staging the
   `StaticSites` gitlink alongside the doc edits:

   ```bash
   git add StaticSites index.md AGENTS.md
   ```

## Notes

- Only the submodule *pointer* changes here — never edit files under
  `StaticSites/` from this repo (they're inert copies). Change those in the
  StaticSites repo, push, then re-run this skill to bump the pointer.
- The final 200-check for the live maps only runs against the deployed site
  after merge; AGENTS.md's "Verifying a change" section has that `curl` loop.
