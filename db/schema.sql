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
  signals jsonb,
  created_at timestamp default now()
);

-- Row-Level Security
alter table mlo_news enable row level security;

create policy "Users can view data"
on mlo_news
for select
using (true);

-- Users table (keeps subscription tiers in sync with Stripe)
create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  plan text not null default 'free',
  created_at timestamp default now()
);
