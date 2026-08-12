"""Switch — /docs/components/switch.

Interactive reference page for the Switch component.
"""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Separator,
    Text,
)
from refast.components.shadcn.controls import Switch
from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import playground_card

PAGE_METADATA = {
    "title": "Switch",
    "route": "/docs/components/switch",
    "icon": "check-circle",
    "group": "Buttons & Actions",
    "order": 5,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _toggle_switch(ctx: Context):
    print(ctx.event_data)
    checked = ctx.event_data.get("value", False)
    ctx.state.set("sw_checked", checked)
    await ctx.refresh()


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("sw_disabled", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    checked = ctx.state.get("sw_checked", False)
    disabled = ctx.state.get("sw_disabled", False)

    state_label = "On" if checked else "Off"

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Disabled", class_name="text-sm font-medium"),
                    Checkbox(
                        label="disabled",
                        checked=disabled,
                        on_change=ctx.callback(_set_disabled),
                    ),
                ],
            ),
        ],
        preview=[
            Switch(
                checked=checked,
                disabled=disabled,
                on_checked_change=ctx.callback(_toggle_switch),
            ),
            Text(
                f"State: {state_label}",
                class_name="text-sm text-muted-foreground",
            ),
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Switch(\n"
                f"    checked={checked},\n"
                f"    disabled={disabled},\n"
                f"    on_checked_change=ctx.callback(handle_change),\n"
                f")\n"
                f"```"
            )
        ),
        preview_class="border rounded-lg p-6 flex items-center gap-4 min-h-[80px] bg-muted/30",
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
A sliding on/off toggle. Use when you want an immediate boolean setting that takes
effect without a form submission — e.g. feature flags, notification preferences.

```python
from refast.components.shadcn.controls import Switch

# Controlled — state lives on the server
Switch(
    checked=airplane_mode,
    on_checked_change=ctx.callback(handle_airplane_mode),
)

# Uncontrolled — initial state only
Switch(default_checked=True)

# With a label
Row(children=[
    Switch(id="notifications", on_checked_change=ctx.callback(handle_notifs)),
    Text("Enable notifications"),
])
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `checked` | `bool | None` | `None` | Controlled checked state |
| `default_checked` | `bool` | `False` | Initial state (uncontrolled) |
| `disabled` | `bool` | `False` | Prevents interaction |
| `name` | `str | None` | `None` | HTML input name for form submission |
| `on_checked_change` | `Callback | None` | `None` | Called with new `bool` value on toggle |
| `id` | `str | None` | `None` | Element ID — useful for pairing with a `<label>` |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Controlled vs Uncontrolled

```python
# Controlled — you own the state, server updates drive the UI
async def handle_change(ctx: Context, checked: bool):
    ctx.state.set("airplane_mode", checked)
    await ctx.refresh()

Switch(
    checked=ctx.state.get("airplane_mode", False),
    on_checked_change=ctx.callback(handle_change),
)

# Uncontrolled — React manages internal state, good for simple local toggles
Switch(default_checked=False)
```

## With a Visible Label

```python
Row(
    gap=2,
    class_name="items-center",
    children=[
        Switch(
            id="dark-mode",
            checked=is_dark,
            on_checked_change=ctx.callback(handle_dark_mode),
        ),
        Text("Dark mode", class_name="text-sm cursor-pointer"),
    ],
)
```

## Disabled State

```python
Switch(checked=True, disabled=True)   # locked on
Switch(checked=False, disabled=True)  # locked off
```
"""
