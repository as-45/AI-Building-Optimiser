"""
Loads the Qwen model and tokenizer.
"""

import torch

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

from llm.model.model_config import ModelConfig


class ModelLoader:

    def __init__(self, config=None):

        self.config = config or ModelConfig()

        self.model = None
        self.tokenizer = None

    # -------------------------------------------------

    def load(self):

        print("\nLoading Qwen3-8B...\n")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_name,
            trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            trust_remote_code=True,
            torch_dtype=torch.float32
        )

        self.model.eval()

        print("✅ Model Loaded Successfully\n")

        return self.model, self.tokenizer