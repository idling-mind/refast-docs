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

from docs import search
from docs.app import NAV_SECTIONS, ui

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


def test_palette_lists_results_for_the_current_query() -> None:
    """The dialog has to render the server's ranking, not re-filter it away."""
    from refast import Context

    ctx = Context()
    ctx.state["search_query"] = "debounce"
    page = ui.pages["/docs/components/textarea"](ctx)
    nodes = list(_walk(page.render() if hasattr(page, "render") else page))

    headings = [n["props"].get("heading") for n in nodes if n.get("type") == "CommandGroup"]
    assert any(str(h).startswith("Pages matching") for h in headings), headings

    items = [n["props"] for n in nodes if n.get("type") == "CommandItem"]
    assert items, "query produced an empty palette"
    assert all("debounce" in str(props.get("value", "")).lower() for props in items), (
        "cmdk scores each item's value against the query client-side; a value "
        "without the query filters the server's own results out"
    )

    inputs = [n["props"] for n in nodes if n.get("type") == "CommandInput"]
    assert inputs and inputs[0].get("onValueChange"), "the input is not wired to the server"


def _walk(node, seen=None):
    seen = [] if seen is None else seen
    if isinstance(node, dict):
        seen.append(node)
        for child in node.get("children") or []:
            _walk(child, seen)
    elif isinstance(node, list):
        for child in node:
            _walk(child, seen)
    return seen
