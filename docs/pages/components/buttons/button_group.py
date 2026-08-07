"""ButtonGroup — /docs/components/button-group.

Interactive reference page for ButtonGroup component.
"""

from refast import Context
from refast.components import (
    Button,
    Card,
    CardContent,
    Column,
    Container,
    Heading,
    Markdown,
    Separator,
    Text,
)
from refast.components.shadcn.button import ButtonGroup

PAGE_TITLE = "ButtonGroup"
PAGE_ROUTE = "/docs/components/button-group"


def render(ctx: Context):
    """Render the ButtonGroup component reference page."""
    from docs.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6 space-y-8",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            _demo_card(ctx),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


def _demo_card(ctx: Context):
    """Demonstrate ButtonGroup variants."""
    return Card(
        children=[
            CardContent(
                class_name="p-6 space-y-6",
                children=[
                    Column(
                        gap=4,
                        children=[
                            Text("Horizontal Button Group", class_name="font-semibold text-sm"),
                            ButtonGroup(
                                orientation="horizontal",
                                children=[
                                    Button("Save"),
                                    Button("Cancel", variant="outline"),
                                    Button("Delete", variant="destructive"),
                                ]
                            ),
                            Text("Vertical Button Group", class_name="font-semibold text-sm mt-4"),
                            ButtonGroup(
                                orientation="vertical",
                                children=[
                                    Button("Top", variant="outline"),
                                    Button("Middle", variant="outline"),
                                    Button("Bottom", variant="outline"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )


INTRO = """
Group related action buttons together with consistent border radiuses and layout alignment.

```python
from refast.components.shadcn.button import Button, ButtonGroup

ButtonGroup(
    orientation="horizontal",
    children=[
        Button("Save"),
        Button("Delete", variant="destructive"),
    ]
)
```
"""

REFERENCE = """
## Component Reference

### `ButtonGroup`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `"horizontal" | "vertical"` | `"horizontal"` | Layout direction of the grouped buttons. |
| `children` | `ChildrenType` | `None` | Grouped buttons, text labels, and separators. |
| `class_name` | `str` | `""` | Additional Tailwind CSS classes. |
"""
