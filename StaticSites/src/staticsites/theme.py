"""Embed the parent site's navigation and theme into portable tool pages."""
from base64 import b64encode
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[3]


def embed_site_theme(page):
    """Use the same header and CSS as Jekyll, with no runtime asset requests."""
    header = (SITE_ROOT / "_includes/site-header.html").read_text(encoding="utf-8")
    style = (SITE_ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    mark = (SITE_ROOT / "assets/apps/tchdevs.svg").read_bytes()
    logo = "data:image/svg+xml;base64," + b64encode(mark).decode("ascii")
    header = header.replace('src="/assets/apps/tchdevs.svg"', f'src="{logo}"')
    header = header.replace('href="/interactive/"', 'href="/interactive/" aria-current="page"')
    header = header.replace('href="/', 'href="https://tianle91.com/')
    page = page.replace("</head>", f"<style>{style}</style>\n</head>", 1)
    page = page.replace("<body>", f'<body class="site-tool">\n{header}', 1)
    return page.replace("<main", '<main id="main-content" tabindex="-1"', 1)
