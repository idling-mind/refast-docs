"""Spreadsheet & Grid Extension — /docs/extensions/grid."""

from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Icon,
    Markdown,
    Row,
    Separator,
    Text,
)

try:
    from refast_grid import RefastGrid
    HAS_GRID = True
except ImportError:
    HAS_GRID = False

PAGE_TITLE = "Spreadsheet & Grid Extension"
PAGE_ROUTE = "/docs/extensions/grid"


def render(ctx):
    """Render the refast_grid documentation page."""
    from docs.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6 space-y-8",
        children=[
            Column(
                gap=2,
                children=[
                    Row(
                        gap=2,
                        align="center",
                        children=[
                            Badge("refast_grid", variant="secondary"),
                            Badge("Data & Tables", variant="outline"),
                            Badge("ReactGrid", variant="outline"),
                        ],
                    ),
                    Heading(PAGE_TITLE, level=1),
                    Text(
                        "Excel-like spreadsheet and data grid component for Refast based on Silevis ReactGrid. Supports cell editing, sticky headers/totals, virtualized scrolling, and 15+ cell types.",
                        class_name="text-lg text-muted-foreground",
                    ),
                ],
            ),
            Separator(),
            # Quick Installation Card
            Card(
                class_name="border-primary/20 bg-muted/20",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                gap=2,
                                align="center",
                                children=[
                                    Icon("download", class_name="text-primary"),
                                    CardTitle("Installation", class_name="text-base"),
                                ],
                            ),
                            CardDescription("Install the extension package from PyPI:"),
                        ],
                    ),
                    CardContent(
                        class_name="pt-0",
                        children=[
                            Container(
                                class_name="bg-card rounded-md border p-3 font-mono text-sm",
                                children=[Text("pip install refast_grid")],
                            ),
                        ],
                    ),
                ],
            ),
            # Live interactive preview card
            _live_preview_card(ctx),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


def _live_preview_card(ctx):
    """Render a live interactive RefastGrid preview card embedded in documentation."""
    async def open_demo(c):
        await c.load("/examples/grid")

    async def on_preview_cells_changed(c):
        changes = c.event_data.get("changes", [])
        rows = list(c.state.get("preview_grid_rows", []))
        if not rows:
            return

        cols = ["name", "role", "status", "active"]
        col_to_idx = {col: i for i, col in enumerate(cols)}
        rows_by_id = {r["row_id"]: r for r in rows}

        for ch in changes:
            row_id = ch.get("rowId")
            col_id = ch.get("columnId")
            new_cell = ch.get("newCell", {})

            if row_id in rows_by_id and col_id in col_to_idx:
                target_row = rows_by_id[row_id]
                idx = col_to_idx[col_id]
                cells = list(target_row.get("cells", []))
                if idx < len(cells):
                    cells[idx] = {**cells[idx], **new_cell}
                    target_row["cells"] = cells

        c.state["preview_grid_rows"] = rows
        await c.update_props("doc-live-grid-preview", {"rows": rows})

        for ch in changes:
            val = ch.get("newCell", {}).get("value") or ch.get("newCell", {}).get("text")
            if val is None and "checked" in ch.get("newCell", {}):
                val = ch.get("newCell", {}).get("checked")
            await c.show_toast(f"Cell updated: {val}", variant="default")

    preview_cols = [
        {"column_id": "name", "width": 160, "resizable": True},
        {"column_id": "role", "width": 140, "resizable": True},
        {"column_id": "status", "width": 110, "resizable": False},
        {"column_id": "active", "width": 80, "resizable": False},
    ]

    if "preview_grid_rows" not in ctx.state:
        ctx.state["preview_grid_rows"] = [
            {
                "row_id": "header",
                "height": 38,
                "cells": [
                    {"type": "header", "text": "Name"},
                    {"type": "header", "text": "Role"},
                    {"type": "header", "text": "Status"},
                    {"type": "header", "text": "Active"},
                ],
            },
            {
                "row_id": "row-1",
                "height": 38,
                "cells": [
                    {"type": "text", "text": "Alice Walker"},
                    {"type": "text", "text": "Lead Architect"},
                    {"type": "badge", "text": "Active", "variant": "success"},
                    {"type": "checkbox", "checked": True},
                ],
            },
            {
                "row_id": "row-2",
                "height": 38,
                "cells": [
                    {"type": "text", "text": "David Miller"},
                    {"type": "text", "text": "Product Lead"},
                    {"type": "badge", "text": "Pending", "variant": "warning"},
                    {"type": "checkbox", "checked": False},
                ],
            },
        ]
    preview_rows = ctx.state["preview_grid_rows"]

    content_children = []
    if HAS_GRID:
        content_children.append(
            RefastGrid(
                id="doc-live-grid-preview",
                columns=preview_cols,
                rows=preview_rows,
                sticky_top_rows=1,
                enable_fill_handle=True,
                on_cells_changed=ctx.callback(on_preview_cells_changed),
            )
        )
    else:
        content_children.append(
            Container(
                class_name="bg-muted p-4 rounded text-center text-sm text-muted-foreground",
                children=[Text("Install refast_grid to view live preview.")],
            )
        )

    return Card(
        class_name="border-primary/30 shadow-sm",
        children=[
            CardHeader(
                children=[
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            Row(
                                gap=2,
                                align="center",
                                children=[
                                    Icon("grid-3x3", class_name="text-primary"),
                                    CardTitle("Live Component Preview", class_name="text-base"),
                                ],
                            ),
                            Button(
                                "Open Fullscreen Example →",
                                size="sm",
                                variant="outline",
                                on_click=ctx.callback(open_demo),
                            ),
                        ],
                    ),
                    CardDescription("Click to edit cells, toggle checkboxes, or drag the fill-handle directly on this page:"),
                ],
            ),
            CardContent(children=content_children),
        ],
    )


