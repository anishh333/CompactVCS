import streamlit as st # pyright: ignore[reportMissingImports]
from src.services.vcs_services import VCSService, VCSError
from src.services.branch_services import BranchService, BranchError
from src.services.history_services import HistoryService, HistoryError

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
        new_file = vcs.file.create_file(repo_id, filename, content)
        if new_file:
            st.success(f"✅ File added: {new_file}")

    if repo_id:
        st.subheader("Files in Repository")
        files = vcs.file.list_files_in_repo(repo_id)
        if files:
            st.table(files)
        else:
            st.warning("No files in this repository yet.")

# -------------------------------
# Commits
# -------------------------------
elif menu == "📝 Commits":
    st.header("📝 Commit Management")

    repo_id = st.number_input("Repository ID (for commits)", min_value=1, step=1)
    message = st.text_input("Commit Message")

    if st.button("💾 Make Commit"):
        commit = vcs.make_commit(repo_id, message)
        if commit:
            st.success(f"✅ Commit created: {commit}")

    if repo_id:
        st.subheader("Recent Commits")
        commits = vcs.commit.list_commits(repo_id)
        if commits:
            st.table(commits)
        else:
            st.warning("No commits found.")

# -------------------------------
# Branches
# -------------------------------
elif menu == "🌿 Branches":
    st.header("🌿 Branch Management")

    repo_id = st.number_input("Repository ID (for branches)", min_value=1, step=1)
    branch_name = st.text_input("Branch Name")

    if st.button("➕ Create Branch"):
        branch = branch_service.add_branch(repo_id, branch_name)
        if branch:
            st.success(f"✅ Branch created: {branch}")

    if repo_id:
        st.subheader("Repository Branches")
        branches = branch_service.list_branches(repo_id)
        if branches:
            st.table(branches)
        else:
            st.warning("No branches yet.")

# -------------------------------
# History
# -------------------------------
elif menu == "📜 History":
    st.header("📜 Commit History")

    repo_id = st.number_input("Repository ID (for history)", min_value=1, step=1)
    if st.button("📖 Show History"):
        history = history_service.get_commit_history(repo_id)
        if history:
            st.table(history)
        else:
            st.warning("No history available.")
