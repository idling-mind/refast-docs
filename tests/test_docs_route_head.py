"""Per-route `<head>`: what a tab, a crawler and a link preview see for one page.

Why this test exists
--------------------
refast renders one static shell for every route, so before `docs/route_head.py` the
document served for `/docs/advanced/sessions` carried `<title>Refast Docs</title>`, the
site's description, and `canonical`/`og:url` naming the *root* — which tells a search
index that a hundred distinct pages are duplicates of one. `test_docs_shell.py` covers
what the shell always contains; this covers what each route has to say about itself, and
the two things that patching an HTML document can break: a duplicate tag where a
replacement was meant, and a response whose body no longer matches its `content-length`.
"""

import html
import json
import re

import pytest
from fastapi.testclient import TestClient

from docs import markdown_export
from docs.app import NAV_SECTIONS, SITE_DESCRIPTION, SITE_URL, app, ui
from docs.route_head import SITE_TITLE

NAV_ROUTES = sorted(
    page[1]
    for section in NAV_SECTIONS
    for group in (section["groups"] if "groups" in section else [section])
    for page in group["pages"]
)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _head(client: TestClient, route: str) -> str:
    response = client.get(route)
    assert response.status_code == 200, f"{route} is not served"
    return response.text.split("</head>")[0]


def _tag(head: str, pattern: str) -> str | None:
    match = re.search(pattern, head)
    return match.group(1) if match else None


@pytest.mark.parametrize("route", NAV_ROUTES)
def test_each_page_is_named_and_addressed_as_itself(route: str, client: TestClient) -> None:
    head = _head(client, route)
    title = html.unescape(_tag(head, r"<title>(.*?)</title>") or "")
    assert title == f"{markdown_export.find(route).title} — {SITE_TITLE}"
    assert _tag(head, r'<link rel="canonical" href="([^"]+)"') == SITE_URL + route
    assert _tag(head, r'<meta property="og:url" content="([^"]+)"') == SITE_URL + route


@pytest.mark.parametrize("route", NAV_ROUTES)
def test_patching_replaces_rather_than_stacking_tags(route: str, client: TestClient) -> None:
    """Two canonicals, or a site description beside a page one, is a coin toss."""
    head = _head(client, route)
    for pattern in (
        r'<link rel="canonical"',
        r'<meta name="description"',
        r'<meta property="og:title"',
        r'<meta property="og:url"',
        r"<title>",
    ):
        found = re.findall(pattern, head)
        assert len(found) == 1, f"{route} has {len(found)} matches for {pattern}"


def test_the_landing_page_keeps_the_site_own_identity(client: TestClient) -> None:
    """/ is the site, so it must not become one page among others."""
    head = _head(client, "/")
    assert _tag(head, r"<title>(.*?)</title>") == SITE_TITLE
    assert _tag(head, r'<link rel="canonical" href="([^"]+)"') == SITE_URL + "/"
    assert _tag(head, r'<meta property="og:type" content="([^"]+)"') == "website"


@pytest.mark.parametrize("route", NAV_ROUTES)
def test_description_is_the_page_rather_than_the_site(route: str, client: TestClient) -> None:
    """A page whose description is the site's says nothing, and `*session*` in a meta
    description is asterisks, not emphasis."""
    head = _head(client, route)
    description = _tag(head, r'<meta name="description" content="([^"]*)"') or ""
    assert description != SITE_DESCRIPTION, f"{route} describes the site, not itself"
    assert len(description) > 20, f"{route} describes itself with {description!r}"
    assert not re.search(r"[*_`]|]\(", description), f"{route}: {description!r} keeps markup"


def test_pages_advertise_their_markdown_mirror(client: TestClient) -> None:
    """`<route>.md` existing is no use if only this repository knows about it."""
    head = _head(client, "/docs/concepts/state")
    href = _tag(head, r'<link rel="alternate" type="text/markdown" href="([^"]+)"')
    assert href == SITE_URL + "/docs/concepts/state.md"
    mirror = client.get(href)
    assert mirror.status_code == 200
    assert mirror.headers["content-type"].startswith("text/markdown")


def test_structured_data_names_the_page_and_where_it_sits(client: TestClient) -> None:
    head = _head(client, "/docs/advanced/sessions")
    payload = json.loads(_tag(head, r'<script type="application/ld\+json">(.*?)</script>'))
    article, crumbs = payload["@graph"]
    assert article["@type"] == "TechArticle"
    assert article["headline"] == "Sessions"
    assert article["url"] == SITE_URL + "/docs/advanced/sessions"
    assert article["isPartOf"]["url"] == SITE_URL + "/"
    assert [item["name"] for item in crumbs["itemListElement"]] == ["Advanced", "Sessions"]


def test_the_body_the_shell_hydrates_from_survives_the_patch(client: TestClient) -> None:
    """Rewriting metadata must not disturb what refast's client boots from."""
    before = client.get("/").text
    after = client.get("/docs/concepts/state").text
    mount = re.compile(r"<body[\s\S]*")
    assert "refast-bootstrap" in after
    assert mount.search(before).group(0)[:400] == mount.search(after).group(0)[:400]
    assert "/docs/concepts/state" in ui.pages


@pytest.mark.parametrize(
    "route, header, value",
    [
        ("/sitemap.xml", "content-type", "application/xml"),
        ("/api/pages.json", "content-type", "application/json"),
        ("/llms.txt", "content-type", "text/markdown"),
    ],
)
def test_responses_that_are_not_pages_are_left_alone(
    route: str, header: str, value: str, client: TestClient
) -> None:
    response = client.get(route)
    assert response.status_code == 200
    assert response.headers[header].startswith(value)
    assert "<title>" not in response.text[:200]


def test_content_length_matches_the_document_actually_sent(client: TestClient) -> None:
    """The patched page is longer than the shell, so a stale header truncates it."""
    response = client.get("/docs/concepts/state")
    assert int(response.headers["content-length"]) == len(response.content)
    assert response.text.rstrip().endswith("</html>")


def test_an_unknown_route_is_not_claimed_by_a_page(client: TestClient) -> None:
    """refast answers unknown paths with the index shell; the patch must follow suit."""
    head = _head(client, "/docs/no-such-page")
    assert _tag(head, r"<title>(.*?)</title>") == SITE_TITLE


def test_the_websocket_still_connects_through_the_middleware(client: TestClient) -> None:
    """A base HTTP middleware sees only http scopes; assert that is what it does here."""
    with client.websocket_connect("/ws") as ws:
        assert ws is not None
