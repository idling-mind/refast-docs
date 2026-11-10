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
_MD_NOISE_RE = re.compile(r"[`*_>]")
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
    headings: list[str] = field(default_factory=list)
    body: str = ""
    snippet: str = ""


@dataclass(frozen=True)
class Hit:
    """A search result."""

    route: str
    title: str
    group: str
    snippet: str
    score: float

    def value_for(self, query: str) -> str:
        """The ``CommandItem`` value cmdk should score this hit against.

        ``Command`` exposes no ``shouldFilter``, so cmdk keeps filtering client
        side; embedding the query in the value is the documented way to keep
        server-chosen results from being filtered out of existence.
        """
        return f"{query} {self.title} {self.group}"

_pages: list[_Doc] = []
_index: dict[str, dict[int, float]] | None = None
_doc_norms: list[float] = []


def set_pages(entries: list[tuple[str, str, str, Callable[..., Any]]]) -> None:
    """Record the searchable pages.

    Args:
        entries: ``(title, route, group, render_function)`` for each page. The
            function is only used to find the module its prose lives in.
    """
    global _index, _doc_norms
    _index, _doc_norms = None, []
    _pages.clear()
    _pages.extend(_doc_from_module(route, title, group, func) for title, route, group, func in entries)


def _doc_from_module(route: str, title: str, group: str, func: Callable[..., Any]) -> _Doc:
    """Pull the prose out of the module that defines ``func``, without importing it again."""
    import sys

    module = sys.modules.get(func.__module__)
    doc = _Doc(route=route, title=title or route, group=group)
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
    global _index, _doc_norms
    index: dict[str, dict[int, float]] = {}
    norms = []
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
        norms.append(math.sqrt(len(counts)) or 1.0)
    _index, _doc_norms = index, norms


def search(query: str, limit: int = 12) -> list[Hit]:
    """Rank pages against ``query``. Returns [] when nothing scores."""
    if _index is None:
        _build()
    terms = _tokenize(query)
    if not terms or not _pages:
        return []

    total = len(_pages)
    scores: dict[int, float] = {}
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
            scores[n] = scores.get(n, 0.0) + idf * tf / _doc_norms[n]

    phrase = query.strip().lower()
    if len(phrase.split()) > 1:
        for n, doc in enumerate(_pages):
            if phrase in doc.title.lower():
                scores[n] = scores.get(n, 0.0) + 20.0

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:limit]
    return [
        Hit(_pages[n].route, _pages[n].title, _pages[n].group, _snippet(_pages[n], terms), s)
        for n, s in ranked
    ]


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
    return re.sub(r"[`*_>#|]+", " ", re.sub(r"\s+", " ", text)).strip()


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


def routes() -> list[str]:
    """Every route in the index, for asserting it matches the navigation."""
    return [doc.route for doc in _pages]


def coverage() -> list[tuple[str, int]]:
    """``(route, characters of prose)`` per page, to spot pages that went unindexed."""
    return [(doc.route, len(doc.body)) for doc in _pages]
