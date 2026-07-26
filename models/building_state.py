"""
building_state.py

Defines the live state of the building.
Every module receives this object.
"""

from dataclasses import dataclass


@dataclass
class BuildingState:

    # Simulation

    timestep: int

    # Outdoor

    outdoor_temp: float
    outdoor_humidity: float

    # Power

    hvac_power: float
    building_power: float
    zones: dict

    # -------------------------------------------------

    def to_dict(self):

        return {

            "timestep": self.timestep,

            "outdoor_temp": self.outdoor_temp,

            "outdoor_humidity": self.outdoor_humidity,


            "hvac_power": self.hvac_power,

            "building_power": self.building_power
        }

    # -------------------------------------------------

    def __str__(self):
        output = []

        output.append("\n========== Building State ==========\n")
        output.append(f"Timestep : {self.timestep}")
        output.append(f"Outdoor Temp : {self.outdoor_temp:.2f} °C")
        output.append(f"Outdoor Humidity : {self.outdoor_humidity:.2f} %")
        output.append(f"Building Power : {self.building_power:.2f} W")
        output.append(f"HVAC Power : {self.hvac_power:.2f} W")

        output.append("\n------------- Zones -------------\n")

        for zone in self.zones.values():
            output.append(str(zone))

        output.append("\n==============================")
        return "\n".join(output)