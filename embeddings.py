import os
import requests


JINA_API_KEY = os.getenv("JINA_API_KEY")
JINA_MODEL = os.getenv("JINA_MODEL", "jina-embeddings-v2-base-en")

if not JINA_API_KEY:
    raise RuntimeError("JINA_API_KEY is not set")


def embed(text: str):
    if not text or not text.strip():
        return None

    response = requests.post(
        "https://api.jina.ai/v1/embeddings",
        headers={
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": JINA_MODEL,
            "input": text[:8000]  # safety limit
        }
    )

    try:
        payload = response.json()
    except Exception:
        raise RuntimeError(f"Invalid response from Jina: {response.text}")

    if "data" not in payload:
        raise RuntimeError(f"Jina error: {payload}")

    return payload["data"][0]["embedding"]
