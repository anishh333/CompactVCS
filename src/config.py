import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env from project root or CWD without touching st.secrets
_here = Path(__file__).resolve()
_root_candidates = [
    _here.parents[1],  # project root (../../ from this file)
    Path.cwd(),
]
for base in _root_candidates:
    env_path = base / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)

def _get_env(*keys: str) -> str | None:
    for k in keys:
        v = os.getenv(k)
        if v:
            return v
    return None

SUPABASE_URL = _get_env("supabase_url", "SUPABASE_URL")
SUPABASE_KEY = _get_env("supabase_key", "SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = _get_env("supabase_service_role_key", "SUPABASE_SERVICE_ROLE_KEY")

def get_supabase() -> Client:
    """Public (anon) Supabase client — reads from environment only."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        missing = []
        if not SUPABASE_URL:
            missing.append("supabase_url")
        if not SUPABASE_KEY:
            missing.append("supabase_key")
        raise ValueError(f"Missing config: {', '.join(missing)}")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_admin() -> Client:
    """Admin client using service role key from environment only."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        missing = []
        if not SUPABASE_URL:
            missing.append("supabase_url")
        if not SUPABASE_SERVICE_ROLE_KEY:
            missing.append("supabase_service_role_key")
        raise ValueError(f"Missing config: {', '.join(missing)}")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
