import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle

# Load embedding model (all-MiniLM is lightweight + fast)
_embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# FAISS index path
INDEX_FILE = "app/data/faiss_index/index.faiss"
DOCS_FILE = "app/data/faiss_index/docs.pkl"

# Cache
_index = None
_docs = []

def load_index():
    global _index, _docs
    if _index is None:
        if not os.path.exists(INDEX_FILE):
            raise ValueError("Vector store not found. Run scripts/ingest_docs.py first.")
        _index = faiss.read_index(INDEX_FILE)
        with open(DOCS_FILE, "rb") as f:
            _docs = pickle.load(f)
    return _index, _docs

def get_vector_store():
    class VectorStore:
        def search(self, query_emb, k=3):
            index, docs = load_index()
            D, I = index.search(np.array([query_emb]), k)
            return D[0], [docs[i] for i in I[0]]
    return VectorStore()

def embed_query(query: str):
    return _embedder.encode(query)
