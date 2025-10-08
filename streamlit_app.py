import os
import sys
sys.path.append(os.path.join(os.getcwd(), "src"))

import streamlit as st
from services.vcs_services import VCSService, VCSError
from services.branch_services import BranchService, BranchError
from services.history_services import HistoryService, HistoryError
from config import get_supabase, get_supabase_admin

# -----------------------
# App Setup
# -----------------------
st.set_page_config(page_title="CompactVCS", layout="wide")
st.title("📂 CompactVCS")

# -----------------------
# Auth setup and helpers
# -----------------------
sb = None
try:
    sb = get_supabase()
except Exception:
    # handled below by services init try/except as well
    pass

if "user" not in st.session_state:
    st.session_state["user"] = None

def sign_up(email: str, password: str, name: str):
    try:
        if not sb:
            raise RuntimeError("Supabase client not initialized")
        auth_response = sb.auth.sign_up({"email": email, "password": password})
        user = getattr(auth_response, "user", None)
        if user:
            # Don't insert profile yet; wait until first successful login
            # This avoids FK errors if the auth user isn't committed/confirmed
            return True, "Signup successful! Please login (confirm email if required)."
        else:
            return False, "Signup failed."
    except Exception as e:
        return False, f"❌ Signup failed: {e}"

def login(email: str, password: str):
    try:
        if not sb:
            raise RuntimeError("Supabase client not initialized")
        auth_response = sb.auth.sign_in_with_password({"email": email, "password": password})
        user = getattr(auth_response, "user", None)
        if user:
            st.session_state["user"] = user
            # Ensure profile exists now that auth user definitely exists
            try:
                admin_sb = get_supabase_admin()
                existing = admin_sb.table("profiles").select("id").eq("id", user.id).execute()
                if not existing.data:
                    display_name = (email.split("@")[0]) if email and "@" in email else ""
                    admin_sb.table("profiles").insert({
                        "id": user.id,
                        "email": email,
                        "name": display_name
                    }).execute()
            except Exception:
                # Non-fatal if profile creation fails; user can still proceed
                pass
            return True, f"Welcome {email}!"
        else:
            return False, "Login failed."
    except Exception as e:
        return False, f"❌ Login failed: {e}"

def logout():
    st.session_state.pop("user", None)

# Initialize services
try:
    vcs = VCSService()
    branches = BranchService()
    history = HistoryService()
except Exception as e:
    st.error("Supabase configuration not found or invalid. Ensure .env contains supabase_url and supabase_key.")
    st.stop()

if st.session_state["user"] is None:
    auth_tab = st.radio("Account", ["Login", "Sign Up"], horizontal=True)
    if auth_tab == "Sign Up":
        st.subheader("📝 Sign Up")
        with st.form("signup_form", clear_on_submit=True):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign Up")
            if submitted:
                success, msg = sign_up(email, password, name)
                (st.success if success else st.error)(msg)
    else:
        st.subheader("🔐 Login")
        with st.form("login_form", clear_on_submit=True):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                success, msg = login(email, password)
                (st.success if success else st.error)(msg)
                if success:
                    st.rerun()
    if st.session_state["user"] is None:
        st.stop()

# -----------------------
# Sidebar: Repository selection and creation (only for logged-in users)
# -----------------------
st.sidebar.write(f"Logged in as: {st.session_state['user'].email}")
if st.sidebar.button("Logout"):
    logout()
    st.rerun()

st.sidebar.header("Repositories")
repos = vcs.list_repos()
repo_names = [f"{r['repo_id']}: {r['name']}" for r in repos]
selected_repo_display = st.sidebar.selectbox("Select Repository", ["-"] + repo_names)
selected_repo_id = None
if selected_repo_display != "-":
    selected_repo_id = int(selected_repo_display.split(":", 1)[0])

with st.sidebar.expander("Create Repository"):
    with st.form("create_repo_form", clear_on_submit=True):
        new_repo_name = st.text_input("Repository Name")
        create_repo_submit = st.form_submit_button("Create")
        if create_repo_submit and new_repo_name.strip():
            try:
                vcs.create_repo(new_repo_name.strip())
                st.success("Repository created")
                st.rerun()
            except VCSError as e:
                st.error(str(e))

