from typing import List


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> List[str]:
    """
    Simple character chunking. Beginner-friendly and reliable.
    """
    text = (text or "").strip()
    if not text:
        return []

    chunks = []
    i = 0

    while i < len(text):
        end = min(len(text), i + chunk_size)
        chunks.append(text[i:end])

        i = end - overlap
        if i < 0:
            i = 0

        if i >= len(text):
            break

    return [c.strip() for c in chunks if c.strip()]
