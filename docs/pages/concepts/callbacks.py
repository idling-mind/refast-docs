"""Callbacks & Events — /docs/concepts/callbacks."""

import asyncio

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
    Link,
    Row,
    Separator,
    Text,
)
from refast.context import Context

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "Callbacks & Events"
PAGE_ROUTE = "/docs/concepts/callbacks"

CONTENT = r"""
## Overview

Callbacks bridge browser events and Python over WebSocket. Each event sends the callback
ID, bound kwargs, optional prop values, and raw event data to the server before invoking
your function.

Different components support different event types (e.g. `on_click`, `on_change`, `on_keydown`),
but the callback pattern is consistent: create a callback with `ctx.callback()`, then pass
it to your component's event prop. Inside the callback, use `ctx` methods to update the UI,
show toasts, and more.

In addition to python callbacks (`ctx.callback`), you can run client-only JavaScript with
`ctx.js()` for instant interactivity without a server roundtrip, or combine both in one
event by calling chaining `ctx.js()` and `ctx.callback()` together using `ctx.chain()`,
or by invoking Python from JavaScript with `refast.invoke()`. You can also just store event
data in the browser without a server hop using `ctx.save_prop()`. We'll cover all these patterns
in this section.

## Basic usage

```python
async def handle_click(ctx: Context, item_id: str):
    await ctx.show_toast(f"Clicked {item_id}!", variant="success")

Button("Click Me", on_click=ctx.callback(handle_click, item_id="Item 1"))
```

{{ basic_demo }}

## Callback with bound args

Attach static kwargs when you create the callback. Great for passing IDs, variants, or
mode flags without relying on client props.

```python
async def send_order(ctx: Context, flavor: str):
    await ctx.show_toast(f"Queued {flavor}")

Button("Vanilla", on_click=ctx.callback(send_order, flavor="vanilla")),
Button("Mocha", on_click=ctx.callback(send_order, flavor="mocha"), variant="secondary"),
Button("Chai", on_click=ctx.callback(send_order, flavor="chai"), variant="outline"),
```

## save_prop + props

`ctx.save_prop(name)` captures event data in the browser without a server hop. Use
`props=[...]` when creating a callback to forward those client-side values to Python.

```python
Input(placeholder="Your name", on_change=ctx.save_prop("demo_prop_name"))
Button("Submit with props", on_click=ctx.callback(submit, props=["demo_prop_name"]))

async def submit(ctx: Context, demo_prop_name: str = ""):
    await ctx.show_toast(f"Hello, {demo_prop_name}!")
```

{{ prop_store_demo }}

## Client-only `ctx.js` (Press Enter)

Run JavaScript directly in the browser for responsive UX without a server roundtrip.

```python
Input(
    placeholder="Type and press Enter",
    on_keydown=ctx.js(
        '''
        if (event.key === 'Enter') {
            const label = document.getElementById('js-enter-status');
            if (label) label.textContent = `Enter pressed: ${event.value || ''}`;
        }
        '''
    ),
)
```

{{ js_enter_demo }}

## `ctx.js` calling Python (refast.invoke)

Use JavaScript to filter events client-side, then call a Python callback only when needed.

```python
async def on_enter(ctx: Context, value: str = ""):
    await ctx.update_text("js-invoke-status", f"Python received: {value}")

Input(
    on_keydown=ctx.js(
        '''
        if (event.key === 'Enter') {
            refast.invoke(args.on_submit, { value: event.value });
        }
        ''',
        on_submit=ctx.callback(on_enter),
    ),
)
```

{{ js_invoke_demo }}

## Chaining actions (serial vs parallel)

Fire multiple actions from one event. Default mode is serial; set `mode="parallel"` to
run them simultaneously.

```python
# Serial (default)
Button(
    "Serial chain",
    on_click=ctx.chain([
        ctx.callback(clear_chain_log),
        ctx.callback(chain_record, message="Serial step 1", delay=0.15),
        ctx.callback(chain_record, message="Serial step 2", delay=0.15),
    ]),
)


# Parallel
Button(
    "Parallel chain",
    on_click=ctx.chain([
        ctx.callback(clear_chain_log),
        ctx.chain([
            ctx.callback(chain_record, message="Parallel A (fast)", delay=0.05),
            ctx.callback(chain_record, message="Parallel B (slower)", delay=0.25),
        ], mode="parallel"),
    ], mode="serial"),
)
```


{{ chain_demo }}


## Event Modifiers — `stop_propagation` & `prevent_default`

By default, DOM interactions follow standard browser rules: click events bubble up through ancestor components, anchor tags navigate to their `href`, and pressing `Enter` in text inputs can trigger form submissions.

Refast provides native boolean modifiers on callback and action definitions so you can control event bubbling and default browser behaviors without complex JavaScript boilerplate:

- **`stop_propagation=True`**: Prevents the event from bubbling up through the DOM tree (invokes `event.stopPropagation()` on the client). Parent components will not receive or fire handlers for this event.
- **`prevent_default=True`**: Suppresses the browser's default action for the event (invokes `event.preventDefault()` on the client). For example, prevents `<a>` links from navigating, forms from submitting on `Enter`, or page scrolling. Your Refast callback or JS action still executes normally.

### Supported Action Types

Modifiers can be set on **all five** Refast action creation methods:

| Method | Usage Example |
|--------|---------------|
| `ctx.callback()` | `ctx.callback(my_func, stop_propagation=True, prevent_default=True)` |
| `ctx.js()` | `ctx.js("alert('hi')", stop_propagation=True, prevent_default=True)` |
| `ctx.bound_js()` | `ctx.bound_js("my-id", "method", stop_propagation=True)` |
| `ctx.save_prop()` | `ctx.save_prop("field", stop_propagation=True)` |
| `ctx.chain()` | `ctx.chain([...], stop_propagation=True, prevent_default=True)` |

> [!NOTE]
> **Action Chains (`ctx.chain`)**: Modifiers can be set on the outer `ctx.chain()` or on any nested action inside the chain. Refast recursively inspects the entire action hierarchy — if any action in the chain specifies `stopPropagation` or `preventDefault`, that modifier is applied before execution.

---

### Core Patterns

#### 1. Controlling Event Bubbling (`stop_propagation`)
When an inner component is nested inside an outer clickable container (e.g. a button inside a clickable card), clicks on the inner component bubble up to trigger the parent's handler unless propagation is halted:

```python
# The outer Container handler triggers for any clicks inside it
Container(
    on_click=ctx.callback(handle_outer_click),
    class_name="p-4 border rounded",
    children=[
        # Bubbles: fires handle_inner_bubble THEN handle_outer_click
        Button("Normal Click (Bubbles)", on_click=ctx.callback(handle_inner_bubble)),
        
        # Stops propagation: fires ONLY handle_inner_stop
        Button(
            "Stop Propagation",
            on_click=ctx.callback(handle_inner_stop, stop_propagation=True),
        ),
    ],
)
```

#### 2. Suppressing Default Browser Actions (`prevent_default`)
Intercept link clicks or form submissions to run server-side Python logic or client JS without leaving the page or triggering a reload:

```python
# Normal navigation occurs: browser opens https://example.com
Link("Visit Example", href="https://example.com")

# Suppresses navigation: browser stays on page, Python callback runs
Link(
    "Execute Server Callback Only",
    href="https://example.com",
    on_click=ctx.callback(handle_link_action, prevent_default=True),
)
```

#### 3. Inspecting Modifier State in Parent Handlers
When an event bubbles up to a parent container, the parent handler can inspect whether child elements prevented default behavior or stopped propagation:

- **Python (`ctx.event_data`)**:
  ```python
  async def handle_parent_click(ctx: Context):
      # True if a child event handler set prevent_default=True
      default_prevented = ctx.event_data.get("default_prevented", False)
      # True if a child event handler set stop_propagation=True
      propagation_stopped = ctx.event_data.get("propagation_stopped", False)
      
      print(f"Parent received event: default_prevented={default_prevented}")
  ```

- **JavaScript (`ctx.js`)**:
  ```javascript
  if (event.defaultPrevented) {
      console.log("Child prevented default action");
  }
  if (event.propagationStopped) {
      console.log("Child stopped propagation");
  }
  ```

#### 4. Keyboard KeyDown Interception (`ctx.js`)
Suppress default form submission or newline behaviors on key presses (such as `Enter`):

```python
Input(
    placeholder="Press Enter here...",
    on_keydown=ctx.js(
        "if (event.key === 'Enter') { refast.invoke(args.on_enter); }",
        on_enter=ctx.callback(handle_keydown_enter),
        prevent_default=True,
    ),
)
```

{{ event_modifiers_demo }}


## Typed Events & Payload Validation

Refast supports Pydantic models for structured event validation. You can type-annotate callbacks with Pydantic models, or listen for custom events via `@ui.on()`. If validation fails, Refast catches the validation error and can invoke custom error handlers or notify the user.

### 1. Typed Callbacks with Pydantic Models

Annotate your callback's parameter with a Pydantic model. Refast will parse and validate the incoming client payload automatically before executing the handler function.

```python
from pydantic import BaseModel, Field
from refast import Context

class SearchQueryPayload(BaseModel):
    query: str = Field(..., min_length=2, description="Search query text")
    limit: int = Field(10, ge=1, le=50, description="Max results")

async def run_search(ctx: Context, payload: SearchQueryPayload):
    # payload is guaranteed to be a valid SearchQueryPayload instance
    query = payload.query
    limit = payload.limit
    await ctx.show_toast(f"Searching for '{query}' (limit: {limit})", variant="success")
```

### 2. Custom Event Listeners (`@ui.on`) and Custom Error Handlers

Register event listeners with `@ui.on()` for custom socket events and attach custom error handling functions using `on_error`:

```python
from refast.events.types import Event

async def event_error_handler(ctx: Context, error: Exception, event: Event):
    await ctx.show_toast(
        message="Validation Failed",
        description="Check your inputs. Query must be at least 2 characters.",
        variant="warning",
    )

@ui.on("search:query_event", on_error=event_error_handler)
async def handle_search_event(ctx: Context, event: Event[SearchQueryPayload]):
    query = event.data.query
    limit = event.data.limit
    await ctx.show_toast(f"Typed Event Validated: {query} (Limit: {limit})")
```


## Next steps

- [State Management](/docs/concepts/state) — Persist data across callbacks
- [DOM Updates](/docs/concepts/updates) — Targeted replacements, appends, and prop updates
- [JavaScript Interop](/docs/concepts/js-interop) — Run browser code and call component methods
"""



