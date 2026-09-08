"""Settings Panel Example — Multi-section settings with various input types."""

from refast import Context
from refast.components import (
    Avatar,
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Input,
    Label,
    Radio,
    RadioGroup,
    Row,
    Select,
    Separator,
    Switch,
    Text,
    Textarea,
)


async def save_profile(ctx: Context):
    """Save profile settings."""
    await ctx.show_toast("Profile saved successfully!", variant="success")


async def save_notifications(ctx: Context, **kwargs):
    """Save notification settings."""
    await ctx.show_toast("Notification preferences updated!", variant="success")


async def save_appearance(ctx: Context):
    """Save appearance settings."""
    await ctx.show_toast("Appearance settings saved!", variant="success")


async def toggle_setting(ctx: Context, key: str):
    """Toggle a boolean setting."""
    current = ctx.state.get(key, False)
    ctx.state.set(key, not current)
    await ctx.refresh()


async def update_input(ctx: Context, key: str, value: str):
    """Update an input value."""
    ctx.state.set(key, value)
    await ctx.refresh()


async def change_section(ctx: Context, section: str):
    """Change active section."""
    ctx.state.set("active_section", section)
    await ctx.refresh()


def settings_panel_page(ctx: Context):
    """Settings page."""
    active_section = ctx.state.get("active_section", "profile")
    theme = ctx.state.get("theme", "system")
    language = ctx.state.get("language", "en")

    menu_items = [
        {"id": "profile", "label": "Profile", "icon": "user"},
        {"id": "notifications", "label": "Notifications", "icon": "bell"},
        {"id": "appearance", "label": "Appearance", "icon": "palette"},
        {"id": "security", "label": "Security", "icon": "shield"},
        {"id": "billing", "label": "Billing", "icon": "credit-card"},
    ]

    content = None

    if active_section == "profile":
        content = Card(
            children=[
                CardHeader(
                    children=[
                        CardTitle("Profile"),
                        CardDescription("Manage your public profile information"),
                    ]
                ),
                CardContent(
                    children=[
                        Column(
                            gap=6,
                            children=[
                                Row(
                                    gap=4,
                                    align="center",
                                    children=[
                                        Avatar(
                                            src="https://github.com/shadcn.png",
                                            alt="User avatar",
                                            size="lg",
                                        ),
                                        Column(
                                            gap=2,
                                            children=[
                                                Button(
                                                    label="Change Avatar",
                                                    variant="outline",
                                                    size="sm",
                                                ),
                                                Text(
                                                    "JPG, GIF or PNG. Max size 2MB.",
                                                    class_name="text-xs text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                Separator(),
                                Row(
                                    gap=4,
                                    children=[
                                        Column(
                                            gap=2,
                                            class_name="flex-1",
                                            children=[
                                                Label("First Name"),
                                                Input(
                                                    name="first_name",
                                                    placeholder="John",
                                                    value=ctx.state.get("first_name", ""),
                                                ),
                                            ],
                                        ),
                                        Column(
                                            gap=2,
                                            class_name="flex-1",
                                            children=[
                                                Label("Last Name"),
                                                Input(
                                                    name="last_name",
                                                    placeholder="Doe",
                                                    value=ctx.state.get("last_name", ""),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Email"),
                                        Input(
                                            name="email",
                                            type="email",
                                            placeholder="john@example.com",
                                            value=ctx.state.get("email", ""),
                                        ),
                                    ],
                                ),
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Username"),
                                        Row(
                                            gap=0,
                                            children=[
                                                Container(
                                                    class_name="bg-muted px-3 py-2 rounded-l-md border border-r-0",
                                                    children=[
                                                        Text("@", class_name="text-muted-foreground")
                                                    ],
                                                ),
                                                Input(
                                                    name="username",
                                                    placeholder="johndoe",
                                                    value=ctx.state.get("username", ""),
                                                    class_name="rounded-l-none",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Bio"),
                                        Textarea(
                                            name="bio",
                                            placeholder="Tell us a little about yourself",
                                            rows=4,
                                            value=ctx.state.get("bio", ""),
                                        ),
                                        Text(
                                            "Brief description for your profile. URLs are hyperlinked.",
                                            class_name="text-xs text-muted-foreground",
                                        ),
                                    ],
                                ),
                                Row(
                                    justify="end",
                                    children=[
                                        Button(
                                            label="Save Changes",
                                            on_click=ctx.callback(save_profile),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    elif active_section == "notifications":
        content = Card(
            children=[
                CardHeader(
                    children=[
                        CardTitle("Notifications"),
                        CardDescription("Configure how you receive notifications"),
                    ]
                ),
                CardContent(
                    children=[
                        Column(
                            gap=6,
                            children=[
                                Row(
                                    justify="between",
                                    align="start",
                                    children=[
                                        Column(
                                            gap=1,
                                            children=[
                                                Text("Email Notifications", class_name="font-medium"),
                                                Text(
                                                    "Receive emails about your account activity",
                                                    class_name="text-sm text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                        Switch(
                                            on_checked_change=ctx.save_prop("email_notifications"),
                                        ),
                                    ],
                                ),
                                Separator(),
                                Row(
                                    justify="between",
                                    align="start",
                                    children=[
                                        Column(
                                            gap=1,
                                            children=[
                                                Text("Push Notifications", class_name="font-medium"),
                                                Text(
                                                    "Receive push notifications on your devices",
                                                    class_name="text-sm text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                        Switch(
                                            on_checked_change=ctx.save_prop("push_notifications"),
                                        ),
                                    ],
                                ),
                                Separator(),
                                Row(
                                    justify="between",
                                    align="start",
                                    children=[
                                        Column(
                                            gap=1,
                                            children=[
                                                Text("Marketing Emails", class_name="font-medium"),
                                                Text(
                                                    "Receive emails about new products and features",
                                                    class_name="text-sm text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                        Switch(
                                            on_checked_change=ctx.save_prop("marketing_emails"),
                                        ),
                                    ],
                                ),
                                Separator(),
                                Row(
                                    justify="between",
                                    align="start",
                                    children=[
                                        Column(
                                            gap=1,
                                            children=[
                                                Text("Weekly Digest", class_name="font-medium"),
                                                Text(
                                                    "Get a weekly summary of your activity",
                                                    class_name="text-sm text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                        Switch(
                                            on_checked_change=ctx.save_prop("weekly_digest"),
                                        ),
                                    ],
                                ),
                                Row(
                                    justify="end",
                                    class_name="mt-4",
                                    children=[
                                        Button(
                                            label="Save Preferences",
                                            on_click=ctx.callback(
                                                save_notifications,
                                                props=[
                                                    "email_notifications",
                                                    "push_notifications",
                                                    "marketing_emails",
                                                    "weekly_digest",
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    elif active_section == "appearance":
        content = Card(
            children=[
                CardHeader(
                    children=[
                        CardTitle("Appearance"),
                        CardDescription("Customize the look and feel of the application"),
                    ]
                ),
                CardContent(
                    children=[
                        Column(
                            gap=6,
                            children=[
                                Row(
                                    children=[
                                        RadioGroup(
                                            orientation="horizontal",
                                            name="theme",
                                            value=theme,
                                            on_change=ctx.save_prop("theme"),
                                            children=[
                                                Card(
                                                    class_name="bg-muted/50 p-3",
                                                    children=[
                                                        Radio(
                                                            name="theme",
                                                            value="light",
                                                            label="Light",
                                                        ),
                                                    ],
                                                ),
                                                Card(
                                                    class_name="bg-muted/50 p-3",
                                                    children=[
                                                        Radio(
                                                            name="theme",
                                                            value="dark",
                                                            label="Dark",
                                                        ),
                                                    ],
                                                ),
                                                Card(
                                                    class_name="bg-muted/50 p-3",
                                                    children=[
                                                        Radio(
                                                            name="theme",
                                                            value="system",
                                                            label="System Default",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                                Separator(),
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Language"),
                                        Select(
                                            value=language,
                                            name="language",
                                            options=[
                                                {"value": "en", "label": "English"},
                                                {"value": "es", "label": "Español"},
                                                {"value": "fr", "label": "Français"},
                                                {"value": "de", "label": "Deutsch"},
                                                {"value": "ja", "label": "日本語"},
                                            ],
                                        ),
                                    ],
                                ),
                                Separator(),
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Font Size"),
                                        Select(
                                            value=ctx.state.get("font_size", "medium"),
                                            name="font_size",
                                            options=[
                                                {"value": "small", "label": "Small"},
                                                {"value": "medium", "label": "Medium"},
                                                {"value": "large", "label": "Large"},
                                            ],
                                        ),
                                    ],
                                ),
                                Row(
                                    justify="end",
                                    class_name="mt-4",
                                    children=[
                                        Button(
                                            label="Save Appearance",
                                            on_click=ctx.callback(save_appearance),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    else:
        # Security or billing placeholder
        content = Card(
            children=[
                CardHeader(
                    children=[
                        CardTitle(active_section.capitalize()),
                        CardDescription(f"Manage your {active_section} preferences"),
                    ]
                ),
                CardContent(
                    children=[
                        Text(
                            f"Configuration for {active_section} section.",
                            class_name="text-sm text-muted-foreground",
                        )
                    ]
                ),
            ]
        )

    return Container(
        class_name="min-h-screen bg-background",
        children=[
            Row(
                children=[
                    # Sidebar
                    Container(
                        class_name="w-64 border-r min-h-screen p-4",
                        children=[
                            Column(
                                gap=6,
                                children=[
                                    Text("Settings", class_name="text-xl font-bold px-2"),
                                    Column(
                                        gap=1,
                                        children=[
                                            Button(
                                                label=item["label"],
                                                variant="default"
                                                if active_section == item["id"]
                                                else "ghost",
                                                class_name="w-full justify-start",
                                                on_click=ctx.callback(
                                                    change_section, section=item["id"]
                                                ),
                                            )
                                            for item in menu_items
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Main content
                    Container(
                        class_name="flex-1 p-8",
                        children=[
                            Container(
                                class_name="max-w-2xl",
                                children=[content],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

