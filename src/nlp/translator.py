import os
import re
from typing import Dict, Optional

class MultilingualLegalTranslator:
    """
    Translation abstraction layer with specialized Indian legal domain glossaries.
    Provides bidirectional translation between English and Indic languages:
    Hindi (hi), Tamil (ta), Telugu (te), Bengali (bn), Marathi (mr), Gujarati (gu), Kannada (kn).
    """

    # Comprehensive Legal Lexicon across Indian languages
    LEGAL_LEXICON: Dict[str, Dict[str, str]] = {
        # English: {lang_code: localized_term}
        "bail": {"hi": "जमानत", "mr": "जामीन", "ta": "ஜாமீன்", "te": "బెయిల్", "bn": "জামিন", "gu": "જામીન", "kn": "ಜಾಮೀನು"},
        "anticipatory bail": {"hi": "अग्रिम जमानत", "mr": "आगाऊ जामीन", "ta": "முன்ஜாமீன்", "te": "ముందస్తు బెయిల్", "bn": "আগাম জামিন", "gu": "અગાઉથી જામીન", "kn": "ನಿರೀಕ್ಷಣಾ ಜಾಮೀನು"},
        "theft": {"hi": "चोरी", "mr": "चोरी", "ta": "திருட்டு", "te": "దొంగతనం", "bn": "চুরি", "gu": "ચોરી", "kn": "ಕಳ್ಳತನ"},
        "murder": {"hi": "हत्या", "mr": "खून / हत्या", "ta": "கொலை", "te": "హత్య", "bn": "খুন / হত্যা", "gu": "હત્યા", "kn": "ಕೊಲೆ"},
        "punishment": {"hi": "सजा / दंड", "mr": "शिक्षा / दंड", "ta": "தண்டனை", "te": "శిక్ష", "bn": "শাস্তি", "gu": "સજા", "kn": "ಶಿಕ್ಷೆ"},
        "imprisonment": {"hi": "कारावास", "mr": "कारावास / तुरुंगवास", "ta": "சிறைத்தண்டனை", "te": "కారాగార శిక్ష", "bn": "কারাদণ্ড", "gu": "કેદની સજા", "kn": "ಸೆರೆವಾಸ"},
        "fine": {"hi": "जुर्माना", "mr": "दंड", "ta": "அபராதம்", "te": "జరిమానా", "bn": "জরিমানা", "gu": "દંડ", "kn": "ದಂಡ"},
        "court": {"hi": "न्यायालय / अदालत", "mr": "न्यायालय", "ta": "நீதிமன்றம்", "te": "న్యాయస్థానం", "bn": "আদালত", "gu": "અદાલત", "kn": "ನ್ಯಾಯಾಲಯ"},
        "supreme court": {"hi": "सर्वोच्च न्यायालय", "mr": "सर्वोच्च न्यायालय", "ta": "உச்ச நீதிமன்றம்", "te": "సుప్రీం కోర్టు", "bn": "সুপ্রিম কোর্ট", "gu": "સર્વોચ્ચ અદાલત", "kn": "ಸರ್ವೋಚ್ಚ ನ್ಯಾಯಾಲಯ"},
        "high court": {"hi": "उच्च न्यायालय", "mr": "उच्च न्यायालय", "ta": "உயர் நீதிமன்றம்", "te": "హైకోర్టు", "bn": "হাইকোর্ট", "gu": "વડી અદાલત", "kn": "ಉಚ್ಚ ನ್ಯಾಯಾಲಯ"},
        "section": {"hi": "धारा", "mr": "कलम", "ta": "பிரிவு", "te": "సెక్షన్ / విభాగం", "bn": "ধারা", "gu": "કલમ", "kn": "ಕಲಂ / ವಿಭಾಗ"},
        "article": {"hi": "अनुच्छेद", "mr": "अनुच्छेद", "ta": "சரத்து", "te": "ఆర్టికల్", "bn": "অনুচ্ছেদ", "gu": "અનુચ્છેદ", "kn": "ಅನುಚ್ಛೇದ"},
        "constitution": {"hi": "संविधान", "mr": "संविधान", "ta": "அரசியலமைப்பு", "te": "రాజ్యాంగం", "bn": "সংবিধান", "gu": "બંધારણ", "kn": "ಸಂವಿಧಾನ"},
        "privacy": {"hi": "निजता / गोपनीयता", "mr": "गोपनीयता", "ta": "தனியுரிமை", "te": "గోప్యత", "bn": "গোপনীয়তা", "gu": "ગોપનીયતા", "kn": "ಗೌಪ್ಯತೆ"},
        "first information report": {"hi": "प्राथमिकी (एफआईआर)", "mr": "प्रथम माहिती अहवाल (एफआयआर)", "ta": "முதல் தகவல் அறிக்கை (எஃப்ஐஆர்)", "te": "ఎఫ్ఐఆర్", "bn": "এফআইআর", "gu": "પ્રથમ માહિતી અહેવાલ", "kn": "ಪ್ರಥಮ ಮಾಹಿತಿ ವರದಿ"},
        "fir": {"hi": "एफआईआर", "mr": "एफआयआर", "ta": "எஃப்ஐஆர்", "te": "ఎఫ్ఐఆర్", "bn": "এফআইআর", "gu": "એફઆઈઆર", "kn": "ಎಫ್ಐಆರ್"},
        "cognizable offence": {"hi": "संज्ञेय अपराध", "mr": "दखलपात्र गुन्हा", "ta": "கைது செய்யக்கூடிய குற்றம்", "te": "కాగ్నిజబుల్ నేరం", "bn": "আমলযোগ্য অপরাধ", "gu": "પોલીસ અધિકારનો ગુનો", "kn": "ಕಾಗ್ನಿಜಬಲ್ ಅಪರಾಧ"},
        "non-bailable": {"hi": "गैर-जमानती", "mr": "अजामीनपात्र", "ta": "ஜாமீனில் வெளிவர முடியாத", "te": "నాన్ బెయిలబుల్", "bn": "অ-জামিনযোগ্য", "gu": "બિનજામીનપાત્ર", "kn": "ಜಾಮೀನು ರಹಿತ"},
        "undertrial": {"hi": "विचाराधीन कैदी", "mr": "न्यायप्रविष्ट कैदी", "ta": "விசாரணைக் கைதி", "te": "విచారణ ఖైదీ", "bn": "বিচারাধীন বন্দি", "gu": "વિચારાધીન કેદી", "kn": "ವಿಚಾರಣಾಧೀನ ಕೈದಿ"},
        "cheating": {"hi": "धोखाधड़ी", "mr": "फसवणूक", "ta": "ஏமாற்றுதல்", "te": "మోసం", "bn": "প্রতারণা", "gu": "છેતરપિંડી", "kn": "ವಂಚನೆ"},
        "personal liberty": {"hi": "व्यक्तिगत स्वतंत्रता", "mr": "व्यक्तिगत स्वातंत्र्य", "ta": "தனிநபர் சுதந்திரம்", "te": "వ్యక్తిగత స్వేచ్ఛ", "bn": "ব্যক্তিগত স্বাধীনতা", "gu": "વ્યક્તિગત સ્વતંત્રતા", "kn": "ವೈಯಕ್ತಿಕ ಸ್ವಾತಂತ್ರ್ಯ"}
    }

    # Reverse mapping: {lang: {localized: english}}
    REVERSE_LEXICON: Dict[str, Dict[str, str]] = {}

    def __init__(self):
        self._build_reverse_lexicon()

    def _build_reverse_lexicon(self):
        for eng_term, translations in self.LEGAL_LEXICON.items():
            for lang, localized_term in translations.items():
                if lang not in self.REVERSE_LEXICON:
                    self.REVERSE_LEXICON[lang] = {}
                # Map individual slash terms
                for variant in localized_term.split("/"):
                    v_clean = variant.strip().lower()
                    self.REVERSE_LEXICON[lang][v_clean] = eng_term

    def translate_to_english(self, text: str, source_lang: str) -> str:
        """
        Translates legal queries from an Indic language to English for high-fidelity RAG retrieval.
        """
        if source_lang == "en" or not text.strip():
            return text

        # Replace domain terms using legal lexicon
        english_translated = text
        if source_lang in self.REVERSE_LEXICON:
            # Sort terms by descending length to prevent partial collisions
            sorted_terms = sorted(self.REVERSE_LEXICON[source_lang].keys(), key=len, reverse=True)
            for localized in sorted_terms:
                if localized in english_translated.lower():
                    eng_equiv = self.REVERSE_LEXICON[source_lang][localized]
                    # Case insensitive replace
                    pattern = re.compile(re.escape(localized), re.IGNORECASE)
                    english_translated = pattern.sub(eng_equiv, english_translated)

        # Standard keyword transliterations/helpers
        if source_lang in ["hi", "mr"]:
            hindi_replacements = {
                "धारा": "Section",
                "कलम": "Section",
                "सजा": "punishment",
                "क्या है": "what is",
                "क्या": "what",
                "के तहत": "under",
                "अनुसार": "according to",
                "संविधान": "Constitution",
                "अनुच्छेद": "Article",
                "बीएनएस": "BNS",
                "आईपीसी": "IPC",
                "सीआरपीसी": "CrPC",
                "डीपीडीपी": "DPDP",
                "अधिकार": "right"
            }
            for h_word, e_word in hindi_replacements.items():
                english_translated = english_translated.replace(h_word, e_word)

        return english_translated.strip()

    def translate_from_english(self, text: str, target_lang: str) -> str:
        """
        Translates or localizes legal summaries/responses from English to target Indian language.
        Preserves authoritative section citations and English casing for precise legal references.
        """
        if target_lang == "en" or not text.strip():
            return text

        localized_text = text
        for eng_term, translations in self.LEGAL_LEXICON.items():
            if target_lang in translations:
                target_term = translations[target_lang]
                # Replace whole words
                pattern = re.compile(r'\b' + re.escape(eng_term) + r'\b', re.IGNORECASE)
                # Replace with format: "Translated Term (Original English)" for precision
                localized_text = pattern.sub(f"{target_term}", localized_text)

        # Prepend localized language header notice
        language_headers = {
            "hi": "⚖️ **भारतीय विधि परामर्श (हिन्दी अनुवाद)**:\n\n",
            "mr": "⚖️ **भारतीय विधी सल्लागार (मराठी अनुवाद)**:\n\n",
            "ta": "⚖️ **இந்திய சட்ட ஆலோசகர் (தமிழ் மொழியாக்கம்)**:\n\n",
            "te": "⚖️ **భారతీయ చట్ట సలహాదారు (తెలుగు అనువాదం)**:\n\n",
            "bn": "⚖️ **ভারতীয় আইন উপদেষ্টা (বাংলা অনুবাদ)**:\n\n",
            "gu": "⚖️ **ભારતીય કાયદાકીય સલાહકાર (ગુજરાતી અનુવાદ)**:\n\n",
            "kn": "⚖️ **ಭಾರತೀಯ ಕಾನೂನು ಸಲಹೆಗಾರ (ಕನ್ನಡ ಅನುವಾದ)**:\n\n"
        }

        header = language_headers.get(target_lang, "")
        return f"{header}{localized_text}"

translator = MultilingualLegalTranslator()
