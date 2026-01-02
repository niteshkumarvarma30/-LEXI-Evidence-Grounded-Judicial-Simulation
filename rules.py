# ======================================================
# LEGAL THRESHOLD RULES (NO AI INVOLVEMENT)
# ======================================================

CRIMINAL_THRESHOLD = 0.75   # beyond reasonable doubt
CIVIL_THRESHOLD = 0.50      # preponderance of evidence


def decide(score: float, case_type: str) -> str:
    """
    Deterministic verdict decision.
    """

    case_type = case_type.lower()

    if case_type == "criminal":
        return "GUILTY" if score >= CRIMINAL_THRESHOLD else "NOT GUILTY"

    if case_type == "civil":
        return "GUILTY" if score >= CIVIL_THRESHOLD else "NOT GUILTY"

    raise ValueError("Invalid case_type. Must be 'criminal' or 'civil'")


def decide_with_reason(score: float, case_type: str, facts_count: int) -> dict:
    """
    Verdict + explainability.
    """

    verdict = decide(score, case_type)

    threshold = (
        CRIMINAL_THRESHOLD if case_type == "criminal"
        else CIVIL_THRESHOLD
    )

    explanation = (
        f"Case type: {case_type.upper()}. "
        f"Required threshold: {threshold}. "
        f"Assessed degree of proof: {score}. "
        f"Facts considered: {facts_count}. "
    )

    if verdict == "GUILTY":
        explanation += "The degree of proof meets or exceeds the legal threshold."
    else:
        explanation += "The degree of proof does not meet the legal threshold."

    return {
        "verdict": verdict,
        "threshold": threshold,
        "score": score,
        "facts_count": facts_count,
        "explanation": explanation
    }
