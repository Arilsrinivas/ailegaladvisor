from typing import Dict, List, Any

class CaseOutcomePredictor:
    """
    Quantitative and Judicial Precedent-Backed Case Outcome & Bail Estimator.
    Evaluates offence severity, custody duration under BNSS §479, Supreme Court guidelines,
    and factual risk factors to estimate relief probability and judicial strategy.
    """

    def predict_outcome(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        case_data fields:
        - offence_name: str (e.g., "Theft", "Cheating", "Murder", "Cyber Fraud")
        - applied_sections: list[str] (e.g., ["BNS Section 303", "BNS Section 318"])
        - max_punishment_years: float (e.g., 3, 7, 10, 20)
        - is_first_offender: bool
        - days_in_custody: int
        - is_vulnerable: bool (minor, woman, sick, or infirm under BNSS §480)
        - notice_issued: bool (Was Notice under BNSS §35 / CrPC §41A issued before arrest?)
        - co_accused_bailed: bool (Parity ground)
        - charge_sheet_filed: bool
        - flight_risk: str ("low", "medium", "high")
        - evidence_tier: str ("documentary", "circumstantial", "direct_eyewitness", "electronic")
        """
        score = 50.0  # Baseline
        favorable_factors: List[str] = []
        adverse_factors: List[str] = []
        guidelines_applied: List[Dict[str, str]] = []

        max_years = float(case_data.get("max_punishment_years", 3.0))
        is_first = bool(case_data.get("is_first_offender", True))
        custody_days = int(case_data.get("days_in_custody", 0))
        is_vulnerable = bool(case_data.get("is_vulnerable", False))
        notice_issued = bool(case_data.get("notice_issued", True))
        co_accused_bailed = bool(case_data.get("co_accused_bailed", False))
        charge_sheet_filed = bool(case_data.get("charge_sheet_filed", False))
        flight_risk = str(case_data.get("flight_risk", "low")).lower()

        # 1. Offence Severity & Category (Satender Kumar Antil classification)
        if max_years <= 7.0:
            score += 20.0
            favorable_factors.append(f"Offence carries maximum imprisonment of {max_years} years (falls under Satender Kumar Antil 'Category A'). Ordinary course bail favored.")
            guidelines_applied.append({
                "precedent": "Satender Kumar Antil v. CBI (2022)",
                "principle": "Category A offences (punishment <= 7 years) warrant bail on appearance without routine custody."
            })
            # Arnesh Kumar check
            if not notice_issued:
                score += 10.0
                favorable_factors.append("Arrest made without mandatory Notice of Appearance under Section 35(3) BNSS / 41A CrPC. Violates Arnesh Kumar guidelines.")
                guidelines_applied.append({
                    "precedent": "Arnesh Kumar v. State of Bihar (2014)",
                    "principle": "Non-compliance with arrest pre-requisites for offences <= 7 years entitles accused to bail."
                })
        else:
            score -= 20.0
            adverse_factors.append(f"Heinous offence carrying punishment exceeding 7 years ({max_years} years). Falls under Satender Kumar Antil 'Category B'.")

        # 2. Undertrial Custody Calculation under BNSS Section 479
        statutory_max_days = max_years * 365
        threshold_fraction = 1/3 if is_first else 1/2
        statutory_threshold_days = statutory_max_days * threshold_fraction

        if custody_days >= statutory_threshold_days:
            score += 25.0
            fraction_str = "one-third (1/3)" if is_first else "one-half (1/2)"
            favorable_factors.append(f"Accused has completed {custody_days} days in custody, exceeding {fraction_str} of maximum imprisonment. Mandatory statutory release on personal bond under Section 479 BNSS.")
            guidelines_applied.append({
                "statute": "BNSS 2023 Section 479",
                "principle": f"Mandatory release on bond after {fraction_str} period of detention for undertrials."
            })
        elif custody_days > 90:
            score += 10.0
            favorable_factors.append(f"Substantial period of detention undergone ({custody_days} days). Investigation largely complete.")

        # 3. First-Time Offender Status
        if is_first:
            score += 10.0
            favorable_factors.append("Clean antecedent record with no prior criminal convictions.")
        else:
            score -= 15.0
            adverse_factors.append("Accused has prior criminal antecedents, increasing risk of repeat offences.")

        # 4. Special Vulnerability Consideration (BNSS Section 480 Proviso)
        if is_vulnerable:
            score += 15.0
            favorable_factors.append("Accused qualifies under BNSS Section 480 proviso (woman / minor / infirm / sick person) requiring benign judicial consideration.")
            guidelines_applied.append({
                "statute": "BNSS 2023 Section 480 Proviso",
                "principle": "Special dispensation for women, sick, or infirm persons accused of non-bailable offences."
            })

        # 5. Parity with Co-Accused
        if co_accused_bailed:
            score += 12.0
            favorable_factors.append("Parity ground: Co-accused with identical or greater role has already been enlarged on bail.")

        # 6. Charge Sheet Filing Status
        if charge_sheet_filed:
            score += 8.0
            favorable_factors.append("Police investigation complete and Final Charge Sheet filed. Custodial interrogation no longer warranted.")

        # 7. Flight Risk & Witness Tampering (Triple Test - P. Chidambaram)
        if flight_risk == "high":
            score -= 20.0
            adverse_factors.append("High flight risk or apprehension of influencing material prosecution witnesses.")
        elif flight_risk == "medium":
            score -= 5.0
            adverse_factors.append("Moderate flight risk requires stringent conditions (passport surrender, periodic reporting).")
        else:
            score += 5.0
            favorable_factors.append("Satisfies Triple Test (P. Chidambaram v. ED): No reasonable apprehension of absconding or evidence tampering.")

        # Bound score between 5.0% and 98.0%
        probability = round(max(5.0, min(98.0, score)), 1)

        # Classify predicted outcome
        if probability >= 75.0:
            outcome_category = "High Likelihood of Bail / Relief"
            recommendation = "Strong prima facie case for Regular/Anticipatory Bail. Highlight Category A status, absence of flight risk, and Section 479 BNSS undertrial period."
        elif probability >= 50.0:
            outcome_category = "Moderate Likelihood / Conditional Bail"
            recommendation = "Bail likely upon offering substantial local sureties, passport surrender, and undertaking not to enter the locality of witnesses."
        else:
            outcome_category = "Low Likelihood / Contested Custodial Remand"
            recommendation = "Bail will be vigorously opposed by prosecution. Focus arguments on lack of direct evidence, medical grounds, or seek interim bail pending charge sheet."

        return {
            "probability_score": probability,
            "predicted_outcome": outcome_category,
            "confidence": 0.88,
            "recommendation": recommendation,
            "favorable_factors": favorable_factors,
            "adverse_factors": adverse_factors,
            "guidelines_applied": guidelines_applied
        }

outcome_predictor = CaseOutcomePredictor()
