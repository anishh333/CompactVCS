import os
from pathlib import Path
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from supabase import create_client, Client  # pyright: ignore[reportMissingImports]

# Try loading .env from multiple likely locations (handles Streamlit CWD differences)
_here = Path(__file__).resolve()
_root_candidates = [
    _here.parents[1],          # project root if this file is src/config.py
    Path.cwd(),                # current working directory
]
for base in _root_candidates:
    env_path = base / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)

# Read config with support for multiple casings
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
    """
    Return a supabase client. Raises RuntimeError if config missing.
    """
    missing = []
    if not SUPABASE_URL:
        missing.append("supabase_url")
    if not SUPABASE_KEY:
        missing.append("supabase_key")
    if missing:
        raise RuntimeError(f"Missing config: {', '.join(missing)}. Ensure .env in project root contains these keys.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_admin() -> Client:
    """
    Return an admin supabase client using the service role key.
    NOTE: This MUST use the service role key; no fallback to anon is allowed.
    """
    if not SUPABASE_URL:
        raise RuntimeError("Missing config: supabase_url")
    if not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Missing config: supabase_service_role_key")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)