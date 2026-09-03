from typing import Dict, Any, List
from datetime import datetime

class LegalDrafter:
    """
    Automated Legal Drafting Engine generating court-compliant Indian legal documents:
    - Regular Bail Application (BNSS §480 / CrPC §439)
    - Anticipatory Bail Application (BNSS §482 / CrPC §438)
    - Legal Notice for Recovery of Money / Breach of Contract
    - Right to Information (RTI) Application (RTI Act 2005 §6(1))
    - Consumer Complaint (Consumer Protection Act 2019 §35)
    - Mutual Consent Divorce Petition (Hindu Marriage Act 1955 §13B)
    - Sworn Affidavit on Oath
    """

    TEMPLATES_METADATA = [
        {
            "id": "regular_bail",
            "name": "Regular Bail Application",
            "statute": "Section 480 BNSS 2023 / Section 439 CrPC",
            "category": "Criminal",
            "description": "Formal petition seeking release of an undertrial prisoner from judicial/police custody."
        },
        {
            "id": "anticipatory_bail",
            "name": "Anticipatory Bail Application",
            "statute": "Section 482 BNSS 2023 / Section 438 CrPC",
            "category": "Criminal",
            "description": "Petition seeking pre-arrest bail in anticipation of apprehension in a non-bailable offence."
        },
        {
            "id": "legal_notice",
            "name": "Legal Notice (Breach / Dues Recovery)",
            "statute": "Section 80 CPC / Indian Contract Act",
            "category": "Civil",
            "description": "Formal statutory demand notice prior to institution of civil recovery or breach of contract suit."
        },
        {
            "id": "rti_application",
            "name": "Right to Information (RTI) Application",
            "statute": "Section 6(1) Right to Information Act 2005",
            "category": "Administrative",
            "description": "Statutory application to Public Information Officer seeking official information/records."
        },
        {
            "id": "consumer_complaint",
            "name": "Consumer Complaint",
            "statute": "Section 35 Consumer Protection Act 2019",
            "category": "Consumer Redressal",
            "description": "Formal petition before District Consumer Disputes Redressal Commission for deficiency of service."
        },
        {
            "id": "mutual_divorce",
            "name": "Mutual Consent Divorce Petition",
            "statute": "Section 13B Hindu Marriage Act 1955",
            "category": "Family",
            "description": "Joint petition for dissolution of marriage by mutual consent with settlement terms."
        },
        {
            "id": "affidavit",
            "name": "General Sworn Affidavit",
            "statute": "Indian Oaths Act 1969",
            "category": "General",
            "description": "Formal declaration of facts under solemn affirmation before an Oath Commissioner / Notary."
        }
    ]

    def get_templates(self) -> List[Dict[str, Any]]:
        return self.TEMPLATES_METADATA

    def generate_draft(self, template_type: str, data: Dict[str, Any]) -> str:
        """
        Populates real legal drafting templates with verified parameters and procedural language.
        """
        today = datetime.now().strftime("%d-%m-%Y")

        if template_type == "regular_bail":
            return self._draft_regular_bail(data, today)
        elif template_type == "anticipatory_bail":
            return self._draft_anticipatory_bail(data, today)
        elif template_type == "legal_notice":
            return self._draft_legal_notice(data, today)
        elif template_type == "rti_application":
            return self._draft_rti_application(data, today)
        elif template_type == "consumer_complaint":
            return self._draft_consumer_complaint(data, today)
        elif template_type == "mutual_divorce":
            return self._draft_mutual_divorce(data, today)
        elif template_type == "affidavit":
            return self._draft_affidavit(data, today)
        else:
            return self._draft_regular_bail(data, today)

    def _draft_regular_bail(self, d: Dict[str, Any], date: str) -> str:
        court = d.get("court_name", "IN THE COURT OF SESSIONS JUDGE, NEW DELHI")
        applicant = d.get("applicant_name", "Rajesh Kumar")
        applicant_details = d.get("applicant_details", "S/o Sh. Ramesh Kumar, R/o Sector 14, Rohini, New Delhi")
        fir_no = d.get("fir_no", "142/2026")
        police_station = d.get("police_station", "Rohini North")
        sections = d.get("sections", "Section 303 / 318 of Bharatiya Nyaya Sanhita (BNS) 2023")
        facts = d.get("case_facts", "The applicant has been falsely implicated on flimsy pretexts without any recovery or direct evidence.")
        custody_date = d.get("custody_date", "10-01-2026")

        return f"""
{court.upper()}
BAIL APPLICATION NO. ______ OF 2026

IN THE MATTER OF:
{applicant}
{applicant_details}
... APPLICANT / ACCUSED

VERSUS

STATE (NCT OF DELHI)
... RESPONDENT

FIR NO: {fir_no}
POLICE STATION: {police_station}
UNDER SECTIONS: {sections}

APPLICATION UNDER SECTION 480 OF THE BHARATIYA NAGARIK SURAKSHA SANHITA (BNSS) 2023 (CORRESPONDING TO SECTION 439 OF Cr.P.C.) FOR GRANT OF REGULAR BAIL ON BEHALF OF THE ACCUSED / APPLICANT

MOST RESPECTFULLY SHOWETH:

1. That the Applicant has been falsely implicated and arrested on {custody_date} in connection with FIR No. {fir_no} registered at Police Station {police_station} under {sections}.

2. That the Applicant is a law-abiding citizen having deep roots in society and has never been convicted of any penal offence in the past.

3. BRIEF FACTS OF THE CASE:
   {facts}

4. GROUNDS FOR BAIL:
   a. Because the investigation in the present case is substantially complete and no further custodial interrogation of the Applicant is warranted.
   b. Because the offence alleged carries punishment not exceeding 7 years, squarely qualifying for benign consideration under the landmark dictum of the Hon'ble Supreme Court in *Satender Kumar Antil v. CBI (2022) 10 SCC 51* (Category A Offences).
   c. Because the mandatory safeguards under Section 35 of BNSS 2023 (Section 41A CrPC) and *Arnesh Kumar v. State of Bihar (2014) 8 SCC 273* were flagrantly disregarded prior to effecting arrest.
   d. Because the Applicant satisfies the paramount Triple Test articulated in *P. Chidambaram v. ED (2019) 9 SCC 24*:
      i. The Applicant is not a flight risk and has surrendered all travel documents.
      ii. There is no possibility of tampering with documentary or electronic evidence already seized by police.
      iii. The Applicant undertakes not to contact or influence any prosecution witnesses.
   e. Because under Section 479 of the BNSS 2023, the detention of an undertrial cannot be punitive and bail remains the cardinal rule while jail is the strict exception (*Babu Singh v. State of U.P.*).

5. PRAYER:
   Wherefore, in the light of the facts and circumstances stated hereinabove, it is most respectfully prayed that this Hon'ble Court may graciously be pleased to:
   a. Order the release of the Applicant/Accused on regular bail in FIR No. {fir_no}, P.S. {police_station}, on such terms and reasonable solvent sureties as this Hon'ble Court may deem fit and proper;
   b. Pass such other or further order(s) as this Hon'ble Court may deem fit in the interest of justice.

DATED: {date}
PLACE: NEW DELHI

APPLICANT
THROUGH COUNSEL
ADVOCATE FOR THE APPLICANT
""".strip()

    def _draft_anticipatory_bail(self, d: Dict[str, Any], date: str) -> str:
        court = d.get("court_name", "IN THE HIGH COURT OF JUDICATURE AT DELHI")
        applicant = d.get("applicant_name", "Vikram Malhotra")
        apprehended_fir = d.get("fir_no", "Anticipated / Unnumbered FIR at PS Connaught Place")
        sections = d.get("sections", "Section 318 BNS 2023 (Cheating)")
        grounds = d.get("grounds", "The dispute is purely of a civil nature arising out of commercial contract disagreement.")

        return f"""
{court.upper()}
CRIMINAL MISCELLANEOUS (ANTICIPATORY BAIL) APPLICATION NO. ______ OF 2026

IN THE MATTER OF:
{applicant}
... APPLICANT

VERSUS

STATE (GOVT. OF NCT OF DELHI)
... RESPONDENT

IN RE: {apprehended_fir}
UNDER SECTIONS: {sections}

APPLICATION UNDER SECTION 482 OF THE BHARATIYA NAGARIK SURAKSHA SANHITA (BNSS) 2023 (SECTION 438 Cr.P.C.) FOR GRANT OF ANTICIPATORY BAIL

MOST RESPECTFULLY SHOWETH:

1. That the Applicant has reasonable and bona fide apprehension of arrest in connection with malicious complaints lodged at the behest of commercial rivals under {sections}.

2. GROUNDS:
   a. {grounds}
   b. That the dispute in question is entirely of a civil and contractual character given a criminal color solely to harass and extract illegal concessions.
   c. That the Applicant has clean antecedents and undertakes to join investigation as and when directed by the Investigating Officer.
   d. That the Hon'ble Supreme Court in *Gurbaksh Singh Sibbia v. State of Punjab* held that the power to grant anticipatory bail must be exercised liberally to safeguard personal liberty under Article 21.

3. PRAYER:
   It is respectfully prayed that in the event of arrest, the Applicant be directed to be enlarged on anticipatory bail upon furnishing reasonable bond.

DATED: {date}
APPLICANT THROUGH COUNSEL
""".strip()

    def _draft_legal_notice(self, d: Dict[str, Any], date: str) -> str:
        sender = d.get("sender_name", "Apex Global Solutions Pvt. Ltd.")
        recipient = d.get("recipient_name", "Horizon Retailers Ltd.")
        amount = d.get("due_amount", "₹12,50,000/- (Rupees Twelve Lakh Fifty Thousand Only)")
        invoice_date = d.get("invoice_date", "15-11-2025")
        days = d.get("notice_days", "15")

        return f"""
LEGAL DEMAND NOTICE
(REGISTERED POST WITH A.D. & EMAIL)

DATE: {date}

TO:
{recipient}
(Noticee)

FROM:
ADVOCATE S.K. VERMA
CHAMBER NO. 412, DELHI HIGH COURT, NEW DELHI
ON BEHALF OF: {sender} (Client)

SUBJECT: LEGAL NOTICE FOR RECOVERY OF OUTSTANDING SUM OF {amount} TOGETHER WITH INTEREST @ 18% PER ANNUM

SIR/MADAM,

Under instructions from and on behalf of our Client, {sender}, we hereby serve upon you this formal Legal Notice:

1. That our Client supplied goods/services pursuant to Purchase Order and Invoices dated {invoice_date}.
2. That despite having acknowledged receipt and quality of services without dispute, you have neglected and failed to liquidate the outstanding liability of {amount}.
3. That your failure to remit the lawful outstanding dues constitutes willful breach of contract, unjust enrichment, and bad faith.

NOW THEREFORE, we call upon you to remit the said sum of {amount} together with interest @ 18% p.a. within {days} days of receipt of this notice, failing which our Client has given peremptory instructions to initiate appropriate Civil and Criminal proceedings before courts of competent jurisdiction, at your sole risk and costs.

ADVOCATE FOR THE CLIENT
""".strip()

    def _draft_rti_application(self, d: Dict[str, Any], date: str) -> str:
        pio = d.get("pio_address", "The Central Public Information Officer (CPIO), Ministry of Law and Justice, Shastri Bhawan, New Delhi")
        applicant = d.get("applicant_name", "Ananya Deshmukh")
        applicant_address = d.get("applicant_address", "Flat 302, Green Enclave, Pune, Maharashtra - 411001")
        queries = d.get("info_requested", "1. Certified copy of the notification implementing the digital court recording pilot project.\n2. Date of sanctions and total budget allocated.")

        return f"""
APPLICATION FOR OBTAINING INFORMATION UNDER SECTION 6(1) OF THE RIGHT TO INFORMATION ACT, 2005

TO:
{pio}

1. NAME OF THE APPLICANT: {applicant}
2. POSTAL ADDRESS: {applicant_address}
3. CITIZENSHIP: Citizen of India
4. PARTICULARS OF INFORMATION SOUGHT:
{queries}

5. PERIOD FOR WHICH INFORMATION IS REQUIRED: Financial Year 2024-2026
6. MODE OF ACCESS DESIRED: Certified hard copies by speed post / email.
7. APPLICATION FEE DETAILS: IPO / Online payment of ₹10/- attached herewith.

I hereby state that the information sought does not fall within the exemptions contained in Section 8 or 9 of the RTI Act 2005, and to the best of my knowledge, pertains to your public authority.

DATE: {date}
PLACE: PUNE

SIGNATURE OF APPLICANT
""".strip()

    def _draft_consumer_complaint(self, d: Dict[str, Any], date: str) -> str:
        commission = d.get("commission", "BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION AT BENGALURU")
        complainant = d.get("complainant_name", "Suresh Menon, R/o Indiranagar, Bengaluru")
        opposite_party = d.get("opposite_party", "Star Appliance Care Pvt. Ltd.")
        facts = d.get("complaint_facts", "Defective electronic equipment supplied on 05-09-2025; failed within 48 hours and warranty service refused.")
        claim_amount = d.get("claim_amount", "₹85,000/- plus ₹50,000/- compensation for mental agony")

        return f"""
{commission.upper()}
CONSUMER COMPLAINT NO. ______ OF 2026

IN THE MATTER OF:
{complainant}
... COMPLAINANT

VERSUS

{opposite_party}
... OPPOSITE PARTY

COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019 FOR DEFICIENCY OF SERVICE AND UNFAIR TRADE PRACTICE

MOST RESPECTFULLY SHOWETH:
1. That the Complainant is a 'consumer' within the definition of Section 2(7) of the Consumer Protection Act, 2019.
2. BRIEF FACTS:
   {facts}
3. That the failure of the Opposite Party to rectify the defect or refund the purchase amount constitutes gross deficiency in service and unfair trade practice.
4. PRAYER:
   It is prayed that this Hon'ble Commission direct the Opposite Party to:
   a. Refund the sum of {claim_amount};
   b. Award litigation costs of ₹25,000/-.

DATE: {date}
COMPLAINANT IN PERSON
""".strip()

    def _draft_mutual_divorce(self, d: Dict[str, Any], date: str) -> str:
        court = d.get("court_name", "IN THE COURT OF PRINCIPAL JUDGE, FAMILY COURT AT JAIPUR")
        p1 = d.get("petitioner_1", "Aditya Sharma")
        p2 = d.get("petitioner_2", "Pooja Sharma")
        marriage_date = d.get("marriage_date", "12-12-2020")
        separation_date = d.get("separation_date", "15-01-2024")

        return f"""
{court.upper()}
H.M.A. PETITION NO. ______ OF 2026

IN THE MATTER OF:
1. {p1}
... FIRST PETITIONER
AND
2. {p2}
... SECOND PETITIONER

JOINT PETITION FOR DISSOLUTION OF MARRIAGE BY A DECREE OF DIVORCE BY MUTUAL CONSENT UNDER SECTION 13B OF THE HINDU MARRIAGE ACT, 1955

MOST RESPECTFULLY SHOWETH:
1. That marriage between the Petitioners was solemnized on {marriage_date} according to Hindu rites and ceremonies.
2. That Petitioners have been living separately since {separation_date} (exceeding one year) due to irreconcilable temperamental differences.
3. That Petitioners have mutually settled all claims regarding maintenance, stridhan, and alimony without any coercion or undue influence.
4. PRAYER:
   It is prayed that this Court pass a decree of divorce dissolving the marriage between the Petitioners.

DATE: {date}
PETITIONER NO. 1                       PETITIONER NO. 2
""".strip()

    def _draft_affidavit(self, d: Dict[str, Any], date: str) -> str:
        deponent = d.get("deponent_name", "Rameshwar Prasad")
        deponent_age = d.get("age", "45")
        residence = d.get("residence", "R/o 12/A, Civil Lines, Prayagraj, UP")
        statements = d.get("statements", "1. That I am the authorized representative of the applicant firm.\n2. That all contents stated in the accompanying petition are true to my personal knowledge.")

        return f"""
AFFIDAVIT

I, {deponent}, aged about {deponent_age} years, {residence}, do hereby solemnly affirm and declare on oath as under:

{statements}

DEPONENT

VERIFICATION:
Verified at on this {date} that the contents of above affidavit are true and correct to the best of my knowledge and belief. No part of it is false and nothing material has been concealed therefrom.

DEPONENT
""".strip()

legal_drafter = LegalDrafter()
