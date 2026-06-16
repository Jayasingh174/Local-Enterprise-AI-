import os
import uuid
import pyttsx3
from app.config import AUDIO_DIR

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 170)
    return _engine


def speak_to_wav(text: str) -> str:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    out = os.path.join(AUDIO_DIR, f"tts-{uuid.uuid4()}.wav")

    eng = get_engine()
    eng.save_to_file(text, out)
    eng.runAndWait()

    return out
