"""Icon — /docs/components/icon."""

import inspect
import re
from pathlib import Path
from typing import get_args

from refast import Context
from refast.components import (
    Card,
    Column,
    Container,
    Grid,
    Heading,
    Icon,
    Input,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)
from refast.components.shadcn.icon import ICON_NAMES
from docs.pages.components.playground import playground_card

PAGE_TITLE = "Icon"
PAGE_ROUTE = "/docs/components/icon"


def get_categorized_icons() -> dict[str, list[str]]:
    """Parse refast icon file to extract categorized icons."""
    try:
        import refast.components.shadcn.icon as icon_module
        source_path = Path(inspect.getfile(icon_module))
        content = source_path.read_text(encoding="utf-8")

        # Match the Literal declaration block
        match = re.search(r"ICON_NAMES\s*=\s*Literal\s*\[(.*?)\]", content, re.DOTALL)
        if not match:
            return {"All Icons": list(get_args(ICON_NAMES))}

        block = match.group(1)
        categories = {}
        current_category = "General"

        for line in block.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                current_category = line.lstrip("#").strip()
                continue

            # Match strings
            str_match = re.match(r'^["\']([^"\']+)["\']', line)
            if str_match:
                icon_name = str_match.group(1)
                categories.setdefault(current_category, []).append(icon_name)

        if not categories:
            return {"All Icons": list(get_args(ICON_NAMES))}

        return categories
    except Exception:
        try:
            return {"All Icons": list(get_args(ICON_NAMES))}
        except Exception:
            return {}


# ── Callbacks ─────────────────────────────────────────────────────────────


async def _set_preview_name(ctx: Context, value: str):
    ctx.state["icon_preview_name"] = value
    await ctx.refresh()


async def _set_preview_size(ctx: Context, value: str):
    try:
        ctx.state["icon_preview_size"] = int(value)
    except ValueError:
        pass
    await ctx.refresh()


async def _set_preview_color(ctx: Context, value: str):
    ctx.state["icon_preview_color"] = value
    await ctx.refresh()


async def _set_preview_stroke_width(ctx: Context, value: str):
    try:
        ctx.state["icon_preview_stroke_width"] = float(value)
    except ValueError:
        pass
    await ctx.refresh()


async def _on_search(ctx: Context, value: str):
    ctx.state["icon_search_query"] = value
    await ctx.refresh()


async def _on_copy(ctx: Context, name: str):
    # Copy to clipboard using browser API via call_js
    await ctx.call_js("navigator.clipboard.writeText(args.text)", text=f'Icon("{name}")')
    # Show toast
    await ctx.show_toast(f'Copied: Icon("{name}")', variant="success")


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    # Preview state
    icon_name = ctx.state.get("icon_preview_name", "home")
    size = ctx.state.get("icon_preview_size", 48)
    color = ctx.state.get("icon_preview_color", "currentColor")
    stroke_width = ctx.state.get("icon_preview_stroke_width", 2.0)

    # Available sample icons for preview selection
    sample_icons = [
        "home",
        "settings",
        "user",
        "star",
        "check",
        "x",
        "play",
        "refresh-cw",
        "search",
        "bell",
        "rocket",
        "zap",
    ]

    options = [
        Column(
            gap=1,
            children=[
                Text("Icon Name", class_name="text-sm font-medium"),
                Select(
                    options=[{"value": name, "label": name} for name in sample_icons],
                    value=icon_name,
                    on_change=ctx.callback(_set_preview_name),
                ),
            ],
        ),
        Column(
            gap=1,
            children=[
                Text("Size (px)", class_name="text-sm font-medium"),
                Select(
                    options=[
                        {"value": "16", "label": "16 (Small)"},
                        {"value": "24", "label": "24 (Medium)"},
                        {"value": "32", "label": "32 (Large)"},
                        {"value": "48", "label": "48 (Extra Large)"},
                        {"value": "64", "label": "64 (Huge)"},
                    ],
                    value=str(size),
                    on_change=ctx.callback(_set_preview_size),
                ),
            ],
        ),
        Column(
            gap=1,
            children=[
                Text("Color", class_name="text-sm font-medium"),
                Select(
                    options=[
                        {"value": "currentColor", "label": "Default"},
                        {"value": "red", "label": "Red"},
                        {"value": "blue", "label": "Blue"},
                        {"value": "green", "label": "Green"},
                        {"value": "orange", "label": "Orange"},
                        {"value": "purple", "label": "Purple"},
                    ],
                    value=color,
                    on_change=ctx.callback(_set_preview_color),
                ),
            ],
        ),
        Column(
            gap=1,
            children=[
                Text("Stroke Width", class_name="text-sm font-medium"),
                Select(
                    options=[
                        {"value": "1.0", "label": "1.0 (Thin)"},
                        {"value": "1.5", "label": "1.5"},
                        {"value": "2.0", "label": "2.0 (Default)"},
                        {"value": "2.5", "label": "2.5"},
                        {"value": "3.0", "label": "3.0 (Thick)"},
                    ],
                    value=str(stroke_width),
                    on_change=ctx.callback(_set_preview_stroke_width),
                ),
            ],
        ),
    ]

    color_val = None if color == "currentColor" else color

    preview = Container(
        class_name="flex items-center justify-center p-8 bg-muted/20 border rounded-lg h-32",
        children=[
            Icon(
                name=icon_name,
                size=size,
                color=color_val,
                stroke_width=stroke_width,
            )
        ],
    )

    color_arg = f', color="{color}"' if color != "currentColor" else ""
    stroke_arg = f", stroke_width={stroke_width}" if stroke_width != 2.0 else ""
    size_arg = f", size={size}" if size != 16 else ""

    code_text = f'Icon("{icon_name}"{size_arg}{color_arg}{stroke_arg})'

    code = Markdown(
        content=(
            f"```python\n"
            f"{code_text}\n"
            f"```"
        )
    )

    return playground_card(
        options=options,
        preview=preview,
        code=code,
    )


