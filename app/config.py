import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

_REQUIRED = {
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_KEY": SUPABASE_KEY,
    "OPENAI_API_KEY": OPENAI_API_KEY,
}

missing = [name for name, value in _REQUIRED.items() if not value]
if missing:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing)}. "
        "Copy .env.example to .env and fill in the values."
    )
