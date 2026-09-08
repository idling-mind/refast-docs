"""3D Visualization Extension (VTK.js) — /docs/extensions/vtk-js."""

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
    from refast_vtk_js import View, GeometryRepresentation, Algorithm
    HAS_VTK = True
except ImportError:
    HAS_VTK = False

PAGE_TITLE = "3D Visualization Extension (VTK.js)"
PAGE_ROUTE = "/docs/extensions/vtk-js"


def render(ctx):
    """Render the refast_vtk_js documentation page."""
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
                            Badge("refast_vtk_js", variant="secondary"),
                            Badge("3D Graphics", variant="outline"),
                            Badge("Kitware VTK.js", variant="outline"),
                            Badge("WebGL", variant="outline"),
                        ],
                    ),
                    Heading(PAGE_TITLE, level=1),
                    Text(
                        "Hardware-accelerated 3D rendering and scientific visualization for Refast powered by Kitware's react-vtk-js. Render polygonal meshes, volumetric medical scans, and interactive CAD models.",
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
                                children=[Text("pip install refast-vtk-js")],
                            ),
                        ],
                    ),
                ],
            ),
            # Live interactive preview card
            _live_preview_card(ctx),
            Markdown(content=CONTENT, enable_mermaid=True),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


def _live_preview_card(ctx):
    """Render a live interactive VTK.js preview card embedded in documentation."""
    async def open_demo(c):
        await c.load("/examples/vtk-js")

    content_children = []
    if HAS_VTK:
        content_children.append(
            View(
                id="doc-live-vtk-preview",
                background=[0.06, 0.08, 0.12],
                style={"width": "100%", "height": "320px", "borderRadius": "8px"},
                children=[
                    GeometryRepresentation(
                        property={"color": [0.95, 0.45, 0.2], "edgeVisibility": True},
                        children=[
                            Algorithm(
                                vtk_class="vtkConeSource",
                                state={"height": 2.5, "radius": 0.8, "resolution": 24},
                            ),
                        ],
                    ),
                ],
            )
        )
    else:
        content_children.append(
            Container(
                class_name="bg-muted p-4 rounded text-center text-sm text-muted-foreground",
                children=[Text("Install refast-vtk-js to view live 3D preview.")],
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
                                    Icon("box", class_name="text-primary"),
                                    CardTitle("Live 3D Viewport Preview", class_name="text-base"),
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
                    CardDescription("Interact with this hardware-accelerated 3D viewport (drag to rotate, scroll to zoom):"),
                ],
            ),
            CardContent(children=content_children),
        ],
    )


