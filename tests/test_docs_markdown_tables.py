"""Keep Markdown tables well-formed.

``Markdown`` renders with ``remark-gfm``, which splits a table row on **every**
``|`` -- including pipes inside an inline code span. A type union written the
natural Python way therefore invents columns::

    | `icon` | `str | None` | `None` | ...     <- 6 cells for a 4 column table

The escape ``\\|`` is required (`` `str \\| None` ``), and since ``"\\|"`` is an
invalid escape sequence in a *normal* Python string (SyntaxWarning / ruff W605),
table content must live in raw strings -- ruff guards that half, this test
guards the shape of every table in the site.
"""

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = ROOT / "docs"

ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
SEPARATOR_RE = re.compile(r"^\s*\|(?:\s*:?-{2,}:?\s*\|)+\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")
CODE_SPAN_RE = re.compile(r"`+[^`]*`+")
UNESCAPED_PIPE_RE = re.compile(r"(?<!\\)\|")


def _unfenced(lines: list[str], first_lineno: int = 1) -> list[tuple[int, str]]:
    """(lineno, text) for lines outside fenced code blocks."""
    kept: list[tuple[int, str]] = []
    in_fence = False
    for index, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept.append((first_lineno + index, line))
    return kept


def _doc_lines() -> list[tuple[Path, list[tuple[int, str]]]]:
    """Every docs module's string constants and every markdown file, fence-free."""
    collected: list[tuple[Path, list[tuple[int, str]]]] = []
    for path in sorted(p for p in DOCS_ROOT.rglob("*") if "__pycache__" not in p.parts):
        if path.suffix == ".md":
            collected.append((path, _unfenced(path.read_text(encoding="utf-8").splitlines())))
        elif path.suffix == ".py":
            lines: list[tuple[int, str]] = []
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    lines.extend(_unfenced(node.value.splitlines(), node.lineno))
            collected.append((path, lines))
    return collected


def _tables(lines: list[tuple[int, str]]) -> list[list[tuple[int, str]]]:
    """Group runs of consecutive table rows; a table is >= 2 lines."""
    tables: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] = []
    for entry in [*lines, (0, "")]:
        if ROW_RE.match(entry[1]):
            current.append(entry)
            continue
        if len(current) > 1:
            tables.append(current)
        current = []
    return tables


def _cell_count(row: str) -> int:
    return len(CELL_SPLIT_RE.split(row.strip()))


def _check_tables(lines: list[tuple[int, str]], where: str) -> list[str]:
    """Column-count problems for every table in these lines."""
    problems: list[str] = []
    for table in _tables(lines):
        header_row = table[1][1] if SEPARATOR_RE.match(table[1][1]) else table[0][1]
        columns = _cell_count(header_row)
        for lineno, row in table:
            if _cell_count(row) != columns:
                problems.append(
                    f"{where}:{lineno}: {_cell_count(row)} cells, header has {columns}: "
                    f"{row.strip()[:70]}"
                )
    return problems


def _span_problems(lines: list[tuple[int, str]], where: str) -> list[str]:
    """Table rows whose code spans contain a pipe that was not escaped."""
    problems: list[str] = []
    for lineno, row in lines:
        if not ROW_RE.match(row):
            continue
        for span in CODE_SPAN_RE.finditer(row):
            if UNESCAPED_PIPE_RE.search(span.group()):
                problems.append(f"{where}:{lineno}: pipe inside {span.group().strip()}")
    return problems


def test_no_unescaped_pipes_inside_code_spans() -> None:
    bad: list[str] = []
    for path, lines in _doc_lines():
        bad.extend(_span_problems(lines, str(path.relative_to(ROOT))))
    assert not bad, (
        "escape pipes inside inline code in table cells as \\|:\n" + "\n".join(sorted(set(bad)))
    )


def test_table_rows_match_their_header() -> None:
    bad: list[str] = []
    for path, lines in _doc_lines():
        bad.extend(_check_tables(lines, str(path.relative_to(ROOT))))
    assert not bad, "malformed tables:\n" + "\n".join(sorted(set(bad)))


def test_generated_props_tables_are_well_formed() -> None:
    """The generator in docs/pages/components/props_table.py must emit valid tables."""
    import refast.components

    from docs.pages.components.props_table import props_table
    from refast.components.base import Component

    components = [
        obj
        for obj in vars(refast.components).values()
        if isinstance(obj, type) and issubclass(obj, Component) and obj is not Component
    ]
    assert len(components) > 100, f"only found {len(components)} components to generate for"

    bad: list[str] = []
    for component in components:
        try:
            table = props_table(component)
        except Exception:  # noqa: BLE001 - exotic signatures are not this test's concern
            continue
        lines = [(index, line) for index, line in enumerate(table.splitlines(), start=1)]
        where = f"props_table({component.__name__})"
        bad.extend(_check_tables(lines, where))
        bad.extend(_span_problems(lines, where))
    assert not bad, "generated props tables are malformed:\n" + "\n".join(sorted(set(bad))[:40])
