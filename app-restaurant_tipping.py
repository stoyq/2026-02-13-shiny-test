from shiny import ui, render, App
import altair as alt
from palmerpenguins import load_penguins
from shinywidgets import render_altair, output_widget

app_ui = ui.page_fillable(
    ui.panel_title("Restaurant tipping"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="slider",
                label="Bill amount",
                min=0,
                max=100,
                value=[0, 100],
            ),
            ui.layout_columns(
                ui.card(ui.card_header('tip header'), full_screen=True),
                ui.card(ui.card_header('other info'), full_screen=True),
                #col_widths=[12]
                col_widths=[3,9]
            ),
            ui.input_checkbox_group(
                id="checkbox_group",
                label="Food service",
                choices={
                    "Lunch": "Lunch",
                    "Dinner": "Dinner",
                },
                selected=[
                    "Lunch",
                    "Dinner",
                ],
            ),
            ui.input_action_button("action_button", "Reset filter"),
            open="desktop",
        ),
        #...
    ),
)

def server(input, output, session):
    pass

app = App(app_ui, server)