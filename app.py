# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

# From shiny, import just reactive and render
from shiny import reactive, render

# From shiny.express, import just ui
from shiny.express import ui

# Imports from Python Standard Library to simulate live data
import random
from datetime import datetime

# --------------------------------------------
# Optional: Import font awesome icons as you like
# --------------------------------------------

from faicons import icon_svg

# --------------------------------------------
# FOR OPTIONAL LOCAL DEVELOPMENT
# --------------------------------------------

# Add all packages not in the Std Library
# to requirements.txt ONLY when working locally:
#
# faicons
# shiny
# shinylive
# 
# And install them into an active project virtual environment (usually in .venv)
# --------------------------------------------

