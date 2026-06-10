"""Desktop Notifications — /docs/concepts/desktop-notifications."""

import datetime
from refast import Context
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Checkbox,
    Column,
    Container,
    Heading,
    Input,
    Row,
    Separator,
    Text,
)

from docs.pages.utils import render_markdown_with_demo_apps

PAGE_TITLE = "Desktop Notifications"
PAGE_ROUTE = "/docs/concepts/desktop-notifications"

# ── Callbacks for Desktop Notification events ──────────────────────────────


async def handle_click(ctx: Context):
    """Fired when the user clicks the native system notification."""
    await ctx.show_toast("Notification Clicked! Window focused.", variant="success")
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    await ctx.prepend(
        "notif-event-logs",
        Row(
            children=[
                Badge("on_click", variant="success"),
                Text(
                    f" {time_str} — Fired click callback (focusing tab)",
                    class_name="text-xs text-muted-foreground ml-2",
                ),
            ],
            class_name="mb-1.5 items-center",
        ),
    )


async def handle_close(ctx: Context):
    """Fired when the desktop notification is dismissed/closed."""
    await ctx.show_toast("Notification dismissed.", variant="info")
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    await ctx.prepend(
        "notif-event-logs",
        Row(
            children=[
                Badge("on_close", variant="outline"),
                Text(
                    f" {time_str} — Fired close/dismiss callback",
                    class_name="text-xs text-muted-foreground ml-2",
                ),
            ],
            class_name="mb-1.5 items-center",
        ),
    )


async def handle_permission_granted(ctx: Context):
    """Fired when the notification permission is granted by user."""
    await ctx.show_toast("Notification permission granted!", variant="success")
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    await ctx.prepend(
        "notif-event-logs",
        Row(
            children=[
                Badge("on_permission_granted", variant="default"),
                Text(
                    f" {time_str} — Permission check: GRANTED",
                    class_name="text-xs text-muted-foreground ml-2",
                ),
            ],
            class_name="mb-1.5 items-center",
        ),
    )


async def handle_permission_denied(ctx: Context):
    """Fired when the notification permission is denied by user."""
    await ctx.show_toast("Notification permission denied/blocked.", variant="error")
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    await ctx.prepend(
        "notif-event-logs",
        Row(
            children=[
                Badge("on_permission_denied", variant="destructive"),
                Text(
                    f" {time_str} — Permission check: DENIED",
                    class_name="text-xs text-muted-foreground ml-2",
                ),
            ],
            class_name="mb-1.5 items-center",
        ),
    )


async def trigger_notification(
    ctx: Context,
    notif_title: str = "Refast Native Alert",
    notif_body: str = "This is a native system notification!",
    notif_tag: str = "refast-group",
    notif_silent: bool = False,
    notif_require_interaction: bool = False,
):
    """Sends the desktop notification command to the browser."""
    title_val = notif_title or "Refast Native Alert"
    body_val = notif_body or "This is a native system notification!"
    tag_val = notif_tag or None

    # Try to clean up the initial waiting placeholder
    try:
        await ctx.remove("awaiting-msg")
    except Exception:
        pass

    await ctx.show_desktop_notification(
        title=title_val,
        body=body_val,
        icon="https://refast.dev/logo.png",
        tag=tag_val,
        silent=notif_silent,
        require_interaction=notif_require_interaction,
        on_click=ctx.callback(handle_click),
        on_close=ctx.callback(handle_close),
        on_permission_granted=ctx.callback(handle_permission_granted),
        on_permission_denied=ctx.callback(handle_permission_denied),
    )

    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    await ctx.prepend(
        "notif-event-logs",
        Row(
            children=[
                Badge("trigger", variant="secondary"),
                Text(
                    f" {time_str} — Sent request: '{title_val}'",
                    class_name="text-xs text-muted-foreground ml-2",
                ),
            ],
            class_name="mb-1.5 items-center",
        ),
    )


