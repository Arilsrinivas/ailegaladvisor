import os
import pickle
from datetime import datetime
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi

from src.core.config import settings
from src.core.security import get_password_hash
from src.db.session import engine, SessionLocal, Base
from src.db.models import User, LegalSource, ComplianceAuditLog

# Comprehensive Indian Legal Sources
STATUTE_AND_PRECEDENT_DATA = [
    # --- BNS (Bharatiya Nyaya Sanhita 2023) ---
    {
        "id": "BNS_103",
        "title": "BNS Section 103 - Punishment for Murder",
        "citation": "Bharatiya Nyaya Sanhita 2023, Section 103",
        "act_code": "BNS",
        "section": "Section 103",
        "enactment_year": 2023,
        "legal_text": "BNS Section 103 (Punishment for murder): (1) Whoever commits murder shall be punished with death or with imprisonment for life, and shall also be liable to fine. (2) When a group of five or more persons acting in concert commits murder on the ground of race, caste or community, sex, place of birth, language, personal belief or any other similar ground, each member of such group shall be punished with death or with imprisonment for life, and shall also be liable to fine. Replaces IPC Section 302.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Mandates capital punishment or life imprisonment for murder. Introduces specific provisions for mob lynching.",
        "source_type": "statute"
    },
    {
        "id": "BNS_303",
        "title": "BNS Section 303 - Theft and Punishment",
        "citation": "Bharatiya Nyaya Sanhita 2023, Section 303",
        "act_code": "BNS",
        "section": "Section 303",
        "enactment_year": 2023,
        "legal_text": "BNS Section 303 (Theft): (1) Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft. (2) Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both. Replaces IPC Section 378 and 379. Community service may be awarded for first-time offenders where stolen value is less than 5,000 rupees.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Defines ingredients of theft: dishonest intention, movable property, without consent, and moving property. Replaces IPC 378/379.",
        "source_type": "statute"
    },
    {
        "id": "BNS_318",
        "title": "BNS Section 318 - Cheating",
        "citation": "Bharatiya Nyaya Sanhita 2023, Section 318",
        "act_code": "BNS",
        "section": "Section 318",
        "enactment_year": 2023,
        "legal_text": "BNS Section 318 (Cheating): Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person... is said to cheat. (4) Whoever cheats and thereby dishonestly induces the person deceived to deliver any property shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine. Replaces IPC Section 415 and 420.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Fraudulent inducement to part with property constitutes cheating with punishment up to 7 years. Replaces IPC 420.",
        "source_type": "statute"
    },
    {
        "id": "BNS_115",
        "title": "BNS Section 115 - Voluntarily Causing Hurt",
        "citation": "Bharatiya Nyaya Sanhita 2023, Section 115",
        "act_code": "BNS",
        "section": "Section 115",
        "enactment_year": 2023,
        "legal_text": "BNS Section 115 (Voluntarily causing hurt): Whoever does any act with the intention of thereby causing hurt to any person, or with the knowledge that he is likely thereby to cause hurt, is said voluntarily to cause hurt. Punishment extends to one year imprisonment or fine up to ten thousand rupees, or both. Replaces IPC Section 323.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Simple hurt is non-cognizable and bailable, punishable with up to 1 year imprisonment.",
        "source_type": "statute"
    },
    {
        "id": "BNS_351",
        "title": "BNS Section 351 - Criminal Intimidation",
        "citation": "Bharatiya Nyaya Sanhita 2023, Section 351",
        "act_code": "BNS",
        "section": "Section 351",
        "enactment_year": 2023,
        "legal_text": "BNS Section 351 (Criminal Intimidation): Whoever threatens another with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested, with intent to cause alarm to that person, commits criminal intimidation. Punishable with imprisonment up to two years or fine or both. Replaces IPC Section 503 and 506.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Threatening injury with intent to cause alarm constitutes criminal intimidation. Replaces IPC 506.",
        "source_type": "statute"
    },
    {
        "id": "BNS_61",
        "title": "BNS Section 61 - Criminal Conspiracy",
        "citation": "Bharatiya Nyaya Sanhita 2023, Section 61",
        "act_code": "BNS",
        "section": "Section 61",
        "enactment_year": 2023,
        "legal_text": "BNS Section 61 (Criminal Conspiracy): (1) When two or more persons agree to do, or cause to be done: (a) an illegal act; or (b) an act which is not illegal by illegal means, such an agreement is designated a criminal conspiracy. Replaces IPC Section 120A and 120B.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Agreement between two or more persons to perform an unlawful act constitutes criminal conspiracy. Replaces IPC 120B.",
        "source_type": "statute"
    },

    # --- BNSS (Bharatiya Nagarik Suraksha Sanhita 2023) ---
    {
        "id": "BNSS_479",
        "title": "BNSS Section 479 - Maximum Period for Undertrial Prisoners",
        "citation": "Bharatiya Nagarik Suraksha Sanhita 2023, Section 479",
        "act_code": "BNSS",
        "section": "Section 479",
        "enactment_year": 2023,
        "legal_text": "BNSS Section 479 (Maximum period for which an undertrial prisoner can be detained): Where a person has, during the period of investigation, inquiry or trial, undergone detention for a period extending up to one-half of the maximum period of imprisonment specified for that offence under that law, he shall be released by the Court on his personal bond with or without sureties. For a first-time offender (who has never been convicted of any offence in the past), the detention period is reduced to one-third of the maximum imprisonment. Does not apply to offences where death or life imprisonment is a specified punishment. Replaces CrPC Section 436A.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "First-time undertrials entitled to mandatory release on personal bond upon completing 1/3 of maximum sentence; others upon completing 1/2. Replaces CrPC 436A.",
        "source_type": "statute"
    },
    {
        "id": "BNSS_480",
        "title": "BNSS Section 480 - Regular Bail for Non-Bailable Offences",
        "citation": "Bharatiya Nagarik Suraksha Sanhita 2023, Section 480",
        "act_code": "BNSS",
        "section": "Section 480",
        "enactment_year": 2023,
        "legal_text": "BNSS Section 480 (When bail may be taken in case of non-bailable offence): When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant... he may be released on bail, but he shall not be so released if there appear reasonable grounds for believing that he has been guilty of an offence punishable with death or imprisonment for life. Provided that the court may direct that a person referred to be released on bail if such person is under the age of sixteen years or is a woman or is sick or infirm. Replaces CrPC Section 437.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Governs judicial discretion for regular bail in non-bailable offences. Carves out special benign consideration for minors, women, sick, and infirm persons. Replaces CrPC 437.",
        "source_type": "statute"
    },
    {
        "id": "BNSS_482",
        "title": "BNSS Section 482 - Anticipatory Bail",
        "citation": "Bharatiya Nagarik Suraksha Sanhita 2023, Section 482",
        "act_code": "BNSS",
        "section": "Section 482",
        "enactment_year": 2023,
        "legal_text": "BNSS Section 482 (Direction for grant of bail to person apprehending arrest): Where any person has reason to believe that he may be arrested on accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction under this section that in the event of such arrest he shall be released on bail. The court considers nature of accusation, criminal antecedents, flight risk, and bona fides. Replaces CrPC Section 438.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Anticipatory bail protects personal liberty against frivolous or motivated arrests. Replaces CrPC 438.",
        "source_type": "statute"
    },
    {
        "id": "BNSS_173",
        "title": "BNSS Section 173 - Information in Cognizable Cases (FIR)",
        "citation": "Bharatiya Nagarik Suraksha Sanhita 2023, Section 173",
        "act_code": "BNSS",
        "section": "Section 173",
        "enactment_year": 2023,
        "legal_text": "BNSS Section 173 (Information in cognizable cases): Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, shall be reduced to writing. Information may also be given electronically (e-FIR) irrespective of territorial jurisdiction (Zero FIR). Preliminary enquiry may be conducted within 14 days before registration of FIR for offences punishable between 3 and 7 years. Replaces CrPC Section 154.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Introduces electronic FIR (e-FIR) and Zero FIR statutory status. Mandates timeline for preliminary enquiry. Replaces CrPC 154.",
        "source_type": "statute"
    },

    # --- BSA (Bharatiya Sakshya Adhiniyam 2023) ---
    {
        "id": "BSA_61",
        "title": "BSA Section 61 - Admissibility of Electronic Records",
        "citation": "Bharatiya Sakshya Adhiniyam 2023, Section 61",
        "act_code": "BSA",
        "section": "Section 61",
        "enactment_year": 2023,
        "legal_text": "BSA Section 61 (Admissibility of electronic records): Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in evidence on the ground that it is an electronic or digital record and such record shall have the same legal effect, validity and enforceability as other document. Replaces Indian Evidence Act 1872 Section 65A.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Confers direct primary evidentiary status to digital and electronic records.",
        "source_type": "statute"
    },
    {
        "id": "BSA_63",
        "title": "BSA Section 63 - Certificate for Electronic Records",
        "citation": "Bharatiya Sakshya Adhiniyam 2023, Section 63",
        "act_code": "BSA",
        "section": "Section 63",
        "enactment_year": 2023,
        "legal_text": "BSA Section 63 (Special provisions as to evidence relating to electronic record): Electronic record printed on paper, stored, recorded or copied in optical or magnetic media shall be deemed to be also a document. Requires a certificate signed by a person in charge of the computer device or an expert. Replaces Indian Evidence Act Section 65B.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Standardizes electronic record certificate requirements. Successor to Section 65B of Indian Evidence Act.",
        "source_type": "statute"
    },

    # --- Constitution of India ---
    {
        "id": "CONST_14",
        "title": "Article 14 - Right to Equality",
        "citation": "Constitution of India, Article 14",
        "act_code": "CONST",
        "section": "Article 14",
        "enactment_year": 1950,
        "legal_text": "Article 14 of the Constitution of India: Equality before law. The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India. Strikes at arbitrariness in state action.",
        "court": "Supreme Court of India",
        "bench": None,
        "ratio_decidendi": "Arbitrariness is an antithesis to equality. Non-arbitrariness pervades the entirety of Article 14.",
        "source_type": "constitution"
    },
    {
        "id": "CONST_19",
        "title": "Article 19 - Protection of Certain Rights Regarding Freedom of Speech, etc.",
        "citation": "Constitution of India, Article 19",
        "act_code": "CONST",
        "section": "Article 19",
        "enactment_year": 1950,
        "legal_text": "Article 19 of the Constitution of India: All citizens shall have the right to freedom of speech and expression; to assemble peaceably and without arms; to form associations or unions; to move freely throughout India; to reside and settle in any part of India; and to practise any profession, trade or business, subject to reasonable restrictions under Clauses (2) to (6).",
        "court": "Supreme Court of India",
        "bench": None,
        "ratio_decidendi": "Fundamental freedoms guaranteed to citizens, subject only to narrowly tailored reasonable restrictions.",
        "source_type": "constitution"
    },
    {
        "id": "CONST_21",
        "title": "Article 21 - Protection of Life and Personal Liberty",
        "citation": "Constitution of India, Article 21",
        "act_code": "CONST",
        "section": "Article 21",
        "enactment_year": 1950,
        "legal_text": "Article 21 of the Constitution of India: Protection of life and personal liberty. No person shall be deprived of his life or personal liberty except according to procedure established by law. Encompasses right to privacy, right to speedy trial, right to bail, and right to dignified livelihood.",
        "court": "Supreme Court of India",
        "bench": None,
        "ratio_decidendi": "Bedrock of fundamental rights. Procedure depriving personal liberty must be just, fair, and reasonable. Speedy trial and bail are integral to Article 21.",
        "source_type": "constitution"
    },
    {
        "id": "CONST_22",
        "title": "Article 22 - Protection Against Arrest and Detention",
        "citation": "Constitution of India, Article 22",
        "act_code": "CONST",
        "section": "Article 22",
        "enactment_year": 1950,
        "legal_text": "Article 22 of the Constitution of India: No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest nor shall he be denied the right to consult, and to be defended by, a legal practitioner of his choice. Every person arrested must be produced before the nearest magistrate within 24 hours.",
        "court": "Supreme Court of India",
        "bench": None,
        "ratio_decidendi": "Mandatory disclosure of grounds of arrest, right to counsel, and production before magistrate within 24 hours.",
        "source_type": "constitution"
    },
    {
        "id": "CONST_32",
        "title": "Article 32 - Remedies for Enforcement of Fundamental Rights (Writs)",
        "citation": "Constitution of India, Article 32",
        "act_code": "CONST",
        "section": "Article 32",
        "enactment_year": 1950,
        "legal_text": "Article 32 of the Constitution of India: The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by Part III is guaranteed. The Supreme Court shall have power to issue directions or orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari.",
        "court": "Supreme Court of India",
        "bench": None,
        "ratio_decidendi": "Constitutional remedy directly enforceable in the Supreme Court for violation of fundamental rights; described as the 'heart and soul' of the Constitution.",
        "source_type": "constitution"
    },

    # --- DPDP Act 2023 ---
    {
        "id": "DPDP_8_5",
        "title": "DPDP Act 2023 Section 8(5) - Mandatory Security Safeguards",
        "citation": "Digital Personal Data Protection Act 2023, Section 8(5)",
        "act_code": "DPDP",
        "section": "Section 8(5)",
        "enactment_year": 2023,
        "legal_text": "DPDP Act 2023 Section 8(5): A Data Fiduciary shall protect personal data in its possession or under its control, including in respect of any processing undertaken by it or on its behalf by a Data Processor, by taking reasonable security safeguards to prevent personal data breach. Non-compliance attracts monetary penalty up to ₹250 crore under Schedule.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Imposes strict liability on Data Fiduciaries to maintain technical and organizational safeguards against data breaches.",
        "source_type": "statute"
    },
    {
        "id": "DPDP_4",
        "title": "DPDP Act 2023 Section 4 - Grounds for Processing Personal Data",
        "citation": "Digital Personal Data Protection Act 2023, Section 4",
        "act_code": "DPDP",
        "section": "Section 4",
        "enactment_year": 2023,
        "legal_text": "DPDP Act 2023 Section 4: A person may process personal data of an individual only in accordance with the provisions of this Act and for a lawful purpose: (a) for which the Data Principal has given her consent; or (b) for certain legitimate uses specified in Section 7.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Personal data processing requires valid consent or explicit statutory legitimate use grounds.",
        "source_type": "statute"
    },

    # --- Consumer Protection Act 2019 & RTI Act 2005 ---
    {
        "id": "CPA_35",
        "title": "Consumer Protection Act 2019 Section 35 - Manner in Which Complaint Shall Be Made",
        "citation": "Consumer Protection Act 2019, Section 35",
        "act_code": "CPA",
        "section": "Section 35",
        "enactment_year": 2019,
        "legal_text": "Consumer Protection Act 2019 Section 35: A complaint, in relation to any goods sold or delivered or agreed to be sold or delivered or any service provided or agreed to be provided, may be filed with a District Commission by the consumer to whom such goods are sold or service provided, or any recognized consumer association. District Commission has jurisdiction up to ₹50 lakh under amended rules.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Provides accessible forum for consumer redressal against deficiency of service or defective goods.",
        "source_type": "statute"
    },
    {
        "id": "RTI_6",
        "title": "RTI Act 2005 Section 6 - Request for Obtaining Information",
        "citation": "Right to Information Act 2005, Section 6(1)",
        "act_code": "RTI",
        "section": "Section 6(1)",
        "enactment_year": 2005,
        "legal_text": "RTI Act 2005 Section 6(1): A person, who desires to obtain any information under this Act, shall make a request in writing or through electronic means in English or Hindi or in the official language of the area, accompanying such fee as may be prescribed, to the Central Public Information Officer or State Public Information Officer. An applicant making request for information shall not be required to give any reason for requesting the information.",
        "court": None,
        "bench": None,
        "ratio_decidendi": "Guarantees citizen's right to information from public authorities without needing to demonstrate locus standi or disclose reason.",
        "source_type": "statute"
    },

    # --- Landmark Supreme Court Precedents ---
    {
        "id": "SC_2022_ANTIL",
        "title": "Satender Kumar Antil v. Central Bureau of Investigation (2022)",
        "citation": "(2022) 10 SCC 51",
        "act_code": "PRECEDENT",
        "section": "Bail Guidelines & Classification",
        "enactment_year": 2022,
        "legal_text": "Supreme Court of India in Satender Kumar Antil v. CBI (2022) 10 SCC 51 laid down comprehensive guidelines on bail categorization: Category A: Offences punishable with imprisonment of 7 years or less - Ordinary course bail on appearance without remand, complying with Arnesh Kumar guidelines. Category B: Offences punishable with death, imprisonment for life, or imprisonment for more than 7 years - Bail decided on merits of evidence, gravity, and antecedents. Category C: Offences punishable under Special Acts (NDPS, PMLA, UAPA) - Subject to statutory negative conditions. Category D: Economic offences not covered by Special Acts. Reaffirmed that bail is the rule and jail is the exception.",
        "court": "Supreme Court of India",
        "bench": "S.K. Kaul & M.M. Sundresh, JJ.",
        "ratio_decidendi": "Bail is the rule, jail is the exception. For offences punishable up to 7 years, undertrials should ordinarily not be taken into custody upon appearance before court if not arrested during investigation.",
        "source_type": "precedent"
    },
    {
        "id": "SC_2014_ARNESH",
        "title": "Arnesh Kumar v. State of Bihar (2014)",
        "citation": "(2014) 8 SCC 273",
        "act_code": "PRECEDENT",
        "section": "Section 41 CrPC / Section 35 BNSS - Mandatory Notice of Appearance",
        "enactment_year": 2014,
        "legal_text": "Supreme Court in Arnesh Kumar v. State of Bihar (2014) 8 SCC 273 held that police officers shall not automatically arrest an accused when an offence punishable with imprisonment for a term which may be less than seven years or which may extend to seven years is alleged. Police must issue a Notice of Appearance (Section 41A CrPC / Section 35(3) BNSS). Arrest must only be made upon recorded satisfaction of reasons such as risk of tampering, flight risk, or prevention of further crime. Magistrates authorizing mechanical detention without independent application of mind face disciplinary proceedings.",
        "court": "Supreme Court of India",
        "bench": "Chandramauli Kr. Prasad & Pinaki Chandra Ghose, JJ.",
        "ratio_decidendi": "Arrest cannot be a routine tool of intimidation. Notice of appearance is mandatory for offences punishable with up to 7 years imprisonment unless specific grounds of necessity exist.",
        "source_type": "precedent"
    },
    {
        "id": "SC_2017_PUTTASWAMY",
        "title": "Justice K.S. Puttaswamy (Retd.) v. Union of India (2017)",
        "citation": "(2017) 10 SCC 1",
        "act_code": "PRECEDENT",
        "section": "Article 21 - Right to Privacy",
        "enactment_year": 2017,
        "legal_text": "A 9-Judge Constitution Bench of the Supreme Court unanimously held that the Right to Privacy is a fundamental right protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution. Established the three-pronged test for state intrusion on privacy: (1) Legality (existence of law); (2) Legitimate state aim; (3) Proportionality (rational nexus between means and goal with least intrusive measure). Directly spurred the enactment of the DPDP Act 2023.",
        "court": "Supreme Court of India",
        "bench": "9-Judge Constitution Bench (J.S. Khehar, C.J., et al.)",
        "ratio_decidendi": "Privacy is an inalienable fundamental right under Article 21. Any state infringement must satisfy legality, legitimate purpose, and strict proportionality.",
        "source_type": "precedent"
    },
    {
        "id": "SC_1997_DK_BASU",
        "title": "D.K. Basu v. State of West Bengal (1997)",
        "citation": "(1997) 1 SCC 416",
        "act_code": "PRECEDENT",
        "section": "Custodial Violence & Arrestee Safeguards",
        "enactment_year": 1997,
        "legal_text": "Supreme Court in D.K. Basu v. State of West Bengal formulated 11 mandatory guidelines to prevent custodial violence and protect the fundamental rights of arrested persons under Articles 21 and 22: Identification tags for interrogators, memo of arrest signed by witness, right of arrestee to inform a friend or relative within 8-12 hours, medical examination every 48 hours, and transmission of records to magistrate. Failure to comply makes police liable for contempt of court and departmental action.",
        "court": "Supreme Court of India",
        "bench": "Kuldip Singh & A.S. Anand, JJ.",
        "ratio_decidendi": "Custodial torture violates human dignity and Article 21. Mandatory compliance with arrest and detention protocols is binding upon all law enforcement agencies.",
        "source_type": "precedent"
    },
    {
        "id": "SC_2014_LALITA_KUMARI",
        "title": "Lalita Kumari v. Government of Uttar Pradesh (2014)",
        "citation": "(2014) 2 SCC 1",
        "act_code": "PRECEDENT",
        "section": "Section 154 CrPC / Section 173 BNSS - Mandatory FIR Registration",
        "enactment_year": 2014,
        "legal_text": "5-Judge Constitution Bench of the Supreme Court held that registration of an FIR is mandatory under Section 154 of the Code of Criminal Procedure (now Section 173 BNSS), if the information discloses commission of a cognizable offence and no preliminary inquiry is permissible in such a situation. If the information does not disclose a cognizable offence but indicates the necessity for an inquiry, a preliminary inquiry may be conducted only to ascertain whether a cognizable offence is disclosed.",
        "court": "Supreme Court of India",
        "bench": "5-Judge Constitution Bench (P. Sathasivam, C.J., et al.)",
        "ratio_decidendi": "Mandatory registration of FIR is the rule upon receiving information disclosing a cognizable offence. Police officer has no discretion to refuse registration.",
        "source_type": "precedent"
    },
    {
        "id": "SC_2019_CHIDAMBARAM",
        "title": "P. Chidambaram v. Directorate of Enforcement (2019)",
        "citation": "(2019) 9 SCC 24",
        "act_code": "PRECEDENT",
        "section": "Bail Triple Test",
        "enactment_year": 2019,
        "legal_text": "Supreme Court reiterated the paramount 'Triple Test' for grant of bail: (1) Whether the accused is a flight risk (likely to abscond from trial); (2) Whether there is a likelihood of tampering with evidence; (3) Whether there is a likelihood of influencing witnesses. Gravity of the offence alone is not the sole criterion to deny bail if the triple test is satisfied.",
        "court": "Supreme Court of India",
        "bench": "R. Banumathi, A.S. Bopanna & Hrishikesh Roy, JJ.",
        "ratio_decidendi": "Bail consideration rests on the objective evaluation of flight risk, evidence tampering, and witness influence (Triple Test), rather than punitive pre-trial incarceration.",
        "source_type": "precedent"
    },
    {
        "id": "SC_2015_SHREYA_SINGHAL",
        "title": "Shreya Singhal v. Union of India (2015)",
        "citation": "(2015) 5 SCC 1",
        "act_code": "PRECEDENT",
        "section": "Section 66A IT Act & Article 19(1)(a)",
        "enactment_year": 2015,
        "legal_text": "Supreme Court struck down Section 66A of the Information Technology Act, 2000 in its entirety as unconstitutional and violative of Article 19(1)(a) freedom of speech and expression. Held that Section 66A was vague, overbroad, and created an unacceptable chilling effect on legitimate online speech. Distinguished between discussion, advocacy, and incitement.",
        "court": "Supreme Court of India",
        "bench": "J. Chelameswar & R.F. Nariman, JJ.",
        "ratio_decidendi": "Vague and overly broad penal provisions criminalizing speech without proximate nexus to public order are unconstitutional under Article 19(1)(a).",
        "source_type": "precedent"
    }
]

