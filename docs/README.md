# Refast Documentation Site

A comprehensive documentation site for the Refast framework, **built with Refast itself**.

## Quick Start

```bash
# From the project root
uvicorn docs.app:app --reload --port 8000
```

Open http://localhost:8000

## Structure

```
docs/
├── app.py                      # Main app, shared layout, route registrations
├── AGENT_INSTRUCTIONS.md       # Top-level instructions for AI agents
├── TODO.md                     # Known issues tracker
├── README.md                   # This file
└── pages/
    ├── home.py                 # Landing page (/)
    ├── getting_started/        # Installation, Architecture, Quick Tour, Examples
    ├── concepts/               # Components, Callbacks, State, Store, Updates, etc.
    ├── components/             # Full API reference for all UI components
    └── advanced/               # Component dev, Extension dev, Security, Sessions, Styling
```

## Adding a Page

1. Create `pages/<section>/<name>.py` with `PAGE_TITLE`, `PAGE_ROUTE`, and `render(ctx)`
2. Import it in `app.py` and add it to `NAV_SECTIONS` as `(label, route, icon, render)`
   — `register_nav_routes()` registers the route, so no `@ui.page()` handler is needed
3. Component pages under `pages/components/` need neither: give the module a
   `PAGE_METADATA` dict and `components/registry.py` discovers it
4. Run `uv run pytest` — it renders every page and checks links, props and tables

## Page Template

```python
"""Page Title — /docs/route."""
from refast.components import Container, Heading, Markdown, Separator

PAGE_TITLE = "Page Title"
PAGE_ROUTE = "/docs/route"

def render(ctx):
    from docs.app import docs_layout
    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content="Your content here"),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)
```

## Search

`⌘K` searches the text of every page, not just the label in the sidebar -- and it
filters **in the browser**. `docs/search.py` reads each page module with `ast` and
indexes every string literal of 120 characters or more; from that index it derives
a short keyword blob per page (title, headings, the ~20 most weighted terms), and
the palette puts that blob in the `value` of the page's `CommandItem`. cmdk scores
`value` against the typed text locally, so matching costs no round trip.

Why not rank on the server? refast's `Command` wrapper forwards neither
`shouldFilter` nor extra props, so cmdk's filter cannot be switched off; and
routing keystrokes through the server means either a controlled input, which
echoes one keystroke behind and drops letters, or item values that lag the
browser's search string by a keystroke -- which cmdk scores at zero, so nothing
matches. Both were tried. Local scoring is the only shape that works with the
component as shipped.

Costs, measured: every page used to carry a 30 KB palette of titles. Now a closed
palette is 242 bytes and opening it sends 56 KB once, of which 25 KB is the
keyword corpus. `search()` still ranks server-side with idf weighting, which is
what a future `/search?q=` page would use.

Two consequences when writing a page:

- Put explanation in a `CONTENT` string (or any long literal). A page whose text
  exists only inside `Heading(...)` calls is searchable by its title alone.
- Keep `PAGE_TITLE` a plain assignment; that is what the extractor reads.

`tests/test_docs_search.py` asserts one thing per page: that it contributes real
prose to the index. A new page that fails it is thin, not broken. It also asserts
the input stays uncontrolled and that no page's blob exceeds 420 characters.

## For AI Agents

Each section folder contains an `AGENT_INSTRUCTIONS.md` with detailed per-page content
requirements, source files to read, and examples to include. Start there.
