"""SPA Multi-Page Navigation Example."""

from refast import Context
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Row,
    Text,
)


async def navigate(ctx: Context, page: str):
    """Navigate to a different page."""
    ctx.state.set("current_page", page)
    await ctx.replace("spa-root-container", render_spa(ctx))


def navbar(ctx: Context, current_page: str):
    """Render the navigation bar."""
    pages = ["Home", "About", "Settings"]

    return Card(
        class_name="mb-6 shadow-sm",
        children=[
            CardContent(
                class_name="p-4",
                children=[
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            Row(
                                gap=2,
                                align="center",
                                children=[
                                    Text("Refast SPA", class_name="font-bold text-lg text-primary"),
                                    Badge("Demo", variant="secondary"),
                                ],
                            ),
                            Row(
                                gap=2,
                                children=[
                                    Button(
                                        page,
                                        variant="default" if current_page == page else "ghost",
                                        size="sm",
                                        on_click=ctx.callback(navigate, page=page),
                                    )
                                    for page in pages
                                ],
                            ),
                        ],
                    )
                ],
            )
        ],
    )


def home_view():
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Welcome Home"),
                    CardDescription("This view was rendered without a full browser reload."),
                ]
            ),
            CardContent(
                children=[
                    Text(
                        "Refast applications can build rich Single Page Application (SPA) navigation "
                        "flows simply by switching components conditioned on session state."
                    )
                ]
            ),
        ]
    )


def about_view():
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("About This Application"),
                    CardDescription("Component-driven Python architectures."),
                ]
            ),
            CardContent(
                children=[
                    Text(
                        "Notice that clicking between navbar tabs instantly swaps the view via WebSocket "
                        "DOM replacement, preserving connection state and app context."
                    )
                ]
            ),
        ]
    )


def settings_view(ctx: Context):
    notifications = ctx.state.get("notifications", True)

    async def toggle_notifications(ctx: Context):
        ctx.state.set("notifications", not ctx.state.get("notifications", True))
        await ctx.replace("spa-root-container", render_spa(ctx))

    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("User Preferences"),
                    CardDescription("Settings stored in persistent session state."),
                ]
            ),
            CardContent(
                children=[
                    Row(
                        align="center",
                        justify="between",
                        children=[
                            Column(
                                children=[
                                    Text("Email Notifications", class_name="font-medium"),
                                    Text(
                                        "Receive daily digest of activity",
                                        class_name="text-xs text-muted-foreground",
                                    ),
                                ]
                            ),
                            Button(
                                "Enabled" if notifications else "Disabled",
                                variant="default" if notifications else "outline",
                                size="sm",
                                on_click=ctx.callback(toggle_notifications),
                            ),
                        ],
                    )
                ]
            ),
        ]
    )


def render_spa(ctx: Context):
    """Render the entire SPA application."""
    current_page = ctx.state.get("current_page", "Home")

    if current_page == "Home":
        content = home_view()
    elif current_page == "About":
        content = about_view()
    elif current_page == "Settings":
        content = settings_view(ctx)
    else:
        content = home_view()

    return Container(
        id="spa-root-container",
        class_name="w-full max-w-3xl mx-auto p-4",
        children=[
            navbar(ctx, current_page),
            content,
        ],
    )


def multi_page_demo(ctx: Context):
    return Container(
        class_name="min-h-screen p-6 bg-background flex flex-col justify-center",
        children=[render_spa(ctx)],
    )

