from dataclasses import dataclass
from typing import List


@dataclass
class Action:

    actuator: str

    current: float

    target: float

    delta: float

    priority: str

    reason: str


@dataclass
class Decision:

    trigger: str

    strategy: str

    confidence: float

    comfort_priority: float

    energy_priority: float

    carbon_priority: float

    why: str

    tradeoffs: List[str]

    actions: List[Action]

    estimated_energy_saving_percent: float

    estimated_carbon_reduction_percent: float

    estimated_comfort_change: str

    assumptions: List[str]