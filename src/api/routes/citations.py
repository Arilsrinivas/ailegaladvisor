from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from src.ai_engine.citation_verifier import citation_verifier

router = APIRouter(prefix="/citations", tags=["Zero-Trust Citation Verification"])

class CitationVerifyRequest(BaseModel):
    text: str

@router.post("/verify")
def verify_citations_in_text(req: CitationVerifyRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    results = citation_verifier.verify_text_citations(req.text)
    return results
