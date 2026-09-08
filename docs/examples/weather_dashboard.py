"""Weather Dashboard Example."""

import random

from refast import Context
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Row,
    Text,
)

CITIES = ["New York", "London", "Tokyo", "Sydney", "Paris"]


def get_random_weather():
    return {
        "temp": random.randint(0, 35),
        "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Snowy"]),
        "humidity": random.randint(30, 90),
    }


async def refresh_data(ctx: Context):
    """Refresh weather data for all cities."""
    weather_data = {city: get_random_weather() for city in CITIES}
    ctx.state.set("weather_data", weather_data)
    await ctx.replace("dashboard-container", render_dashboard(ctx))


def weather_card(city: str, data: dict):
    temp = data["temp"]
    condition = data["condition"]
    humidity = data["humidity"]

    variant = "default"
    if condition == "Sunny":
        variant = "warning"
    elif condition == "Rainy":
        variant = "default"
    elif condition == "Snowy":
        variant = "secondary"

    return Card(
        class_name="w-full shadow-md",
        children=[
            CardHeader(
                children=[
                    Row(
                        justify="between",
                        align="center",
                        children=[CardTitle(city), Badge(condition, variant=variant)],
                    )
                ]
            ),
            CardContent(
                children=[
                    Column(
                        gap=2,
                        children=[
                            Text(f"{temp}°C", class_name="text-4xl font-bold text-primary"),
                            Text(f"Humidity: {humidity}%", class_name="text-muted-foreground text-sm"),
                        ],
                    )
                ]
            ),
        ],
    )


def render_dashboard(ctx: Context):
    weather_data = ctx.state.get("weather_data")

    return Container(
        id="dashboard-container",
        class_name="max-w-6xl mx-auto p-6 space-y-6",
        children=[
            Row(
                justify="between",
                align="center",
                class_name="mb-6",
                children=[
                    Column(
                        children=[
                            Heading("Weather Dashboard", level=1, class_name="text-3xl font-extrabold"),
                            Text("Real-time simulated weather monitoring", class_name="text-muted-foreground text-sm"),
                        ]
                    ),
                    Button("Refresh Data", variant="default", on_click=ctx.callback(refresh_data)),
                ],
            ),
            Container(
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                children=[weather_card(city, weather_data[city]) for city in CITIES],
            ),
        ],
    )


def weather_page(ctx: Context):
    if not ctx.state.get("weather_data"):
        ctx.state.set("weather_data", {city: get_random_weather() for city in CITIES})

    return Container(
        class_name="min-h-screen p-6 bg-background",
        children=[render_dashboard(ctx)],
    )

