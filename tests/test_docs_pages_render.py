"""Render every documentation page and example through Refast's page API.

Why this test exists
--------------------
A Refast page function is *not* executed while serving the initial HTML
request: ``GET /<path>`` only returns the app shell. The component tree is
built in ``GET /api/page`` (used for SPA navigation and refresh) and in the
WebSocket ``page_render`` flow. That means a renamed prop, a deleted component
or a bad import does not turn a page into an HTTP 500 -- the page simply fails
to render in the browser, which nothing else in this repository would notice.

This test exercises the page function for every registered route and asserts a
non-empty component tree comes back, so API drift between refast releases and
the docs site fails CI with the original traceback.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from docs.app import NAV_SECTIONS, app, ui

TEST_BASE_URL = "http://testserver"


def _page_routes() -> dict[str, object]:
    """Registered page routes; ``pages`` is a property in refast >= 0.9."""
    pages = getattr(ui, "pages", None)
    if callable(pages):
        pages = pages()
    return dict(pages or {})


def _nav_routes() -> list[str]:
    """Every route reachable from the sidebar."""
    routes: list[str] = ["/"]
    for section in NAV_SECTIONS:
        groups = section["groups"] if "groups" in section else [section]
        for group in groups:
            for page in group["pages"]:
                routes.append(page[1])
    return routes


def _registered_routes() -> list[str]:
    """Every route registered on the Refast app, minus parameterised ones."""
    return sorted({route for route in _page_routes() if "{" not in route})


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.parametrize("route", _registered_routes())
def test_page_function_renders_a_component_tree(route: str, client: TestClient) -> None:
    """Each page function must build and render without raising."""
    response = client.get("/api/page", headers={"referer": f"{TEST_BASE_URL}{route}"})

    assert response.status_code == 200, (
        f"{route} failed to render: {response.status_code} {response.text[:500]}"
    )
    tree = response.json()
    assert tree.get("type"), f"{route} rendered an empty component tree: {tree!r}"


def test_sidebar_routes_are_all_registered() -> None:
    """The sidebar must not link to routes that no page handles."""
    registered = set(_page_routes())
    missing = [route for route in _nav_routes() if route not in registered]
    assert not missing, f"nav sections link to unregistered pages: {missing}"


def test_page_routes_are_documented_in_nav() -> None:
    """Every /docs page should be reachable from the sidebar."""
    nav_routes = set(_nav_routes())
    orphans = [
        route
        for route in _registered_routes()
        if route.startswith("/docs") and route not in nav_routes
    ]
    assert not orphans, f"/docs pages missing from the sidebar: {orphans}"
