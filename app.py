# --------------------------------------------
# Imports at the top - Full Shiny Version
# --------------------------------------------

from shiny import App, ui, reactive, render
import random
from datetime import datetime

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

# Add Font Awesome CSS to the app
font_awesome_css = ui.tags.head(
    ui.tags.link(
        rel="stylesheet",
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
    ),
    ui.tags.style(
        """
        .location-container, .message-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .location-icon, .message-icon {
            margin-left: 10px;
        }
        .temperature-box {
            background: linear-gradient(to right, #d3d3d3, #808080); /* Gradient grey */
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-size: 1.5em;
            text-align: center;
            margin-top: 10px;
        }
        """
    ),
)

# Create the sidebar using ui.sidebar()
sidebar = ui.sidebar(
    font_awesome_css,  # Include Font Awesome CSS and custom styling
    ui.h2("Antarctic Explorer", class_="text-center"),
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica in Celsius, Fahrenheit, or Kelvin.",
        class_="text-center",
    ),
    # Add the drop-down box (select input) for locations above the radio buttons
    ui.input_select(
        id="location",
        label="Select Location:",
        choices=["Palmer Station", "Port Lockroy", "Yelcho Base"],
        selected="Palmer Station",
    ),
    # Use input_radio_buttons for temperature unit selection, adding Kelvin as an option
    ui.input_radio_buttons(
        id="temp_unit",
        label="Select Temperature Unit:",
        choices=["Celsius", "Fahrenheit", "Kelvin"],
        selected="Celsius",
    ),
    # Add Current Date and Time in the sidebar
    ui.hr(),
    ui.h3("Current Date and Time"),
    ui.output_text("display_time"),
)

# Define the full page layout correctly
app_ui = ui.page_sidebar(
    sidebar,
    # Display Selected Location in a value box above Current Temperature
    ui.h2("Selected Location"),
    ui.layout_columns(
        ui.value_box(
            theme="bg-gradient-blue-purple",
            title="Location",
            value=ui.output_ui("display_location_with_icon"),  # Updated to handle HTML
        )
    ),
    ui.hr(),
    ui.h2("Current Temperature"),
    # Add the temperature in a custom-styled div with a gradient grey background
    ui.div(
        ui.output_text("display_temp"),  # Temperature value
        class_="temperature-box",  # Gradient grey styling
    ),
    # Add the conditional message with right-aligned icons
    ui.output_ui("temp_message"),  # Updated to handle HTML with icons
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
    @render.ui
    def display_location_with_icon():
        """Display the selected location with a right-justified icon."""
        location = input.location()
        if location == "Palmer Station":
            return ui.HTML(
                f"""
                <div class="location-container">
                    <span>{location}</span>
                    <i class="fa-solid fa-flag-usa location-icon" style="color: white;"></i>
                </div>
                """
            )
        elif location == "Port Lockroy":
            return ui.HTML(
                f"""
                <div class="location-container">
                    <span>{location}</span>
                    <i class="fa-solid fa-flag-checkered location-icon" style="color: white;"></i>
                </div>
                """
            )
        elif location == "Yelcho Base":
            return ui.HTML(
                f"""
                <div class="location-container">
                    <span>{location}</span>
                    <i class="fa-regular fa-flag location-icon" style="color: white;"></i>
                </div>
                """
            )
        return ui.HTML(location)

    @output
    @render.ui
    def temp_message():
        """Return a message with an icon based on the current temperature."""
        latest_dictionary_entry = reactive_calc_combined()
        temp_celsius = latest_dictionary_entry["temp"]

        if temp_celsius > -17:
            # Micro Heatwave with red sun icon
            return ui.HTML(
                f"""
                <div class="message-container">
                    <span>Micro Heatwave</span>
                    <i class="fa-regular fa-sun message-icon" style="color: red;"></i>
                </div>
                """
            )
        else:
            # Could be Warmer with blue snowflake icon
            return ui.HTML(
                f"""
                <div class="message-container">
                    <span>Could be Warmer</span>
                    <i class="fa-solid fa-snowflake message-icon" style="color: blue;"></i>
                </div>
                """
            )


# ------------------------------------------------
# Run the App
# ------------------------------------------------

app = App(app_ui, server)
