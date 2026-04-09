# MLO Intelligence SaaS

> "Know what to do before your competitors do."

The Bloomberg Terminal for Loan Officers — now as a monetizable SaaS.

## What It Does

- Aggregates mortgage industry news in real-time (RSS + scraper)
- Detects actionable **deal signals** (Refi, Purchase, Regulation, Lender Shift)
- Exposes a FastAPI backend consumed by a Next.js dashboard
- Auth via Supabase (JWT + Row-Level Security)
- Billing via Stripe (Free / Pro $29/mo / Elite $99/mo)

## Sources

- National Mortgage News
- HousingWire
- Mortgage Professional America

## Stack

| Layer     | Technology                      |
| --------- | ------------------------------- |
| Ingestion | Python (feedparser + requests)  |
| Signals   | `workers/signal_engine.py`      |
| Database  | Supabase (PostgreSQL + pgvector)|
| Embeddings| OpenAI                          |
| API       | FastAPI + Uvicorn               |
| Auth      | Supabase Auth (JWT + RLS)       |
| Billing   | Stripe Checkout + Webhooks      |
| Frontend  | Next.js (TypeScript + Tailwind) |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in all values in .env
```

## Database

Run the SQL in `db/schema.sql` against your Supabase project. It creates:

- `mlo_news` — articles with signals, embeddings, and RLS policies
- `users` — subscription tier tracking (synced by Stripe webhooks)

## Run

```bash
# Run the pipeline once
python app/main.py

# Run on a schedule (every 30 minutes)
python cron/scheduler.py

# Start the API server
uvicorn app.api:app --reload

# Start the Stripe webhook server (separate port)
uvicorn stripe.webhook:app --port 8001 --reload
```

## API Endpoints

| Method | Path                  | Description                  |
| ------ | --------------------- | ---------------------------- |
| GET    | `/signals`            | Articles with deal signals   |
| GET    | `/feed`               | Latest news feed             |
| GET    | `/articles/{id}`      | Single article by UUID       |
| POST   | `/stripe/webhook`     | Stripe subscription events   |

## Signal Types

| Signal             | Trigger                          | Action                              |
| ------------------ | -------------------------------- | ----------------------------------- |
| Refi Opportunity   | Rate drop / rates fall           | Call past refi clients              |
| Purchase Opportunity | Inventory rise / housing supply | Target first-time homebuyers        |
| Regulation Alert   | CFPB / regulation mention        | Review compliance messaging         |
| Lender Shift       | Lender / competitor pricing move | Reposition offer                    |

## Project Structure

```
mlo-intelligence-saas/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── app/
│   ├── main.py        # Pipeline entry point
│   ├── api.py         # FastAPI app (signals + feed endpoints)
│   ├── config.py      # Centralized config / env loading
│
├── workers/
│   ├── rss_worker.py     # RSS feed ingestion
│   ├── scraper.py        # Full-article HTML scraper
│   ├── enricher.py       # Category + tag logic
│   ├── embeddings.py     # OpenAI embedding generation
│   ├── signal_engine.py  # Deal Signal Engine 🔥
│
├── db/
│   ├── schema.sql     # Supabase table definitions + RLS policies
│
├── services/
│   ├── supabase_client.py  # Supabase upsert helpers
│
├── cron/
│   ├── scheduler.py   # 30-minute recurring scheduler
│
├── stripe/
│   ├── webhook.py     # Stripe webhook handler (plan sync)
│
├── frontend/
│   ├── pages/
│   │   ├── index.tsx      # Landing page + pricing
│   │   ├── dashboard.tsx  # Signal feed + opportunity panel
```

## Monetization

| Tier       | Price   | Features                              |
| ---------- | ------- | ------------------------------------- |
| Free       | $0      | Daily digest, top 5 signals           |
| Pro        | $29/mo  | Full signal feed, insights dashboard  |
| Elite      | $99/mo  | Lead signals, priority alerts         |
| Enterprise | Custom  | Lender intelligence, white-label      |

## Stripe Webhook Flow

```
User subscribes → Stripe Checkout
        ↓
Stripe fires webhook → /stripe/webhook
        ↓
Update users.plan = 'pro' | 'elite'
        ↓
Unlock gated features in API / frontend
```

