"""Auto-discovery and group registry for component documentation pages."""

import importlib
import pkgutil
from pathlib import Path
from typing import Any

# Canonical group ordering and icons
GROUP_METADATA: dict[str, dict[str, Any]] = {
    "Foundations": {"icon": "box", "order": 1},
    "Layout": {"icon": "layout", "order": 2},
    "Typography": {"icon": "type", "order": 3},
    "Buttons & Actions": {"icon": "mouse-pointer-click", "order": 4},
    "Form Inputs": {"icon": "text-cursor-input", "order": 5},
    "Cards & Containers": {"icon": "credit-card", "order": 6},
    "Data Display": {"icon": "table", "order": 7},
    "Navigation": {"icon": "compass", "order": 8},
    "Feedback & Overlay": {"icon": "message-square", "order": 9},
    "Charts": {"icon": "bar-chart-3", "order": 10},
    "Utility": {"icon": "wrench", "order": 11},
}


def discover_component_groups() -> list[dict[str, Any]]:
    """Scan `docs/pages/components/` for component modules and assemble NAV_SECTIONS groups.

    Returns:
        List of section group dicts:
        [
            {
                "label": "Foundations",
                "icon": "box",
                "pages": [("Base", "/docs/components/base", "box", render_fn), ...],
            },
            ...
        ]
    """
    import docs.pages.components as components_pkg

    pkg_dir = Path(components_pkg.__file__).parent
    grouped_pages: dict[str, list[dict[str, Any]]] = {}

    for path in pkg_dir.rglob("*.py"):
        if path.name.startswith("_") or path.name in ("playground.py", "common.py", "registry.py"):
            continue

        rel_path = path.relative_to(pkg_dir.parent.parent.parent)
        mod_name = str(rel_path.with_suffix("")).replace("\\", ".").replace("/", ".")

        try:
            mod = importlib.import_module(mod_name)
        except Exception as err:
            print(f"Warning: failed to import component module {mod_name}: {err}")
            continue

        render_fn = getattr(mod, "render", None)
        if not render_fn:
            continue

        page_meta = getattr(mod, "PAGE_METADATA", None)
        if page_meta:
            title = page_meta.get("title")
            route = page_meta.get("route")
            icon = page_meta.get("icon", "box")
            group = page_meta.get("group", "Utility")
            order = page_meta.get("order", 99)
        else:
            title = getattr(mod, "PAGE_TITLE", path.stem.replace("_", " ").title())
            route = getattr(mod, "PAGE_ROUTE", f"/docs/components/{path.stem.replace('_', '-')}")
            icon = "box"
            group = "Utility"
            order = 99

        if not title or not route:
            continue

        item = {
            "title": title,
            "route": route,
            "icon": icon,
            "render": render_fn,
            "order": order,
        }
        grouped_pages.setdefault(group, []).append(item)

    # Sort groups according to GROUP_METADATA order
    def group_sort_key(group_name: str) -> tuple[int, str]:
        meta = GROUP_METADATA.get(group_name, {})
        return (meta.get("order", 99), group_name)

    sorted_group_names = sorted(grouped_pages.keys(), key=group_sort_key)

    result_groups = []
    for gname in sorted_group_names:
        items = grouped_pages[gname]
        # Sort items inside group by order then title
        items.sort(key=lambda x: (x["order"], x["title"]))

        gicon = GROUP_METADATA.get(gname, {}).get("icon", "box")
        pages_tuples = [(it["title"], it["route"], it["icon"], it["render"]) for it in items]

        result_groups.append(
            {
                "label": gname,
                "icon": gicon,
                "pages": pages_tuples,
            }
        )

    return result_groups