CONTENT = r"""
## Overview

`refast_vtk_js` brings high-performance 3D graphics and scientific visualization to the Refast ecosystem by integrating [VTK.js](https://kitware.github.io/vtk-js/) and [react-vtk-js](https://github.com/Kitware/react-vtk-js).

Key capabilities include:

- **Hardware-Accelerated WebGL/WebGPU Rendering**: Smooth 60 FPS viewport interaction even with complex geometries.
- **Surface & Volume Rendering**: Render point clouds, polygonal surfaces, wireframes, and dense 3D volume grids (CT, MRI, CFD simulations).
- **Procedural Sources & Filters**: Instantiate VTK algorithms (e.g. `vtkConeSource`, `vtkSphereSource`, `vtkOutlineFilter`) directly from Python.
- **Remote Model Loading**: Load OBJ, STL, and VTK data files via URL using `Reader`.
- **Interactive 3D Picking**: Detect clicked 3D coordinates in world space and pass coordinates to Python handlers.
- **Synchronized Multi-Views & Shared Datasets**: Render multiple synchronized viewports sharing the same 3D dataset in GPU memory.

---

## The VTK Scene Graph in Refast

VTK uses a hierarchical scene graph composed of views, representations, datasets, and algorithms:

```mermaid
graph TD
    View[View / MultiViewRoot] --> Representation[Geometry / Volume / Slice Representation]
    View --> Axes[AxesActor / Orientation Marker]
    View --> Picking[Picking Tool]
    Representation --> Dataset[PolyData / ImageData / Dataset]
    Representation --> Algorithm[Algorithm / Source / Reader]
    Dataset --> PointData[PointData / CellData]
    PointData --> DataArray[DataArray / Scalars]
```

1. **`View`**: The WebGL container and camera context.
2. **`Representation`**: Determines *how* the data is displayed (e.g., surface, wireframe, volume, slice plane).
3. **`Dataset` or `Algorithm`**: The underlying geometric or volumetric data source (e.g., `PolyData`, `ImageData`, `vtkConeSource`, or `vtkOBJReader`).
4. **`DataArray`**: Attach scalar/vector values (temperature, velocity, density) to vertices or cells for colormapping.

---

## Quick Start: Basic 3D Polygon

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Heading
from refast_vtk_js import View, GeometryRepresentation, PolyData

ui = RefastApp(title="VTK.js Demo")

@ui.page("/")
def home(ctx: Context):
    # Define triangle coordinates [x0, y0, z0, x1, y1, z1, x2, y2, z2]
    triangle_points = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.5, 1.0, 0.0]

    return Container(
        class_name="p-8 max-w-4xl mx-auto space-y-4",
        children=[
            Heading("3D Polygonal Mesh"),
            View(
                background=[0.1, 0.12, 0.16],
                style={"width": "100%", "height": "420px", "borderRadius": "8px"},
                children=[
                    GeometryRepresentation(
                        property={"color": [0.2, 0.7, 1.0]},
                        children=[
                            PolyData(
                                points=triangle_points,
                                connectivity="triangles",
                            )
                        ],
                    ),
                ],
            ),
        ],
    )

app = FastAPI()
app.include_router(ui.router)
```

---

## Component Reference

### 1. View Components

| Component | Description | Key Props |
|---|---|---|
| `View` | Primary 3D canvas viewport and camera controller. | `background` (RGB list, e.g. `[0.1, 0.1, 0.1]`), `sync_group` (str: links cameras across views sharing the same name), `camera_position`, `camera_focal_point`, `style`, `class_name`. |
| `MultiViewRoot` | Container coordinating multiple synchronized sub-views. | None (wraps multiple `View` instances). |
| `AxesActor` | 3D orientation indicator showing X (red), Y (green), Z (blue) axes. | None (added as child of `View`). |

### 2. Representation Components

| Component | Description | Key Props |
|---|---|---|
| `GeometryRepresentation` | Renders surfaces, wireframes, and point clouds. | `property` dict (`color`, `opacity`, `representation`: `"surface"`, `"wireframe"`, `"points"`), `color_map_preset`. |
| `VolumeRepresentation` | Volumetric ray-casting for regular 3D grids. | `color_map_preset` (e.g. `"Cool to Warm"`, `"Viridis"`), `volume_property` dict. |
| `SliceRepresentation` | 2D orthogonal slice through a 3D volume. | `i_slice`, `j_slice`, `k_slice`, `color_window`, `color_level`. |
| `Geometry2DRepresentation`| 2D overlay geometry inside a 3D view. | `property` dict. |

### 3. Dataset & Data Array Components

| Component | Description | Key Props |
|---|---|---|
| `PolyData` | Explicit polygonal mesh (points, lines, triangles). | `points` (flat list of floats), `connectivity` (`"triangles"`, `"strips"`, `"manual"`), `polys`, `lines`. |
| `ImageData` | Uniform rectangular 3D grid for volumetric data. | `dimensions` (`[nx, ny, nz]`), `spacing` (`[dx, dy, dz]`), `origin` (`[x0, y0, z0]`). |
| `PointData` | Container for vertex-associated scalar and vector fields. | `children` (`DataArray` list). |
| `CellData` | Container for cell/element-associated data arrays. | `children` (`DataArray` list). |
| `DataArray` | Numerical array applied to vertices or cells. | `registration` (`"setScalars"`, `"setVectors"`), `values` (flat list), `number_of_components`. |

### 4. Algorithm & Reader Components

| Component | Description | Key Props |
|---|---|---|
| `Algorithm` | Instantiates a procedural VTK algorithm or source. | `vtk_class` (e.g. `"vtkConeSource"`, `"vtkSphereSource"`, `"vtkOutlineFilter"`), `state` (dict of algorithm properties). |
| `Reader` | Loads a 3D asset file over HTTP/HTTPS. | `vtk_class` (`"vtkOBJReader"`, `"vtkSTLReader"`, `"vtkXMLPolyDataReader"`), `url`. |

### 5. Interaction & Data Sharing

| Component | Description | Key Props |
|---|---|---|
| `Picking` | Intercepts click/hover events and computes 3D coordinates. | `on_click`, `on_hover`, `pointer_size`. |
| `ShareDataSetRoot` | Root node for sharing GPU data between views. | None. |
| `RegisterDataSet` | Binds a dataset to an ID for reuse. | `dataset_id` (str). |
| `UseDataSet` | References a previously registered shared dataset. | `dataset_id` (str). |

---

## Detailed Code Examples

### 1. Procedural 3D Source (`Algorithm` with `vtkConeSource`)

Create 3D primitives without writing vertex coordinates manually:

```python
from refast import RefastApp, Context
from refast.components import Container, Row, Slider, Text
from refast_vtk_js import View, GeometryRepresentation, Algorithm

ui = RefastApp()

@ui.page("/")
def cone_demo(ctx: Context):
    resolution = ctx.state.get("cone_res", 30)
    radius = ctx.state.get("cone_radius", 1.0)

    async def update_res(c):
        data = c.event_data
        val = data[0] if isinstance(data, list) else data
        c.state["cone_res"] = int(val)
        await c.refresh()

    return Container(
        class_name="p-6 space-y-4 max-w-4xl mx-auto",
        children=[
            Row(
                gap=4,
                align="center",
                children=[
                    Text("Cone Resolution:"),
                    Slider(
                        min=6,
                        max=60,
                        value=[resolution],
                        on_value_change=ctx.callback(update_res),
                        class_name="w-64",
                    ),
                    Text(str(resolution), class_name="font-mono font-bold"),
                ],
            ),
            View(
                background=[0.05, 0.08, 0.12],
                style={"width": "100%", "height": "450px", "borderRadius": "8px"},
                children=[
                    GeometryRepresentation(
                        property={"color": [0.9, 0.4, 0.2], "edgeVisibility": True},
                        children=[
                            Algorithm(
                                vtk_class="vtkConeSource",
                                state={
                                    "height": 3.0,
                                    "radius": radius,
                                    "resolution": resolution,
                                },
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
```

---

### 2. 3D Volume Rendering (`ImageData` + `VolumeRepresentation`)

Render 3D volumetric fields (such as CT scans, magnetic fields, or temperature distributions):

```python
from refast_vtk_js import View, VolumeRepresentation, ImageData, PointData, DataArray

# Define a 12x12x12 scalar field
nx, ny, nz = 12, 12, 12
scalar_values = [
    ((x - 6)**2 + (y - 6)**2 + (z - 6)**2)**0.5
    for z in range(nz) for y in range(ny) for x in range(nx)
]

volume_view = View(
    background=[0.0, 0.0, 0.0],
    style={"width": "100%", "height": "450px"},
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
                                    values=scalar_values,
                                    number_of_components=1,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
```

---

### 3. Loading Remote 3D CAD/OBJ Models (`Reader`)

Load OBJ or STL files directly from a static asset path or remote URL:

```python
from refast_vtk_js import View, GeometryRepresentation, Reader

model_view = View(
    background=[0.15, 0.15, 0.18],
    style={"width": "100%", "height": "450px"},
    children=[
        GeometryRepresentation(
            property={"color": [0.8, 0.8, 0.8]},
            children=[
                Reader(
                    vtk_class="vtkOBJReader",
                    url="https://kitware.github.io/react-vtk-js/data/obj/space-shuttle-orbiter/space-shuttle-orbiter.obj",
                ),
            ],
        ),
    ],
)
```

---

### 4. Interactive 3D Coordinate Picking

Attach a `Picking` component to intercept mouse clicks and extract 3D Cartesian coordinates:

```python
from refast import Context
from refast.components import Text
from refast_vtk_js import View, GeometryRepresentation, PolyData, Picking, AxesActor

async def handle_3d_click(ctx: Context):
    selection = ctx.event_data.get("selection", {})
    world_pos = selection.get("worldPosition")
    if world_pos:
        x, y, z = world_pos[0], world_pos[1], world_pos[2]
        await ctx.show_toast(f"Clicked point: ({x:.2f}, {y:.2f}, {z:.2f})", variant="info")

picking_view = View(
    background=[0.08, 0.1, 0.14],
    style={"width": "100%", "height": "400px"},
    children=[
        Picking(
            on_click=ctx.callback(handle_3d_click),
            pointer_size=6,
        ),
        GeometryRepresentation(
            property={"color": [0.3, 0.8, 0.4]},
            children=[
                PolyData(
                    points=[0, 0, 0, 1, 0, 0, 0.5, 1, 0],
                    connectivity="triangles",
                ),
            ],
        ),
        AxesActor(),
    ],
)
```

---

### 5. Multi-View Synchronized Data Sharing

Share a single geometric model between two viewports without duplicating data in GPU memory:

```python
from refast_vtk_js import (
    ShareDataSetRoot,
    RegisterDataSet,
    UseDataSet,
    View,
    GeometryRepresentation,
    Algorithm,
)

synced_views = ShareDataSetRoot(
    children=[
        # Register the shared sphere geometry once
        RegisterDataSet(
            dataset_id="shared-sphere",
            children=[
                Algorithm(
                    vtk_class="vtkSphereSource",
                    state={"radius": 2.0, "thetaResolution": 30, "phiResolution": 30},
                ),
            ],
        ),
        # View A: Rendered as surface with color
        View(
            style={"width": "48%", "height": "350px", "display": "inline-block"},
            children=[
                GeometryRepresentation(
                    property={"color": [1.0, 0.3, 0.3]},
                    children=[UseDataSet(dataset_id="shared-sphere")],
                ),
            ],
        ),
        # View B: Rendered as wireframe
        View(
            style={"width": "48%", "height": "350px", "display": "inline-block"},
            children=[
                GeometryRepresentation(
                    property={"representation": "wireframe", "color": [0.2, 0.8, 1.0]},
                    children=[UseDataSet(dataset_id="shared-sphere")],
                ),
            ],
        ),
    ],
)
```

---

### 6. Synchronizing Viewport Cameras (`sync_group`)

Link cameras across multiple viewports so rotating, panning, or zooming any one viewport automatically synchronizes all other viewports in the same group. Unlike `ShareDataSetRoot`, `sync_group` works with standalone `View` components anywhere in your DOM layout (inside `Row`, `ResizablePanelGroup`, or custom grid containers):

```python
from refast import Context
from refast.components import Row
from refast_vtk_js import View, GeometryRepresentation, Algorithm

# Link two viewports by giving them identical sync_group values
views = Row(
    gap=4,
    children=[
        View(
            id="view-cone",
            sync_group="main",
            background=[0.1, 0.12, 0.18],
            style={"width": "50%", "height": "400px"},
            children=[
                GeometryRepresentation(
                    children=[Algorithm(vtk_class="vtkConeSource")],
                ),
            ],
        ),
        View(
            id="view-sphere",
            sync_group="main",  # Linked to "main" camera group
            background=[0.18, 0.1, 0.12],
            style={"width": "50%", "height": "400px"},
            children=[
                GeometryRepresentation(
                    children=[Algorithm(vtk_class="vtkSphereSource")],
                ),
            ],
        ),
    ],
)

# Dynamically link/unlink cameras at runtime via Python
async def unlink_cone_camera(ctx: Context):
    await ctx.update_props("view-cone", {"sync_group": None})
```

---

## Next Steps

- [ECharts Extension](/docs/extensions/echarts) — 2D business charts and dashboards
- [Spreadsheet Grid Extension](/docs/extensions/grid) — Virtualized spreadsheets and data entry
- [Building Extensions](/docs/advanced/extension-dev) — How to package and distribute custom Refast extensions
"""
