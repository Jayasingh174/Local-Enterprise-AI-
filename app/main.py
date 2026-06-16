import os 
import uuid 
from fastapi import FastAPI, UploadFile, File 
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse 
from fastapi.staticfiles import StaticFiles 
from app.config import APP_NAME, DATA_DIR, AUDIO_DIR, MAX_CONTEXT_CHARS 
from app.security import log_event, sanitize_user_text, guard_no_internet_tools 
from app.ai.ollama_client import OllamaClient 
from app.ai.prompts import build_prompt 
from app.rag.store import VectorStore 
from app.rag.ingest import build_chunks 
from app.voice.stt import transcribe 
from app.voice.tts import speak_to_wav 

app = FastAPI(title=APP_NAME) 

# Ensure dirs 
os.makedirs(DATA_DIR, exist_ok=True) 
os.makedirs(AUDIO_DIR, exist_ok=True) 

web_dir = os.path.join(os.path.dirname(__file__), "web")

# Serve static files
app.mount("/app/web", StaticFiles(directory=web_dir), name="web")

ollama = OllamaClient() 
store = VectorStore() 

@app.get("/", response_class=HTMLResponse)
def home():
    index_path = os.path.join(web_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/ingest") 
def ingest(): 
    """Reads PDFs from data/docs, chunks them, embeds using Ollama, stores in ChromaDB.""" 
    ids, docs, metas = build_chunks() 
    if not docs: 
        return JSONResponse({"ok": False, "message": "No PDFs found in data/docs"}, status_code=400) 
    # Reset for simplicity (v1). For production, do incremental ingest. 
    store.reset() 
    embeddings = ollama.embed(docs) 
    store.add(ids=ids, embeddings=embeddings, documents=docs, metadatas=metas) 
    log_event({"type": "ingest", "chunks": len(docs)}) 
    return {"ok": True, "chunks": len(docs)} 

@app.post("/chat") 
def chat(payload: dict): 
    """payload: { message: str, use_rag: bool }""" 
    guard_no_internet_tools() 
    msg = sanitize_user_text(payload.get("message", "")) 
    use_rag = bool(payload.get("use_rag", True)) 
    context = "" 
    retrieved = [] 
    if use_rag and msg: 
        qvec = ollama.embed([msg])[0] 
        hits = store.query(qvec) 
        retrieved = hits 
        # Build context with sources; cap length for CPU sanity 
        parts = [] 
        for h in hits: 
            src = h["meta"].get("source", "unknown") 
            ch = h["meta"].get("chunk", -1) 
            parts.append(f"[{src}#{ch}] {h['text']}") 
        context = "\n\n".join(parts)[:MAX_CONTEXT_CHARS] 
    prompt = build_prompt(msg, context if context else None) 
    answer = ollama.chat(prompt) 
    log_event({ 
        "type": "chat", 
        "use_rag": use_rag, 
        "message": msg[:5000], 
        "retrieved_count": len(retrieved), 
        "answer": answer[:5000], 
    }) 
    return {"ok": True, "answer": answer, "retrieved": retrieved} 

@app.post("/stt") 
async def stt(file: UploadFile = File(...)): 
    """Receives an audio file and returns transcript.""" 
    filename = f"stt-{uuid.uuid4()}-{file.filename}" 
    path = os.path.join(AUDIO_DIR, filename) 
    with open(path, "wb") as f: 
        f.write(await file.read()) 
    text = transcribe(path) 
    log_event({"type": "stt", "file": filename, "text": text[:5000]}) 
    return {"ok": True, "text": text} 

@app.post("/tts") 
def tts(payload: dict): 
    """payload: { text: str } returns wav file url""" 
    text = sanitize_user_text(payload.get("text", "")) 
    if not text: 
        return JSONResponse({"ok": False, "message": "No text"}, status_code=400) 
    wav_path = speak_to_wav(text) 
    wav_name = os.path.basename(wav_path) 
    log_event({"type": "tts", "file": wav_name, "text": text[:2000]}) 
    return {"ok": True, "audio_url": f"/audio/{wav_name}"} 

@app.get("/audio/{name}") 
def get_audio(name: str): 
    path = os.path.join(AUDIO_DIR, name) 
    if not os.path.isfile(path): 
        return JSONResponse({"ok": False, "message": "Not found"}, status_code=404) 
    return FileResponse(path, media_type="audio/wav")