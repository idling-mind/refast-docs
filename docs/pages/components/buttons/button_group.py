"""ButtonGroup — /docs/components/button-group.

Interactive reference page for ButtonGroup component.
"""

from refast import Context
from docs.pages.components.common import render_doc_page
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

PAGE_METADATA = {
    "title": "Button Group",
    "route": "/docs/components/button-group",
    "icon": "rows",
    "group": "Buttons & Actions",
    "order": 2,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


def render(ctx: Context):
    """Render the ButtonGroup component reference page."""
    return render_doc_page(
        ctx,
        title=PAGE_TITLE,
        route=PAGE_ROUTE,
        intro=INTRO,
        playground=_demo_card(ctx),
        reference=REFERENCE,
    )


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

REFERENCE = r"""
## Component Reference

### `ButtonGroup`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Layout direction of the grouped buttons. |
| `children` | `ChildrenType` | `None` | Grouped buttons, text labels, and separators. |
| `class_name` | `str` | `""` | Additional Tailwind CSS classes. |
"""
