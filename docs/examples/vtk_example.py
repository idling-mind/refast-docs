"""Standalone VTK.js Extension Example — /examples/vtk-js."""

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
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
    Row,
    Separator,
    Slider,
    Tabs,
    TabItem,
    Text,
    ToggleGroup,
    ToggleGroupItem,
)
from refast_vtk_js import (
    Algorithm,
    AxesActor,
    DataArray,
    GeometryRepresentation,
    ImageData,
    Picking,
    PointData,
    PolyData,
    View,
    VolumeRepresentation,
)


TRIANGLE_POINTS = [
    0.0, 0.0, 0.0,
    2.0, 0.0, 0.0,
    1.0, 1.8, 0.0,
]


def create_volume_data():
    """Generate a 10x10x10 spherical gradient scalar volume."""
    nx, ny, nz = 10, 10, 10
    scalars = [
        ((x - 5)**2 + (y - 5)**2 + (z - 5)**2)**0.5
        for z in range(nz) for y in range(ny) for x in range(nx)
    ]
    return nx, ny, nz, scalars


async def update_cone_resolution(ctx: Context):
    data = ctx.event_data
    if isinstance(data, list) and data:
        val = data[0]
    elif isinstance(data, dict):
        val = data.get("value", [24])[0] if isinstance(data.get("value"), list) else data.get("value", 24)
    else:
        val = data or 24
    ctx.state["vtk_cone_res"] = int(val)
    await ctx.refresh()


async def on_3d_pick(ctx: Context):
    selection = ctx.event_data.get("selection", {})
    pos = selection.get("worldPosition")
    if pos:
        formatted = f"({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})"
        ctx.state["vtk_picked_pos"] = formatted
        await ctx.show_toast(f"Selected 3D point: {formatted}", variant="info")
        await ctx.refresh()


async def toggle_sync_view(ctx: Context, view_id: str):
    data = ctx.event_data
    val = data.get("value") if isinstance(data, dict) else data
    new_sync = "main" if val else None
    await ctx.update_props(target_id=view_id, props={"sync_group": new_sync})
    name = view_id.replace("view-", "").capitalize()
    status = "linked to camera sync group ('main')" if new_sync else "unlinked (independent camera)"
    await ctx.show_toast(f"{name} view {status}", variant="info")


async def back_to_docs(ctx: Context):
    await ctx.load("/docs/extensions/vtk-js")


