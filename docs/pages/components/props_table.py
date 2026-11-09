"""Generate Markdown props tables from live component signatures.

Props tables used to be typed by hand, which meant every refast release left the
documentation quietly wrong: a renamed prop kept rendering as a row, defaults
drifted, and a type union written as ``str | None`` broke the table because
remark-gfm splits cells on unescaped pipes (see ``tests/test_docs_markdown_tables.py``).

:func:`props_table` renders the table from the component that is actually
installed -- its ``__init__`` signature for names, types and defaults, and its
docstring ``Args:`` block for descriptions -- so the table cannot disagree with
the library.
"""

import inspect
import re
import types
import typing
from collections.abc import Iterable
from typing import Any

# A pipe inside an inline code span has to reach the renderer escaped.
PIPE = "\\|"

#: props inherited from Component and documented once on /docs/components/base
BASE_PROPS = ("id", "class_name", "style", "parent_style", "extra_props")

_ARGS_HEADER = re.compile(r"^\s*(Args|Arguments|Parameters)\s*:\s*$")
_SECTION_END = re.compile(
    r"^(Returns|Yields|Raises|Attributes|Example|Examples|Note|Notes|Todo)\s*:"
)
_ARG_LINE = re.compile(r"^([a-z_][a-z0-9_]*)\s*(\([^)]*\))?\s*:\s*(.*)$")


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def docstring_args(component: type) -> dict[str, str]:
    """Extract ``{name: description}`` from a class docstring's ``Args:`` block."""
    doc = inspect.getdoc(component) or ""
    lines = doc.splitlines()
    start = None
    base_indent = 0
    for index, line in enumerate(lines):
        if _ARGS_HEADER.match(line):
            start = index
            base_indent = _indent(line)
            break
    if start is None:
        return {}

    args: dict[str, str] = {}
    current: str | None = None
    for line in lines[start + 1 :]:
        if not line.strip():
            continue
        if _indent(line) <= base_indent or _SECTION_END.match(line.strip()):
            break
        match = _ARG_LINE.match(line.strip())
        if match:
            current = match.group(1)
            args[current] = match.group(3).strip()
        elif current:
            args[current] = f"{args[current]} {line.strip()}".strip()
    return args


def _literal_value(value: Any) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, (bytes,)):
        return repr(value.decode(errors="replace"))
    return repr(value)


def _from_string(annotation: str) -> str:
    """Best-effort label for a stringized annotation (PEP 563 modules)."""
    text = annotation.strip().strip('"').strip("'")
    text = re.sub(r"\btyping\.", "", text)
    literal = re.match(r"^Literal\[(.*)\]$", text)
    if literal:
        members = [part.strip().replace("'", '"') for part in literal.group(1).split(",")]
        return f" {PIPE} ".join(part for part in members if part)
    return text


def type_label(annotation: Any) -> str:
    """Render a type annotation as one escaped-pipe-safe code span."""
    if annotation is inspect.Parameter.empty:
        return "Any"
    if isinstance(annotation, str):
        return _from_string(annotation)

    origin = typing.get_origin(annotation)
    members = typing.get_args(annotation)

    if origin is typing.Literal:
        return f" {PIPE} ".join(_literal_value(member) for member in members)
    if origin is typing.Union or origin is getattr(types, "UnionType", None):
        return f" {PIPE} ".join(type_label(member) for member in members)
    if annotation is None or annotation is type(None):
        return "None"
    if isinstance(annotation, typing.ForwardRef):
        return annotation.__forward_arg__
    if origin is not None:
        name = getattr(origin, "__name__", None) or str(origin).rsplit(".", 1)[-1]
        inner = ", ".join(type_label(member) for member in members)
        return f"{name}[{inner}]" if inner else name
    if isinstance(annotation, type):
        return annotation.__name__
    return str(annotation).replace("typing.", "")


def default_label(value: Any) -> str:
    """Render a parameter default for the table's Default column."""
    if value is inspect.Parameter.empty:
        return "*(positional)*"
    if isinstance(value, str):
        return f"`{_literal_value(value)}`"
    if value is None or isinstance(value, (bool, int, float)):
        return f"`{value}`"
    return f"`{_literal_value(value)}`"


def _cell(text: str) -> str:
    """Escape bare pipes so an override label cannot split the row."""
    return text if PIPE in text else text.replace("|", PIPE)


def props_table(
    component: type,
    *,
    exclude: Iterable[str] = BASE_PROPS,
    include_base: bool = False,
    type_overrides: dict[str, str] | None = None,
    notes: str = "",
) -> str:
    """Build a ``## Props`` Markdown table for one component class.

    Args:
        component: the component class to introspect.
        exclude: parameter names to leave out; defaults to the shared
            :class:`~refast.components.base.Component` props.
        include_base: append the inherited props, for pages that want the
            complete signature in one table.
        type_overrides: per-prop labels to use instead of the introspected
            type, for unions that are technically correct but unreadable.
        notes: optional prose added under the table.

    Returns:
        Markdown with a header row and one row per accepted keyword.
    """
    skip = set() if include_base else set(exclude)
    overrides = type_overrides or {}
    signature = inspect.signature(component)
    documented = docstring_args(component)

    rows: list[str] = []
    for name, parameter in signature.parameters.items():
        if name == "self" or name in skip:
            continue
        if parameter.kind in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
            continue
        description = documented.get(name, "")
        if "|" in description:
            description = description.replace("|", PIPE)
        label = _cell(overrides.get(name) or type_label(parameter.annotation))
        rows.append(
            f"| `{name}` | `{label}` | "
            f"{default_label(parameter.default)} | {description} |"
        )

    header = [
        "## Props",
        "",
        "| Prop | Type | Default | Description |",
        "|------|------|---------|-------------|",
    ]
    body = header + rows
    if notes:
        body.append("")
        body.append(notes.strip())
    return "\n".join(body)
