"""Markdown — /docs/components/markdown."""

from typing import Any

from refast import Context
from docs.pages.components.common import render_doc_page
from refast.components import (
    Badge,
    Button,
    Container,
    Heading,
    Markdown,
    Row,
    Separator,
)

PAGE_METADATA = {
    "title": "Markdown",
    "route": "/docs/components/markdown",
    "icon": "file-text",
    "group": "Typography",
    "order": 5,
}

PAGE_TITLE = PAGE_METADATA["title"]
PAGE_ROUTE = PAGE_METADATA["route"]


async def handle_click(ctx: Context):
    count = ctx.store.local.get("click_count", 0) + 1
    ctx.store.local["click_count"] = count
    await ctx.show_toast(f"Custom component button clicked {count} times!", variant="success")
    await ctx.refresh()


def render(ctx: Context):

    if "click_count" not in ctx.store.local:
        ctx.store.local["click_count"] = 0
    click_count = ctx.store.local["click_count"]

    def make_badge(label: str, variant: str = "default"):
        return Badge(children=label, variant=variant)

    def make_button(label: str):
        return Button(label, on_click=ctx.callback(handle_click))

    def make_button_row(children: Any):
        return Row(
            class_name="flex flex-row gap-2 items-center p-2 border rounded bg-muted/10 my-2",
            children=children
        )

    custom_tags = {
        "StatusBadge": make_badge,
        "ClickButton": make_button,
        "ButtonRow": make_button_row,
    }

    demo_content = f"""
### Live Custom Tags Demo

Below is a live render of interactive Refast components embedded directly inside this Markdown block:

* **Self-closing tag with attributes:** A warning label: <StatusBadge label="Warning" variant="warning" />
* **State & callback binding:** <ClickButton label="Click Me" /> (Clicked **{click_count}** times)

**Container tags (horizontal row of buttons):**
<ButtonRow>
  <ClickButton label="Row Button 1" />
  <ClickButton label="Row Button 2" />
</ButtonRow>

---
"""

    sections = [
        Markdown(content=INTRO, enable_latex=True),
        Markdown(content=SHOWCASE, enable_latex=True),
        Heading("Custom Tags Demo", level=2, class_name="mt-8 mb-4"),
        Markdown(content=demo_content, custom_tags=custom_tags),
        Markdown(content=CUSTOM_COMPONENTS_DOC),
    ]
    return render_doc_page(
        ctx,
        title=PAGE_TITLE,
        route=PAGE_ROUTE,
        sections=sections,
        reference=REFERENCE,
    )


INTRO = """
Rich text rendering with **GitHub Flavored Markdown** (GFM), syntax-highlighted
code blocks, tables, task lists, and KaTeX math.

```python
from refast.components import Markdown

Markdown(content=\"\"\"
# Hello World

This is **bold** and *italic* text.

```python
print("Hello!")
```
\"\"\")
```
"""

SHOWCASE = r"""
## Showcase

Below is a live render of various Markdown features:

---

### Text Formatting

Regular text, **bold**, *italic*, ~~strikethrough~~, and `inline code`.

> Blockquote: "Design is not just what it looks like and feels like. Design is how it works."
> — Steve Jobs

---

### Headings

# Heading 1
## Heading 2
### Heading 3
#### Heading 4

---

### Lists

**Unordered:**
- Item one
- Item two
  - Nested item
  - Another nested item
- Item three

**Ordered:**
1. First step
2. Second step
3. Third step

**Task list:**
- [x] Install Refast
- [x] Create your first page
- [ ] Deploy to production

---

### Code Block

```python
from refast import RefastApp, Context
from refast.components import Container, Heading, Button

ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="p-8",
        children=[
            Heading("Welcome", level=1),
            Button("Click me"),
        ],
    )
```

---

### Table

| Component | Category | Interactive |
|-----------|----------|-------------|
| `Button` | Actions | ✓ |
| `Input` | Forms | ✓ |
| `Markdown` | Typography | — |
| `Card` | Containers | — |

---

### Math (KaTeX)

Inline math: $E = mc^2$

Block math:

$$
\int_{-\infty}^{\infty} e^{-x^2}\, dx = \sqrt{\pi}
$$

The quadratic formula: $x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}$
"""

