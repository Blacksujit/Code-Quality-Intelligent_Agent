"""
RAG (Retrieval-Augmented Generation) modules for enhanced code search.
"""

# Optional imports with proper error handling
try:
    from .faiss_index import FAISSRAGIndex, create_faiss_rag_index, HybridRAGIndex
    _RAG_AVAILABLE = True
except ImportError as e:
    print(f"[RAG] Optional RAG dependencies not available: {e}")
    FAISSRAGIndex = None
    create_faiss_rag_index = None
    HybridRAGIndex = None
    _RAG_AVAILABLE = False

__all__ = ["FAISSRAGIndex", "create_faiss_rag_index", "HybridRAGIndex"]
