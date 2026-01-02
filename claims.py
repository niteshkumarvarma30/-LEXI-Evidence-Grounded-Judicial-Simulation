from db import insert
from embeddings import embed


def add_claim(case_id, side, text):
    return insert("claims", {
        "case_id": case_id,
        "side": side,
        "text": text,
        "embedding": embed(text)
    })
