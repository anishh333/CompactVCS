import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports] 
from supabase import create_client, Client # pyright: ignore[reportMissingImports] 

load_dotenv()  # loads .env from project root
 
SUPABASE_URL = os.getenv("supabase_url")
SUPABASE_KEY = os.getenv("supabase_key")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("supabase_service_role_key")

def get_supabase() -> Client:
    """
    Return a supabase client. Raises RuntimeError if config missing.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment (.env)")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_admin() -> Client:
    """
    Return an admin supabase client using the service role key.
    NOTE: This MUST use the service role key; no fallback to anon is allowed.
    """
    if not SUPABASE_URL:
        raise RuntimeError("SUPABASE_URL must be set in environment (.env)")
    if not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY must be set in environment (.env)")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)