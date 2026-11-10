# Component Reference Section — Agent Instructions

## Section Goal

Provide a **complete API reference** for every UI component in Refast. Each page covers
a group of related components with props tables, code examples, and live rendered demos.

---

## Format for Each Component

For every component on a page, include:

1. **Heading** (h3) with the component name
2. **One-sentence description** of what it renders
3. **Code example** as a Markdown code block showing typical usage
4. **Props table** with columns: Prop | Type | Default | Description
5. **Live rendered example** using actual Refast components (not just code)
6. **Notes** about variants, sizes, or special behaviors

### Props Table Template

```markdown
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | (positional) | Button text |
| `variant` | `"default" \| "secondary"` | `"default"` | Visual variant |
```

### Live Example Pattern

After the code block, embed the actual component:

```python
# In render():
Column(gap=4, children=[
    Heading("Button", level=3),
    Markdown(content="...code and props table..."),
    # Live demo
    Card(class_name="p-4", children=[
        Row(gap=2, children=[
            Button("Default"),
            Button("Secondary", variant="secondary"),
            Button("Destructive", variant="destructive"),
            Button("Ghost", variant="ghost"),
        ]),
    ]),
])
```

---

## Pages

> Each component now has its **own module** inside the group folder below
> (e.g. `pages/components/buttons/button.py`), and pages are discovered
> automatically by `pages/components/registry.py` from their `PAGE_METADATA`
> dict (`title`, `route`, `icon`, `group`, `order`). No `app.py` edit is needed
> to add a component page — but a page without `PAGE_METADATA` silently lands in
> the "Utility" group, so always declare it.

### 1. `components/layout/*.py` — Layout Components (group `Layout`, e.g. `/docs/components/container`)

**Read:** `src/refast/components/base.py`, `src/refast/components/shadcn/layout.py`

**Components to document:**
- `Container` — div wrapper (id, class_name, children, style)
- `Flex` — flexbox (direction, align, justify, gap, wrap)
- `Row` — Flex shortcut for direction="row"
- `Column` — Flex shortcut for direction="column"
- `Grid` — CSS grid (columns, gap)
- `Center` — Centers children
- `Box` — Generic container
- `Separator` — Horizontal/vertical divider (orientation)
- `AspectRatio` — Fixed aspect ratio container (ratio)
- `ScrollArea` / `ScrollBar` — Custom scrollable area
- `ResizablePanelGroup` / `ResizablePanel` / `ResizableHandle` — Split panes (direction, sizes)

---

### 2. `components/typography/*.py` — Typography (group `Typography`, e.g. `/docs/components/text`)

**Read:** `src/refast/components/shadcn/typography.py`

**Components to document:**
- `Heading` — h1-h6 (text, level)
- `Text` — inline span (text, class_name)
- `Paragraph` — block p (text)
- `Code` — inline code (text)
- `Link` — hyperlink (text, href, target)
- `Markdown` — rich text with GFM, syntax highlighting, KaTeX (text)
- `Label` — form label (text, html_for)
- `Badge` — status indicator (text, variant)
- `Kbd` — keyboard shortcut display (text)

---

### 3. `components/buttons/*.py` — Buttons & Actions (group `Buttons & Actions`, e.g. `/docs/components/button`)

**Read:** `src/refast/components/shadcn/button.py`, `src/refast/components/shadcn/controls.py`, `src/refast/components/shadcn/overlay.py`

**Components to document:**
- `Button` — variants (default, secondary, destructive, outline, ghost, link), sizes (default, sm, lg, icon), icon, disabled, on_click
- `IconButton` — icon-only button
- `Toggle` — pressed/unpressed toggle (pressed, on_pressed_change, variant)
- `ToggleGroup` / `ToggleGroupItem` — group of toggles (type single/multiple)
- `DropdownMenu` / `DropdownMenuTrigger` / `DropdownMenuContent` / `DropdownMenuItem` / `DropdownMenuLabel` / `DropdownMenuSeparator` / `DropdownMenuCheckboxItem` / `DropdownMenuRadioGroup` / `DropdownMenuRadioItem` / `DropdownMenuSub` / `DropdownMenuSubTrigger` / `DropdownMenuSubContent`
- `ContextMenu` / `ContextMenuTrigger` / `ContextMenuContent` / `ContextMenuItem` / `ContextMenuSeparator` / `ContextMenuCheckboxItem`

---

### 4. `components/form_inputs/*.py` — Form Inputs (group `Form Inputs`, e.g. `/docs/components/input`)

**Read:** `src/refast/components/shadcn/input.py`, `src/refast/components/shadcn/form.py`, `src/refast/components/shadcn/controls.py`

