"""ScrollArea — /docs/components/scroll-area."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    ScrollArea,
    Select,
    Separator,
    Text,
)
from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import playground_card

PAGE_METADATA = {
    "title": "Scroll Area",
    "route": "/docs/components/scroll-area",
    "icon": "layout-list",
    "group": "Layout",
    "order": 5,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_type(ctx: Context, value: str):
    ctx.state.set("sa_type", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    scroll_type = ctx.state.get("sa_type", "hover")

    items = [
        "JavaScript",
        "TypeScript",
        "Python",
        "Rust",
        "Go",
        "Java",
        "C++",
        "Swift",
        "Kotlin",
        "Ruby",
        "Scala",
        "Haskell",
        "Elixir",
        "Clojure",
        "Dart",
    ]

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("type", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["auto", "always", "scroll", "hover"]
                        ],
                        value=scroll_type,
                        on_change=ctx.callback(_set_type),
                    ),
                ],
            ),
        ],
        preview=[
            Text(
                "Hover over the area or scroll inside it to see the scrollbar:",
                class_name="text-sm text-muted-foreground mb-2",
            ),
            ScrollArea(
                type=scroll_type,
                class_name="border rounded-lg",
                style={"height": "12rem", "width": "16rem"},
                children=[
                    Column(
                        gap=1,
                        class_name="p-3",
                        children=[
                            Container(
                                class_name="py-1 px-2 rounded text-sm hover:bg-muted cursor-default",
                                children=[Text(item)],
                            )
                            for item in items
                        ],
                    )
                ],
            ),
        ],
        preview_class="",
    )


def render(ctx: Context):
    return render_doc_page(
        ctx,
        title=PAGE_TITLE,
        route=PAGE_ROUTE,
        intro=INTRO,
        playground=_playground(ctx),
        reference=REFERENCE,
    )


INTRO = """
A scrollable container with custom, styled scrollbars (Radix UI `ScrollArea`).

```python
from refast.components import ScrollArea

ScrollArea(
    class_name="h-72 w-48",
    children=[
        # tall content here
    ]
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list | Component | None` | `None` | Scrollable content |
| `type` | `"auto" | "always" | "scroll" | "hover"` | `"hover"` | When the scrollbar is visible |
| `scroll_hide_delay` | `int` | `600` | ms before scrollbar hides (hover/scroll modes) |
| `dir` | `"ltr" | "rtl" | None` | `None` | Reading direction (inherits from document) |
| `stick_to_bottom` | `bool` | `False` | Auto-scroll to bottom as content updates |
| `scroll_direction` | `"both" | "vertical" | "horizontal"` | `"both"` | Restrict scrolling direction |
| `id` | `str | None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes (use for height/width) |


## Notes

Always set a height via `class_name` (e.g. `h-72`). The `type` prop controls
scrollbar visibility:

- `"hover"` — shows on mouse hover  
- `"auto"` — shows when content overflows  
- `"always"` — always visible  
- `"scroll"` — shows while actively scrolling  

## Examples

```python
# Vertical list in a fixed height box
ScrollArea(
    class_name="h-80",
    children=[Column(gap=1, children=[Text(item) for item in long_list])],
)

# Horizontal scroll
ScrollArea(
    class_name="w-full",
    children=[
        Row(
            gap=4,
            class_name="w-max",
            children=[Card(...) for _ in range(20)],
        )
    ],
)
```
"""
