"""Refast Documentation Site.

A comprehensive documentation site for the Refast framework, built with Refast itself.

Run:
    cd <project_root>
    uvicorn docs.app:app --reload
"""
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

from .pages import home  # noqa: E402
from .pages.advanced import (  # noqa: E402
    component_dev,
    extension_dev,
    security,
    sessions,
)
from .pages.components import base  # noqa: E402
from .pages.components.buttons import (  # noqa: E402
    button,
    button_group,
    context_menu,
    dropdown_menu,
    icon_button,
    slider,
    switch,
    toggle,
)
from .pages.components.cards import (  # noqa: E402
    card as card_page,
)
from .pages.components.cards import (
    collapsible as collapsible_page,
)
from .pages.components.charts import (  # noqa: E402
    area_chart as area_chart_page,
)
from .pages.components.charts import (
    bar_chart as bar_chart_page,
)
from .pages.components.charts import (
    line_chart as line_chart_page,
)
from .pages.components.charts import (
    other_charts as other_charts_page,
)
from .pages.components.charts import (
    pie_chart as pie_chart_page,
)
from .pages.components.data_display import (  # noqa: E402
    accordion as accordion_page,
)
from .pages.components.data_display import (
    avatar as avatar_page,
)
from .pages.components.data_display import (
    data_table as data_table_page,
)
from .pages.components.data_display import (
    hover_card as hover_card_page,
)
from .pages.components.data_display import (
    list_component as list_page,
)
from .pages.components.data_display import (
    table as table_page,
)
from .pages.components.data_display import (
    tabs as tabs_page,
)
from .pages.components.data_display import (
    tooltip as tooltip_page,
)
from .pages.components.feedback import (  # noqa: E402
    alert as alert_page,
)
from .pages.components.feedback import (
    dialog as dialog_page,
)
from .pages.components.feedback import (
    popover as popover_page,
)
from .pages.components.feedback import (
    progress as progress_page,
)
from .pages.components.feedback import (
    sheet as sheet_page,
)
from .pages.components.form_inputs import (  # noqa: E402
    checkbox,
    combobox,
    date_picker,
    input_otp,
    radio,
    textarea,
)
from .pages.components.form_inputs import (
    form as form_input_page,
)
from .pages.components.form_inputs import (
    input as input_page,
)
from .pages.components.form_inputs import (
    select as select_page,
)
from .pages.components.layout import (  # noqa: E402
    column,
    container,
    flex,
    grid,
    resizable,
    row,
    scroll_area,
)
from .pages.components.navigation import (  # noqa: E402
    breadcrumb as breadcrumb_page,
)
from .pages.components.navigation import (
    navigation_menu as navigation_menu_page,
)
from .pages.components.navigation import (
    pagination as pagination_page,
)
from .pages.components.navigation import (
    sidebar_nav as sidebar_nav_page,
)
from .pages.components.typography import (
    badge as badge_page,
)
from .pages.components.typography import (
    blockquote as blockquote_page,
)
from .pages.components.typography import (
    code as code_page,
)
from .pages.components.typography import (  # noqa: E402
    heading,
)
from .pages.components.typography import (
    kbd as kbd_page,
)
from .pages.components.typography import (
    link as link_page,
)
from .pages.components.typography import (
    markdown as markdown_page,
)
from .pages.components.typography import (
    text as text_page,
)
from .pages.components.utility import (  # noqa: E402
    aspect_ratio as aspect_ratio_page,
)
from .pages.components.utility import (
    carousel as carousel_page,
)
from .pages.components.utility import (
    icon as icon_page,
)
from .pages.components.utility import (
    keyboard_shortcut as keyboard_shortcut_page,
)
from .pages.components.utility import (
    separator as separator_page,
)
from .pages.components.utility import (
    timer as timer_page,
)
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
from .pages.getting_started import (  # noqa: E402
    architecture,
    examples_gallery,
    installation,
    quick_tour,
    todo_app_live,
)

# ── App instance ─────────────────────────────────────────────────────────

