# AI Legal Advisor (Nyaya AI)
### Production-Quality Multilingual AI Legal Assistance Platform for the Indian Judiciary

**AI Legal Advisor** is an AI-powered legal assistance, document analysis, citation verification, and research platform specialized for the Indian legal ecosystem. Grounded in the newly enacted 2023/2024 reform acts—**Bharatiya Nyaya Sanhita (BNS)**, **Bharatiya Nagarik Suraksha Sanhita (BNSS)**, **Bharatiya Sakshya Adhiniyam (BSA)**, alongside the **Constitution of India** and the **Digital Personal Data Protection (DPDP) Act 2023**—the platform ensures zero-trust citation verification and structured IRAC legal reasoning.

---

## Key Capabilities

1. **AI Legal Consultation & Grounded IRAC Research**:
   - Multilingual query processing with automatic language detection across **8 Indian languages** (English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada).
   - Hybrid Dense-Sparse vector retrieval fusing **FAISS** semantic similarity and **BM25** statutory lexical matching via Reciprocal Rank Fusion (RRF).
   - Authoritative synthesis in formal **IRAC (Issue, Rule, Application, Conclusion)** format with exact legal excerpts.

2. **Zero-Trust Citation Verification**:
   - Automated identification of statutory provisions and judicial precedents cited in legal arguments.
   - Cross-referencing against the authoritative legal database with instant status badges (`VERIFIED`, `REPLACED_BY_NEW_CODE`, `UNVERIFIED`).
   - Automated detection of repealed Indian Penal Code (IPC) and CrPC sections, with bidirectional mapping to new BNS and BNSS sections.

3. **Document Ingestion & CLAUSE Loophole Auditor**:
   - PDF, DOCX, and TXT parsing with PyMuPDF.
   - Automatic Executive Summary and clause classification (Termination, Indemnity, Dispute Resolution, Data Protection).
   - Adversarial CLAUSE framework detecting regulatory non-compliance under DPDP Act 2023 §8(5), asymmetric termination clauses, uncapped indemnities, and arbitration seat vs. venue ambiguities.

4. **Structured Court Document Drafter**:
   - Court-ready templates with dynamic parameter substitution:
     - **Regular Bail Application** (under BNSS §480 / CrPC §439)
     - **Anticipatory Bail Application** (under BNSS §482 / CrPC §438)
     - **Legal Notice for Recovery / Breach of Contract**
     - **Right to Information (RTI) Application** (RTI Act 2005 §6(1))
     - **Consumer Complaint** (Consumer Protection Act 2019 §35)
     - **Mutual Consent Divorce Petition** (Hindu Marriage Act 1955 §13B)
     - **General Sworn Affidavit on Oath**
   - Real-time preview, copy, download, and print-ready view.

5. **Case Outcome & Bail Estimator**:
   - Quantitative factor scoring model evaluating offence severity, custodial duration under BNSS §479, first-time offender thresholds (1/3 sentence), vulnerability proviso under BNSS §480, and parity.
   - Grounded in landmark Supreme Court guidelines (*Satender Kumar Antil v. CBI*, *Arnesh Kumar v. State of Bihar*, *P. Chidambaram v. ED*).
   - Visual probability gauge (0-100%), favorable factors, and prosecution objection mitigations.

6. **Precedent & Case Law Finder**:
   - Semantic and metadata search across landmark Supreme Court and High Court rulings.
   - Filterable by Court, enactment year, and source type, displaying authoritative *Ratio Decidendi*.

7. **DPDP 2025 Security & Compliance Vault**:
   - Enforces the **Seven Pillars of Security**: AES-256 encryption, strict RBAC, 365-day immutable audit log retention, and processor compliance.

---

## Technology Stack

- **Backend**: Python 3.9+, FastAPI, Pydantic v2, SQLAlchemy 2.0.
- **Database**: Dual-engine architecture (Zero-dependency SQLite `data/legaladvisor.db` for instant local execution, with native PostgreSQL support).
- **Retrieval & NLP**: FAISS (dense vector store), BM25 (sparse lexical index), Hugging Face Sentence Transformers (`all-MiniLM-L6-v2`), Legal NER, script-based language detection.
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS v4, Lucide React icons, Axios.
- **DevOps**: Docker, `docker-compose.yml`, multi-stage builds.

---

## Quick Start (Local Execution)

### 1. Prerequisites
- Python 3.9+ installed
- Node.js 18+ and npm installed

### 2. Run Single-Command Launcher
To launch both the FastAPI backend (`http://127.0.0.1:8000`) and the Vite React frontend (`http://localhost:5173`) simultaneously:
```powershell
python run_app.py
```
*The script automatically checks and seeds the database/vector indices on first run, starts both services, and opens the application in your default browser.*

---

## Manual Execution (Independent Services)

### 1. Initialize Database & Vector Indices
```powershell
python -m src.db.init_db
```

### 2. Start FastAPI Backend
```powershell
uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive Swagger API documentation is available at:
👉 **`http://127.0.0.1:8000/docs`**

### 3. Start React Frontend
```powershell
cd frontend
npm install
npm run dev
```
Open your browser at:
👉 **`http://localhost:5173`**

---

## Verification & Automated Tests

Run the complete test suite:
```powershell
python tests/test_api.py
```
Run legacy Article mapping verification:
```powershell
python tests/verify_mapping.py
```

---

## Production Docker Deployment

Deploy with PostgreSQL and Redis:
```bash
docker-compose up --build
```
- API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
