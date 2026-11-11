"""The machine-readable surfaces: `.md` mirrors, `/llms.txt`, `/llms-full.txt`, JSON.

Why this test exists
--------------------
refast draws every page in the browser, so `GET /docs/concepts/state` returns the same
shell for every route and a reader that cannot run JavaScript — a crawler, an LLM told
to go and read a page — receives no prose at all. ``docs/markdown_export.py`` gives
those readers text, and this test is what stops that text from quietly going stale or
empty: an endpoint that returns 200 and a page's worth of nothing would pass every
other check in this suite.

Each test here asserts one way the surface can rot:

- a page added to the sidebar, and missing from `/llms.txt`
- a mirror that serves the shell instead of the text
- `{{ demo_app }}` markers or playground labels leaking into a page's Markdown
- links inside exported text that lead to a route nobody registered
- `/api/search` answering with pages that have no readable mirror
"""

import re

import pytest
from fastapi.testclient import TestClient

from docs import markdown_export
from docs.app import NAV_SECTIONS, SITE_URL, app
from docs.markdown_export import corpus_delimiter

NAV_ROUTES = {
    page[1]
    for section in NAV_SECTIONS
    for group in (section["groups"] if "groups" in section else [section])
    for page in group["pages"]
}

#: How much text a mirror has to carry to be worth fetching. A page below this
#: exported its header and lost its body, which is what happens when the walker
#: mistakes prose for a live example.
MIN_BODY_CHARS = 300

#: llms-full.txt is for one-shot prompts. Past a few hundred KB it stops fitting in one.
FULL_CORPUS_BUDGET = 700_000


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _listed_urls(text: str) -> list[str]:
    """Every absolute URL this site wrote into a piece of exported text."""
    return re.findall(r"%s[^)\s\]]+" % re.escape(SITE_URL), text)


def test_llms_txt_lists_every_page_once_as_markdown(client: TestClient) -> None:
    """The index has to be the navigation, with every row pointing at text."""
    body = client.get("/llms.txt").text
    assert body.startswith("# ")
    assert "\n> " in body, "llms.txt wants a blockquote description of the site"

    listed = {url[: -len(".md")].removeprefix(SITE_URL) for url in _listed_urls(body) if url.endswith(".md")}
    assert NAV_ROUTES <= listed, "pages are missing from the index"
    assert len(listed) == len(NAV_ROUTES) + 1, "the index lists a page twice, or one that is not in the nav"

    html_pages = [
        url
        for url in _listed_urls(body)
        if re.match(rf"{re.escape(SITE_URL)}/docs", url) and not url.endswith(".md")
    ]
    assert not html_pages, f"rows that link to a shell instead of text: {html_pages}"


def test_llms_txt_describes_pages_rather_than_naming_them(client: TestClient) -> None:
    """`- [Rowing](…): Rowing` is a row that says nothing an agent can use."""
    body = client.get("/llms.txt").text
    thin = [
        label
        for label, _url, summary in re.findall(r"^- \[([^\]]+)\]\(([^)]+)\)(: .*)?$", body, re.MULTILINE)
        if (summary or "").lstrip(": ").strip() == label.strip()
    ]
    assert not thin, f"listed with no description: {thin}"


@pytest.mark.parametrize("route", sorted(NAV_ROUTES))
def test_page_mirror_serves_text_not_the_shell(route: str, client: TestClient) -> None:
    """The whole point: a URL that answers with the page's prose."""
    response = client.get(f"{route}.md")
    assert response.status_code == 200, f"{route}.md is missing"
    assert response.headers["content-type"].startswith("text/markdown")
    body = response.text
    assert 'id="root"' not in body, f"{route}.md served the JavaScript shell"
    assert body.startswith(f"# {markdown_export.find(route).title}"), f"{route}.md has no H1"
    assert len(body) > MIN_BODY_CHARS, f"{route}.md exports {len(body)} chars of a page"
    assert "**URL:**" in body and "**Section:**" in body, f"{route}.md lost its header"


def test_home_page_has_a_mirror(client: TestClient) -> None:
    """/` cannot take a `.md` suffix, so it gets a path of its own."""
    response = client.get("/index.md")
    assert response.status_code == 200
    assert response.text.startswith("# ")


def test_every_mirror_is_reachable_from_its_own_page(client: TestClient) -> None:
    """A surface nobody can discover is a surface nobody uses; the footer is the link."""
    response = client.get("/api/page", headers={"referer": f"{SITE_URL}/docs/concepts/state"})
    assert response.status_code == 200
    assert "/docs/concepts/state.md" in response.text, "no link to the mirror on the page"


