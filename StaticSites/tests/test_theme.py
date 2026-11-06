"""The standalone shell shares navigation while keeping its assets embedded."""
from html.parser import HTMLParser

from staticsites.theme import embed_site_theme


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))
        if tag == "img":
            self.images.append(dict(attrs))


def test_portable_header_uses_shared_assets_and_absolute_navigation():
    html = embed_site_theme('<html><head><title>Example</title></head><body><main>Chart</main></body></html>')
    parsed = Links()
    parsed.feed(html)
    assert '<title>Example</title>' in html
    assert 'id="main-content"' in html
    assert '--site-accent:' in html
    assert parsed.images[0]['src'].startswith('data:image/svg+xml;base64,')
    assert [link['href'] for link in parsed.links] == [
        '#main-content', 'https://tianle91.com/', 'https://tianle91.com/apps/',
        'https://tianle91.com/interactive/', 'https://tianle91.com/writing/',
        'https://tianle91.com/about.html',
    ]
    assert [link['href'] for link in parsed.links if link.get('aria-current') == 'page'] == [
        'https://tianle91.com/interactive/']
