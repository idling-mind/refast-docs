"""What the initial HTML document contains, before any component tree renders.

Why this test exists
--------------------
``GET /`` returns a shell built by refast (``refast.assets.render_html_shell``)
and nothing else: pages are drawn client-side afterwards. That shell is the only
part of the site a browser tab, a link preview, or a crawler sees first, and
until now nothing checked it. The site shipped ``favicon="📖"`` for example,
which refast emits verbatim as ``<link rel="icon" href="📖">`` -- a request for a
file called "📖", while a real ``public/favicon.ico`` sat in the repository
unserved.
"""

import re

import pytest
from fastapi.testclient import TestClient

from docs.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


FAVICON_RE = re.compile(r'<link rel="icon" href="(?P<href>[^"]+)">')
TITLE_RE = re.compile(r"<title>(?P<title>[^<]*)</title>")


def _shell(client: TestClient) -> str:
    response = client.get("/")
    assert response.status_code == 200
    return response.text


def test_favicon_is_linked_and_served(client: TestClient) -> None:
    """An emoji in href is not a favicon; the file has to exist and be reachable."""
    href = FAVICON_RE.search(_shell(client)).group("href")
    assert href.startswith("/"), f"{href!r} is a glyph, not a URL"  # refast emits href verbatim
    response = client.get(href)
    assert response.status_code == 200, f"{href} is linked but not served"
    assert len(response.content) > 64, f"{href} is not an icon"


def test_document_title_names_the_site(client: TestClient) -> None:
    """refast takes <title> from RefastApp(title=...), which tab bars and history use."""
    title = TITLE_RE.search(_shell(client)).group("title")
    assert "refast" in title.lower() and len(title) < 60, title


def _urls(xml: str) -> set[str]:
    return set(re.findall(r"<loc>([^<]+)</loc>", xml))


def test_robots_txt_offers_a_sitemap(client: TestClient) -> None:
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "User-agent: *" in response.text
    assert response.text.rstrip().endswith("/sitemap.xml"), response.text


def test_sitemap_covers_every_registered_page(client: TestClient) -> None:
    """A page missing from the sitemap is a page nothing will ever find."""
    from docs.app import SITE_URL, ui

    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")

    expected = {SITE_URL + ("" if route == "/" else route) for route in ui.pages if "{" not in route}
    assert _urls(response.text) == expected
    assert response.text.count("<url>") == len(expected)


def test_link_previews_get_a_description(client: TestClient) -> None:
    """The shell is the only thing a crawler or a chat preview ever sees."""
    from docs.app import SITE_URL

    shell = _shell(client)
    assert 'name="description"' in shell
    assert 'property="og:title"' in shell and 'property="og:description"' in shell
    assert f'property="og:url" content="{SITE_URL}/"' in shell
    assert f'rel="canonical" href="{SITE_URL}/"' in shell
    # One shell serves every route, so only the root can be canonical. Per-page
    # titles and descriptions need server rendering; see docs/TODO.md.
    assert shell.count("rel=\"canonical\"") == 1


def test_head_tags_are_well_formed(client: TestClient) -> None:
    """A stray quote or angle bracket in a meta tag truncates the rest of <head>."""
    head = _shell(client).split("</head>")[0]
    tags = re.findall(r"<(?:meta|link)\b[^>]*>", head)
    assert tags, "no metadata tags reached the head"
    for tag in tags:
        for value in re.findall(r'content="([^"]*)"', tag):
            assert value.strip(), f"empty content attribute: {tag}"
            assert "<" not in value and ">" not in value, f"unescaped tag in {tag}"
