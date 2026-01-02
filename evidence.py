import os, hashlib, pdfplumber, pytesseract
from PIL import Image
import numpy as np
from db import insert, fetch
from embeddings import embed
from llm import extract_facts

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def extract_text(path, ext):
    if ext == "pdf":
        text = ""
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages:
                text += p.extract_text() or ""
        return text.strip()

    if ext in ["png", "jpg", "jpeg"]:
        return pytesseract.image_to_string(Image.open(path)).strip()

    if ext == "txt":
        return open(path, encoding="utf-8", errors="ignore").read()

    return ""


def add_evidence_file(case_id, side, file):
    raw = file.file.read()
    h = hashlib.sha256(raw).hexdigest()
    ext = file.filename.split(".")[-1]
    path = f"{UPLOAD_DIR}/{h}.{ext}"

    open(path, "wb").write(raw)
    text = extract_text(path, ext)

    insert("evidence", {
        "case_id": case_id,
        "side": side,
        "file_name": file.filename,
        "hash": h,
        "extracted_text": text
    })

    incident = fetch("incidents", {"id": case_id})[0]["description"]
    facts = extract_facts(text, incident)

    if facts == "NO RELEVANT FACTS":
        return

    if cosine(embed(incident), embed(facts)) < 0.25:
        return

    insert("facts", {
        "case_id": case_id,
        "facts": facts,
        "embedding": embed(facts)
    })
