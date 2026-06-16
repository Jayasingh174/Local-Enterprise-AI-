# Local Enterprise AI (FastAPI) - Windows 
## What it does - Local chat using Ollama - RAG over PDFs (ChromaDB) - STT using faster-whisper (local) - TTS using pyttsx3 (offline) - Basic guardrails + logging 
## Setup (Windows PowerShell) 
1) Install Python 3.10+ 
2) Install FFmpeg: 
winget install Gyan.FFmpeg 
3) Install Ollama + pull models: 
ollama pull llama3.1:8b-instruct-q4_K_M 
ollama pull nomic-embed-text 
4) Create venv + install deps: 
python -m venv .venv 
.\.venv\Scripts\activate 
pip install -r requirements.txt 
5) Copy .env.example to .env and adjust if needed 
6) Run: 
uvicorn app.main:app --port 8001 --reload
Open: http://127.0.0.1:8001
## Use 
1) Put PDFs in data/docs/ 
2) Click "Ingest Docs" 
3) Ask questions via chat or voice# Local-Enterprise-AI-  
