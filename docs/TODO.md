# Refast Documentation — Known Issues & TODOs

Issues discovered during documentation site development. Fix these in the framework
or document them as known limitations.

---

## Framework Issues

### 1. DataTable component may be non-functional
- **Location:** `src/refast/components/shadcn/data_display.py` → `DataTable`
- **Evidence:** `examples/data_table/app.py` builds tables manually from `Table`/`TableRow`/`TableCell` primitives rather than using the `DataTable` component
- **Action:** Verify if `DataTable` works. If not, either fix it or mark as experimental in docs.

### 2. Stage 8 plan uses outdated theme API
- **Location:** `plan/stage-8-docs.md`
- **Evidence:** References hex color constructors, but `Theme` now uses Pydantic `ThemeColors` with HSL tokens
- **Action:** Update the plan file or mark as superseded.

### 3. `style` prop usage inconsistency
- **Location:** `.github/copilot-instructions.md` says "No inline styles" but `docs/STYLING_GUIDE.md` explicitly documents `style` as supported for dynamic values
- **Evidence:** Several examples use `style={"display": "none"}` for conditional visibility
- **Action:** Clarify the guideline — `style` is fine for dynamic values, not for static styling.

### 4. No wildcard/catch-all route support
- **Evidence:** `examples/multi_page/app.py` and all examples register each page explicitly. No `@ui.page("/docs/*")` pattern exists.
- **Action:** Document as a known limitation. Consider implementing wildcard routes.

### 5. `ctx.state` unavailable on initial HTTP GET
- **Evidence:** Page handlers run for both HTTP GET (initial load) and within WebSocket context. On HTTP GET, there's no persistent state — `ctx.state` is empty.
- **Action:** Document clearly that state is only meaningful within callback/WebSocket context. Recommend using `ctx.store` for initial-load-required values.

### 6. Markdown component capabilities underdocumented
- **Evidence:** The `Markdown` component supports GFM (tables, strikethrough), syntax highlighting (via react-syntax-highlighter), and KaTeX math equations. None of this is mentioned in existing documentation.
- **Action:** Document all Markdown features in the Typography components reference page.

---

## Documentation TODOs

### Content Completion

Every page now has real prose; the `> **TODO**` banners are gone (the last one, on
`advanced/sessions.py`, was removed when that page was rewritten against the actual
session API). What is missing is pages for the workflows a reader hits after the
tutorial:

- [ ] Deployment — process managers, workers, `uvicorn main:app`, reverse proxy and
      HTTPS cookie settings, a Dockerfile
- [ ] Changelog / migration notes per refast release, breaking changes called out
- [ ] Troubleshooting / FAQ — the errors a reader actually sees in a console
- [ ] Extension version matrix — which of `refast-echarts` / `refast-grid` /
      `refast-vtk-js` needs which core

Sections still thinnest relative to how often they are used: Getting Started
(architecture), and the component pages that carry code samples but no live example.

### Live Examples

Many component reference pages need live interactive examples (actual Refast components
rendered alongside their code snippets). Priority:

- [ ] Button variants demo
- [ ] Input + store_as demo
- [ ] Card composition demo
- [ ] Tabs demo
- [ ] Chart demo (one per chart type)
- [ ] Dialog/Sheet/Drawer demo
- [ ] Toast variants demo (with working buttons)

### Search

- [ ] Implement in-page search using `Command*` components (client-side filtering of sidebar items)
  - Current state: `⌘K` filters page *titles* only (`_get_search_items()` in `app.py`); page
    bodies are not indexed.

---

## Quality Gates

CI (`.github/workflows/ci.yml`) runs `tests/`, which guard the docs against upstream
refast releases:

| Test | Catches |
|------|---------|
| `test_docs_pages_render.py` | a page function that raises while building its tree (bad props, bad imports, bad return) |
| `test_docs_component_props.py` | a prop passed to a component that does not accept it |
| `test_docs_links.py` | links to unregistered routes and "View source" URLs that 404 |
| `test_docs_markdown_tables.py` | Markdown tables that render with the wrong number of columns |

Open items:

- [x] ~~Import hygiene sweep~~ — done: `ruff check --select F401 --fix` removed 429 unused
      imports from `docs/`, and `F401` is now part of the default rule set. Component pages
      import only what they instantiate; names shown inside their Markdown samples are
      illustrative and need no import.
- [ ] Commit `uv.lock`? It is still untracked. A recent `uv sync` re-resolved it against
      the public index (no internal-feed URLs remain), so committing it would now make
      `uv sync --locked` work for contributors and CI alike — confirm before doing so, in
      case the internal mirror was pinned on purpose.
- [x] ~~Commit `uv.lock`?~~ — done: tracked, resolved against the public index. A
      `uv sync` on a machine whose `UV_DEFAULT_INDEX` points at an internal mirror
      rewrites those URLs back, so re-run `uv lock` with the public index before
      committing a changed lock.
- [ ] Run the suite against a framework checkout in a scheduled job
      (`REFAST_REPO=../refast pytest`), which also verifies every "View source" link.
