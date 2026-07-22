# [tianle91.github.io](https://tianle91.github.io)

Depends on [github pages and jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll)

## StaticSites submodule

The interactive maps and plots linked from `index.md` are served straight out of the
[StaticSites](https://github.com/tianle91/StaticSites) submodule, so clone with:

```bash
git clone --recurse-submodules https://github.com/tianle91/tianle91.github.io.git
```

To publish an updated map: commit and push in StaticSites first, then bump the pointer here.

```bash
git submodule update --remote StaticSites
git commit -am 'bump StaticSites'
```

StaticSites must stay public — this site uses the legacy GitHub Pages build, which
fetches submodules anonymously over HTTPS and fails on a private one.
