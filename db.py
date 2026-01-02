import os
from embeddings import embed
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set as environment variables"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ======================================================
# Generic helpers
# ======================================================
def insert(table: str, data: dict):
    res = supabase.table(table).insert(data).execute()
    return res.data


def fetch(table: str, filters: dict):
    q = supabase.table(table).select("*")
    for k, v in filters.items():
        q = q.eq(k, v)
    res = q.execute()
    return res.data


# ======================================================
# pgvector similarity (Constitution)
# ======================================================


def fetch_similar_constitution_articles(query: str, top_k: int = 5):
    query_embedding = embed(query)

    res = supabase.rpc(
        "match_constitution_articles",
        {
            "query_embedding": query_embedding,
            "match_count": top_k
        }
    ).execute()

    return res.data
