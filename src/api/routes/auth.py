from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.db.session import get_db
from src.db.models import User, ComplianceAuditLog
from src.core.security import verify_password, get_password_hash, create_access_token, decode_access_token, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: Optional[str] = "citizen"
    language_preference: Optional[str] = "en"

class UserLoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    if not token:
        # For public demo queries, allow anonymous default access
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user = db.query(User).filter(User.id == user_id).first()
    return user

@router.post("/register", response_model=TokenResponse)
def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already registered.")
    
    new_user = User(
        email=req.email,
        hashed_password=get_password_hash(req.password),
        full_name=req.full_name,
        role=req.role or "citizen",
        language_preference=req.language_preference or "en"
    )
    db.add(new_user)
    
    # Audit log
    audit = ComplianceAuditLog(
        user_id=req.email,
        action="USER_REGISTRATION",
        resource_id="AUTH",
        details=f"New user registered with role {req.role}"
    )
    db.add(audit)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(subject=new_user.id, role=new_user.role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role,
            "language_preference": new_user.language_preference
        }
    }

@router.post("/login", response_model=TokenResponse)
def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token(subject=user.id, role=user.role)
    
    # Audit log
    audit = ComplianceAuditLog(
        user_id=user.email,
        action="USER_LOGIN",
        resource_id="AUTH",
        details="User successfully authenticated."
    )
    db.add(audit)
    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "language_preference": user.language_preference
        }
    }

@router.get("/me")
def get_profile(current_user: Optional[User] = Depends(get_current_user)):
    if not current_user:
        # Return guest profile
        return {
            "id": "guest-user",
            "email": "guest@nyaya.gov.in",
            "full_name": "Guest Citizen",
            "role": "citizen",
            "language_preference": "en"
        }
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "language_preference": current_user.language_preference
    }