async def clear_logs(ctx: Context):
    """Clear the logs."""
    await ctx.update_props(
        "notif-event-logs",
        {
            "children": Text(
                "Awaiting notification triggers...",
                id="awaiting-msg",
                class_name="text-xs text-muted-foreground italic",
            )
        },
    )


# ── Interactive Playground Component ──────────────────────────────────────────


def _desktop_notifications_demo(ctx: Context):
    ctx.store.local["notif_title"] = ctx.store.local.get(
        "notif_title", "Refast Native Alert"
    )
    ctx.store.local["notif_body"] = ctx.store.local.get(
        "notif_body", "Backend-triggered system notification!"
    )
    ctx.store.local["notif_tag"] = ctx.store.local.get("notif_tag", "refast-group")
    ctx.store.local["notif_silent"] = ctx.store.local.get("notif_silent", False)
    ctx.store.local["notif_require_interaction"] = ctx.store.local.get(
        "notif_require_interaction", False
    )

    playground = Card(
        class_name="border shadow-sm mb-6",
        children=[
            CardHeader(
                children=[
                    CardTitle("Interactive Playground"),
                    CardDescription(
                        "Configure and fire native notifications to test permission prompts, sounds, and callbacks."
                    ),
                ]
            ),
            CardContent(
                children=[
                    Row(
                        gap=6,
                        class_name="flex-col md:flex-row",
                        children=[
                            # Left side: Configuration
                            Column(
                                gap=4,
                                class_name="flex-1",
                                children=[
                                    Column(
                                        gap=1.5,
                                        children=[
                                            Text(
                                                "Notification Title",
                                                class_name="text-sm font-semibold",
                                            ),
                                            Input(
                                                placeholder="Enter title...",
                                                value=ctx.store.local["notif_title"],
                                                on_change=ctx.save_prop("notif_title"),
                                            ),
                                        ],
                                    ),
                                    Column(
                                        gap=1.5,
                                        children=[
                                            Text(
                                                "Body Message (Content)",
                                                class_name="text-sm font-semibold",
                                            ),
                                            Input(
                                                placeholder="Enter body...",
                                                value=ctx.store.local["notif_body"],
                                                on_change=ctx.save_prop("notif_body"),
                                            ),
                                        ],
                                    ),
                                    Column(
                                        gap=1.5,
                                        children=[
                                            Text(
                                                "Deduplication Tag",
                                                class_name="text-sm font-semibold",
                                            ),
                                            Text(
                                                "Notifications with the same tag will replace each other instead of stacking.",
                                                class_name="text-[11px] text-muted-foreground",
                                            ),
                                            Input(
                                                placeholder="e.g. status-updates",
                                                value=ctx.store.local["notif_tag"],
                                                on_change=ctx.save_prop("notif_tag"),
                                            ),
                                        ],
                                    ),
                                    Row(
                                        gap=4,
                                        children=[
                                            Row(
                                                gap=2,
                                                align="center",
                                                children=[
                                                    Checkbox(
                                                        id="notif-silent-chk",
                                                        checked=ctx.store.local[
                                                            "notif_silent"
                                                        ],
                                                        on_change=ctx.save_prop(
                                                            "notif_silent"
                                                        ),
                                                    ),
                                                    Text(
                                                        "Silent", class_name="text-sm"
                                                    ),
                                                ],
                                            ),
                                            Row(
                                                gap=2,
                                                align="center",
                                                children=[
                                                    Checkbox(
                                                        id="notif-interact-chk",
                                                        checked=ctx.store.local[
                                                            "notif_require_interaction"
                                                        ],
                                                        on_change=ctx.save_prop(
                                                            "notif_require_interaction"
                                                        ),
                                                    ),
                                                    Text(
                                                        "Require Interaction",
                                                        class_name="text-sm",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Button(
                                        "Trigger Notification",
                                        on_click=ctx.chain(
                                            [
                                                ctx.js(
                                                    """
                                            if (!('Notification' in window)) {
                                                alert('This browser does not support desktop notifications.');
                                            } else if (Notification.permission === 'denied') {
                                                console.log("[Refast] Notification permission denied")
                                            } else {
                                                Notification.requestPermission().then(function(p) {
                                                    console.log("[Refast] Notification permission granted")
                                                });
                                            };
                                            """
                                                ),
                                                ctx.callback(
                                                    trigger_notification,
                                                    props=[
                                                        "notif_title",
                                                        "notif_body",
                                                        "notif_tag",
                                                        "notif_silent",
                                                        "notif_require_interaction",
                                                    ],
                                                ),
                                            ]
                                        ),
                                        class_name="w-full mt-2 bg-primary hover:bg-primary/95 text-primary-foreground font-semibold py-2 rounded-md transition-colors",
                                    ),
                                    Button(
                                        "Hidden Trigger",
                                        id="hidden-trigger-btn",
                                        class_name="hidden",
                                    ),
                                ],
                            ),
                            # Right side: Event Logger
                            Column(
                                gap=3,
                                class_name="flex-1 border-t md:border-t-0 md:border-l pt-4 md:pt-0 md:pl-6",
                                children=[
                                    Heading(
                                        "Real-time Event Logger",
                                        level=5,
                                        class_name="text-sm font-semibold",
                                    ),
                                    Text(
                                        "Browser permission prompts, notification triggers, user clicks, and dismissals will update below in real-time.",
                                        class_name="text-xs text-muted-foreground",
                                    ),
                                    Container(
                                        id="notif-event-logs",
                                        class_name="border rounded-md p-3 h-[250px] overflow-y-auto bg-muted/40 font-mono",
                                        children=[
                                            Text(
                                                "Awaiting notification triggers...",
                                                id="awaiting-msg",
                                                class_name="text-xs text-muted-foreground italic",
                                            )
                                        ],
                                    ),
                                    Button(
                                        "Clear Logs",
                                        variant="outline",
                                        size="sm",
                                        on_click=ctx.callback(clear_logs),
                                        class_name="self-end",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
        ],
    )
    return playground


def render(ctx: Context):
    """Render the desktop notifications page."""
    from docs.app import docs_layout

    desktop_notifications_demo = _desktop_notifications_demo(ctx)

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
Desktop notifications let your application send native, system-level alerts to the user's
desktop or mobile device. Unlike toast notifications, desktop notifications:
- Display outside the browser window.
- Can persist when your web application is minimized or runs in the background.
- Can receive clicks that focus or navigate the application.
- Require explicit permission from the user before they can be displayed.

---

## Basic Usage

To display a native notification, invoke `ctx.show_desktop_notification()` in any async callback:

```python
async def handle_alert(ctx: Context):
    await ctx.show_desktop_notification(
        title="Server Alert",
        body="CPU usage exceeded 90% on server node-42.",
        icon="https://example.com/alert-icon.png",
    )
```

Refast automatically handles the underlying browser's Notification API. The browser will automatically prompt the user for permission when the first notification is triggered, if not already configured.

---

## Live Demo & Event Playground

Configure the fields below to customize a notification payload, and observe how Python handles browser callbacks for permission changes, notification clicks, and close events in real-time.

{{ desktop_notifications_demo }}

---

## API Reference

### `ctx.show_desktop_notification()`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `str` | *Required* | Bold title displayed at the top of the notification. |
| `body` | `str` | `""` | Subtext/message body of the notification. |
| `icon` | `str \| None` | `None` | URL to a logo or image file displayed within the notification. |
| `tag` | `str \| None` | `None` | Unique string identifier to group notifications. Notifications with the same tag overwrite each other in place. |
| `silent` | `bool` | `False` | When `True`, system audio/vibration cues are disabled. |
| `require_interaction` | `bool` | `False` | When `True`, the notification remains active on screen until dismissed manually. |
| `on_click` | `Callback \| None` | `None` | Fired when the user clicks the notification. Focuses the browser tab automatically. |
| `on_close` | `Callback \| None` | `None` | Fired when the notification is dismissed by the user or closed programmatically. |
| `on_permission_granted` | `Callback \| None` | `None` | Fired immediately if permission is granted when requesting. |
| `on_permission_denied` | `Callback \| None` | `None` | Fired immediately if permission is blocked or denied when requesting. |

---

## Key Concepts & Patterns

### Permission Handling

Operating systems and browsers require the user's explicit consent to show desktop notifications. 
- Refast prompts the user for permission automatically when `ctx.show_desktop_notification()` is first called.
- If permission is already granted, it shows the notification immediately.
- If the user blocks notifications, subsequent calls are silently ignored by the OS.
- You can register `on_permission_granted` and `on_permission_denied` callbacks to respond to these choices (e.g., updating UI settings, showing warning banners).

```python
await ctx.show_desktop_notification(
    title="Enable Alerts",
    on_permission_granted=ctx.callback(on_granted),
    on_permission_denied=ctx.callback(on_denied),
)
```

> [!WARNING]
> **Production Latency & User Gesture Blocks**
> 
> Modern browsers enforce strict security policies regarding **User Gestures** (transient user activation) for permission prompts like `Notification.requestPermission()`.
> 
> Because Refast is a backend-driven framework, callbacks typically execute on the server over WebSockets. In production environments, the network latency (WebSocket hop) can cause the browser to consider the user gesture "expired" by the time the notification command returns. As a result, the browser will block the permission prompt and log a warning in the developer console.
> 
> *(Note: This works on `localhost` because browsers bypass or have loose gesture expiration rules for local loops).*

#### Production-Safe Permission Workaround

To ensure that the permission prompt is always triggered within a valid user gesture in production, you should request permission on the client side using a client-side JavaScript callback (`ctx.js`) *before* invoking the backend callback.

You can accomplish this easily using `ctx.chain` to link a client-side JS check with your server-side callback:

```python
Button(
    "Trigger Alert",
    on_click=ctx.chain([
        ctx.js(
            \"""
            if (!('Notification' in window)) {
                alert('This browser does not support desktop notifications.');
            } else if (Notification.permission === 'denied') {
                console.log("[Refast] Notification permission denied");
            } else {
                // Requests permission client-side directly within the user click gesture
                Notification.requestPermission().then(function(p) {
                    console.log("[Refast] Notification permission: " + p);
                });
            }
            \"""
        ),
        ctx.callback(
            trigger_notification,
            props=["notif_title", "notif_body"]
        )
    ])
)
```

Once the user has granted permission on their first click, subsequent clicks will bypass the request phase and display the desktop alert instantly.


### De-duplication using Tags

If you send multiple alerts in a short time frame, they will stack and clutter the user's system notification center. By supplying a stable `tag`, you ensure that a new notification replaces any existing active notification with the same tag in place:

```python
# Updates the progress notification in-place instead of stacking
async def update_progress(ctx: Context, pct: int):
    await ctx.show_desktop_notification(
        title="File Upload",
        body=f"Progress: {pct}% complete",
        tag="upload-progress-alert",
        silent=True, # Prevent sound on every progress increment
    )
```

### Actions on Click

When a user clicks on a desktop notification, the browser automatically focuses the browser window/tab. In the `on_click` Python callback, you can perform additional actions like navigating to a specific route, updating state, or showing a dialog:

```python
async def handle_click(ctx: Context):
    # Focuses and redirects the user's tab to the details page
    await ctx.load("/docs/concepts/desktop-notifications")
    await ctx.show_toast("Redirected from desktop alert!", variant="info")
```

---

## Next Steps

- [Toast Notifications](/docs/concepts/toasts) — Inline overlay alerts for immediate feedback
- [Callbacks & Events](/docs/concepts/callbacks) — Under the hood of Refast's Python-to-JS events
- [JavaScript Interop](/docs/concepts/js-interop) — Advanced scripting for browser controls
"""