**Components to document:**
- `Input` — text input (placeholder, value, type, on_change, store_as, disabled)
- `InputWrapper` — input with label and description
- `Textarea` — multi-line (placeholder, value, rows, on_change, store_as)
- `Select` — dropdown (options, placeholder, value, on_value_change, store_as)
- `Checkbox` — single checkbox (label, checked, on_checked_change)
- `CheckboxGroup` — grouped checkboxes
- `Radio` / `RadioGroup` — radio selection (options, value, on_value_change)
- `Switch` — toggle switch (checked, on_checked_change, label)
- `Slider` — range slider (min, max, step, value, on_value_change)
- `DatePicker` — date selection
- `Combobox` — searchable select (options, placeholder, on_value_change)
- `InputOTP` / `InputOTPGroup` / `InputOTPSlot` / `InputOTPSeparator` — OTP input
- `Form` / `FormField` — form wrapper
- `Label` — form label

---

### 5. `components/cards/*.py` — Cards & Containers (group `Cards & Containers`, e.g. `/docs/components/card`)

**Read:** `src/refast/components/shadcn/card.py`, `src/refast/components/shadcn/utility.py`

**Components to document:**
- `Card` — bordered container
- `CardHeader` — card header section
- `CardTitle` — card title
- `CardDescription` — card subtitle
- `CardContent` — card body
- `CardFooter` — card footer
- `Collapsible` / `CollapsibleTrigger` / `CollapsibleContent` — expandable section

---

### 6. `components/data_display/*.py` — Data Display (group `Data Display`, e.g. `/docs/components/table`)

**Read:** `src/refast/components/shadcn/data_display.py`, `src/refast/components/shadcn/controls.py`

**Components to document:**
- `Table` / `TableHeader` / `TableBody` / `TableRow` / `TableHead` / `TableCell`
- `DataTable` — higher-level table (document if functional, note if not)
- `Avatar` — user avatar (src, alt, fallback)
- `Image` — responsive image (src, alt)
- `List` — ordered/unordered list
- `Calendar` — date calendar
- `Progress` — progress bar (value, max)
- `Skeleton` — loading placeholder (variant)
- `Carousel` / `CarouselContent` / `CarouselItem` / `CarouselPrevious` / `CarouselNext`
- `Accordion` / `AccordionItem` / `AccordionTrigger` / `AccordionContent` — (type single/multiple, collapsible)
- `Tabs` / `TabItem` — tabbed sections (default_value)
- `HoverCard` / `HoverCardTrigger` / `HoverCardContent`
- `Tooltip` — hover tooltip (content, side)

---

### 7. `components/navigation/*.py` — Navigation (group `Navigation`, e.g. `/docs/components/sidebar-nav`)

**Read:** `src/refast/components/shadcn/navigation.py`

**Components to document:**
- All Breadcrumb components
- All NavigationMenu components
- All Pagination components
- All Menubar components
- All Command components (command palette)
- All Sidebar components (22+ sub-components)

**Reference examples:** `examples/sidebar_showcase/app.py`, `examples/navigation_showcase/app.py`

---

### 8. `components/feedback/*.py` — Feedback & Overlay (group `Feedback & Overlay`, e.g. `/docs/components/alert`)

**Read:** `src/refast/components/shadcn/feedback.py`, `src/refast/components/shadcn/overlay.py`

**Components to document:**
- `Alert` — info/error alert (title, description, variant)
- `Spinner` — loading spinner (size)
- `Progress` — progress bar
- `Skeleton` — loading placeholder
- All Dialog components
- All Sheet components (side: top/right/bottom/left)
- All Drawer components
- All Popover components
- `Tooltip`
- `LoadingOverlay`

---

### 9. `components/charts/*.py` — Charts (group `Charts`, e.g. `/docs/components/bar-chart`)

**Read:** `src/refast/components/shadcn/charts.py`, `examples/charts_showcase/app.py`

**Components to document:**
- `ChartContainer` + `ChartConfig` + `ChartColor`
- `BarChart` + `Bar`
- `LineChart` + `Line`
- `AreaChart` + `Area`
- `PieChart` + `Pie` + `Cell`
- `RadarChart` + `Radar`
- `RadialChart` + `RadialBar`
- `ScatterChart` + `Scatter`
- Shared: `XAxis`, `YAxis`, `CartesianGrid`, `PolarGrid`, `PolarAngleAxis`, `PolarRadiusAxis`
- `ChartTooltip` / `ChartTooltipContent`
- `ChartLegend` / `ChartLegendContent`
- `ReferenceLine`

**Live demos:** Include at least one working chart per type

---

### 10. `components/utility/*.py` — Utility (group `Utility`, e.g. `/docs/components/icon`)

**Read:** `src/refast/components/shadcn/icon.py`, `src/refast/components/shadcn/utility.py`, `src/refast/components/slot.py`

**Components to document:**
- `Icon` — Lucide icon (name, size). List all available icon names.
- `ThemeSwitcher` — light/dark/system toggle
- `ConnectionStatus` — WebSocket connection indicator
- `Slot` — dynamic content placeholder (id, fallback)
- `Empty` — renders nothing
- `LoadingOverlay` — full-screen loading overlay
- `Kbd` — keyboard shortcut display
