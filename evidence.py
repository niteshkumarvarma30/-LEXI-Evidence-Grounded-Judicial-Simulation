import os
import hashlib
import numpy as np
from PIL import Image

# ------------------------------
# Optional dependencies (safe)
# ------------------------------
try:
    import pdfplumber
    PDF_AVAILABLE = True
except Exception:
    PDF_AVAILABLE = False

try:
    import pytesseract
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False

from db import insert, fetch
from embeddings import embed
from llm import extract_facts

# ------------------------------
# Storage
# ------------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ------------------------------
# Utilities
# ------------------------------
def cosine(a, b):
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def extract_text(path: str, ext: str) -> str:
    """
    Extract text in an environment-safe manner.
    Never crashes the backend.
    """

    # ---------- PDF ----------
    if ext == "pdf" and PDF_AVAILABLE:
        text = ""
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception:
            pass
        return text.strip()

    # ---------- IMAGE (OCR) ----------
    if ext in ["png", "jpg", "jpeg"] and OCR_AVAILABLE:
        try:
            return pytesseract.image_to_string(Image.open(path)).strip()
        except Exception:
            return ""

    # ---------- TEXT ----------
    if ext == "txt":
        try:
            return open(path, encoding="utf-8", errors="ignore").read()
        except Exception:
            return ""

    # ---------- Unsupported / OCR disabled ----------
    return ""


# ------------------------------
# Main pipeline
# ------------------------------
def add_evidence_file(case_id: int, side: str, file):
    """
    Evidence ingestion pipeline:
    - hash preservation
    - safe text extraction
    - incident-anchored fact extraction
    - semantic relevance gating
    """

    # Read file
    raw = file.file.read()
    file_hash = hashlib.sha256(raw).hexdigest()

    ext = file.filename.split(".")[-1].lower()
    path = f"{UPLOAD_DIR}/{file_hash}.{ext}"

    with open(path, "wb") as f:
        f.write(raw)

    # Extract text safely
    extracted_text = extract_text(path, ext)

    # Store evidence metadata (always)
    insert("evidence", {
        "case_id": case_id,
        "side": side,
        "file_name": file.filename,
        "hash": file_hash,
        "extracted_text": extracted_text
    })

    # If no usable text, stop here (no hallucination)
    if not extracted_text.strip():
        return

    # Fetch incident (ground truth anchor)
    incident_row = fetch("incidents", {"id": case_id})
    if not incident_row:
        return

    incident_text = incident_row[0]["description"]

    # Extract incident-anchored facts using LLM
    facts = extract_facts(extracted_text, incident_text)

    if facts == "NO RELEVANT FACTS":
        return

    # Semantic grounding check (prevents drift)
    try:
        if cosine(embed(incident_text), embed(facts)) < 0.25:
            return
    except Exception:
        return

    # Persist grounded facts
    insert("facts", {
        "case_id": case_id,
        "facts": facts,
        "embedding": embed(facts)
    })
