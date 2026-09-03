import os
import re
from typing import Dict, List, Any

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

class DocumentAnalyzer:
    """
    Analyzes legal documents (Contracts, NDAs, Service Agreements, Charge Sheets, FIRs).
    Extracts text, identifies key clauses, detects adversarial vulnerabilities (CLAUSE framework),
    evaluates DPDP 2023 compliance, and computes risk scores.
    """

    CLAUSE_PATTERNS = {
        "termination": [
            r'(?:termination|terminate|cancellation|right\s+to\s+terminate)[^\.\n]+(?:\.|\n)',
            r'either\s+party\s+may\s+terminate[^\.\n]+'
        ],
        "liability_indemnity": [
            r'(?:indemnify|indemnification|hold\s+harmless|limitation\s+of\s+liability)[^\.\n]+(?:\.|\n)',
            r'in\s+no\s+event\s+shall\s+(?:either\s+party|supplier)[^\.\n]+'
        ],
        "dispute_resolution": [
            r'(?:arbitration|dispute\s+resolution|governing\s+law|jurisdiction)[^\.\n]+(?:\.|\n)',
            r'courts\s+at\s+[A-Za-z\s]+\s+shall\s+have\s+exclusive\s+jurisdiction[^\.\n]+'
        ],
        "confidentiality_dpdp": [
            r'(?:confidential\s+information|data\s+protection|personal\s+data|dpdp|privacy)[^\.\n]+(?:\.|\n)',
            r'reasonable\s+security\s+safeguards[^\.\n]+'
        ],
        "intellectual_property": [
            r'(?:intellectual\s+property|ipr|proprietary\s+rights|patents?|trademarks?)[^\.\n]+(?:\.|\n)'
        ]
    }

    def extract_text_from_file(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            text = ""
            if fitz:
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text() + "\n"
                doc.close()
            else:
                from pypdf import PdfReader
                reader = PdfReader(file_path)
                for page in reader.pages:
                    text += (page.extract_text() or "") + "\n"
            return text.strip()
        elif ext in [".txt", ".md", ".json"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()

    def analyze_text(self, text: str, filename: str = "document.pdf") -> Dict[str, Any]:
        if not text or not text.strip():
            return {
                "summary": "Document appears empty or unreadable.",
                "risk_score": 0.0,
                "key_clauses": {},
                "vulnerabilities": []
            }

        text_clean = text.replace("\r", " ")
        lower_text = text_clean.lower()

        # 1. Extract Key Clauses
        extracted_clauses: Dict[str, List[str]] = {}
        for clause_name, patterns in self.CLAUSE_PATTERNS.items():
            matches = []
            for pat in patterns:
                found = re.findall(pat, text_clean, re.IGNORECASE)
                for f in found:
                    cleaned_str = str(f).strip()
                    if len(cleaned_str) > 20 and cleaned_str not in matches:
                        matches.append(cleaned_str[:300])
            extracted_clauses[clause_name] = matches[:3]

        # 2. Loophole & Vulnerability Detection (CLAUSE framework)
        vulnerabilities: List[Dict[str, Any]] = []
        risk_score = 2.0  # Base standard risk

        # Check A: DPDP 2023 Compliance
        if "personal data" in lower_text or "user data" in lower_text:
            if "dpdp" not in lower_text and "reasonable security safeguards" not in lower_text:
                risk_score += 2.5
                vulnerabilities.append({
                    "type": "REGULATORY_COMPLIANCE_RISK",
                    "severity": "HIGH",
                    "title": "Missing Mandatory DPDP Act 2023 Data Protection Safeguards",
                    "description": "Document deals with personal data processing but lacks statutory compliance covenants mandated under Section 8(5) of the DPDP Act 2023 (penalty exposure up to ₹250 Cr).",
                    "remedy": "Incorporate explicit Data Processor contractual obligations, data breach notification protocols within 72 hours, and reasonable security safeguards."
                })

        # Check B: Asymmetric Termination
        if "unilateral" in lower_text or ("terminate without cause" in lower_text and "exclusive right" in lower_text):
            risk_score += 2.0
            vulnerabilities.append({
                "type": "COMMERCIAL_EXPOSURE",
                "severity": "HIGH",
                "title": "Unilateral / Asymmetric Termination Clause",
                "description": "One party holds unconditional right to terminate without adequate notice, creating operational instability.",
                "remedy": "Ensure mutual bilateral termination covenants with minimum 30-day cure period."
            })

        # Check C: Arbitration Seat vs Venue Ambiguity
        if "arbitration" in lower_text:
            if "seat" not in lower_text and "venue" in lower_text:
                risk_score += 1.5
                vulnerabilities.append({
                    "type": "JURISDICTION_AMBIGUITY",
                    "severity": "MEDIUM",
                    "title": "Seat vs Venue Ambiguity in Arbitration Clause",
                    "description": "Agreement specifies 'venue' without explicitly anchoring the juridical 'seat', creating high risk of jurisdictional litigation under Arbitration & Conciliation Act 1996 (*BGS SGS Soma*).",
                    "remedy": "Expressly designate both seat and venue: 'The seat and venue of arbitration shall be New Delhi, India.'"
                })
        else:
            vulnerabilities.append({
                "type": "DISPUTE_RESOLUTION_OMISSION",
                "severity": "MEDIUM",
                "title": "Absence of Alternative Dispute Resolution (ADR) Clause",
                "description": "No formal arbitration or mediation tier provided, leaving parties exposed to protracted court litigation.",
                "remedy": "Insert structured 2-tier dispute resolution: (1) Senior executive mediation (30 days); (2) Sole arbitrator under ACA 1996."
            })

        # Check D: Liability Cap
        if "indemnif" in lower_text and "consequential damages" not in lower_text and "limitation of liability" not in lower_text:
            risk_score += 2.0
            vulnerabilities.append({
                "type": "FINANCIAL_EXPOSURE",
                "severity": "HIGH",
                "title": "Uncapped Indemnity / Missing Liability Cap",
                "description": "Indemnification obligations are open-ended with no overall financial ceiling or exclusion of consequential damages.",
                "remedy": "Insert an aggregate liability cap tied to fees paid over the preceding 12 months."
            })

        risk_score = round(min(10.0, max(1.0, risk_score)), 1)

        # 3. Generate Executive Summary
        word_count = len(text.split())
        summary_points = [
            f"**Document Profile**: {filename} ({word_count:,} words).",
            f"**Risk Evaluation**: Overall Risk Score of **{risk_score}/10** with **{len(vulnerabilities)} flagged vulnerabilities**.",
            f"**Core Clauses**: Identified {sum(len(v) for v in extracted_clauses.values())} key contractual covenants across termination, liability, dispute resolution, and data protection.",
        ]
        if vulnerabilities:
            summary_points.append(f"**Primary Action Required**: {vulnerabilities[0]['title']}.")

        summary = "\n\n".join(summary_points)

        return {
            "summary": summary,
            "risk_score": risk_score,
            "key_clauses": extracted_clauses,
            "vulnerabilities": vulnerabilities,
            "word_count": word_count
        }

document_analyzer = DocumentAnalyzer()
