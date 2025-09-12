from __future__ import annotations

import math
import re
from dataclasses import dataclass
import json
import hashlib
from pathlib import Path

from cq_agent.ingestion import RepoContext

# Optional FAISS integration
try:
    from cq_agent.rag import create_faiss_rag_index, HybridRAGIndex
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]+")
_FUNCTION_RE = re.compile(r"def\s+([A-Za-z_][A-Za-z0-9_]*)|function\s+([A-Za-z_][A-Za-z0-9_]*)|const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=")


@dataclass
class Chunk:
	path: str
	start_line: int
	end_line: int
	text: str
	functions: List[str]  # function names found in this chunk


def _extract_functions(text: str) -> List[str]:
	"""Extract function names from code text."""
	functions = []
	for match in _FUNCTION_RE.finditer(text):
		for group in match.groups():
			if group:
				functions.append(group.lower())
	return functions


def _tokenize(text: str) -> List[str]:
	return [t.lower() for t in _TOKEN_RE.findall(text)]


def _split_into_chunks(text: str, lines_per: int = 120) -> List[Tuple[int, int, str]]:
	lines = text.splitlines()
	chunks: List[Tuple[int, int, str]] = []
	for i in range(0, len(lines), lines_per):
		start = i + 1
		end = min(i + lines_per, len(lines))
		chunks.append((start, end, "\n".join(lines[i:end])))
	return chunks


class TfidfIndex:
	def __init__(self) -> None:
		self.vocab_idf: Dict[str, float] = {}
		self.doc_tfs: List[Dict[str, float]] = []
		self.docs: List[Chunk] = []

	def add_documents(self, docs: List[Chunk]) -> None:
		self.docs.extend(docs)
		# compute df
		df: Dict[str, int] = {}
		docs_tokens: List[Dict[str, int]] = []
		for ch in docs:
			tokens = _tokenize(ch.text)
			# Boost function names and filename tokens
			boosted_tokens = tokens.copy()
			boosted_tokens.extend([f.lower() for f in ch.functions])  # function names
			boosted_tokens.extend([Path(ch.path).stem.lower()])  # filename without extension
			
			counts: Dict[str, int] = {}
			for tok in boosted_tokens:
				counts[tok] = counts.get(tok, 0) + 1
			docs_tokens.append(counts)
			for tok in counts:
				df[tok] = df.get(tok, 0) + 1
		# update idf
		n_docs = len(self.docs)
		for tok, c in df.items():
			# smooth idf
			self.vocab_idf[tok] = math.log((1 + n_docs) / (1 + c)) + 1.0
		# compute tf vectors (normalized)
		for counts in docs_tokens:
			tf: Dict[str, float] = {}
			norm = 0.0
			for tok, cnt in counts.items():
				weight = (cnt / max(1, sum(counts.values()))) * self.vocab_idf.get(tok, 1.0)
				tf[tok] = weight
				norm += weight * weight
			norm = math.sqrt(norm) or 1.0
			for tok in list(tf.keys()):
				tf[tok] /= norm
			self.doc_tfs.append(tf)

	def _vectorize_query(self, query: str) -> Dict[str, float]:
		# Enhanced query preprocessing
		query_lower = query.lower()
		# Extract potential function names from query
		query_functions = _extract_functions(query)
		
		counts: Dict[str, int] = {}
		# Regular tokens
		for tok in _tokenize(query):
			counts[tok] = counts.get(tok, 0) + 1
		# Boost function names if mentioned
		for func in query_functions:
			counts[func] = counts.get(func, 0) + 2  # 2x boost for function names
		
		tf: Dict[str, float] = {}
		norm = 0.0
		for tok, cnt in counts.items():
			w = (cnt / max(1, sum(counts.values()))) * self.vocab_idf.get(tok, 1.0)
			tf[tok] = w
			norm += w * w
		norm = math.sqrt(norm) or 1.0
		for tok in list(tf.keys()):
			tf[tok] /= norm
		return tf

	def search(self, query: str, top_k: int = 5) -> List[Tuple[Chunk, float]]:
		q = self._vectorize_query(query)
		results: List[Tuple[int, float]] = []
		for idx, d in enumerate(self.doc_tfs):
			s = 0.0
			for tok, wq in q.items():
				s += wq * d.get(tok, 0.0)
			results.append((idx, s))
		results.sort(key=lambda p: p[1], reverse=True)
		return [(self.docs[i], score) for i, score in results[:top_k]]


def build_index(repo: RepoContext, max_files: int = 1000, use_faiss: bool = False) -> TfidfIndex:
	"""Build search index with optional FAISS enhancement."""
	index = TfidfIndex()
	docs: List[Chunk] = []
	for idx, (rel_path, rec) in enumerate(repo["files"].items()):
		if idx >= max_files:
			break
		for start, end, sub in _split_into_chunks(rec.get("text", "")):
			functions = _extract_functions(sub)
			docs.append(Chunk(path=rel_path, start_line=start, end_line=end, text=sub, functions=functions))
	index.add_documents(docs)
	
	# Add FAISS enhancement if requested and available
	if use_faiss and FAISS_AVAILABLE:
		try:
			faiss_index = create_faiss_rag_index(repo, force_rebuild=False)
			if faiss_index:
				# Return hybrid index that combines TF-IDF and FAISS
				return HybridRAGIndex(index, faiss_index)
		except Exception as e:
			print(f"[RAG] FAISS integration failed: {e}, using TF-IDF only")
	
	return index


def _repo_head_key(repo: RepoContext) -> str:
	# Use root plus sum of file hashes to approximate HEAD state
	root = repo.get("root", "")
	hasher = hashlib.sha256(root.encode("utf-8"))
	for path, rec in sorted(repo.get("files", {}).items()):
		hasher.update(path.encode("utf-8"))
		hasher.update(rec.get("hash", "").encode("utf-8"))
	return hasher.hexdigest()[:16]


def save_index(index: TfidfIndex, cache_dir: Path, key: str) -> None:
	cache_dir.mkdir(parents=True, exist_ok=True)
	data = {
		"docs": [
			{
				"path": c.path,
				"start": c.start_line,
				"end": c.end_line,
				"text": c.text,
				"functions": c.functions,
			}
			for c in index.docs
		],
		"vocab_idf": index.vocab_idf,
		"doc_tfs": index.doc_tfs,
	}
	(cache_dir / f"tfidf_{key}.json").write_text(json.dumps(data), encoding="utf-8")


def load_index(cache_dir: Path, key: str) -> TfidfIndex | None:
	p = cache_dir / f"tfidf_{key}.json"
	if not p.exists():
		return None
	try:
		raw = json.loads(p.read_text(encoding="utf-8"))
		index = TfidfIndex()
		index.vocab_idf = raw.get("vocab_idf", {})
		index.doc_tfs = raw.get("doc_tfs", [])
		index.docs = [
			Chunk(
				path=it.get("path", ""),
				start_line=int(it.get("start", 1)),
				end_line=int(it.get("end", 1)),
				text=it.get("text", ""),
				functions=list(it.get("functions", [])),
			)
			for it in raw.get("docs", [])
		]
		return index
	except Exception:
		return None
