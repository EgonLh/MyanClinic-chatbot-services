"""
Shared dependencies for routes.
Example: DB sessions, vector store, etc.
"""

from app.utils.vector_utils import get_vector_store

def get_vector_db():
    return get_vector_store()
