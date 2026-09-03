import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.core.config import settings
from src.ai_engine.embeddings import get_embeddings_model

class VectorStoreInterface(ABC):
    @abstractmethod
    def similarity_search(self, query: str, top_k: int = 5, filter_dict: Optional[Dict[str, Any]] = None) -> List[Document]:
        pass

    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        pass

class FAISSVectorStore(VectorStoreInterface):
    """
    FAISS-based dense vector search engine with metadata filtering capability.
    Pluggable design allows replacing with pgvector / Elasticsearch without altering consumers.
    """
    def __init__(self, index_dir: str = settings.FAISS_INDEX_DIR):
        self.index_dir = index_dir
        self.embeddings = get_embeddings_model()
        self.vector_db = None
        self._load_index()

    def _load_index(self):
        if os.path.exists(os.path.join(self.index_dir, "index.faiss")):
            self.vector_db = FAISS.load_local(
                self.index_dir,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            self.vector_db = None

    def similarity_search(self, query: str, top_k: int = 5, filter_dict: Optional[Dict[str, Any]] = None) -> List[Document]:
        if not self.vector_db:
            self._load_index()
            if not self.vector_db:
                return []

        # Retrieve a slightly larger pool for post-filtering if metadata filters are specified
        fetch_k = top_k * 3 if filter_dict else top_k
        docs = self.vector_db.similarity_search(query, k=fetch_k)

        if not filter_dict:
            return docs[:top_k]

        # Apply metadata filters
        filtered_docs = []
        for doc in docs:
            match = True
            for key, val in filter_dict.items():
                if val is not None and doc.metadata.get(key) != val:
                    match = False
                    break
            if match:
                filtered_docs.append(doc)
            if len(filtered_docs) >= top_k:
                break

        return filtered_docs

    def add_documents(self, documents: List[Document]) -> None:
        if not self.vector_db:
            self.vector_db = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_db.add_documents(documents)
        os.makedirs(self.index_dir, exist_ok=True)
        self.vector_db.save_local(self.index_dir)

vector_store = FAISSVectorStore()