def vtk_page(ctx: Context):
    """Render the standalone VTK.js example showcase page."""
    cone_res = ctx.state.get("vtk_cone_res", 24)
    picked_pos = ctx.state.get("vtk_picked_pos", "Click on the surface...")
    nx, ny, nz, scalars = create_volume_data()

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
                                    Badge("refast_vtk_js", variant="outline"),
                                    Badge("WebGL", variant="outline"),
                                ],
                            ),
                            Heading("VTK.js 3D Visualization Showcase", level=1, class_name="text-3xl font-extrabold"),
                            Text("Hardware-accelerated 3D graphics, procedural algorithms, and coordinate picking", class_name="text-muted-foreground text-sm"),
                        ]
                    ),
                    Button("← Back to Docs", variant="outline", on_click=ctx.callback(back_to_docs)),
                ],
            ),
            Separator(),
            # Showcase Tabs
            Tabs(
                default_value="cone",
                children=[
                    TabItem(
                        value="cone",
                        label="Procedural 3D Source",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("VTK Cone Algorithm with Dynamic Resolution"),
                                            CardDescription("Use the slider below to control the tessellation detail of the procedural vtkConeSource:"),
                                        ]
                                    ),
                                    CardContent(
                                        class_name="space-y-4",
                                        children=[
                                            Row(
                                                gap=4,
                                                align="center",
                                                children=[
                                                    Text("Tessellation Resolution:"),
                                                    Slider(
                                                        min=6,
                                                        max=64,
                                                        value=[cone_res],
                                                        on_value_change=ctx.callback(update_cone_resolution),
                                                        class_name="w-64",
                                                    ),
                                                    Text(f"{cone_res} segments", class_name="font-mono font-bold text-primary"),
                                                ],
                                            ),
                                            View(
                                                background=[0.07, 0.09, 0.13],
                                                style={"width": "100%", "height": "420px", "borderRadius": "8px"},
                                                children=[
                                                    GeometryRepresentation(
                                                        property={"color": [0.95, 0.45, 0.2], "edgeVisibility": True},
                                                        children=[
                                                            Algorithm(
                                                                vtk_class="vtkConeSource",
                                                                state={
                                                                    "height": 2.6,
                                                                    "radius": 0.85,
                                                                    "resolution": cone_res,
                                                                },
                                                            ),
                                                        ],
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
                        value="picking",
                        label="3D Coordinate Picking",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Interactive 3D Surface Picking"),
                                            CardDescription("Click anywhere on the geometry below to compute exact 3D world space coordinates:"),
                                        ]
                                    ),
                                    CardContent(
                                        class_name="space-y-4",
                                        children=[
                                            View(
                                                background=[0.06, 0.08, 0.12],
                                                style={"width": "100%", "height": "400px", "borderRadius": "8px"},
                                                children=[
                                                    Picking(
                                                        on_click=ctx.callback(on_3d_pick),
                                                        pointer_size=6,
                                                    ),
                                                    GeometryRepresentation(
                                                        property={"color": [0.25, 0.75, 0.95]},
                                                        children=[
                                                            PolyData(
                                                                points=TRIANGLE_POINTS,
                                                                connectivity="triangles",
                                                            ),
                                                        ],
                                                    ),
                                                    AxesActor(),
                                                ],
                                            ),
                                            Container(
                                                class_name="bg-muted/40 p-4 rounded-lg border",
                                                children=[
                                                    Text(
                                                        f"Picked 3D Coordinates (X, Y, Z): {picked_pos}",
                                                        class_name="font-mono text-sm font-semibold text-primary",
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
                        value="volume",
                        label="3D Volume Rendering",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Volumetric Ray Casting"),
                                            CardDescription("Render 3D scalar density fields with transfer functions and color maps:"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            View(
                                                background=[0.02, 0.02, 0.02],
                                                style={"width": "100%", "height": "420px", "borderRadius": "8px"},
                                                children=[
                                                    VolumeRepresentation(
                                                        color_map_preset="Cool to Warm",
                                                        children=[
                                                            ImageData(
                                                                dimensions=[nx, ny, nz],
                                                                spacing=[1.0, 1.0, 1.0],
                                                                origin=[0.0, 0.0, 0.0],
                                                                children=[
                                                                    PointData(
                                                                        children=[
                                                                            DataArray(
                                                                                registration="setScalars",
                                                                                values=scalars,
                                                                                number_of_components=1,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
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
                        value="synced",
                        label="Synced Views",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Synchronized Multi-Viewports (`sync_group`)"),
                                            CardDescription(
                                                "Views sharing the same sync_group link their cameras — rotating, panning, or zooming any viewport updates all linked views in real-time. Use the 🔄 toggle in the top-right of each panel to link or unlink viewports dynamically:"
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        class_name="space-y-3",
                                        children=[
                                            ResizablePanelGroup(
                                                direction="horizontal",
                                                class_name="border rounded-lg overflow-hidden",
                                                style={"width": "100%", "height": "520px"},
                                                children=[
                                                    ResizablePanel(
                                                        min_size=25,
                                                        default_size=50,
                                                        class_name="bg-card",
                                                        children=[
                                                            Container(
                                                                class_name="relative h-full w-full",
                                                                children=[
                                                                    Text(
                                                                        "Cone (Linked)",
                                                                        class_name="absolute top-2 left-2 z-10 bg-card/90 border px-2 py-1 rounded text-xs font-semibold text-foreground pointer-events-none shadow-sm",
                                                                    ),
                                                                    Container(
                                                                        class_name="absolute top-2 right-2 z-10",
                                                                        children=[
                                                                            ToggleGroup(
                                                                                default_value="toggle-cone",
                                                                                type="single",
                                                                                size="sm",
                                                                                children=[
                                                                                    ToggleGroupItem(
                                                                                        name="toggle-cone",
                                                                                        icon="refresh-cw",
                                                                                    )
                                                                                ],
                                                                                on_value_change=ctx.callback(
                                                                                    toggle_sync_view, view_id="view-cone"
                                                                                ),
                                                                            )
                                                                        ],
                                                                    ),
                                                                    View(
                                                                        id="view-cone",
                                                                        background=[0.12, 0.14, 0.22],
                                                                        sync_group="main",
                                                                        style={"width": "100%", "height": "100%"},
                                                                        children=[
                                                                            GeometryRepresentation(
                                                                                property={
                                                                                    "color": [0.2, 0.6, 1.0],
                                                                                    "edgeVisibility": True,
                                                                                    "edgeColor": [0.35, 0.35, 0.35],
                                                                                },
                                                                                children=[
                                                                                    Algorithm(
                                                                                        vtk_class="vtkConeSource",
                                                                                        state={
                                                                                            "resolution": 32,
                                                                                            "radius": 0.5,
                                                                                            "height": 1.0,
                                                                                            "capping": True,
                                                                                        },
                                                                                    )
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            )
                                                        ],
                                                    ),
                                                    ResizableHandle(with_handle=True),
                                                    ResizablePanel(
                                                        min_size=25,
                                                        default_size=50,
                                                        class_name="bg-card",
                                                        children=[
                                                            ResizablePanelGroup(
                                                                direction="vertical",
                                                                style={"height": "100%", "width": "100%"},
                                                                children=[
                                                                    ResizablePanel(
                                                                        min_size=25,
                                                                        default_size=60,
                                                                        class_name="bg-card",
                                                                        children=[
                                                                            Container(
                                                                                class_name="relative h-full w-full",
                                                                                children=[
                                                                                    Text(
                                                                                        "Sphere (Linked)",
                                                                                        class_name="absolute top-2 left-2 z-10 bg-card/90 border px-2 py-1 rounded text-xs font-semibold text-foreground pointer-events-none shadow-sm",
                                                                                    ),
                                                                                    Container(
                                                                                        class_name="absolute top-2 right-2 z-10",
                                                                                        children=[
                                                                                            ToggleGroup(
                                                                                                default_value="toggle-sphere",
                                                                                                type="single",
                                                                                                size="sm",
                                                                                                children=[
                                                                                                    ToggleGroupItem(
                                                                                                        name="toggle-sphere",
                                                                                                        icon="refresh-cw",
                                                                                                    )
                                                                                                ],
                                                                                                on_value_change=ctx.callback(
                                                                                                    toggle_sync_view, view_id="view-sphere"
                                                                                                ),
                                                                                            )
                                                                                        ],
                                                                                    ),
                                                                                    View(
                                                                                        id="view-sphere",
                                                                                        background=[0.22, 0.12, 0.14],
                                                                                        sync_group="main",
                                                                                        style={"width": "100%", "height": "100%"},
                                                                                        children=[
                                                                                            GeometryRepresentation(
                                                                                                property={
                                                                                                    "color": [1.0, 0.35, 0.35],
                                                                                                    "edgeVisibility": True,
                                                                                                    "edgeColor": [0.35, 0.35, 0.35],
                                                                                                },
                                                                                                children=[
                                                                                                    Algorithm(
                                                                                                        vtk_class="vtkSphereSource",
                                                                                                        state={
                                                                                                            "thetaResolution": 24,
                                                                                                            "phiResolution": 24,
                                                                                                            "radius": 0.5,
                                                                                                        },
                                                                                                    )
                                                                                                ],
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                ],
                                                                            )
                                                                        ],
                                                                    ),
                                                                    ResizableHandle(with_handle=True),
                                                                    ResizablePanel(
                                                                        min_size=25,
                                                                        default_size=40,
                                                                        class_name="bg-card",
                                                                        children=[
                                                                            Container(
                                                                                class_name="relative h-full w-full",
                                                                                children=[
                                                                                    Text(
                                                                                        "Cylinder (Independent / Click 🔄 to sync)",
                                                                                        class_name="absolute top-2 left-2 z-10 bg-card/90 border px-2 py-1 rounded text-xs font-semibold text-foreground pointer-events-none shadow-sm",
                                                                                    ),
                                                                                    Container(
                                                                                        class_name="absolute top-2 right-2 z-10",
                                                                                        children=[
                                                                                            ToggleGroup(
                                                                                                type="single",
                                                                                                size="sm",
                                                                                                children=[
                                                                                                    ToggleGroupItem(
                                                                                                        name="toggle-cylinder",
                                                                                                        icon="refresh-cw",
                                                                                                    )
                                                                                                ],
                                                                                                on_value_change=ctx.callback(
                                                                                                    toggle_sync_view, view_id="view-cylinder"
                                                                                                ),
                                                                                            )
                                                                                        ],
                                                                                    ),
                                                                                    View(
                                                                                        id="view-cylinder",
                                                                                        background=[0.12, 0.22, 0.14],
                                                                                        sync_group=None,
                                                                                        style={"width": "100%", "height": "100%"},
                                                                                        children=[
                                                                                            GeometryRepresentation(
                                                                                                property={
                                                                                                    "color": [0.3, 0.9, 0.4],
                                                                                                    "edgeVisibility": True,
                                                                                                    "edgeColor": [0.35, 0.35, 0.35],
                                                                                                },
                                                                                                children=[
                                                                                                    Algorithm(
                                                                                                        vtk_class="vtkCylinderSource",
                                                                                                        state={
                                                                                                            "resolution": 32,
                                                                                                            "radius": 0.4,
                                                                                                            "height": 1.0,
                                                                                                        },
                                                                                                    )
                                                                                                ],
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                ],
                                                                            )
                                                                        ],
                                                                    ),
                                                                ],
                                                            )
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            Text(
                                                "Controls: Left-drag to rotate, Right-drag to zoom, Middle-drag to pan, Scroll to zoom toward pointer.",
                                                class_name="text-xs text-muted-foreground",
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
