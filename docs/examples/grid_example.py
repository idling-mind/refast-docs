"""Standalone RefastGrid Extension Example — /examples/grid."""

from refast import Context
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
    Row,
    Separator,
    Tabs,
    TabItem,
    Text,
)
from refast_grid import RefastGrid


# ============================================================================
# Example 1: Editable Inventory Spreadsheet
# ============================================================================

INVENTORY_COLUMNS = [
    {"column_id": "sku", "width": 120, "resizable": False},
    {"column_id": "name", "width": 220, "resizable": True},
    {"column_id": "category", "width": 140, "resizable": True},
    {"column_id": "qty", "width": 100, "resizable": True},
    {"column_id": "price", "width": 110, "resizable": True},
    {"column_id": "reorder", "width": 90, "resizable": False},
]

DEFAULT_INVENTORY_DATA = [
    {"id": "row-1", "sku": "PROD-001", "name": "Ultra-Wide Monitor 34\"", "category": "Displays", "qty": 35, "price": 599.99, "reorder": False},
    {"id": "row-2", "sku": "PROD-002", "name": "Mechanical Keyboard (RGB)", "category": "Peripherals", "qty": 8, "price": 129.50, "reorder": True},
    {"id": "row-3", "sku": "PROD-003", "name": "Wireless Ergonomic Mouse", "category": "Peripherals", "qty": 62, "price": 79.99, "reorder": False},
    {"id": "row-4", "sku": "PROD-004", "name": "USB-C Dual 4K Dock", "category": "Accessories", "qty": 14, "price": 199.00, "reorder": True},
]


def build_inventory_rows(data: list[dict]) -> list[dict]:
    header_row = {
        "row_id": "header",
        "height": 38,
        "cells": [
            {"type": "header", "text": "SKU"},
            {"type": "header", "text": "Product Name"},
            {"type": "header", "text": "Category"},
            {"type": "header", "text": "Quantity"},
            {"type": "header", "text": "Price ($)"},
            {"type": "header", "text": "Reorder"},
        ],
    }
    data_rows = []
    for item in data:
        data_rows.append({
            "row_id": item["id"],
            "height": 38,
            "cells": [
                {"type": "text", "text": item["sku"], "non_editable": True, "class_name": "font-mono bg-muted/40 text-center"},
                {"type": "text", "text": item["name"]},
                {"type": "text", "text": item["category"]},
                {"type": "number", "value": item["qty"]},
                {"type": "number", "value": item["price"]},
                {"type": "checkbox", "checked": item["reorder"]},
            ],
        })
    return [header_row, *data_rows]


async def on_inventory_cells_changed(ctx: Context):
    data = ctx.state.get("inventory_data", [dict(x) for x in DEFAULT_INVENTORY_DATA])
    changes = ctx.event_data.get("changes", [])
    
    for change in changes:
        row_id = change.get("rowId")
        col_id = change.get("columnId")
        new_cell = change.get("newCell", {})
        
        item = next((x for x in data if x["id"] == row_id), None)
        if not item:
            continue
            
        if col_id == "name":
            item["name"] = new_cell.get("text", "")
        elif col_id == "category":
            item["category"] = new_cell.get("text", "")
        elif col_id == "qty":
            item["qty"] = int(new_cell.get("value", 0))
        elif col_id == "price":
            item["price"] = float(new_cell.get("value", 0.0))
        elif col_id == "reorder":
            item["reorder"] = bool(new_cell.get("checked", False))
            
        val = new_cell.get("value") or new_cell.get("text") or new_cell.get("checked")
        await ctx.show_toast(f"Updated {item['sku']} [{col_id}] → {val}", variant="info")

    ctx.state["inventory_data"] = data
    await ctx.update_props("inventory-grid-demo", {"rows": build_inventory_rows(data)})


# ============================================================================
# Example 2: Invoice with Sticky Totals & Calculated Cells
# ============================================================================

INVOICE_COLUMNS = [
    {"column_id": "desc", "width": 320, "resizable": True},
    {"column_id": "hours", "width": 100, "resizable": True},
    {"column_id": "rate", "width": 120, "resizable": True},
    {"column_id": "subtotal", "width": 140, "resizable": True},
]

DEFAULT_INVOICE_DATA = [
    {"id": "item-1", "desc": "Architecture Design & Schema Review", "hours": 24, "rate": 175.0},
    {"id": "item-2", "desc": "Refast Extensions Development & Integration", "hours": 60, "rate": 150.0},
    {"id": "item-3", "desc": "Documentation & Performance Benchmarking", "hours": 16, "rate": 125.0},
]


