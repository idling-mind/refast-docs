"""The search palette has to find prose, not just page titles.

Why this test exists
--------------------
``⌘K`` used to compare the query against the sidebar labels, so the only
questions it could answer were ones whose wording the reader had already
guessed: searching "save_prop" returned nothing, because no page is called
"save_prop". ``docs/search.py`` indexes the text of every page instead, and this
test holds it to that -- including the cmdk detail that makes server-side results
survive the palette's client-side filter.
"""

import pytest
from fastapi.testclient import TestClient

from docs import search
from docs.app import NAV_SECTIONS, app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

NAV_ROUTES = {
    page[1]
    for section in NAV_SECTIONS
    for group in (section["groups"] if "groups" in section else [section])
    for page in group["pages"]
}


def _best(query: str) -> str | None:
    hits = search.search(query, limit=1)
    return hits[0].route if hits else None


def test_index_covers_every_page_in_the_navigation() -> None:
    """A page reachable from the sidebar must be findable by its content."""
    assert set(search.routes()) == NAV_ROUTES, "the index and the sidebar disagree"
    assert len(search.routes()) == len(set(search.routes())), "routes are indexed twice"


@pytest.mark.parametrize("route", sorted(NAV_ROUTES))
def test_every_page_contributes_prose(route: str) -> None:
    """Catch pages whose text moved somewhere the extractor cannot read."""
    size = dict(search.coverage())[route]
    assert size > 400, f"{route} contributes only {size} characters to the index"


def test_finds_a_term_that_appears_in_no_title() -> None:
    """The point of the exercise: body text, not labels."""
    query = "save_prop"
    hits = search.search(query, limit=5)
    assert hits, f"nothing found for {query!r}, so the index is not covering page bodies"
    assert all(query.lower() not in hit.title.lower() for hit in hits), (
        "results came from titles; a titles-only index would pass this too"
    )


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("rate limit", "/docs/advanced/security"),
        ("echarts", "/docs/extensions/echarts"),
        ("pagination", "/docs/components/pagination"),
        ("sessionStorage", "/docs/advanced/sessions"),
    ],
)
def test_ranking_puts_the_documenting_page_first(query: str, expected: str) -> None:
    assert _best(query) == expected, f"{query!r} ranked {search.search(query, limit=3)}"


def test_prefix_of_a_word_still_matches() -> None:
    """Readers type stems; an identifier-shaped index should cope."""
    assert _best("pagin") == "/docs/components/pagination"


def test_queries_with_no_match_return_nothing() -> None:
    assert search.search("") == []
    assert search.search("   ") == []
    assert search.search("qqzzxwvnotaterm") == []


def test_snippet_is_prose_not_a_code_sample() -> None:
    """A preview that opens with an import line tells the reader nothing."""
    for hit in search.search("sessionStorage", limit=5):
        snippet = hit.snippet.strip()
        assert not snippet.startswith(("```", "python", "from ", "import ", "<")), hit.route
        assert "```" not in snippet


def _palette(open_: bool = True) -> list[dict]:
    """The rendered nodes of the search dialog, the way a page would emit them."""
def _palette(open_: bool = True) -> list[dict]:
    """The rendered nodes of the search dialog, the way a page would emit them."""
    from refast import Context

    import docs.app as app

    ctx = Context()
    ctx.state["search_open"] = open_
    return _walk(app._build_search_dialog(ctx, "/docs/components/textarea").render())


def _walk(node, seen=None) -> list[dict]:
    seen = [] if seen is None else seen
    if isinstance(node, dict):
        seen.append(node)
        for child in node.get("children") or []:
            _walk(child, seen)
    elif isinstance(node, list):
        for child in node:
            _walk(child, seen)
    return seen


def _items(nodes: list[dict]) -> list[tuple[str, str]]:
    """(label, value) for every palette row; the label renders, the value scores."""
    return [
        ((n.get("children") or [""])[0], str(n["props"].get("value", "")))
        for n in nodes
        if n.get("type") == "CommandItem"
    ]


def test_every_palette_row_says_which_section_it_is_in() -> None:
    """Without the section, "Styling" and "Styling" in another group are identical.

    cmdk gives a row one line of text, so the section rides in the label; the
    results page has room to put it on the right and add a snippet.
    """
    rows = [label for label, _value in _items(_palette())]
    assert any(label.endswith("— Core Concepts") for label in rows), sorted(rows)[:5]
    assert all("—" in label for label in rows if not label.startswith("Search")), sorted(rows)[:5]


def test_palette_rows_score_against_page_text_not_just_titles() -> None:
    """cmdk filters locally over each row's value, so the words have to be there.

    cmdk's Command wrapper forwards neither shouldFilter nor extra props, so a
    server cannot opt out of that filter -- what it can choose is what the value
    contains. Ordering it by tf-idf is what makes position work: the page named
    Styling leads with the word, the nine pages that mention it do not.
    """
    values = [value for _label, value in _items(_palette())]
    assert values, "the open palette shipped no rows"
    assert any("safelisted" in value for value in values), "no row is findable by its body text"
    with_terms = [v for v in values if len(v.split()) > 3]
    assert len(with_terms) > len(values) * 0.8, "most rows carry nothing but a title"
    styling = [v for label, v in _items(_palette()) if label.startswith("Styling ")]
    assert styling and styling[0].lower().startswith("styling"), styling


