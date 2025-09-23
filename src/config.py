import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports] 
from supabase import create_client, Client # pyright: ignore[reportMissingImports] 

load_dotenv()  # loads .env from project root
 
SUPABASE_URL = os.getenv("supabase_url")
SUPABASE_KEY = os.getenv("supabase_key")
 
def get_supabase() -> Client:
    """
    Return a supabase client. Raises RuntimeError if config missing.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment (.env)")
    return create_client(SUPABASE_URL, SUPABASE_KEY)