import streamlit as st
from supabase import create_client

url = st.secrets["supabase"]["supabase_url"]
key = st.secrets["supabase"]["supabse_key"]
supabase = create_client(url, key)