# --------------------------------------------
# Imports at the top - Full Shiny Version
# --------------------------------------------

from shiny import App, ui, reactive, render
import random
from datetime import datetime
import pandas as pd
from plotly import express as px
from scipy.stats import linregress
from collections import deque

# --------------------------------------------
# SET UP THE REACTIVE CONTENT
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 1

# Simulated deque for storing data and a DataFrame for plotting
MAX_DEQUE_LENGTH = 100  # Store up to 100 entries
temp_deque = deque(maxlen=MAX_DEQUE_LENGTH)


@reactive.calc()
def reactive_calc_combined():
    # Simulate temperature and time
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    temp = round(random.uniform(-18, -16), 1)
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Add the new data to the deque
    temp_deque.append({"temp": temp, "timestamp": timestamp})

    # Convert to DataFrame for plotting
    df = pd.DataFrame(temp_deque)

    # Latest dictionary entry
    latest_dictionary_entry = {"temp": temp, "timestamp": timestamp}
    return temp_deque, df, latest_dictionary_entry


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
            align-items: center;
        }
        .location-icon, .message-icon {
            margin-left: 8px;
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
    # Display the selected location directly in the value box
    ui.layout_columns(
        ui.value_box(
            theme="bg-gradient-blue-purple",
            title="Location",
            value=ui.output_ui("display_location_with_icon"),  # Updated to handle HTML
        )
    ),
    ui.hr(),
    # Add the temperature in a custom-styled div with a gradient grey background
    ui.div(
        ui.HTML("<strong>Current Temperature:</strong>"),
        ui.output_text("display_temp"),  # Temperature value
        class_="temperature-box",  # Gradient grey styling
    ),
    # Add the conditional message with right-aligned icons
    ui.output_ui("temp_message"),  # Updated to handle HTML with icons
    # Add the card with the temperature chart
    ui.card(
        ui.card_header("Chart with Current Trend"),
        ui.output_ui("display_plot"),  # Plotly chart as HTML
    ),
)

# ------------------------------------------------
# Define the Server Logic
# ------------------------------------------------


def server(input, output, session):
    @output
    @render.text
    def display_temp():
        """Get the latest reading and return a temperature string"""
        _, _, latest_dictionary_entry = reactive_calc_combined()
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
        _, _, latest_dictionary_entry = reactive_calc_combined()
        return f"{latest_dictionary_entry['timestamp']}"

    @output
    @render.ui
    def display_location_with_icon():
        """Display the selected location with a right-aligned icon."""
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
        _, _, latest_dictionary_entry = reactive_calc_combined()
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

    @output
    @render.ui
    def display_plot():
        """Render the current trend of temperature readings."""
        _, df, _ = reactive_calc_combined()

        # Ensure the DataFrame is not empty before plotting
        if not df.empty:
            # Convert the 'timestamp' column to datetime for better plotting
            df["timestamp"] = pd.to_datetime(
                df["timestamp"], format="%d-%m-%Y %H:%M:%S"
            )

            # Create scatter plot for readings
            fig = px.scatter(
                df,
                x="timestamp",
                y="temp",
                title="Temperature Readings with Regression Line",
                labels={"temp": "Temperature (°C)", "timestamp": "Time"},
                color_discrete_sequence=["blue"],
            )

            # Linear regression - generate regression line
            x_vals = range(len(df))
            y_vals = df["temp"]
            slope, intercept, _, _, _ = linregress(x_vals, y_vals)
            df["best_fit_line"] = [slope * x + intercept for x in x_vals]

            # Add the regression line to the figure
            fig.add_scatter(
                x=df["timestamp"],
                y=df["best_fit_line"],
                mode="lines",
                name="Regression Line",
            )

            # Update layout for better visualization
            fig.update_layout(xaxis_title="Time", yaxis_title="Temperature (°C)")

            # Return the Plotly figure as HTML
            return ui.HTML(fig.to_html(full_html=False))

        return ui.HTML("<div>No data available for plotting.</div>")


# ------------------------------------------------
# Run the App
# ------------------------------------------------

app = App(app_ui, server)
