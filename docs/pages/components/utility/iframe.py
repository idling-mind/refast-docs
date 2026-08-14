"""Iframe — /docs/components/iframe."""

from docs.pages.components.common import render_doc_page
from docs.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Column,
    Iframe,
    Markdown,
    Select,
    Text,
)

PAGE_METADATA = {
    "title": "Iframe",
    "route": "/docs/components/iframe",
    "icon": "globe",
    "group": "Utility",
    "order": 7,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]

_SRC_OPTIONS = [
    {"value": "wiki", "label": "Wikipedia (External URL)"},
    {"value": "html", "label": "Welcome Card (Inline HTML)"},
]

_HEIGHT_OPTIONS = [
    {"value": "300px", "label": "300px"},
    {"value": "400px", "label": "400px"},
    {"value": "500px", "label": "500px"},
]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_source(ctx: Context, value: str):
    ctx.state.set("iframe_source", value)
    await ctx.refresh()


async def _set_height(ctx: Context, value: str):
    ctx.state.set("iframe_height", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    source_key = ctx.state.get("iframe_source", "wiki")
    height_val = ctx.state.get("iframe_height", "400px")

    if source_key == "wiki":
        src_attr = 'src="https://www.wikipedia.org"'
        srcdoc_attr = ""
        iframe_comp = Iframe(
            src="https://www.wikipedia.org",
            title="Wikipedia Embed",
            width="100%",
            height=height_val,
            class_name="border rounded bg-white w-full",
        )
    else:
        src_attr = ""
        srcdoc_attr = (
            'srcdoc="<div style=\'padding: 20px; background: linear-gradient(to right, '
            '#4f46e5, #ec4899); color: white; border-radius: 8px; text-align: center;\'>'
            '<h2>Hello from Refast!</h2><p>Inline HTML embed using srcdoc.</p></div>"'
        )
        iframe_comp = Iframe(
            srcdoc=(
                "<div style='padding: 20px; font-family: system-ui, sans-serif; "
                "background: linear-gradient(to right, #4f46e5, #ec4899); color: white; "
                "border-radius: 8px; text-align: center;'><h2>Hello from Refast!</h2>"
                "<p>Inline HTML embed using srcdoc.</p></div>"
            ),
            title="Inline HTML Embed",
            width="100%",
            height=height_val,
            class_name="border rounded bg-white w-full",
        )

    code_lines = [
        "Iframe(",
        f"    {src_attr}," if src_attr else None,
        f"    {srcdoc_attr}," if srcdoc_attr else None,
        '    title="Iframe Embed",',
        '    width="100%",',
        f'    height="{height_val}",',
        '    class_name="border rounded",',
        ")",
    ]
    code_content = "\n".join([line for line in code_lines if line is not None])

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Source Type", class_name="text-sm font-medium"),
                    Select(
                        options=_SRC_OPTIONS,
                        value=source_key,
                        on_change=ctx.callback(_set_source),
                    ),
                ],
                class_name="mb-4",
            ),
            Column(
                gap=1,
                children=[
                    Text("Height", class_name="text-sm font-medium"),
                    Select(
                        options=_HEIGHT_OPTIONS,
                        value=height_val,
                        on_change=ctx.callback(_set_height),
                    ),
                ],
            ),
        ],
        preview=[iframe_comp],
        code=Markdown(content=f"```python\n{code_content}\n```"),
        preview_class="w-full",
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
Embeds external websites or inline HTML content securely and responsively
within your Refast layouts.

```python
from refast.components import Iframe

Iframe(src="https://example.com", title="External Site")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `src` | `str | None` | `None` | The URL of the page to embed. |
| `srcdoc` | `str | None` | `None` | Inline HTML to embed (takes precedence over `src`). |
| `title` | `str | None` | `None` | Title of the iframe (important for accessibility). |
| `name` | `str | None` | `None` | Name of the iframe. |
| `allow` | `str | None` | `None` | Feature policy permissions (e.g. `geolocation`). |
| `sandbox` | `str | None` | `None` | Sandbox restrictions (e.g. `allow-scripts`). |
| `referrer_policy` | `str | None` | `None` | Referrer policy for loading the iframe. |
| `loading` | `Literal["lazy", "eager"]` | `"lazy"` | Browser loading strategy. |
| `width` | `int | str | None` | `None` | Width of the iframe (pixels or CSS string). |
| `height` | `int | str | None` | `None` | Height of the iframe (pixels or CSS string). |

## Basic External Embed

```python
Iframe(
    src="https://example.com",
    title="Example Domain",
    width="100%",
    height=400,
)
```

## Inline HTML content (srcdoc)

You can render custom, styling-isolated HTML structures directly without making a
separate HTTP request using the `srcdoc` property:

```python
Iframe(
    srcdoc="<div style='color: blue;'>Hello World</div>",
    title="Inline Frame",
    width="100%",
    height=200,
)
```

## Security Sandboxing

When embedding untrusted external contents, it's highly recommended to apply sandbox constraints:

```python
Iframe(
    src="https://example.com",
    title="Sandboxed Content",
    sandbox="allow-scripts allow-same-origin",
)
```
"""
