import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'src'))
import streamlit as st # pyright: ignore[reportMissingImports]

from services.vcs_services import VCSService
from services.branch_services import BranchService
from services.history_services import HistoryService

# Initialize services
vcs = VCSService()
branch_service = BranchService()
history_service = HistoryService()

st.set_page_config(page_title="CompactVCS", layout="wide")

# Sidebar
st.sidebar.title("📂 CompactVCS")
st.sidebar.markdown("A mini Git-like system with Supabase backend")

menu = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "📦 Repositories", "📑 Files", "📝 Commits", "🌿 Branches", "📜 History"]
)

# -------------------------------
# Dashboard (GitHub-style home)
# -------------------------------
if menu == "🏠 Dashboard":
    st.title("🚀 Welcome to CompactVCS")
    st.markdown(
        """
        CompactVCS is a **lightweight version control system** built with Python,  
        Supabase as backend, and Streamlit for the UI.  

        ### Features
        - Manage repositories
        - Track files & commits
        - Create & switch branches
        - View commit history
        """
    )

# -------------------------------
# Repositories
# -------------------------------
elif menu == "📦 Repositories":
    st.header("📦 Repository Management")

    with st.form("repo_form", clear_on_submit=True):
        repo_name = st.text_input("Repository Name")
        submitted = st.form_submit_button("Create Repository")
        if submitted:
            new_repo = vcs.repo.create_repo(repo_name)
            if new_repo:
                st.success(f"✅ Repository created: {new_repo}")

    st.subheader("Existing Repositories")
    repos = vcs.repo.list_repos()
    if repos:
        st.table(repos)
    else:
        st.info("No repositories found.")


# -------------------------------
# Files
# -------------------------------
elif menu == "📑 Files":
    st.header("📑 File Management")

    repo_id = st.number_input("Repository ID", min_value=1, step=1)
    filename = st.text_input("Filename")
    content = st.text_area("File Content")

    if st.button("➕ Add File"):
        try:
            new_file = vcs.add_file(repo_id, filename, content)
            st.success(f"✅ File added: {new_file}")
        except Exception as e:
            st.error(f"❌ {e}")

    if repo_id:
        st.subheader("Files in Repository")
        try:
            files = vcs.list_files_in_repo(repo_id)
            if files:
                st.table(files)
            else:
                st.warning("No files in this repository yet.")
        except Exception as e:
            st.error(f"❌ {e}")
    # Rollback to a commit
    st.subheader("↩️ Rollback to Files")
    rollback_commit_id = st.number_input("Commit ID to rollback", min_value=1, step=1, key="rollback_commit")
    rollback_content= st.text_area("Content")
    if st.button("Rollback file"):
        try:
            success = vcs.rollback_files(rollback_commit_id,rollback_content)
            if success:
                st.success(f"✅ Rolled back to commit {rollback_commit_id}")
        except Exception as e:
            st.error(f"❌ {e}")


# -------------------------------
# Commits
# -------------------------------
elif menu == "📝 Commits":
    st.header("📝 Commit Management")

    repo_id = st.number_input("Repository ID (for commits)", min_value=1, step=1, key="commit_repo")
    message = st.text_input("Commit Message")

    if st.button("💾 Make Commit"):
        try:
            commit = vcs.make_commit(repo_id, message)
            st.success(f"✅ Commit created: {commit}")
        except Exception as e:
            st.error(f"❌ {e}")

    if repo_id:
        st.subheader("Recent Commits")
        try:
            commits = vcs.list_commits(repo_id)
            if commits:
                st.table(commits)
            else:
                st.warning("No commits found.")
        except Exception as e:
            st.error(f"❌ {e}")

    # Rollback to a commit
    st.subheader("↩️ Rollback to Commit")
    rollback_commit_id = st.number_input("Commit ID to rollback", min_value=1, step=1, key="rollback_commit")
    if st.button("Rollback Commit"):
        try:
            success = vcs.rollback_commit(rollback_commit_id)
            if success:
                st.success(f"✅ Rolled back to commit {rollback_commit_id}")
        except Exception as e:
            st.error(f"❌ {e}")


# -------------------------------
# Branches
# -------------------------------
elif menu == "🌿 Branches":
    st.header("🌿 Branch Management")

    # Select repository
    repo_id = st.number_input("Repository ID", min_value=1, step=1)

    # Add branch
    st.subheader("➕ Create Branch")
    branch_name = st.text_input("Branch Name")
    if st.button("Create Branch"):
        try:
            new_branch = branch_service.add_branch(repo_id, branch_name)
            st.success(f"✅ Branch created: {new_branch}")
        except Exception as e:
            st.error(f"❌ {e}")

    # List branches
    st.subheader("📋 Existing Branches")
    if repo_id:
        try:
            branches = branch_service.list_branches(repo_id)
            if branches:
                st.table(branches)
            else:
                st.info("No branches found for this repository.")
        except Exception as e:
            st.error(f"❌ {e}")

    # Checkout branch
    st.subheader("🔄 Checkout Branch")
    checkout_id = st.number_input("Branch ID to checkout", min_value=1, step=1, key="checkout_branch")
    if st.button("Checkout Branch"):
        try:
            branch_info = branch_service.checkout_branch(checkout_id)
            st.success(f"✅ Checked out branch: {branch_info}")
        except Exception as e:
            st.error(f"❌ {e}")

    # Merge branches
    st.subheader("🔀 Merge Branches")
    source_id = st.number_input("Source Branch ID", min_value=1, step=1, key="source_branch")
    target_id = st.number_input("Target Branch ID", min_value=1, step=1, key="target_branch")
    if st.button("Merge Branches"):
        try:
            merged = branch_service.merge_branches(source_id, target_id)
            st.success(f"✅ Branches merged: {merged}")
        except Exception as e:
            st.error(f"❌ {e}")

    # Delete branch
    st.subheader("🗑️ Delete Branch")
    delete_id = st.number_input("Branch ID to delete", min_value=1, step=1, key="delete_branch")
    if st.button("Delete Branch"):
        try:
            branch_service.delete_branch(delete_id)
            st.success(f"✅ Branch {delete_id} deleted")
        except Exception as e:
            st.error(f"❌ {e}")


# -------------------------------
# History
# -------------------------------
elif menu == "📜 History":
    st.header("📜 Commit History")

    repo_id = st.number_input("Repository ID (for history)", min_value=1, step=1)
    if st.button("📖 Show History"):
        history = history_service.show_history(repo_id)
        if history:
            st.table(history)
        else:
            st.warning("No history available.")
