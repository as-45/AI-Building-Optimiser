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
        print(f"\nLoading {self.config.model_name}...\n")
        self.tokenizer = AutoTokenizer.from_pretrained(
        self.config.model_name,
        trust_remote_code=True)

        self.model = AutoModelForCausalLM.from_pretrained(
        self.config.model_name,
        trust_remote_code=True,

        # New API
        dtype=torch.float16,

        # Automatically use GPU if available
        device_map="auto")

        self.model.eval()

        print("✅ Model Loaded Successfully\n")

        return self.model, self.tokenizer