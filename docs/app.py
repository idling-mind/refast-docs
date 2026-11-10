"""Refast Documentation Site.

A comprehensive documentation site for the Refast framework, built with Refast itself.

Run:
    cd <project_root>
    uvicorn docs.app:app --reload
"""
import inspect
from importlib.metadata import version

from pathlib import Path

from fastapi import FastAPI
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
    CommandGroup,
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

# ── App instance ─────────────────────────────────────────────────────────

ui = RefastApp(
    title="Refast Docs",
    theme=default_theme,
    favicon="/public/favicon.ico",
    custom_css="/styles/main.css",
    preloaded_features=["markdown", "controls", "navigation", "overlay"],
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
    ctx.state["search_query"] = ""
    await ctx.load(current_path)


async def search_query(ctx: Context, query: str = ""):
    """Re-rank the palette as the reader types, against page bodies not just titles."""
    ctx.state["search_query"] = query
    await ctx.refresh(target_id="search-results")


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

_ICONS_BY_ROUTE = {item["route"]: item["icon"] for item in _SEARCH_ITEMS}

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


def _build_search_dialog(ctx: Context, current_path: str):
    """Build the CMD+K search dialog overlay."""
    is_open = ctx.state.get("search_open", False)
    query = str(ctx.state.get("search_query", "") or "")

    if query.strip():
        # Ranking happens on the server, over the text of every page. cmdk then
        # filters its own items client-side, which would throw away results
        # whose titles do not contain the query -- so the query goes into each
        # item's value, the documented way of driving cmdk from a backend.
        command_groups = [
            CommandGroup(
                heading=f"Pages matching \u201c{query}\u201d",
                children=[
                    CommandItem(
                        label=hit.title,
                        value=hit.value_for(query),
                        icon=_ICONS_BY_ROUTE.get(hit.route, "file-text"),
                        on_select=ctx.callback(search_navigate, path=hit.route),
                    )
                    for hit in search_index.search(query)
                ],
            )
        ]
    else:
        # Group items by section label
        groups: dict[str, list[dict]] = {}
        for item in _SEARCH_ITEMS:
            groups.setdefault(item["group"], []).append(item)

        command_groups = []
        for group_label, group_items in groups.items():
            command_groups.append(
                CommandGroup(
                    heading=group_label,
                    children=[
                        CommandItem(
                            label=item["label"],
                            value=item["label"],
                            icon=item["icon"],
                            on_select=ctx.callback(search_navigate, path=item["route"]),
                        )
                        for item in group_items
                    ],
                )
            )

    return Dialog(
        open=is_open,
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
                                value=query,
                                on_value_change=ctx.callback(search_query),
                            ),
                            CommandList(
                                id="search-results",
                                children=[
                                    CommandEmpty(message="No pages found."),
                                    *command_groups,
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
            class_name="flex justify-center pt-3",
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
        class_name="border-t px-6 py-4 mt-8",
        children=[
            Flex(
                direction="row",
                justify="between",
                children=[prev_btn, next_btn],
            ),
            edit_link,
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
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

