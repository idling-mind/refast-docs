"""ECharts Extension — /docs/extensions/echarts."""

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
    from refast_echarts import ECharts
    HAS_ECHARTS = True
except ImportError:
    HAS_ECHARTS = False

PAGE_TITLE = "ECharts Extension"
PAGE_ROUTE = "/docs/extensions/echarts"


def render(ctx):
    """Render the refast-echarts documentation page."""
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
                            Badge("refast-echarts", variant="secondary"),
                            Badge("Visualization", variant="outline"),
                            Badge("Apache ECharts 5", variant="outline"),
                        ],
                    ),
                    Heading(PAGE_TITLE, level=1),
                    Text(
                        "Apache ECharts integration for Refast. Build dynamic, interactive, and responsive 2D/3D charts with full server-side control.",
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
                                children=[Text("pip install refast-echarts")],
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
    """Render a live interactive preview card embedded in documentation."""
    async def open_demo(c):
        await c.load("/examples/echarts")

    async def on_preview_click(c):
        data = c.event_data
        name = data.get("name")
        val = data.get("value")
        await c.show_toast(f"Live preview clicked: {name} = {val}", variant="info")

    preview_option = {
        "title": {"text": "Weekly Sales Overview", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Sales",
                "type": "bar",
                "data": [120, 200, 150, 80, 70, 110, 130],
                "itemStyle": {"borderRadius": [4, 4, 0, 0]},
            }
        ],
    }

    content_children = []
    if HAS_ECHARTS:
        content_children.append(
            ECharts(
                id="doc-live-echarts-preview",
                option=preview_option,
                height="320px",
                on_click=ctx.callback(on_preview_click),
            )
        )
    else:
        content_children.append(
            Container(
                class_name="bg-muted p-4 rounded text-center text-sm text-muted-foreground",
                children=[Text("Install refast-echarts to view live preview.")],
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
                                    Icon("bar-chart-2", class_name="text-primary"),
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
                    CardDescription("Interact with this live ECharts component directly on this page (click any bar):"),
                ],
            ),
            CardContent(children=content_children),
        ],
    )