def init_database():
    print("[DB Init] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Seed Default Admin & Advocate Users
        admin_user = db.query(User).filter(User.email == "admin@nyaya.gov.in").first()
        if not admin_user:
            admin_user = User(
                email="admin@nyaya.gov.in",
                hashed_password=get_password_hash("Admin@Nyaya2026!"),
                full_name="Chief Legal Administrator",
                role="admin",
                language_preference="en"
            )
            db.add(admin_user)
            print("[DB Init] Created default admin user: admin@nyaya.gov.in")
            
        advocate_user = db.query(User).filter(User.email == "advocate@nyaya.gov.in").first()
        if not advocate_user:
            advocate_user = User(
                email="advocate@nyaya.gov.in",
                hashed_password=get_password_hash("Advocate@Nyaya2026!"),
                full_name="Senior Advocate Sharma",
                role="advocate",
                language_preference="hi"
            )
            db.add(advocate_user)
            print("[DB Init] Created default advocate user: advocate@nyaya.gov.in")
            
        citizen_user = db.query(User).filter(User.email == "citizen@nyaya.gov.in").first()
        if not citizen_user:
            citizen_user = User(
                email="citizen@nyaya.gov.in",
                hashed_password=get_password_hash("Citizen@Nyaya2026!"),
                full_name="Rajesh Kumar",
                role="citizen",
                language_preference="en"
            )
            db.add(citizen_user)
            print("[DB Init] Created default citizen user: citizen@nyaya.gov.in")

        # 2. Seed Legal Sources
        print(f"[DB Init] Seeding {len(STATUTE_AND_PRECEDENT_DATA)} verified statutes and precedents...")
        for item in STATUTE_AND_PRECEDENT_DATA:
            existing = db.query(LegalSource).filter(LegalSource.id == item["id"]).first()
            if not existing:
                source = LegalSource(
                    id=item["id"],
                    title=item["title"],
                    citation=item["citation"],
                    act_code=item["act_code"],
                    section=item.get("section"),
                    enactment_year=item.get("enactment_year"),
                    legal_text=item["legal_text"],
                    court=item.get("court"),
                    bench=item.get("bench"),
                    ratio_decidendi=item.get("ratio_decidendi"),
                    source_type=item.get("source_type", "statute")
                )
                db.add(source)
            else:
                existing.title = item["title"]
                existing.legal_text = item["legal_text"]
                existing.citation = item["citation"]
                existing.ratio_decidendi = item.get("ratio_decidendi")

        # Log compliance initialization
        audit_log = ComplianceAuditLog(
            user_id="SYSTEM_INIT",
            action="DATABASE_SEED",
            resource_id="LEGAL_SOURCES",
            details="Seeded initial authoritative legal database with BNS, BNSS, BSA, Constitution, DPDP, and SC precedents."
        )
        db.add(audit_log)
        db.commit()
        print("[DB Init] Database records committed successfully.")
        
    finally:
        db.close()

def build_vector_and_sparse_indices():
    print("[Index Init] Building FAISS dense vector index and BM25 sparse index...")
    os.makedirs(settings.FAISS_INDEX_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(settings.BM25_INDEX_FILE), exist_ok=True)
    
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        cache_folder=settings.EMBEDDING_CACHE_DIR
    )
    
    docs = []
    bm25_texts = []
    
    for item in STATUTE_AND_PRECEDENT_DATA:
        content = f"{item['title']} - {item['citation']}\n{item['legal_text']}"
        if item.get("ratio_decidendi"):
            content += f"\nRatio Decidendi: {item['ratio_decidendi']}"
            
        metadata = {
            "id": item["id"],
            "title": item["title"],
            "citation": item["citation"],
            "act_code": item["act_code"],
            "section": item.get("section", ""),
            "source_type": item.get("source_type", "statute"),
            "court": item.get("court", ""),
            "year": item.get("enactment_year", 2024)
        }
        docs.append(Document(page_content=content, metadata=metadata))
        bm25_texts.append(content)

    # 1. FAISS dense index
    vector_db = FAISS.from_documents(docs, embeddings)
    vector_db.save_local(settings.FAISS_INDEX_DIR)
    print(f"[Index Init] FAISS dense index built with {len(docs)} documents at {settings.FAISS_INDEX_DIR}")

    # 2. BM25 sparse index
    tokenized_corpus = [doc.lower().split() for doc in bm25_texts]
    bm25 = BM25Okapi(tokenized_corpus)
    with open(settings.BM25_INDEX_FILE, "wb") as f:
        pickle.dump({"bm25": bm25, "documents": bm25_texts, "metadata": [d.metadata for d in docs]}, f)
    print(f"[Index Init] BM25 sparse index saved at {settings.BM25_INDEX_FILE}")

if __name__ == "__main__":
    init_database()
    build_vector_and_sparse_indices()
