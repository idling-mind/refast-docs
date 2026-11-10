"""Refast Documentation Site.

A comprehensive documentation site for the Refast framework, built with Refast itself.

Run:
    cd <project_root>
    uvicorn docs.app:app --reload
"""
import inspect
import os
from importlib.metadata import version
from html import escape
from urllib.parse import quote

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

from refast import Context, RefastApp
from refast.components import (
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
    Button,
    Command,
    CommandEmpty,
    CommandInput,
    CommandItem,
    CommandList,
    ConnectionStatus,
    Container,
    Dialog,
    DialogContent,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    Flex,
    IconButton,
    Link,
    Row,
    Separator,
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarInset,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarMenuSub,
    SidebarMenuSubButton,
    SidebarMenuSubItem,
    SidebarProvider,
    SidebarRail,
    SidebarSeparator,
    SidebarTrigger,
    Text,
    Tooltip,
)
from refast.components.shadcn import KeyboardShortcut, ThemeSwitcher
from refast.theme import (
    amber_minimal_theme,
    caffine_theme,
    catppuccin_theme,
    default_theme,
    ocean_breeze_theme,
)

from . import search as search_index  # noqa: E402
from .pages import home  # noqa: E402
from .pages.advanced import (  # noqa: E402
    component_dev,
    extension_dev,
    security,
    sessions,
)
from .pages.components.registry import discover_component_groups  # noqa: E402
from .pages.concepts import (  # noqa: E402
    background,
    bundle_splitting,
    callbacks,
    desktop_notifications,
    file_transfers,
    js_interop,
    routing,
    state,
    streaming,
    styling,
    theming,
    toasts,
    updates,
)
from .pages.concepts import (
    components as concepts_components,
)
from .pages.extensions import (  # noqa: E402
    echarts as extensions_echarts,
    grid as extensions_grid,
    overview as extensions_overview,
    vtk_js as extensions_vtk_js,
)
from .pages.getting_started import (  # noqa: E402
    architecture,
    examples_gallery,
    installation,
    quick_tour,
    todo_app_live,
)
from docs.examples.routes import register_example_routes  # noqa: E402

#: the results page is not in NAV_SECTIONS -- it is a utility route, registered by hand
PAGE_ROUTE_SEARCH = "/search"

# ── App instance ─────────────────────────────────────────────────────────

ui = RefastApp(
    title="Refast Docs",
    theme=default_theme,
    favicon="/public/favicon.ico",
    custom_css="/styles/main.css",
    preloaded_features=["markdown", "controls", "navigation", "overlay"],
)

# Enter in the palette should mean "look that up in the pages", not "open whichever
# row cmdk happened to select first". cmdk auto-selects the top match as you type and
# its Command wrapper exposes no way to turn that off, so the difference has to be
# read from intent: if the last thing you did was arrow through rows, Enter selects
# one; if it was type, Enter asks /search, which can rank and explain properly.
#
# The text goes to the page by URL rather than through ctx.save_prop, because a
# mirrored value is one debounce behind and an Enter pressed immediately after typing
# deserves what is actually on screen. location.assign loads /search as a document;
# refast exposes no public JS navigation call to do it more cheaply.
ui.add_js(
    """
(() => {
  let arrowed = false;
  document.addEventListener("keydown", (event) => {
    const input = event.target;
    if (!input || !input.hasAttribute || !input.hasAttribute("cmdk-input")) {
      arrowed = false;
      return;
    }
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      arrowed = true;
    } else if (event.key === "Enter") {
      if (arrowed) return;
      event.preventDefault();
      event.stopPropagation();
      const query = input.value.trim();
      window.location.assign(query ? `/search?q=${encodeURIComponent(query)}` : "/search");
    } else {
      arrowed = false;
    }
  }, true);
})();
"""
)

# ── Navigation structure ─────────────────────────────────────────────────
# Each section has a label, icon, and list of pages.
# Pages are (label, route, icon) tuples.

