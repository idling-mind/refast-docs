"""Examples Gallery — /docs/examples."""

from refast import Context
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Container,
    Grid,
    Heading,
    Icon,
    Input,
    Row,
    Separator,
    Text, Column, Link,
)

PAGE_TITLE = "Examples Gallery"
PAGE_ROUTE = "/docs/examples"

CATEGORIES = [
    "All",
    "Basic",
    "Layout & Navigation",
    "Data & Charts",
    "Real-time & Markdown",
    "Advanced & Desktop",
]

EXAMPLES = [
    {
        "title": "Hello World",
        "desc": "Minimal Refast app — one page, one component.",
        "icon": "hand-metal",
        "file": "examples/hello.py",
        "tags": ["Basic"],
    },
    {
        "title": "Basic App",
        "desc": "Counter with state management and callbacks.",
        "icon": "play",
        "file": "examples/basic/app.py",
        "tags": ["Basic"],
    },
    {
        "title": "Todo App",
        "desc": "Classic todo list with add, toggle, and delete.",
        "icon": "check-square",
        "file": "examples/todo_app/app.py",
        "tags": ["Basic"],
    },
    {
        "title": "Todo App (Single-file)",
        "desc": "Single-file implementation of the classic task management Todo app.",
        "icon": "clipboard-check",
        "file": "examples/todoapp.py",
        "tags": ["Basic"],
    },
    {
        "title": "Input Features",
        "desc": "Showcase of advanced Input component attributes including required states, descriptions, and error message rendering.",
        "icon": "text-cursor-input",
        "file": "examples/input_features/app.py",
        "tags": ["Basic"],
    },
    {
        "title": "Prop Store",
        "desc": "Client-side form state with store_as and prop_store.",
        "icon": "hard-drive",
        "file": "examples/prop_store/app.py",
        "tags": ["Basic"],
    },
    {
        "title": "Form Validation",
        "desc": "Input validation patterns and error display.",
        "icon": "shield-check",
        "file": "examples/form_validation/app.py",
        "tags": ["Basic"],
    },
    {
        "title": "Refresh Counter",
        "desc": "A basic counter exhibiting periodic background execution and asynchronous client state synchronization.",
        "icon": "timer",
        "file": "examples/refresh_counter.py",
        "tags": ["Basic", "Real-time"],
    },
    {
        "title": "Multi-Page SPA",
        "desc": "SPA navigation with shared layout and ctx.load().",
        "icon": "route",
        "file": "examples/multi_page/app.py",
        "tags": ["Navigation"],
    },
    {
        "title": "URL Parameters",
        "desc": "Handles path variables, query parameters, current URL parsing, and history-preserving routing transitions.",
        "icon": "link",
        "file": "examples/url_params/app.py",
        "tags": ["Navigation"],
    },
    {
        "title": "Navigation Showcase",
        "desc": "Breadcrumbs, menus, pagination, and command palette.",
        "icon": "compass",
        "file": "examples/navigation_showcase/app.py",
        "tags": ["Navigation"],
    },
    {
        "title": "Sidebar Layout",
        "desc": "Full sidebar navigation with groups and submenus.",
        "icon": "panel-left",
        "file": "examples/sidebar_showcase/app.py",
        "tags": ["Navigation", "Layout"],
    },
    {
        "title": "Dashboard",
        "desc": "Multi-section dashboard with cards and charts.",
        "icon": "layout-dashboard",
        "file": "examples/dashboard/app.py",
        "tags": ["Layout", "Charts"],
    },
    {
        "title": "Kanban Board",
        "desc": "Drag-style column board with task management.",
        "icon": "columns",
        "file": "examples/kanban_board/app.py",
        "tags": ["Layout", "Data"],
    },
    {
        "title": "File Manager",
        "desc": "Tree-style file browser with context menus.",
        "icon": "folder",
        "file": "examples/file_manager/app.py",
        "tags": ["Layout", "Data"],
    },
    {
        "title": "Settings Panel",
        "desc": "Settings form with tabs, switches, and selects.",
        "icon": "settings",
        "file": "examples/settings_panel/app.py",
        "tags": ["Layout"],
    },
    {
        "title": "Resizable Panels",
        "desc": "Imperative client-side and server-side control (collapse, expand, resize) over resizable grid/panel boundaries.",
        "icon": "grip-horizontal",
        "file": "examples/resizable_panels/app.py",
        "tags": ["Layout"],
    },
    {
        "title": "Component Showcase",
        "desc": "Kitchen sink demo of all available components.",
        "icon": "component",
        "file": "examples/component_showcase/app.py",
        "tags": ["Layout"],
    },
    {
        "title": "E-Commerce Product",
        "desc": "Product page with images, variants, and cart.",
        "icon": "shopping-cart",
        "file": "examples/ecommerce_product/app.py",
        "tags": ["Layout"],
    },
    {
        "title": "Weather Dashboard",
        "desc": "A beautiful weather report UI featuring styled cards, layout columns, and dynamically updating weather metrics.",
        "icon": "sun",
        "file": "examples/weather_dashboard/app.py",
        "tags": ["Layout"],
    },
    {
        "title": "AI Chat",
        "desc": "Interactive chat client with sidebar history, tags, resizable panels, and custom tooltips.",
        "icon": "message-square",
        "file": "examples/aichat/app.py",
        "tags": ["Real-time", "Layout"],
    },
    {
        "title": "Analytics Dashboard",
        "desc": "Sleek, modern dashboard featuring sparkline metrics, area/bar/pie charts, and interactive transaction data tables.",
        "icon": "line-chart",
        "file": "examples/analytics_dashboard/app.py",
        "tags": ["Layout", "Charts", "Data"],
    },
    {
        "title": "Chat App",
        "desc": "Real-time chat with broadcasting to connected clients.",
        "icon": "message-square",
        "file": "examples/chat_app/app.py",
        "tags": ["Real-time"],
    },
    {
        "title": "Streaming",
        "desc": "Incremental text streaming with ctx.stream().",
        "icon": "radio",
        "file": "examples/streaming/app.py",
        "tags": ["Real-time"],
    },
    {
        "title": "Real-time Dashboard",
        "desc": "Background tasks broadcasting to all clients.",
        "icon": "activity",
        "file": "examples/realtime_dashboard/app.py",
        "tags": ["Real-time", "Charts"],
    },
    {
        "title": "Scroll Stream",
        "desc": "Renders real-time text streaming inside a scrollable area with sticky-bottom auto-scrolling.",
        "icon": "arrow-down",
        "file": "examples/scroll_stream/app.py",
        "tags": ["Real-time", "Markdown"],
    },
    {
        "title": "Markdown Features",
        "desc": "Renders Markdown text with math formulas (LaTeX) and interactive structural diagrams (Mermaid).",
        "icon": "file-text",
        "file": "examples/markdown_features/app.py",
        "tags": ["Markdown"],
    },
    {
        "title": "Markdown Custom Tags",
        "desc": "Renders custom inline Refast components inside Markdown text with Pydantic type coercion and validation.",
        "icon": "tag",
        "file": "examples/markdown_custom_tags/app.py",
        "tags": ["Markdown", "Advanced"],
    },
    {
        "title": "Charts Showcase",
        "desc": "Bar, line, area, pie, radar, and radial charts.",
        "icon": "bar-chart-3",
        "file": "examples/charts_showcase/app.py",
        "tags": ["Charts"],
    },
    {
        "title": "Data Table",
        "desc": "Sortable, filterable table with pagination.",
        "icon": "table",
        "file": "examples/data_table/app.py",
        "tags": ["Data"],
    },
    {
        "title": "Rich Table",
        "desc": "Combines tables with inline components (badges, progress bars) and DataTable cell component serialization.",
        "icon": "layout-grid",
        "file": "examples/rich_table/app.py",
        "tags": ["Data"],
    },
    {
        "title": "Toast Showcase",
        "desc": "All toast variants, positions, and configurations.",
        "icon": "bell",
        "file": "examples/toast_showcase/app.py",
        "tags": ["Utility"],
    },
    {
        "title": "Theme Showcase",
        "desc": "Theme switching, presets, and custom themes.",
        "icon": "palette",
        "file": "examples/theme_showcase/app.py",
        "tags": ["Utility"],
    },
    {
        "title": "Connection Status",
        "desc": "WebSocket connection monitoring component.",
        "icon": "wifi",
        "file": "examples/connection_status/app.py",
        "tags": ["Utility"],
    },
    {
        "title": "Colors Showcase",
        "desc": "All semantic color tokens and their usage.",
        "icon": "paintbrush",
        "file": "examples/colors_showcase/app.py",
        "tags": ["Utility"],
    },
    {
        "title": "JS Callbacks",
        "desc": "Client-side JS without server roundtrip.",
        "icon": "code",
        "file": "examples/js_callbacks/app.py",
        "tags": ["Advanced"],
    },
    {
        "title": "Long Running Tasks",
        "desc": "Background job with progress and targeted DOM updates.",
        "icon": "clock",
        "file": "examples/longrunning.py",
        "tags": ["Advanced", "Real-time"],
    },
    {
        "title": "Component Refresh",
        "desc": "Demonstrates full page vs. targeted partial DOM refreshes using target_id in callbacks.",
        "icon": "refresh-cw",
        "file": "examples/component_refresh/app.py",
        "tags": ["Advanced"],
    },
    {
        "title": "File Transfer",
        "desc": "Dropzone uploader, progress indicators, CSV exports, and programmatic downloads via trigger_download.",
        "icon": "upload-cloud",
        "file": "examples/file_transfer/app.py",
        "tags": ["Advanced"],
    },
    {
        "title": "Lazy Loading",
        "desc": "Refast bundle size optimization by configuring on-demand chunk loading (preloaded_features) for heavy components.",
        "icon": "zap",
        "file": "examples/lazy_loading/app.py",
        "tags": ["Advanced"],
    },
    {
        "title": "Desktop App Wrapper",
        "desc": "Wraps a Refast application inside a pywebview frame to run as a native desktop application with OS dialog integrations.",
        "icon": "monitor",
        "file": "examples/desktop_app.py",
        "tags": ["Desktop", "Advanced"],
    },
    {
        "title": "Desktop Notifications",
        "desc": "Triggers and configures native desktop notifications with interactive click and dismissal callbacks.",
        "icon": "bell",
        "file": "examples/desktop_notifications.py",
        "tags": ["Desktop", "Utility"],
    },
]


