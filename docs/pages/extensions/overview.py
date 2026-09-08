"""Extensions Overview — /docs/extensions."""

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
    Grid,
    Heading,
    Icon,
    Markdown,
    Row,
    Separator,
    Text,
)

PAGE_TITLE = "Extensions Overview"
PAGE_ROUTE = "/docs/extensions"


def render(ctx):
    """Render the extensions ecosystem overview page."""
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
                            Badge("Ecosystem", variant="secondary"),
                            Badge("Plugins", variant="outline"),
                        ],
                    ),
                    Heading(PAGE_TITLE, level=1),
                    Text(
                        "Extend Refast applications with custom React components, third-party libraries, and rich visualizations.",
                        class_name="text-lg text-muted-foreground",
                    ),
                ],
            ),
            Separator(),
            # Extension Cards
            Grid(
                columns="repeat(auto-fit, minmax(260px, 1fr))",
                gap=6,
                children=[
                    _extension_card(
                        ctx=ctx,
                        title="refast-echarts",
                        tag="Visualization",
                        icon="bar-chart-2",
                        description="Interactive Apache ECharts 5 integration with 20+ chart types, real-time updates via setOption, mouse event callbacks, and dark/light themes.",
                        route="/docs/extensions/echarts",
                        pip="pip install refast-echarts",
                    ),
                    _extension_card(
                        ctx=ctx,
                        title="refast_grid",
                        tag="Data & Spreadsheet",
                        icon="grid-3x3",
                        description="Excel-like data grid and spreadsheet component based on Silevis ReactGrid. Features cell editing, sticky rows/cols, virtualized scrolling, and 15+ cell types.",
                        route="/docs/extensions/grid",
                        pip="pip install refast_grid",
                    ),
                    _extension_card(
                        ctx=ctx,
                        title="refast_vtk_js",
                        tag="3D Graphics & SciViz",
                        icon="box",
                        description="High-performance 3D visualization powered by Kitware react-vtk-js. Supports polygonal meshes, volumetric medical rendering, filters, and 3D picking.",
                        route="/docs/extensions/vtk-js",
                        pip="pip install refast-vtk-js",
                    ),
                ],
            ),
            Separator(),
            Markdown(content=CONTENT, enable_mermaid=True),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


def _extension_card(ctx, title: str, tag: str, icon: str, description: str, route: str, pip: str):
    """Render a card highlighting an extension."""
    async def _navigate(c):
        await c.load(route)

    return Card(
        class_name="flex flex-col justify-between hover:border-primary/50 transition-colors",
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
                                    Icon(icon, class_name="text-primary h-5 w-5"),
                                    CardTitle(title, class_name="text-lg"),
                                ],
                            ),
                            Badge(tag, variant="secondary", class_name="text-xs"),
                        ],
                    ),
                    CardDescription(description, class_name="pt-2 text-sm leading-relaxed"),
                ],
            ),
            CardContent(
                class_name="pt-0 space-y-3",
                children=[
                    Container(
                        class_name="bg-muted/60 rounded px-2.5 py-1.5 font-mono text-xs text-muted-foreground",
                        children=[Text(pip)],
                    ),
                    Button(
                        "View Documentation →",
                        variant="outline",
                        size="sm",
                        class_name="w-full",
                        on_click=ctx.callback(_navigate),
                    ),
                ],
            ),
        ],
    )


