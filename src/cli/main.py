"""
main.py: CLI for CompactVCS (menu-driven)
"""

import sys
from src.services.vcs_services import VCSService, VCSError
from src.services.branch_services import BranchService, BranchError
from src.services.history_services import HistoryService, HistoryError

def main_menu():
    print("\n=== CompactVCS CLI ===")
    print("1. Repository Operations")
    print("2. File Operations")
    print("3. Commit Operations")
    print("4. Rollback")
    print("5. Branch Operations")
    print("6. View Commit History")
    print("0. Exit")
    choice = input("Enter your choice: ")
    return choice.strip()

# ---------------- Services ----------------
vcs_service = VCSService()
branch_service = BranchService()
history_service = HistoryService()

# ---------------- Helper Functions ----------------
def repo_menu():
    print("\n--- Repository Menu ---")
    print("1. Create Repository")
    print("2. List Repositories")
    print("3. View Repository by ID")
    choice = input("Enter your choice: ").strip()
    return choice

def file_menu():
    print("\n--- File Menu ---")
    print("1. Add File to Repo")
    print("2. List Files in Repo")
    print("3. Update File")
    print("4. Delete File")
    choice = input("Enter your choice: ").strip()
    return choice

def commit_menu():
    print("\n--- Commit Menu ---")
    print("1. Commit Changes")
    print("2. List Commits")
    choice = input("Enter your choice: ").strip()
    return choice

def branch_menu():
    print("\n--- Branch Menu ---")
    print("1. Create Branch")
    print("2. List Branches")
    print("3. Checkout Branch")
    print("4. Merge Branches")
    print("5. Delete Branch")
    choice = input("Enter your choice: ").strip()
    return choice

def history_menu():
    print("\n--- History Menu ---")
    print("1. Show Commit History")
    print("2. Show Files in Commit")
    choice = input("Enter your choice: ").strip()
    return choice

# ---------------- Main Loop ----------------
def main():
    while True:
        choice = main_menu()
        
        if choice == "1":  # Repository
            r_choice = repo_menu()
            if r_choice == "1":
                name = input("Repository Name: ")
                try:
                    repo = vcs_service.create_repo(name)
                    print(f"Repository created: {repo}")
                except VCSError as e:
                    print(f"Error: {e}")
            elif r_choice == "2":
                repos = vcs_service.list_repos()
                print("Repositories:")
                for r in repos:
                    print(r)
            elif r_choice == "3":
                repo_id = int(input("Repository ID: "))
                try:
                    repo = vcs_service.get_repo(repo_id)
                    print(repo)
                except VCSError as e:
                    print(f"Error: {e}")

        elif choice == "2":  # File
            f_choice = file_menu()
            if f_choice == "1":
                repo_id = int(input("Repository ID: "))
                filename = input("File Name: ")
                content = input("File Content: ")
                try:
                    file = vcs_service.add_file(repo_id, filename, content)
                    print(f"File added: {file}")
                except VCSError as e:
                    print(f"Error: {e}")
            elif f_choice == "2":
                repo_id = int(input("Repository ID: "))
                files = vcs_service.list_files_in_repo(repo_id)
                print("Files in Repo:")
                for f in files:
                    print(f)
            elif f_choice == "3":
                file_id = int(input("File ID: "))
                new_name = input("New Name (leave blank to skip): ")
                new_content = input("New Content (leave blank to skip): ")
                try:
                    updated = vcs_service.update_file(
                        file_id,
                        new_filename=new_name if new_name else None,
                        new_content=new_content if new_content else None
                    )
                    print(f"File updated: {updated}")
                except VCSError as e:
                    print(f"Error: {e}")
            elif f_choice == "4":
                file_id = int(input("File ID to delete: "))
                try:
                    success = vcs_service.file.delete_file(file_id)
                    print("File deleted" if success else "Delete failed")
                except VCSError as e:
                    print(f"Error: {e}")

        elif choice == "3":  # Commit
            c_choice = commit_menu()
            if c_choice == "1":
                repo_id = int(input("Repository ID: "))
                message = input("Commit Message: ")
                try:
                    commit = vcs_service.commit_changes(repo_id, message)
                    print(f"Commit created: {commit}")
                except VCSError as e:
                    print(f"Error: {e}")
            elif c_choice == "2":
                repo_id = int(input("Repository ID: "))
                commits = vcs_service.list_commits(repo_id)
                print("Commits:")
                for c in commits:
                    print(c)

        elif choice == "4":  # Rollback
            commit_id = int(input("Commit ID to rollback: "))
            try:
                success = vcs_service.rollback(commit_id)
                print("Rollback successful" if success else "Rollback failed")
            except VCSError as e:
                print(f"Error: {e}")

        elif choice == "5":  # Branch
            b_choice = branch_menu()
            if b_choice == "1":
                repo_id = int(input("Repository ID: "))
                name = input("Branch Name: ")
                head_commit_id = input("Head Commit ID (optional): ")
                head_commit_id = int(head_commit_id) if head_commit_id else None
                try:
                    branch = branch_service.add_branch(repo_id, name, head_commit_id)
                    print(f"Branch created: {branch}")
                except BranchError as e:
                    print(f"Error: {e}")
            elif b_choice == "2":
                repo_id = int(input("Repository ID: "))
                branches = branch_service.list_branches(repo_id)
                for b in branches:
                    print(b)
            elif b_choice == "3":
                branch_id = int(input("Branch ID to checkout: "))
                try:
                    branch = branch_service.checkout_branch(branch_id)
                    print(f"Checked out branch: {branch}")
                except BranchError as e:
                    print(f"Error: {e}")
            elif b_choice == "4":
                source_id = int(input("Source Branch ID: "))
                target_id = int(input("Target Branch ID: "))
                try:
                    merged = branch_service.merge_branches(source_id, target_id)
                    print(f"Branches merged: {merged}")
                except BranchError as e:
                    print(f"Error: {e}")
            elif b_choice == "5":
                branch_id = int(input("Branch ID to delete: "))
                try:
                    success = branch_service.delete_branch(branch_id)
                    print("Branch deleted" if success else "Delete failed")
                except BranchError as e:
                    print(f"Error: {e}")

        elif choice == "6":  # History
            h_choice = history_menu()
            if h_choice == "1":
                repo_id = int(input("Repository ID: "))
                try:
                    history = history_service.show_history(repo_id)
                    for h in history:
                        print(h)
                except HistoryError as e:
                    print(f"Error: {e}")
            elif h_choice == "2":
                commit_id = int(input("Commit ID: "))
                try:
                    files = history_service.get_files_in_commit(commit_id)
                    for f in files:
                        print(f)
                except HistoryError as e:
                    print(f"Error: {e}")

        elif choice == "0":
            print("Exiting CompactVCS CLI...")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
