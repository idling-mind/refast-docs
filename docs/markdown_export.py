"""Markdown for machines: per-page mirrors, `/llms.txt`, `/llms-full.txt`, page index.

Why this module exists
----------------------
refast serves one static shell for every route (`tests/test_docs_shell.py` says what
that shell contains), and the component tree is drawn in the browser afterwards. A
crawler can be told about a page by `/sitemap.xml`; an LLM told to read
`/docs/concepts/state` fetches that shell and gets no prose at all, which makes the
whole site invisible to it. This module gives every page a URL that answers with its
text: ``<route>.md``, plus the two indexes built from those same files.

Why it walks the rendered tree
------------------------------
``docs/search.py`` reads page prose out of string literals with ``ast``, which is the
right tool for an index and the wrong one for a mirror: props tables come from
``inspect``, code samples come from component signatures, and the order the literals
appear in a module is not the order a reader meets them in. So this module calls each
page function and converts *what the reader would have seen* back into Markdown,
descending from the ``docs-content-*`` container that :func:`docs.app.docs_layout`
puts the page body inside.

The conversion drops live examples, but at the narrowest place it can: a node whose
children are a control and nothing written (`variant`, `size`: a playground's vocabulary
rather than its prose) is pruned whole, while a paragraph that happens to sit beside a
button keeps the paragraph and loses the button. Each file says in its header whether
anything was dropped this way, so a reader who needs to click knows where to go;
`tests/test_docs_llm_surfaces.py` is what notices if a page that has prose ever exports
none.
"""

from __future__ import annotations

import inspect
import json
import re
from dataclasses import dataclass
from importlib.metadata import version as _pkg_version
from typing import Any, Callable

from fastapi.responses import PlainTextResponse, Response

#: The prefix of the container :func:`docs.app.docs_layout` puts page content inside.
CONTENT_ID_PREFIX = "docs-content-"

#: Component types that are a live demo rather than a sentence. Their labels are option
#: names, so they carry no prose with them.
_CONTROLS = frozenset(
    {
        "Button",
        "IconButton",
        "Checkbox",
        "CheckboxGroup",
        "Combobox",
        "Command",
        "CommandDialog",
        "CommandEmpty",
        "CommandGroup",
        "CommandInput",
        "CommandItem",
        "CommandList",
        "CommandSeparator",
        "CommandShortcut",
        "ContextMenu",
        "ContextMenuContent",
        "ContextMenuTrigger",
        "DataTable",
        "DatePicker",
        "Dialog",
        "DialogContent",
        "DialogTrigger",
        "DropdownMenu",
        "DropdownMenuContent",
        "DropdownMenuTrigger",
        "Form",
        "Input",
        "InputOTP",
        "KeyboardShortcut",
        "NavigationMenu",
        "Pagination",
        "Popover",
        "PopoverContent",
        "PopoverTrigger",
        "RadioGroup",
        "RefastGrid",
        "Select",
        "Sheet",
        "SheetContent",
        "SheetTrigger",
        "Sidebar",
        "SidebarProvider",
        "Slider",
        "Switch",
        "ThemeSwitcher",
        "Timer",
        "Toggle",
        "Tooltip",
        "TooltipContent",
        "TooltipTrigger",
        "VtkAlgorithm",
        "VtkGeometryRepresentation",
        "VtkView",
    }
)

#: Types whose name ends in this are a chart, whatever the wrapper is called.
_CHART_SUFFIXES = ("Chart",)

#: Types that are decoration rather than content, so they are dropped on their own.
_DROP = frozenset({"Icon", "Separator", "ConnectionStatus", "AspectRatio", "Iframe"})

#: Types that carry written prose, as opposed to a label beside a control.
_PROSE = frozenset({"Markdown", "Alert", "Code", "Table", "Accordion"})

#: Heading levels that would duplicate the ``# `` line this module writes itself.
_PAGE_TITLE_LEVEL = 1

_WS_RE = re.compile(r"[ \t]+\n")
_TRAILING_RE = re.compile(r"\n{3,}")


