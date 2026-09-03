from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from src.db.session import get_db
from src.db.models import QueryHistory, User, ComplianceAuditLog
from src.api.routes.auth import get_current_user
from src.nlp.language_detector import language_detector
from src.nlp.translator import translator
from src.nlp.intent_classifier import intent_classifier
from src.nlp.legal_ner import legal_ner
from src.ai_engine.hybrid_retriever import hybrid_retriever
from src.ai_engine.citation_verifier import citation_verifier
from src.ai_engine.llm_layer import legal_llm

router = APIRouter(prefix="/qa", tags=["Legal Q&A & Research"])

class LegalQueryRequest(BaseModel):
    query: str
    target_language: Optional[str] = None  # None for auto-match or explicit 'hi', 'ta', 'te', etc.
    preferred_jurisdiction: Optional[str] = "All India"

class LegalQueryResponse(BaseModel):
    query: str
    detected_language: str
    detected_language_name: str
    intent: str
    intent_confidence: float
    entities: Dict[str, List[str]]
    answer: str
    irac: Dict[str, str]
    citations: List[Dict[str, Any]]
    verification_summary: Dict[str, Any]
    retrieved_sources: List[Dict[str, Any]]
    model_used: str

@router.post("/query", response_model=LegalQueryResponse)
def handle_legal_query(
    req: LegalQueryRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    user_query = req.query.strip()
    if not user_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # 1. Multilingual Language Detection
    detected_lang = language_detector.detect(user_query)
    lang_name = language_detector.get_language_name(detected_lang)
    target_lang = req.target_language if req.target_language else detected_lang

    # 2. Translation to English for High-Precision Retrieval if needed
    search_query = translator.translate_to_english(user_query, detected_lang)

    # 3. Intent Classification & Legal Named Entity Recognition
    intent_info = intent_classifier.classify(search_query)
    entities = legal_ner.extract_entities(search_query)

    # 4. Hybrid Dense (FAISS) + Sparse (BM25) Retrieval
    sources = hybrid_retriever.search(search_query, top_k=4)

    # 5. IRAC Legal Reasoning & LLM Synthesis
    llm_output = legal_llm.generate_legal_response(
        query=search_query,
        retrieved_sources=sources,
        intent=intent_info["intent"],
        detected_language=detected_lang
    )
    raw_answer = llm_output["answer"]
    irac_dict = llm_output.get("irac", {})

    # 6. Zero-Trust Citation Verification
    verif_results = citation_verifier.verify_text_citations(raw_answer)

    # 7. Localization / Translation back to Target Language if required
    final_answer = raw_answer
    if target_lang != "en":
        final_answer = translator.translate_from_english(raw_answer, target_lang)

    # 8. Persist Query History & DPDP Compliance Audit
    user_id = current_user.id if current_user else None
    history_record = QueryHistory(
        user_id=user_id,
        query_text=user_query,
        detected_language=detected_lang,
        target_language=target_lang,
        intent=intent_info["intent"],
        retrieved_sources=[{"id": s.get("id"), "title": s.get("metadata", {}).get("title"), "citation": s.get("metadata", {}).get("citation")} for s in sources],
        answer=final_answer,
        citations=verif_results.get("verifications", []),
        confidence_score=intent_info["confidence"],
        irac_breakdown=irac_dict
    )
    db.add(history_record)

    audit = ComplianceAuditLog(
        user_id=current_user.email if current_user else "CITIZEN_GUEST",
        action="LEGAL_QUERY_EXECUTION",
        resource_id=f"INTENT_{intent_info['intent']}",
        details=f"Query executed in {lang_name}. Retrieved {len(sources)} legal sources."
    )
    db.add(audit)
    db.commit()

    return {
        "query": user_query,
        "detected_language": detected_lang,
        "detected_language_name": lang_name,
        "intent": intent_info["intent"],
        "intent_confidence": intent_info["confidence"],
        "entities": entities,
        "answer": final_answer,
        "irac": irac_dict,
        "citations": verif_results.get("verifications", []),
        "verification_summary": {
            "is_verified": verif_results.get("is_verified", True),
            "verification_rate": verif_results.get("verification_rate", 100.0),
            "total_citations": verif_results.get("total_citations", 0)
        },
        "retrieved_sources": [
            {
                "id": s.get("id"),
                "title": s.get("metadata", {}).get("title", ""),
                "citation": s.get("metadata", {}).get("citation", ""),
                "act_code": s.get("metadata", {}).get("act_code", ""),
                "section": s.get("metadata", {}).get("section", ""),
                "score": s.get("score", 0.0),
                "excerpt": s.get("content", "")[:280] + "..."
            }
            for s in sources
        ],
        "model_used": llm_output.get("model_used", "Nyaya IRAC Engine")
    }

@router.get("/history")
def get_query_history(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    query = db.query(QueryHistory)
    if current_user:
        query = query.filter(QueryHistory.user_id == current_user.id)
    records = query.order_by(QueryHistory.created_at.desc()).limit(limit).all()
    return records
