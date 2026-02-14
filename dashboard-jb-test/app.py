from pathlib import Path
from shiny import App, render, ui, reactive
from shinywidgets import render_widget, output_widget
import pandas as pd
import ipyleaflet as L

# Load data
data_path = Path(__file__).parent.parent / "data" / "raw" / "gbif-beetle.csv"
if data_path.exists():
    df = pd.read_csv(data_path, sep="\t", low_memory=False)
else:
    df = pd.DataFrame({
        "year": [2000, 2005, 2010, 2015, 2020],
        "stateProvince": ["Ontario", "Ohio", "Michigan", "Ontario", "Ohio"],
        "basisOfRecord": ["HUMAN_OBSERVATION", "HUMAN_OBSERVATION", "MACHINE_OBSERVATION", "HUMAN_OBSERVATION", "MACHINE_OBSERVATION"],
        "decimalLatitude": [43.65, 40.42, 42.73, 44.23, 39.96],
        "decimalLongitude": [-79.38, -82.91, -84.55, -76.50, -83.00],
    })

# UI
app_ui = ui.page_fluid(
    ui.panel_title("Japanese Beetle — Invasive Species Tracker"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="year_range",
                label="Year Range",
                min=int(df["year"].min()),
                max=int(df["year"].max()),
                value=[int(df["year"].min()), int(df["year"].max())],
                sep="",
            ),
            ui.input_selectize(
                id="region",
                label="Region",
                choices=["All"] + sorted(df["stateProvince"].dropna().unique().tolist()),
                selected="All",
            ),
            ui.input_radio_buttons(
                id="obs_type",
                label="Observation Type",
                choices={
                    "All": "All Observations",
                    "HUMAN_OBSERVATION": "Research Grade",
                    "MACHINE_OBSERVATION": "Machine Observation",
                },
                selected="All",
            ),
            open="desktop",
        ),
        # Summary value boxes
        ui.layout_columns(
            ui.value_box("Total Observations", ui.output_text("total_obs")),
            ui.value_box("First Recorded", ui.output_text("first_recorded")),
            ui.value_box("Status in Region", ui.output_text("status")),
            fill=False,
        ),
        # Map placeholder
        ui.layout_columns(
            ui.card(
                ui.card_header("Geographic Distribution Map"),
                output_widget("map"),
                full_screen=True,
            ),
        ),
        # Bottom row: time series + pie chart
        ui.layout_columns(
            ui.card(
                ui.card_header("Occurrences Over Time"),
                "Placeholder: Time series chart will go here",
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Basis of Record"),
                "Placeholder: Pie chart of record types will go here",
                full_screen=True,
            ),
            col_widths=[6, 6],
        ),
    ),
)


# Server
def server(input, output, session):

    @reactive.calc
    def filtered_data():
        data = df.copy()
        data = data[data["year"].between(input.year_range()[0], input.year_range()[1])]
        if input.region() != "All":
            data = data[data["stateProvince"] == input.region()]
        if input.obs_type() != "All":
            data = data[data["basisOfRecord"] == input.obs_type()]
        return data

    @render_widget
    def map():
        return L.Map(center=(39, -98), zoom=4, layout={"height": "450px"})

    @render.text
    def total_obs():
        return f"{filtered_data().shape[0]:,}"

    @render.text
    def first_recorded():
        return str(int(filtered_data()["year"].min()))

    @render.text
    def status():
        if filtered_data().shape[0] > 0:
            return "Present"
        return "Not detected"


# Create app
app = App(app_ui, server)
