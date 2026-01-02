from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from schemas import IncidentIn, ClaimIn
from incident import create_incident, get_case_history
from claims import add_claim
from evidence import add_evidence_file
from llm import constitutional_check, maintainability_check
from db import fetch_similar_constitution_articles, fetch
from rules import decide_with_reason

app = FastAPI(title="LEXI Judicial System")


@app.post("/screen-incident")
def screen_incident(incident: str):
    articles = fetch_similar_constitution_articles(incident, top_k=5)
    constitutional = constitutional_check(incident, articles)
    maintainability = maintainability_check(incident)

    return {
        "constitutional": constitutional,
        "maintainability": maintainability
    }


@app.post("/incident")
def create_case(data: IncidentIn):
    return {"id": create_incident(data.title, data.description)[0]["id"]}


@app.post("/claim")
def submit_claim(data: ClaimIn):
    return add_claim(data.case_id, data.side, data.text)


@app.post("/evidence/upload")
def upload_evidence(
    case_id: int = Form(...),
    side: str = Form(...),
    file: UploadFile = File(...)
):
    add_evidence_file(case_id, side, file)
    return {"status": "ok"}


@app.get("/case/{case_id}/history")
def history(case_id: int):
    return get_case_history(case_id)


@app.get("/verdict-with-reason")
def verdict(case_id: int, score: float, case_type: str):
    facts = fetch("facts", {"case_id": case_id})
    return decide_with_reason(score, case_type, len(facts))
