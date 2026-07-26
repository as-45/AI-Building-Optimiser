from llm.inference.inference_engine import InferenceEngine


engine = InferenceEngine()

prompt = """
You are an AI building management assistant.

Outdoor temperature : 34 C
Indoor temperature : 29 C
Occupancy : High
Electricity price : High

Recommend actions.
"""

response = engine.generate(prompt)

print("\n========================\n")

print(response)

print("\n========================\n")