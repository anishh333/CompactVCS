import streamlit as st
from supabase import create_client 

def get_supabase():
    url = st.secrets["supabase"]["supabase_url"]
    key = st.secrets["supabase"]["supabase_key"]
    return create_client(url, key)

supabase = get_supabase()