async def _nav(ctx: Context, path):
    """Navigate to example page."""
    await ctx.redirect(f"https://github.com/idling-mind/refast/tree/main/{path}")


async def handle_search(ctx: Context, value: str):
    """Save the search query and refresh the grid."""
    ctx.store.local["examples_search"] = value
    await ctx.refresh(target_id="examples-grid-container")


async def select_category(ctx: Context, category: str):
    """Save the selected category filter and refresh the grid."""
    ctx.store.local["examples_category"] = category
    await ctx.refresh(target_id="examples-grid-container")
    await ctx.refresh(target_id="category-tabs")


async def clear_filters(ctx: Context):
    """Clear all filters and search queries."""
    ctx.store.local["examples_search"] = ""
    ctx.store.local["examples_category"] = "All"
    await ctx.refresh(target_id="examples-grid-container")
    await ctx.refresh(target_id="category-tabs")


def matches_category(example_tags, selected_category):
    """Check if an example matches the selected category filter."""
    if selected_category == "All":
        return True
    elif selected_category == "Basic":
        return "Basic" in example_tags
    elif selected_category == "Layout & Navigation":
        return "Layout" in example_tags or "Navigation" in example_tags
    elif selected_category == "Data & Charts":
        return "Data" in example_tags or "Charts" in example_tags
    elif selected_category == "Real-time & Markdown":
        return "Real-time" in example_tags or "Markdown" in example_tags
    elif selected_category == "Advanced & Desktop":
        return "Advanced" in example_tags or "Desktop" in example_tags or "Utility" in example_tags
    return False