# -----------------------
# Main Panels
# -----------------------
if not selected_repo_id:
    st.info("Select or create a repository to begin.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Files")
    files = vcs.list_files_in_repo(selected_repo_id)
    if files:
        st.table([{ "file_id": f["file_id"], "filename": f["filename"] } for f in files])
    else:
        st.write("No files yet.")

    with st.form("add_file_form", clear_on_submit=True):
        filename = st.text_input("Filename")
        content = st.text_area("Content", height=150)
        add_file_submit = st.form_submit_button("Add File")
        if add_file_submit and filename.strip():
            try:
                vcs.add_file(selected_repo_id, filename.strip(), content)
                st.success("File added")
                st.experimental_rerun()
            except VCSError as e:
                st.error(str(e))

    with st.form("update_file_form", clear_on_submit=True):
        st.caption("Update filename or content of an existing file")
        file_options = [f"{f['file_id']}: {f['filename']}" for f in files] if files else []
        selected_file = st.selectbox("Choose File", ["-"] + file_options)
        new_filename = st.text_input("New Filename (optional)")
        new_content = st.text_area("New Content (optional)", height=120)
        update_file_submit = st.form_submit_button("Update File")
        if update_file_submit and selected_file != "-":
            file_id = int(selected_file.split(":", 1)[0])
            try:
                updated = vcs.update_file(file_id, new_filename=new_filename or None, new_content=new_content or None)
                if updated:
                    st.success("File updated")
                    st.rerun()
                else:
                    st.warning("No changes provided")
            except VCSError as e:
                st.error(str(e))

with col2:
    st.subheader("Commits")
    with st.form("commit_form", clear_on_submit=True):
        message = st.text_input("Commit Message")
        commit_submit = st.form_submit_button("Create Commit")
        if commit_submit and message.strip():
            try:
                vcs.make_commit(selected_repo_id, message.strip())
                st.success("Commit created")
                st.rerun()
            except VCSError as e:
                st.error(str(e))

    try:
        commits = history.show_history(selected_repo_id)
        if commits:
            st.table(commits)
            commit_ids = [str(c["commit_id"]) for c in commits]
            rollback_id = st.selectbox("Rollback to commit", ["-"] + commit_ids)
            if st.button("Rollback") and rollback_id != "-":
                try:
                    vcs.rollback_commit(int(rollback_id))
                    st.success("Rollback complete")
                    st.experimental_rerun()
                except VCSError as e:
                    st.error(str(e))
        else:
            st.write("No commits yet.")
    except HistoryError as e:
        st.info(str(e))

st.subheader("Branches")
branch_col1, branch_col2 = st.columns(2)
with branch_col1:
    try:
        branch_list = branches.list_branches(selected_repo_id)
        if branch_list:
            st.table([{ "branch_id": b["branch_id"], "name": b["name"], "head_commit_id": b.get("head_commit_id") } for b in branch_list])
        else:
            st.write("No branches yet.")
    except BranchError as e:
        st.info(str(e))

with branch_col2:
    with st.form("create_branch_form", clear_on_submit=True):
        branch_name = st.text_input("New Branch Name")
        head_commit = st.text_input("Head Commit ID (optional)")
        create_branch_submit = st.form_submit_button("Create Branch")
        if create_branch_submit and branch_name.strip():
            try:
                head_commit_id = int(head_commit) if head_commit.strip() else None
                branches.add_branch(selected_repo_id, branch_name.strip(), head_commit_id)
                st.success("Branch created")
                st.rerun()
            except (BranchError, ValueError) as e:
                st.error(str(e))

with st.expander("Merge Branches"):
    if 'branch_list' not in locals():
        branch_list = branches.list_branches(selected_repo_id)
    branch_options = [f"{b['branch_id']}: {b['name']}" for b in branch_list] if branch_list else []
    source_sel = st.selectbox("Source Branch", ["-"] + branch_options, key="merge_src")
    target_sel = st.selectbox("Target Branch", ["-"] + branch_options, key="merge_tgt")
    merge_clicked = st.button("Merge")
    if merge_clicked:
        if source_sel != "-" and target_sel != "-":
            try:
                source_id = int(source_sel.split(":", 1)[0])
                target_id = int(target_sel.split(":", 1)[0])
                branches.merge_branches(source_id, target_id)
                st.success("Merge complete (head updated)")
                st.experimental_rerun()
            except BranchError as e:
                st.error(str(e))
        else:
            st.warning("Select both source and target branches")
