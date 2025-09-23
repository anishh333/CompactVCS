"""BranchService: handles branch creation, checkout, and merge."""
from typing import Optional, List, Dict
from src.dao.branch_dao import Branch

class BranchError(Exception):
    pass

class BranchService:
    def __init__(self):
        self.branch: Branch = Branch()
    
    # ---------------- Branch Operations ----------------
    def add_branch(self, repo_id: int, name: str, head_commit_id: Optional[int] = None) -> Dict:
        """
        Create a new branch in a repository.
        head_commit_id can be None (branch created at initial state).
        """
        existing = self.branch.get_branch_by_name(repo_id, name)
        if existing:
            raise BranchError(f"Branch '{name}' already exists in repository {repo_id}")
        
        branch = self.branch.create_branch(repo_id, name, head_commit_id)
        if not branch:
            raise BranchError("Failed to create branch")
        return branch

    def delete_branch(self, branch_id: int) -> bool:
        """Delete a branch by its ID."""
        success = self.branch.delete_branch(branch_id)
        if not success:
            raise BranchError(f"Failed to delete branch {branch_id}")
        return True

    def list_branches(self, repo_id: int) -> List[Dict]:
        """List all branches in a repository."""
        return self.branch.list_branches(repo_id)

    def get_branch(self, branch_id: int) -> Dict:
        """Fetch a branch by its ID."""
        b = self.branch.get_branch_by_id(branch_id)
        if not b:
            raise BranchError(f"Branch {branch_id} not found")
        return b

    # ---------------- Checkout ----------------
    def checkout_branch(self, branch_id: int) -> Dict:
        """
        Checkout a branch: returns branch info and current head commit.
        Actual file restoration should be handled by VCSService using head_commit_id.
        """
        branch = self.get_branch(branch_id)
        if not branch.get("head_commit_id"):
            raise BranchError(f"Branch {branch_id} has no commits yet")
        return branch

    # ---------------- Merge ----------------
    def merge_branches(self, source_branch_id: int, target_branch_id: int) -> Dict:
        """
        Merge source branch into target branch.
        This method just updates the head_commit_id of target branch to the latest commit of source.
        Conflict resolution is not handled here.
        """
        source_branch = self.get_branch(source_branch_id)
        target_branch = self.get_branch(target_branch_id)

        source_head = source_branch.get("head_commit_id")
        if not source_head:
            raise BranchError(f"Source branch {source_branch_id} has no commits to merge")

        # Update target branch head commit
        updated_branch = self.branch.update_head_commit(target_branch_id, source_head)
        if not updated_branch:
            raise BranchError("Failed to merge branches")
        
        return updated_branch