def build_invoice_rows(items: list[dict]) -> list[dict]:
    header_row = {
        "row_id": "header",
        "height": 38,
        "cells": [
            {"type": "header", "text": "Service / Milestone"},
            {"type": "header", "text": "Hours"},
            {"type": "header", "text": "Rate ($/hr)"},
            {"type": "header", "text": "Subtotal ($)"},
        ],
    }
    data_rows = []
    grand_total = 0.0
    for item in items:
        subtotal = item["hours"] * item["rate"]
        grand_total += subtotal
        data_rows.append({
            "row_id": item["id"],
            "height": 38,
            "cells": [
                {"type": "text", "text": item["desc"]},
                {"type": "number", "value": item["hours"]},
                {"type": "number", "value": item["rate"]},
                {"type": "number", "value": subtotal, "non_editable": True, "class_name": "font-mono font-semibold bg-muted/20"},
            ],
        })

    # Sticky bottom total summary row
    total_row = {
        "row_id": "total-summary",
        "height": 42,
        "cells": [
            {"type": "text", "text": "Grand Total (USD)", "non_editable": True, "class_name": "font-bold text-right"},
            {"type": "text", "text": "", "non_editable": True},
            {"type": "text", "text": "", "non_editable": True},
            {"type": "number", "value": grand_total, "non_editable": True, "class_name": "font-bold font-mono text-primary text-base bg-primary/10"},
        ],
    }
    return [header_row, *data_rows, total_row]


async def on_invoice_cells_changed(ctx: Context):
    items = ctx.state.get("invoice_data", [dict(x) for x in DEFAULT_INVOICE_DATA])
    changes = ctx.event_data.get("changes", [])

    for change in changes:
        row_id = change.get("rowId")
        col_id = change.get("columnId")
        new_cell = change.get("newCell", {})

        item = next((x for x in items if x["id"] == row_id), None)
        if not item:
            continue

        if col_id == "desc":
            item["desc"] = new_cell.get("text", "")
        elif col_id == "hours":
            item["hours"] = float(new_cell.get("value", 0.0))
        elif col_id == "rate":
            item["rate"] = float(new_cell.get("value", 0.0))

    ctx.state["invoice_data"] = items
    updated_rows = build_invoice_rows(items)
    grand_total = sum(x["hours"] * x["rate"] for x in items)
    await ctx.update_props("invoice-grid-demo", {"rows": updated_rows})
    await ctx.show_toast(f"Invoice recalculated! New Total: ${grand_total:,.2f}", variant="success")


# ============================================================================
# Example 3: Rich Cell Types (Avatars, Badges, Ratings, Dropdowns, Progress)
# ============================================================================

RICH_COLUMNS = [
    {"column_id": "member", "width": 270, "resizable": True},
    {"column_id": "status", "width": 130, "resizable": True},
    {"column_id": "priority", "width": 140, "resizable": True},
    {"column_id": "rating", "width": 150, "resizable": True},
    {"column_id": "progress", "width": 180, "resizable": True},
]

DEFAULT_RICH_DATA = [
    {
        "id": "user-1",
        "name": "Elena Rostova",
        "subtext": "Frontend Architect",
        "status": "Active",
        "variant": "success",
        "priority": "high",
        "rating": 5,
        "progress": 0.85,
    },
    {
        "id": "user-2",
        "name": "Marcus Vance",
        "subtext": "DevOps Engineer",
        "status": "In Review",
        "variant": "warning",
        "priority": "med",
        "rating": 4,
        "progress": 0.65,
    },
    {
        "id": "user-3",
        "name": "Sophia Tanaka",
        "subtext": "Data Scientist",
        "status": "Completed",
        "variant": "info",
        "priority": "high",
        "rating": 5,
        "progress": 0.98,
    },
]


def build_rich_rows(items: list[dict]) -> list[dict]:
    header_row = {
        "row_id": "header",
        "height": 38,
        "cells": [
            {"type": "header", "text": "Team Member"},
            {"type": "header", "text": "Status"},
            {"type": "header", "text": "Priority"},
            {"type": "header", "text": "Satisfaction"},
            {"type": "header", "text": "Quarterly Target"},
        ],
    }
    data_rows = []
    for item in items:
        data_rows.append({
            "row_id": item["id"],
            "height": 56,  # Generous height to prevent squishing of avatar & text details
            "cells": [
                {"type": "avatar", "name": item["name"], "subtext": item["subtext"]},
                {"type": "badge", "text": item["status"], "variant": item["variant"]},
                {
                    "type": "dropdown",
                    "value": item["priority"],
                    "options": [
                        {"value": "low", "label": "Low"},
                        {"value": "med", "label": "Medium"},
                        {"value": "high", "label": "High"},
                    ],
                },
                {"type": "rating", "value": item["rating"], "max": 5, "icon": "star"},
                {"type": "progress", "value": item["progress"]},
            ],
        })
    return [header_row, *data_rows]


