import requests
from typing import List
from app.config import OLLAMA_BASE_URL, CHAT_MODEL, EMBED_MODEL


class OllamaClient:

    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def chat(self, prompt: str) -> str:
        """
        Uses Ollama /api/generate for simplicity (single prompt).
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": CHAT_MODEL,
            "prompt": prompt,
            "stream": False,
        }

        r = requests.post(url, json=payload, timeout=180)
        r.raise_for_status()
        data = r.json()

        return data.get("response", "").strip()

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Uses Ollama /api/embeddings (batch).
        """
        url = f"{self.base_url}/api/embeddings"
        vectors: List[List[float]] = []

        for t in texts:
            payload = {
                "model": EMBED_MODEL,
                "prompt": t
            }

            r = requests.post(url, json=payload, timeout=180)
            r.raise_for_status()
            data = r.json()

            vec = data.get("embedding")
            if not vec:
                raise RuntimeError("No embedding returned from Ollama")

            vectors.append(vec)

        return vectors