CONTENT = r"""
## How Extensions Work

Refast extensions package React frontend components, static assets (JS and CSS bundles), and Python wrappers into distributed Python packages. Once installed, they integrate directly into Refast's server-driven UI architecture.

```mermaid
graph LR
    subgraph Python Environment
        App[RefastApp] --> Discovery[Auto-Discovery / Entry Points]
        Discovery --> ExtClass[Extension Class]
        ExtClass --> PyComp[Python Component API]
    end

    subgraph Browser Client
        Shell[HTML Shell] --> RefastClient[window.RefastClient]
        RefastClient --> ExtJS[Extension Bundle: /static/ext/...]
        ExtJS --> Registry[ComponentRegistry.register]
    end

    PyComp -.-> |JSON serialization| Registry
```

---

## 1. Auto-Discovery via Entry Points

Extensions use standard Python packaging entry points under the `refast.extensions` group in their `pyproject.toml`:

```toml
[project.entry-points."refast.extensions"]
refast_echarts = "refast_echarts:EchartsExtension"
refast_grid = "refast_grid:RefastGridExtension"
refast_vtk_js = "refast_vtk_js:VtkExtension"
```

When you start your `RefastApp`:

1. Refast automatically scans installed packages for `refast.extensions` entry points.
2. It discovers the extension class and registers its static assets.
3. Extension scripts and styles are automatically injected into the HTML shell.
4. Python components can be imported and used immediately—no manual configuration required!

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container
# Simply import components from the installed extension
from refast_echarts import ECharts

ui = RefastApp(title="My Dashboard")

@ui.page("/")
def home(ctx: Context):
    return Container(
        children=[
            ECharts(
                option={
                    "xAxis": {"data": ["Q1", "Q2", "Q3", "Q4"]},
                    "yAxis": {},
                    "series": [{"type": "bar", "data": [54, 86, 92, 110]}],
                },
                height="350px",
            ),
        ]
    )
```

---

## 2. Manual Extension Registration

If you prefer to disable auto-discovery or want explicit control over loaded extensions:

```python
from refast import RefastApp
from refast_echarts import ECharts, EchartsExtension
from refast_grid import RefastGrid, RefastGridExtension

ui = RefastApp(
    title="Custom Dashboard",
    auto_discover_extensions=False,
    extensions=[
        EchartsExtension(),
        RefastGridExtension(),
    ],
)
```

---

## 3. Asset Serving and Loading Order

Refast guarantees a deterministic asset loading order:

1. **`refast-client.css`**: Core Tailwind theme tokens and base styles.
2. **Extension CSS files**: Served at `/static/ext/{extension_name}/{filename}.css`.
3. **`refast-client.js`**: Core client runtime, establishing `window.RefastClient` and `ComponentRegistry`.
4. **Extension JavaScript files**: Served at `/static/ext/{extension_name}/{filename}.js`.

Because extension scripts load after `window.RefastClient`, extension components register cleanly into the registry without race conditions:

```javascript
// Inside extension bundle
const { componentRegistry } = window.RefastClient;
componentRegistry.register('ECharts', EChartsReactComponent);
```

---

## 4. Ecosystem Comparison

| Extension | Primary Use Case | Underlying Technology | Key Strengths |
|---|---|---|---|
| [**`refast-echarts`**](/docs/extensions/echarts) | Business intelligence, data charts, dashboards | [Apache ECharts 5](https://echarts.apache.org/) | 20+ chart types, smooth transitions, `setOption` bound method, light/dark mode |
| [**`refast_grid`**](/docs/extensions/grid) | Spreadsheets, financial tables, hierarchical data | [Silevis ReactGrid](https://reactgrid.com/) | Keyboard navigation, cell editing, sticky headers/totals, 15+ custom cell types |
| [**`refast_vtk_js`**](/docs/extensions/vtk-js) | 3D graphics, scientific computing, CAD, medical imaging | [Kitware VTK.js](https://kitware.github.io/vtk-js/) | WebGL hardware acceleration, volume rendering, 3D mouse picking, synced multi-views |

---

## Next Steps

- Explore [**refast-echarts**](/docs/extensions/echarts) for charts and data visualization
- Explore [**refast_grid**](/docs/extensions/grid) for interactive spreadsheets and data editing
- Explore [**refast_vtk_js**](/docs/extensions/vtk-js) for 3D surfaces and volumetric rendering
- Read [**Building Extensions**](/docs/advanced/extension-dev) to learn how to create and publish your own extension
"""

