"""Event Modifiers Showcase Example — stop_propagation and prevent_default."""

from datetime import datetime

from refast import Context
from refast.components import (
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Grid,
    Heading,
    Input,
    Link,
    Row,
    Text,
)


def log_event(ctx: Context, message: str) -> None:
    """Add a timestamped event log message."""
    logs = ctx.state.get("mod_logs", [])
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs.append(f"[{timestamp}] {message}")
    ctx.state["mod_logs"] = logs


def render_logs(ctx: Context) -> Column:
    """Helper to render log entries."""
    logs = ctx.state.get("mod_logs", [])
    if not logs:
        return Column(
            [
                Text(
                    "No events received yet. Click interactive elements to trigger logs.",
                    class_name="text-muted-foreground italic text-xs",
                )
            ],
            id="log-container",
            class_name="bg-muted/40 p-4 rounded-md border border-border h-64 overflow-y-auto flex items-center justify-center",
        )

    return Column(
        [
            Text(
                log,
                class_name="font-mono text-[11px] text-emerald-600 dark:text-emerald-400 py-1 border-b border-border/50 last:border-0",
            )
            for log in reversed(logs)
        ],
        id="log-container",
        class_name="bg-muted/40 p-4 rounded-md border border-border h-64 overflow-y-auto",
    )


# --- Callback Handlers ---


async def clear_logs(ctx: Context):
    """Clear all logged events."""
    ctx.state["mod_logs"] = []
    await ctx.replace("log-container", render_logs(ctx))


# Card 1 handlers (Stop Propagation)
async def handle_outer_click(ctx: Context):
    """Handle click on outer container when event bubbles up."""
    log_event(ctx, "💥 Outer Card Click handler fired (bubbled)")
    await ctx.replace("log-container", render_logs(ctx))


async def handle_inner_bubble(ctx: Context):
    """Inner button with normal bubbling."""
    log_event(ctx, "🔵 Inner Button Click fired (Normal - will bubble)")
    await ctx.replace("log-container", render_logs(ctx))


async def handle_inner_stop(ctx: Context):
    """Inner button with stop_propagation=True."""
    log_event(ctx, "🔒 Inner Button Click fired (stop_propagation=True - propagation stopped)")
    await ctx.replace("log-container", render_logs(ctx))


# Card 2 handlers (Prevent Default on Link)
async def handle_default_link(ctx: Context):
    """Link click with prevent_default=True."""
    log_event(
        ctx,
        "🔗 Link Callback fired! (prevent_default=True - browser navigation suppressed)",
    )
    await ctx.replace("log-container", render_logs(ctx))


# Card 3 handlers (Checking default_prevented)
async def handle_parent_click(ctx: Context):
    """Parent container inspecting modifier state in ctx.event_data."""
    default_prevented = ctx.event_data.get("default_prevented", False)
    propagation_stopped = ctx.event_data.get("propagation_stopped", False)

    status = f"default_prevented={default_prevented}, propagation_stopped={propagation_stopped}"
    log_event(ctx, f"📦 Parent Container click handler received: [{status}]")
    await ctx.replace("log-container", render_logs(ctx))


async def handle_child_prevent_default(ctx: Context):
    """Child button clicking and preventing default."""
    log_event(ctx, "⚠️ Child Button clicked & prevented default behavior")
    await ctx.replace("log-container", render_logs(ctx))


# Card 4 handlers (Keyboard modifiers)
async def handle_keydown_enter(ctx: Context):
    """Keyboard Enter pressed and default prevented."""
    log_event(ctx, "⌨️ Input KeyDown Callback: 'Enter' captured and default behavior prevented!")
    await ctx.replace("log-container", render_logs(ctx))


