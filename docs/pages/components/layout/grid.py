"""Grid — /docs/components/grid."""

from refast import Context
from refast.components import (
    Column,
    Container,
    Grid,
    Select,
    Text,
)
from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import playground_card

PAGE_METADATA = {
    "title": "Grid",
    "route": "/docs/components/grid",
    "icon": "layout-grid",
    "group": "Layout",
    "order": 4,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_cols(ctx: Context, value: str):
    ctx.state.set("gr_cols", value)
    await ctx.refresh()


async def _set_gap(ctx: Context, value: str):
    ctx.state.set("gr_gap", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    cols = int(ctx.state.get("gr_cols", "3"))
    gap = int(ctx.state.get("gr_gap", "4"))

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("columns", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["1", "2", "3", "4", "5", "6"]
                        ],
                        value=str(cols),
                        on_change=ctx.callback(_set_cols),
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
                            for v in ["1", "2", "4", "6"]
                        ],
                        value=str(gap),
                        on_change=ctx.callback(_set_gap),
                    ),
                ],
            ),
        ],
        preview=[
            Grid(
                columns=cols,
                gap=gap,
                children=[
                    Container(
                        class_name="border rounded-md p-3 bg-background text-center text-sm font-medium",
                        children=[Text(f"Cell {i + 1}")],
                    )
                    for i in range(cols * 2)
                ],
            )
        ],
        preview_class="border rounded-lg p-4 bg-muted/30",
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
CSS Grid container for equal-column layouts.

```python
from refast.components import Grid

Grid(
    columns=3,
    gap=4,
    children=[Card(...) for _ in range(6)],
)
```
"""

REFERENCE = r"""
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Grid cell components |
| `columns` | `int \| str` | `1` | Number of equal columns, or a CSS `gridTemplateColumns` string |
| `rows` | `int \| str \| None` | `None` | Number of equal rows, or a CSS `gridTemplateRows` string |
| `gap` | `int` | `4` | Gap between cells (Tailwind spacing unit) |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Advanced: Custom Template

Pass a CSS string to `columns` or `rows` for custom sizing:

```python
Grid(
    columns="200px 1fr 200px",
    gap=4,
    children=[sidebar, main, aside],
)
```

## Examples

```python
# 3-column card grid
Grid(
    columns=3,
    gap=6,
    class_name="max-w-5xl",
    children=[
        Card(children=[CardHeader(title=title)])
        for title in ["Alpha", "Beta", "Gamma"]
    ],
)
```
"""
