# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "plotly==6.0.1",
#     "pandas==2.2.3",
#     "numpy==2.2.5",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import plotly.express as px
    from marimo import ui
    import marimo as mo

    # Create sample data
    np.random.seed(42)
    cities = ["New York", "San Francisco", "Chicago"]
    base_temps = {"New York": 45, "San Francisco": 60, "Chicago": 40}
    dates = pd.date_range(start="2024-01-01", periods=10, freq="D")

    # Create a DataFrame
    data = pd.DataFrame(
        [
            {"Date": date, "City": city, "Temperature": base_temps[city] + temp}
            for city in cities
            for date, temp in zip(dates, np.random.normal(0, 5, len(dates)))
        ]
    )
    data
    return cities, data, mo, px, ui


@app.cell
def _(cities, mo, ui):
    city_selector = ui.multiselect(
        cities, label="Select Cities", value=["New York", "San Francisco"]
    )

    mo.md(f"Choose a city: {city_selector}")
    return (city_selector,)


@app.cell
def _(mo, ui):
    chart_type = ui.dropdown(["Line", "Bar"], label="Chart Type", value="Line")

    mo.md(f"Choose a chart type: {chart_type}")
    return (chart_type,)


@app.cell
def _(chart_type, city_selector, data, px):
    # Filter data for selected cities
    plot_data = data[data["City"].isin(city_selector.value)]

    # Create plot based on selection
    if chart_type.value == "Line":
        fig = px.line(
            plot_data,
            x="Date",
            y="Temperature",
            color="City",
            title="Temperature Trends",
        )
    else:
        fig = px.bar(
            plot_data,
            x="Date",
            y="Temperature",
            color="City",
            title="Daily Temperatures",
            barmode="group",
        )
    fig
    return


@app.cell
def _(city_selector, data, mo):
    # Simple summary statistics
    stats = (
        data[data["City"].isin(city_selector.value)]
        .groupby("City")["Temperature"]
        .agg(["mean", "min", "max"])
        .round(1)
    )

    # Format stats for display
    stats_md = "### Summary Statistics\n\n"
    for city in city_selector.value:
        city_stats = stats.loc[city]
        stats_md += f"**{city}**: {city_stats['mean']}°F (avg), range: {city_stats['min']}°F - {city_stats['max']}°F\n\n"
    mo.md(stats_md)

    return


if __name__ == "__main__":
    app.run()
