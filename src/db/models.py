import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from src.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="citizen")  # citizen, advocate, judicial_clerk, admin
    language_preference = Column(String(10), default="en")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    queries = relationship("QueryHistory", back_populates="user", cascade="all, delete-orphan")
    drafts = relationship("LegalDraft", back_populates="user", cascade="all, delete-orphan")
    outcomes = relationship("OutcomeAnalysis", back_populates="user", cascade="all, delete-orphan")

class LegalSource(Base):
    __tablename__ = "legal_sources"
    
    id = Column(String(100), primary_key=True)  # e.g., BNS_103, CONST_21, SC_2022_ANTIL
    title = Column(String(255), nullable=False, index=True)
    citation = Column(String(255), nullable=False, index=True)
    act_code = Column(String(100), nullable=False, index=True)  # BNS, IPC, BNSS, CrPC, BSA, CONST, DPDP, CPA, RTI
    section = Column(String(100), nullable=True)  # Section 103, Article 21, etc.
    enactment_year = Column(Integer, nullable=True)
    legal_text = Column(Text, nullable=False)
    court = Column(String(100), nullable=True)  # Supreme Court of India, Delhi High Court, etc.
    bench = Column(String(100), nullable=True)  # Division Bench, Constitution Bench, etc.
    ratio_decidendi = Column(Text, nullable=True)
    source_type = Column(String(50), default="statute")  # statute, constitution, precedent, regulation
    created_at = Column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, txt, docx
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    extracted_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    risk_score = Column(Float, default=0.0)  # 0.0 to 10.0
    key_clauses = Column(JSON, default=dict)
    vulnerabilities = Column(JSON, default=list)
    status = Column(String(50), default="processed")  # uploaded, processing, processed, failed
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="documents")

class QueryHistory(Base):
    __tablename__ = "query_history"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    query_text = Column(Text, nullable=False)
    detected_language = Column(String(10), default="en")
    target_language = Column(String(10), default="en")
    intent = Column(String(100), default="STATUTE_QUERY")
    retrieved_sources = Column(JSON, default=list)
    answer = Column(Text, nullable=False)
    citations = Column(JSON, default=list)
    confidence_score = Column(Float, default=0.95)
    irac_breakdown = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="queries")

class LegalDraft(Base):
    __tablename__ = "legal_drafts"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    template_type = Column(String(100), nullable=False)  # bail_application, legal_notice, rti_application, consumer_complaint, mutual_divorce, affidavit
    title = Column(String(255), nullable=False)
    form_data = Column(JSON, default=dict)
    generated_content = Column(Text, nullable=False)
    format_type = Column(String(50), default="markdown")
    status = Column(String(50), default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="drafts")

class OutcomeAnalysis(Base):
    __tablename__ = "outcome_analyses"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    case_title = Column(String(255), nullable=False)
    offence_type = Column(String(100), nullable=False)
    applied_sections = Column(JSON, default=list)
    factors = Column(JSON, default=dict)  # criminal_antecedents, custody_days, max_penalty, etc.
    predicted_outcome = Column(String(100), nullable=False)  # e.g., High Likelihood of Bail, Conditional Bail
    confidence = Column(Float, default=0.85)  # 0.0 to 1.0
    probability_score = Column(Float, default=75.0)  # 0 to 100%
    reasoning = Column(Text, nullable=False)
    sc_guidelines = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="outcomes")

class ComplianceAuditLog(Base):
    __tablename__ = "compliance_audit_logs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(255), default="ANONYMOUS")
    action = Column(String(100), nullable=False)
    resource_id = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    ip_address = Column(String(100), default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.utcnow)
