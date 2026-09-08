"""Centralized registration for standalone runnable example routes."""

from refast import Context, RefastApp


def register_example_routes(ui: RefastApp):
    """Register all standalone example routes with the Refast app."""

    @ui.page("/examples/hello")
    def page_examples_hello(ctx: Context):
        from docs.examples.hello import hello_world_page
        return hello_world_page(ctx)

    @ui.page("/examples/counter")
    def page_examples_counter(ctx: Context):
        from docs.examples.basic_counter import counter_page
        return counter_page(ctx)

    @ui.page("/examples/form-validation")
    def page_examples_form_validation(ctx: Context):
        from docs.examples.form_validation import form_validation_page
        return form_validation_page(ctx)

    @ui.page("/examples/all-inputs")
    def page_examples_all_inputs(ctx: Context):
        from docs.examples.all_inputs import all_inputs_page
        return all_inputs_page(ctx)

    @ui.page("/examples/input-features")
    def page_examples_input_features(ctx: Context):
        from docs.examples.input_features import input_features_page
        return input_features_page(ctx)

    @ui.page("/examples/multi-page")
    def page_examples_multi_page(ctx: Context):
        from docs.examples.multi_page import multi_page_demo
        return multi_page_demo(ctx)

    @ui.page("/examples/weather")
    def page_examples_weather(ctx: Context):
        from docs.examples.weather_dashboard import weather_page
        return weather_page(ctx)

    @ui.page("/examples/resizable-panels")
    def page_examples_resizable_panels(ctx: Context):
        from docs.examples.resizable_panels import resizable_panels_page
        return resizable_panels_page(ctx)

    @ui.page("/examples/markdown-features")
    def page_examples_markdown_features(ctx: Context):
        from docs.examples.markdown_features import markdown_features_page
        return markdown_features_page(ctx)

    @ui.page("/examples/scroll-stream")
    def page_examples_scroll_stream(ctx: Context):
        from docs.examples.scroll_stream import scroll_stream_page
        return scroll_stream_page(ctx)

    @ui.page("/examples/kanban")
    def page_examples_kanban(ctx: Context):
        from docs.examples.kanban_board import kanban_board_page
        return kanban_board_page(ctx)

    @ui.page("/examples/settings-panel")
    def page_examples_settings_panel(ctx: Context):
        from docs.examples.settings_panel import settings_panel_page
        return settings_panel_page(ctx)

    @ui.page("/examples/echarts")
    def page_examples_echarts(ctx: Context):
        from docs.examples.echarts_example import echarts_page
        return echarts_page(ctx)

    @ui.page("/examples/grid")
    def page_examples_grid(ctx: Context):
        from docs.examples.grid_example import grid_page
        return grid_page(ctx)

    @ui.page("/examples/vtk-js")
    def page_examples_vtk(ctx: Context):
        from docs.examples.vtk_example import vtk_page
        return vtk_page(ctx)

    @ui.page("/examples/event-modifiers")
    def page_examples_event_modifiers(ctx: Context):
        from docs.examples.event_modifiers import event_modifiers_page
        return event_modifiers_page(ctx)


