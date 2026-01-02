import os
import google.generativeai as genai
from typing import List, Dict, Any

# ======================================================
# Gemini setup
# ======================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")


# ======================================================
# Low-level call
# ======================================================
def call_llm(prompt: str) -> str:
    try:
        res = model.generate_content(
            prompt,
            generation_config={"temperature": 0.0, "max_output_tokens": 512}
        )
        parts = res.candidates[0].content.parts
        return "\n".join(p.text.strip() for p in parts if hasattr(p, "text"))
    except Exception:
        return "INCONCLUSIVE"


# ======================================================
# STEP 2 — Criminal / Civil Maintainability
# ======================================================
def maintainability_check(incident: str) -> str:
    prompt = f"""
You are performing a legal maintainability check.

STRICT RULES:
- Do NOT cite IPC sections
- Do NOT mention the Constitution
- Do NOT decide guilt
- Do NOT assume missing facts

INCIDENT:
{incident}

Respond with EXACTLY ONE:
CRIMINAL MAINTAINABLE
CIVIL MAINTAINABLE
NOT MAINTAINABLE
"""
    result = call_llm(prompt).strip()
    return result if result in {
        "CRIMINAL MAINTAINABLE",
        "CIVIL MAINTAINABLE",
        "NOT MAINTAINABLE"
    } else "NOT MAINTAINABLE"


# ======================================================
# STEP 1 — Constitutional Screening (non-blocking)
# ======================================================
def constitutional_check(
    incident: str,
    articles: List[Dict[str, Any]]
) -> dict:

    if not articles:
        return {
            "constitutional_violation": False,
            "constitutional_context": [],
            "analysis": "NO CONSTITUTIONAL ISSUE"
        }

    formatted = []
    context_refs = []

    for row in articles:
        title = row.get("article_title") or "Unknown Article"
        text = row.get("article_text") or ""
        if not text.strip():
            continue
        formatted.append(f"{title}\n{text}")
        context_refs.append(title)

    if not formatted:
        return {
            "constitutional_violation": False,
            "constitutional_context": [],
            "analysis": "NO CONSTITUTIONAL ISSUE"
        }

    joined = "\n\n".join(formatted)

    prompt = f"""
You are assisting in constitutional screening.

RULES:
- Use ONLY the constitutional provisions below
- If no constitutional adjudication is required, respond EXACTLY:
NO CONSTITUTIONAL ISSUE

INCIDENT:
{incident}

CONSTITUTIONAL PROVISIONS:
{joined}

TASK:
State whether this incident requires constitutional adjudication.
"""

    analysis = call_llm(prompt)

    return {
        "constitutional_violation": "NO CONSTITUTIONAL ISSUE" not in analysis,
        "constitutional_context": context_refs,
        "analysis": analysis
    }
# ======================================================
# FACT EXTRACTION (INCIDENT-ANCHORED)
# ======================================================
def extract_facts(evidence_text: str, incident_text: str) -> str:
    """
    Extract ONLY facts that are directly related to the registered incident.
    This function MUST NOT hallucinate or infer.
    """

    prompt = f"""
INCIDENT:
{incident_text}

EVIDENCE:
{evidence_text}

TASK:
Extract ONLY facts that are directly related to the incident.

RULES:
- Use bullet points only
- Do NOT infer intent or guilt
- Do NOT add external information
- If no relevant facts exist, respond EXACTLY:
NO RELEVANT FACTS
"""

    return call_llm(prompt)
