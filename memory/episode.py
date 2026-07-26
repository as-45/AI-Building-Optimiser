"""
episode.py

Represents one complete building episode.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Episode:

    episode_id: str

    start_time: str

    end_time: str

    trigger: str

    summary: str

    average_outdoor_temp: float

    average_building_power: float

    average_hvac_power: float

    average_comfort: float

    worst_zone: str

    actions: List = field(default_factory=list)

    outcome: str = ""