NAV_SECTIONS = [
    {
        "label": "Getting Started",
        "icon": "rocket",
        "pages": [
            ("Installation", "/docs/getting-started", "download", installation.render),
            ("Architecture", "/docs/architecture", "layers", architecture.render),
            ("Quick Tour", "/docs/quick-tour", "zap", quick_tour.render),
            ("Live Todo Demo", "/docs/todo-live", "check-circle", todo_app_live.render),
            ("Examples Gallery", "/docs/examples", "grid-3x3", examples_gallery.render),
        ],
    },
    {
        "label": "Core Concepts",
        "icon": "layers",
        "pages": [
            ("Components", "/docs/concepts/components", "box", concepts_components.render),
            ("Callbacks & Events", "/docs/concepts/callbacks", "mouse-pointer-click", callbacks.render),
            ("State & Store", "/docs/concepts/state", "database", state.render),
            ("DOM Updates", "/docs/concepts/updates", "refresh-cw", updates.render),
            ("Routing & Navigation", "/docs/concepts/routing", "route", routing.render),
            ("Streaming", "/docs/concepts/streaming", "radio", streaming.render),
            ("Background Jobs", "/docs/concepts/background", "clock", background.render),
            ("Theming", "/docs/concepts/theming", "palette", theming.render),
            ("Styling", "/docs/concepts/styling", "paintbrush", styling.render),
            ("Toast Notifications", "/docs/concepts/toasts", "bell", toasts.render),
            ("Desktop Notifications", "/docs/concepts/desktop-notifications", "bell", desktop_notifications.render),
            ("JavaScript Interop", "/docs/concepts/js-interop", "code", js_interop.render),
            ("File Uploads & Downloads", "/docs/concepts/file-transfers", "upload", file_transfers.render),
            ("Bundle Splitting", "/docs/concepts/bundle-splitting", "package", bundle_splitting.render),
        ],
    },
    {
        "label": "Components",
        "icon": "component",
        "groups": discover_component_groups(),
    },
    {
        "label": "Extensions",
        "icon": "puzzle",
        "pages": [
            ("Overview", "/docs/extensions", "puzzle", extensions_overview.render),
            ("ECharts", "/docs/extensions/echarts", "bar-chart-2", extensions_echarts.render),
            ("Spreadsheet Grid", "/docs/extensions/grid", "grid-3x3", extensions_grid.render),
            ("3D VTK.js", "/docs/extensions/vtk-js", "box", extensions_vtk_js.render),
        ],
    },
    {
        "label": "Advanced",
        "icon": "settings",
        "pages": [
            ("Building Components", "/docs/advanced/component-dev", "hammer", component_dev.render),
            ("Building Extensions", "/docs/advanced/extension-dev", "puzzle", extension_dev.render),
            ("Security", "/docs/advanced/security", "shield", security.render),
            ("Sessions", "/docs/advanced/sessions", "key", sessions.render),
        ],
    },
]

# Build flat lookup: route -> (section_label, page_label)
_PAGE_LOOKUP: dict[str, tuple[str, str]] = {}
for _section in NAV_SECTIONS:
    if "groups" in _section:
        for _group in _section["groups"]:
            for _label, _route, *_ in _group["pages"]:
                _PAGE_LOOKUP[_route] = (_section["label"], _label)
    else:
        for _label, _route, *_ in _section["pages"]:
            _PAGE_LOOKUP[_route] = (_section["label"], _label)


# ── Navigation callback ─────────────────────────────────────────────────


async def nav(ctx: Context, path: str = "/"):
    """Navigate to a documentation page."""
    ctx.state["search_open"] = False
    await ctx.load(path)


async def open_search(ctx: Context, current_path: str = "/"):
    """Open the search dialog."""
    ctx.state["search_open"] = True
    await ctx.load(current_path)


async def close_search(ctx: Context, current_path: str = "/"):
    """Close the search dialog."""
    ctx.state["search_open"] = False
    await ctx.load(current_path)


async def open_full_search(ctx: Context):
    """Hand the palette's text to the results page.

    The query is read through save_prop rather than the item's own payload: a
    CommandItem's on_select carries nothing, and making the input controlled to
    get at it is what cost keystrokes before.
    """
    query = str(ctx.state.get("palette_query", "") or "").strip()
    await ctx.load(f"{PAGE_ROUTE_SEARCH}?q={quote(query)}" if query else PAGE_ROUTE_SEARCH)


async def search_navigate(ctx: Context, path: str = "/"):
    """Navigate from a search result and close the dialog."""
    ctx.state["search_open"] = False
    await ctx.load(path)


# ── Search helpers ───────────────────────────────────────────────────────


def _get_search_items() -> list[dict]:
    """Flatten NAV_SECTIONS into a list of searchable items grouped by section."""
    items: list[dict] = []
    for section in NAV_SECTIONS:
        group_label = section["label"]
        if "groups" in section:
            for group in section["groups"]:
                for label, route, icon, render in group["pages"]:
                    items.append(
                        {"label": label, "route": route, "icon": icon, "group": group_label, "render": render}
                    )
        else:
            for label, route, icon, render in section["pages"]:
                items.append(
                    {"label": label, "route": route, "icon": icon, "group": group_label, "render": render}
                )
    return items