CUSTOM_COMPONENTS_DOC = """
## Custom Components (Custom Tags)

Refast's `Markdown` component allows you to embed **interactive Refast components** directly inside standard Markdown text blocks using HTML-like tags (e.g. `<MyTag />` or `<MyContainer>content</MyContainer>`).

### How It Works

1. **Register Tag Callables**: Pass a dictionary of `custom_tags` to the `Markdown` component.
   - The key is the tag name. It **must** start with an uppercase letter (e.g., `StatusBadge`, `ActionButton`).
   - The value is a Python callable (a function or class constructor) that returns a Refast `Component`.
2. **Pydantic Validation & Coercion**: When Refast encounters a registered tag in the Markdown content, it extracts the attributes and passes them to your callable. Arguments are validated and coerced (e.g. string numbers like `"42"` to `int`/`float`, or string values to `Enum` types) using Pydantic validation based on the callable's signature.
3. **Container Tags**: If a tag is used as a container (e.g. `<MyCard>Some text</MyCard>`) and the registered callable accepts a parameter named `children` or `content`, Refast automatically parses the inner content and passes it in (either as a nested `Markdown` component or a raw string).
4. **Interactive Callbacks**: Since these are full Refast components, you can hook them up to Python callbacks using `ctx.callback(...)`.

### Simple Example

Here is how you define and use custom tags:

```python
from typing import Any, Literal
from refast import Context
from docs.pages.components.common import render_doc_page
from refast.components import Badge, Button, Markdown, Row

# 1. Define a module-level callback
async def increment_counter(ctx: Context):
    ctx.store.local["counter"] = ctx.store.local.get("counter", 0) + 1
    await ctx.show_toast("Incremented counter!")
    await ctx.refresh()

# 2. Inside your page handler
def my_page(ctx: Context):
    # Setup state
    counter_val = ctx.store.local.get("counter", 0)

    # Define tag factory callables
    def make_badge(label: str, variant: Literal["default", "secondary", "destructive"] = "default"):
        return Badge(children=label, variant=variant)

    def make_button(label: str):
        return Button(label, on_click=ctx.callback(increment_counter))

    def make_button_row(children: Any):
        return Row(
            class_name="flex flex-row gap-2 items-center p-2 border rounded bg-muted/10 my-2",
            children=children
        )

    # Register the tags
    custom_tags = {
        "StatusBadge": make_badge,
        "ClickButton": make_button,
        "ButtonRow": make_button_row,
    }

    markdown_text = f\"\"\"
# Welcome to my page

Current status: <StatusBadge label="Beta" variant="secondary" />

Click the button below to update:
<ClickButton label="Click Me" />

Total Clicks: **{counter_val}**

Or use a container tag to group buttons horizontally:
<ButtonRow>
  <ClickButton label="Yes" />
  <ClickButton label="No" />
</ButtonRow>
\"\"\"

    return Markdown(content=markdown_text, custom_tags=custom_tags)
```
"""

REFERENCE = r"""
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `str` | *(required)* | Markdown string to render |
| `allow_html` | `bool` | `False` | Allow raw HTML inside markdown (security risk) |
| `enable_mermaid` | `bool` | `False` | Enable Mermaid diagram rendering for fenced blocks |
| `enable_latex` | `bool` | `False` | Enable LaTeX / KaTeX math rendering ($..$ and $$..$$) |
| `custom_tags` | `dict[str, Callable[..., Component]] \| None` | `None` | A dictionary mapping tag names (str) to callables that return a component |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes on the wrapper |

## Features

- **GFM** — GitHub Flavored Markdown: tables, strikethrough, task lists
- **Syntax highlighting** — fenced code blocks with language detection
- **KaTeX math** — inline `$...$` and block `$$...$$` LaTeX
- **Custom Tags** — embed interactive components inside markdown text
- **Security** — HTML is stripped by default (`allow_html=False`)

## Notes

- `allow_latex` is deprecated (LaTeX is always rendered); it is accepted for
  backward compatibility but ignored.
- For untrusted content never set `allow_html=True`.
"""

