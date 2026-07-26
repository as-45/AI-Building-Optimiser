"""
memory_schema.py

Defines one building experience.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class BuildingExperience:

    # -----------------------------
    # Metadata
    # -----------------------------

    timestamp: str

    trigger: str

    # -----------------------------
    # Weather
    # -----------------------------

    outdoor_temperature: float

    outdoor_humidity: float

    # -----------------------------
    # Building Summary
    # -----------------------------

    building_power: float

    hvac_power: float

    average_comfort: float

    worst_zone: str

    # -----------------------------
    # Zone Snapshot
    # -----------------------------

    zones: Dict

    # -----------------------------
    # AI Decision
    # -----------------------------

    llm_reasoning: str = ""

    actions: List = field(default_factory=list)

    # -----------------------------
    # Result
    # -----------------------------

    energy_after: float = 0

    comfort_after: float = 0

    carbon_after: float = 0

# Why this schema?

# Every AI memory should answer four questions:

# 1. What happened?
# Outdoor Temp = 24°C

# PMV = 0.9

# Worst Zone = CORE_TOP
# 2. Why did the AI wake up?
# Trigger

# Comfort
# 3. What did the AI do?
# Reduce Cooling Setpoint

# 1°C
# 4. Did it work?
# Energy ↓ 8%

# Comfort ↑ 5%

# This is what allows the AI to learn from previous situations