def matches_search(ex, query):
    """Check if an example matches the search query string."""
    if not query:
        return True
    q = query.lower()
    return (
        q in ex["title"].lower()
        or q in ex["desc"].lower()
        or q in ex["file"].lower()
        or any(q in tag.lower() for tag in ex.get("tags", []))
    )


def render(ctx):
    """Render the examples gallery page."""
    from docs.app import docs_layout

    # Retrieve current filter states from store
    selected_category = ctx.store.local.get("examples_category", "All")
    search_query = ctx.store.local.get("examples_search", "")

    # Clean categories to ensure store value is valid
    if selected_category not in CATEGORIES:
        selected_category = "All"

    # Filter examples
    filtered = [
        ex
        for ex in EXAMPLES
        if matches_category(ex["tags"], selected_category)
        and matches_search(ex, search_query)
    ]

    # Category Tab Pills
    category_tabs = Row(
        id="category-tabs",
        gap=2,
        class_name="flex-wrap items-center",
        children=[
            Button(
                label=cat,
                variant="secondary" if selected_category == cat else "ghost",
                class_name=(
                    "rounded-full px-4 py-1 text-sm font-medium transition-all cursor-pointer "
                    f"{'bg-primary text-primary-foreground shadow-sm hover:bg-primary/90' if selected_category == cat else 'text-muted-foreground hover:text-foreground'}"
                ),
                on_click=ctx.callback(select_category, category=cat),
            )
            for cat in CATEGORIES
        ]
    )

    # Search Bar
    search_bar = Container(
        class_name="w-full md:w-80",
        children=[
            Input(
                placeholder="Search examples...",
                value=search_query,
                debounce=200,
                on_change=ctx.callback(handle_search),
                class_name="w-full rounded-full",
            )
        ]
    )

    # Info bar showing results count and clear option
    info_row = Row(
        justify="between",
        align="center",
        class_name="mb-6 px-1 text-sm text-muted-foreground",
        children=[
            Text(
                f"Showing {len(filtered)} of {len(EXAMPLES)} examples",
                class_name="font-medium",
            ),
            Button(
                label="Clear filters",
                variant="link",
                class_name="h-auto p-0 text-xs text-primary hover:underline",
                on_click=ctx.callback(clear_filters),
            )
            if (search_query or selected_category != "All")
            else Container(),
        ],
    )

    # Main Grid of Cards or Empty State
    if filtered:
        grid_content = Grid(
            columns="repeat(auto-fit, minmax(280px, 1fr))",
            gap=4,
            children=[
                Link(
                    href=f"https://github.com/idling-mind/refast/tree/main/{ex['file']}",
                    target="_blank",
                    variant="unstyled",
                    class_name="block h-full hover:no-underline",
                    children=[
                        Card(
                            class_name="hover:border-primary hover:shadow-md transition-all duration-200 bg-card/65 flex flex-col h-full",
                            children=[
                                CardHeader(
                                    class_name="pb-2 flex-grow-0",
                                    children=[
                                        Row(
                                            gap=2,
                                            align="center",
                                            children=[
                                                Icon(ex["icon"], size=16, class_name="text-primary"),
                                                CardTitle(ex["title"], class_name="text-base font-semibold"),
                                            ],
                                        ),
                                    ],
                                ),
                                CardContent(
                                    class_name="flex-1 flex flex-col justify-between pt-0 pb-4",
                                    children=[
                                        Text(
                                            ex["desc"],
                                            class_name="text-xs text-muted-foreground leading-relaxed flex-1 mb-4",
                                        ),
                                        Row(
                                            gap=1.5,
                                            class_name="flex-wrap mt-auto pt-3 border-t border-muted/30",
                                            children=[
                                                Badge(
                                                    tag,
                                                    variant="secondary",
                                                    class_name="text-[10px] px-2 py-0 font-normal bg-secondary/60 text-secondary-foreground border-0",
                                                )
                                                for tag in ex["tags"]
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                )
                for ex in filtered
            ],
        )
    else:
        grid_content = Card(
            class_name="p-10 text-center flex flex-col items-center justify-center border-dashed border-2 bg-card/20",
            children=[
                Icon("search", size=32, class_name="text-muted-foreground mb-3"),
                Heading("No examples match your filter", level=3, class_name="text-base font-semibold"),
                Text(
                    "Try checking your keywords or switching to a different category tab.",
                    class_name="text-xs text-muted-foreground mt-1 mb-4",
                ),
                Button(
                    "Reset Filters",
                    variant="outline",
                    class_name="rounded-full text-xs px-4",
                    on_click=ctx.callback(clear_filters),
                ),
            ],
        )

    # Combine everything
    content = Container(
        class_name="max-w-5xl mx-auto p-6 space-y-6",
        children=[
            Container(
                children=[
                    Heading(PAGE_TITLE, level=1, class_name="text-3xl font-extrabold tracking-tight"),
                    Text(
                        "Explore working examples demonstrating the full capabilities of the Refast framework.",
                        class_name="text-sm text-muted-foreground mt-1",
                    ),
                ]
            ),
            Separator(class_name="my-4"),
            # Interactive Filter controls row
            Column(
                align="center",
                justify="between",
                gap=4,
                # class_name="flex-col md:flex-row gap-4 mb-2 items-stretch md:items-center",
                children=[
                    category_tabs,
                    search_bar,
                ],
            ),
            # Target container for AJAX refreshing
            Container(
                id="examples-grid-container",
                class_name="min-h-[200px]",
                children=[
                    info_row,
                    grid_content,
                ],
            ),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)
