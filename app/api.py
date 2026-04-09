"""FastAPI application — serves deal signals and news feed to the frontend."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.supabase_client import supabase

app = FastAPI(title="MLO Intelligence API", version="1.0.0")

_allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
# Fall back to a permissive default only in local development
if not any(_allowed_origins):
    _allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/signals")
def get_signals():
    """Return articles that contain at least one deal signal, newest first."""
    res = (
        supabase.table("mlo_news")
        .select("id, title, url, source, published_at, signals")
        .not_.is_("signals", "null")
        .order("published_at", desc=True)
        .limit(50)
        .execute()
    )
    return res.data


@app.get("/feed")
def get_feed():
    """Return the latest articles with title, summary, category, and tags."""
    res = (
        supabase.table("mlo_news")
        .select("id, title, url, source, published_at, summary, category, tags")
        .order("published_at", desc=True)
        .limit(100)
        .execute()
    )
    return res.data


@app.get("/articles/{article_id}")
def get_article(article_id: str):
    """Return a single article by its UUID."""
    res = (
        supabase.table("mlo_news")
        .select("*")
        .eq("id", article_id)
        .maybe_single()
        .execute()
    )
    if res.data is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return res.data
