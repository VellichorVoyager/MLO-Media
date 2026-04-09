from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upsert_article(article):
    """Insert article, or update it if the URL already exists."""
    return (
        supabase.table("mlo_news")
        .upsert(article, on_conflict="url")
        .execute()
    )


# Keep a simple insert alias for callers that don't need upsert semantics.
insert_article = upsert_article
