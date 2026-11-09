"""IconButton — /docs/components/icon-button.

Interactive reference page for the IconButton component.
"""

from refast import Context
from refast.components import (
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
from refast.components.shadcn.button import IconButton
from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import make_state_setter, playground_card

PAGE_METADATA = {
    "title": "Icon Button",
    "route": "/docs/components/icon-button",
    "icon": "circle",
    "group": "Buttons & Actions",
    "order": 3,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────

_set_icon = make_state_setter("ib_icon")
_set_variant = make_state_setter("ib_variant")
_set_size = make_state_setter("ib_size")
_set_disabled = make_state_setter("ib_disabled")



async def _noop(ctx: Context):
    pass


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    icon = ctx.state.get("ib_icon", "settings")
    variant = ctx.state.get("ib_variant", "ghost")
    size = ctx.state.get("ib_size", "md")
    disabled = ctx.state.get("ib_disabled", False)

    icon_options = [
        "settings",
        "trash",
        "edit",
        "copy",
        "download",
        "upload",
        "search",
        "plus",
        "x",
        "check",
        "star",
        "heart",
        "bell",
        "mail",
    ]

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Icon", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in icon_options
                        ],
                        value=icon,
                        on_change=ctx.callback(_set_icon),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Variant", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in [
                                "ghost",
                                "default",
                                "secondary",
                                "destructive",
                                "outline",
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
        ],
        preview=[
            IconButton(
                icon=icon,
                variant=variant,
                size=size,
                disabled=disabled,
                aria_label=icon,
                on_click=ctx.callback(_noop),
            )
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"IconButton(\n"
                f'    icon="{icon}",\n'
                f'    variant="{variant}",\n'
                f'    size="{size}",\n'
                f'    disabled={disabled},\n'
                f'    aria_label="{icon}",\n'
                f"    on_click=ctx.callback(handle_click),\n"
                f")\n"
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
A square icon-only button. Useful for toolbars, action columns, and compact UIs where
a text label would take too much space.

```python
from refast.components.shadcn.button import IconButton

IconButton(icon="trash", aria_label="Delete item", on_click=ctx.callback(handle_delete))
IconButton(icon="settings", variant="outline", size="lg")
IconButton(icon="copy", variant="ghost")
```
"""

REFERENCE = r"""
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `icon` | `str` | *(required)* | Lucide icon name (e.g. `"trash"`, `"edit"`, `"settings"`) |
| `variant` | `"ghost" \| "default" \| "secondary" \| "destructive" \| "outline"` | `"ghost"` | Visual style |
| `size` | `"xs" \| "sm" \| "md" \| "lg" \| "xl"` | `"md"` | Button dimensions (also controls icon size) |
| `disabled` | `bool` | `False` | Prevents interaction |
| `aria_label` | `str \| None` | `None` | Accessible label — defaults to icon name if omitted |
| `on_click` | `Callback \| None` | `None` | Server callback invoked on click |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## All Variants

```python
IconButton(icon="settings")                          # ghost (default)
IconButton(icon="settings", variant="default")
IconButton(icon="settings", variant="secondary")
IconButton(icon="settings", variant="destructive")
IconButton(icon="settings", variant="outline")
```

## All Sizes

```python
IconButton(icon="settings", size="xs")
IconButton(icon="settings", size="sm")
IconButton(icon="settings", size="md")
IconButton(icon="settings", size="lg")
IconButton(icon="settings", size="xl")
```

## With Accessible Label

```python
# Always provide aria_label for screen-reader accessibility
IconButton(icon="trash", aria_label="Delete item", on_click=ctx.callback(handle_delete))
```

## Common Use Cases

```python
# Toolbar actions
Row(children=[
    IconButton(icon="bold", aria_label="Bold"),
    IconButton(icon="italic", aria_label="Italic"),
    IconButton(icon="underline", aria_label="Underline"),
])

# Table row actions
Row(children=[
    IconButton(icon="edit", aria_label="Edit", on_click=ctx.callback(handle_edit)),
    IconButton(icon="trash", variant="destructive", aria_label="Delete",
               on_click=ctx.callback(handle_delete)),
])
```
"""
