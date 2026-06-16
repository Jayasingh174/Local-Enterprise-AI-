import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from app.config import CHROMA_DIR, RAG_TOP_K

COLLECTION_NAME = "docs"


class VectorStore:

    def __init__(self, persist_dir: str = CHROMA_DIR):
        os.makedirs(persist_dir, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )

        self.col = self.client.get_or_create_collection(COLLECTION_NAME)

    def reset(self) -> None:
        self.client.delete_collection(COLLECTION_NAME)
        self.col = self.client.get_or_create_collection(COLLECTION_NAME)

    def add(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        self.col.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(
        self,
        embedding: List[float],
        top_k: int = RAG_TOP_K
    ) -> List[Dict[str, Any]]:

        res = self.col.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]

        out = []
        for doc, meta, dist in zip(docs, metas, dists):
            out.append({
                "text": doc,
                "meta": meta,
                "distance": dist,
            })

        return out
