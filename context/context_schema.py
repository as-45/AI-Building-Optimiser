"""
Defines everything that will be sent to the Prompt Builder.
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Context:

    current_state: Dict

    trend_report: Dict

    retrieved_memories: List

    trigger: Dict

    weather: Dict

    objectives: Dict