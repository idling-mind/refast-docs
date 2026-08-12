"""Button — /docs/components/button.

Interactive reference page for the Button component.
"""

from refast import Context
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)
from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import make_state_setter, playground_card

PAGE_METADATA = {
    "title": "Button",
    "route": "/docs/components/button",
    "icon": "square",
    "group": "Buttons & Actions",
    "order": 1,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────

_set_variant = make_state_setter("btn_variant")
_set_size = make_state_setter("btn_size")
_set_disabled = make_state_setter("btn_disabled")
_set_loading = make_state_setter("btn_loading")



async def _noop(ctx: Context):
    pass


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    variant = ctx.state.get("btn_variant", "default")
    size = ctx.state.get("btn_size", "md")
    disabled = ctx.state.get("btn_disabled", False)
    loading = ctx.state.get("btn_loading", False)

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Variant", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in [
                                "default",
                                "secondary",
                                "destructive",
                                "outline",
                                "ghost",
                                "link",
                            ]
                        ],
                        value=variant,
                        on_change=ctx.callback(_set_variant),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Size", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["xs", "sm", "md", "lg", "xl"]
                        ],
                        value=size,
                        on_change=ctx.callback(_set_size),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Disabled", class_name="text-sm font-medium"),
                    Checkbox(
                        label="disabled",
                        checked=disabled,
                        on_change=ctx.callback(_set_disabled),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Loading", class_name="text-sm font-medium"),
                    Checkbox(
                        label="loading",
                        checked=loading,
                        on_change=ctx.callback(_set_loading),
                    ),
                ],
            ),
        ],
        preview=[
            Button(
                "Click me",
                variant=variant,
                size=size,
                disabled=disabled,
                loading=loading,
                on_click=ctx.callback(_noop),
            )
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f'Button(\n'
                f'    "Click me",\n'
                f'    variant="{variant}",\n'
                f'    size="{size}",\n'
                f'    disabled={disabled},\n'
                f'    loading={loading},\n'
                f'    on_click=ctx.callback(handle_click),\n'
                f')\n'
                f"```"
            )
        ),
        preview_class="border rounded-lg p-6 flex items-center justify-center min-h-[80px] bg-muted/30",
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
A standard clickable button styled with shadcn/ui conventions.

```python
from refast.components import Button

Button("Save", on_click=ctx.callback(handle_save))
Button("Delete", variant="destructive", icon="trash", on_click=ctx.callback(handle_delete))
Button("Next", variant="ghost", icon="arrow-right", icon_position="right")
Button("Processing…", loading=True)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(positional)* | Button text |
| `variant` | `"default" | "secondary" | "destructive" | "outline" | "ghost" | "link"` | `"default"` | Visual style |
| `size` | `"sm" | "md" | "lg" | `"md"` | Button dimensions |
| `icon` | `str | None` | `None` | Lucide icon name (e.g. `"save"`, `"trash"`) |
| `icon_position` | `"left" | "right"` | `"left"` | Icon placement relative to label |
| `disabled` | `bool` | `False` | Prevents interaction |
| `loading` | `bool` | `False` | Shows spinner and disables the button |
| `type` | `"button" | "submit" | "reset"` | `"button"` | HTML button type attribute |
| `on_click` | `Callback | None` | `None` | Server callback invoked on click |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## All Variants

```python
Button("Default")
Button("Secondary", variant="secondary")
Button("Destructive", variant="destructive")
Button("Outline", variant="outline")
Button("Ghost", variant="ghost")
Button("Link", variant="link")
```

## All Sizes

```python
Button("Extra Small", size="xs")
Button("Small",       size="sm")
Button("Medium",      size="md")
Button("Large",       size="lg")
Button("Extra Large", size="xl")
```

## With Icons

```python
Button("Save", icon="save")                                    # icon on left (default)
Button("Next", icon="arrow-right", icon_position="right")     # icon on right
```

## States

```python
Button("Disabled", disabled=True)
Button("Loading…", loading=True)
```
"""
