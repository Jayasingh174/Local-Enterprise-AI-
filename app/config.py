import os
from dotenv import load_dotenv

load_dotenv()

def getenv(name: str, default: str) -> str:
    val = os.getenv(name)
    return val if val is not None and val.strip() != "" else default


APP_NAME = getenv("APP_NAME", "Local Enterprise AI")
OLLAMA_BASE_URL = getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
CHAT_MODEL = getenv("CHAT_MODEL", "llama3.1:8b-instruct-q4_K_M")
EMBED_MODEL = getenv("EMBED_MODEL", "nomic-embed-text")

DATA_DIR = getenv("DATA_DIR", "./data")
DOCS_DIR = getenv("DOCS_DIR", os.path.join(DATA_DIR, "docs"))
CHROMA_DIR = getenv("CHROMA_DIR", os.path.join(DATA_DIR, "chroma"))
AUDIO_DIR = getenv("AUDIO_DIR", os.path.join(DATA_DIR, "audio"))
LOG_DIR = getenv("LOG_DIR", os.path.join(DATA_DIR, "logs"))

RAG_TOP_K = int(getenv("RAG_TOP_K", "5"))
MAX_CONTEXT_CHARS = int(getenv("MAX_CONTEXT_CHARS", "6000"))
