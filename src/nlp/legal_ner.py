import re
from typing import Dict, List, Any

class IndianLegalNER:
    """
    Named Entity Recognition engine optimized for Indian Legal Entities:
    - STATUTES (Acts and Codes)
    - PROVISIONS (Sections, Articles, Orders, Rules)
    - COURTS (Supreme Court, High Courts, District/Sessions Courts)
    - OFFENCES (Theft, Murder, Cheating, Defamation, Hurt, etc.)
    - REMEDIES (Bail, Anticipatory Bail, Injunction, Quashing, Habeas Corpus)
    - PENALTIES (Life imprisonment, Death penalty, Fine, Community service)
    """

    ACT_PATTERNS = [
        r'\b(?:Bharatiya\s+Nyaya\s+Sanhita|BNS)(?:\s*,?\s*2023)?\b',
        r'\b(?:Bharatiya\s+Nagarik\s+Suraksha\s+Sanhita|BNSS)(?:\s*,?\s*2023)?\b',
        r'\b(?:Bharatiya\s+Sakshya\s+Adhiniyam|BSA)(?:\s*,?\s*2023)?\b',
        r'\b(?:Indian\s+Penal\s+Code|IPC)(?:\s*,?\s*1860)?\b',
        r'\b(?:Code\s+of\s+Criminal\s+Procedure|CrPC)(?:\s*,?\s*1973)?\b',
        r'\b(?:Indian\s+Evidence\s+Act|IEA)(?:\s*,?\s*1872)?\b',
        r'\bConstitution(?:\s+of\s+India)?\b',
        r'\b(?:Digital\s+Personal\s+Data\s+Protection\s+Act|DPDP(?:\s+Act)?)(?:\s*,?\s*2023)?\b',
        r'\b(?:Consumer\s+Protection\s+Act|CPA)(?:\s*,?\s*2019)?\b',
        r'\b(?:Right\s+to\s+Information\s+Act|RTI(?:\s+Act)?)(?:\s*,?\s*2005)?\b',
        r'\b(?:Negotiable\s+Instruments\s+Act|NI\s+Act)\b',
        r'\b(?:Arbitration\s+and\s+Conciliation\s+Act)\b'
    ]

    PROVISION_PATTERNS = [
        r'\b(?:Section|Sec\.?|धारा|कलम)\s+(\d+[A-Za-z]?(?:\(\d+\))*(?:\([a-z]\))*)',
        r'\b(?:Article|Art\.?|अनुच्छेद)\s+(\d+[A-Za-z]?(?:\(\d+\))*(?:\([a-z]\))*)',
        r'\b(?:Order\s+[XVICDLM]+\s+Rule\s+\d+)\b'
    ]

    COURT_PATTERNS = [
        r'\b(?:Supreme\s+Court(?:\s+of\s+India)?|सर्वोच्च\s+न्यायालय)\b',
        r'\b(?:High\s+Court(?:\s+of\s+[A-Za-z\s]+)?|उच्च\s+न्यायालय)\b',
        r'\b(?:Sessions\s+Court|District\s+Court|Magistrate\s+Court)\b',
        r'\b(?:Consumer\s+Disputes\s+Redressal\s+Commission|NCLT|NCLAT)\b'
    ]

    OFFENCE_PATTERNS = [
        r'\b(?:theft|murder|culpable\s+homicide|cheating|fraud|rape|kidnapping|criminal\s+breach\s+of\s+trust|extortion|robbery|dacoity|criminal\s+intimidation|assault|hurt|grevious\s+hurt|defamation|cybercrime)\b',
        r'\b(?:चोरी|हत्या|धोखाधड़ी|अपहरण|हमला|मानहानि)\b'
    ]

    REMEDY_PATTERNS = [
        r'\b(?:regular\s+bail|anticipatory\s+bail|default\s+bail|interim\s+bail|discharge|quashing|habeas\s+corpus|mandamus|certiorari|injunction|damages)\b',
        r'\b(?:जमानत|अग्रिम\s+जमानत|अंतरिम\s+जमानत|दोषमुक्ति)\b'
    ]

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        entities: Dict[str, List[str]] = {
            "statutes": [],
            "provisions": [],
            "courts": [],
            "offences": [],
            "remedies": []
        }

        # Statutes
        for pat in self.ACT_PATTERNS:
            matches = re.findall(pat, text, re.IGNORECASE)
            entities["statutes"].extend(matches)

        # Provisions (Sections / Articles)
        for pat in self.PROVISION_PATTERNS:
            matches = re.findall(pat, text, re.IGNORECASE)
            entities["provisions"].extend(matches)

        # Courts
        for pat in self.COURT_PATTERNS:
            matches = re.findall(pat, text, re.IGNORECASE)
            entities["courts"].extend(matches)

        # Offences
        for pat in self.OFFENCE_PATTERNS:
            matches = re.findall(pat, text, re.IGNORECASE)
            entities["offences"].extend(matches)

        # Remedies
        for pat in self.REMEDY_PATTERNS:
            matches = re.findall(pat, text, re.IGNORECASE)
            entities["remedies"].extend(matches)

        # Clean duplicates while preserving order
        for key in entities:
            seen = set()
            unique_list = []
            for item in entities[key]:
                item_str = str(item).strip()
                if item_str.lower() not in seen:
                    seen.add(item_str.lower())
                    unique_list.append(item_str)
            entities[key] = unique_list

        return entities

legal_ner = IndianLegalNER()