@dataclass
class Page:
    """One documentation page, as machine-readable text."""

    route: str
    title: str
    section: str
    group: str
    markdown: str
    source_url: str | None = None
    headings: tuple[str, ...] = ()
    has_demo: bool = False

    @property
    def chars(self) -> int:
        return len(self.markdown)

    @property
    def tokens(self) -> int:
        """Rough size for a reader whose budget is counted in tokens, not bytes."""
        return len(self.markdown) // 4

    @property
    def summary(self) -> str:
        """First sentence of real prose, for the one-line description in indexes."""
        for block in self.markdown.split("\n\n"):
            text = block.strip()
            if not text or text.startswith(("#", ">", "|", "```", "-", "* ", "![")):
                continue
            text = re.sub(r"\s+", " ", _strip_md(text)).strip()
            if len(text) < 20:
                continue
            sentence = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
            return sentence if len(sentence) < 220 else text[:217].rstrip() + "…"
        return ""

    @property
    def plain_summary(self) -> str:
        """:attr:`summary` without Markdown, for a context with no markup at all.

        `<meta description>` is read as text by everything that consumes it, where a
        stray `*` from ``*session*`` is noise and a link is a truncation.
        """
        return _plain_markup(self.summary)


@dataclass
class Entry:
    """A page as navigation knows it, before its tree has been rendered."""

    title: str
    route: str
    section: str
    func: Callable[..., Any]


def _no_source(route: str) -> str | None:
    """Until ``docs.app`` configures the real one, no page claims a source file."""


_pages: list[Page] = []
_entries: list[Entry] = []
_built = False
_site_url = ""
_source_url_for: Callable[[str], str | None] = _no_source


def configure(
    entries: list[tuple[str, str, str, Callable[..., Any]]],
    *,
    site_url: str,
    source_url_for: Callable[[str], str | None],
) -> None:
    """Record the pages to export. Mirrors :func:`docs.search.set_pages`.

    Rendering is not done here. Building ~110 component trees costs a second or so,
    and doing it during ``import docs.app`` would slow every test and every worker
    start for a surface only a crawler asks for; the first `.md` request pays for it
    and every later one is served from :data:`_pages`.

    Args:
        entries: ``(nav label, route, section, render function)`` per page.
        site_url: canonical origin, so links inside exported text are absolute.
        source_url_for: route to blob URL, for the "Source" line of each page.
    """
    global _site_url, _source_url_for, _built, _entries
    _site_url = site_url.rstrip("/")
    _source_url_for = source_url_for
    _entries = [Entry(title, route, section, func) for title, route, section, func in entries]
    _built = False
    _pages.clear()


def _build() -> None:
    """Render each recorded page once and keep the Markdown."""
    global _built
    if _built:
        return
    _pages.extend(
        Page(
            route=entry.route,
            title=_page_title(entry) or entry.title,
            section=entry.section,
            group=entry.section,
            markdown=markdown,
            source_url=_source_url_for(entry.route),
            has_demo=has_demo,
        )
        for entry, (markdown, has_demo) in zip(
            _entries, (_from_render_func(entry.func) for entry in _entries)
        )
    )
    for page in _pages:
        page.headings = tuple(_HEADING_RE.findall(page.markdown))
    _built = True


def pages() -> list[Page]:
    """Every configured page, in navigation order."""
    _build()
    return list(_pages)


def register_fastapi_routes(api: Any) -> None:
    """Attach the text surfaces to the FastAPI app: `.md`, `/llms.txt`, and friends.

    Call this after :func:`configure` and before the app's catch-all page route is
    included, or `/{path:path}` swallows them -- the same ordering reason
    `/robots.txt` is registered where it is in ``docs/app.py``.
    """
    for route in sorted({entry.route for entry in _entries}):
        _register(api, _markdown_path(route), _mirror_handler(route))

    _register(api, "/llms.txt", llms_txt_response)
    _register(api, "/llms-full.txt", llms_full_txt_response)
    _register(api, "/api/pages.json", pages_json_response)


def _mirror_handler(route: str) -> Callable[[], Response]:
    """One handler per page, with the route bound now rather than looked up later."""

    def serve() -> Response:
        return _markdown_response(page_markdown(route) or "")

    return serve


def _markdown_response(body: str) -> Response:
    return Response(content=body, media_type="text/markdown; charset=utf-8")


def llms_txt_response() -> Response:
    """`/llms.txt`: the index, in the shape llmstxt.org describes."""
    return _markdown_response(llms_txt())


def llms_full_txt_response() -> Response:
    """`/llms-full.txt`: every page, concatenated in navigation order."""
    return _markdown_response(llms_full_txt())


def pages_json_response() -> Response:
    """`/api/pages.json`: the same inventory as data rather than prose."""
    return PlainTextResponse(
        json.dumps(index_json(), indent=2), media_type="application/json"
    )


