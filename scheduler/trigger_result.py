from dataclasses import dataclass


@dataclass
class TriggerResult:

    invoke_llm: bool

    trigger_name: str

    priority: str

    confidence: float

    reason: str