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

Then open http://localhost:8000. `uv sync` resolves refast from the configured package
index; run `uv lock` first if there is no `uv.lock` in the checkout (and once more after
pulling this change, so the `dev` group gets recorded in the lockfile).

## Checking your changes

Everything the site claims is verified by tests, so run them before pushing:

```bash
uv run pytest                     # render every page, links, props tables
uv run ruff check docs tests      # lint
REFAST_REPO=../refast uv run pytest  # also resolve every "View source" link
```

`tests/` renders every page function, rejects props that the installed components do not
accept, checks that every link leads to a registered route, and asserts that the Markdown
tables have the right number of columns. CI runs them on Python 3.12 and 3.13 against the
newest refast release, so a framework change that breaks a page fails here rather than in
a reader's browser.

Contributions are welcome!
