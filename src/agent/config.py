from pydantic import BaseModel
import os

class Settings(BaseModel):
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    temperature: float = 0.2
    max_context_chars: int = 6000

def load_settings() -> Settings:
    return Settings(
        ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434").strip(),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b").strip(),
        temperature=float(os.getenv("TEMPERATURE", "0.2").strip()),
        max_context_chars=int(os.getenv("MAX_CONTEXT_CHARS", "6000").strip()),
    )
