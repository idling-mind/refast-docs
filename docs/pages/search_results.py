"""Full-text search results — /search.

The ⌘K palette navigates: it is a command palette, so its rows are one line of
text scored by cmdk in the browser, and neither of those is a place to explain
*why* a page matched. This is the page for that query -- ranked server-side over
the text of every page, with the section on the right of each row and the matched
words marked in the snippet.

The query lives in the URL (``/search?q=…``), so results can be linked, reopened
and shared, and typing costs nothing until the form is submitted.
"""

from urllib.parse import quote

from refast import Context
from refast.components import (
    Badge,
    Button,
    Column,
    Container,
    Form,
    Heading,
    Input,
    Link,
    Markdown,
    Row,
    Separator,
    Text,
)

from .. import search as search_index

PAGE_TITLE = "Search"
PAGE_ROUTE = "/search"


async def run_search(ctx: Context, q: str = ""):
    """Go to the results for ``q``; the URL is the state."""
    await ctx.load(f"{PAGE_ROUTE}?q={quote(q.strip())}" if q.strip() else PAGE_ROUTE)


def render(ctx: Context):
    """Render the results page for the query in the URL."""
    from docs.app import docs_layout

    params = ctx.query_params
    # A property in refast 0.12 and 0.13; a method in some releases. Asking the
    # object, not the version, is how ui.pages is handled too.
    query = (params() if callable(params) else params).get("q", "")
    hits = search_index.search(query, limit=25) if query.strip() else []

    children = [
        Heading(PAGE_TITLE, level=1),
        Separator(class_name="my-4"),
        Form(
            on_submit=ctx.callback(run_search),
            class_name="flex gap-2 items-center",
            children=[
                Input(
                    name="q",
                    placeholder="Search every page…",
                    default_value=query,
                    class_name="flex-1",
                ),
                Button("Search", type="submit"),
            ],
        ),
        Text(
            (
                f"{len(hits)} of {search_index.indexed_pages()} pages match \u201c{query}\u201d."
                if query.strip()
                else "Search the text of every page, not only its title."
            ),
            class_name="text-sm text-muted-foreground mt-4",
        ),
    ]

    for hit in hits:
        children.append(
            Column(
                gap=1,
                class_name="border-b pb-4 pt-4",
                children=[
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            Link(hit.title, href=hit.route),
                            Badge(hit.group, variant="secondary"),
                        ],
                    ),
                    Markdown(
                        content=search_index.highlight(query, hit.snippet),
                        class_name="text-sm text-muted-foreground",
                    ),
                ],
            )
        )

    if query.strip() and not hits:
        # Markdown, with the identifier in backticks: raw `save_prop` in prose is an
        # emphasis hazard, and the underscore opened an _italic run_ that swallowed
        # the rest of the line. A Row of its own keeps it out of the count above.
        children.append(
            Row(
                class_name="mt-4",
                children=[
                    Markdown(
                        content=(
                            "Nothing matched. Try an API name such as `save_prop`, or a "
                            "word you remember reading in the documentation."
                        )
                    )
                ],
            )
        )

    content = Container(class_name="max-w-3xl mx-auto p-6", children=children)
    return docs_layout(ctx, content, PAGE_ROUTE)
