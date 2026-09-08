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
    "Extensions",
]

EXAMPLES = [
    # ── Basic ─────────────────────────────────────────────────────────────
    {
        "title": "Hello World",
        "desc": "Minimal Refast app — one page, one component with reactive state and greeting updates.",
        "icon": "hand-metal",
        "route": "/examples/hello",
        "code_url": "https://github.com/idling-mind/refast/blob/main/examples/hello.py",
        "tags": ["Basic"],
    },
    {
        "title": "Interactive Counter",
        "desc": "Clean counter demonstrating page routing, button callbacks, direct number input, and reactive state updates.",
        "icon": "plus",
        "route": "/examples/counter",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/basic",
        "tags": ["Basic"],
    },
    {
        "title": "Todo Task Manager",
        "desc": "Complete task management app with task creation, completion toggles, targeted DOM replacement, and toast alerts.",
        "icon": "check-circle-2",
        "route": "/docs/todo-live",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/todo_app",
        "tags": ["Basic"],
    },
    {
        "title": "All Form Inputs Showcase",
        "desc": "Unified showcase of standard and advanced form controls submitting to a single server callback: inputs, selects, sliders, date pickers, and switches.",
        "icon": "text-cursor-input",
        "route": "/examples/all-inputs",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/all_inputs_form",
        "tags": ["Basic", "Forms"],
    },
    {
        "title": "Form Validation & Alerts",
        "desc": "User registration form demonstrating client & server validation logic, dynamic error banners, and success feedback with Alert.",
        "icon": "shield-check",
        "route": "/examples/form-validation",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/form_validation",
        "tags": ["Basic", "Forms"],
    },
    {
        "title": "Enhanced Input Features",
        "desc": "Deep dive into Input component features: debounced keystrokes, inline validation error states, labels with required markers, and description hints.",
        "icon": "edit-3",
        "route": "/examples/input-features",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/input_features",
        "tags": ["Basic"],
    },
    {
        "title": "SPA Multi-Page App",
        "desc": "Single Page Application architecture with a shared Navbar layout and instant view swapping conditioned on session state without page reloads.",
        "icon": "layout",
        "route": "/examples/multi-page",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/multi_page",
        "tags": ["Basic", "Navigation"],
    },
    {
        "title": "Bookstore URL Routing & Params",
        "desc": "Full routing demo featuring typed path parameters (/books/{id:int}), slug parameters, and search query strings with browser history preservation.",
        "icon": "route",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/url_params",
        "tags": ["Basic", "Navigation"],
    },

    # ── Layout & Navigation ───────────────────────────────────────────────
    {
        "title": "Resizable Panels",
        "desc": "Draggable multi-panel layouts with collapsible sidebars and imperative client/server resize methods via ctx.bound_js().",
        "icon": "columns",
        "route": "/examples/resizable-panels",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/resizable_panels",
        "tags": ["Layout"],
    },
    {
        "title": "Settings Panel",
        "desc": "Multi-section settings interface featuring sidebar navigation, avatar upload, switch toggles, radio groups, and toast feedback.",
        "icon": "settings",
        "route": "/examples/settings-panel",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/settings_panel",
        "tags": ["Layout", "Forms"],
    },
    {
        "title": "Sidebar Showcase",
        "desc": "Collapsible and responsive desktop sidebars with nested menu groups, active route highlights, badges, and icon indicators.",
        "icon": "panel-left",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/sidebar_showcase",
        "tags": ["Layout", "Navigation"],
    },
    {
        "title": "Bound Overlays & Drawers",
        "desc": "Sheet, Drawer, and Dialog overlay primitives controlled imperatively via Python callbacks and bound JS actions.",
        "icon": "layers",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/bound_overlays",
        "tags": ["Layout"],
    },
    {
        "title": "Navigation Showcase",
        "desc": "Header navigation bars, responsive breadcrumbs, pagination controls, and active link states across desktop and mobile.",
        "icon": "compass",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/navigation_showcase",
        "tags": ["Navigation"],
    },
    {
        "title": "Tabs Sizing & Alignment",
        "desc": "Multi-tab content panels with custom tab bar sizing, horizontal scrolling, icon tabs, and reactive panel switching.",
        "icon": "layout-grid",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/tabs_sizing",
        "tags": ["Layout"],
    },

    # ── Data & Charts ─────────────────────────────────────────────────────
    {
        "title": "Weather Dashboard",
        "desc": "Multi-city live weather monitoring cards with dynamic temperature gauges, condition badges, and data refresh callbacks.",
        "icon": "cloud",
        "route": "/examples/weather",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/weather",
        "tags": ["Data"],
    },
    {
        "title": "Analytics Dashboard",
        "desc": "Executive business metrics dashboard featuring KPI cards, revenue summaries, period filters, and activity timelines.",
        "icon": "bar-chart-3",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/analytics_dashboard",
        "tags": ["Data", "Charts"],
    },
    {
        "title": "Charts Showcase",
        "desc": "Interactive data visualisations with bar charts, line plots, area graphs, and customizable theme palettes.",
        "icon": "line-chart",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/charts",
        "tags": ["Charts", "Data"],
    },
    {
        "title": "Data Table",
        "desc": "Structured tabular data display with typed column formats, striped rows, empty states, and action triggers.",
        "icon": "table",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/data_table",
        "tags": ["Data"],
    },
    {
        "title": "Rich Table (Sort & Filter)",
        "desc": "Advanced data table supporting client and server-side column sorting, multi-column search, pagination, and row selection.",
        "icon": "table",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/rich_table",
        "tags": ["Data"],
    },

    # ── Real-time & Markdown ──────────────────────────────────────────────
    {
        "title": "Markdown Features",
        "desc": "Full GitHub-flavored Markdown rendering with lazy-loaded interactive Mermaid SVG diagrams and LaTeX KaTeX math formulas.",
        "icon": "code",
        "route": "/examples/markdown-features",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/markdown_features",
        "tags": ["Markdown"],
    },
    {
        "title": "Scroll-Stream Markdown",
        "desc": "Real-time token streaming into Markdown inside a ScrollArea with automatic sticky-to-bottom tracking and manual override.",
        "icon": "arrow-down",
        "route": "/examples/scroll-stream",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/scroll_stream",
        "tags": ["Real-time", "Markdown"],
    },
    {
        "title": "AI Chat Interface",
        "desc": "Conversational LLM assistant UI with message bubbles, avatar indicators, token streaming, and scroll lock.",
        "icon": "bot",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/ai_chat",
        "tags": ["Real-time", "AI"],
    },
    {
        "title": "Markdown Custom Tags",
        "desc": "Extending standard Markdown syntax with custom HTML components, callout alert blocks, and styled badges.",
        "icon": "code-2",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/markdown_custom_tags",
        "tags": ["Markdown"],
    },
    {
        "title": "Collapsible Stream",
        "desc": "Dynamic thought/reasoning chains and expandable step logs streaming live content into collapsible disclosure sections.",
        "icon": "layout-list",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/collapsible_stream",
        "tags": ["Real-time", "Markdown"],
    },
    {
        "title": "Real-time Dashboard",
        "desc": "Live server-push telemetry dashboard updating system metrics, memory gauges, and event counters over WebSockets.",
        "icon": "activity",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/realtime_dashboard",
        "tags": ["Real-time", "Data"],
    },
    {
        "title": "Chat Application",
        "desc": "Multi-client WebSocket chat application with user channels, online participant presence, and message broadcasts.",
        "icon": "message-circle",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/chat_app",
        "tags": ["Real-time"],
    },

    # ── Advanced & Desktop ────────────────────────────────────────────────
    {
        "title": "Kanban Board",
        "desc": "Full task management board with customizable columns, priority tags, assignee avatars, and creation sheets.",
        "icon": "layout",
        "route": "/examples/kanban",
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/kanban_board",
        "tags": ["Advanced"],
    },
    {
        "title": "File Manager",
        "desc": "Desktop-style file browser with folder navigation trees, file grid views, size calculations, and breadcrumbs.",
        "icon": "folder",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/file_manager",
        "tags": ["Advanced"],
    },
    {
        "title": "E-Commerce Catalog",
        "desc": "Product store with category filtering, price sliders, image carousels, shopping cart drawer, and order checkout.",
        "icon": "shopping-bag",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/ecommerce_product",
        "tags": ["Advanced"],
    },
    {
        "title": "Prop Store Optimization",
        "desc": "Techniques for extreme rendering performance using targeted DOM prop updates instead of full component tree re-renders.",
        "icon": "database",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/prop_store",
        "tags": ["Advanced", "Performance"],
    },
    {
        "title": "JS Callbacks",
        "desc": "Direct client-side JavaScript execution, window event bindings, and imperative DOM interactions via ctx.bound_js().",
        "icon": "terminal",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/js_callbacks",
        "tags": ["Advanced"],
    },
    {
        "title": "File Transfer & Upload",
        "desc": "Robust file uploads with drag-and-drop dropzones, progress bar updates, file type filters, and chunked transfer.",
        "icon": "upload",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/file_transfer",
        "tags": ["Advanced"],
    },
    {
        "title": "Desktop Native App",
        "desc": "Packaging a Refast application as a standalone native desktop GUI window using PyWebView with zero web browser UI.",
        "icon": "monitor",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/desktop_app",
        "tags": ["Desktop"],
    },
    {
        "title": "Desktop Notifications",
        "desc": "Triggering OS-level system tray and desktop push notifications from server-side Python events.",
        "icon": "bell",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/desktop_notifications",
        "tags": ["Desktop"],
    },
    {
        "title": "Long-Running Tasks",
        "desc": "Managing asynchronous background jobs with live progress bars, cancellation triggers, and completion alerts.",
        "icon": "timer",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/long_running_task",
        "tags": ["Advanced"],
    },
    {
        "title": "Theme Customization",
        "desc": "Live theme swapping with Refast CSS variables, custom color palettes, and seamless dark/light mode switching.",
        "icon": "palette",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/theme_showcase",
        "tags": ["Advanced"],
    },
    {
        "title": "Event Modifiers",
        "desc": "Optimizing user input latency and server load using event debounce, throttle, and preventDefault decorators.",
        "icon": "mouse-pointer-click",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/event_modifiers",
        "tags": ["Advanced"],
    },
    {
        "title": "Custom Extensions",
        "desc": "Building third-party React and Python extensions with custom entry points, npm bundling, and asset pipelines.",
        "icon": "puzzle",
        "route": None,
        "code_url": "https://github.com/idling-mind/refast/tree/main/examples/custom_extension",
        "tags": ["Advanced"],
    },

    # ── Official Extensions ───────────────────────────────────────────────
    {
        "title": "ECharts Visualizations",
        "desc": "Apache ECharts integration with 20+ interactive chart types, real-time setOption updates, and mouse events.",
        "icon": "bar-chart-2",
        "route": "/examples/echarts",
        "code_url": "https://github.com/idling-mind/refast-echarts",
        "tags": ["Extensions", "Data & Charts"],
    },
    {
        "title": "Spreadsheet Data Grid",
        "desc": "Excel-like spreadsheet component based on ReactGrid with 15+ cell types, inline editing, and sticky totals.",
        "icon": "grid-3x3",
        "route": "/examples/grid",
        "code_url": "https://github.com/idling-mind/refast_grid",
        "tags": ["Extensions", "Advanced"],
    },
    {
        "title": "3D VTK.js Visualization",
        "desc": "Hardware-accelerated 3D rendering with react-vtk-js: polygonal meshes, volume rendering, and coordinate picking.",
        "icon": "box",
        "route": "/examples/vtk-js",
        "code_url": "https://github.com/idling-mind/refast_vtk_js",
        "tags": ["Extensions", "Advanced"],
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
        return "Real-time" in example_tags or "Markdown" in example_tags or "AI" in example_tags
    elif selected_category == "Advanced & Desktop":
        return "Advanced" in example_tags or "Desktop" in example_tags or "Performance" in example_tags
    elif selected_category == "Extensions":
        return "Extensions" in example_tags or "Extension" in example_tags
    return False


def matches_search(ex, query):
    """Check if an example matches the search query string."""
    if not query:
        return True
    q = query.lower()
    return (
        q in (ex.get("title") or "").lower()
        or q in (ex.get("desc") or "").lower()
        or q in (ex.get("route") or "").lower()
        or any(q in (tag or "").lower() for tag in ex.get("tags", []) if tag)
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
                Card(
                    class_name="hover:border-primary hover:shadow-md transition-all duration-200 bg-card/65 flex flex-col h-full",
                    children=[
                        CardHeader(
                            class_name="pb-2 flex-grow-0 space-y-2",
                            children=[
                                Row(
                                    gap=2,
                                    align="center",
                                    children=[
                                        Icon(ex["icon"], size=16, class_name="text-primary flex-shrink-0"),
                                        CardTitle(ex["title"], class_name="text-base font-semibold"),
                                    ],
                                ),
                                Row(
                                    gap=1.5,
                                    class_name="flex-wrap",
                                    children=[
                                        Badge(
                                            tag,
                                            variant="secondary",
                                            class_name="text-[10px] px-2 py-0.5 font-medium border border-border/40",
                                        )
                                        for tag in ex["tags"]
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
                                    gap=2.5,
                                    justify="end",
                                    align="center",
                                    class_name="mt-auto pt-3 border-t border-muted/30",
                                    children=[
                                        Link(
                                            text="Launch Demo",
                                            href=ex["route"],
                                            target="_blank",
                                            class_name="inline-flex items-center justify-center rounded-md text-xs font-semibold bg-primary text-primary-foreground hover:bg-primary/90 h-8 px-3.5 whitespace-nowrap transition-colors shadow-sm cursor-pointer",
                                        )
                                        if ex.get("route")
                                        else None,
                                        Link(
                                            text="View Code",
                                            href=ex["code_url"],
                                            target="_blank",
                                            class_name="inline-flex items-center justify-center rounded-md text-xs font-semibold border border-input bg-background hover:bg-accent hover:text-accent-foreground h-8 px-3.5 whitespace-nowrap transition-colors shadow-sm cursor-pointer",
                                        ),
                                    ],
                                ),
                            ],
                        ),
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
