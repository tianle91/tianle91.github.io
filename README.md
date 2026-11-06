# [tianle91.github.io](https://tianle91.com)

The personal site at **tianle91.com**, published with
[GitHub Pages and Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll).
Pushing to `master` publishes; there is no build step to run yourself.

Developer/agent notes live in [AGENTS.md](AGENTS.md).

## Writing a blog post

Add a Markdown file to [`_posts/`](_posts/) named `YYYY-MM-DD-Title.md`, starting
with front matter:

```markdown
---
layout: post
title:  "Your Title"
tags: ads
hidden: true
---

Your post.
```

- **`hidden: true` keeps a post off the front page.** [index.md](index.md) only lists
  posts where `hidden` is absent or false, so a draft is safe to commit. Delete the
  line when you want it to appear.
- `tags` is optional and free-form.
- `excerpt_separator: <!--more-->` lets you control where the front-page blurb ends.

The post is live a minute or two after you push.

## Pages that aren't blog posts

- [about.md](about.md), [publications.md](publications.md) — edit directly.
- [index.md](index.md) — the front page with featured apps, projects, and writing.
- [apps.html](apps.html) — app portfolio, using metadata in `_data/apps.json`.
- [interactive.md](interactive.md) — generated project directory.
- [writing.html](writing.html) — visible blog posts.
- `_layouts/`, `_includes/`, and `assets/css/site.css` — shared theme and navigation.
- `assets/` — images. Reference them as `/assets/...`.

## Publishing an updated map or chart

The maps, charts, source code, datasets and generated outputs live in
[StaticSites/](StaticSites/) in this repository. A normal clone includes everything;
there is no submodule to initialize or separate pointer PR to merge.

From `StaticSites/`, edit the project and run its build and tests as described in
[StaticSites/README.md](StaticSites/README.md). Commit the source, data and generated
outputs together. From this repository's root:

```bash
make sync      # regenerate the project directory after metadata/project changes
make check     # directory and post checks, plus all static project tests/builds
```

Open one PR in this repository. Merging to `master` publishes the committed HTML
through the existing legacy GitHub Pages builder. The checks workflow tests and
builds static projects from committed inputs; it does not refresh datasets or
deploy the site. After publication, run `make verify` to check the Pages build
and every published map/chart URL.

Existing URLs stay at `/StaticSites/<project>/output/<project>.html`. A new
project belongs in `StaticSites/`; use its scaffolder, edit `site.toml`, run
`make manifest` there, then `make sync` here. `make` lists the root targets.

The former [StaticSites repository](https://github.com/tianle91/StaticSites) remains
available for historical issues and PRs. Its Git history was imported without
rewriting the original commits. New work belongs here.
