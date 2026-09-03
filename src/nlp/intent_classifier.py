import re
from typing import Dict, Any

class LegalIntentClassifier:
    """
    Classifies user queries into discrete legal operational intents:
    - STATUTE_QUERY: Asking about sections, laws, punishments, definitions
    - PRECEDENT_SEARCH: Asking for case laws, judgments, Supreme Court rulings
    - LEGAL_DRAFTING: Seeking to draft a petition, notice, agreement, or affidavit
    - DOCUMENT_ANALYSIS: Asking to analyze, review, or summarize a contract or document
    - OUTCOME_PREDICTION: Asking about chances of bail, acquittal, or case outcome
    - PROCEDURAL_GUIDE: Inquiring about court procedures, filing, summons, limitation periods
    """

    INTENT_KEYWORDS = {
        "LEGAL_DRAFTING": [
            "draft", "template", "format", "notice", "petition", "bail application",
            "rti application", "consumer complaint", "affidavit", "power of attorney",
            "agreement", "contract", "mou", "ड्राफ्ट", "याचिका", "नोटिस", "आवेदन"
        ],
        "OUTCOME_PREDICTION": [
            "chance", "likelihood", "outcome", "probability", "will i get bail",
            "bail chances", "predict", "estimate", "verdict", "risk of conviction",
            "संभावना", "क्या जमानत मिलेगी", "परिणाम"
        ],
        "PRECEDENT_SEARCH": [
            "precedent", "case law", "judgment", "ruling", "supreme court", "high court",
            "ratio decidendi", "cited", "landmark case", "air", "scc", "फैसला", "निर्णय", "केस लॉ"
        ],
        "DOCUMENT_ANALYSIS": [
            "summarize", "analyze", "review", "clause", "agreement review",
            "vulnerability", "risk score", "loophole", "समीक्षा", "विश्लेषण", "संक्षेप"
        ],
        "PROCEDURAL_GUIDE": [
            "procedure", "step by step", "how to file", "limitation period", "jurisdiction",
            "magistrate", "summons", "warrant", "process", "प्रक्रिया", "दायर कैसे करें"
        ],
        "STATUTE_QUERY": [
            "section", "article", "punishment", "bns", "ipc", "bnss", "crpc", "bsa",
            "constitution", "dpdp", "theft", "murder", "cheating", "fine", "धारा", "सजा", "अपराध"
        ]
    }

    def classify(self, query: str) -> Dict[str, Any]:
        text_lower = query.lower()
        scores = {intent: 0.0 for intent in self.INTENT_KEYWORDS}

        for intent, keywords in self.INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[intent] += 1.0

        # Determine highest scoring intent
        best_intent = max(scores, key=scores.get)
        confidence = 0.5 + min(0.48, scores[best_intent] * 0.15) if scores[best_intent] > 0 else 0.65

        # Fallback to STATUTE_QUERY if generic or tied at 0
        if scores[best_intent] == 0:
            best_intent = "STATUTE_QUERY"
            confidence = 0.70

        return {
            "intent": best_intent,
            "confidence": round(confidence, 2),
            "scores": scores
        }

intent_classifier = LegalIntentClassifier()
