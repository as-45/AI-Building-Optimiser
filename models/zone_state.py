"""
zone_state.py
"""

from dataclasses import dataclass


@dataclass
class ZoneState:

    name: str

    temperature: float

    humidity: float

    predicted_heating_load: float

    predicted_cooling_load: float

    actual_heating_rate: float

    actual_cooling_rate: float

    # -------- PMV --------

    pmv: float = None

    ppd: float = None

    thermal_sensation: str = ""

    comfort_level: str = ""

    comfort_score: float = 0.0

    def __str__(self):

        return (

            f"{self.name:25s}"

            f"T={self.temperature:6.2f}°C  "

            f"RH={self.humidity:6.2f}%  "

            f"PMV={self.pmv:5.2f}  "

            f"PPD={self.ppd:6.2f}%  "

            f"{self.comfort_level}"

        )