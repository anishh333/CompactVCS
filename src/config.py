import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

load_dotenv()  # ✅ loads .env variables

def get_supabase():
    # Try Streamlit secrets first (for deployment)
    if "supabase" in st.secrets:
        url = st.secrets["supabase"]["supabase_url"]
        key = st.secrets["supabase"]["supabase_key"]
    else:
        # Fallback to .env file for local development
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Supabase configuration not found or invalid. Ensure .env contains supabase_url and supabase_key.")

    supabase: Client = create_client(url, key)
    return supabase
