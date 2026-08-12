"""Common layout helper for component documentation pages."""

from typing import Any
from refast import Context
from refast.components import (
    Container,
    Heading,
    Markdown,
    Separator,
)


def render_doc_page(
    ctx: Context,
    title: str,
    route: str,
    intro: str | None = None,
    playground: Any = None,
    reference: str | None = None,
    sections: list | None = None,
    children: list | None = None,
    max_width: str = "max-w-4xl",
):
    """Render a standardized component documentation page.

    Args:
        ctx: The request Context instance.
        title: Page heading title.
        route: Current route string passed to docs_layout.
        intro: Optional intro Markdown text.
        playground: Optional playground component tree or callable `playground(ctx)`.
        reference: Optional reference/props Markdown text.
        sections: Optional additional section components.
        children: Optional full children override for Container.
        max_width: Tailwind max-width class (defaults to "max-w-4xl").
    """
    from docs.app import docs_layout

    if children is None:
        page_children = [
            Heading(title, level=1),
            Separator(class_name="my-4"),
        ]
        if intro:
            page_children.append(Markdown(content=intro))
        if playground is not None:
            if callable(playground):
                page_children.append(playground(ctx))
            else:
                page_children.append(playground)
        if sections:
            page_children.extend(sections)
        if reference:
            page_children.append(Markdown(content=reference))
    else:
        page_children = children

    content = Container(
        class_name=f"{max_width} mx-auto p-6",
        children=page_children,
    )
    return docs_layout(ctx, content, route)
