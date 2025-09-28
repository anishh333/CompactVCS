"""HistoryService: View logs and manage commit metadata."""
import sys, os
sys.path.append(os.path.join(os.getcwd(), 'src')) 
from typing import List, Dict
from dao.commit_dao import Commit
from dao.commitFile_dao import CommitFile

class HistoryError(Exception):
    pass

class HistoryService:
    def __init__(self):
        self.commit: Commit = Commit()
        self.commitfile: CommitFile = CommitFile()

    # ---------------- Commit Logs ----------------
    def get_commit_by_id(self, commit_id: int) -> Dict:
        """Fetch commit metadata by commit_id."""
        commit = self.commit.get_commit_by_id(commit_id)
        if not commit:
            raise HistoryError(f"Commit {commit_id} not found")
        return commit

    def list_commits(self, repo_id: int) -> List[Dict]:
        """List all commits in a repository, newest first."""
        commits = self.commit.list_commits(repo_id)
        if not commits:
            raise HistoryError(f"No commits found for repository {repo_id}")
        return commits

    # ---------------- Commit Files ----------------
    def get_files_in_commit(self, commit_id: int) -> List[Dict]:
        """Get all files associated with a specific commit."""
        files = self.commitfile.get_files_by_commit(commit_id)
        if not files:
            raise HistoryError(f"No files found for commit {commit_id}")
        return files

    def get_file_version(self, commit_id: int, file_id: int) -> Dict:
        """Get a specific file version in a commit."""
        file_version = self.commitfile.get_file_version(commit_id, file_id)
        if not file_version:
            raise HistoryError(f"File {file_id} not found in commit {commit_id}")
        return file_version

    # ---------------- Utility ----------------
    def show_history(self, repo_id: int) -> List[Dict]:
        """
        Returns a summarized history of commits:
        commit_id, message, timestamp
        """
        commits = self.list_commits(repo_id)
        return [{"commit_id": c["commit_id"], "message": c["message"], "timestamp": c["timestamp"]} for c in commits]