_SEARCH_ITEMS = _get_search_items()

# The palette matched page titles only, so a reader hunting for "save_prop" had
# to know which page documented it first. This hands the same routes to the
# full-text index in docs/search.py, which covers the prose on them.
search_index.set_pages(
    [(item["label"], item["route"], item["group"], item["render"]) for item in _SEARCH_ITEMS]
)


# Where the site's own source lives; used for the footer's "Edit this page".
SITE_SOURCE_REPO = "https://github.com/idling-mind/refast-docs"
_REPO_ROOT = Path(__file__).resolve().parent.parent


def _source_url(route: str) -> str | None:
    """Blob URL of the module that renders ``route``, or None if it cannot be found.

    Derived from the page function rather than from the route, because the two do
    not line up: ``/docs/components/button`` is rendered by
    ``pages/components/buttons/button.py``.
    """
    func = next((item["render"] for item in _SEARCH_ITEMS if item["route"] == route), None)
    if func is None:
        return None
    try:
        path = Path(inspect.getsourcefile(inspect.unwrap(func))).resolve()
        return f"{SITE_SOURCE_REPO}/blob/main/{path.relative_to(_REPO_ROOT)}"
    except (TypeError, ValueError):  # no source available, or outside this repo
        return None


class PaletteRow(CommandItem):
    """A cmdk row that puts the page title on the left and its section on the right.

    CommandItem renders ``children: [label]``, so a plain label is the only text a
    row can carry. Gluing the section onto the title with an em-dash makes it read
    as part of the page's name, so this subclasses the row and hands it two spans.
    cmdk still scores ``value`` -- untouched -- and still owns selection; the extra
    span is decoration.
    """

    def __init__(self, label: str, section: str, **kwargs):
        super().__init__(label, **kwargs)
        self._title_text = Text(label, class_name="truncate")
        self._section_text = Text(
            section, class_name="ml-auto shrink-0 pl-4 text-xs text-muted-foreground"
        )

    def render(self) -> dict:
        node = super().render()
        node["children"] = [self._title_text.render(), self._section_text.render()]
        return node


