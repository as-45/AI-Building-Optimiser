from dataclasses import dataclass
from typing import List


@dataclass
class ExecutionResult:

    success: bool

    applied_actions: List[str]

    errors: List[str]