def event_modifiers_page(ctx: Context) -> Container:
    """Render the full Event Modifiers standalone showcase page."""
    return Container(
        [
            # Navigation breadcrumb / back link
            Row(
                [
                    Link(
                        text="← Back to Examples",
                        href="/docs/examples",
                        class_name="text-xs text-muted-foreground hover:text-foreground transition-colors",
                    ),
                    Link(
                        text="View Concept Docs →",
                        href="/docs/concepts/callbacks",
                        class_name="text-xs text-primary hover:underline",
                    ),
                ],
                justify="between",
                class_name="pt-4 mb-2",
            ),
            # Header
            Column(
                [
                    Heading(
                        "Event Modifiers Showcase",
                        level=1,
                        class_name="text-3xl font-extrabold tracking-tight",
                    ),
                    Text(
                        "Demonstrating native `stop_propagation` and `prevent_default` event modifiers in Refast.",
                        class_name="text-muted-foreground text-sm max-w-2xl mt-1",
                    ),
                ],
                class_name="py-4 border-b mb-8",
            ),
            Grid(
                [
                    # Left side: Interactive Examples (2 cols)
                    Column(
                        [
                            # Card 1: Propagation Controls
                            Card(
                                [
                                    CardHeader(
                                        title="1. Event Bubbling & stop_propagation",
                                        description="Demonstrates stopping click propagation to outer components.",
                                    ),
                                    CardContent(
                                        [
                                            Container(
                                                [
                                                    Text(
                                                        "Clicking inside this card triggers the Card's click handler unless propagation is stopped.",
                                                        class_name="text-xs text-muted-foreground mb-4 block",
                                                    ),
                                                    Row(
                                                        [
                                                            Button(
                                                                "Normal Click (Bubbles)",
                                                                on_click=ctx.callback(
                                                                    handle_inner_bubble
                                                                ),
                                                                variant="outline",
                                                                size="sm",
                                                            ),
                                                            Button(
                                                                "Stop Propagation",
                                                                on_click=ctx.callback(
                                                                    handle_inner_stop,
                                                                    stop_propagation=True,
                                                                ),
                                                                variant="default",
                                                                size="sm",
                                                            ),
                                                        ],
                                                        gap=3,
                                                    ),
                                                ],
                                                on_click=ctx.callback(handle_outer_click),
                                                class_name="p-4 rounded-md border border-dashed border-border hover:bg-muted/30 transition-colors cursor-pointer",
                                            )
                                        ]
                                    ),
                                ],
                                class_name="shadow-sm",
                            ),
                            # Card 2: Prevent Default Navigation
                            Card(
                                [
                                    CardHeader(
                                        title="2. prevent_default Navigation Control",
                                        description="Preventing default anchor/link action to execute a server callback instead.",
                                    ),
                                    CardContent(
                                        [
                                            Column(
                                                [
                                                    Row(
                                                        [
                                                            Text("Standard Link:", class_name="text-sm"),
                                                            Link(
                                                                text="Go to Example.com (Normal Navigation)",
                                                                href="https://example.com",
                                                                target="_blank",
                                                                class_name="text-xs text-blue-500 hover:underline",
                                                            ),
                                                        ],
                                                        justify="between",
                                                    ),
                                                    Row(
                                                        [
                                                            Text("Modified Link:", class_name="text-sm"),
                                                            Link(
                                                                text="Execute Server Callback Only",
                                                                href="https://example.com",
                                                                on_click=ctx.callback(
                                                                    handle_default_link,
                                                                    prevent_default=True,
                                                                ),
                                                                class_name="text-xs text-indigo-500 hover:underline cursor-pointer font-medium",
                                                            ),
                                                        ],
                                                        justify="between",
                                                        class_name="mt-3",
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                ],
                                class_name="shadow-sm",
                            ),
                            # Card 3: Inspecting Modifier State
                            Card(
                                [
                                    CardHeader(
                                        title="3. Inspecting Modifier State",
                                        description="Accessing default_prevented and propagation_stopped on outer container event data.",
                                    ),
                                    CardContent(
                                        [
                                            Container(
                                                [
                                                    Text(
                                                        "Clicking the child button below triggers its handler and bubbles. The parent handler inspects if the event default was prevented.",
                                                        class_name="text-xs text-muted-foreground mb-4 block",
                                                    ),
                                                    Button(
                                                        "Click & Prevent Default",
                                                        on_click=ctx.callback(
                                                            handle_child_prevent_default,
                                                            prevent_default=True,
                                                        ),
                                                        variant="secondary",
                                                        size="sm",
                                                    ),
                                                ],
                                                on_click=ctx.callback(handle_parent_click),
                                                class_name="p-4 rounded-md border border-dashed border-border hover:bg-muted/30 transition-colors cursor-pointer",
                                            )
                                        ]
                                    ),
                                ],
                                class_name="shadow-sm",
                            ),
                            # Card 4: Keyboard Event Modifiers
                            Card(
                                [
                                    CardHeader(
                                        title="4. KeyDown Modifiers",
                                        description="Capturing keyboard combinations and suppressing default actions.",
                                    ),
                                    CardContent(
                                        [
                                            Column(
                                                [
                                                    Text(
                                                        "Type in the input below and press 'Enter'. It captures the event and prevents default input submission.",
                                                        class_name="text-xs text-muted-foreground mb-3 block",
                                                    ),
                                                    Input(
                                                        placeholder="Press Enter here...",
                                                        on_keydown=ctx.js(
                                                            "if (event.key === 'Enter') { refast.invoke(args.on_enter); }",
                                                            on_enter=ctx.callback(
                                                                handle_keydown_enter
                                                            ),
                                                            prevent_default=True,
                                                        ),
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                ],
                                class_name="shadow-sm",
                            ),
                        ],
                        gap=6,
                        class_name="md:col-span-2",
                    ),
                    # Right side: Event Log console (1 col)
                    Column(
                        [
                            Card(
                                [
                                    CardHeader(
                                        title="Event Log Console",
                                        description="Real-time log of events triggered on the page.",
                                    ),
                                    CardContent(
                                        [
                                            render_logs(ctx),
                                            Row(
                                                [
                                                    Button(
                                                        "Clear Logs",
                                                        on_click=ctx.callback(clear_logs),
                                                        variant="ghost",
                                                        size="xs",
                                                    )
                                                ],
                                                justify="end",
                                                class_name="mt-3",
                                            ),
                                        ]
                                    ),
                                ],
                                class_name="shadow-md sticky top-6 h-fit border-border",
                            )
                        ],
                        class_name="md:col-span-1",
                    ),
                ],
                columns="1 md:grid-cols-3",
                gap=6,
            ),
        ],
        class_name="container mx-auto px-4 max-w-6xl pb-16 min-h-screen",
    )
