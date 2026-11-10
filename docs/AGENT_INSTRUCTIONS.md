# Refast Documentation Site — Agent Instructions

## Project Overview

This is a **documentation site for the Refast framework**, built using Refast itself (dogfooding).
It runs as a standard Refast app with a sidebar-based layout and 30+ pages of documentation.

## How to Run

```bash
cd <project_root>
uvicorn docs.app:app --reload --port 8000
```

Open http://localhost:8000 in your browser.

## Architecture

- **`app.py`** — Main app. Contains `RefastApp`, shared `docs_layout()` function, all route registrations.
- **`pages/`** — Each page is a Python module with a `render(ctx)` function.
- **Navigation** — Sidebar with 4 sections (Getting Started, Concepts, Components, Advanced). SPA navigation via `ctx.load()`.
- **Content** — Primarily `Markdown(content="""...""")` blocks for prose, with real Refast components for live examples.

## Content Format Rules

1. **Page structure**: Every page's `render(ctx)` returns `docs_layout(ctx, content, PAGE_ROUTE)` where content is wrapped in `Container(class_name="max-w-4xl mx-auto p-6", children=[...])`.
2. **Title**: Start with `Heading(PAGE_TITLE, level=1)` followed by `Separator(class_name="my-4")`.
3. **Prose**: Use `Markdown(content="""...""")` for body text, tables, code blocks.
4. **Live examples**: Embed actual Refast components alongside their code snippets so readers see both the code and the rendered result.
5. **Callouts**: Use `Alert(title="...", message="...")` for important notes.
6. **Code examples**: Use triple-backtick code blocks inside the Markdown text. The Markdown component supports syntax highlighting.
7. **Cross-links**: Reference other pages by their routes (e.g., `[State Management](/docs/concepts/state)`).
8. **Tables**: `Markdown` renders with `remark-gfm`, which splits cells on **every** `|` in a row — including inside code spans. Escape type unions as `\|` (write `` `str \| None` ``, never `` `str | None` ``), and keep the cell count identical to the header row. Because `\|` is an invalid Python escape sequence, store table content in **raw** strings (`CONTENT = r"""…"""`).

## Adding a New Page

1. Create `pages/<section>/<page_name>.py` with `PAGE_TITLE`, `PAGE_ROUTE`, and `render(ctx)`.
2. Add the page to `NAV_SECTIONS` in `app.py` — import the module and list it as
   `(label, route, icon, module.render)`. Routes are registered from `NAV_SECTIONS`
   by `register_nav_routes()`; do **not** add a separate `@ui.page()` handler, or the
   route gets registered twice and the second definition shadows the first.
3. Component pages under `pages/components/` skip step 2 entirely: create the module
   with a `PAGE_METADATA` dict (`title`, `route`, `icon`, `group`, `order`) and
   `pages/components/registry.py` picks it up. A module without `PAGE_METADATA`
   silently lands in the "Utility" group.
4. For a component's Props table, use `props_table(Component)` from
   `pages/components/props_table.py` instead of typing one — it reads the installed
   signature and docstring, so it cannot go stale or emit a broken row.

## Checking Your Work

```bash
uv run pytest                      # renders every page, checks links and tables
uv run ruff check docs tests       # lint
```

The suite in `tests/` is the contract with refast: it renders every registered page,
rejects props the components do not accept, fails on links to unregistered routes, and
checks that every Markdown table has as many cells as its header. If you rename a route,
update the pages that link to it or `test_docs_links.py` will fail.

## Available Components for Documentation

From `refast.components`: Container, Flex, Row, Column, Grid, Center, Heading, Text, Paragraph, Code, Link, Markdown, Badge, Icon, Button, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Tabs, TabItem, Accordion, AccordionItem, AccordionTrigger, AccordionContent, Alert, Separator, Table, TableHeader, TableBody, TableRow, TableHead, TableCell, and many more.

## Source Files Reference

When writing documentation content, read these source files for accuracy:

| Topic | Source Files |
|-------|-------------|
| App & Router | `src/refast/app.py`, `src/refast/router.py` |
| Context | `src/refast/context.py` |
| State | `src/refast/state.py` |
| Store | `src/refast/store.py` |
| Components (base) | `src/refast/components/base.py` |
| Components (shadcn) | `src/refast/components/shadcn/*.py` |
| Events | `src/refast/events/types.py`, `src/refast/events/manager.py` |
| Streaming | `src/refast/events/stream.py` |
| Broadcasting | `src/refast/events/broadcast.py` |
| Sessions | `src/refast/session/` |
| Security | `src/refast/security/` |
| Theme | `src/refast/theme/` |
| Extensions | `src/refast/extensions/` |
| Examples | `examples/` (25+ working examples) |
| Existing docs | `docs/*.md` |

## Known Issues

See `TODO.md` in this directory for tracked issues found during development.

## Section-Specific Instructions

Each section folder has its own `AGENT_INSTRUCTIONS.md` with per-page content requirements:

- `pages/getting_started/AGENT_INSTRUCTIONS.md`
- `pages/concepts/AGENT_INSTRUCTIONS.md`
- `pages/components/AGENT_INSTRUCTIONS.md`
- `pages/advanced/AGENT_INSTRUCTIONS.md`
