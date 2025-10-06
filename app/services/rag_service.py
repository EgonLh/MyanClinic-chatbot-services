from app.services.llm_service import call_llm
from app.utils.vector_utils import get_vector_store, embed_query

def rag_chat(query: str) -> str:
    # 1. Embed query
    q_emb = embed_query(query)

    # 2. Search FAISS for top docs
    vector_store = get_vector_store()
    scores, docs = vector_store.search(q_emb, k=3)

    # 3. Build context safely: only use 'question' and 'answer'
    context = "\n".join([
        f"Q: {doc['question']}\nA: {doc['answer']}" if isinstance(doc, dict) else str(doc)
        for doc in docs
    ])
    print(context)

    # 4. Call LLM with context + query
    prompt = f"Answer the user based on context.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    answer = call_llm(prompt)

    return answer
