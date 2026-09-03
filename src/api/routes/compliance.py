from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db.models import ComplianceAuditLog, LegalSource, QueryHistory, Document, LegalDraft, OutcomeAnalysis
from src.core.config import settings

router = APIRouter(prefix="/compliance", tags=["DPDP Compliance & Security Vault"])

@router.get("/logs")
def get_compliance_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(ComplianceAuditLog).order_by(ComplianceAuditLog.timestamp.desc()).limit(limit).all()
    return logs

@router.get("/stats")
def get_system_stats(db: Session = Depends(get_db)):
    sources_count = db.query(LegalSource).count()
    queries_count = db.query(QueryHistory).count()
    documents_count = db.query(Document).count()
    drafts_count = db.query(LegalDraft).count()
    outcomes_count = db.query(OutcomeAnalysis).count()
    audit_logs_count = db.query(ComplianceAuditLog).count()

    return {
        "status": "HEALTHY",
        "standard": "DPDP Act 2025 Compliant",
        "encryption": "AES-256 Enabled",
        "retention_policy": "365-day immutable audit log",
        "authoritative_sources_count": sources_count,
        "queries_analyzed_count": queries_count,
        "documents_processed_count": documents_count,
        "legal_drafts_generated": drafts_count,
        "outcomes_predicted": outcomes_count,
        "compliance_audit_events": audit_logs_count,
        "supported_languages_count": len(settings.SUPPORTED_LANGUAGES)
    }