CONTENT = r"""
## Overview

`refast-echarts` wraps [Apache ECharts](https://echarts.apache.org/) into a native Refast component. It enables:

- **20+ Chart Types**: Bar, line, area, pie, donut, scatter, radar, candlestick, heatmap, gauge, funnel, treemap, sunburst, and more.
- **Client & Server Interactivity**: Subscribe to mouse clicks, double-clicks, and hover events directly from Python handlers.
- **Dynamic Updates without Remounting**: Modify series data, swap options, or trigger animations imperatively using `ctx.call_bound_js()`.
- **Theming & Responsiveness**: Supports light/dark themes and automatically resizes when parent containers shift or resize.

---

## Quick Start Example

Refast automatically discovers `refast-echarts` after installation. You can import `ECharts` immediately:

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Heading
from refast_echarts import ECharts

ui = RefastApp(title="Sales Dashboard")

@ui.page("/")
def home(ctx: Context):
    bar_option = {
        "title": {"text": "Weekly Revenue ($k)"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Revenue",
                "type": "bar",
                "data": [12.5, 18.2, 15.0, 22.4, 28.0, 32.5, 29.8],
                "itemStyle": {"borderRadius": 4},
            }
        ],
    }

    return Container(
        class_name="p-8 max-w-4xl mx-auto space-y-4",
        children=[
            Heading("Company Performance"),
            ECharts(option=bar_option, height="400px"),
        ],
    )

app = FastAPI()
app.include_router(ui.router)
```

---

## Component Reference: `ECharts`

```python
from refast_echarts import ECharts
# or alias: from refast_echarts import Echarts
```

### Props Reference

| Prop | Type | Default | Description |
|---|---|---|---|
| `option` | `dict` | `{}` | Complete Apache ECharts option dictionary (series, axes, tooltip, legend, etc.). |
| `theme` | `str \| dict \| None` | `None` | Theme name (`"light"`, `"dark"`) or custom theme object. |
| `init_opts` | `dict \| None` | `None` | Options passed to `echarts.init()` (e.g. `{"renderer": "svg"}`). |
| `auto_resize` | `bool` | `True` | Automatically triggers chart resize whenever window or container dimensions change. |
| `width` | `str \| None` | `None` | Chart container width (e.g. `"100%"`, `"600px"`). |
| `height` | `str \| None` | `None` | Chart container height (e.g. `"400px"`, `"50vh"`). |
| `loading` | `bool` | `False` | Displays ECharts built-in loading spinner animation. |
| `loading_opts` | `dict \| None` | `None` | Customization options for the loading indicator (`text`, `color`, etc.). |
| `id` | `str \| None` | `None` | Required when invoking bound JavaScript methods (`ctx.call_bound_js`). |
| `class_name` | `str` | `""` | Additional Tailwind CSS classes applied to the chart container element. |
| `style` | `dict \| None` | `None` | Inline CSS styles applied to the chart container element. |

---

## Event Callbacks

`ECharts` translates DOM mouse and chart interactions into Python callbacks. When an event fires, interaction details are available in `ctx.event_data`.

### Available Event Props

| Callback Prop | Event Trigger |
|---|---|
| `on_click` | Clicked on a chart element (bar, slice, point, legend) |
| `on_dblclick` | Double-clicked on a chart element |
| `on_mousedown` | Mouse button pressed down over chart |
| `on_mouseup` | Mouse button released over chart |
| `on_mouseover` | Mouse entered a specific chart element |
| `on_mouseout` | Mouse left a specific chart element |
| `on_globalout` | Mouse cursor left the entire chart canvas |
| `on_contextmenu` | Right-click context menu triggered on chart |

### Event Data Schema (`ctx.event_data`)

When a user interacts with a chart element, `ctx.event_data` contains:

```python
{
    "componentType": "series",       # "series", "markPoint", "timeline", etc.
    "seriesType": "bar",            # "bar", "line", "pie", etc.
    "seriesIndex": 0,               # Index of the series
    "seriesName": "Revenue",        # Name of the series
    "name": "Wed",                  # Category name / label
    "dataIndex": 2,                 # Index of the data point
    "data": 15.0,                   # Raw data item
    "value": 15.0,                  # Value of the clicked item
    "color": "#5470c6",             # Item fill color
}
```

#### Example: Handling Clicks

```python
async def on_bar_click(ctx: Context):
    data = ctx.event_data
    category = data.get("name")
    val = data.get("value")
    series = data.get("seriesName")
    await ctx.show_toast(f"Selected {series} - {category}: ${val}k", variant="info")

ECharts(
    option=bar_option,
    height="400px",
    on_click=ctx.callback(on_bar_click),
)
```

---

## Imperative Bound Methods (`ctx.call_bound_js`)

Every `ECharts` component registers imperative methods on its underlying DOM element. You can invoke them from Python without rebuilding the UI component tree:

```python
await ctx.call_bound_js("my-chart-id", "methodName", *args)
```

### Available Methods

| Method | Parameters | Description |
|---|---|---|
| `setOption` | `option: dict`, `notMerge: bool = False`, `lazyUpdate: bool = False` | Incrementally merges or replaces chart options and re-renders animations smoothly. |
| `resize` | `opts: dict = None` | Forces an immediate resize calculation (e.g. `{"width": 800, "height": 400}`). |
| `showLoading` | `type: str = "default"`, `opts: dict = None` | Displays loading spinner with optional message and color styling. |
| `hideLoading` | None | Hides active loading spinner. |
| `clear` | None | Clears all components and charts from the instance. |
| `getDataURL` | `opts: dict = None` | Exports chart canvas to base64 image data URL (`{"type": "png", "pixelRatio": 2}`). |
| `dispose` | None | Disposes the chart instance and releases WebGL/Canvas memory. |

---

## Comprehensive Code Examples

### 1. Real-Time Dynamic Updates with `setOption`

Update chart data on-the-fly without refreshing the page or reconstructing the component:

```python
import random
from refast import RefastApp, Context
from refast.components import Container, Row, Button, Text
from refast_echarts import ECharts

ui = RefastApp()

INITIAL_OPTION = {
    "title": {"text": "Server Load (%)"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": [f"{i}s" for i in range(10)]},
    "yAxis": {"type": "value", "min": 0, "max": 100},
    "series": [
        {
            "name": "CPU",
            "type": "line",
            "smooth": True,
            "data": [45, 52, 49, 60, 58, 65, 70, 68, 72, 75],
            "areaStyle": {"opacity": 0.2},
        }
    ],
}

async def refresh_metrics(ctx: Context):
    new_data = [random.randint(30, 95) for _ in range(10)]
    # Partial update: only specify the series data to update
    partial_option = {
        "series": [{"name": "CPU", "data": new_data}]
    }
    await ctx.call_bound_js("cpu-chart", "setOption", partial_option)
    await ctx.show_toast("Metrics updated!", variant="success")

@ui.page("/")
def metrics_page(ctx: Context):
    return Container(
        class_name="p-6 space-y-4 max-w-3xl mx-auto",
        children=[
            Row(
                justify="between",
                align="center",
                children=[
                    Text("Live Telemetry Monitor", class_name="font-semibold text-lg"),
                    Button("Refresh Data", on_click=ctx.callback(refresh_metrics)),
                ],
            ),
            ECharts(
                id="cpu-chart",
                option=INITIAL_OPTION,
                height="350px",
            ),
        ],
    )
```

---

### 2. Interactive Pie / Donut Chart

A donut chart featuring customized legend positions, center labels, and slice selection toasts:

```python
from refast import Context
from refast.components import Card, CardHeader, CardTitle, CardContent
from refast_echarts import ECharts

DONUT_OPTION = {
    "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
    "legend": {"bottom": "0%", "left": "center"},
    "series": [
        {
            "name": "Traffic Source",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 8, "borderColor": "#fff", "borderWidth": 2},
            "label": {"show": False, "position": "center"},
            "emphasis": {
                "label": {"show": True, "fontSize": 18, "fontWeight": "bold"}
            },
            "data": [
                {"value": 1048, "name": "Search Engines"},
                {"value": 735, "name": "Direct"},
                {"value": 580, "name": "Email Marketing"},
                {"value": 484, "name": "Union Ads"},
                {"value": 300, "name": "Video Ads"},
            ],
        }
    ],
}

async def on_slice_click(ctx: Context):
    slice_name = ctx.event_data.get("name")
    slice_val = ctx.event_data.get("value")
    await ctx.show_toast(f"Filter applied: {slice_name} ({slice_val} hits)", variant="default")

def donut_card(ctx: Context):
    return Card(
        children=[
            CardHeader(children=[CardTitle("Traffic Attribution")]),
            CardContent(
                children=[
                    ECharts(
                        id="traffic-donut",
                        option=DONUT_OPTION,
                        height="320px",
                        on_click=ctx.callback(on_slice_click),
                    )
                ]
            ),
        ]
    )
```

---

### 3. Radar (Spider) Chart with Clear & Restore

```python
from refast import Context
from refast.components import Row, Button
from refast_echarts import ECharts

RADAR_OPTION = {
    "title": {"text": "Developer Skill Profile"},
    "radar": {
        "indicator": [
            {"name": "Python", "max": 100},
            {"name": "React / TS", "max": 100},
            {"name": "FastAPI", "max": 100},
            {"name": "DevOps", "max": 100},
            {"name": "Database / SQL", "max": 100},
            {"name": "UI / Design", "max": 100},
        ]
    },
    "series": [
        {
            "type": "radar",
            "data": [
                {"value": [95, 80, 92, 75, 88, 70], "name": "Senior Full-Stack"}
            ],
        }
    ],
}

async def clear_radar(ctx: Context):
    await ctx.call_bound_js("radar-chart", "clear")

async def reset_radar(ctx: Context):
    await ctx.call_bound_js("radar-chart", "setOption", RADAR_OPTION, True)

def radar_demo(ctx: Context):
    return Row(
        direction="col",
        gap=3,
        children=[
            Row(
                gap=2,
                children=[
                    Button("Clear Chart", variant="outline", on_click=ctx.callback(clear_radar)),
                    Button("Restore Profile", on_click=ctx.callback(reset_radar)),
                ],
            ),
            ECharts(
                id="radar-chart",
                option=RADAR_OPTION,
                height="380px",
            ),
        ],
    )
```

---

## Theming & Dark Mode

Refast supports seamless dark mode switching. ECharts supports this natively via the `theme` prop:

```python
ECharts(
    option=chart_option,
    theme="dark",   # or "light"
    height="400px",
)
```

You can dynamically bind the theme to the active Refast session theme, or use semantic HSL variables in your color definitions:

```python
chart_option = {
    "color": [
        "hsl(var(--chart-1))",
        "hsl(var(--chart-2))",
        "hsl(var(--chart-3))",
        "hsl(var(--chart-4))",
    ],
    # ...
}
```

---

## Next Steps

- [refast_grid](/docs/extensions/grid) — Interactive spreadsheets and high-performance tabular data
- [refast_vtk_js](/docs/extensions/vtk-js) — High-performance 3D scientific visualization
- [Building Extensions](/docs/advanced/extension-dev) — How to package your own React components
"""
