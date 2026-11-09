"""Alert — /docs/components/alert."""

from refast import Context
from refast.components import (
    Alert,
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
from docs.pages.components.playground import playground_card

PAGE_METADATA = {
    "title": "Alert",
    "route": "/docs/components/alert",
    "icon": "alert-triangle",
    "group": "Feedback & Overlay",
    "order": 1,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_variant(ctx: Context, value: str):
    ctx.state.set("alrt_variant", value)
    await ctx.refresh()


async def _set_dismissible(ctx: Context, value: bool):
    ctx.state.set("alrt_dismissible", value)
    await ctx.refresh()


async def _dismiss(ctx: Context):
    ctx.state.set("alrt_dismissed", True)
    await ctx.refresh()


async def _reset_alert(ctx: Context):
    ctx.state.set("alrt_dismissed", False)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    variant = ctx.state.get("alrt_variant", "default")
    dismissible = ctx.state.get("alrt_dismissible", False)
    dismissed = ctx.state.get("alrt_dismissed", False)

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
                                "success",
                                "warning",
                                "destructive",
                                "info",
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
                    Text("Dismissible", class_name="text-sm font-medium"),
                    Checkbox(
                        label="dismissible",
                        checked=dismissible,
                        on_change=ctx.callback(_set_dismissible),
                    ),
                ],
            ),
        ],
        preview=[
            Alert(
                title="Heads up!",
                message="This is an example alert message.",
                variant=variant,
                dismissible=dismissible,
                on_dismiss=ctx.callback(_dismiss) if dismissible else None,
            )
            if not dismissed
            else Button("Reset", on_click=ctx.callback(_reset_alert))
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Alert(\n"
                f'    title="Heads up!",\n'
                f'    message="This is an example alert message.",\n'
                f'    variant="{variant}",\n'
                f"    dismissible={dismissible},\n"
                + (
                    "    on_dismiss=ctx.callback(handle_dismiss),\n"
                    if dismissible
                    else ""
                )
                + ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30",
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
An inline status message that draws the user's attention without
interrupting their workflow (unlike a dialog or toast).

```python
from refast.components import Alert

Alert(title="Success!", message="Your changes have been saved.", variant="success")
```
"""

REFERENCE = r"""
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `str \| None` | `None` | Bold heading of the alert |
| `message` | `str \| None` | `None` | Body text |
| `variant` | `"default" \| "success" \| "warning" \| "destructive" \| "info"` | `"default"` | Color and icon |
| `dismissible` | `bool` | `False` | Show a close button |
| `on_dismiss` | `Callback \| None` | `None` | Called when the close button is clicked |
| `children` | `ChildrenType` | `None` | Custom content inside the alert |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Variants

```python
Alert(title="Note", message="Informational message.", variant="default")
Alert(title="Success", message="Operation completed.", variant="success")
Alert(title="Warning", message="Proceed with caution.", variant="warning")
Alert(title="Error", message="Something went wrong.", variant="destructive")
Alert(title="Info", message="Here is some information.", variant="info")
```

## Dismissible Alert

```python
async def handle_dismiss(ctx: Context):
    ctx.state.set("show_alert", False)
    await ctx.refresh()

# In your render function:
Alert(
    title="Session expiring",
    message="Your session will expire in 5 minutes.",
    variant="warning",
    dismissible=True,
    on_dismiss=ctx.callback(handle_dismiss),
)
```

## With Custom Children

```python
Alert(
    title="Custom content",
    children=[
        Text("This alert has a custom body with rich content."),
        Button("Take action", size="sm", variant="outline", class_name="mt-2"),
    ]
)
```
"""
