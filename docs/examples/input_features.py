"""Enhanced Input Features Showcase Example."""

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
    Heading,
    Input,
    Text,
)


async def set_state(ctx: Context, key: str):
    """Set state value on input change."""
    value = ctx.event_data.get("value", "")
    ctx.state.set(key, value)


async def validate_email(ctx: Context):
    """Validate email on change."""
    value = ctx.event_data.get("value", "")
    if "@" in value and "." in value:
        await ctx.update_props("email", {"error": ""})
        ctx.state.set("email", value)
    else:
        await ctx.update_props("email", {"error": "Please enter a valid email address"})


async def validate_password(ctx: Context):
    """Validate password on change."""
    value = ctx.event_data.get("value", "")
    if len(value) >= 8:
        await ctx.update_props("password", {"error": ""})
        ctx.state.set("password", value)
    else:
        await ctx.update_props("password", {"error": "Password must be at least 8 characters"})


async def handle_submit(ctx: Context):
    """Handle form submission."""
    email = ctx.state.get("email", "")
    password = ctx.state.get("password", "")
    username = ctx.state.get("username", "")

    if email and password and username:
        await ctx.show_toast(
            "Account created successfully!",
            variant="success",
        )
    else:
        await ctx.show_toast(
            "Please fill in all required fields properly.",
            variant="error",
        )


def input_features_page(ctx: Context):
    """Input component feature showcase page."""
    return Container(
        class_name="min-h-screen flex items-center justify-center p-4 bg-background",
        children=[
            Card(
                class_name="w-full max-w-lg shadow-lg",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Input Features Showcase"),
                            CardDescription(
                                "Demonstrates debouncing, inline error validation, labels, and description hints"
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                class_name="space-y-4",
                                children=[
                                    # Input with label and required asterisk
                                    Input(
                                        name="username",
                                        label="Username",
                                        description="Choose a unique username",
                                        placeholder="johndoe",
                                        required=True,
                                        value=ctx.state.get("username", ""),
                                        on_change=ctx.callback(set_state, key="username"),
                                        debounce=300,
                                    ),
                                    # Input with validation and error state
                                    Input(
                                        id="email",
                                        name="email",
                                        type="email",
                                        label="Email Address",
                                        description="We'll never share your email address",
                                        placeholder="you@example.com",
                                        required=True,
                                        value=ctx.state.get("email", ""),
                                        on_change=ctx.callback(validate_email),
                                        debounce=300,
                                    ),
                                    # Input with password validation
                                    Input(
                                        id="password",
                                        name="password",
                                        type="password",
                                        label="Password",
                                        description="Must be at least 8 characters",
                                        placeholder="••••••••",
                                        required=True,
                                        value=ctx.state.get("password", ""),
                                        on_change=ctx.callback(validate_password),
                                        debounce=300,
                                    ),
                                    # Optional phone input
                                    Input(
                                        id="phone",
                                        name="phone",
                                        type="tel",
                                        label="Phone Number",
                                        description="Optional — for account recovery",
                                        placeholder="+1 (555) 000-0000",
                                        value=ctx.state.get("phone", ""),
                                        on_change=ctx.callback(set_state, key="phone"),
                                        debounce=300,
                                    ),
                                    # Submit button
                                    Button(
                                        "Submit Registration",
                                        variant="default",
                                        class_name="w-full mt-4",
                                        on_click=ctx.callback(handle_submit),
                                    ),
                                ],
                            )
                        ]
                    ),
                ],
            )
        ],
    )

