from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from src.core.config import settings
from src.api.routes.auth import router as auth_router
from src.api.routes.qa import router as qa_router
from src.api.routes.documents import router as documents_router
from src.api.routes.precedents import router as precedents_router
from src.api.routes.drafts import router as drafts_router
from src.api.routes.outcomes import router as outcomes_router
from src.api.routes.citations import router as citations_router
from src.api.routes.compliance import router as compliance_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-quality AI-powered Multilingual Legal Assistance Platform for the Indian Judiciary (Nyaya AI).",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Timing and Audit Middleware
@app.middleware("http")
async def add_process_time_and_dpdp_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-Sec"] = f"{process_time:.4f}"
    response.headers["X-Compliance-Standard"] = "DPDP-Act-2025"
    response.headers["X-Security-Pillar"] = "Seven-Pillars-Enforced"
    return response

# Include all modular API routers under /api
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(qa_router, prefix=settings.API_V1_STR)
app.include_router(documents_router, prefix=settings.API_V1_STR)
app.include_router(precedents_router, prefix=settings.API_V1_STR)
app.include_router(drafts_router, prefix=settings.API_V1_STR)
app.include_router(outcomes_router, prefix=settings.API_V1_STR)
app.include_router(citations_router, prefix=settings.API_V1_STR)
app.include_router(compliance_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "status": "ONLINE",
        "api_docs": "/docs",
        "version": "2.0.0",
        "jurisdiction": "Republic of India",
        "statutes": ["BNS 2023", "BNSS 2023", "BSA 2023", "Constitution of India", "DPDP Act 2023"],
        "compliance": "DPDP 2025 Seven Security Pillars Active"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time()
    }
