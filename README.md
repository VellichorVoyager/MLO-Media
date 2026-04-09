# MLO Intelligence Engine

The Bloomberg Terminal for Loan Officers.

## What It Does
- Aggregates mortgage industry news in real-time
- Extracts insights for loan officers
- Tags opportunities (rates, regulation, lead gen)
- Enables semantic search across all content

## Sources
- National Mortgage News
- HousingWire
- Mortgage Professional America

## Stack
- Python
- Supabase (DB + Vector)
- OpenAI (Embeddings + Summaries)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in SUPABASE_URL, SUPABASE_KEY, and OPENAI_API_KEY in .env
```

## Database

Run the SQL in `db/schema.sql` against your Supabase project to create the `mlo_news` table (requires the `pgvector` extension).

## Run

```bash
# Run the pipeline once
python app/main.py

# Run on a schedule (every 30 minutes)
python cron/scheduler.py
```

## Project Structure

```
mlo-intelligence-engine/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── app/
│   ├── main.py        # Pipeline entry point
│   ├── config.py      # Centralized config / env loading
│
├── workers/
│   ├── rss_worker.py  # RSS feed ingestion
│   ├── scraper.py     # Full-article HTML scraper
│   ├── enricher.py    # Category + tag logic
│   ├── embeddings.py  # OpenAI embedding generation
│
├── db/
│   ├── schema.sql     # Supabase table definition
│
├── services/
│   ├── supabase_client.py  # Supabase insert helper
│
├── cron/
│   ├── scheduler.py   # 30-minute recurring scheduler
```

## Next Steps

| Feature | Description |
| ------- | ----------- |
| Daily Brief Generator | "What matters today for LOs" |
| Deal Trigger Engine | "Rates dropped → push refi leads" |
| UI Dashboard | "Top opportunities this week" |

## Monetization

| Tier | Product |
| ---- | ------- |
| Free | Daily digest |
| $29/mo | Insights dashboard |
| $99/mo | Lead signals |
| Enterprise | Lender intelligence |
