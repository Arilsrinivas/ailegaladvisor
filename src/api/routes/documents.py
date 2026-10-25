import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from src.db.session import get_db
from src.db.models import Document, User, ComplianceAuditLog
from src.api.routes.auth import get_current_user
from src.core.config import settings
from src.ai_engine.document_analyzer import document_analyzer

router = APIRouter(prefix="/documents", tags=["Document Ingestion & Analysis"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".pdf", ".txt", ".docx", ".md"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a PDF or TXT document.")

    safe_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    # Extract and Analyze Document
    try:
        extracted_text = document_analyzer.extract_text_from_file(file_path)
        analysis = document_analyzer.analyze_text(extracted_text, filename=file.filename)
    except Exception as e:
        extracted_text = ""
        analysis = {
            "summary": f"Extraction notice: {str(e)}",
            "risk_score": 3.0,
            "key_clauses": {},
            "vulnerabilities": []
        }

    # Save to Database
    user_id = current_user.id if current_user else None
    doc_record = Document(
        user_id=user_id,
        filename=file.filename,
        file_type=file_ext.replace(".", ""),
        file_path=file_path,
        file_size=file_size,
        extracted_text=extracted_text,
        summary=analysis["summary"],
        risk_score=analysis["risk_score"],
        key_clauses=analysis["key_clauses"],
        vulnerabilities=analysis["vulnerabilities"],
        status="processed"
    )
    db.add(doc_record)

    audit = ComplianceAuditLog(
        user_id=current_user.email if current_user else "CITIZEN_GUEST",
        action="DOCUMENT_UPLOAD_AND_ANALYZE",
        resource_id=file.filename,
        details=f"Analyzed {file_size} bytes. Risk score: {analysis['risk_score']}."
    )
    db.add(audit)
    db.commit()
    db.refresh(doc_record)

    return {
        "id": doc_record.id,
        "filename": doc_record.filename,
        "file_size": doc_record.file_size,
        "risk_score": doc_record.risk_score,
        "summary": doc_record.summary,
        "key_clauses": doc_record.key_clauses,
        "vulnerabilities": doc_record.vulnerabilities,
        "created_at": doc_record.created_at
    }

@router.get("/")
def list_documents(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    query = db.query(Document)
    if current_user:
        query = query.filter(Document.user_id == current_user.id)
    return query.order_by(Document.created_at.desc()).all()

@router.get("/{doc_id}")
def get_document(
    doc_id: str,
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return doc

@router.post("/analyze-text")
@router.post("/summarize")
def analyze_raw_text(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    raw_text = payload.get("text") or payload.get("content") or ""
    title = payload.get("title", "Contract Agreement")
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    analysis = document_analyzer.analyze_text(raw_text, filename=title)
    return analysis
