from transformers import pipeline

# Load a local or downloaded model
generator = pipeline("text-generation", model="distilgpt2")

prompt = "Once upon a time, in a distant kingdom,"

result = generator(prompt, max_new_tokens=50, do_sample=True)
print(result[0]["generated_text"])
