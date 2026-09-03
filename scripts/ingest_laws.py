import os
import pickle
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.retrieval.graph_rag import GraphRAGEngine

load_dotenv()

# Sample Data: BNS, IPC, and Constitution
LAW_DATA = [
    {
        "text": "BNS Section 103 (Punishment for murder): (1) Whoever commits murder shall be punished with death or with imprisonment for life, and shall also be liable to fine.",
        "id": "BNS_103",
        "type": "statute"
    },
    {
        "text": "BNS Section 303 (Theft): Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft.",
        "id": "BNS_303",
        "type": "statute"
    },
    {
        "text": "Article 21 of the Constitution of India: Protection of life and personal liberty. No person shall be deprived of his life or personal liberty except according to procedure established by law.",
        "id": "CONST_21",
        "type": "constitution"
    },
    {
        "text": "DPDP Act 2023 Section 8(5): Data Fiduciary shall protect personal data in its possession or under its control by taking reasonable security safeguards to prevent personal data breach.",
        "id": "DPDP_8_5",
        "type": "statute"
    }
]

def ingest_vector_db():
    print("[Ingestion] Initializing FAISS Vector DB...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    documents = [Document(page_content=item["text"], metadata={"id": item["id"], "type": item["type"]}) for item in LAW_DATA]
    
    vector_db = FAISS.from_documents(documents, embeddings)
    os.makedirs("data", exist_ok=True)
    vector_db.save_local("data/faiss_index")
    print(f"[Ingestion] Saved FAISS index with {len(documents)} documents.")

def ingest_bm25():
    print("[Ingestion] Initializing BM25 Index...")
    texts = [item["text"] for item in LAW_DATA]
    tokenized_corpus = [doc.lower().split() for doc in texts]
    
    from rank_bm25 import BM25Okapi
    bm25 = BM25Okapi(tokenized_corpus)
    
    # Store BOTH the bm25 object and the raw texts
    with open("data/bm25_index.pkl", "wb") as f:
        pickle.dump({"bm25": bm25, "documents": texts}, f)
    print(f"[Ingestion] Saved BM25 index and documents.")

def ingest_graph_db():
    print("[Ingestion] Seeding Neo4j relationships...")
    try:
        graph = GraphRAGEngine()
        if not graph.driver:
            print("[Warning] Neo4j driver not connected. Skipping Graph ingestion.")
            return

        cypher_commands = [
            "MERGE (a:Article {id: 'IPC_302', name: 'IPC Section 302'}) MERGE (b:Section {id: 'BNS_103', name: 'BNS Section 103'}) MERGE (a)-[:REPLACED_BY]->(b)",
            "MERGE (a:Article {id: 'IPC_378', name: 'IPC Section 378'}) MERGE (b:Section {id: 'BNS_303', name: 'BNS Section 303'}) MERGE (a)-[:REPLACED_BY]->(b)",
            "MERGE (c:LegalConcept {name: 'Privacy'}) MERGE (a:Article {id: 'CONST_21'}) MERGE (a)-[:RELEVANT_TO]->(c)"
        ]

        with graph.driver.session() as session:
            for cmd in cypher_commands:
                session.run(cmd)
        
        graph.close()
        print("[Ingestion] Neo4j seed complete.")
    except Exception as e:
        print(f"[Warning] Neo4j seeding failed: {e}. Skipping Graph ingestion.")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    ingest_vector_db()
    ingest_bm25()
    ingest_graph_db()
