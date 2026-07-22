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
- [index.md](index.md) — the front page: the nav links, the **Interactive** list, and
  the Misc section.
- `assets/` — images. Reference them as `/assets/...`.

## Publishing an updated map or chart

The interactive maps and plots in the **Interactive** section are built in the separate
[StaticSites](https://github.com/tianle91/StaticSites) repo and pulled in here as a
submodule. This site never rebuilds them; it serves the HTML that StaticSites has
already committed.

To publish a change to one of them: commit and push it in StaticSites first, then in
this repo point at the new version.

```bash
git submodule update --remote StaticSites
git commit -am 'bump StaticSites'
git push
```

To add a *new* map to the front page, do the same, then add a bullet to the
**Interactive** list in [index.md](index.md).

> **StaticSites must stay a public repo.** This site uses the legacy GitHub Pages
> builder, which fetches submodules anonymously over HTTPS. If StaticSites is made
> private, every build of this site fails and the maps 404.
