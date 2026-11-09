"""Every link the docs site emits must lead somewhere that exists.

Two failure modes this catches:

* a page links to ``/docs/advanced/styling`` after that page moved to
  ``/docs/concepts/styling``. Nothing errors -- ``_page_handler`` falls back to
  the index page for unknown paths, so the reader silently lands elsewhere;
* a "View source" link says ``examples/charts`` while the repository directory
  is called ``examples/charts_showcase``.

Live links are read from the parsed module (``href=`` / ``path=`` / ``route=``
string literals handed to components and callbacks) so code samples embedded in
Markdown strings are not mistaken for navigation, and prose links are read from
the Markdown itself with fenced blocks skipped.
"""

import ast
import os
import re
from pathlib import Path

import pytest

from docs.app import ui

ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = ROOT / "docs"

#: the docs site's own route namespaces
ROUTE_PREFIXES = ("/docs", "/examples")

LINK_RE = re.compile(r"\[[^\]]*\]\((/[^\s#)]+)(?:#[^)]*)?\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
GITHUB_PATH_RE = re.compile(
    r"https://github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)/(?P<kind>tree|blob)/"
    r"(?P<ref>[\w.-]+)/(?P<path>[^\s)\"']+)"
)


def _page_routes() -> set[str]:
    """Routes registered with a page function (``pages`` is a property)."""
    pages = getattr(ui, "pages", None)
    if callable(pages):
        pages = pages()
    return set(pages or {})


def _files(suffixes: tuple[str, ...]) -> list[Path]:
    return sorted(
        p
        for p in DOCS_ROOT.rglob("*")
        if p.is_file() and p.suffix in suffixes and "__pycache__" not in p.parts
    )


def _markdown_lines(text: str, first_lineno: int = 1) -> list[tuple[int, str]]:
    """Lines of a Markdown block that are outside a fenced code block."""
    kept: list[tuple[int, str]] = []
    in_fence = False
    for index, line in enumerate(text.splitlines()):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept.append((first_lineno + index, line))
    return kept


def _prose_links(path: Path) -> list[tuple[int, str]]:
    """(line, target) for every Markdown link outside fenced code blocks."""
    if path.suffix == ".md":
        lines: list[tuple[int, str]] = _markdown_lines(path.read_text(encoding="utf-8"))
    else:
        lines = []
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=str(path))):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                lines.extend(_markdown_lines(node.value, node.lineno))
    return [
        (lineno, match.group(1))
        for lineno, line in lines
        for match in LINK_RE.finditer(line)
    ]


def _link_props(path: Path) -> list[tuple[int, str]]:
    """href= / path= / route= literals passed to live components and callbacks."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg in {"href", "path", "route"} and isinstance(keyword.value, ast.Constant):
                if isinstance(keyword.value.value, str):
                    found.append((node.lineno, keyword.value.value))
    return found


def test_internal_markdown_links_point_at_registered_pages() -> None:
    routes = _page_routes()
    bad = [
        f"{path.relative_to(ROOT)}:{lineno}: {target}"
        for path in _files((".py", ".md"))
        for lineno, target in _prose_links(path)
        if target.startswith(ROUTE_PREFIXES) and target not in routes
    ]
    assert not bad, "links to pages that are not registered:\n" + "\n".join(sorted(set(bad)))


def test_internal_link_props_point_at_registered_pages() -> None:
    routes = _page_routes()
    bad = [
        f"{path.relative_to(ROOT)}:{lineno}: {target}"
        for path in _files((".py",))
        for lineno, target in _link_props(path)
        if target.startswith(ROUTE_PREFIXES) and target not in routes
    ]
    assert not bad, "component links point at unregistered routes:\n" + "\n".join(sorted(set(bad)))


def test_nav_and_registered_routes_agree() -> None:
    """The catch-all GET route hides typos in NAV_SECTIONS, so compare directly."""
    from docs.app import NAV_SECTIONS

    nav_routes: set[str] = set()
    for section in NAV_SECTIONS:
        for group in (section["groups"] if "groups" in section else [section]):
            nav_routes.update(page[1] for page in group["pages"])

    pages = _page_routes()
    dead_links = sorted(nav_routes - pages)
    unlisted = sorted(r for r in pages - nav_routes if r.startswith("/docs"))
    assert not dead_links, f"sidebar routes with no page function: {dead_links}"
    assert not unlisted, f"/docs pages missing from the sidebar: {unlisted}"


def test_github_source_links_resolve() -> None:
    """Check "View source" URLs against a local refast checkout, when available.

    Set ``REFAST_REPO`` to a refast checkout to enable; CI skips it because it
    installs refast from a wheel and must not need a second repository.
    """
    repo = os.environ.get("REFAST_REPO")
    if not repo:
        pytest.skip("set REFAST_REPO to a refast checkout to verify source links")

    bad = [
        f"{path.relative_to(ROOT)}: {match['repo']}/{match['path']}"
        for path in _files((".py", ".md"))
        for match in GITHUB_PATH_RE.finditer(path.read_text(encoding="utf-8"))
        if match["owner"] == "idling-mind"
        and match["repo"] == "refast"
        and "{" not in match["path"]
        and not Path(repo, match["path"].rstrip("/")).exists()
    ]
    assert not bad, "GitHub source links point at paths that do not exist:\n" + "\n".join(sorted(set(bad)))
