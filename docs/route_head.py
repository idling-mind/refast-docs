"""Route-specific ``<head>`` tags, patched into refast's shell per request.

Why this module exists
----------------------
refast renders one static shell for every route (`docs/app.py` calls the consequence
out at the `canonical` tag, and `tests/test_docs_shell.py` pins it): the document served
for `/docs/advanced/sessions` is the document served for `/`, so its title says "Refast
Docs", its description says what the *site* is, and its canonical URL and `og:url` name
the root. A tab, a link preview, a search index and an LLM fetching a page URL all get
the same identity for a hundred different pages, and `canonical` pointing at the root
tells a crawler that the page it just read is a duplicate of the home page.

The fix belongs in the framework — `RefastApp(render_shell_for=path)` or a
`head_tags=` argument on `@ui.page`, item 1 of "Discovery & SEO" in `docs/TODO.md` —
but a shell is text, so this module rewrites the one refast emits. It changes only the
tags that describe *which page this is*: title, description, `og:*`, `canonical`, a
Markdown `alternate`, and JSON-LD for the engines and answer engines that read schema
rather than prose. The body still hydrates exactly as it did.

Where the values come from
--------------------------
From :mod:`docs.markdown_export`, which already renders each page and knows its title,
section and first sentence. That is deliberate: the head, the `.md` mirror and the
`/llms.txt` row describing a page all quote the same sentence, so they cannot disagree.
"""

from __future__ import annotations

import json
import re
from html import escape

from . import markdown_export

#: The site name, kept after an em-dash so a tab bar says which site, not only which page.
SITE_TITLE = "Refast Docs"

_TITLE_RE = re.compile(r"<title>.*?</title>", re.DOTALL)
_CANONICAL_RE = re.compile(r'<link rel="canonical" href="[^"]*">')
_DESCRIPTION_RE = re.compile(r'<meta name="description" content="[^"]*">')


def page_title(route: str) -> str:
    """What a tab for ``route`` should say, or '' when no page claims the route."""
    page = markdown_export.find(route)
    return f"{page.title} — {SITE_TITLE}" if page else ""


def head_tags(route: str, *, site_url: str) -> str:
    """The tags that describe ``route`` alone, for appending before ``</head>``.

    Only additions go here; the tags the shell already carries are rewritten in place
    by :func:`patch_shell` so that a page never has two descriptions or two canonicals.
    """
    page = markdown_export.find(route)
    if page is None:
        return ""
    url = f"{site_url}{route}"
    markdown_url = f"{site_url}{markdown_export.markdown_href(route)}"
    crumbs = [part for part in (page.section, page.title) if part]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "@id": url,
                "headline": page.title,
                "description": page.plain_summary,
                "url": url,
                "inLanguage": "en",
                "isPartOf": {"@type": "WebSite", "name": SITE_TITLE, "url": f"{site_url}/"},
                "codingSystem": "Python",
                "about": crumbs,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
                    for i, name in enumerate(crumbs)
                ],
            },
        ],
    }
    return "\n    ".join(
        [
            # A client that does not execute JavaScript can now find the text version
            # from the page itself, which is the missing half of <route>.md existing.
            f'<link rel="alternate" type="text/markdown" href="{escape(markdown_url, quote=True)}">',
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=True)}</script>',
        ]
    )


def patch_shell(html: str, *, route: str, site_url: str, default_description: str = "") -> str:
    """Rewrite the shell's identity tags to describe ``route``."""
    page = markdown_export.find(route)
    if page is None or "</head>" not in html:
        return html

    url = f"{site_url}{route}"
    title = escape(f"{page.title} — {SITE_TITLE}", quote=True)
    description = escape(page.plain_summary or default_description, quote=True)

    html = _TITLE_RE.sub(f"<title>{title}</title>", html, count=1)
    html = _CANONICAL_RE.sub(f'<link rel="canonical" href="{escape(url, quote=True)}">', html, count=1)
    html = _DESCRIPTION_RE.sub(f'<meta name="description" content="{description}">', html, count=1)
    for prop, value in (
        ("og:title", title),
        ("og:description", description),
        ("og:url", escape(url, quote=True)),
        ("og:type", "article"),
    ):
        html = _meta_prop(html, prop, value)

    extra = head_tags(route, site_url=site_url)
    return html.replace("</head>", f"{extra}\n</head>", 1) if extra else html


def _meta_prop(html: str, prop: str, content: str) -> str:
    """Replace one ``og:*`` tag's content, keeping its position in the head.

    The tag has to be rewritten where it is rather than appended: a second
    ``og:title`` is a tie between two values that renderers resolve differently.
    """
    pattern = re.compile(rf'<meta property="{re.escape(prop)}" content="[^"]*">')
    tag = f'<meta property="{prop}" content="{content}">'
    return pattern.sub(tag, html, count=1) if pattern.search(html) else html + f"\n    {tag}"
