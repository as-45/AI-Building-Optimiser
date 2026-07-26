"""
Inference Engine

Runs prompts through Qwen3-8B and returns generated text.
"""

import torch

from llm.model.model_loader import ModelLoader


class InferenceEngine:

    def __init__(self):

        loader = ModelLoader()

        self.model, self.tokenizer = loader.load()

    # ----------------------------------------

    def generate(
        self,
        prompt: str,
        max_new_tokens=512
    ):

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        )

        device = next(self.model.parameters()).device

        inputs = {
            k: v.to(device)
            for k, v in inputs.items()
        }

        with torch.no_grad():

            outputs = self.model.generate(

                **inputs,

                max_new_tokens=max_new_tokens,

                do_sample=False,

                temperature=0.2,

                top_p=0.9,

                repetition_penalty=1.05

            )

        generated = self.tokenizer.decode(

            outputs[0],

            skip_special_tokens=True

        )

        return generated