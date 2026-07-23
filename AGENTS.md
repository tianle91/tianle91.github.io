# AGENTS.md

Developer- and agent-facing notes for this repo. Humans writing posts or administering
the site: see [README.md](README.md).

## What this repo is

A zero-config Jekyll site on the **legacy** GitHub Pages builder — no `Gemfile`,
nothing to install. GitHub builds it server-side from `master` at the repo root.
Verify with:

```bash
gh api repos/tianle91/tianle91.github.io/pages   # build_type: legacy, source: master /
```

Do not add a `Gemfile`, a Pages **build/deploy** workflow, or a local build step
without a reason to leave the zero-config setup — the tradeoff is that the constraints
below are fixed. Two things that look like a build but aren't: `Makefile` only wraps
submodule/index chores and checks (`make` lists them), and
`.github/workflows/checks.yml` is a plain CI **check** that calls those same targets.
Neither builds or deploys the site, so `build_type` stays `legacy`. Keeping both
non-deploying is the line not to cross.

Layout: `_posts/` (blog), `_config.yml` (only sets the GA property), `index.md`,
`about.md`, `publications.md`, `assets/`, `CNAME` (`tianle91.com`), and the
`StaticSites/` submodule.

## Clone with submodules

```bash
git clone --recurse-submodules https://github.com/tianle91/tianle91.github.io.git
```

A plain clone leaves `StaticSites/` empty and every map link 404s locally. Fix an
existing clone with `git submodule update --init`.

## The StaticSites submodule

`StaticSites/` is a gitlink to [tianle91/StaticSites](https://github.com/tianle91/StaticSites),
pinned to a commit. That repo builds several self-contained sites and commits each one's
`output/<project>.html`; this site just serves those files. The links in
[index.md](index.md) point at the submodule's real paths
(`/StaticSites/<project>/output/<project>.html`) because files inside a submodule can't
be given Jekyll front matter from here, so they can't be given prettier permalinks
without wrapper pages.

The **Interactive** list in [index.md](index.md) is generated, not hand-edited: the
block between the `<!-- staticsites:start -->` / `<!-- staticsites:end -->` markers is
rewritten by [scripts/sync_staticsites.py](scripts/sync_staticsites.py) from the
submodule's `StaticSites/sites.json` manifest. To pull new/renamed sites and refresh the
list in one step:

```bash
make update    # python3 scripts/sync_staticsites.py --update-submodule
make publish   # the above, then commit + push
make check     # what CI runs: --check plus the post-filename guard
```

The script also verifies every manifest link resolves and flags any built site missing
from the manifest, so drift can't slip through. Edit the site titles/blurbs in
StaticSites (each project's `pyproject.toml`), not here.

Two constraints the legacy builder imposes — both will silently break the site:

- **The submodule URL must be public HTTPS.** The legacy builder fetches submodules
  anonymously; an SSH or `git://` URL in `.gitmodules`, or making StaticSites private,
  fails the build.
- **Nothing here rebuilds StaticSites.** Its Python source, `Makefile`s, and `uv.lock`
  get copied into the published site as inert static files. That is harmless — no
  `_config.yml` `exclude` is needed — but it means editing files under `StaticSites/`
  from this repo is never the right move. Change them in StaticSites, push, then bump
  the pointer here (`make update`).

## Gotchas

- **Every `.md` file here is Liquid-rendered, even without YAML front matter** — the
  build enables `jekyll-optional-front-matter`. That is why [index.md](index.md)'s
  {% raw %}`{% for post in site.posts %}`{% endraw %} loop renders despite having no front
  matter; don't "fix" that. It also means **this file is rendered**: any Liquid tag you
  write in these docs, even inside backticks or a fenced block, is parsed, and an
  unbalanced one fails the whole site build. Wrap literal tags in a Liquid `raw` block
  (and note you cannot nest one inside another, so document `raw` itself in prose).
- The front-page loop skips posts with `hidden: true`, which most posts currently set.
  A post that doesn't show up is usually hidden, not broken.
- `resume.html` is a `<meta http-equiv="refresh">` stub to a Google Doc, not a page.

## Verifying a change

There is no local build, so verify against the deployed site. After pushing to `master`:

```bash
make verify   # Pages build status, then every map in sites.json over HTTP
```

Expect `built` on your commit with no error, and `200` for every map. To confirm
a submodule change will build *before* pushing, reproduce the builder's anonymous fetch:

```bash
git clone --recurse-submodules -c credential.helper= \
  https://github.com/tianle91/tianle91.github.io.git /tmp/pages-check
```
