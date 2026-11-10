# Refast Documentation

[Refast](https://github.com/idling-mind/refast) is a framework that enables building reactive web applications with
Python-first development. It uses FastAPI for the backend and React with shadcn/ui for the frontend.

This site is built **with Refast itself** — the pages you read are rendered by the same
framework they document.

## Running the documentation locally

```bash
git clone https://github.com/idling-mind/refast-docs.git
cd refast-docs
uv sync
uv run uvicorn main:app --reload
```

Then open http://localhost:8000. `uv sync` installs from the lockfile, which resolves
refast and its dependencies from the public index; refast itself is not vendored here,
so the site tracks whatever version the lock (or your index) provides.

## Checking your changes

Everything the site claims is verified by tests, so run them before pushing:

```bash
uv run pytest                     # render every page, links, props tables
uv run ruff check docs tests      # lint
REFAST_REPO=../refast uv run pytest  # also resolve every "View source" link
```

`tests/` renders every page function, rejects props that the installed components do not
accept, checks that every link leads to a registered route, asserts that the Markdown
tables have the right number of columns, verifies that every page contributes text to the
search index, and checks the HTML document every tab and crawler sees first — title,
favicon, share metadata, `robots.txt`, `sitemap.xml`. CI runs them on Python 3.12 and 3.13
against the newest refast release, so a framework change that breaks a page fails here
rather than in a reader's browser.

## What the site offers readers

- `⌘K` navigates by page title and text, filtered in the browser; `/search?q=…`
  ranks server-side, shows each result's section, and marks what matched
  (`docs/search.py`, `docs/pages/search_results.py`)
- every page links to its own source file in the footer, and to the framework's
  source where a component is documented
- `/robots.txt` and `/sitemap.xml` for machines, and light/dark plus five colour
  themes for everyone else

Contributions are welcome!
