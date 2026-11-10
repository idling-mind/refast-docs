"""Row — /docs/components/row."""

from refast import Context
from refast.components import (
    Button,
    Column,
    Row,
    Select,
    Text,
)
from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import playground_card

PAGE_METADATA = {
    "title": "Row",
    "route": "/docs/components/row",
    "icon": "rows",
    "group": "Layout",
    "order": 1,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_justify(ctx: Context, value: str):
    ctx.state.set("row_justify", value)
    await ctx.refresh()


async def _set_align(ctx: Context, value: str):
    ctx.state.set("row_align", value)
    await ctx.refresh()


async def _set_gap(ctx: Context, value: str):
    ctx.state.set("row_gap", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    justify = ctx.state.get("row_justify", "start")
    align = ctx.state.get("row_align", "start")
    gap = int(ctx.state.get("row_gap", "2"))

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("justify", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in [
                                "start",
                                "end",
                                "center",
                                "between",
                                "around",
                                "evenly",
                            ]
                        ],
                        value=justify,
                        on_change=ctx.callback(_set_justify),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("align", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in [
                                "start",
                                "end",
                                "center",
                                "stretch",
                                "baseline",
                            ]
                        ],
                        value=align,
                        on_change=ctx.callback(_set_align),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("gap", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["1", "2", "4", "6", "8"]
                        ],
                        value=str(gap),
                        on_change=ctx.callback(_set_gap),
                    ),
                ],
            ),
        ],
        preview=[
            Row(
                justify=justify,
                align=align,
                gap=gap,
                children=[
                    Button("Item 1", variant="outline"),
                    Button("Item 2", variant="outline"),
                    Button("Item 3", variant="outline"),
                ],
            )
        ],
        preview_class="border rounded-lg p-4 bg-muted/30 min-h-[80px]",
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
Horizontal flex container (`flex flex-row`) for arranging children side by side.

```python
from refast.components import Row

Row(
    children=[Button("Save"), Button("Cancel", variant="outline")],
    justify="end",
    align="center",
    gap=2,
)
```
"""

REFERENCE = r"""
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Child components |
| `justify` | `"start" \| "end" \| "center" \| "between" \| "around" \| "evenly"` | `"start"` | justify-content |
| `align` | `"start" \| "end" \| "center" \| "stretch" \| "baseline"` | `"start"` | align-items |
| `gap` | `int` | `2` | Gap between children (Tailwind spacing unit) |
| `wrap` | `bool` | `False` | Whether children wrap |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Examples

```python
# Spaced action bar
Row(
    justify="between",
    align="center",
    children=[
        Heading("Page Title", level=2),
        Row(gap=2, children=[Button("New"), Button("Settings", variant="ghost")]),
    ],
)

# Wrapping tag list
Row(
    wrap=True,
    gap=2,
    children=[Badge(children=[tag]) for tag in tags],
)
```
"""
