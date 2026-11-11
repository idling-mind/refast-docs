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

### Discovery & SEO

- [x] ~~Per-page metadata~~ partially: the shell carries a description, Open Graph and
      Twitter tags, `/robots.txt` and a `/sitemap.xml` of all 108 registered pages.
      Because refast serves one static shell for every route, `<title>`, `og:url` and
      `canonical` can only describe the root — a crawler or link preview never sees
      "Sessions" as the title of `/docs/advanced/sessions`.
- [x] ~~Prerender or server-render the shell per route~~ — done in site code instead of
      framework code: the `per_route_head` middleware in `docs/app.py` rewrites title,
      description, `og:*`, `canonical` and adds a Markdown `alternate` plus JSON-LD, so
      each page is addressed as itself. `docs/route_head.py` says why, and
      `tests/test_docs_route_head.py` that a tag was replaced rather than stacked.
      Framework support (`head_tags=` on `@ui.page`, or `render_shell_for=path`) would
      still be the better home for it: this pays for a regex pass over a document that
      never needed one, and it cannot give a route a different body.
- [ ] Add an `og:image` (1200×630) and point `og:image` at it; previews are currently
      text-only because `public/` holds nothing but a favicon.
- [ ] Set `REFAST_DOCS_URL` on preview deployments, or they will claim
      `refast.fastapicloud.dev` as canonical.

### Machine-readable surfaces

- [x] ~~Give LLMs something to fetch~~ — done: `docs/markdown_export.py` renders each
      page and converts the tree back to Markdown, served at `<route>.md`
      (`/index.md` for `/`), indexed in `/llms.txt`, concatenated in
      `/llms-full.txt`, described in `/api/pages.json`, and searchable through
      `/api/search?q=`. `docs/pages/getting_started/ai_agents.py` documents it for
      readers; `tests/test_docs_llm_surfaces.py` holds it in place.
- [ ] **Serve the mirrors' HTML twin.** A prerendered `/docs/concepts/state.html` (or
      a `?_escaped_fragment`-style static export) would let Google-class crawlers index
      the text at the canonical URL instead of at a `.md` sibling. Same generator.
- [ ] Content negotiation on the page routes: `Accept: text/markdown` returning the
      mirror, so a client that knows the page URL but not the convention still gets
      text. The `.md` suffix is the documented path today.
- [ ] **MCP server** exposing `search_docs`, `get_page`, `list_pages` over the same
      modules (`/.well-known/mcp/server-card.json` for discovery, plus a stdio shim).
      The JSON API is the substrate; the server is packaging.
- [ ] "Copy page as Markdown" in the footer, next to "View as Markdown", for the human
      who pastes documentation into a chat.
- [ ] A one-page cheat sheet (`/docs/cheatsheet.md`, under ~2k tokens: app skeleton,
      the components that cover most apps, the `ctx` API, the five mistakes) and point
      `/llms.txt`'s blockquote at it as the thing to read first. Most agent sessions
      need exactly that and nothing else.
- [ ] Error-first troubleshooting page, keyed by the literal text of exceptions
      (`store_as` is FastUI's API, not refast's, is one such entry already). Agents
      retrieve by pasting an error, and today they would find nothing.

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
- [ ] Input + `ctx.save_prop` / `props=[...]` demo. The previous item here asked for a
      `store_as` demo; `store_as` is FastUI's API and does not exist in refast 0.12 or
      0.13 -- grep found it nowhere in either — so it was unsatisfiable as written.
- [ ] Card composition demo
- [ ] Tabs demo
- [ ] Chart demo (one per chart type)
- [ ] Dialog/Sheet/Drawer demo
- [ ] Toast variants demo (with working buttons)

### Search

- [x] ~~`/search?q=` for readers whose query is too vague for the palette~~ — done: the
      results page ranks server-side, shows the section on the right of each row, and
      bolds the matched words in a snippet. It is the only surface with `search.search()`.
- [x] ~~Palette rows labelled `Title — Section`~~ — done, and superseded: the section is
      now a right-aligned muted span at the end of each row (`PaletteRow` in `docs/app.py`),
      and the rows sit in one flat list. Grouping them by section made every tie fall back
      to DOM order, so Getting Started led every search.
- [x] ~~Nothing should be pre-selected while typing~~ — done: Enter goes to
      `/search?q=…` unless ArrowUp/ArrowDown moved the caret first. cmdk highlights its top
      match as soon as there is one and the Command wrapper exposes no way to turn that off,
      so the script in the shell reads intent from the keys instead.
- [x] ~~The "Nothing matched" hint rendered wrong~~ — done: it is a Markdown paragraph in a
      Row of its own, with `save_prop` code-fenced. Snippets keep their backticks for the
      same reason; stripped of them, an underscore opens an emphasis run and the line loses
      its spaces.
- [x] ~~The palette scrolls away from its own results~~ — done: cmdk does not sort, only
      show-or-hide, so rows stayed in sidebar order and it selected the first visible one,
      a dozen rows down for a query like "form", then scrolled it into view. The shell
      script now re-orders the rows by where the query falls in each keyword blob and
      resets the list's scroll, in the capture phase of `input`, before cmdk filters.
- [ ] **Verify the palette in a browser.** The row structure, the flat list and the script
      are asserted in tests, and the ranking was simulated in node against the real blobs
      (`form` → Form instead of Column, `session` → Sessions instead of State & Store). But
      nothing here has been seen in a real tab: cmdk's `data-selected` styling can still
      make a row look chosen while you type, and the reorder happens to DOM nodes React
      believes it owns.
- [ ] `/search` has no entry in the sidebar, so it is only reachable from the palette
      hand-off row, the Enter key, or a URL. Adding it to `NAV_SECTIONS` would make it
      searchable-by-content, which is circular, and the sitemap already lists it.
- [ ] Index the examples and the home page too; today only `NAV_SECTIONS` routes are
      searchable, so "counter" finds the guide page but not `/examples/counter`.
- [ ] The keyword blobs cost ~9 KB when the palette opens. If that ever matters, the
      corpus could be fetched once and cached in the browser instead of riding in the
      dialog tree.
- [ ] The Icons page (`/docs/components/icon`) filters the way the palette used to: a
      controlled `Input` plus `await ctx.refresh()` per keystroke, which re-renders every
      icon tile and echoes the value back one change behind. The same fix applies to any
      page that filters a long list.

---

## Quality Gates

CI (`.github/workflows/ci.yml`) runs `tests/`, which guard the docs against upstream
refast releases:

| Test | Catches |
|------|---------|
| `test_docs_pages_render.py` | a page function that raises while building its tree (bad props, bad imports, bad return) |
| `test_docs_component_props.py` | a prop passed to a component that does not accept it |
| `test_docs_links.py` | links to unregistered routes, "View source" URLs that 404, and "Edit this page" URLs whose file is gone |
| `test_docs_markdown_tables.py` | Markdown tables that render with the wrong number of columns |
| `test_docs_search.py` | pages that vanished from the search index, and ranking that stopped reflecting page text |
| `test_docs_llm_surfaces.py` | a Markdown mirror that serves the shell, an empty export, a `{{ demo_app }}` marker that leaked, or an index that no longer matches the sidebar |
| `test_docs_route_head.py` | a page whose title, canonical URL or description still describes the site, a tag stacked instead of replaced, a stale `content-length`, a mirror nobody advertises |
| `test_docs_shell.py` | the HTML document every tab and crawler sees first: title, favicon, share metadata, robots.txt, sitemap.xml |

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
