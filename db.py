import os
import time
import httpx
from supabase import create_client
from postgrest.exceptions import APIError

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL / SUPABASE_KEY missing")


def get_client():
    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY,
        options={
            "schema": "public",
            "timeout": 10
        }
    )


# -----------------------------
# SAFE FETCH
# -----------------------------
def fetch(table: str, filters: dict = None, retries: int = 3):
    for attempt in range(retries):
        try:
            sb = get_client()
            q = sb.table(table).select("*")
            if filters:
                for k, v in filters.items():
                    q = q.eq(k, v)
            return q.execute().data or []
        except (APIError, httpx.ReadError):
            if attempt == retries - 1:
                return []   # ← never crash UI
            time.sleep(0.7)


# -----------------------------
# SAFE INSERT
# -----------------------------
def insert(table: str, data: dict, retries: int = 3):
    for attempt in range(retries):
        try:
            sb = get_client()
            return sb.table(table).insert(data).execute().data
        except (APIError, httpx.ReadError):
            if attempt == retries - 1:
                return []
            time.sleep(0.7)


# -----------------------------
# SAFE VECTOR SEARCH
# -----------------------------
def fetch_similar_constitution_articles(text: str, top_k: int = 5):
    for attempt in range(3):
        try:
            sb = get_client()
            res = sb.rpc(
                "match_constitution_articles",
                {
                    "query_text": text,
                    "match_count": top_k
                }
            ).execute()
            return res.data or []
        except (APIError, httpx.ReadError):
            if attempt == 2:
                return []
            time.sleep(0.7)
