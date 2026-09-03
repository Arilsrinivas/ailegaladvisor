from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from src.db.session import get_db
from src.db.models import OutcomeAnalysis, User, ComplianceAuditLog
from src.api.routes.auth import get_current_user
from src.ai_engine.outcome_predictor import outcome_predictor

router = APIRouter(prefix="/outcomes", tags=["Case Outcome & Bail Analysis"])

class OutcomePredictRequest(BaseModel):
    case_title: str
    offence_name: str
    applied_sections: List[str]
    max_punishment_years: float = 3.0
    is_first_offender: bool = True
    days_in_custody: int = 0
    is_vulnerable: bool = False
    notice_issued: bool = True
    co_accused_bailed: bool = False
    charge_sheet_filed: bool = False
    flight_risk: str = "low"
    evidence_tier: str = "documentary"

@router.post("/predict")
def predict_case_outcome(
    req: OutcomePredictRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    case_data = req.model_dump()
    result = outcome_predictor.predict_outcome(case_data)

    user_id = current_user.id if current_user else None
    outcome_record = OutcomeAnalysis(
        user_id=user_id,
        case_title=req.case_title,
        offence_type=req.offence_name,
        applied_sections=req.applied_sections,
        factors=case_data,
        predicted_outcome=result["predicted_outcome"],
        confidence=result["confidence"],
        probability_score=result["probability_score"],
        reasoning=result["recommendation"],
        sc_guidelines=result["guidelines_applied"]
    )
    db.add(outcome_record)

    audit = ComplianceAuditLog(
        user_id=current_user.email if current_user else "CITIZEN_GUEST",
        action="OUTCOME_PREDICTION_RUN",
        resource_id=req.case_title,
        details=f"Estimated relief likelihood: {result['probability_score']}% ({result['predicted_outcome']})."
    )
    db.add(audit)
    db.commit()
    db.refresh(outcome_record)

    return {
        "id": outcome_record.id,
        "case_title": req.case_title,
        "probability_score": result["probability_score"],
        "predicted_outcome": result["predicted_outcome"],
        "confidence": result["confidence"],
        "recommendation": result["recommendation"],
        "favorable_factors": result["favorable_factors"],
        "adverse_factors": result["adverse_factors"],
        "guidelines_applied": result["guidelines_applied"],
        "created_at": outcome_record.created_at
    }

@router.get("/history")
def get_outcome_history(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    query = db.query(OutcomeAnalysis)
    if current_user:
        query = query.filter(OutcomeAnalysis.user_id == current_user.id)
    return query.order_by(OutcomeAnalysis.created_at.desc()).limit(15).all()
