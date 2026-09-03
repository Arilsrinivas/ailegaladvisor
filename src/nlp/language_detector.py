import re
from typing import Dict, Tuple

class LanguageDetector:
    """
    Detects Indian languages and English using Unicode script ranges and character frequency analysis.
    Supported: English (en), Hindi (hi), Tamil (ta), Telugu (te), Bengali (bn), Marathi (mr), Gujarati (gu), Kannada (kn)
    """
    
    # Unicode block ranges
    SCRIPT_RANGES = {
        "hi": (0x0900, 0x097F),  # Devanagari (Hindi, Marathi)
        "bn": (0x0980, 0x09FF),  # Bengali
        "gu": (0x0A80, 0x0AFF),  # Gujarati
        "ta": (0x0B80, 0x0BFF),  # Tamil
        "te": (0x0C00, 0x0C7F),  # Telugu
        "kn": (0x0C80, 0x0CFF),  # Kannada
    }
    
    # Marathi specific common vocabulary markers to distinguish from Hindi in Devanagari
    MARATHI_MARKERS = ["आहे", "नाही", "झाले", "करणे", "केले", "यांचे", "कायद्यानुसार", "जामीन", "खटला"]
    HINDI_MARKERS = ["है", "नहीं", "किया", "कहा", "सकते", "धारा", "जमानत", "अनुसार", "सजा", "अपराध"]

    def detect(self, text: str) -> str:
        """
        Returns language code: 'en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn'
        """
        if not text or not text.strip():
            return "en"
            
        cleaned_text = text.strip()
        script_counts: Dict[str, int] = {lang: 0 for lang in self.SCRIPT_RANGES}
        total_letters = 0

        for char in cleaned_text:
            code = ord(char)
            if (0x0041 <= code <= 0x005A) or (0x0061 <= code <= 0x007A):
                total_letters += 1
                continue
            for lang, (start, end) in self.SCRIPT_RANGES.items():
                if start <= code <= end:
                    script_counts[lang] += 1
                    total_letters += 1
                    break

        if total_letters == 0:
            return "en"

        # Determine dominant script
        dominant_lang = max(script_counts, key=script_counts.get)
        dominant_count = script_counts[dominant_lang]

        # If Indic characters account for >= 15% of the text or highest count is substantial
        if dominant_count > 2 and dominant_count / total_letters >= 0.15:
            if dominant_lang == "hi":
                # Disambiguate Hindi vs Marathi
                text_lower = cleaned_text.lower()
                marathi_hits = sum(1 for m in self.MARATHI_MARKERS if m in text_lower)
                hindi_hits = sum(1 for h in self.HINDI_MARKERS if h in text_lower)
                if marathi_hits > hindi_hits:
                    return "mr"
                return "hi"
            return dominant_lang

        return "en"

    def get_language_name(self, code: str) -> str:
        names = {
            "en": "English",
            "hi": "Hindi (हिंदी)",
            "ta": "Tamil (தமிழ்)",
            "te": "Telugu (తెలుగు)",
            "bn": "Bengali (বাংলা)",
            "mr": "Marathi (मराठी)",
            "gu": "Gujarati (ગુજરાતી)",
            "kn": "Kannada (ಕನ್ನಡ)"
        }
        return names.get(code, "English")

language_detector = LanguageDetector()
