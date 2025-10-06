from transformers import pipeline

LOCAL_MODEL = "google/flan-t5-small"  # instruction-tuned
generator = pipeline("text2text-generation", model=LOCAL_MODEL)

def call_llm(prompt: str, max_tokens: int = 150) -> str:
    try:
        result = generator(prompt, max_new_tokens=max_tokens)
        print(result)
        return result[0]["generated_text"]
    except Exception as e:
        return f"[Error] Generation failed: {e}"
