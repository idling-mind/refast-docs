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

Two surfaces, because one row of text cannot do both jobs.

**`⌘K` navigates.** The palette is one flat list of every page in `NAV_SECTIONS`: the
page title on the left, its section right-aligned and muted on the right. cmdk
filters that list **in the browser** against each row's `value`. That is not a
preference: refast's `Command` wrapper forwards neither `shouldFilter` nor extra
props, so the server cannot take cmdk's filter away -- it can only choose what the
value contains. `docs/search.py` reads each page module with `ast`, indexes every
string literal of 120 characters or more, and gives each page a blob: its nav label,
its `PAGE_TITLE`, its section, then its most distinctive terms in tf-idf order.

Nothing in cmdk sorts on that blob. A row's score decides only whether it is shown;
the rows you see stay in DOM order, which for us is sidebar order, and the row cmdk
selects is the first *visible* one in that order. Searching "form" therefore landed on
Column, a dozen rows down, and scrolled the list away from the page called Form. So a
small script on the shell re-orders the rows by where the query falls in each blob --
position 0 means the page is named for it -- and resets the list's scroll, in the
capture phase of `input`, so that the order cmdk filters and selects from is already
the ranked one. Ordering the blob by tf-idf is what makes that read correctly: the
page called Styling leads with the word, the nine pages that mention styling do not.

Nothing is pre-selected by typing either. cmdk highlights its top match as soon as
there is one, and Enter would otherwise open it; the same script reads intent from the
keys instead -- Enter goes to `/search?q=…` unless ArrowUp/ArrowDown moved the caret
first. The rows are not grouped by section either, because a group is a bucket in DOM
order and cannot rank: groups that tie fall back to the sidebar, and Getting Started
led every search while they existed.

Driving the ranking from the server was tried first and failed twice: a controlled
input echoes one keystroke behind, so letters dropped; and with values rewritten
per keystroke, cmdk scored its live string against the stale echo, scored 0, and hid
everything. The palette input is deliberately uncontrolled, and its `ctx.save_prop`
mirror stays out of the render path -- `save_prop` writes to the browser's prop store
and makes no round trip at all, which is why ranking the rows from Python per keystroke
was never on the table.

**`/search` answers.** The results page ranks server-side (title 8x, headings 4x,
idf-scaled, plus a bonus when the whole phrase is a title), shows the section on the
right of every row, and bolds the matched words inside a snippet drawn from the
page's prose -- the thing a palette row cannot say. Snippets keep their backticks for
that reason: stripped of them, `` `save_prop` `` reaches the Markdown renderer as bare
text, the underscore opens an emphasis run, and the rest of the line loses its spaces
and turns italic. The query is a URL parameter (`/search?q=styling`), so results can
be linked and reopened, and the form means typing costs nothing until it is submitted.
The palette's first row hands off to it.

Measured: a closed palette is 242 bytes and ordinary pages no longer carry a 30 KB
title list at all; opening it sends 9 KB of keywords.

Two consequences when writing a page:

- Put explanation in a `CONTENT` string (or any long literal). A page whose text
  exists only inside `Heading(...)` calls is searchable by its title alone.
- Keep `PAGE_TITLE` a plain assignment; that is what the extractor reads.

`tests/test_docs_search.py` asserts one thing per page: that it contributes real
prose to the index. A new page that fails it is thin, not broken. It also pins the
ranking (`styling` is the canary), the uncontrolled input, the keyword budget, and
that every result link and section badge on `/search` points at something that
exists.

## For AI Agents

Each section folder contains an `AGENT_INSTRUCTIONS.md` with detailed per-page content
requirements, source files to read, and examples to include. Start there.
