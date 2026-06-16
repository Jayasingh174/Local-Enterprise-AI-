import sys
import os
import time
from typing import Dict, Any
from app.config import LOG_DIR


def ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)


def log_event(event: Dict[str, Any]) -> None:
    """
    Simple JSONL logging (enterprise-friendly baseline).
    Keep logs separate from RAG memory
    """
    ensure_dirs()
    ts = time.strftime("%Y-%m-%d")
    path = os.path.join(LOG_DIR, f"events-{ts}.jsonl")

    safe = dict(event)
    safe["ts"] = time.time()

    with open(path, "a", encoding="utf-8") as f:
        f.write(str(safe).replace("\n", " ") + "\n")


def guard_no_internet_tools():
    # placeholder: in this codebase we simply DO NOT implement any web-browsing tool.
    return True


def sanitize_user_text(text: str) -> str:
    # basic sanitation; keep minimal for beginner
    return (text or "").strip()[:20000]
