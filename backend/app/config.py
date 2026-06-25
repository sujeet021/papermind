from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "llama3.2:3b"          # via Ollama
    ollama_host: str = "http://localhost:11434"
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k: int = 5
    index_dir: str = "./data/index"
    score_threshold: float = 0.35           # min similarity to ground answers

    class Config:
        env_file = ".env"

settings = Settings()