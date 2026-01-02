import os
import time
from supabase import create_client, Client
from postgrest.exceptions import APIError
import httpx

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")

# Create client with safe timeout
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options={
        "schema": "public",
        "timeout": 10
    }
)

# -----------------------------
# Retry-safe fetch
# -----------------------------
def fetch(table: str, filters: dict = None, retries: int = 3):
    for attempt in range(retries):
        try:
            q = supabase.table(table).select("*")
            if filters:
                for k, v in filters.items():
                    q = q.eq(k, v)
            return q.execute().data or []
        except (APIError, httpx.ReadError):
            if attempt == retries - 1:
                raise
            time.sleep(0.5)


# -----------------------------
# Retry-safe insert
# -----------------------------
def insert(table: str, data: dict, retries: int = 3):
    for attempt in range(retries):
        try:
            return supabase.table(table).insert(data).execute().data
        except (APIError, httpx.ReadError):
            if attempt == retries - 1:
                raise
            time.sleep(0.5)


# -----------------------------
# Vector similarity (safe)
# -----------------------------
def fetch_similar_constitution_articles(text: str, top_k: int = 5):
    for attempt in range(3):
        try:
            res = supabase.rpc(
                "match_constitution_articles",
                {
                    "query_text": text,
                    "match_count": top_k
                }
            ).execute()
            return res.data or []
        except (APIError, httpx.ReadError):
            if attempt == 2:
                raise
            time.sleep(0.5)
