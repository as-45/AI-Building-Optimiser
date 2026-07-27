"""Registers EnergyPlus sensor and actuator handles for the runtime."""

import json
from pathlib import Path


class HandleManager:
    """Owns every EnergyPlus API handle used by the controller.

    Actuator definitions live in ``config/runtime_config.json`` so the Python
    control layer and the IDF can be audited together.
    """

    def __init__(self):
        self.initialized = False
        self.variables = {}
        self.actuators = {}

        project_root = Path(__file__).resolve().parent.parent
        with open(project_root / "config" / "runtime_config.json", encoding="utf-8") as file:
            self.config = json.load(file)

    def initialize(self, api, state):
        """Acquire handles after EnergyPlus reports that API data is ready."""
        if self.initialized:
            return

        exchange = api.exchange
        print("\nInitializing EnergyPlus sensor and actuator handles...\n")

        self.variables = {
            "outdoor_temp": exchange.get_variable_handle(
                state, "Site Outdoor Air DryBulb Temperature", "Environment"
            ),
            "outdoor_humidity": exchange.get_variable_handle(
                state, "Site Outdoor Air Relative Humidity", "Environment"
            ),
            "building_power": exchange.get_variable_handle(
                state, "Facility Total Electricity Demand Rate", "Whole Building"
            ),
            "hvac_power": exchange.get_variable_handle(
                state, "Facility Total HVAC Electricity Demand Rate", "Whole Building"
            ),
            "zones": {},
        }

        for zone in self.config["monitored_zones"]:
            self.variables["zones"][zone] = {
                "temperature": exchange.get_variable_handle(state, "Zone Air Temperature", zone),
                "humidity": exchange.get_variable_handle(state, "Zone Air Relative Humidity", zone),
                "predicted_heating": exchange.get_variable_handle(
                    state,
                    "Zone Predicted Sensible Load to Heating Setpoint Heat Transfer Rate",
                    zone,
                ),
                "predicted_cooling": exchange.get_variable_handle(
                    state,
                    "Zone Predicted Sensible Load to Cooling Setpoint Heat Transfer Rate",
                    zone,
                ),
                "actual_heating": exchange.get_variable_handle(
                    state, "Zone Air System Sensible Heating Rate", zone
                ),
                "actual_cooling": exchange.get_variable_handle(
                    state, "Zone Air System Sensible Cooling Rate", zone
                ),
            }

        for name, definition in self.config["actuators"].items():
            handle = exchange.get_actuator_handle(
                state,
                definition["component_type"],
                definition["control_type"],
                definition["actuator_key"],
            )
            if handle == -1:
                raise RuntimeError(
                    f"EnergyPlus actuator handle was not found for {name}: "
                    f"{definition['component_type']} / {definition['control_type']} / "
                    f"{definition['actuator_key']}"
                )
            self.actuators[name] = {"handle": handle, **definition}
            print(f"Actuator ready: {name} ({definition['actuator_key']})")

        self.initialized = True
        print("Handles registered successfully.\n")

    def get(self, name):
        return self.variables[name]

    def get_actuator(self, name):
        if name not in self.actuators:
            available = ", ".join(self.actuators) or "none"
            raise KeyError(f"Unknown actuator '{name}'. Available: {available}")
        return self.actuators[name]
