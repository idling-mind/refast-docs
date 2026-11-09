"""Separator — /docs/components/separator."""

from refast import Context
from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import playground_card
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_METADATA = {
    "title": "Separator",
    "route": "/docs/components/separator",
    "icon": "minus",
    "group": "Utility",
    "order": 2,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_orientation(ctx: Context, value: str):
    ctx.state.set("sep_orientation", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    orientation = ctx.state.get("sep_orientation", "horizontal")

    is_vertical = orientation == "vertical"

    if is_vertical:
        preview = Row(
            gap=4,
            align="center",
            class_name="h-12",
            children=[
                Text("Left content", class_name="text-sm"),
                Separator(orientation="vertical", class_name="h-full"),
                Text("Right content", class_name="text-sm"),
            ],
        )
    else:
        preview = Column(
            gap=3,
            children=[
                Text("Above the separator", class_name="text-sm"),
                Separator(orientation="horizontal"),
                Text("Below the separator", class_name="text-sm"),
            ],
        )

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Orientation", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["horizontal", "vertical"]
                        ],
                        value=orientation,
                        on_change=ctx.callback(_set_orientation),
                    ),
                ],
            ),
        ],
        preview=[preview],
        code=Markdown(
            content=(
                f"```python\n"
                f'Separator(orientation="{orientation}")\n'
                f"```"
            )
        ),
        preview_class="border rounded-lg p-6 bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    return render_doc_page(
        ctx,
        title=PAGE_TITLE,
        route=PAGE_ROUTE,
        intro=INTRO,
        playground=_playground(ctx),
        reference=REFERENCE,
    )


# ── Content ───────────────────────────────────────────────────────────────

INTRO = """
A thin visual divider between sections of content. Supports both
horizontal and vertical orientations.

```python
from refast.components import Separator

Separator()                              # default: horizontal
Separator(orientation="vertical", class_name="h-6")
```
"""

REFERENCE = r"""
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Axis of the separator line |
| `decorative` | `bool` | `True` | When `True`, hidden from the accessibility tree |
| `class_name` | `str` | `""` | Extra Tailwind classes (e.g. `"h-6"` for vertical) |

## Horizontal (default)

```python
Column(
    gap=4,
    children=[
        Heading("Section One", level=3),
        Paragraph("Content of section one."),
        Separator(),
        Heading("Section Two", level=3),
        Paragraph("Content of section two."),
    ]
)
```

## Vertical

Use a `class_name` to constrain the height or let it fill flexbox height.

```python
Row(
    align="center",
    gap=4,
    class_name="h-10",
    children=[
        Text("Item A"),
        Separator(orientation="vertical"),
        Text("Item B"),
        Separator(orientation="vertical"),
        Text("Item C"),
    ]
)
```

## Non-decorative (Semantic)

For content where the separator has meaning (e.g. separating form sections):

```python
Separator(decorative=False)
```
"""
