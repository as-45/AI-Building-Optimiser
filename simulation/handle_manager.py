"""
handle_manager.py

Registers all EnergyPlus variable handles.
Supports multiple monitored zones.
"""

import json
from pathlib import Path


class HandleManager:

    def __init__(self):

        self.initialized = False

        self.variables = {}

        project_root = Path(__file__).resolve().parent.parent

        with open(project_root / "config" / "runtime_config.json") as f:

            self.config = json.load(f)

    # -----------------------------------------------------

    def initialize(self, api, state):

        if self.initialized:
            return

        exchange = api.exchange

        print("\nInitializing Handles...\n")

        # -----------------------------
        # Outdoor Variables
        # -----------------------------

        self.variables["outdoor_temp"] = exchange.get_variable_handle(

            state,

            "Site Outdoor Air DryBulb Temperature",

            "Environment"

        )

        self.variables["outdoor_humidity"] = exchange.get_variable_handle(

            state,

            "Site Outdoor Air Relative Humidity",

            "Environment"

        )

        self.variables["building_power"] = exchange.get_variable_handle(

            state,

            "Facility Total Electricity Demand Rate",

            "Whole Building"

        )

        self.variables["hvac_power"] = exchange.get_variable_handle(

            state,

            "Facility Total HVAC Electricity Demand Rate",

            "Whole Building"

        )

        # -----------------------------
        # Zone Variables
        # -----------------------------

        self.variables["zones"] = {}

        for zone in self.config["monitored_zones"]:
            self.variables["zones"][zone] = {
                "temperature":
                exchange.get_variable_handle(state,
                "Zone Air Temperature",
                zone
        ),

                "humidity":
                exchange.get_variable_handle(state,
                "Zone Air Relative Humidity",
                zone
        ),

    # Predicted Loads
                "predicted_heating":
                exchange.get_variable_handle(state,
                "Zone Predicted Sensible Load to Heating Setpoint Heat Transfer Rate",
                zone
        ),

                "predicted_cooling":
                exchange.get_variable_handle(state,
                "Zone Predicted Sensible Load to Cooling Setpoint Heat Transfer Rate",
                zone
        ),

    # Actual HVAC Rates
                "actual_heating":
                exchange.get_variable_handle(state,
                "Zone Air System Sensible Heating Rate",
                zone
        ),

                "actual_cooling":
                exchange.get_variable_handle(
                state,
                "Zone Air System Sensible Cooling Rate",
                zone
        )

}

        self.initialized = True

        print("Handles Registered Successfully.")

    # -----------------------------------------------------

    def get(self, name):

        return self.variables[name]