def test_the_palette_input_keeps_the_browsers_text() -> None:
    """Neither controlled nor server-round-tripped per keystroke.

    A controlled input echoes one keystroke behind, so letters drop; and if the
    values were rewritten per keystroke, cmdk would score its live string against
    a stale echo and hide every row. Mirroring the text through save_prop has no
    echo to fight with -- the browser keeps ownership of what is typed.
    """
    nodes = _palette()
    inputs = [n["props"] for n in nodes if n.get("type") == "CommandInput"]
    assert len(inputs) == 1
    assert inputs[0].get("value") is None, "controlled input: keystrokes will drop"
    mirror = inputs[0].get("onValueChange")
    assert isinstance(mirror, dict) and mirror.get("saveProp"), "typing is not mirrored to state"


def test_the_palette_leads_to_the_results_page() -> None:
    """The row that turns a vague query into ranked, highlighted results."""
    nodes = _palette()
    rows = [n for n in nodes if n.get("type") == "CommandItem" and "Search page text" in str(n.get("children"))]
    assert len(rows) == 1, "the palette needs exactly one hand-off row"
    callback = rows[0]["props"]["on_select"]
    assert callback and callback.get("callbackId"), "the hand-off row goes nowhere"

    headings = [n["props"].get("heading") for n in nodes if n.get("type") == "CommandGroup"]
    assert headings[0] == "Go to", headings


def test_a_closed_page_does_not_ship_the_search_corpus() -> None:
    """~90 keyword blobs on every page load is payload nobody asked for."""
    import json

    closed = _palette(open_=False)
    assert not _items(closed), "the closed palette still ships rows"
    assert len(json.dumps(closed)) < 1_500
    assert len(_items(_palette())) == len(NAV_ROUTES) + 1  # plus the hand-off row


def test_keyword_blobs_stay_small_enough_to_send() -> None:
    """The corpus crosses the socket when ⌘K opens, so it costs latency."""
    sizes = [len(search.keywords(route)) for route in search.routes()]
    assert max(sizes) <= 200, f"largest blob is {max(sizes)} characters"
    assert sum(sizes) < 12_000, f"the palette corpus weighs {sum(sizes)} characters"


def _results(query: str) -> list[dict]:
    from fastapi.testclient import TestClient

    from docs.app import app

    client = TestClient(app)
    response = client.get("/api/page", headers={"referer": f"http://testserver/search?q={query}"})
    assert response.status_code == 200, response.text[:400]
    return _walk(response.json())


def test_the_results_page_is_registered() -> None:
    from docs.app import ui

    assert "/search" in ui.pages, "the results page has no route"


def test_the_results_page_answers_by_relevance_not_by_section() -> None:
    """The complaint that made this page: Getting Started led every search."""
    nodes = _results("styling")
    links = [n["props"].get("href") for n in nodes if n.get("type") == "Link" and n["props"].get("href", "").startswith("/docs")]
    assert links, "no results for a term several pages document"
    assert links[0] == "/docs/concepts/styling", links[:5]


def test_each_result_shows_its_section_on_the_right() -> None:
    nodes = _results("styling")
    badges = [(n.get("children") or [""])[0] for n in nodes if n.get("type") == "Badge"]
    assert "Core Concepts" in badges, badges

    sections = {section["label"] for section in NAV_SECTIONS}
    assert set(badges) <= sections, f"unknown section labels: {set(badges) - sections}"


def test_the_results_page_marks_what_matched() -> None:
    """Otherwise a list of titles says nothing the sidebar doesn't already."""
    for query in ("styling", "save_prop"):
        nodes = _results(query)
        contents = [str(n["props"].get("content")) for n in nodes if n.get("type") == "Markdown"]
        assert any(f"**{query}**" in c.lower() for c in contents), (query, contents[:2])
        assert not any("**" in c and c.count("**") % 2 for c in contents), "unbalanced bold in a snippet"


def test_result_links_all_lead_to_registered_pages() -> None:
    from docs.app import ui

    hrefs = {
        n["props"].get("href")
        for query in ("styling", "table", "session", "echarts")
        for n in _results(query)
        if n.get("type") == "Link"
    }
    dead = [h for h in hrefs if h and h.startswith("/docs") and h not in ui.pages]
    assert not dead, dead


def test_a_query_that_matches_nothing_says_so() -> None:
    nodes = _results("qqzzxwvnotaterm")
    texts = [" ".join(str(x) for x in (n.get("children") or [])) for n in nodes if n.get("type") == "Text"]
    assert any("0 of" in t for t in texts), texts[:3]
    assert any("Nothing matched" in t for t in texts), texts[:3]