def _register(api: Any, path: str, handler: Callable[[], Response]) -> None:
    """Add one GET route without a `@decorator`, so the loop above stays legible."""
    api.add_api_route(path, handler, methods=["GET"], include_in_schema=False)


def find(route: str) -> Page | None:
    """The page registered for ``route``, or None."""
    _build()
    return next((p for p in _pages if p.route == route), None)


def markdown_url(route: str) -> str:
    """Absolute URL of a page's Markdown mirror."""
    return f"{_site_url}{_markdown_path(route)}"


def markdown_href(route: str) -> str:
    """Same, site-relative, for a link that lives on the page it points to."""
    return _markdown_path(route)


def site_href(route: str) -> str:
    """Absolute URL of the rendered page, for saying "run this" in exported text."""
    return f"{_site_url}{route}"


def knows(route: str) -> bool:
    """Whether ``route`` has a Markdown mirror, without rendering anything."""
    return any(entry.route == route for entry in _entries)


def _markdown_path(route: str) -> str:
    return "/index.md" if route == "/" else f"{route}.md"


# ── Tree → Markdown ──────────────────────────────────────────────────────

_HEADING_RE = re.compile(r"^#{2,6}\s+(.*)$", re.MULTILINE)


def _page_title(entry: Entry) -> str:
    """The page's own ``PAGE_TITLE``, which is the heading its reader sees.

    The sidebar label is what navigation calls the page, and the two differ: the file
    at `/docs/getting-started` is titled "Installation & Getting Started". Identity —
    `<title>`, the mirror's H1, the index row — follows the page, so a reader who
    arrived by URL and a reader who arrived by link are reading the same name.
    """
    module = inspect.getmodule(entry.func)
    return str(getattr(module, "PAGE_TITLE", "") or "")


def _from_render_func(func: Callable[..., Any]) -> tuple[str, bool]:
    """Build the page and flatten it to Markdown; ('', False) if it will not build."""
    from refast.context import Context

    try:
        tree = func(Context())
        if inspect.isawaitable(tree):  # pragma: no cover - every page here is sync
            import asyncio

            tree = asyncio.run(tree)
    except Exception:  # a page that cannot render has no text to export, and /llms.txt
        # must not 500 because of one broken module. tests/test_docs_pages_render.py
        # is where that failure belongs.
        return "", False
    return _content_of(tree)


_RELATIVE_LINK_RE = re.compile(r"\]\((/[^)\s#][^)]*)(#[^)]*)?\)")

