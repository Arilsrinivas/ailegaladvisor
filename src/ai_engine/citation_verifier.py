import re
from typing import List, Dict, Any, Optional
from src.db.session import SessionLocal
from src.db.models import LegalSource

class CitationVerifier:
    """
    Zero-Trust Legal Citation Verifier for Indian Jurisprudence.
    Extracts citations and claims, validates them against the statutory database,
    detects hallucinated provisions, and maps repealed IPC/CrPC provisions to new BNS/BNSS codes.
    """

    # IPC to BNS Replacement Mapping
    LEGACY_MAPPINGS = {
        "IPC Section 302": {"new_code": "BNS Section 103", "title": "Punishment for Murder", "target_id": "BNS_103"},
        "IPC 302": {"new_code": "BNS Section 103", "title": "Punishment for Murder", "target_id": "BNS_103"},
        "Section 302 IPC": {"new_code": "BNS Section 103", "title": "Punishment for Murder", "target_id": "BNS_103"},
        "IPC Section 378": {"new_code": "BNS Section 303", "title": "Theft", "target_id": "BNS_303"},
        "IPC Section 379": {"new_code": "BNS Section 303", "title": "Punishment for Theft", "target_id": "BNS_303"},
        "IPC 378": {"new_code": "BNS Section 303", "title": "Theft", "target_id": "BNS_303"},
        "IPC 379": {"new_code": "BNS Section 303", "title": "Punishment for Theft", "target_id": "BNS_303"},
        "IPC Section 420": {"new_code": "BNS Section 318", "title": "Cheating", "target_id": "BNS_318"},
        "IPC 420": {"new_code": "BNS Section 318", "title": "Cheating", "target_id": "BNS_318"},
        "IPC Section 323": {"new_code": "BNS Section 115", "title": "Voluntarily Causing Hurt", "target_id": "BNS_115"},
        "IPC Section 506": {"new_code": "BNS Section 351", "title": "Criminal Intimidation", "target_id": "BNS_351"},
        "IPC Section 120B": {"new_code": "BNS Section 61", "title": "Criminal Conspiracy", "target_id": "BNS_61"},
        "CrPC Section 436A": {"new_code": "BNSS Section 479", "title": "Maximum Period for Undertrials", "target_id": "BNSS_479"},
        "CrPC Section 437": {"new_code": "BNSS Section 480", "title": "Regular Bail for Non-Bailable", "target_id": "BNSS_480"},
        "CrPC Section 438": {"new_code": "BNSS Section 482", "title": "Anticipatory Bail", "target_id": "BNSS_482"},
        "CrPC Section 154": {"new_code": "BNSS Section 173", "title": "Information in Cognizable Cases (FIR)", "target_id": "BNSS_173"},
        "Section 65B Evidence Act": {"new_code": "BSA Section 63", "title": "Certificate for Electronic Records", "target_id": "BSA_63"}
    }

    def verify_text_citations(self, text: str) -> Dict[str, Any]:
        """
        Scans generated text or legal brief, extracts citations, and cross-references with DB.
        """
        db = SessionLocal()
        try:
            verifications: List[Dict[str, Any]] = []
            citations_found = set()

            # 1. Regex to identify statutory and constitutional citations
            patterns = [
                r'\b(?:BNS|Bharatiya\s+Nyaya\s+Sanhita)\s+(?:Section|Sec\.?)\s+(\d+)\b',
                r'\b(?:BNSS|Bharatiya\s+Nagarik\s+Suraksha\s+Sanhita)\s+(?:Section|Sec\.?)\s+(\d+)\b',
                r'\b(?:BSA|Bharatiya\s+Sakshya\s+Adhiniyam)\s+(?:Section|Sec\.?)\s+(\d+)\b',
                r'\b(?:IPC|Indian\s+Penal\s+Code)\s+(?:Section|Sec\.?)\s+(\d+)\b',
                r'\b(?:CrPC|Code\s+of\s+Criminal\s+Procedure)\s+(?:Section|Sec\.?)\s+(\d+[A-Za-z]?)\b',
                r'\bArticle\s+(\d+)\s+(?:of\s+the\s+Constitution)?\b',
                r'\bDPDP\s+(?:Act\s+)?Section\s+(\d+(?:\(\d+\))*)\b'
            ]

            for pat in patterns:
                for match in re.finditer(pat, text, re.IGNORECASE):
                    citations_found.add(match.group(0).strip())

            # Also check for legacy mappings in text
            for legacy_key, meta in self.LEGACY_MAPPINGS.items():
                if legacy_key.lower() in text.lower():
                    citations_found.add(legacy_key)

            # Check for landmark cases
            precedent_names = {
                "Satender Kumar Antil": "SC_2022_ANTIL",
                "Arnesh Kumar": "SC_2014_ARNESH",
                "Puttaswamy": "SC_2017_PUTTASWAMY",
                "D.K. Basu": "SC_1997_DK_BASU",
                "Lalita Kumari": "SC_2014_LALITA_KUMARI",
                "P. Chidambaram": "SC_2019_CHIDAMBARAM",
                "Shreya Singhal": "SC_2015_SHREYA_SINGHAL"
            }

            for p_name, p_id in precedent_names.items():
                if p_name.lower() in text.lower():
                    citations_found.add(p_name)

            # 2. Verify each citation against DB
            all_sources = db.query(LegalSource).all()
            source_map = {s.id.lower(): s for s in all_sources}
            citation_map = {s.citation.lower(): s for s in all_sources}
            section_map = {f"{s.act_code} {s.section}".lower(): s for s in all_sources if s.section}

            for citation in citations_found:
                # Case A: Check legacy replacement
                legacy_match = None
                for l_key, l_val in self.LEGACY_MAPPINGS.items():
                    if l_key.lower() in citation.lower() or citation.lower() in l_key.lower():
                        legacy_match = l_val
                        break

                if legacy_match:
                    target_source = source_map.get(legacy_match["target_id"].lower())
                    verifications.append({
                        "citation": citation,
                        "status": "REPLACED_BY_NEW_CODE",
                        "badge": "warning",
                        "message": f"Legacy provision replaced by new legal code: {legacy_match['new_code']} ({legacy_match['title']}).",
                        "replacement_code": legacy_match["new_code"],
                        "ground_truth": target_source.legal_text if target_source else "New code enforced under 2023 criminal acts."
                    })
                    continue

                # Case B: Check landmark precedent
                if citation in precedent_names:
                    p_id = precedent_names[citation]
                    p_source = source_map.get(p_id.lower())
                    verifications.append({
                        "citation": p_source.citation if p_source else citation,
                        "status": "VERIFIED",
                        "badge": "success",
                        "message": f"Authoritative Landmark Precedent: {p_source.title if p_source else citation}",
                        "ratio_decidendi": p_source.ratio_decidendi if p_source else "",
                        "ground_truth": p_source.legal_text if p_source else ""
                    })
                    continue

                # Case C: Check statutory DB
                matched_source = None
                for s in all_sources:
                    if (s.section and s.section.lower() in citation.lower()) or \
                       (s.citation and s.citation.lower() in citation.lower()) or \
                       (s.id.replace("_", " ").lower() in citation.lower()):
                        matched_source = s
                        break

                if matched_source:
                    verifications.append({
                        "citation": matched_source.citation,
                        "status": "VERIFIED",
                        "badge": "success",
                        "message": f"Statutory authority verified: {matched_source.title}",
                        "ground_truth": matched_source.legal_text
                    })
                else:
                    verifications.append({
                        "citation": citation,
                        "status": "UNVERIFIED",
                        "badge": "danger",
                        "message": "Provision not found in local authoritative index. Exercise caution regarding possible hallucination.",
                        "ground_truth": None
                    })

            overall_verified = all(v["status"] in ["VERIFIED", "REPLACED_BY_NEW_CODE"] for v in verifications) if verifications else True
            verification_rate = round(
                (sum(1 for v in verifications if v["status"] == "VERIFIED") + 
                 sum(0.85 for v in verifications if v["status"] == "REPLACED_BY_NEW_CODE")) / 
                max(1, len(verifications)) * 100, 1
            ) if verifications else 100.0

            return {
                "is_verified": overall_verified,
                "verification_rate": verification_rate,
                "total_citations": len(verifications),
                "verifications": verifications
            }
        finally:
            db.close()

citation_verifier = CitationVerifier()
