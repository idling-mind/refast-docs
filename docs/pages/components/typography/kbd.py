"""Kbd — /docs/components/kbd."""

from refast import Context
from docs.pages.components.common import render_doc_page
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Kbd,
    Markdown,
    Paragraph,
    Row,
    Separator,
    Text,
)

PAGE_METADATA = {
    "title": "Kbd",
    "route": "/docs/components/kbd",
    "icon": "terminal",
    "group": "Typography",
    "order": 8,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


def render(ctx: Context):
    return render_doc_page(
        ctx,
        title=PAGE_TITLE,
        route=PAGE_ROUTE,
        intro=INTRO,
        playground=_showcase(),
        reference=REFERENCE,
    )


def _showcase():
    shortcuts = [
        ("Open command palette", ["⌘", "K"]),
        ("Save file", ["Ctrl", "S"]),
        ("Undo", ["⌘", "Z"]),
        ("Redo", ["⌘", "Shift", "Z"]),
        ("Find", ["Ctrl", "F"]),
        ("Select all", ["⌘", "A"]),
        ("Copy", ["⌘", "C"]),
        ("Paste", ["⌘", "V"]),
    ]

    return Card(
        children=[
            CardHeader(title="Keyboard Shortcuts Showcase"),
            CardContent(
                children=[
                    Column(
                        gap=3,
                        children=[
                            Row(
                                justify="between",
                                align="center",
                                children=[
                                    Text(label, class_name="text-sm text-muted-foreground"),
                                    Row(
                                        gap=1,
                                        align="center",
                                        children=[
                                            *[Kbd(k) for k in keys[:-1]],
                                            *([Text("+", class_name="text-xs text-muted-foreground mx-0.5")] if len(keys) > 1 else []),
                                            Kbd(keys[-1]),
                                        ]
                                        if len(keys) == 1
                                        else [
                                            item
                                            for i, k in enumerate(keys)
                                            for item in (
                                                [Kbd(k)]
                                                if i == 0
                                                else [
                                                    Text(
                                                        "+",
                                                        class_name="text-xs text-muted-foreground",
                                                    ),
                                                    Kbd(k),
                                                ]
                                            )
                                        ],
                                    ),
                                ],
                            )
                            for label, keys in shortcuts
                        ],
                    ),
                ]
            ),
        ]
    )


INTRO = """
Renders a keyboard key in a styled `<kbd>` element. Use it to document
keyboard shortcuts in help text and documentation.

```python
from refast.components import Kbd, Text

# Inline in prose
Text("Press ")
Kbd("⌘")
Text(" + ")
Kbd("K")
Text(" to open the command palette.")

# Single key
Kbd("Enter")
Kbd("Escape")
Kbd("Tab")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `key` | `str` | *(required)* | The key label to display |
| `id` | `str | None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Notes

`Kbd` is a pure display component — it renders the key label inside a styled
`<kbd>` HTML element. Combine multiple `Kbd` components with separator `Text`
(e.g. `"+"` or `"then"`) to represent key combinations.

## Common Key Symbols

| Symbol | Meaning |
|--------|---------|
| `⌘` | Command (macOS) |
| `⌃` | Control |
| `⌥` | Option / Alt |
| `⇧` | Shift |
| `⏎` | Return / Enter |
| `⌫` | Backspace |
| `⇥` | Tab |
| `⎋` | Escape |
"""
