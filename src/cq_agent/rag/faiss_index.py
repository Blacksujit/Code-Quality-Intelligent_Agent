"""
FAISS-based vector RAG for enhanced semantic search over codebases.
Optional enhancement to the existing TF-IDF system.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

from cq_agent.ingestion import RepoContext, FileRecord


class FAISSRAGIndex:
    """FAISS-based RAG index for semantic code search."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", dimension: int = 384):
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS not available. Install with: pip install faiss-cpu")
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers not available. Install with: pip install sentence-transformers")
        
        self.model_name = model_name
        self.dimension = dimension
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.metadata = []
        
    def _get_cache_path(self, repo_root: str) -> Path:
        """Get cache path for this repo."""
        cache_dir = Path.home() / ".cq_agent_cache" / "faiss"
        cache_dir.mkdir(parents=True, exist_ok=True)
        repo_hash = hashlib.sha1(repo_root.encode()).hexdigest()[:16]
        return cache_dir / f"faiss_{repo_hash}_{self.model_name.replace('/', '_')}.json"
    
    def _chunk_file(self, file_record: FileRecord, chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, Any]]:
        """Chunk a file into overlapping segments for better semantic search."""
        text = file_record["text"]
        lines = text.splitlines()
        chunks = []
        
        current_chunk = []
        current_length = 0
        
        for i, line in enumerate(lines):
            current_chunk.append(line)
            current_length += len(line) + 1  # +1 for newline
            
            if current_length >= chunk_size or i == len(lines) - 1:
                chunk_text = "\n".join(current_chunk)
                if chunk_text.strip():
                    chunks.append({
                        "text": chunk_text,
                        "file": file_record["path"],
                        "start_line": max(1, i - len(current_chunk) + 1),
                        "end_line": i + 1,
                        "language": file_record["language"],
                        "sloc": len([l for l in current_chunk if l.strip()])
                    })
                
                # Overlap for next chunk
                if i < len(lines) - 1:
                    overlap_lines = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                    current_chunk = overlap_lines
                    current_length = sum(len(l) + 1 for l in overlap_lines)
                else:
                    current_chunk = []
                    current_length = 0
        
        return chunks
    
    def build_index(self, repo: RepoContext, force_rebuild: bool = False) -> None:
        """Build FAISS index from repository."""
        cache_path = self._get_cache_path(repo["root"])
        
        # Try to load from cache
        if not force_rebuild and cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                if cache_data.get("model_name") == self.model_name:
                    self.chunks = cache_data.get("chunks", [])
                    self.metadata = cache_data.get("metadata", [])
                    
                    # Rebuild FAISS index from cached vectors
                    vectors = np.array(cache_data.get("vectors", []))
                    if len(vectors) > 0:
                        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
                        self.index.add(vectors.astype('float32'))
                        print(f"[FAISS] Loaded cached index with {len(vectors)} vectors")
                        return
            except Exception as e:
                print(f"[FAISS] Cache load failed: {e}, rebuilding...")
        
        # Build new index
        print(f"[FAISS] Building index for {len(repo['files'])} files...")
        all_chunks = []
        
        for file_record in repo["files"].values():
            chunks = self._chunk_file(file_record)
            all_chunks.extend(chunks)
        
        if not all_chunks:
            print("[FAISS] No chunks to index")
            return
        
        # Generate embeddings
        texts = [chunk["text"] for chunk in all_chunks]
        print(f"[FAISS] Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Normalize for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Build FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(embeddings.astype('float32'))
        
        self.chunks = all_chunks
        self.metadata = [{"chunk_id": i, "file": chunk["file"], "start_line": chunk["start_line"], 
                         "end_line": chunk["end_line"], "language": chunk["language"]} 
                         for i, chunk in enumerate(all_chunks)]
        
        # Save to cache
        try:
            cache_data = {
                "model_name": self.model_name,
                "vectors": embeddings.tolist(),
                "chunks": self.chunks,
                "metadata": self.metadata
            }
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            print(f"[FAISS] Cached index to {cache_path}")
        except Exception as e:
            print(f"[FAISS] Cache save failed: {e}")
        
        print(f"[FAISS] Built index with {len(embeddings)} vectors")
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.3) -> List[Tuple[Dict[str, Any], float]]:
        """Search for semantically similar code chunks."""
        if self.index is None or len(self.chunks) == 0:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), min(top_k, len(self.chunks)))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= threshold and idx < len(self.chunks):
                chunk = self.chunks[idx]
                metadata = self.metadata[idx] if idx < len(self.metadata) else {}
                
                # Create result object similar to TF-IDF format
                result = {
                    "text": chunk["text"],
                    "path": chunk["file"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "language": chunk["language"],
                    "sloc": chunk["sloc"]
                }
                results.append((result, float(score)))
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        return {
            "total_chunks": len(self.chunks),
            "index_size": self.index.ntotal if self.index else 0,
            "model_name": self.model_name,
            "dimension": self.dimension
        }


def create_faiss_rag_index(repo: RepoContext, model_name: str = "all-MiniLM-L6-v2", 
                          force_rebuild: bool = False) -> Optional[FAISSRAGIndex]:
    """Create a FAISS RAG index for the repository."""
    if not FAISS_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
        print("[FAISS] Dependencies not available. Install with: pip install faiss-cpu sentence-transformers")
        return None
    
    try:
        index = FAISSRAGIndex(model_name=model_name)
        index.build_index(repo, force_rebuild=force_rebuild)
        return index
    except Exception as e:
        print(f"[FAISS] Failed to create index: {e}")
        return None


# Hybrid search that combines TF-IDF and FAISS
class HybridRAGIndex:
    """Combines TF-IDF and FAISS for better search results."""
    
    def __init__(self, tfidf_index, faiss_index: Optional[FAISSRAGIndex] = None):
        self.tfidf_index = tfidf_index
        self.faiss_index = faiss_index
    
    def search(self, query: str, top_k: int = 5, faiss_weight: float = 0.7) -> List[Tuple[Dict[str, Any], float]]:
        """Hybrid search combining TF-IDF and FAISS results."""
        results = []
        
        # Get TF-IDF results
        tfidf_results = self.tfidf_index.search(query, top_k=top_k * 2)  # Get more for re-ranking
        
        # Get FAISS results if available
        faiss_results = []
        if self.faiss_index:
            faiss_results = self.faiss_index.search(query, top_k=top_k * 2)
        
        # Combine and re-rank
        if faiss_results:
            # Create a combined score
            combined_scores = {}
            
            for result, score in tfidf_results:
                key = f"{result.path}:{result.start_line}-{result.end_line}"
                combined_scores[key] = {"result": result, "tfidf_score": score, "faiss_score": 0.0}
            
            for result, score in faiss_results:
                key = f"{result['path']}:{result['start_line']}-{result['end_line']}"
                if key in combined_scores:
                    combined_scores[key]["faiss_score"] = score
                else:
                    # Convert FAISS result to TF-IDF format
                    from types import SimpleNamespace
                    tfidf_result = SimpleNamespace(
                        text=result["text"],
                        path=result["path"],
                        start_line=result["start_line"],
                        end_line=result["end_line"],
                        language=result["language"]
                    )
                    combined_scores[key] = {"result": tfidf_result, "tfidf_score": 0.0, "faiss_score": score}
            
            # Calculate combined scores
            for data in combined_scores.values():
                combined_score = (1 - faiss_weight) * data["tfidf_score"] + faiss_weight * data["faiss_score"]
                results.append((data["result"], combined_score))
        else:
            # Fallback to TF-IDF only
            results = tfidf_results
        
        # Sort by combined score and return top_k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
