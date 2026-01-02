from db import insert, fetch


# ======================================================
# INCIDENT REGISTRATION
# ======================================================
def create_incident(title: str, description: str):
    """
    Creates a new incident AFTER constitutional screening.
    Returns inserted row(s).
    """
    return insert("incidents", {
        "title": title,
        "description": description
    })


# ======================================================
# CASE HISTORY (AUDITABLE RECORD)
# ======================================================
def get_case_history(case_id: int):
    """
    Reconstructs the complete case state.
    """

    return {
        "incident": fetch("incidents", {"id": case_id}),
        "claims": fetch("claims", {"case_id": case_id}),
        "evidence": fetch("evidence", {"case_id": case_id}),
        "facts": fetch("facts", {"case_id": case_id})
    }
