from llm.model.model_loader import ModelLoader

loader = ModelLoader()

model, tokenizer = loader.load()

print("Model Name:")
print(model.config._name_or_path)

print()

print("Vocabulary Size:")
print(tokenizer.vocab_size)

print()

print("Ready for Inference.")