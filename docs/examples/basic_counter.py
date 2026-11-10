"""Basic Counter Example."""

from refast import Context
from refast.components import (
    Badge,
    Button,
    Card,
    Column,
    Heading,
    Input,
    Link,
    Row,
    Separator,
    Text,
)

MIN_COUNT = 0
MAX_COUNT = 99
DEFAULT_STEP = 1


def parse_step(raw: str | int | None, fallback: int = DEFAULT_STEP) -> int:
    """Turn the step field into a usable increment."""
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        return fallback
    return max(1, min(MAX_COUNT, value))


def count(ctx: Context) -> int:
    """Counter value held in server state."""
    return int(ctx.state.get("count", 0))


async def change_count(ctx: Context, delta: int, step: str = "") -> None:
    """Move the counter by delta steps, clamped to the supported range."""
    previous = int(ctx.state.get("step", DEFAULT_STEP))
    move = delta * parse_step(step, fallback=previous)
    ctx.state["step"] = parse_step(step, fallback=previous)
    ctx.state["count"] = max(MIN_COUNT, min(MAX_COUNT, count(ctx) + move))
    await ctx.refresh(target_id="counter-card")


async def increment(ctx: Context, step: str = "") -> None:
    await change_count(ctx, delta=1, step=step)


async def decrement(ctx: Context, step: str = "") -> None:
    await change_count(ctx, delta=-1, step=step)


async def reset(ctx: Context) -> None:
    """Clear the counter and forget the custom step."""
    ctx.state["count"] = 0
    ctx.state["step"] = DEFAULT_STEP
    await ctx.refresh(target_id="counter-card")


def render_counter(ctx: Context):
    """Card showing the counter; refreshed as a subtree whenever the value moves.

    The step field is captured with ``ctx.save_prop`` so typing never round-trips
    to the server, and forwarded with ``props=["step"]`` when a button is clicked.
    """
    value = count(ctx)
    step = int(ctx.state.get("step", DEFAULT_STEP))
    return Card(
        id="counter-card",
        title="Counter",
        description="State lives on the server, so the value survives reloads of the page function.",
        children=[
            Column(
                gap=4,
                align="center",
                children=[
                    Heading(str(value), level=2, id="counter-value"),
                    Badge(f"moving by {step}", variant="secondary"),
                    Row(
                        [
                            Button(
                                "Decrement",
                                variant="secondary",
                                icon="arrow-down",
                                disabled=value <= MIN_COUNT,
                                on_click=ctx.callback(decrement, props=["step"]),
                            ),
                            Button(
                                "Reset",
                                variant="ghost",
                                on_click=ctx.callback(reset),
                            ),
                            Button(
                                "Increment",
                                icon="arrow-up",
                                disabled=value >= MAX_COUNT,
                                on_click=ctx.callback(increment, props=["step"]),
                            ),
                        ],
                        gap=2,
                    ),
                    Separator(),
                    Input(
                        id="step-input",
                        label="Step size",
                        type="number",
                        value=str(step),
                        on_change=ctx.save_prop("step"),
                    ),
                    Text(
                        f"Range: {MIN_COUNT} to {MAX_COUNT}",
                        class_name="text-xs text-muted-foreground",
                    ),
                ],
            )
        ],
    )


def counter_page(ctx: Context):
    return Column(
        gap=6,
        align="center",
        class_name="min-h-screen flex items-center justify-center p-6 bg-background",
        children=[
            Text("Basic Counter", class_name="text-2xl font-semibold"),
            render_counter(ctx),
            Link("Back to the examples gallery", href="/docs/examples", variant="ghost"),
        ],
    )
