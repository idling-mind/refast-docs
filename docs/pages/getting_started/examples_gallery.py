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
        "route": "/examples/hello",
        "code_url": "https://github.com/idling-mind/refast-docs/blob/main/docs/examples/hello.py",
        "tags": ["Basic"],
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
        or q in ex.get("route", "").lower()
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
                                    gap=4,
                                    justify="between",
                                    align="center",
                                    class_name="mt-auto pt-3 border-t border-muted/30",
                                    children=[
                                        # Left side: tags
                                        Row(
                                            gap=1.5,
                                            class_name="flex-wrap",
                                            children=[
                                                Badge(
                                                    tag,
                                                    variant="secondary",
                                                    class_name="text-[10px] px-2 py-0 font-normal bg-secondary/60 text-secondary-foreground border-0",
                                                )
                                                for tag in ex["tags"]
                                            ],
                                        ),
                                        # Right side: Action links
                                        Row(
                                            gap=3,
                                            children=[
                                                Link(
                                                    text="Launch Demo",
                                                    href=ex["route"],
                                                    target="_blank",
                                                    class_name="inline-flex items-center justify-center rounded-md text-xs font-semibold bg-primary text-primary-foreground hover:bg-primary/90 h-8 px-3 transition-colors shadow-sm cursor-pointer",
                                                ),
                                                Link(
                                                    text="View Code",
                                                    href=ex["code_url"],
                                                    target="_blank",
                                                    class_name="inline-flex items-center justify-center rounded-md text-xs font-semibold border border-input bg-background hover:bg-accent hover:text-accent-foreground h-8 px-3 transition-colors shadow-sm cursor-pointer",
                                                ),
                                            ],
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