CONTENT = r"""
## Overview

`refast_grid` brings an Excel-like editing experience to Refast web applications. It wraps the powerful [Silevis ReactGrid](https://reactgrid.com/) library, delivering:

- **Full Keyboard Navigation**: Arrow keys, Enter, Tab, and Escape behave like a native spreadsheet.
- **Rich Cell Types**: Support for text, numbers, checkboxes, dropdowns, badges, ratings, avatars, progress bars, sparklines, and hierarchical tree chevrons.
- **Sticky / Pinned Rows & Columns**: Pin headers at the top, totals at the bottom, or IDs on the left/right.
- **Excel-Style Interactions**: Column resizing, fill handles (drag-to-copy), multi-cell range selections, and drag-and-drop row/column reordering.
- **Server-Side Callbacks**: Stream edits and cell mutations back to Python with exact coordinates and diffs.

---

## Quick Start Example

Install `refast_grid` and run this complete example:

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Heading
from refast_grid import RefastGrid

ui = RefastApp(title="Grid Demo")

columns = [
    {"column_id": "name", "width": 180, "resizable": True},
    {"column_id": "role", "width": 150, "resizable": True},
    {"column_id": "salary", "width": 120, "resizable": True},
    {"column_id": "active", "width": 90, "resizable": False},
]

default_rows = [
    # Header Row
    {
        "row_id": "header",
        "height": 38,
        "cells": [
            {"type": "header", "text": "Employee Name"},
            {"type": "header", "text": "Role"},
            {"type": "header", "text": "Salary ($)"},
            {"type": "header", "text": "Active"},
        ],
    },
    # Data Rows
    {
        "row_id": "emp-1",
        "height": 38,
        "cells": [
            {"type": "text", "text": "Alice Johnson"},
            {"type": "text", "text": "Senior Engineer"},
            {"type": "number", "value": 145000},
            {"type": "checkbox", "checked": True},
        ],
    },
    {
        "row_id": "emp-2",
        "height": 38,
        "cells": [
            {"type": "text", "text": "Bob Smith"},
            {"type": "text", "text": "Product Manager"},
            {"type": "number", "value": 135000},
            {"type": "checkbox", "checked": True},
        ],
    },
]

async def on_cells_changed(ctx: Context):
    changes = ctx.event_data.get("changes", [])
    rows = ctx.state.get("grid_rows", [dict(r) for r in default_rows])
    rows_by_id = {r["row_id"]: r for r in rows}
    col_order = ["name", "role", "salary", "active"]
    col_idx_map = {col: i for i, col in enumerate(col_order)}

    for c in changes:
        row_id = c.get("rowId")
        col_id = c.get("columnId")
        new_cell = c.get("newCell", {})
        if row_id in rows_by_id and col_id in col_idx_map:
            target_row = rows_by_id[row_id]
            idx = col_idx_map[col_id]
            target_row["cells"][idx] = {**target_row["cells"][idx], **new_cell}

    # Persist updated rows in state and push to frontend
    ctx.state["grid_rows"] = rows
    await ctx.update_props("staff-grid", {"rows": rows})

@ui.page("/")
def home(ctx: Context):
    if "grid_rows" not in ctx.state:
        ctx.state["grid_rows"] = [dict(r) for r in default_rows]

    return Container(
        class_name="p-8 max-w-4xl mx-auto space-y-4",
        children=[
            Heading("Staff Directory"),
            RefastGrid(
                id="staff-grid",
                columns=columns,
                rows=ctx.state["grid_rows"],
                sticky_top_rows=1,
                enable_range_selection=True,
                enable_fill_handle=True,
                on_cells_changed=ctx.callback(on_cells_changed),
            ),
        ],
    )

app = FastAPI()
app.include_router(ui.router)
```

> [!IMPORTANT]
> **Controlled Component & State Persistence**: ReactGrid is a strictly controlled component. When users edit cells, `on_cells_changed` receives the changes, but ReactGrid does not mutate rows locally. To persist edits, update your state in Python and call `await ctx.update_props(grid_id, {"rows": updated_rows})`.

---

## Component Reference: `RefastGrid`

```python
from refast_grid import RefastGrid
```

### Props Reference

| Prop | Type | Default | Description |
|---|---|---|---|
| `columns` | `list[dict]` | **Required** | Column definitions. Dict keys: `column_id`, `width`, `resizable`, `reorderable`. |
| `rows` | `list[dict]` | **Required** | Row definitions. Dict keys: `row_id`, `cells` (list of cell dicts), `height`, `reorderable`. |
| `sticky_top_rows` | `int` | `0` | Number of rows pinned at the top (e.g. headers). |
| `sticky_bottom_rows` | `int` | `0` | Number of rows pinned at the bottom (e.g. totals or summaries). |
| `sticky_left_columns` | `int` | `0` | Number of columns pinned to the left edge. |
| `sticky_right_columns` | `int` | `0` | Number of columns pinned to the right edge. |
| `enable_column_resize_on_all_headers` | `bool` | `True` | Enables dragging header cell borders to resize columns. |
| `can_reorder_rows` | `bool` | `True` | Allows users to drag-and-drop reorder rows. |
| `can_reorder_columns` | `bool` | `True` | Allows users to drag-and-drop reorder columns. |
| `enable_fill_handle` | `bool` | `False` | Displays the Excel bottom-right fill handle to drag-copy cell values. |
| `enable_range_selection` | `bool` | `False` | Allows selecting multi-cell rectangular ranges. |
| `enable_row_selection` | `bool` | `False` | Allows clicking row headers to select entire rows. |
| `enable_column_selection` | `bool` | `False` | Allows clicking column headers to select entire columns. |
| `highlights` | `list[dict] \| None` | `None` | Coordinate list to highlight: `{"row_id": ..., "column_id": ..., "color": ...}`. |
| `focus_location` | `dict \| None` | `None` | Programmatically moves cell focus: `{"row_id": "...", "column_id": "..."}`. |
| `initial_focus_location` | `dict \| None` | `None` | Focus location set on initial component mount. |
| `id` | `str \| None` | `None` | Component ID (required for bound JS calls). |
| `class_name` | `str` | `""` | CSS classes applied to grid container. |

---

## Cell Types Reference

`RefastGrid` supports both standard spreadsheet cells and custom rich UI components.

### 1. Standard Built-in Types

| Cell `type` | Required / Common Keys | Description |
|---|---|---|
| `"header"` | `text` | Static column or row header cell. |
| `"text"` | `text`, `placeholder`, `non_editable` | Standard editable text cell. |
| `"number"` | `value` (float/int), `format`, `nan_to_zero` | Formatted numeric input cell. |
| `"checkbox"` | `checked` (bool), `disabled` | Interactive toggle checkbox. |
| `"date"` | `date` (ISO date string) | Native HTML5 date picker popup. |
| `"time"` | `time` (HH:MM string) | Time input picker. |
| `"email"` | `text` | Validated email address field. |
| `"chevron"` | `text`, `is_expanded` (bool), `has_children` (bool), `indent` (int) | Tree grid cell with collapsible chevron arrow icon. |

### 2. Premium / Custom Rich Types

| Cell `type` | Keys | Description |
|---|---|---|
| `"badge"` | `text`, `variant` (`"primary"`, `"secondary"`, `"success"`, `"warning"`, `"destructive"`, `"info"`) | Styled pill tag for status or categories. |
| `"dropdown"` | `value`, `options` (list of `{"value": ..., "label": ...}`) | Select dropdown menu within the cell. |
| `"button"` | `text`, `action_id`, `variant` (`"primary"`, `"secondary"`, `"destructive"`, `"outline"`) | Action button that triggers a cell change event on click. |
| `"progress"` | `value` (0.0 to 1.0) | Horizontal progress completion bar. |
| `"avatar"` | `name`, `avatar_url`, `subtext` | Profile photo/initials alongside descriptive text. |
| `"sparkline"` | `values` (list of numbers), `chart_type` (`"line"` or `"bar"`) | Embedded mini SVG trend chart inside the cell. |
| `"rating"` | `value` (int), `max` (default 5), `icon` (`"star"`, `"heart"`, `"dot"`) | Interactive star or heart rating widget. |
| `"link"` | `text`, `url`, `new_tab` (bool) | Clickable navigation anchor link. |
| `"tags"` | `values` (list of strings) | Inline multi-tag badge collection. |
| `"color"` | `value` (hex/rgb string) | Color swatch with click-to-pick color popup. |
| `"slider"` | `value`, `min`, `max`, `step` | Draggable range slider. |

---

## Event Callbacks

Subscribe to grid interactions from Python:

| Callback Prop | Trigger & Data |
|---|---|
| `on_cells_changed` | Triggered when users finish editing cells. `ctx.event_data["changes"]` contains list of change dicts. |
| `on_focus_location_changed` | Triggered when the focused cell changes. Receives `{"location": {"rowId": ..., "columnId": ...}}`. |
| `on_column_resized` | Triggered when column resizing completes. Receives `{"columnId": ..., "width": ...}`. |
| `on_rows_reordered` | Triggered on drag-and-drop row reorder. Receives `{"targetRowId": ..., "rowIds": ..., "dropPosition": ...}`. |
| `on_columns_reordered` | Triggered on drag-and-drop column reorder. Receives `{"targetColumnId": ..., "columnIds": ..., "dropPosition": ...}`. |

### Inspecting `on_cells_changed`

```python
async def handle_edits(ctx: Context):
    changes = ctx.event_data.get("changes", [])
    for change in changes:
        row_id = change["rowId"]
        col_id = change["columnId"]
        prev_cell = change["previousCell"]
        new_cell = change["newCell"]
        print(f"Row {row_id}, Col {col_id}: {prev_cell} -> {new_cell}")
```

---

## Advanced Real-World Examples

### 1. Invoice with Sticky Calculated Totals

Demonstrates how to combine editable cells with pinned bottom summary rows:

```python
from refast import Context
from refast.components import Container, Heading
from refast_grid import RefastGrid

invoice_columns = [
    {"column_id": "desc", "width": 260, "resizable": True},
    {"column_id": "qty", "width": 80, "resizable": True},
    {"column_id": "price", "width": 120, "resizable": True},
    {"column_id": "subtotal", "width": 130, "resizable": True},
]

def build_invoice_grid(items: list[dict], ctx: Context):
    header = {
        "row_id": "header",
        "cells": [
            {"type": "header", "text": "Item"},
            {"type": "header", "text": "Quantity"},
            {"type": "header", "text": "Unit Price"},
            {"type": "header", "text": "Subtotal"},
        ],
    }

    data_rows = []
    total_amount = 0.0
    for item in items:
        subtotal = item["qty"] * item["price"]
        total_amount += subtotal
        data_rows.append({
            "row_id": item["id"],
            "cells": [
                {"type": "text", "text": item["desc"]},
                {"type": "number", "value": item["qty"]},
                {"type": "number", "value": item["price"]},
                {"type": "number", "value": subtotal, "non_editable": True, "class_name": "font-mono font-semibold"},
            ],
        })

    # Sticky bottom grand total row
    summary_row = {
        "row_id": "grand-total",
        "cells": [
            {"type": "text", "text": "Total Invoice", "non_editable": True, "class_name": "font-bold text-right"},
            {"type": "text", "text": "", "non_editable": True},
            {"type": "text", "text": "", "non_editable": True},
            {"type": "number", "value": total_amount, "non_editable": True, "class_name": "font-bold font-mono text-primary"},
        ],
    }

    return RefastGrid(
        id="invoice-grid",
        columns=invoice_columns,
        rows=[header, *data_rows, summary_row],
        sticky_top_rows=1,
        sticky_bottom_rows=1,
    )
```

---

### 2. Hierarchical Tree Grid (Collapsible Chevrons)

Use `"chevron"` cells to build expandable folder structures, department hierarchies, or bill-of-materials:

```python
tree_columns = [
    {"column_id": "department", "width": 260, "resizable": True},
    {"column_id": "headcount", "width": 120, "resizable": True},
    {"column_id": "budget", "width": 140, "resizable": True},
]

tree_rows = [
    {
        "row_id": "header",
        "cells": [
            {"type": "header", "text": "Department / Team"},
            {"type": "header", "text": "Headcount"},
            {"type": "header", "text": "Annual Budget"},
        ],
    },
    # Root node
    {
        "row_id": "eng-dept",
        "cells": [
            {"type": "chevron", "text": "Engineering", "is_expanded": True, "has_children": True, "indent": 0},
            {"type": "number", "value": 45, "non_editable": True},
            {"type": "number", "value": 5200000, "non_editable": True},
        ],
    },
    # Child node (indented)
    {
        "row_id": "eng-frontend",
        "cells": [
            {"type": "chevron", "text": "Frontend & Design", "is_expanded": False, "has_children": False, "indent": 1},
            {"type": "number", "value": 18},
            {"type": "number", "value": 2100000},
        ],
    },
    {
        "row_id": "eng-backend",
        "cells": [
            {"type": "chevron", "text": "Backend & Cloud", "is_expanded": False, "has_children": False, "indent": 1},
            {"type": "number", "value": 27},
            {"type": "number", "value": 3100000},
        ],
    },
]
```

---

### 3. Rich Dashboard Grid (Badges, Ratings, Avatars, Dropdowns)

```python
rich_columns = [
    {"column_id": "user", "width": 260},
    {"column_id": "status", "width": 130},
    {"column_id": "priority", "width": 130},
    {"column_id": "rating", "width": 140},
    {"column_id": "progress", "width": 160},
]

rich_rows = [
    {
        "row_id": "header",
        "height": 38,
        "cells": [
            {"type": "header", "text": "Member"},
            {"type": "header", "text": "Status"},
            {"type": "header", "text": "Priority"},
            {"type": "header", "text": "Satisfaction"},
            {"type": "header", "text": "Sprint Progress"},
        ],
    },
    {
        "row_id": "row-1",
        "height": 56,  # Explicit height (56px) prevents squishing for avatar & multi-line cells
        "cells": [
            {"type": "avatar", "name": "Elena Rostova", "subtext": "Frontend Lead"},
            {"type": "badge", "text": "Active", "variant": "success"},
            {"type": "dropdown", "value": "high", "options": [{"value": "low", "label": "Low"}, {"value": "high", "label": "High"}]},
            {"type": "rating", "value": 5, "max": 5, "icon": "star"},
            {"type": "progress", "value": 0.85},
        ],
    },
]
```

> [!TIP]
> **Row Height for Custom Cells**: By default, ReactGrid assigns a compact row height (~25px). When rendering `"avatar"` cells (which include an image/circle and two lines of text) or button cells, set `"height": 56` on each row object to give the content adequate vertical room and prevent clipping.

---

## Next Steps

- [refast-echarts](/docs/extensions/echarts) — Rich charts and data visualization
- [refast_vtk_js](/docs/extensions/vtk-js) — 3D graphics and volumetric rendering
- [Building Extensions](/docs/advanced/extension-dev) — Authoring custom Refast extensions
"""
