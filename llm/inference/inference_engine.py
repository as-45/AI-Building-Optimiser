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

    def generate(self, prompt: str, max_new_tokens=512):
        
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        ).to(self.model.device)

        with torch.no_grad():

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated = self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True
        )

        return generated.strip()