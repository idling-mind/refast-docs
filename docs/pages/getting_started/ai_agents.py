"""AI & Machine-Readable Docs — /docs/ai-agents."""

from refast import Context
from refast.components import Container, Heading, Markdown, Separator

PAGE_TITLE = "AI & Machine-Readable Docs"
PAGE_ROUTE = "/docs/ai-agents"

CONTENT = r"""
Every page on this site is written for two readers. The one you are looking at is a
Refast app, which means its text is assembled in your browser — and a reader that
cannot run JavaScript would fetch it and find nothing. So each page has a second
form: plain Markdown, generated from the same components you are reading.

If you are a person skimming for a `curl` command, it is this:

```bash
curl -s https://refast.fastapicloud.com/llms.txt          # the whole site, as an index
curl -s https://refast.fastapicloud.com/docs/concepts/state.md   # one page, as text
curl -s "https://refast.fastapicloud.com/api/search?q=save_prop" # find the page by content
```

## The surfaces

| Surface | What it is for |
|---------|----------------|
| `<page url>.md` | One page as Markdown — the page's URL plus `.md`, e.g. `/docs/concepts/state.md`. The landing page is `/index.md`. |
| [`/llms.txt`](/llms.txt) | An index of every page: title, one-line summary, section headings, and a link to the Markdown form. Written to the [llms.txt](https://llmstxt.org) convention. ~6k tokens. |
| [`/llms-full.txt`](/llms-full.txt) | Every page concatenated, in navigation order, for a prompt that wants the whole documentation at once. ~100k tokens. |
| [`/api/pages.json`](/api/pages.json) | The same inventory as data: route, title, section, headings, source file and token estimate per page, so a program can plan what to read. |
| [`/api/search?q=…`](/api/search?q=save_prop) | Ranked results over the text of every page, as JSON, with a snippet and the matching page's `.md` URL. |
| [`/sitemap.xml`](/sitemap.xml) | The HTML routes, for crawlers that want to render JavaScript. |

Markdown mirrors make each page fetchable; the search API is what makes the site
*navigable* without downloading the whole site into a context window, which no prompt
wants to spend on it.

## What a page URL says about itself

One shell is served for every route, so the metadata in it would otherwise describe the
site wherever you fetched it. Each page's HTML therefore carries its own title
(`State & Store — Refast Docs`), its own description — the first sentence of the page,
stated once in prose and reused here — a `canonical` that names the page rather than the
root, Open Graph tags for link previews, and:

```html
<link rel="alternate" type="text/markdown" href="/docs/concepts/state.md">
```

which is how a client that fetched the page, rather than the index, learns that a text
version exists. Pages also embed `TechArticle` and `BreadcrumbList` JSON-LD, so an
engine that reads schema instead of prose can tell what the page is about and where it
sits.

## Pointing an assistant at it

Paste the starting URL into the tool's instructions rather than hoping it guesses:

```text
Refast documentation: fetch https://refast.fastapicloud.com/llms.txt for the index,
then fetch only the .md pages you need. Answer from those pages, and cite their URLs.
```

- **Claude Code / Cursor / Codex** — add that block to the project's rules file, or ask
  for it in the prompt when a question is framework-specific.
- **A RAG pipeline** — crawl `/llms.txt`, fetch the links it lists, and split on `## `;
  the mirrors contain no navigation, footer or chrome to strip.
- **A chat widget with a "context" budget** — feed it `/llms-full.txt`, or `/llms.txt`
  plus the two or three pages the question needs.

A useful habit, when an answer names a component or an argument you do not recognise:
ask for the page it came from. Every mirror states its own URL and the file it was
built from, and the search API's `snippet` quotes the sentence that matched.

## What the Markdown leaves out

A live example is a running app, not a paragraph, so mirrors replace playgrounds and
embedded demos with a line saying so and a link to the page. If a mirror mentions
**Live examples**, the interactive version is at the URL in its header — component
props tables, code and prose are all there; the widgets are not.

Everything else is complete, including the tables, which reach you with `\|` escaped:
in a Markdown table a bare `|` would end the cell.

## How it stays correct

The mirrors are not files. Each one is built on request by rendering the page function
and converting the component tree back into Markdown, so a page cannot be updated and
forgotten at the same time — and the props tables inside them come from the installed
`refast`, so a released rename shows up rather than rotting.

`tests/test_docs_llm_surfaces.py` holds the rest of the contract: every page in the
navigation has a mirror, no mirror serves an empty shell, no demo-app marker leaks, and
every link inside exported text leads to a route that exists.
"""


def render(ctx: Context):
    from docs.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)
