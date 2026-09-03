import os
import pickle
from rank_bm25 import BM25Okapi
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class HybridRetrievalEngine:
    """
    Implements a real Hybrid RAG (Dense + Sparse) for Indian Law.
    """
    def __init__(self, vector_db_path="data/faiss_index", bm25_path="data/bm25_index.pkl"):
        self.vector_db_path = vector_db_path
        self.bm25_path = bm25_path
        # Specifying a local cache folder to ensure offline availability
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_folder="./models/embeddings"
        )
        
        # Load or initialize vector DB
        if os.path.exists(vector_db_path):
            self.vector_db = FAISS.load_local(vector_db_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            self.vector_db = None

        # Load or initialize BM25
        if os.path.exists(bm25_path):
            with open(bm25_path, 'rb') as f:
                data = pickle.load(f)
                self.bm25 = data["bm25"]
                self.documents = data["documents"]
        else:
            self.bm25 = None
            self.documents = []

    def search(self, query, top_k=5):
        """
        Performs hybrid search by combining results from FAISS and BM25.
        """
        if not self.vector_db or not self.bm25:
            print("[Warning] Indices not initialized. Run ingest_laws.py first.")
            return []

        # 1. Dense Retrieval (FAISS)
        dense_results = self.vector_db.similarity_search(query, k=top_k*2)
        
        # 2. Sparse Retrieval (BM25)
        tokenized_query = query.lower().split()
        sparse_hits = self.bm25.get_top_n(tokenized_query, self.documents, n=top_k*2)
        
        # 3. Reciprocal Rank Fusion (Simple Merging for Demo)
        seen_content = set()
        final_results = []
        
        # Add sparse hits first (high precision for section numbers)
        for hit in sparse_hits:
            if hit not in seen_content:
                final_results.append(hit)
                seen_content.add(hit)
        
        # Add dense hits (semantic coverage)
        for doc in dense_results:
            if doc.page_content not in seen_content:
                final_results.append(doc.page_content)
                seen_content.add(doc.page_content)

        return final_results[:top_k]

class HeadTailContextManager:
    """
    Implements the 'Head+Tail' strategy for long-context judgments.
    """
    def __init__(self, head_limit=1500, tail_limit=1500):
        self.head_limit = head_limit
        self.tail_limit = tail_limit

    def process_document(self, text):
        if len(text) <= (self.head_limit + self.tail_limit):
            return text
        
        head = text[:self.head_limit]
        tail = text[-self.tail_limit:]
        
        return f"{head}\n\n[... OMITTED MIDDLE FOR CONTEXT EFFICIENCY ...]\n\n{tail}"