@pytest.mark.parametrize("route", sorted(NAV_ROUTES))
def test_mirror_holds_nothing_the_reader_cannot_read(route: str) -> None:
    """Demo-app markers and half-written code fences are rendering failures, not prose."""
    page = markdown_export.find(route)
    assert "{{" not in page.markdown, f"{route} leaked a demo-app marker"
    fences = len(re.findall(r"^```", page.markdown, re.MULTILINE))
    assert fences % 2 == 0, f"{route} exports {fences} fence markers, so a block is unclosed"


def test_full_corpus_holds_every_page_exactly_once(client: TestClient) -> None:
    body = client.get("/llms-full.txt").text
    assert len(body) < FULL_CORPUS_BUDGET, f"llms-full.txt is {len(body):,} chars"
    routes = {page.route for page in markdown_export.pages()}
    assert body.count("<!-- =") == len(routes), "a page is missing, or appears twice"
    for route in routes:
        assert corpus_delimiter(route) in body, f"{route} is missing from the corpus"


def test_pages_json_is_an_index_a_program_can_plan_with(client: TestClient) -> None:
    payload = client.get("/api/pages.json").json()
    assert payload["count"] == len(markdown_export.pages())
    assert payload["site"] == SITE_URL
    assert payload["refast_version"]
    routes = {entry["route"] for entry in payload["pages"]}
    assert NAV_ROUTES <= routes and "/" in routes, "the index is not the navigation"
    for entry in payload["pages"][:10]:
        assert entry["title"] and entry["section"] and entry["summary"]
        assert entry["approx_tokens"] > 0 and entry["chars"] > MIN_BODY_CHARS
        assert client.get(entry["markdown_url"].removeprefix(SITE_URL)).status_code == 200


def test_search_api_ranks_and_links_to_text(client: TestClient) -> None:
    """/api/search is how an agent finds a page without downloading all of them."""
    payload = client.get("/api/search", params={"q": "styling"}).json()
    assert payload["results"], "a query with obvious matches returned nothing"
    assert payload["results"][0]["route"] == "/docs/concepts/styling"
    assert payload["pages_indexed"] == len(NAV_ROUTES)
    for hit in payload["results"]:
        assert client.get(hit["markdown_url"].removeprefix(SITE_URL)).status_code == 200


def test_search_api_says_so_when_nothing_matches(client: TestClient) -> None:
    payload = client.get("/api/search", params={"q": "zzqqx"}).json()
    assert payload["count"] == 0 and payload["results"] == []


def test_every_mirror_holds_a_sentence_about_itself() -> None:
    """`Page.summary` is what `/llms.txt` and `/api/pages.json` describe a page with."""
    thin = [page.route for page in markdown_export.pages() if not page.summary]
    assert not thin, f"no first sentence to quote: {thin}"


def test_links_inside_exported_text_lead_somewhere() -> None:
    """A mirror is fetched standalone, so its links have to be absolute and real."""
    registered = _registered_routes()
    for route in NAV_ROUTES:
        markdown = markdown_export.find(route).markdown
        assert not re.search(r"\]\(/(?!/)", markdown), f"{route} kept a site-relative link"
        for url in _listed_urls(markdown):
            target = url.removeprefix(SITE_URL).split("#")[0]
            assert target in registered or target.endswith(".md"), f"{route} links to {url}"


def test_robots_txt_points_at_the_index(client: TestClient) -> None:
    body = client.get("/robots.txt").text
    assert "/llms.txt" in body, "robots.txt is the one file both crawlers and harnesses read"
    assert body.rstrip().endswith("/sitemap.xml"), "the Sitemap line has to stay last"


def test_markdown_paths_are_predictable() -> None:
    """The convention is a documented promise: any page URL plus `.md`."""
    assert markdown_export.markdown_href("/docs/concepts/state") == "/docs/concepts/state.md"
    assert markdown_export.markdown_href("/") == "/index.md"
    assert markdown_export.knows("/docs/concepts/state")
    assert not markdown_export.knows("/nope")


def _registered_routes() -> set[str]:
    """Routes refast serves, so an exported link can be checked against them."""
    from docs.app import ui

    pages = getattr(ui, "pages", None)
    pages = pages() if callable(pages) else pages
    return {route for route in dict(pages or {}) if "{" not in route}
