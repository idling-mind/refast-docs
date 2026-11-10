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
        ("sessionStorage", "/docs/concepts/state"),
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


def test_the_palette_ships_page_text_for_cmdk_to_score() -> None:
    """Body words have to reach the browser, because cmdk filters locally.

    refast's Command wrapper forwards neither ``shouldFilter`` nor extra props, so
    a server cannot opt out of cmdk's scoring. The terms come from the index
    rather than being hardcoded: whatever ``search()`` found in a page body has to
    be in that page's item value, or the palette cannot find it either.
    """
    values = {
        str(n["props"].get("value", "")).lower()
        for n in _palette()
        if n.get("type") == "CommandItem"
    }
    assert values, "the open palette shipped no items"

    for query in ("save_prop", "debounce"):
        hits = search.search(query, limit=8)
        assert hits, f"the index itself knows nothing about {query!r}"
        assert any(query in search.keywords(h.route).lower() for h in hits), (
            f"{query!r} is ranked by the index but reaches no item value, so cmdk cannot match it"
        )
        assert any(query in v for v in values), f"{query!r} is not searchable in the palette"


def test_the_palette_input_is_uncontrolled() -> None:
    """A controlled input loses keystrokes; the palette must not echo them.

    The first version sent every keystroke to the server and echoed it back as
    ``value=``. Typing arrived one letter at a time, and cmdk then scored its
    live string against item values that were one keystroke stale -- so nothing
    matched. Local filtering has no such window.
    """
    inputs = [n["props"] for n in _palette() if n.get("type") == "CommandInput"]
    assert len(inputs) == 1
    assert inputs[0].get("value") is None, "the palette input is controlled; keystrokes will drop"
    assert not inputs[0].get("onValueChange"), "typing round-trips to the server again"


def test_a_closed_page_does_not_ship_the_search_corpus() -> None:
    """90 keyword blobs on every page load is payload nobody asked for."""
    import json

    closed = _palette(open_=False)
    assert not [n for n in closed if n.get("type") == "CommandItem"]
    assert len(json.dumps(closed)) < 1_500, "the closed palette still carries the corpus"

    items = [n for n in _palette(open_=True) if n.get("type") == "CommandItem"]
    assert len(items) == len(NAV_ROUTES), "every page in the navigation should be reachable"


def test_keyword_blobs_stay_small_enough_to_send() -> None:
    """The corpus crosses the socket the moment ⌘K is pressed, so it costs latency."""
    sizes = [len(search.keywords(route)) for route in search.routes()]
    assert max(sizes) <= 420, f"largest blob is {max(sizes)} characters"
    assert sum(sizes) < 30_000, f"the palette corpus weighs {sum(sizes)} characters"


def test_keywords_name_the_page_they_came_from() -> None:
    """A blob that lost its own title would rank badly in cmdk's scoring."""
    blob = search.keywords("/docs/advanced/sessions").lower()
    assert "session" in blob and "cookie" in blob, blob
