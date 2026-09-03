import os
import pickle
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document

from src.core.config import settings
from src.ai_engine.vector_store import vector_store

class HybridRetriever:
    """
    Production-grade Hybrid Dense (FAISS) + Sparse (BM25) Retrieval Engine.
    Employs Reciprocal Rank Fusion (RRF) to combine semantic similarity with lexical keyword precision.
    """
    def __init__(self, bm25_path: str = settings.BM25_INDEX_FILE):
        self.bm25_path = bm25_path
        self.vector_store = vector_store
        self.bm25: Optional[BM25Okapi] = None
        self.bm25_documents: List[str] = []
        self.bm25_metadata: List[Dict[str, Any]] = []
        self._load_bm25()

    def _load_bm25(self):
        if os.path.exists(self.bm25_path):
            with open(self.bm25_path, 'rb') as f:
                data = pickle.load(f)
                self.bm25 = data.get("bm25")
                self.bm25_documents = data.get("documents", [])
                self.bm25_metadata = data.get("metadata", [])

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
        rrf_k: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Executes hybrid retrieval and fuses results via Reciprocal Rank Fusion:
        RRF_Score(d) = 1 / (rrf_k + rank_dense(d)) + 1 / (rrf_k + rank_sparse(d))
        """
        if not self.bm25:
            self._load_bm25()

        # 1. Dense Search (FAISS)
        dense_docs = self.vector_store.similarity_search(query, top_k=top_k * 2, filter_dict=filter_dict)
        
        # 2. Sparse Search (BM25)
        sparse_hits = []
        if self.bm25 and len(self.bm25_documents) > 0:
            tokenized_query = query.lower().split()
            scores = self.bm25.get_scores(tokenized_query)
            # Rank indices by BM25 score descending
            ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
            for idx in ranked_indices[:top_k * 2]:
                if scores[idx] > 0:
                    meta = self.bm25_metadata[idx] if idx < len(self.bm25_metadata) else {}
                    # Filter check
                    if filter_dict:
                        match = all(meta.get(k) == v for k, v in filter_dict.items() if v is not None)
                        if not match:
                            continue
                    sparse_hits.append({
                        "content": self.bm25_documents[idx],
                        "metadata": meta,
                        "bm25_score": scores[idx]
                    })

        # 3. Reciprocal Rank Fusion (RRF)
        doc_scores: Dict[str, float] = {}
        doc_registry: Dict[str, Dict[str, Any]] = {}

        # Dense rank scoring
        for rank, doc in enumerate(dense_docs, 1):
            doc_id = doc.metadata.get("id", doc.page_content[:40])
            rrf_score = 1.0 / (rrf_k + rank)
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + rrf_score
            doc_registry[doc_id] = {
                "id": doc_id,
                "content": doc.page_content,
                "metadata": doc.metadata,
                "source": "dense"
            }

        # Sparse rank scoring
        for rank, hit in enumerate(sparse_hits, 1):
            doc_id = hit["metadata"].get("id", hit["content"][:40])
            rrf_score = 1.0 / (rrf_k + rank)
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + rrf_score
            if doc_id not in doc_registry:
                doc_registry[doc_id] = {
                    "id": doc_id,
                    "content": hit["content"],
                    "metadata": hit["metadata"],
                    "source": "sparse"
                }

        # Sort by final fused RRF score
        sorted_doc_ids = sorted(doc_scores.keys(), key=lambda did: doc_scores[did], reverse=True)

        results = []
        for did in sorted_doc_ids[:top_k]:
            item = doc_registry[did]
            item["score"] = round(doc_scores[did], 4)
            results.append(item)

        return results

hybrid_retriever = HybridRetriever()
