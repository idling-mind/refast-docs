"""Resizable — /docs/components/resizable."""

from refast import Context
from refast.components import (
    Column,
    Container,
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
    Select,
    Text,
)
from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import playground_card

PAGE_METADATA = {
    "title": "Resizable",
    "route": "/docs/components/resizable",
    "icon": "grip-horizontal",
    "group": "Layout",
    "order": 6,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_direction(ctx: Context, value: str):
    ctx.state.set("rs_direction", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    direction = ctx.state.get("rs_direction", "horizontal")

    if direction == "horizontal":
        panel_class = "h-32 flex items-center justify-center"
    else:
        panel_class = "h-24 flex items-center justify-center"

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("direction", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["horizontal", "vertical"]
                        ],
                        value=direction,
                        on_change=ctx.callback(_set_direction),
                    ),
                ],
            ),
        ],
        preview=[
            Container(
                class_name="border rounded-lg overflow-hidden",
                style={"height": "300px"},
                children=[
                    ResizablePanelGroup(
                        direction=direction,
                        class_name="h-full",
                        children=[
                            ResizablePanel(
                                default_size=50,
                                min_size=20,
                                class_name=panel_class,
                                children=[
                                    Column(
                                        gap=1,
                                        align="center",
                                        children=[
                                            Text(
                                                "Panel A",
                                                class_name="font-medium text-sm",
                                            ),
                                            Text(
                                                "Drag the handle",
                                                class_name="text-xs text-muted-foreground",
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            ResizableHandle(with_handle=True),
                            ResizablePanel(
                                default_size=50,
                                min_size=20,
                                class_name=panel_class,
                                children=[
                                    Column(
                                        gap=1,
                                        align="center",
                                        children=[
                                            Text(
                                                "Panel B",
                                                class_name="font-medium text-sm",
                                            ),
                                            Text(
                                                "to resize",
                                                class_name="text-xs text-muted-foreground",
                                            ),
                                        ],
                                    )
                                ],
                            ),
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
Split-pane layout built on Radix UI `ResizablePanelGroup`. Users can drag
the handle to resize panels at runtime.

```python
from refast.components import ResizablePanelGroup, ResizablePanel, ResizableHandle

ResizablePanelGroup(
    direction="horizontal",
    children=[
        ResizablePanel(default_size=30, min_size=15, children=[sidebar]),
        ResizableHandle(with_handle=True),
        ResizablePanel(default_size=70, children=[main_content]),
    ],
)
```
"""

REFERENCE = r"""
## ResizablePanelGroup

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `direction` | `"horizontal" \| "vertical"` | `"horizontal"` | Split orientation |
| `children` | `list \| Component \| None` | `None` | Alternating panels and handles |
| `on_layout` | `Callback \| None` | `None` | Fired with new panel size array on resize |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## ResizablePanel

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `default_size` | `float` | `50` | Initial size as % of group |
| `min_size` | `float \| None` | `None` | Minimum size % |
| `max_size` | `float \| None` | `None` | Maximum size % |
| `collapsible` | `bool` | `False` | Allow fully collapsing the panel |
| `collapsed_size` | `float \| None` | `None` | Size % when fully collapsed |
| `children` | `list \| Component \| None` | `None` | Panel content |

## ResizableHandle

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `with_handle` | `bool` | `False` | Show a visible grip icon on the handle |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Examples

```python
# Three-column layout
ResizablePanelGroup(
    direction="horizontal",
    class_name="min-h-screen",
    children=[
        ResizablePanel(default_size=20, min_size=10, children=[nav]),
        ResizableHandle(),
        ResizablePanel(default_size=60, children=[editor]),
        ResizableHandle(),
        ResizablePanel(default_size=20, min_size=10, children=[sidebar]),
    ],
)
```
"""
