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
