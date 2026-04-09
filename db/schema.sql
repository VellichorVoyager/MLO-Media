-- Enable pgvector extension (run once per Supabase project)
create extension if not exists vector;

create table mlo_news (
  id uuid primary key default gen_random_uuid(),
  title text,
  url text unique,
  source text,
  published_at timestamp,
  summary text,
  content text,
  category text,
  tags text[],
  embedding vector(1536),
  created_at timestamp default now()
);
