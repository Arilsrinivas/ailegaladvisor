from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from src.db.session import get_db
from src.db.models import LegalSource
from src.ai_engine.hybrid_retriever import hybrid_retriever

router = APIRouter(prefix="/precedents", tags=["Legal Precedents & Judgments"])

@router.get("/search")
def search_precedents(
    q: Optional[str] = Query(None, description="Search terms or legal concept"),
    court: Optional[str] = Query(None, description="Filter by Court"),
    source_type: Optional[str] = Query(None, description="statute or precedent"),
    year_min: Optional[int] = Query(None, description="Minimum enactment/judgment year"),
    year_max: Optional[int] = Query(None, description="Maximum enactment/judgment year"),
    db: Session = Depends(get_db)
):
    query_builder = db.query(LegalSource)

    if source_type:
        query_builder = query_builder.filter(LegalSource.source_type == source_type)
    
    if court:
        query_builder = query_builder.filter(LegalSource.court.ilike(f"%{court}%"))

    if year_min:
        query_builder = query_builder.filter(LegalSource.enactment_year >= year_min)

    if year_max:
        query_builder = query_builder.filter(LegalSource.enactment_year <= year_max)

    if q and q.strip():
        # Hybrid semantic search via vector engine
        vector_results = hybrid_retriever.search(q, top_k=10)
        found_ids = [r["id"] for r in vector_results]
        
        # Also keyword match from SQL
        kw_matches = query_builder.filter(
            (LegalSource.title.ilike(f"%{q}%")) |
            (LegalSource.legal_text.ilike(f"%{q}%")) |
            (LegalSource.ratio_decidendi.ilike(f"%{q}%")) |
            (LegalSource.citation.ilike(f"%{q}%"))
        ).all()
        
        kw_dict = {item.id: item for item in kw_matches}
        
        # Combine prioritizing hybrid rank
        combined = []
        seen = set()
        for r in vector_results:
            source = db.query(LegalSource).filter(LegalSource.id == r["id"]).first()
            if source and source.id not in seen:
                seen.add(source.id)
                combined.append(source)
                
        for s_id, source in kw_dict.items():
            if s_id not in seen:
                seen.add(s_id)
                combined.append(source)

        return combined

    return query_builder.order_by(LegalSource.enactment_year.desc().nullslast()).limit(25).all()

@router.get("/{source_id}")
def get_precedent_details(source_id: str, db: Session = Depends(get_db)):
    item = db.query(LegalSource).filter(LegalSource.id == source_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Legal source or precedent not found.")
    return item
