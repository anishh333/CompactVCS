import os
import sys
sys.path.append(os.path.join(os.getcwd(), "src"))

import streamlit as st
from supabase import create_client, Client

# -----------------------
# Supabase setup
# -----------------------
SUPABASE_URL = st.secrets["supabase"]["supabase_url"]
SUPABASE_KEY = st.secrets["supabase"]["supabase_key"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------
# Helper functions
# -----------------------
def sign_up(email: str, password: str, name: str):
    """Sign up user and create profile"""
    try:
        auth_response = supabase.auth.sign_up({"email": email, "password": password})
        user = auth_response.user
        if user:
            # Insert into profiles with user.id
            supabase.table("profiles").insert({
                "id": user.id,
                "email": email,
                "name": name
            }).execute()
            return True, "Signup successful! Please login."
        else:
            return False, "Signup failed."
    except Exception as e:
        return False, f"❌ Signup failed: {e}"

def login(email: str, password: str):
    """Login user"""
    try:
        auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = auth_response.user
        if user:
            st.session_state["user"] = user
            return True, f"Welcome {email}!"
        else:
            return False, "Login failed."
    except Exception as e:
        return False, f"❌ Login failed: {e}"

def logout():
    """Logout user"""
    st.session_state.pop("user", None)

# -----------------------
# Session state for user
# -----------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="CompactVCS", layout="wide")

st.title("📂 CompactVCS")

if st.session_state["user"] is None:
    menu = st.radio("Navigate", ["Login", "Sign Up"])

    if menu == "Sign Up":
        st.header("📝 Sign Up")
        with st.form("signup_form", clear_on_submit=True):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign Up")
            if submitted:
                success, msg = sign_up(email, password, name)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

    elif menu == "Login":
        st.header("🔐 Login")
        with st.form("login_form", clear_on_submit=True):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                success, msg = login(email, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

else:
    st.sidebar.write(f"Logged in as: {st.session_state['user'].email}")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()

    # Main Dashboard
    st.header("🚀 CompactVCS Dashboard")
    st.markdown("""
    Welcome! You are logged in. Here you can manage repositories, files, commits, branches, and history.
    """)

    # Example: show user profile info
    profile = supabase.table("profiles").select("*").eq("id", st.session_state["user"].id).single().execute()
    if profile.data:
        st.subheader("Your Profile")
        st.write(profile.data)
    else:
        st.warning("Profile not found.")
