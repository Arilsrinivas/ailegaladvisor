# Nyaya-Orchestrator Retrieval Architecture

This module implements a **Domain-Partitioned Hybrid RAG** integrated with a **Neo4j Knowledge Graph (GraphRAG)** for high-precision legal retrieval.

## Components

### 1. Hybrid RAG (`hybrid_rag.py`)
- **Sparse Retrieval**: Uses BM25 (via ElasticSearch or local ranker) to capture specific legal keywords and section numbers.
- **Dense Retrieval**: Uses Vector Embeddings (HuggingFace/OpenAI) to capture semantic relationships and factual scenarios.
- **Re-ranking**: A Cross-Encoder reresolved the top-20 results from both streams to ensure maximum fidelity.

### 2. GraphRAG (`graph_rag.py`)
- **Schema**: 
  - `(Article)-[:REPLACED_BY]->(BNS_Section)`
  - `(Section)-[:INTERPRETED_BY]->(CaseLaw)`
  - `(CaseLaw)-[:CITES]->(Statute)`
- **Query Logic**: Performs N-hop traversal to find relevant precedents even when semantic similarity is low.

### 3. Head+Tail Strategy (`context_manager.py`)
- Implements the 'Head+Tail' chunking for Supreme Court judgments.
- Retains the first 1000 and last 1000 tokens of a judgment to preserve the **Facts/Issues** and the **Final Ratio/Conclusion**.

## Compliance Logic
- All retrieval queries are logged with a unique `request_id` for DPDP 2025 compliance.
- Metadata is encrypted using AES-256 before storage in the Vector DB.