async def on_rich_cells_changed(ctx: Context):
    items = ctx.state.get("rich_data", [dict(x) for x in DEFAULT_RICH_DATA])
    changes = ctx.event_data.get("changes", [])

    for change in changes:
        row_id = change.get("rowId")
        col_id = change.get("columnId")
        new_cell = change.get("newCell", {})

        item = next((x for x in items if x["id"] == row_id), None)
        if not item:
            continue

        if col_id == "priority":
            item["priority"] = new_cell.get("value", item["priority"])
            await ctx.show_toast(f"{item['name']} priority updated to: {item['priority'].upper()}", variant="info")
        elif col_id == "rating":
            item["rating"] = int(new_cell.get("value", item["rating"]))
            await ctx.show_toast(f"{item['name']} satisfaction rating: {item['rating']}/5 stars", variant="info")
        elif col_id == "progress":
            item["progress"] = float(new_cell.get("value", item["progress"]))
            await ctx.show_toast(f"{item['name']} progress: {int(item['progress'] * 100)}%", variant="info")

    ctx.state["rich_data"] = items
    await ctx.update_props("rich-grid-demo", {"rows": build_rich_rows(items)})


# ============================================================================
# Main Page Renderer
# ============================================================================

async def back_to_docs(ctx: Context):
    await ctx.load("/docs/extensions/grid")


def grid_page(ctx: Context):
    """Render the standalone RefastGrid example showcase page."""
    # Ensure session state is initialized
    if "inventory_data" not in ctx.state:
        ctx.state["inventory_data"] = [dict(x) for x in DEFAULT_INVENTORY_DATA]
    if "invoice_data" not in ctx.state:
        ctx.state["invoice_data"] = [dict(x) for x in DEFAULT_INVOICE_DATA]
    if "rich_data" not in ctx.state:
        ctx.state["rich_data"] = [dict(x) for x in DEFAULT_RICH_DATA]

    inventory_rows = build_inventory_rows(ctx.state["inventory_data"])
    invoice_rows = build_invoice_rows(ctx.state["invoice_data"])
    rich_rows = build_rich_rows(ctx.state["rich_data"])

    return Container(
        class_name="min-h-screen bg-background p-6 space-y-6 max-w-6xl mx-auto",
        children=[
            # Header
            Row(
                justify="between",
                align="center",
                children=[
                    Column(
                        children=[
                            Row(
                                gap=2,
                                align="center",
                                children=[
                                    Badge("Extension Demo", variant="secondary"),
                                    Badge("refast_grid", variant="outline"),
                                    Badge("ReactGrid", variant="outline"),
                                ],
                            ),
                            Heading("RefastGrid Spreadsheet Showcase", level=1, class_name="text-3xl font-extrabold"),
                            Text("Fully reactive spreadsheet with server-side cell change mutations and custom cells", class_name="text-muted-foreground text-sm"),
                        ]
                    ),
                    Button("← Back to Docs", variant="outline", on_click=ctx.callback(back_to_docs)),
                ],
            ),
            Separator(),
            # Showcase Tabs
            Tabs(
                default_value="inventory",
                children=[
                    TabItem(
                        value="inventory",
                        label="Editable Inventory",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Interactive Spreadsheet with Server Mutation"),
                                            CardDescription("Type to edit text or numbers, toggle checkboxes, and drag the fill-handle. Changes persist immediately:"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            RefastGrid(
                                                id="inventory-grid-demo",
                                                columns=INVENTORY_COLUMNS,
                                                rows=inventory_rows,
                                                sticky_top_rows=1,
                                                enable_fill_handle=True,
                                                enable_range_selection=True,
                                                on_cells_changed=ctx.callback(on_inventory_cells_changed),
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                    ),
                    TabItem(
                        value="invoice",
                        label="Invoice with Sticky Totals",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Calculated Spreadsheet with Pinned Rows"),
                                            CardDescription("Edit Hours or Rate; Subtotals and Grand Total recalculate dynamically on the server:"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            RefastGrid(
                                                id="invoice-grid-demo",
                                                columns=INVOICE_COLUMNS,
                                                rows=invoice_rows,
                                                sticky_top_rows=1,
                                                sticky_bottom_rows=1,
                                                on_cells_changed=ctx.callback(on_invoice_cells_changed),
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                    ),
                    TabItem(
                        value="rich",
                        label="Rich Cell Types",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Dashboard Directory (Row Height: 56px)"),
                                            CardDescription("Avatars with name & role subtext, status badges, priority dropdowns, and rating stars:"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            RefastGrid(
                                                id="rich-grid-demo",
                                                columns=RICH_COLUMNS,
                                                rows=rich_rows,
                                                sticky_top_rows=1,
                                                on_cells_changed=ctx.callback(on_rich_cells_changed),
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