def render(ctx):
    """Render the callbacks concept page with inline live demos."""
    from docs.app import docs_layout

    basic_demo = Container(
        id="callbacks-basic-demo",
        class_name="space-y-3",
        children=[
            Heading("Live demo: basic callback", level=3, class_name="text-lg font-semibold"),
            Text(
                "Clicking the button sends a callback with a bound argument to Python.",
                class_name="text-sm text-muted-foreground block",
            ),
            Button("Click Me", on_click=ctx.callback(handle_click, item_id="Item 1")),
        ],
    )

    bound_args_demo = Container(
        id="callbacks-bound-args",
        class_name="space-y-3",
        children=[
            Heading(
                "Live demo: ctx.callback bound args", level=3, class_name="text-lg font-semibold"
            ),
            Text(
                "Each button sends its flavor as a bound argument without reading client props.",
                class_name="text-sm text-muted-foreground block",
            ),
            Container(
                class_name="flex flex-wrap gap-2",
                children=[
                    Button("Vanilla", on_click=ctx.callback(demo_bound_arg, flavor="vanilla")),
                    Button(
                        "Mocha",
                        on_click=ctx.callback(demo_bound_arg, flavor="mocha"),
                        variant="secondary",
                    ),
                    Button(
                        "Chai",
                        on_click=ctx.callback(demo_bound_arg, flavor="chai"),
                        variant="outline",
                    ),
                ],
            ),
        ],
    )

    prop_store_demo = Container(
        id="callbacks-props-demo",
        class_name="space-y-4",
        children=[
            Heading("Live demo: save_prop + props", level=3, class_name="text-lg font-semibold"),
            Text(
                "Typing stores the value client-side via save_prop; the button forwards it to Python with props=[...].",
                class_name="text-sm text-muted-foreground",
            ),
            Input(
                id="callbacks-name-input",
                placeholder="Your name",
                on_change=ctx.save_prop("demo_prop_name"),
            ),
            Container(
                class_name="flex flex-wrap gap-2",
                children=[
                    Button(
                        "Submit with props",
                        on_click=ctx.callback(demo_prop_submit, props=["demo_prop_name"]),
                        variant="default",
                    ),
                    Button(
                        "Clear message",
                        on_click=ctx.callback(clear_prop_message),
                        variant="secondary",
                    ),
                ],
            ),
            Text(
                "Waiting for submission...",
                id="callbacks-props-status",
                class_name="text-sm text-muted-foreground",
            ),
        ],
    )

    js_enter_demo = Container(
        id="callbacks-js-enter",
        class_name="space-y-3",
        children=[
            Heading("Live demo: ctx.js (press Enter)", level=3, class_name="text-lg font-semibold"),
            Text(
                "Client-only JavaScript handles the Enter key and updates the status without a server call.",
                class_name="text-sm text-muted-foreground",
            ),
            Input(
                id="js-enter-input",
                placeholder="Type here and press Enter",
                on_keydown=ctx.js(
                    """
                    const label = document.getElementById('js-enter-status');
                    if (!label) return;
                    if (event.key === 'Enter') {
                        label.textContent = `Enter pressed: ${event.value || ''}`;
                        label.classList.remove('text-muted-foreground');
                        label.classList.add('text-emerald-600');
                    } else {
                        label.textContent = 'Waiting for Enter...';
                        label.classList.add('text-muted-foreground');
                        label.classList.remove('text-emerald-600');
                    }
                    """
                ),
            ),
            Text(
                "Waiting for Enter...",
                id="js-enter-status",
                class_name="text-sm text-muted-foreground",
            ),
        ],
    )

    js_invoke_demo = Container(
        id="callbacks-js-invoke",
        class_name="space-y-3",
        children=[
            Heading(
                "Live demo: ctx.js + refast.invoke", level=3, class_name="text-lg font-semibold"
            ),
            Text(
                "JavaScript filters events and only calls Python on Enter using refast.invoke().",
                class_name="text-sm text-muted-foreground",
            ),
            Input(
                id="js-invoke-input",
                placeholder="Type and press Enter to call Python",
                on_keydown=ctx.js(
                    """
                    if (event.key === 'Enter') {
                        refast.invoke(args.on_submit, { value: event.value });
                    }
                    """,
                    on_submit=ctx.callback(demo_invoke_python),
                ),
            ),
            Text(
                "Python has not run yet — press Enter to send a message.",
                id="js-invoke-status",
                class_name="text-sm text-muted-foreground",
            ),
        ],
    )

    chain_demo = Container(
        id="callbacks-chain",
        class_name="space-y-4",
        children=[
            Heading("Live demo: ctx.chain", level=3, class_name="text-lg font-semibold"),
            Text(
                "Serial runs actions one-by-one; parallel fires them together.",
                class_name="text-sm text-muted-foreground",
            ),
            Container(
                class_name="flex flex-wrap gap-2",
                children=[
                    Button(
                        "Serial chain",
                        on_click=ctx.chain(
                            [
                                ctx.callback(clear_chain_log),
                                ctx.callback(chain_record, message="Serial step 1", delay=0.15),
                                ctx.callback(chain_record, message="Serial step 2", delay=0.15),
                            ]
                        ),
                    ),
                    Button(
                        "Parallel chain",
                        on_click=ctx.chain(
                            [
                                ctx.callback(clear_chain_log),
                                ctx.chain(
                                    [
                                        ctx.callback(
                                            chain_record, message="Parallel A (fast)", delay=0.05
                                        ),
                                        ctx.callback(
                                            chain_record, message="Parallel B (slower)", delay=0.25
                                        ),
                                    ],
                                    mode="parallel",
                                ),
                            ]
                        ),
                        variant="secondary",
                    ),
                ],
            ),
            Container(
                id="chain-log",
                class_name="min-h-12 space-y-1 rounded-md border bg-white/60 p-3",
                children=[
                    Text(
                        "Run a chain to see events here.",
                        class_name="text-sm text-muted-foreground",
                    ),
                ],
            ),
        ],
    )

    event_modifiers_demo = Container(
        id="callbacks-event-modifiers",
        class_name="space-y-4",
        children=[
            Heading(
                "Live demo: stop_propagation and prevent_default",
                level=3,
                class_name="text-lg font-semibold",
            ),
            Text(
                "Click the dashed card area, the buttons inside it, or the link to test propagation and default action suppression.",
                class_name="text-sm text-muted-foreground",
            ),
            Container(
                id="mod-outer-card",
                on_click=ctx.callback(handle_mod_outer_click),
                class_name="p-4 rounded-md border-2 border-dashed border-border hover:bg-muted/30 transition-colors cursor-pointer space-y-3",
                children=[
                    Row(
                        [
                            Text(
                                "Outer Container (Click anywhere inside this dashed area)",
                                class_name="text-xs font-semibold text-muted-foreground",
                            ),
                        ],
                        justify="between",
                    ),
                    Row(
                        [
                            Button(
                                "Normal Click (Bubbles)",
                                on_click=ctx.callback(handle_mod_inner_bubble),
                                variant="outline",
                                size="sm",
                            ),
                            Button(
                                "Stop Propagation",
                                on_click=ctx.callback(
                                    handle_mod_inner_stop, stop_propagation=True
                                ),
                                variant="default",
                                size="sm",
                            ),
                            Link(
                                text="Prevent Default Link",
                                href="https://example.com",
                                on_click=ctx.callback(
                                    handle_mod_link, prevent_default=True
                                ),
                                class_name="text-xs text-primary underline font-medium hover:opacity-80 transition-opacity self-center cursor-pointer",
                            ),
                        ],
                        gap=3,
                        class_name="flex-wrap items-center",
                    ),
                ],
            ),
            Container(
                id="mod-log-console",
                class_name="min-h-16 space-y-1 rounded-md border border-border bg-muted/20 p-3",
                children=[
                    Text(
                        "Event log: click any interactive element above to see events fire.",
                        id="mod-log-status",
                        class_name="text-xs font-mono text-muted-foreground",
                    )
                ],
            ),
            Row(
                [
                    Button(
                        "Clear Event Log",
                        on_click=ctx.callback(clear_mod_logs),
                        variant="ghost",
                        size="xs",
                    ),
                ],
                justify="end",
            ),
        ],
    )

    content = Container(
        class_name="max-w-4xl mx-auto p-6 space-y-8",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


async def handle_click(ctx: Context, item_id: str) -> None:
    """Example callback handler for basic demo."""
    await ctx.show_toast(f"Clicked {item_id}!", variant="success")


async def demo_bound_arg(ctx: Context, flavor: str) -> None:
    """Show a toast using a bound argument passed at callback creation time."""
    await ctx.show_toast(f"Queued {flavor}", variant="success")


async def demo_prop_submit(ctx: Context, demo_prop_name: str = "") -> None:
    """Read a saved prop from the client and surface it in the UI."""
    who = (demo_prop_name or "friend").strip() or "friend"
    await ctx.update_text("callbacks-props-status", f"Server received: {who}")
    await ctx.show_toast(f"Hello, {who}!", variant="info")


async def clear_prop_message(ctx: Context) -> None:
    """Reset the prop demo status label."""
    await ctx.update_text("callbacks-props-status", "Waiting for submission...")
    await ctx.update_props("callbacks-name-input", {"value": ""})  # Clear the input field as well


async def demo_invoke_python(ctx: Context, value: str = "") -> None:
    """Handle JS-triggered submit via refast.invoke()."""
    cleaned = value.strip()
    label = cleaned or "(empty)"
    await ctx.update_text("js-invoke-status", f"Python received: {label}")
    await ctx.show_toast(f"Processed: {label}", variant="success")


async def clear_chain_log(ctx: Context) -> None:
    """Reset the chain log container."""
    await ctx.replace(
        "chain-log",
        Container(
            id="chain-log",
            class_name="min-h-12 space-y-1 rounded-md border bg-white/60 p-3",
            children=[],
        ),
    )


async def chain_record(ctx: Context, message: str, delay: float = 0.0) -> None:
    """Append a log entry to illustrate chain ordering."""
    if delay:
        await asyncio.sleep(delay)
    await ctx.append("chain-log", Text(message, class_name="text-sm font-mono"))
    await ctx.show_toast(message, variant="secondary")


async def handle_mod_outer_click(ctx: Context) -> None:
    """Outer container click handler which inspects event modifiers."""
    default_prevented = ctx.event_data.get("default_prevented", False)
    propagation_stopped = ctx.event_data.get("propagation_stopped", False)
    msg = (
        f"💥 Outer Container received click "
        f"[default_prevented={default_prevented}, propagation_stopped={propagation_stopped}]"
    )
    await ctx.append(
        "mod-log-console",
        Text(msg, class_name="text-xs font-mono text-amber-500 dark:text-amber-400 block"),
    )
    await ctx.show_toast("Outer Container click fired (bubbled up)", variant="warning")


async def handle_mod_inner_bubble(ctx: Context) -> None:
    """Inner button with normal bubbling."""
    msg = "🔵 Inner Button clicked (Normal — bubbling to outer container)"
    await ctx.append(
        "mod-log-console",
        Text(msg, class_name="text-xs font-mono text-blue-500 dark:text-blue-400 block"),
    )
    await ctx.show_toast("Inner Button clicked (Bubbles)", variant="info")


async def handle_mod_inner_stop(ctx: Context) -> None:
    """Inner button with stop_propagation=True."""
    msg = "🔒 Inner Button clicked (stop_propagation=True — propagation stopped!)"
    await ctx.append(
        "mod-log-console",
        Text(msg, class_name="text-xs font-mono text-emerald-500 dark:text-emerald-400 block"),
    )
    await ctx.show_toast("Inner Button clicked (Propagation stopped)", variant="success")


async def handle_mod_link(ctx: Context) -> None:
    """Link with prevent_default=True."""
    msg = "🔗 Link clicked (prevent_default=True — browser navigation suppressed, server callback executed!)"
    await ctx.append(
        "mod-log-console",
        Text(msg, class_name="text-xs font-mono text-purple-500 dark:text-purple-400 block"),
    )
    await ctx.show_toast("Link clicked (Navigation suppressed)", variant="success")


async def clear_mod_logs(ctx: Context) -> None:
    """Reset the event modifier log console."""
    await ctx.replace(
        "mod-log-console",
        Container(
            id="mod-log-console",
            class_name="min-h-16 space-y-1 rounded-md border border-border bg-muted/20 p-3",
            children=[
                Text(
                    "Event log reset. Click an interactive element above to see events fire.",
                    id="mod-log-status",
                    class_name="text-xs font-mono text-muted-foreground",
                )
            ],
        ),
    )

