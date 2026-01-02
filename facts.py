from db import insert
from embeddings import embed
from llm import extract_facts


def promote_facts(case_id, evidence_text, incident_text):
    facts = extract_facts(evidence_text, incident_text)
    if facts == "NO RELEVANT FACTS":
        return None

    return insert("facts", {
        "case_id": case_id,
        "facts": facts,
        "embedding": embed(facts)
    })
