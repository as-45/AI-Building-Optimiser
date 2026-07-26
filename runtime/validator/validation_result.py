from dataclasses import dataclass
from typing import List


@dataclass
class ValidationResult:

    valid: bool

    errors: List[str]