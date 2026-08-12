"""Tooltip — /docs/components/tooltip.

Interactive reference page for the Tooltip component.
"""

from refast import Context
from refast.components import (
    Button,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Input,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
    Tooltip,
)
from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import playground_card

PAGE_METADATA = {
    "title": "Tooltip",
    "route": "/docs/components/tooltip",
    "icon": "info",
    "group": "Data Display",
    "order": 6,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_side(ctx: Context, value: str):
    ctx.state.set("ttp_side", value)
    await ctx.refresh()


async def _set_content(ctx: Context, value: str):
    ctx.state.set("ttp_content", value)
    await ctx.refresh()


async def _noop(ctx: Context):
    pass


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    side = ctx.state.get("ttp_side", "top")
    content = ctx.state.get("ttp_content", "This is a helpful tooltip.")

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Side", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "top", "label": "top"},
                            {"value": "right", "label": "right"},
                            {"value": "bottom", "label": "bottom"},
                            {"value": "left", "label": "left"},
                        ],
                        value=side,
                        on_change=ctx.callback(_set_side),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Tooltip content", class_name="text-sm font-medium"),
                    Input(
                        value=content,
                        placeholder="Tooltip text…",
                        on_change=ctx.callback(_set_content),
                    ),
                ],
            ),
        ],
        preview=[
            Tooltip(
                content=content or "Tooltip text",
                side=side,
                children=[
                    Button(
                        "Hover over me",
                        variant="outline",
                        on_click=ctx.callback(_noop),
                    )
                ],
            )
        ],
        code=Markdown(
            content=(
                "```python\n"
                "Tooltip(\n"
                f'    content="{content or "Tooltip text"}",\n'
                f'    side="{side}",\n'
                "    children=[Button(\"Hover over me\")],\n"
                ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-8 flex items-center justify-center bg-muted/30",
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
A hover tooltip that wraps any trigger element. The `content` string is
shown in a floating popover when the user hovers over the child.

```python
from refast.components import Tooltip, Button

Tooltip(
    content="This action cannot be undone.",
    children=[Button("Delete", variant="destructive")],
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `str` | *(required)* | Plain-text tooltip message. |
| `children` | `list` | `[]` | The trigger element(s). Typically a single component. |
| `side` | `"top" | "right" | "bottom" | "left"` | `"top"` | Preferred side of the trigger to display the tooltip. |
| `side_offset` | `int | None` | `None` | Pixel gap between the trigger and the tooltip. |
| `class_name` | `str` | `""` | Extra Tailwind classes applied to the tooltip content. |

## All sides

```python
Row(gap=4, children=[
    Tooltip(content="Top",    side="top",    children=[Button("Top")]),
    Tooltip(content="Right",  side="right",  children=[Button("Right")]),
    Tooltip(content="Bottom", side="bottom", children=[Button("Bottom")]),
    Tooltip(content="Left",   side="left",   children=[Button("Left")]),
])
```

## With icon button

```python
Tooltip(
    content="Open settings",
    side="right",
    children=[IconButton(icon="settings", variant="ghost")],
)
```

## With custom offset

```python
Tooltip(
    content="Saved!",
    side="top",
    side_offset=8,
    children=[Button("Save", icon="save")],
)
```
"""