def _build_search_dialog(ctx: Context, current_path: str):
    """Build the CMD+K search dialog overlay.

    Filtering happens in the browser. cmdk scores each item against the value it
    registers, and refast's Command wrapper forwards neither ``shouldFilter`` nor
    extra props, so the page text has to reach the client for body search to work
    at all: each row carries its page's title, section and most distinctive terms,
    ordered by tf-idf so that ``command-score``'s preference for early matches
    lands the right page on top. Driving the ranking from the server instead --
    refreshing per keystroke -- lost letters and then matched nothing, because a
    controlled input echoes one keystroke behind while cmdk scores the live string
    against that stale echo.

    One flat list, because sections are navigation and not ranking: while rows were
    grouped by section, any tie between groups fell back to DOM order, and Getting
    Started therefore led every search. The section sits at the right end of each
    row now.

    The list is built only while the dialog is open, which keeps the corpus out of
    every ordinary page payload.
    """
    if not ctx.state.get("search_open", False):
        return Dialog(open=False, children=[])

    rows: list[CommandItem] = [
        PaletteRow(
            "Search the text of every page",
            "\u21b5 results",
            value="full text search results page body snippet relevance",
            icon="search",
            on_select=ctx.callback(open_full_search),
        )
    ]
    rows.extend(
        PaletteRow(
            item["label"],
            item["group"],
            value=search_index.keywords(item["route"]),
            icon=item["icon"],
            on_select=ctx.callback(search_navigate, path=item["route"]),
        )
        for item in _SEARCH_ITEMS
    )

    return Dialog(
        open=True,
        on_open_change=ctx.callback(close_search, current_path=current_path),
        children=[
            DialogContent(
                class_name="p-0 overflow-hidden gap-0 max-w-lg",
                children=[
                    Command(
                        class_name="rounded-lg border-0 shadow-none",
                        children=[
                            CommandInput(
                                placeholder="Search titles and page text\u2026",
                                # Uncontrolled: the browser owns what is typed.
                                # save_prop only mirrors the text to the server so
                                # the results row can hand it over, and mirroring
                                # has no echo loop to lose keystrokes in.
                                on_value_change=ctx.save_prop("palette_query", debounce=200),
                            ),
                            CommandList(
                                children=[
                                    CommandEmpty(message="No pages found."),
                                    *rows,
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# ── Shared layout ────────────────────────────────────────────────────────


def docs_layout(ctx: Context, content, current_path: str = "/"):
    """Wrap page content in the documentation layout with sidebar navigation.

    Args:
        ctx: The request context.
        content: The page content component tree.
        current_path: Current page route for active-state highlighting.
    """
    # Use path-specific ID for content container to force scroll reset on navigation
    safe_path = current_path.replace("/", "-").strip("-") or "home"
    content_id = f"docs-content-{safe_path}"

    return SidebarProvider(
        id="docs-sidebar-provider",
        children=[
            _build_sidebar(ctx, current_path),
            SidebarInset(
                id="docs-sidebar-inset",
                class_name="min-w-0",
                children=[
                    _build_topbar(ctx, current_path),
                    Container(
                        id=content_id,
                        class_name="flex-1 min-w-0 overflow-y-auto overflow-x-hidden",
                        children=[content],
                    ),
                    _build_footer(ctx, current_path),
                ],
            ),
            _build_search_dialog(ctx, current_path),
            KeyboardShortcut(
                shortcuts={"ctrl+k": ctx.callback(open_search, current_path=current_path)},
                priority=10,
                prevent_default=True,
            ),
            ConnectionStatus(),
        ],
    )


def _build_sidebar(ctx: Context, current_path: str):
    """Build the sidebar with all navigation sections."""
    return Sidebar(
        id="docs-sidebar",
        collapsible="icon",
        children=[
            # Header — brand
            SidebarHeader(
                id="docs-sidebar-header",
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                id="docs-brand-item",
                                children=[
                                    SidebarMenuButton(
                                        "Refast Docs",
                                        icon="layers",
                                        size="lg",
                                        is_active=(current_path == "/"),
                                        on_click=ctx.callback(nav, path="/"),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            SidebarSeparator(),
            # Navigation sections
            SidebarContent(
                id="docs-sidebar-content",
                children=[_build_nav_group(ctx, section, current_path) for section in NAV_SECTIONS],
            ),
            SidebarSeparator(),
            # Footer — version + theme
            SidebarFooter(
                id="docs-sidebar-footer",
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                id="docs-footer-item",
                                children=[
                                    Row(
                                        [
                                            SidebarMenuButton(
                                                f"v{version('refast')}",
                                                icon="tag",
                                                size="sm",
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            SidebarRail(),
        ],
    )


def _build_nav_group(ctx: Context, section: dict, current_path: str):
    """Build a single navigation group in the sidebar."""
    section_id = section["label"].lower().replace(" ", "-")

    if "groups" in section:
        # Nested groups structure (Components section)
        menu_items = [
            _build_nav_subgroup(ctx, group, current_path)
            for group in section["groups"]
        ]
        return SidebarGroup(
            id=f"nav-group-{section_id}",
            children=[
                SidebarGroupLabel(section["label"]),
                SidebarGroupContent(
                    children=[SidebarMenu(children=menu_items)],
                ),
            ],
        )

    return SidebarGroup(
        id=f"nav-group-{section_id}",
        children=[
            SidebarGroupLabel(section["label"]),
            SidebarGroupContent(
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                id=f"nav-item-{route.strip('/').replace('/', '-')}",
                                children=[
                                    Tooltip(
                                        children=[
                                            SidebarMenuButton(
                                                label,
                                                icon=icon,
                                                is_active=(current_path == route),
                                                on_click=ctx.callback(nav, path=route),
                                            ),
                                        ],
                                        content=label,
                                        side="right",
                                    )
                                ],
                            )
                            for label, route, icon, *_ in section["pages"]
                        ],
                    ),
                ],
            ),
        ],
    )


def _build_nav_subgroup(ctx: Context, group: dict, current_path: str):
    """Build a collapsible sub-group with SidebarMenuSub items."""
    group_id = group["label"].lower().replace(" ", "-")
    is_any_active = any(page[1] == current_path for page in group["pages"])

    return SidebarMenuItem(
        id=f"nav-subgroup-{group_id}",
        children=[
            SidebarMenuButton(
                group["label"],
                icon=group.get("icon"),
                is_active=is_any_active,
            ),
            SidebarMenuSub(
                children=[
                    SidebarMenuSubItem(
                        id=f"nav-sub-{route.strip('/').replace('/', '-')}",
                        children=[
                            SidebarMenuSubButton(
                                label,
                                is_active=(current_path == route),
                                on_click=ctx.callback(nav, path=route),
                            )
                        ],
                    )
                    for label, route, *_ in group["pages"]
                ],
            ),
        ],
    )


async def _on_theme_change(ctx: Context, theme_name: str):
    """Handle theme change from the theme switcher."""
    theme_map = {
        "default": default_theme,
        "caffine": caffine_theme,
        "catppuccin": catppuccin_theme,
        "ocean-breeze": ocean_breeze_theme,
        "amber-minimal": amber_minimal_theme,
    }
    selected_theme = theme_map.get(theme_name, default_theme)
    await ctx.set_theme(selected_theme)


def theme_switcher(ctx: Context):
    return DropdownMenu(
        children=[
            DropdownMenuTrigger(
                IconButton(
                    icon="palette",
                    variant="ghost",
                    size="sm",
                )
            ),
            DropdownMenuContent(
                children=[
                    DropdownMenuItem(
                        theme.title(), on_select=ctx.callback(_on_theme_change, theme_name=theme)
                    )
                    for theme in [
                        "default",
                        "caffine",
                        "catppuccin",
                        "ocean-breeze",
                        "amber-minimal",
                    ]
                ]
            ),
        ]
    )


def _build_topbar(ctx: Context, current_path: str):
    """Build the top bar with breadcrumb and theme toggle."""
    # Build breadcrumb from current path
    crumbs = [("Docs", "/")]
    info = _PAGE_LOOKUP.get(current_path)
    if info:
        section_label, page_label = info
        crumbs.append((section_label, None))
        crumbs.append((page_label, current_path))

    breadcrumb_items = []
    for i, (label, route) in enumerate(crumbs):
        if i > 0:
            breadcrumb_items.append(BreadcrumbSeparator())
        if route and i < len(crumbs) - 1:
            breadcrumb_items.append(BreadcrumbItem(children=[BreadcrumbLink(label, href=route)]))
        else:
            breadcrumb_items.append(BreadcrumbItem(children=[BreadcrumbPage(label)]))

    return Container(
        id="docs-topbar",
        class_name="border-b px-4 py-3 sticky top-0 bg-background z-10",
        children=[
            Row(
                align="center",
                justify="between",
                children=[
                    Row(
                        [
                            SidebarTrigger(),
                            Separator(orientation="vertical", class_name="h-6 hidden md:block"),
                            Breadcrumb(children=[BreadcrumbList(children=breadcrumb_items)], class_name="hidden md:block"),
                        ],
                        align="center",
                        gap=4,
                    ),
                    Row(
                        [
                            IconButton(
                                icon="search",
                                size="sm",
                                on_click=ctx.callback(open_search, current_path=current_path),
                            ),
                            ThemeSwitcher(),
                            theme_switcher(ctx),
                        ],
                        align="center",
                        gap=2,
                    ),
                ],
            ),
        ],
    )


def _build_footer(ctx: Context, current_path: str):
    """Build prev/next navigation footer."""
    # Find current page index in flat list
    all_pages = []
    for section in NAV_SECTIONS:
        if "groups" in section:
            for group in section["groups"]:
                for label, route, *_ in group["pages"]:
                    all_pages.append((label, route))
        else:
            for label, route, *_ in section["pages"]:
                all_pages.append((label, route))

    current_idx = None
    for i, (label, route) in enumerate(all_pages):
        if route == current_path:
            current_idx = i
            break

    prev_btn = Container()  # empty spacer
    next_btn = Container()

    if current_idx is not None:
        if current_idx > 0:
            prev_label, prev_route = all_pages[current_idx - 1]
            prev_btn = Button(
                f"← {prev_label}",
                variant="ghost",
                on_click=ctx.callback(nav, path=prev_route),
            )
        if current_idx < len(all_pages) - 1:
            next_label, next_route = all_pages[current_idx + 1]
            next_btn = Button(
                f"{next_label} →",
                variant="ghost",
                on_click=ctx.callback(nav, path=next_route),
            )

    edit_link = Container()
    source_url = _source_url(current_path)
    if source_url:
        edit_link = Container(
            class_name="flex justify-end px-6 pb-2",
            children=[
                Link(
                    "Edit this page",
                    href=source_url,
                    variant="ghost",
                    external=True,
                    class_name="text-xs text-muted-foreground",
                )
            ],
        )

    return Container(
        id="docs-page-footer",
        # No horizontal padding here: the rule below has to reach both edges of
        # the column, so the rows are inset individually instead.
        class_name="mt-8",
        children=[
            edit_link,
            # The rule divides the prose from the page-to-page controls, so it has
            # to sit below both of those; the edit link belongs with the prose.
            Container(
                class_name="border-t",
                children=[
                    Flex(
                        direction="row",
                        justify="between",
                        class_name="px-6 py-4",
                        children=[prev_btn, next_btn],
                    )
                ],
            ),
        ],
    )


# ── Register all pages ───────────────────────────────────────────────────


def register_page(ui_app: RefastApp, route: str, render_fn):
    """Register a single page route handler on the RefastApp instance."""

    @ui_app.page(route)
    def _page_handler(ctx: Context):
        return render_fn(ctx)


def register_nav_routes(ui_app: RefastApp, nav_sections: list[dict]):
    """Dynamically register page handlers for all pages defined in NAV_SECTIONS."""
    for section in nav_sections:
        if "groups" in section:
            for group in section["groups"]:
                for page in group["pages"]:
                    route, render_fn = page[1], page[3]
                    register_page(ui_app, route, render_fn)
        else:
            for page in section["pages"]:
                route, render_fn = page[1], page[3]
                register_page(ui_app, route, render_fn)


# Standalone / root page
register_page(ui, "/", home.render)

# Register all navigation section pages dynamically
register_nav_routes(ui, NAV_SECTIONS)


@ui.page(PAGE_ROUTE_SEARCH)
def page_search(ctx: Context):
    """Full-text results. Reachable from the palette and by linking /search?q=…"""
    from .pages.search_results import render as render_search

    return render_search(ctx)

# Standalone example apps mounted under /examples/...
register_example_routes(ui)


# ── FastAPI app ──────────────────────────────────────────────────────────

app = FastAPI(title="Refast Documentation")
app.mount(
    "/styles", StaticFiles(directory=Path(__file__).parent / "styles"), name="styles"
)  # serve custom CSS and JS
# Refast emits `favicon` as a plain <link rel="icon" href=...>, so the file it
# points at has to be served; it sat unused in public/ while every tab requested
# href="📖".
app.mount(
    "/public", StaticFiles(directory=_REPO_ROOT / "public"), name="public"
)

# ── Discovery ───────────────────────────────────────────────────────────

#: Where this site is published. refast's own README points readers here;
#: override with REFAST_DOCS_URL on a preview deployment so a staging host does
#: not advertise itself as canonical.
SITE_URL = os.environ.get("REFAST_DOCS_URL", "https://refast.fastapicloud.com").rstrip("/")

SITE_DESCRIPTION = (
    "Documentation for Refast, a Python framework for building reactive web "
    "applications: a FastAPI-style backend drives a React, shadcn/ui and Tailwind "
    "frontend over a persistent WebSocket."
)

for _tag in (
    f'<meta name="description" content="{escape(SITE_DESCRIPTION)}">',
    '<meta property="og:type" content="website">',
    f'<meta property="og:site_name" content="{escape(ui.title)}">',
    f'<meta property="og:title" content="{escape(ui.title)}">',
    f'<meta property="og:description" content="{escape(SITE_DESCRIPTION)}">',
    f'<meta property="og:url" content="{SITE_URL}/">',
    '<meta name="twitter:card" content="summary">',
    # One shell is served for every route, so the canonical URL can only be the
    # root; per-page URLs and titles need server rendering. See docs/TODO.md.
    f'<link rel="canonical" href="{SITE_URL}/">',
):
    ui.add_head_tag(_tag)


@app.get("/robots.txt", include_in_schema=False)
async def robots_txt() -> PlainTextResponse:
    """Crawl everything; the site has no private routes."""
    return PlainTextResponse(
        "User-agent: *\nAllow: /\n\nSitemap: " + SITE_URL + "/sitemap.xml\n",
        media_type="text/plain",
    )


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml() -> Response:
    """Every registered page. Parameterised routes are left out: there is no way
    to enumerate what they would resolve to."""
    locations = "".join(
        f"  <url><loc>{escape(SITE_URL + ('' if route == '/' else route))}</loc></url>\n"
        for route in sorted(ui.pages)
        if "{" not in route
    )
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{locations}</urlset>\n",
        media_type="application/xml",
    )


app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

