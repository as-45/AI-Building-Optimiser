"""
Represents trend analysis results.
"""

from dataclasses import dataclass


@dataclass
class TrendReport:

    temperature_trend: str

    humidity_trend: str

    hvac_trend: str

    power_trend: str

    comfort_trend: str

    carbon_trend: str

    predicted_power: float

    predicted_hvac: float

    predicted_comfort: float