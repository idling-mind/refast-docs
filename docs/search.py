"""Full-text search over the documentation pages.

The palette in ``docs/app.py`` used to offer the sidebar titles and nothing else,
which meant a reader looking for "save_prop" had to already know which page
documented it. This module builds an inverted index over the prose each page
actually renders, so the body text is searchable.

Pages register themselves with :func:`set_pages` — passing callables rather than
importing ``docs.app`` keeps the dependency one-way, since ``app`` imports this
module. The index itself is built on first use, not at import time: extracting
strings from ~110 modules costs a few hundred milliseconds, and doing it during
``import docs.app`` would slow every test and every worker start.
"""

from __future__ import annotations

import ast
import math
import re
from dataclasses import dataclass, field
from typing import Any, Callable

# Terms too common in prose to be worth an entry in the index.
_STOPWORDS = frozenset(
    """
    a about again all also an and any are as at be because been before being
    below between both but by can could did do does doing down during each few
    for from further had has have having he her here hers him his how i if in
    into is it its itself just me more most my no nor not now of off on once
    only or other our ours out over own same she should so some such than that
    the their theirs them then there these they this those through to too under
    until very was we were what when where which while who whom why will with
    would you your yours
    """.split()
)

_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.+\-/]*")
# Markdown emphasis and raw-markup noise, deliberately without `_`: in this
# corpus underscores belong to API names -- save_prop, store_as, ctx.file_store --
# and splitting them turns one searchable identifier into two common English
# words, which is how a search for save_prop ends up matching 25 pages.
_MD_NOISE_RE = re.compile(r"[`*>]")
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)

# A string literal shorter than this is a label or an argument, not prose.
_MIN_BODY_CHARS = 120

TITLE_WEIGHT = 8.0
HEADING_WEIGHT = 4.0
BODY_WEIGHT = 1.0


@dataclass
class _Doc:
    """One searchable page."""

    route: str
    title: str
    group: str
    nav_label: str = ""
    headings: list[str] = field(default_factory=list)
    body: str = ""
    snippet: str = ""
    title_terms: frozenset[str] = frozenset()
    heading_terms: frozenset[str] = frozenset()
    terms: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Hit:
    """A search result."""

    route: str
    title: str
    group: str
    snippet: str
    score: float


_pages: list[_Doc] = []
_index: dict[str, dict[int, float]] | None = None


def set_pages(entries: list[tuple[str, str, str, Callable[..., Any]]]) -> None:
    """Record the searchable pages.

    Args:
        entries: ``(title, route, group, render_function)`` for each page. The
            function is only used to find the module its prose lives in.
    """
    global _index
    _index = None
    _pages.clear()
    _pages.extend(_doc_from_module(route, title, group, func) for title, route, group, func in entries)


def _doc_from_module(route: str, title: str, group: str, func: Callable[..., Any]) -> _Doc:
    """Pull the prose out of the module that defines ``func``, without importing it again."""
    import sys

    module = sys.modules.get(func.__module__)
    doc = _Doc(route=route, title=title or route, group=group, nav_label=title or "")
    if module is None or not getattr(module, "__file__", None):
        return doc

    tree = ast.parse(_source(module.__file__), filename=str(module.__file__))
    chunks: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            text = node.value
            if len(text) >= _MIN_BODY_CHARS:
                chunks.append(text)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "PAGE_TITLE" and isinstance(node.value, ast.Constant):
                    doc.title = str(node.value.value)
    doc.body = "\n".join(chunks)
    doc.snippet = _plain(doc.body)
    doc.headings = _HEADING_RE.findall(doc.body)
    doc.title_terms = frozenset(_tokenize(doc.title))
    doc.heading_terms = frozenset(t for h in doc.headings for t in _tokenize(h))
    if not doc.title or doc.title == route:
        doc.title = title or route
    return doc


def _source(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def _tokenize(text: str) -> list[str]:
    """Lowercase word and identifier tokens, minus stopwords."""
    cleaned = _LINK_RE.sub(r"\1", _MD_NOISE_RE.sub(" ", text))
    return [t for t in (m.group(0).lower() for m in _TOKEN_RE.finditer(cleaned)) if t not in _STOPWORDS and len(t) > 1]


def _build() -> None:
    """Invert the pages into ``term -> {doc number: weighted frequency}``."""
    global _index
    index: dict[str, dict[int, float]] = {}
    weights: list[dict[str, float]] = []
    for n, doc in enumerate(_pages):
        counts: dict[str, float] = {}
        for term in _tokenize(doc.title):
            counts[term] = counts.get(term, 0.0) + TITLE_WEIGHT
        for heading in doc.headings:
            for term in _tokenize(heading):
                counts[term] = counts.get(term, 0.0) + HEADING_WEIGHT
        for term in _tokenize(doc.body):
            counts[term] = counts.get(term, 0.0) + BODY_WEIGHT
        for term, freq in counts.items():
            index.setdefault(term, {})[n] = 1.0 + math.log(freq)
        weights.append(counts)
    _index = index

    total = len(_pages)
    for doc, counts in zip(_pages, weights):
        doc.terms = sorted(
            counts,
            key=lambda t: (
                -(1.0 + math.log(counts[t])) * math.log(1.0 + total / len(index[t])),
                t,
            ),
        )[:12]


def search(query: str, limit: int = 12) -> list[Hit]:
    """Rank pages against ``query``. Returns [] when nothing scores.

    Frequency alone ranks badly: on a docs site the word "styling" appears in a
    dozen pages, and a short page that mentions it once outscored the page called
    Styling. So position beats volume -- a term in the title is worth far more
    than any number of mentions in the body -- and the whole phrase being a title
    is worth more still.
    """
    if _index is None:
        _build()
    terms = _tokenize(query)
    if not terms or not _pages:
        return []

    total = len(_pages)
    scores: dict[int, float] = {}
    matched: dict[int, set[str]] = {}
    for term in dict.fromkeys(terms):
        postings = _index.get(term, {})
        # Prefix pass: a stem like "pagin" should still find "pagination".
        if not postings:
            postings = {
                n: s for t, p in _index.items() if t.startswith(term) for n, s in p.items()
            }
        if not postings:
            continue
        idf = math.log(1.0 + total / len(postings))
        for n, tf in postings.items():
            scores[n] = scores.get(n, 0.0) + idf * tf
            matched.setdefault(n, set()).add(term)

    for n, found in matched.items():
        doc = _pages[n]
        if any(_in_terms(t, doc.title_terms) for t in found):
            scores[n] += 14.0 * sum(1 for t in found if _in_terms(t, doc.title_terms))
        elif any(_in_terms(t, doc.heading_terms) for t in found):
            scores[n] += 5.0

    phrase = " ".join(terms)
    if " " in phrase:
        for n, doc in enumerate(_pages):
            title = " ".join(_tokenize(doc.title))
            if phrase in title:
                scores[n] += 25.0
            elif any(phrase in " ".join(_tokenize(h)) for h in doc.headings):
                scores[n] += 6.0

    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], _pages[kv[0]].title.lower()))[:limit]
    return [
        Hit(_pages[n].route, _pages[n].title, _pages[n].group, _snippet(_pages[n], terms), s)
        for n, s in ranked
    ]


