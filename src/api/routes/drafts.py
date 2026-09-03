from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from src.db.session import get_db
from src.db.models import LegalDraft, User, ComplianceAuditLog
from src.api.routes.auth import get_current_user
from src.ai_engine.legal_drafter import legal_drafter

router = APIRouter(prefix="/drafts", tags=["Structured Legal Drafting"])

class DraftGenerateRequest(BaseModel):
    template_type: str
    title: Optional[str] = None
    form_data: Dict[str, Any]

@router.get("/templates")
def list_templates():
    return legal_drafter.get_templates()

@router.post("/generate")
def generate_draft(
    req: DraftGenerateRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    try:
        content = legal_drafter.generate_draft(req.template_type, req.form_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Draft generation failed: {str(e)}")

    default_title = req.title or f"{req.template_type.replace('_', ' ').title()} - {req.form_data.get('applicant_name', req.form_data.get('sender_name', 'Legal Draft'))}"
    user_id = current_user.id if current_user else None

    draft_record = LegalDraft(
        user_id=user_id,
        template_type=req.template_type,
        title=default_title,
        form_data=req.form_data,
        generated_content=content,
        format_type="markdown",
        status="completed"
    )
    db.add(draft_record)

    audit = ComplianceAuditLog(
        user_id=current_user.email if current_user else "CITIZEN_GUEST",
        action="LEGAL_DRAFT_GENERATION",
        resource_id=req.template_type,
        details=f"Generated draft for {default_title}."
    )
    db.add(audit)
    db.commit()
    db.refresh(draft_record)

    return draft_record

@router.get("/")
def list_drafts(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    query = db.query(LegalDraft)
    if current_user:
        query = query.filter(LegalDraft.user_id == current_user.id)
    return query.order_by(LegalDraft.created_at.desc()).all()

@router.get("/{draft_id}")
def get_draft(draft_id: str, db: Session = Depends(get_db)):
    draft = db.query(LegalDraft).filter(LegalDraft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found.")
    return draft
