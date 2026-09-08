"""Form Validation Example."""

from refast import Context
from refast.components import (
    Alert,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Input,
)


async def handle_submit(ctx: Context, **kwargs):
    """Validate and submit the form."""
    name = kwargs.get("name", "")
    email = kwargs.get("email", "")
    password = kwargs.get("password", "")
    confirm_password = kwargs.get("confirm_password", "")

    errors = []
    if not name:
        errors.append("Name is required")
    if not email or "@" not in email:
        errors.append("Valid email is required")
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters")
    if password != confirm_password:
        errors.append("Passwords do not match")

    if errors:
        ctx.state.set("errors", errors)
        ctx.state.set("success", False)
    else:
        ctx.state.set("errors", [])
        ctx.state.set("success", True)
        ctx.state.set("submitted_name", name)

    await ctx.replace("form-container", render_form(ctx))


def render_form(ctx: Context):
    errors = ctx.state.get("errors", [])
    success = ctx.state.get("success", False)
    submitted_name = ctx.state.get("submitted_name", "")

    return Container(
        id="form-container",
        class_name="w-full max-w-md shadow-lg",
        children=[
            Card(
                id="registration-card",
                children=[
                    CardHeader(
                        id="card-header",
                        children=[
                            CardTitle("Account Registration"),
                            CardDescription("Form validation with dynamic errors and success alerts"),
                        ],
                    ),
                    CardContent(
                        id="card-content",
                        children=[
                            Column(
                                id="form-column",
                                gap=4,
                                children=[
                                    # Error Alerts
                                    *[
                                        Alert(variant="destructive", title="Validation Error", message=err)
                                        for err in errors
                                    ],
                                    # Success Alert
                                    Alert(
                                        variant="success",
                                        title="Registration Successful",
                                        message=f"Welcome aboard, {submitted_name}! Your account was created.",
                                    )
                                    if success
                                    else None,
                                    # Form Fields
                                    Input(
                                        id="input-name",
                                        name="name",
                                        label="Full Name",
                                        placeholder="Jane Doe",
                                        on_change=ctx.save_prop("name"),
                                    ),
                                    Input(
                                        id="input-email",
                                        name="email",
                                        label="Email Address",
                                        type="email",
                                        placeholder="jane@example.com",
                                        on_change=ctx.save_prop("email"),
                                    ),
                                    Input(
                                        id="input-password",
                                        name="password",
                                        label="Password (min 6 chars)",
                                        type="password",
                                        on_change=ctx.save_prop("password"),
                                    ),
                                    Input(
                                        id="input-confirm-password",
                                        name="confirm_password",
                                        label="Confirm Password",
                                        type="password",
                                        on_change=ctx.save_prop("confirm_password"),
                                    ),
                                    # Submit Button
                                    Button(
                                        "Create Account",
                                        on_click=ctx.callback(
                                            handle_submit,
                                            props=["name", "email", "password", "confirm_password"],
                                        ),
                                        class_name="w-full mt-2",
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            )
        ],
    )


def form_validation_page(ctx: Context):
    return Container(
        class_name="min-h-screen flex items-center justify-center p-4 bg-background",
        children=[render_form(ctx)],
    )

