import os
from faster_whisper import WhisperModel
from app.config import AUDIO_DIR

# CPU-friendly model: "small" (balanced). You can change to "base" for faster/lower accuracy.
_MODEL = None


def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = WhisperModel("small", device="cpu", compute_type="int8")
    return _MODEL


def transcribe(audio_path: str) -> str:
    model = get_model()
    segments, info = model.transcribe(audio_path, beam_size=3)

    text = []
    for seg in segments:
        text.append(seg.text)

    return " ".join(text).strip()
