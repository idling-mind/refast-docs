"""Standalone ECharts Extension Example — /examples/echarts."""

import random
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
    Icon,
    Row,
    Separator,
    Tabs,
    TabItem,
    Text,
)
from refast_echarts import ECharts


BAR_OPTION = {
    "title": {"text": "Quarterly Revenue by Region ($M)", "left": "center"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {
        "type": "category",
        "data": ["North America", "Europe", "Asia-Pacific", "Latin America", "Middle East"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": "Revenue",
            "type": "bar",
            "data": [142.5, 98.4, 165.2, 54.1, 72.8],
            "itemStyle": {"borderRadius": [6, 6, 0, 0]},
        }
    ],
}

LINE_OPTION = {
    "title": {"text": "Live Cluster CPU Load (%)", "left": "center"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": [f"-{i * 5}s" for i in reversed(range(10))]},
    "yAxis": {"type": "value", "min": 0, "max": 100},
    "series": [
        {
            "name": "Node A",
            "type": "line",
            "smooth": True,
            "data": [45, 52, 48, 62, 58, 65, 72, 68, 75, 78],
            "areaStyle": {"opacity": 0.2},
        }
    ],
}

DONUT_OPTION = {
    "title": {"text": "Traffic Channel Attribution", "left": "center"},
    "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
    "legend": {"bottom": "0%", "left": "center"},
    "series": [
        {
            "name": "Source",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 8, "borderColor": "#fff", "borderWidth": 2},
            "data": [
                {"value": 1048, "name": "Organic Search"},
                {"value": 735, "name": "Direct Inbound"},
                {"value": 580, "name": "Email Newsletter"},
                {"value": 484, "name": "Partner Referrals"},
                {"value": 300, "name": "Social Media"},
            ],
        }
    ],
}


async def on_bar_click(ctx: Context):
    """Handle click events on bar chart elements."""
    data = ctx.event_data
    region = data.get("name")
    val = data.get("value")
    ctx.state["echarts_selected_region"] = region
    ctx.state["echarts_selected_val"] = val
    await ctx.show_toast(f"Selected {region}: ${val}M", variant="info")
    await ctx.refresh()


async def refresh_telemetry(ctx: Context):
    """Incrementally update line chart data via setOption bound method."""
    new_data = [random.randint(30, 95) for _ in range(10)]
    partial_option = {
        "series": [{"name": "Node A", "data": new_data}]
    }
    await ctx.call_bound_js("echarts-telemetry", "setOption", partial_option)
    await ctx.show_toast("Updated telemetry metrics via setOption!", variant="success")


async def back_to_docs(ctx: Context):
    await ctx.load("/docs/extensions/echarts")


def echarts_page(ctx: Context):
    """Render the standalone ECharts example showcase page."""
    selected_region = ctx.state.get("echarts_selected_region", "Click any bar...")
    selected_val = ctx.state.get("echarts_selected_val", "")

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
                                    Badge("refast-echarts", variant="outline"),
                                ],
                            ),
                            Heading("Apache ECharts Showcase", level=1, class_name="text-3xl font-extrabold"),
                            Text("Interactive charts with server-side event callbacks and imperative updates", class_name="text-muted-foreground text-sm"),
                        ]
                    ),
                    Button("← Back to Docs", variant="outline", on_click=ctx.callback(back_to_docs)),
                ],
            ),
            Separator(),
            # Tabs for different use cases
            Tabs(
                default_value="bar",
                children=[
                    TabItem(
                        value="bar",
                        label="Interactive Bar Chart",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Click Events & State Synchronization"),
                                            CardDescription("Click any bar below to capture the event in Python and synchronize selection state:"),
                                        ]
                                    ),
                                    CardContent(
                                        class_name="space-y-4",
                                        children=[
                                            ECharts(
                                                id="echarts-bar",
                                                option=BAR_OPTION,
                                                height="380px",
                                                on_click=ctx.callback(on_bar_click),
                                            ),
                                            Container(
                                                class_name="bg-muted/40 p-4 rounded-lg border",
                                                children=[
                                                    Text(
                                                        f"Current Selection: {selected_region} " + (f"(${selected_val}M)" if selected_val else ""),
                                                        class_name="font-semibold text-primary",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                    TabItem(
                        value="telemetry",
                        label="Real-Time Updates",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            Row(
                                                justify="between",
                                                align="center",
                                                children=[
                                                    Column(
                                                        children=[
                                                            CardTitle("Dynamic setOption via Bound JS"),
                                                            CardDescription("Updates chart data smoothly over WebSocket without remounting the component:"),
                                                        ]
                                                    ),
                                                    Button("Simulate New Data", on_click=ctx.callback(refresh_telemetry)),
                                                ],
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            ECharts(
                                                id="echarts-telemetry",
                                                option=LINE_OPTION,
                                                height="380px",
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                    TabItem(
                        value="donut",
                        label="Attribution Donut",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Donut Chart with Rich Tooltips"),
                                            CardDescription("Multi-segment breakdown with formatted tooltips and center labels:"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            ECharts(
                                                id="echarts-donut",
                                                option=DONUT_OPTION,
                                                height="380px",
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