#: What refast's ``Markdown`` turns a `<custom_tag/>` into: an image whose src is a
#: component id, which the browser swaps for the real component. Nowhere else does
#: that URL lead, so a mirror must say what was here instead of linking to nothing.
_COMPONENT_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((?:https?://[^/\s)]+)?/refast-component/[^)]+\)")


def _inline_components(text: str) -> tuple[str, bool]:
    """Replace embedded-component placeholders, and report whether any were there."""
    found = bool(_COMPONENT_IMAGE_RE.search(text))
    replaced = _COMPONENT_IMAGE_RE.sub(lambda m: f"a live {m.group(1)} component", text)
    return replaced, found


def _absolutize(text: str) -> str:
    """Make site-relative links whole.

    A mirror is fetched on its own, often by something with no memory of where it
    came from; `](/docs/concepts/state)` is only a link if you know the origin.
    """
    if not _site_url:
        return text
    return _RELATIVE_LINK_RE.sub(
        lambda m: f"]({_site_url}{m.group(1)}{m.group(2) or ''})", text
    )


def _content_of(component: Any) -> tuple[str, bool]:
    """Markdown for everything below the layout, and whether a live example was left out."""
    node = component.render() if hasattr(component, "render") else component
    body = _find_content(node)
    blocks: list[str] = []
    state = {"demo": False}
    _walk(body if body is not None else node, blocks, state)
    text = "\n\n".join(b for b in blocks if b.strip())
    text = _TRAILING_RE.sub("\n\n", _WS_RE.sub("\n", text)).strip()
    text, embedded = _inline_components(text)
    state["demo"] = state["demo"] or embedded
    return _absolutize(text), state["demo"]


def _find_content(node: dict) -> dict | None:
    """The container ``docs_layout`` wrapped the page body in, by its id prefix."""
    if not isinstance(node, dict):
        return None
    if str(node.get("id", "")).startswith(CONTENT_ID_PREFIX):
        return node
    for child in node.get("children") or []:
        if isinstance(child, dict):
            found = _find_content(child)
            if found is not None:
                return found
    return None


def _walk(node: Any, blocks: list[str], state: dict) -> None:
    if isinstance(node, str):
        if text := node.strip():
            blocks.append(text)
        return
    if not isinstance(node, dict):
        return

    kind = node.get("type") or ""
    props = node.get("props") or {}
    children = node.get("children") or []

    if kind in _DROP:
        return
    if _is_widget(node):
        # A control has no text worth exporting, and its label is an option name.
        state["demo"] = True
        return

    if any(_is_widget(child) for child in children if isinstance(child, dict)) and not any(
        _has_prose(child) for child in children if isinstance(child, dict)
    ):
        # One child is a live widget and none is prose, so this row exists to be
        # clicked rather than read: a playground's `variant`/`size` labels are its
        # children, and they are vocabulary, not documentation. Prune the row.
        state["demo"] = True
        return

    if kind == "Markdown":
        if content := str(props.get("content") or "").strip():
            blocks.append(content)
        return
    if kind == "Heading":
        text = _text(children)
        level = int(props.get("level") or 2)
        if text and level > _PAGE_TITLE_LEVEL:
            blocks.append(f"{'#' * min(level, 6)} {text}")
        return
    if kind in ("Text", "Paragraph", "CardDescription"):
        if text := _text(children):
            blocks.append(text)
        return
    if kind in ("CardTitle", "SheetTitle"):
        if text := _text(children):
            blocks.append(f"### {text}")
        return
    if kind == "Alert":
        title = str(props.get("title") or "").strip()
        message = str(props.get("message") or "").strip() or _text(children)
        quoted = "\n".join(f"> {line}" for line in message.splitlines() if line.strip())
        blocks.append(f"> **{title}**\n{quoted}" if title else f"> {message}")
        return
    if kind == "Code":
        blocks.append(f"```\n{_text(children) or str(props.get('content') or '')}\n```")
        return
    if kind == "Link":
        href = str(props.get("href") or "")
        label = _text(children) or href
        blocks.append(f"[{label}]({_absolute(href)})")
        return

    for child in children:
        _walk(child, blocks, state)


def _is_widget(node: Any) -> bool:
    """Whether this node is itself a live control rather than a container of text."""
    if not isinstance(node, dict):
        return False
    kind = node.get("type") or ""
    return kind in _CONTROLS or kind.endswith(_CHART_SUFFIXES)


def _has_prose(node: dict) -> bool:
    """Whether anything below ``node`` is written to be read.

    The distinction lets a page that puts a paragraph and a button in the same row
    export the paragraph and drop the button, instead of losing the row.
    """
    kind = node.get("type") or ""
    if kind in _PROSE:
        return True
    return any(
        isinstance(child, dict) and not _is_widget(child) and _has_prose(child)
        for child in node.get("children") or []
    )


def _text(children: Any) -> str:
    """Plain text of an inline subtree, with links kept as links."""
    if isinstance(children, str):
        return children.strip()
    parts: list[str] = []
    for child in children or []:
        if isinstance(child, str):
            parts.append(child.strip())
        elif isinstance(child, dict):
            if child.get("type") == "Link":
                href = str((child.get("props") or {}).get("href") or "")
                parts.append(f"[{_text(child.get('children'))}]({_absolute(href)})")
            else:
                parts.append(_text(child.get("children")))
    return " ".join(p for p in parts if p).strip()


def _strip_md(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)


def _plain_markup(text: str) -> str:
    """Emphasis, code spans and heading marks removed; the words kept."""
    return re.sub(r"[*_`]{1,3}", "", text).strip()


def _absolute(href: str) -> str:
    """Site-relative links have no meaning to a reader who fetched one file."""
    if href.startswith("/") and _site_url:
        return f"{_site_url}{href}"
    return href


# ── The four surfaces ────────────────────────────────────────────────────


def page_document(page: Page) -> str:
    """One page as a standalone Markdown file, with the metadata an agent needs."""
    header = [f"# {page.title}", ""]
    facts = [
        f"- **Section:** {page.section}",
        f"- **URL:** {site_href(page.route)}",
        f"- **Markdown:** {markdown_url(page.route)}",
    ]
    if page.source_url:
        facts.append(f"- **Source:** {page.source_url}")
    if page.has_demo:
        facts.append(
            "- **Live examples:** the widgets on this page need a browser; "
            "open the URL above to try them."
        )
    try:
        facts.append(f"- **Applies to:** refast {_pkg_version('refast')}")
    except Exception:  # pragma: no cover - an uninstalled distribution
        pass
    footer = [
        "",
        "---",
        "",
        f"Part of the Refast documentation: [all pages]({site_href('/llms.txt')}), "
        f"[everything on one page]({site_href('/llms-full.txt')}), "
        f"[search]({site_href('/api/search')}?q=save_prop).",
    ]
    body = page.markdown or "_This page is a live example; open it in a browser._"
    return "\n".join(header + facts + ["", body] + footer) + "\n"


def page_markdown(route: str) -> str | None:
    """The ``.md`` file for ``route``, or None when no page is registered for it."""
    page = find(route)
    return page_document(page) if page else None


def corpus_delimiter(route: str) -> str:
    """The line `/llms-full.txt` puts above each page.

    A rule of hyphens would read better, and could not be counted: the pages
    themselves contain `---` separators, so the corpus needs a marker that prose
    cannot imitate.
    """
    return f"<!-- {'=' * 12} {route} {'=' * 12} -->"


def _heading_tree(page: Page) -> str:
    return " · ".join(page.headings[:6])


def llms_txt(description: str = "") -> str:
    """`/llms.txt <https://llmstxt.org>`_: an index, not a corpus.

    The links point at Markdown mirrors rather than the HTML routes, because the
    point of the file is that a model can follow one and get text back.
    """
    lines = [
        "# Refast Docs",
        "",
        (
            description
            or (
                "> Documentation for Refast, a Python framework for building reactive "
                "web applications: a FastAPI-style backend drives a React, shadcn/ui "
                "and Tailwind frontend over a persistent WebSocket."
            )
        ),
        "",
        "> Every page also exists as Markdown at its URL plus `.md`, and this file "
        "links to those. "
        f"`{_site_url}/llms-full.txt` holds all of them concatenated, for one-shot "
        f"prompts, and `{_site_url}/api/search?q=styling` returns ranked JSON.",
        "",
    ]
    by_section: dict[str, list[Page]] = {}
    for page in pages():
        by_section.setdefault(page.section, []).append(page)
    for section, section_pages in by_section.items():
        lines.append(f"## {section}")
        lines.append("")
        for page in section_pages:
            summary = page.summary or page.title
            tail = f" ({_heading_tree(page)})" if len(page.headings) > 3 else ""
            lines.append(f"- [{page.title}]({markdown_url(page.route)}): {summary}{tail}")
        lines.append("")
    lines += [
        "## Machine-readable surfaces",
        "",
        f"- [Page index]({_site_url}/api/pages.json): route, title, section, headings "
        "and size of every page, for planning a read.",
        f"- [Search API]({_site_url}/api/search?q=save_prop): ranked results over the "
        "text of every page, as JSON.",
        f"- [Full corpus]({_site_url}/llms-full.txt): every page, in one file.",
        "",
    ]
    return "\n".join(lines)


def llms_full_txt(description: str = "") -> str:
    """`/llms-full.txt`: every page in one file, in navigation order."""
    all_pages = pages()
    total = sum(page.chars for page in all_pages)
    lines = [
        "# Refast Docs — full corpus",
        "",
        description or f"> See {markdown_url('/')} for the index. ",
        "",
        f"> {len(all_pages)} pages, ~{total // 4:,} tokens. Separated in navigation order; "
        f"each section header carries the page's URL.",
        "",
    ]
    for page in all_pages:
        lines += [
            corpus_delimiter(page.route),
            "",
            f"# {page.title}",
            "",
            f"Section: {page.section} — URL: {_site_url}{page.route}",
            "",
            page.markdown or "_Live example only; see the URL above._",
            "",
        ]
    return _TRAILING_RE.sub("\n\n", "\n".join(lines)).strip() + "\n"


def index_json() -> dict[str, Any]:
    """`/api/pages.json`: the same inventory as `/llms.txt`, as data."""
    all_pages = pages()
    return {
        "site": _site_url,
        "refast_version": _pkg_version("refast"),
        "count": len(all_pages),
        "pages": [
            {
                "route": page.route,
                "title": page.title,
                "section": page.section,
                "url": f"{_site_url}{page.route}",
                "markdown_url": markdown_url(page.route),
                "source_url": page.source_url,
                "summary": page.summary,
                "headings": list(page.headings),
                "chars": page.chars,
                "approx_tokens": page.tokens,
            }
            for page in all_pages
        ],
    }