def _in_terms(term: str, terms: frozenset[str]) -> bool:
    """Whether ``term`` names one of ``terms``, allowing for a typed stem.

    The postings already fall back to a prefix match so "pagin" finds Pagination;
    without the same courtesy in the title bonus, the page about pagination and a
    page that merely mentions it arrive at an identical score.
    """
    return term in terms or any(t.startswith(term) or term.startswith(t) for t in terms)


def highlight(query: str, text: str) -> str:
    """Bold the words from ``query`` that ``text`` contains, for result listings.

    A reader who got here by searching needs to see *why* a page matched --
    otherwise a list of titles says nothing more than the sidebar does.
    """
    terms = [t for t in dict.fromkeys(_tokenize(query)) if len(t) > 2]
    if not terms:
        return text
    pattern = re.compile(r"\b(" + "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True)) + r")\w*", re.IGNORECASE)
    return pattern.sub(lambda m: f"**{m.group(0)}**", text)


_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_TAG_RE = re.compile(r"</?[A-Za-z][^>]*>")


def _plain(body: str) -> str:
    """Body text as a reader would see it, for building snippets.

    Code samples are indexed -- searching for ``save_prop`` should find the page
    that shows it -- but a snippet that opens with
    ``python from refast.components import`` is useless as a preview.
    """
    text = _FENCE_RE.sub(" ", body)
    text = _LINK_RE.sub(r"\1", text)
    text = _TAG_RE.sub(" ", text)
    # Backticks stay: a snippet that loses them hands `save_prop` to the markdown
    # renderer as bare text, where the underscore opens emphasis and the rest of
    # the line collapses.
    return re.sub(r"[*<>#|]+", " ", re.sub(r"\s+", " ", text)).strip()


def _snippet(doc: _Doc, terms: list[str], width: int = 150) -> str:
    """A sentence-sized window around the first match in the body."""
    text = doc.snippet
    lowered = text.lower()
    for term in terms:
        at = lowered.find(term)
        if at >= 0:
            start = max(0, at - 40)
            window = text[start : start + width]
            return ("…" if start else "") + window.rsplit(" ", 1)[0] + ("…" if start + width < len(text) else "")
    return text[:width].rsplit(" ", 1)[0] + ("…" if len(text) > width else "")


def indexed_pages() -> int:
    """How many pages the index covers (0 before the first search)."""
    return len(_pages)




def keywords(route: str, limit: int = 8) -> str:
    """The text cmdk should score ``route`` against, for the ⌘K palette.

    cmdk filters client-side over each item's registered value and refast's
    Command wrapper forwards neither ``shouldFilter`` nor extra props, so the
    words have to reach the browser for page bodies to be searchable at all.
    Driving the ranking from the server instead -- refreshing per keystroke --
    lost letters and then matched nothing, because a controlled input echoes one
    keystroke behind while cmdk scores the live string against that stale echo.

    ``command-score`` weighs *where* in the value a match falls, in roughly the
    first ten characters, and knows nothing about how rare the word is. Ordering
    the blob by tf-idf instead of raw frequency is what makes position work for
    us: the words that identify a page lead it, so the page called Styling beats
    the nine pages that merely mention styling. That ordering was the complaint.
    """
    if _index is None:
        _build()
    doc = next((d for d in _pages if d.route == route), None)
    if doc is None:
        return ""
    # The row shows the nav label, so the label leads the blob: the palette's ranker
    # reads position 0 as "this page is called that". PAGE_TITLE follows, because it
    # is the heading the page itself opens with and the two are not always identical.
    return " ".join(dict.fromkeys([doc.nav_label, doc.title, doc.group, *doc.terms[:limit]]))


def routes() -> list[str]:
    """Every route in the index, for asserting it matches the navigation."""
    return [doc.route for doc in _pages]


def coverage() -> list[tuple[str, int]]:
    """``(route, characters of prose)`` per page, to spot pages that went unindexed."""
    return [(doc.route, len(doc.body)) for doc in _pages]
