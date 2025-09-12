"""
Enhanced RAG with Vector Embeddings
Provides semantic code search using vector embeddings
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import pickle
from pathlib import Path
import re
import ast
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class CodeChunk:
    """Represents a chunk of code with metadata"""
    content: str
    file_path: str
    start_line: int
    end_line: int
    chunk_type: str  # 'function', 'class', 'import', 'comment', 'code'
    language: str
    embedding: Optional[np.ndarray] = None
    metadata: Optional[Dict] = None


class CodeEmbeddingIndex:
    """Vector embedding index for semantic code search"""
    
    def __init__(self, model_name: str = "tfidf"):
        self.model_name = model_name
        self.chunks: List[CodeChunk] = []
        self.vectorizer = None
        self.embeddings_matrix = None
        self.chunk_metadata = {}
        
    def add_code_chunks(self, repo_data: Dict) -> int:
        """Add code chunks from repository data"""
        chunks_added = 0
        
        for file_path, file_data in repo_data.get('files', {}).items():
            content = file_data.get('content', '')
            language = file_data.get('language', 'unknown')
            
            # Extract different types of chunks
            file_chunks = self._extract_code_chunks(file_path, content, language)
            
            for chunk in file_chunks:
                self.chunks.append(chunk)
                chunks_added += 1
        
        return chunks_added
    
    def _extract_code_chunks(self, file_path: str, content: str, language: str) -> List[CodeChunk]:
        """Extract meaningful code chunks from file content"""
        chunks = []
        lines = content.split('\n')
        
        if language == 'python':
            chunks.extend(self._extract_python_chunks(file_path, content, lines))
        elif language in ['javascript', 'typescript']:
            chunks.extend(self._extract_js_chunks(file_path, content, lines))
        else:
            # Generic chunking for other languages
            chunks.extend(self._extract_generic_chunks(file_path, content, lines))
        
        return chunks
    
    def _extract_python_chunks(self, file_path: str, content: str, lines: List[str]) -> List[CodeChunk]:
        """Extract Python-specific chunks"""
        chunks = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Function definition
                    start_line = node.lineno
                    end_line = node.end_lineno or start_line
                    func_content = '\n'.join(lines[start_line-1:end_line])
                    
                    chunks.append(CodeChunk(
                        content=func_content,
                        file_path=file_path,
                        start_line=start_line,
                        end_line=end_line,
                        chunk_type='function',
                        language='python',
                        metadata={
                            'function_name': node.name,
                            'args': [arg.arg for arg in node.args.args],
                            'docstring': ast.get_docstring(node),
                            'decorators': [ast.unparse(dec) for dec in node.decorator_list]
                        }
                    ))
                
                elif isinstance(node, ast.ClassDef):
                    # Class definition
                    start_line = node.lineno
                    end_line = node.end_lineno or start_line
                    class_content = '\n'.join(lines[start_line-1:end_line])
                    
                    chunks.append(CodeChunk(
                        content=class_content,
                        file_path=file_path,
                        start_line=start_line,
                        end_line=end_line,
                        chunk_type='class',
                        language='python',
                        metadata={
                            'class_name': node.name,
                            'bases': [ast.unparse(base) for base in node.bases],
                            'docstring': ast.get_docstring(node)
                        }
                    ))
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    # Import statements
                    import_content = ast.unparse(node)
                    chunks.append(CodeChunk(
                        content=import_content,
                        file_path=file_path,
                        start_line=node.lineno,
                        end_line=node.lineno,
                        chunk_type='import',
                        language='python',
                        metadata={'import_type': 'import' if isinstance(node, ast.Import) else 'from_import'}
                    ))
        
        except:
            # Fallback to generic chunking if AST parsing fails
            chunks.extend(self._extract_generic_chunks(file_path, content, lines))
        
        return chunks
    
    def _extract_js_chunks(self, file_path: str, content: str, lines: List[str]) -> List[CodeChunk]:
        """Extract JavaScript/TypeScript chunks using regex patterns"""
        chunks = []
        
        # Function patterns
        function_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{[^}]*\}',
            r'(\w+)\s*:\s*function\s*\([^)]*\)\s*\{[^}]*\}'
        ]
        
        for pattern in function_patterns:
            for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
                func_content = match.group(0)
                func_name = match.group(1)
                
                # Find line numbers
                start_line = content[:match.start()].count('\n') + 1
                end_line = content[:match.end()].count('\n') + 1
                
                chunks.append(CodeChunk(
                    content=func_content,
                    file_path=file_path,
                    start_line=start_line,
                    end_line=end_line,
                    chunk_type='function',
                    language='javascript',
                    metadata={'function_name': func_name}
                ))
        
        # Import patterns
        import_patterns = [
            r'import\s+.*?from\s+[\'"][^\'"]+[\'"]',
            r'require\s*\([\'"][^\'"]+[\'"]\)'
        ]
        
        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                import_content = match.group(0)
                start_line = content[:match.start()].count('\n') + 1
                
                chunks.append(CodeChunk(
                    content=import_content,
                    file_path=file_path,
                    start_line=start_line,
                    end_line=start_line,
                    chunk_type='import',
                    language='javascript',
                    metadata={'import_type': 'es6' if 'import' in import_content else 'commonjs'}
                ))
        
        return chunks
    
    def _extract_generic_chunks(self, file_path: str, content: str, lines: List[str]) -> List[CodeChunk]:
        """Extract generic code chunks for any language"""
        chunks = []
        
        # Split into logical blocks (functions, classes, etc.)
        current_chunk = []
        current_start = 1
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Start of new logical block
            if (stripped.startswith(('def ', 'class ', 'function ', 'const ', 'let ', 'var ')) or
                stripped.startswith(('import ', 'from ', 'require(')) or
                stripped.startswith(('//', '/*', '#', '<!--'))):
                
                # Save previous chunk if it exists
                if current_chunk:
                    chunk_content = '\n'.join(current_chunk)
                    if len(chunk_content.strip()) > 10:  # Only save meaningful chunks
                        chunks.append(CodeChunk(
                            content=chunk_content,
                            file_path=file_path,
                            start_line=current_start,
                            end_line=i-1,
                            chunk_type='code',
                            language='unknown'
                        ))
                
                # Start new chunk
                current_chunk = [line]
                current_start = i
            else:
                current_chunk.append(line)
        
        # Save last chunk
        if current_chunk:
            chunk_content = '\n'.join(current_chunk)
            if len(chunk_content.strip()) > 10:
                chunks.append(CodeChunk(
                    content=chunk_content,
                    file_path=file_path,
                    start_line=current_start,
                    end_line=len(lines),
                    chunk_type='code',
                    language='unknown'
                ))
        
        return chunks
    
    def build_embeddings(self) -> bool:
        """Build vector embeddings for all chunks"""
        if not self.chunks:
            return False
        
        # Prepare text for vectorization
        texts = []
        for chunk in self.chunks:
            # Create enhanced text representation
            enhanced_text = self._enhance_chunk_text(chunk)
            texts.append(enhanced_text)
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        
        # Fit and transform
        self.embeddings_matrix = self.vectorizer.fit_transform(texts)
        
        return True
    
    def _enhance_chunk_text(self, chunk: CodeChunk) -> str:
        """Enhance chunk text for better semantic search"""
        text_parts = []
        
        # Add file path (boosted)
        file_name = Path(chunk.file_path).name
        text_parts.extend([file_name] * 3)  # Boost file name
        
        # Add chunk type
        text_parts.append(chunk.chunk_type)
        
        # Add metadata
        if chunk.metadata:
            if 'function_name' in chunk.metadata:
                text_parts.extend([chunk.metadata['function_name']] * 2)  # Boost function names
            if 'class_name' in chunk.metadata:
                text_parts.extend([chunk.metadata['class_name']] * 2)  # Boost class names
            if 'args' in chunk.metadata:
                text_parts.extend(chunk.metadata['args'])
        
        # Add content
        text_parts.append(chunk.content)
        
        return ' '.join(text_parts)
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[CodeChunk, float]]:
        """Search for similar code chunks"""
        if not self.vectorizer or self.embeddings_matrix is None:
            return []
        
        # Transform query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.embeddings_matrix).flatten()
        
        # Get top results
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append((self.chunks[idx], similarities[idx]))
        
        return results
    
    def get_similar_chunks(self, chunk: CodeChunk, top_k: int = 5) -> List[Tuple[CodeChunk, float]]:
        """Find chunks similar to a given chunk"""
        if not self.vectorizer or self.embeddings_matrix is None:
            return []
        
        # Find chunk index
        chunk_idx = None
        for i, c in enumerate(self.chunks):
            if (c.file_path == chunk.file_path and 
                c.start_line == chunk.start_line and 
                c.end_line == chunk.end_line):
                chunk_idx = i
                break
        
        if chunk_idx is None:
            return []
        
        # Get similarities for this chunk
        similarities = cosine_similarity(
            self.embeddings_matrix[chunk_idx:chunk_idx+1], 
            self.embeddings_matrix
        ).flatten()
        
        # Get top results (excluding self)
        top_indices = similarities.argsort()[-top_k-1:][::-1]
        
        results = []
        for idx in top_indices:
            if idx != chunk_idx and similarities[idx] > 0.1:
                results.append((self.chunks[idx], similarities[idx]))
        
        return results
    
    def save_index(self, file_path: str) -> bool:
        """Save the embedding index to disk"""
        try:
            index_data = {
                'chunks': self.chunks,
                'vectorizer': self.vectorizer,
                'embeddings_matrix': self.embeddings_matrix,
                'model_name': self.model_name
            }
            
            with open(file_path, 'wb') as f:
                pickle.dump(index_data, f)
            
            return True
        except:
            return False
    
    def load_index(self, file_path: str) -> bool:
        """Load the embedding index from disk"""
        try:
            with open(file_path, 'rb') as f:
                index_data = pickle.load(f)
            
            self.chunks = index_data['chunks']
            self.vectorizer = index_data['vectorizer']
            self.embeddings_matrix = index_data['embeddings_matrix']
            self.model_name = index_data['model_name']
            
            return True
        except:
            return False


class EnhancedRAG:
    """Enhanced RAG system with vector embeddings"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.embedding_index = CodeEmbeddingIndex()
        self.index_file = Path(repo_path) / '.cq_embeddings.pkl'
        
    def build_index(self, repo_data: Dict) -> bool:
        """Build the embedding index from repository data"""
        # Add code chunks
        chunks_added = self.embedding_index.add_code_chunks(repo_data)
        
        if chunks_added == 0:
            return False
        
        # Build embeddings
        success = self.embedding_index.build_embeddings()
        
        if success:
            # Save index
            self.embedding_index.save_index(str(self.index_file))
        
        return success
    
    def load_index(self) -> bool:
        """Load existing embedding index"""
        if self.index_file.exists():
            return self.embedding_index.load_index(str(self.index_file))
        return False
    
    def search_code(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for code using semantic similarity"""
        results = self.embedding_index.search(query, top_k)
        
        search_results = []
        for chunk, similarity in results:
            search_results.append({
                'file_path': chunk.file_path,
                'start_line': chunk.start_line,
                'end_line': chunk.end_line,
                'content': chunk.content,
                'chunk_type': chunk.chunk_type,
                'language': chunk.language,
                'similarity': similarity,
                'metadata': chunk.metadata or {}
            })
        
        return search_results
    
    def find_similar_code(self, file_path: str, start_line: int, end_line: int) -> List[Dict]:
        """Find code similar to a specific code block"""
        # Find the chunk
        target_chunk = None
        for chunk in self.embedding_index.chunks:
            if (chunk.file_path == file_path and 
                chunk.start_line == start_line and 
                chunk.end_line == end_line):
                target_chunk = chunk
                break
        
        if not target_chunk:
            return []
        
        # Find similar chunks
        similar_chunks = self.embedding_index.get_similar_chunks(target_chunk)
        
        results = []
        for chunk, similarity in similar_chunks:
            results.append({
                'file_path': chunk.file_path,
                'start_line': chunk.start_line,
                'end_line': chunk.end_line,
                'content': chunk.content,
                'chunk_type': chunk.chunk_type,
                'language': chunk.language,
                'similarity': similarity,
                'metadata': chunk.metadata or {}
            })
        
        return results
    
    def get_code_context(self, file_path: str, line_number: int) -> Dict:
        """Get context around a specific line"""
        context_chunks = []
        
        for chunk in self.embedding_index.chunks:
            if (chunk.file_path == file_path and 
                chunk.start_line <= line_number <= chunk.end_line):
                context_chunks.append(chunk)
        
        if not context_chunks:
            return {}
        
        # Find the most relevant chunk
        best_chunk = min(context_chunks, key=lambda c: abs(c.start_line - line_number))
        
        return {
            'file_path': best_chunk.file_path,
            'start_line': best_chunk.start_line,
            'end_line': best_chunk.end_line,
            'content': best_chunk.content,
            'chunk_type': best_chunk.chunk_type,
            'language': best_chunk.language,
            'metadata': best_chunk.metadata or {}
        }


def create_enhanced_rag(repo_path: str) -> EnhancedRAG:
    """Create enhanced RAG instance"""
    return EnhancedRAG(repo_path)
