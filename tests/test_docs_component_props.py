"""Catch docs examples that pass props the installed components do not accept.

Refast components declare their props as explicit ``__init__`` keyword
arguments and inherit only ``id``/``class_name``/``style``/``parent_style``/
``extra_props`` from the base class -- there is no ``**kwargs`` sink. A prop
that was renamed or removed upstream therefore raises ``TypeError`` while the
page tree is being built, which (see ``test_docs_pages_render.py``) a plain HTTP
GET would not even notice.

Rather than importing 130+ page modules, this test parses each file under
``docs/`` with ``ast`` and resolves every ``SomeComponent(...)`` call against the
*installed* refast packages with ``inspect.signature`` -- a fast, side-effect-free
contract check between the documentation and the library it documents.
"""

import ast
import importlib
import inspect
import pkgutil
from pathlib import Path

from refast.components.base import Component

DOCS_ROOT = Path(__file__).resolve().parent.parent / "docs"

COMPONENT_PACKAGES = (
    "refast.components",
    "refast_grid",
    "refast_echarts",
    "refast_vtk_js",
)

# The abstract base is referenced in docs prose but takes no props of its own.
SKIP_CLASSES = {"Component"}


def _doc_files() -> list[Path]:
    return sorted(p for p in DOCS_ROOT.rglob("*.py") if "__pycache__" not in p.parts)


def _component_registry() -> dict[str, type[Component]]:
    """Map every importable Component class name to its class object."""
    registry: dict[str, type[Component]] = {}
    for package_name in COMPONENT_PACKAGES:
        try:
            package = importlib.import_module(package_name)
        except ImportError:  # an optional extension is not installed
            continue
        modules = [package]
        for info in pkgutil.walk_packages(getattr(package, "__path__", []), f"{package_name}."):
            if info.name.rsplit(".", 1)[-1].startswith("_"):
                continue
            try:
                modules.append(importlib.import_module(info.name))
            except Exception:  # pragma: no cover - extensions may need browser assets
                continue
        for module in modules:
            for name in dir(module):
                obj = getattr(module, name, None)
                if isinstance(obj, type) and issubclass(obj, Component):
                    registry.setdefault(obj.__name__, obj)
    return registry


REGISTRY = _component_registry()


def _accepted_keywords(component: type) -> set[str] | None:
    """Keyword names the class accepts, or None if it swallows **kwargs."""
    try:
        signature = inspect.signature(component)
    except (TypeError, ValueError):  # pragma: no cover - exotic callables
        return None
    keywords: set[str] = set()
    for name, param in signature.parameters.items():
        if name == "self":
            continue
        if param.kind is inspect.Parameter.VAR_KEYWORD:
            return None
        keywords.add(name)
    return keywords


def check_file(path: Path) -> list[str]:
    """Return human-readable prop violations found in one docs module."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    problems: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        else:
            continue
        component = REGISTRY.get(name)
        if component is None or name in SKIP_CLASSES:
            continue
        accepted = _accepted_keywords(component)
        if accepted is None:
            continue
        for keyword in node.keywords:
            if keyword.arg is None:  # ** unpacking, not checkable statically
                continue
            if keyword.arg not in accepted:
                problems.append(
                    f"{path.relative_to(DOCS_ROOT.parent)}:{node.lineno}: "
                    f"{name}() got an unexpected keyword '{keyword.arg}' "
                    f"(accepts: {', '.join(sorted(accepted))})"
                )
    return problems


def test_component_registry_was_resolved() -> None:
    """Guard the guard: the imports above must actually find components."""
    assert len(REGISTRY) > 150, f"only resolved {len(REGISTRY)} component classes"


def test_docs_use_only_supported_props() -> None:
    problems = [problem for path in _doc_files() for problem in check_file(path)]
    assert not problems, "docs pass props that components do not accept:\n" + "\n".join(problems)