# ── Search Grid Section ───────────────────────────────────────────────────


def _icon_search_section(ctx: Context):
    search_query = ctx.state.get("icon_search_query", "").strip().lower()

    categorized = get_categorized_icons()

    filtered_categories = {}
    total_count = 0
    match_count = 0

    for cat, icons in categorized.items():
        total_count += len(icons)
        matching = [i for i in icons if search_query in i.lower()]
        if matching:
            filtered_categories[cat] = matching
            match_count += len(matching)

    # Search bar & status info
    search_bar = Container(
        class_name="mb-6",
        children=[
            Row(
                gap=3,
                align="center",
                children=[
                    Container(
                        class_name="flex-1",
                        children=[
                            Input(
                                name="icon_search",
                                placeholder="Search all icons...",
                                value=ctx.state.get("icon_search_query", ""),
                                on_change=ctx.callback(_on_search),
                                debounce=200,
                            )
                        ],
                    ),
                ],
            ),
            Row(
                justify="between",
                class_name="text-sm text-muted-foreground mt-2 px-1",
                children=[
                    Text(
                        f"Showing {match_count} of {total_count} icons"
                        if search_query
                        else f"Total: {total_count} icons available"
                    ),
                    Text("Click an icon card to copy code", class_name="italic"),
                ],
            ),
        ],
    )

    # List matching categories and icons
    category_views = []

    for cat, icons in filtered_categories.items():
        grid_items = []
        for name in icons:
            grid_items.append(
                Card(
                    on_click=ctx.callback(_on_copy, name=name),
                    class_name=(
                        "flex flex-col items-center justify-center p-4 border rounded-lg "
                        "hover:bg-accent hover:text-accent-foreground cursor-pointer "
                        "transition-all duration-200 text-center gap-3 aspect-square select-none"
                    ),
                    children=[
                        Icon(name=name, size=28, class_name="text-foreground"),
                        Text(
                            name,
                            class_name="text-xs text-muted-foreground font-mono truncate max-w-full",
                        ),
                    ],
                )
            )

        category_views.append(
            Column(
                gap=3,
                class_name="mt-8",
                children=[
                    Heading(
                        f"{cat} ({len(icons)})",
                        level=3,
                        class_name="text-lg font-semibold border-b pb-2 mb-2",
                    ),
                    Grid(
                        columns="repeat(auto-fill, minmax(110px, 1fr))",
                        gap=4,
                        children=grid_items,
                    ),
                ],
            )
        )

    if not category_views:
        category_views.append(
            Container(
                class_name="text-center py-12 border rounded-lg bg-muted/10 mt-8",
                children=[
                    Icon("search", size=32, class_name="mx-auto text-muted-foreground mb-2"),
                    Text("No icons match your search query", class_name="text-muted-foreground font-medium"),
                ],
            )
        )

    return Column(children=[search_bar, *category_views])


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Icon page."""
    from docs.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            _playground(ctx),
            Separator(class_name="my-8"),
            Heading("Available Icons", level=2, class_name="text-2xl font-bold mb-4"),
            _icon_search_section(ctx),
            Separator(class_name="my-8"),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Markdown Content ──────────────────────────────────────────────────────

INTRO = """
The `Icon` component renders Lucide icons by name. It supports custom sizing, coloring, and stroke weights.

```python
from refast.components import Icon

# Simple icon
Icon("home")

# Custom size and color
Icon("settings", size=24, color="blue")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str` | *(required)* | Lucide icon name (e.g. `"home"`, `"settings"`) or emoji fallback. |
| `size` | `int` | `16` | Icon height and width in pixels. |
| `color` | `str | None` | `None` | CSS color value (e.g. `"red"`, `"#ff0000"`, `"currentColor"`). |
| `stroke_width` | `float` | `2.0` | Thickness of the icon stroke lines. |
| `class_name` | `str` | `""` | Extra Tailwind classes applied to the icon. |
| `style` | `dict | None` | `None` | Inline CSS style dictionary. |

---

## Emojis / Fallback Text

If the provided name is not a valid Lucide icon name, the component will render it as plain text (perfect for emojis like `"🏠"` or `"⚙️"`).

```python
Icon("🏠", size=24)
```
"""
