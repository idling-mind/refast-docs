from typing import Any, Callable

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Row,
)


def make_state_setter(key: str) -> Callable:
    """Return an async callback that sets ctx.state[key] = value and refreshes.

    Args:
        key: The state key to set in ctx.state.
    """
    async def _setter(ctx: Context, value: Any):
        ctx.state.set(key, value)
        await ctx.refresh()

    return _setter


def make_state_toggle(key: str) -> Callable:
    """Return an async callback that toggles a boolean state value and refreshes.

    Args:
        key: The state key to toggle in ctx.state.
    """
    async def _toggle(ctx: Context):
        current = ctx.state.get(key, False)
        ctx.state.set(key, not current)
        await ctx.refresh()

    return _toggle



def playground_card(
    options: list,
    preview,
    code=None,
    title: str = "Interactive Playground",
    preview_class: str = "border rounded-lg p-6 bg-muted/30",
):
    """Return an Interactive Playground Card with a two-column layout.

    The component preview is on the left (flex-1) and the option controls
    are stacked in a column on the right (fixed width, shrinks cleanly).

    Args:
        options: List of Column widgets representing individual option controls.
        preview: The component (or Container) to preview.
        code: Optional Markdown widget with the live code snippet.
        title: Card header title (defaults to "Interactive Playground").
        preview_class: Tailwind classes for the preview wrapper Container.
    """
    content_children = [
        Row(
            gap=6,
            class_name="items-start",
            children=[
                # ── Left: preview area ─────────────────────────────────
                Container(
                    class_name=f"flex-1 min-w-0 {preview_class}",
                    children=preview if isinstance(preview, list) else [preview],
                ),
                # ── Right: stacked option controls ─────────────────────
                Column(
                    gap=4,
                    class_name="w-52 shrink-0",
                    children=options,
                ),
            ],
        ),
    ]

    if code is not None:
        content_children.append(code)

    return Card(
        children=[
            CardHeader(title=title),
            CardContent(children=content_children),
        ]
    )
