from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class LLMResult:
    text: str
    latency_s: float


class OllamaClient:
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3.1:8b", temperature: float = 0.2):
        self.host = host.rstrip("/")
        self.model = model
        self.temperature = temperature

    def chat(self, user: str, system: Optional[str] = None) -> LLMResult:
        payload = {
            "model": self.model,
            "messages": [],
            "options": {"temperature": self.temperature},
            "stream": False,
        }
        if system:
            payload["messages"].append({"role": "system", "content": system})
        payload["messages"].append({"role": "user", "content": user})

        t0 = time.time()
        r = requests.post(f"{self.host}/api/chat", json=payload, timeout=120)
        if r.status_code != 200:
            raise RuntimeError(f"Ollama error {r.status_code}: {r.text[:300]}")
        data = r.json()
        text = (data.get("message", {}) or {}).get("content", "") or ""
        return LLMResult(text=text.strip(), latency_s=round(time.time() - t0, 4))
