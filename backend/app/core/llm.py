import ollama
from app.config import settings

client = ollama.Client(host=settings.ollama_host)

def generate(prompt: str, system: str) -> str:
    resp = client.chat(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        options={"temperature": 0.1},
    )
    return resp["message"]["content"].strip()