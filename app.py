# --------------------------------------------
# Imports at the top - Full Shiny Version
# --------------------------------------------

from shiny import App, ui, reactive, render
import random
from datetime import datetime
from faicons import icon_svg

# --------------------------------------------
# SET UP THE REACTIVE CONTENT
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 1


@reactive.calc()
def reactive_calc_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    temp = round(random.uniform(-18, -16), 1)
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    latest_dictionary_entry = {"temp": temp, "timestamp": timestamp}
    return latest_dictionary_entry


# ------------------------------------------------
# Define the Shiny UI Layout Using page_sidebar()
# ------------------------------------------------

# Create the sidebar using ui.sidebar()
sidebar = ui.sidebar(
    ui.h2("Antarctic Explorer", class_="text-center"),
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica in Celsius, Fahrenheit, or Kelvin.",
        class_="text-center",
    ),
    # Use input_radio_buttons for temperature unit selection, adding Kelvin as an option
    ui.input_radio_buttons(
        id="temp_unit",
        label="Select Temperature Unit:",
        choices=["Celsius", "Fahrenheit", "Kelvin"],
        selected="Celsius",
    ),
    # Add a dropdown box (select input) for locations
    ui.input_select(
        id="location",
        label="Select Location:",
        choices=["Palmer Station", "Port Lockroy", "Yelcho Base"],
        selected="Palmer Station",
    ),
)

# Define the full page layout correctly
app_ui = ui.page_sidebar(
    sidebar,
    ui.h2("Current Temperature"),
    ui.output_text("display_temp"),
    ui.p("Could be warmer"),
    # Display poo-storm icon in brown and water icon in blue
    ui.HTML(
        f'<span style="color: #8B4513;">{icon_svg("poo-storm", style="solid")}</span> '
        f'<span style="color: #1E90FF;">{icon_svg("water", style="solid")}</span>'
    ),
    ui.hr(),
    ui.h2("Current Date and Time"),
    ui.output_text("display_time"),
    # Display the selected location
    ui.hr(),
    ui.h2("Selected Location"),
    ui.output_text("display_location"),
)

# ------------------------------------------------
# Define the Server Logic
# ------------------------------------------------


def server(input, output, session):
    @output
    @render.text
    def display_temp():
        """Get the latest reading and return a temperature string"""
        latest_dictionary_entry = reactive_calc_combined()
        temp_celsius = latest_dictionary_entry["temp"]

        # Check the radio button value to determine the unit
        if input.temp_unit() == "Fahrenheit":
            temp_fahrenheit = round((temp_celsius * 9 / 5) + 32, 1)
            return f"{temp_fahrenheit} °F"
        elif input.temp_unit() == "Kelvin":
            temp_kelvin = round(temp_celsius + 273.15, 1)
            return f"{temp_kelvin} K"
        else:
            return f"{temp_celsius} °C"

    @output
    @render.text
    def display_time():
        """Get the latest reading and return a timestamp string"""
        latest_dictionary_entry = reactive_calc_combined()
        return f"{latest_dictionary_entry['timestamp']}"

    @output
    @render.text
    def display_location():
        """Display the selected location"""
        return f"Currently viewing: {input.location()}"


# ------------------------------------------------
# Run the App
# ------------------------------------------------

app = App(app_ui, server)