ui = RefastApp(
    title="Refast Docs",
    theme=default_theme,
    favicon="📖",
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
        "groups": [
            {
                "label": "Foundations",
                "icon": "box",
                "pages": [
                    ("Base", "/docs/components/base", "box", base.render),
                    ("Container", "/docs/components/container", "panel-left", container.render),
                ],
            },
            {
                "label": "Layout",
                "icon": "layout",
                "pages": [
                    ("Row", "/docs/components/row", "rows", row.render),
                    ("Column", "/docs/components/column", "columns", column.render),
                    ("Flex", "/docs/components/flex", "expand", flex.render),
                    ("Grid", "/docs/components/grid", "layout-grid", grid.render),
                    ("Scroll Area", "/docs/components/scroll-area", "layout-list", scroll_area.render),
                    ("Resizable", "/docs/components/resizable", "grip-horizontal", resizable.render),
                ],
            },
            {
                "label": "Typography",
                "icon": "type",
                "pages": [
                    ("Heading", "/docs/components/heading", "type", heading.render),
                    ("Text & Paragraph", "/docs/components/text", "type", text_page.render),
                    ("Code", "/docs/components/code", "code", code_page.render),
                    ("Link", "/docs/components/link", "link", link_page.render),
                    ("Markdown", "/docs/components/markdown", "file-text", markdown_page.render),
                    ("BlockQuote", "/docs/components/blockquote", "quote", blockquote_page.render),
                    ("Badge", "/docs/components/badge", "tag", badge_page.render),
                    ("Kbd", "/docs/components/kbd", "terminal", kbd_page.render),
                ],
            },
            {
                "label": "Buttons & Actions",
                "icon": "mouse-pointer-click",
                "pages": [
                    ("Button", "/docs/components/button", "square", button.render),
                    ("Button Group", "/docs/components/button-group", "rows", button_group.render),
                    ("Icon Button", "/docs/components/icon-button", "circle", icon_button.render),
                    ("Toggle", "/docs/components/toggle", "check-square", toggle.render),
                    ("Switch", "/docs/components/switch", "check-circle", switch.render),
                    ("Slider", "/docs/components/slider", "sliders", slider.render),
                    ("Dropdown Menu", "/docs/components/dropdown-menu", "chevron-down", dropdown_menu.render),
                    ("Context Menu", "/docs/components/context-menu", "mouse-pointer-click", context_menu.render),
                ],
            },
            {
                "label": "Form Inputs",
                "icon": "text-cursor-input",
                "pages": [
                    ("Input", "/docs/components/input", "text-cursor-input", input_page.render),
                    ("Textarea", "/docs/components/textarea", "edit", textarea.render),
                    ("Select", "/docs/components/select", "chevrons-down", select_page.render),
                    ("Checkbox", "/docs/components/checkbox", "check-square", checkbox.render),
                    ("Radio", "/docs/components/radio", "circle-dot", radio.render),
                    ("Combobox", "/docs/components/combobox", "search", combobox.render),
                    ("Date Picker", "/docs/components/date-picker", "calendar", date_picker.render),
                    ("Input OTP", "/docs/components/input-otp", "shield-check", input_otp.render),
                    ("Form", "/docs/components/form", "clipboard", form_input_page.render),
                ],
            },
            {
                "label": "Cards & Containers",
                "icon": "credit-card",
                "pages": [
                    ("Card", "/docs/components/card", "credit-card", card_page.render),
                    ("Collapsible", "/docs/components/collapsible", "chevron-down", collapsible_page.render),
                ],
            },
            {
                "label": "Data Display",
                "icon": "table",
                "pages": [
                    ("Table", "/docs/components/table", "table", table_page.render),
                    ("Data Table", "/docs/components/data-table", "table", data_table_page.render),
                    ("Tabs", "/docs/components/tabs", "panel-top", tabs_page.render),
                    ("Accordion", "/docs/components/accordion", "layout-list", accordion_page.render),
                    ("Avatar", "/docs/components/avatar", "user", avatar_page.render),
                    ("Tooltip", "/docs/components/tooltip", "info", tooltip_page.render),
                    ("Hover Card", "/docs/components/hover-card", "credit-card", hover_card_page.render),
                    ("List", "/docs/components/list", "layout-list", list_page.render),
                ],
            },
            {
                "label": "Navigation",
                "icon": "compass",
                "pages": [
                    ("Breadcrumb", "/docs/components/breadcrumb", "more-horizontal", breadcrumb_page.render),
                    ("Sidebar", "/docs/components/sidebar-nav", "panel-left", sidebar_nav_page.render),
                    ("Pagination", "/docs/components/pagination", "more-horizontal", pagination_page.render),
                    ("Navigation Menu", "/docs/components/navigation-menu", "menu", navigation_menu_page.render),
                ],
            },
            {
                "label": "Feedback & Overlay",
                "icon": "message-square",
                "pages": [
                    ("Alert", "/docs/components/alert", "alert-triangle", alert_page.render),
                    ("Progress & Spinner", "/docs/components/progress", "loader", progress_page.render),
                    ("Dialog", "/docs/components/dialog", "x-circle", dialog_page.render),
                    ("Sheet", "/docs/components/sheet", "panel-right", sheet_page.render),
                    ("Popover", "/docs/components/popover", "message-square", popover_page.render),
                ],
            },
            {
                "label": "Charts",
                "icon": "bar-chart-3",
                "pages": [
                    ("Bar Chart", "/docs/components/bar-chart", "bar-chart", bar_chart_page.render),
                    ("Line Chart", "/docs/components/line-chart", "line-chart", line_chart_page.render),
                    ("Area Chart", "/docs/components/area-chart", "activity", area_chart_page.render),
                    ("Pie Chart", "/docs/components/pie-chart", "pie-chart", pie_chart_page.render),
                    ("Other Charts", "/docs/components/other-charts", "bar-chart-2", other_charts_page.render),
                ],
            },
            {
                "label": "Utility",
                "icon": "wrench",
                "pages": [
                    ("Icon", "/docs/components/icon", "star", icon_page.render),
                    ("Separator", "/docs/components/separator", "minus", separator_page.render),
                    ("Aspect Ratio", "/docs/components/aspect-ratio", "maximize", aspect_ratio_page.render),
                    ("Carousel", "/docs/components/carousel", "image", carousel_page.render),
                    ("Keyboard Shortcut", "/docs/components/keyboard-shortcut", "keyboard", keyboard_shortcut_page.render),
                    ("Timer", "/docs/components/timer", "timer", timer_page.render),
                ],
            },
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
                for label, route, icon, *_ in group["pages"]:
                    items.append({"label": label, "route": route, "icon": icon, "group": group_label})
        else:
            for label, route, icon, *_ in section["pages"]:
                items.append({"label": label, "route": route, "icon": icon, "group": group_label})
    return items



_SEARCH_ITEMS = _get_search_items()


def _build_search_dialog(ctx: Context, current_path: str):
    """Build the CMD+K search dialog overlay."""
    is_open = ctx.state.get("search_open", False)

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
                            CommandInput(placeholder="Search docs..."),
                            CommandList(
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
                            # Text(
                            #     f"Active users: {len(ui.active_contexts)}",
                            #     class_name="text-sm text-muted-foreground",
                            # )
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

    return Container(
        id="docs-page-footer",
        class_name="border-t px-6 py-4 mt-8",
        children=[
            Flex(
                direction="row",
                justify="between",
                children=[prev_btn, next_btn],
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




@ui.page("/docs/components/table")
def page_components_table(ctx: Context):
    return table_page.render(ctx)


@ui.page("/docs/components/tabs")
def page_components_tabs(ctx: Context):
    return tabs_page.render(ctx)


@ui.page("/docs/components/accordion")
def page_components_accordion(ctx: Context):
    return accordion_page.render(ctx)


@ui.page("/docs/components/avatar")
def page_components_avatar(ctx: Context):
    return avatar_page.render(ctx)


@ui.page("/docs/components/tooltip")
def page_components_tooltip(ctx: Context):
    return tooltip_page.render(ctx)


@ui.page("/docs/components/list")
def page_components_list(ctx: Context):
    return list_page.render(ctx)


@ui.page("/docs/components/data-table")
def page_components_data_table(ctx: Context):
    return data_table_page.render(ctx)


@ui.page("/docs/components/hover-card")
def page_components_hover_card(ctx: Context):
    return hover_card_page.render(ctx)



@ui.page("/docs/components/breadcrumb")
def page_components_breadcrumb(ctx: Context):
    return breadcrumb_page.render(ctx)


@ui.page("/docs/components/sidebar-nav")
def page_components_sidebar_nav(ctx: Context):
    return sidebar_nav_page.render(ctx)


@ui.page("/docs/components/pagination")
def page_components_pagination(ctx: Context):
    return pagination_page.render(ctx)


@ui.page("/docs/components/navigation-menu")
def page_components_navigation_menu(ctx: Context):
    return navigation_menu_page.render(ctx)



@ui.page("/docs/components/alert")
def page_components_alert(ctx: Context):
    return alert_page.render(ctx)


@ui.page("/docs/components/progress")
def page_components_progress(ctx: Context):
    return progress_page.render(ctx)


@ui.page("/docs/components/dialog")
def page_components_dialog(ctx: Context):
    return dialog_page.render(ctx)


@ui.page("/docs/components/sheet")
def page_components_sheet(ctx: Context):
    return sheet_page.render(ctx)


@ui.page("/docs/components/popover")
def page_components_popover(ctx: Context):
    return popover_page.render(ctx)



@ui.page("/docs/components/bar-chart")
def page_components_bar_chart(ctx: Context):
    return bar_chart_page.render(ctx)


@ui.page("/docs/components/line-chart")
def page_components_line_chart(ctx: Context):
    return line_chart_page.render(ctx)


@ui.page("/docs/components/area-chart")
def page_components_area_chart(ctx: Context):
    return area_chart_page.render(ctx)


@ui.page("/docs/components/pie-chart")
def page_components_pie_chart(ctx: Context):
    return pie_chart_page.render(ctx)


@ui.page("/docs/components/other-charts")
def page_components_other_charts(ctx: Context):
    return other_charts_page.render(ctx)



@ui.page("/docs/components/icon")
def page_components_icon(ctx: Context):
    return icon_page.render(ctx)


@ui.page("/docs/components/separator")
def page_components_separator(ctx: Context):
    return separator_page.render(ctx)


@ui.page("/docs/components/aspect-ratio")
def page_components_aspect_ratio(ctx: Context):
    return aspect_ratio_page.render(ctx)


@ui.page("/docs/components/carousel")
def page_components_carousel(ctx: Context):
    return carousel_page.render(ctx)


@ui.page("/docs/components/keyboard-shortcut")
def page_components_keyboard_shortcut(ctx: Context):
    return keyboard_shortcut_page.render(ctx)


@ui.page("/docs/components/timer")
def page_components_timer(ctx: Context):
    return timer_page.render(ctx)


# Advanced
@ui.page("/docs/advanced/component-dev")
def page_advanced_component_dev(ctx: Context):
    return component_dev.render(ctx)


@ui.page("/docs/advanced/extension-dev")
def page_advanced_extension_dev(ctx: Context):
    return extension_dev.render(ctx)


@ui.page("/docs/advanced/security")
def page_advanced_security(ctx: Context):
    return security.render(ctx)


@ui.page("/docs/advanced/sessions")
def page_advanced_sessions(ctx: Context):
    return sessions.render(ctx)


@ui.page("/docs/concepts/styling")
def page_concepts_styling(ctx: Context):
    return styling.render(ctx)


# ── Standalone Examples ──────────────────────────────────────────────────

@ui.page("/examples/hello")
def page_examples_hello(ctx: Context):
    from docs.examples.hello import hello_world_page
    return hello_world_page(ctx)


# ── FastAPI app ──────────────────────────────────────────────────────────

app = FastAPI(title="Refast Documentation")
app.mount(
    "/styles", StaticFiles(directory=Path(__file__).parent / "styles"), name="styles"
)  # serve custom CSS and JS
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

