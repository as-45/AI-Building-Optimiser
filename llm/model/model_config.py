"""
LLM Model Configuration
"""

from dataclasses import dataclass


@dataclass
class ModelConfig:

    # Official Qwen3 Chat Model
    model_name: str = "Qwen/Qwen3-8B"

    # Generation
    max_new_tokens: int = 512

    temperature: float = 0.2

    top_p: float = 0.9

    do_sample: bool = False

    repetition_penalty: float = 1.05

    # CPU for now
    device: str = "cpu"