import os
import uuid
from typing import List, Dict, Any, Tuple
from pypdf import PdfReader
from app.config import DOCS_DIR
from app.rag.textsplits import chunk_text

def list_pdfs() -> List[str]:
    """
    List all PDF files in the DOCS_DIR folder.
    Returns a sorted list of file paths.
    """
    if not os.path.isdir(DOCS_DIR):
        return []

    files = []
    for name in os.listdir(DOCS_DIR):
        if name.lower().endswith(".pdf"):
            files.append(os.path.join(DOCS_DIR, name))
    return sorted(files)

def extract_pdf_text(path: str) -> str:
    """
    Extracts text from a PDF file using PdfReader.
    Returns the full text as a single string.
    """
    reader = PdfReader(path)
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)

def build_chunks() -> Tuple[List[str], List[str], List[Dict[str, Any]]]:
    """
    Reads PDFs from DOCS_DIR, splits them into chunks, and returns:
    (ids, documents, metadatas)
    """
    pdfs = list_pdfs()
    ids: List[str] = []
    docs: List[str] = []
    metas: List[Dict[str, Any]] = []

    for pdf in pdfs:
        raw = extract_pdf_text(pdf)
        chunks = chunk_text(raw)
        base = os.path.basename(pdf)

        for idx, ch in enumerate(chunks):
            cid = str(uuid.uuid4())
            ids.append(cid)
            docs.append(ch)
            metas.append({"source": base, "chunk": idx})

    return ids, docs, metas
