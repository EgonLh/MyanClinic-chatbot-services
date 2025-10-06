"""
Ingest documents into FAISS vector DB.
Run: pipenv run python scripts/ingest_docs.py
"""

import os, pickle, faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DOCS_PATH = "app/data/main_db/"
INDEX_FILE = "app/data/faiss_index/index.faiss"
DOCS_FILE = "app/data/faiss_index/docs.pkl"

import json


def load_documents():
    docs = []
    for file in os.listdir(DOCS_PATH):
        if file.endswith(".txt") or file.endswith(".jsonl"):
            with open(os.path.join(DOCS_PATH, file), "r", encoding="utf-8") as f:
                if file.endswith(".txt"):
                    content = f.read().strip()
                    if content:
                        docs.append(content)
                elif file.endswith(".jsonl"):
                    for line in f:
                        try:
                            obj = json.loads(line)
                            q = obj.get("question", "")
                            a = obj.get("answer", "")
                            aliases = " ".join(obj.get("aliases", []))
                            # Combine into one searchable document
                            text = f"Q: {q}\nAliases: {aliases}\nA: {a}"
                            if text.strip():
                                docs.append(text)
                        except json.JSONDecodeError:
                            continue
    return docs

    docs = []
    for file in os.listdir(DOCS_PATH):
        if file.endswith(".txt") or file.endswith(".jsonl"):
            with open(os.path.join(DOCS_PATH, file), "r", encoding="utf-8") as f:
                if file.endswith(".txt"):
                    content = f.read().strip()
                    if content:
                        docs.append(content)
                elif file.endswith(".jsonl"):
                    for line in f:
                        try:
                            obj = json.loads(line)
                            q = obj.get("question", "")
                            a = obj.get("answer", "")
                            aliases = " ".join(obj.get("aliases", []))
                            # Combine into one searchable document
                            text = f"Q: {q}\nAliases: {aliases}\nA: {a}"
                            if text.strip():
                                docs.append(text)
                        except json.JSONDecodeError:
                            continue
    return docs

if __name__ == "__main__":
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    docs = load_documents()

    if not docs:
        raise ValueError(f"No documents found in {DOCS_PATH}")

    # Always ensure list input
    embeddings = embedder.encode(docs, convert_to_numpy=True)

    # Make sure embeddings are 2D
    if len(embeddings.shape) == 1:
        embeddings = embeddings.reshape(1, -1)

    # Save FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    faiss.write_index(index, INDEX_FILE)

    with open(DOCS_FILE, "wb") as f:
        pickle.dump(docs, f)

    print(f"Ingested {len(docs)} docs into FAISS index.")
