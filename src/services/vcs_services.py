"""VCSService: orchestrates commits, rollback, and file operations."""
import sys, os
sys.path.append(os.path.join(os.getcwd(), 'src')) 
from typing import List, Dict
from dao.repo_dao import Repo
from dao.file_dao import File
from dao.commit_dao import Commit
from dao.commitFile_dao import CommitFile

class VCSError(Exception):
    pass
class VCSService:
    def __init__(self):
        self.repo : Repo=Repo()
        self.file : File=File()
        self.commit : Commit=Commit()
        self.commitfile : CommitFile=CommitFile()
    
    # ---------------- Repository Operations ----------------
    def create_repo(self, name: str) -> Dict:
        repo = self.repo.create_repo(name)
        if not repo:
            raise VCSError("Failed to create repository")
        return repo

    def list_repos(self) -> List[Dict]:
        return self.repo.list_repos()

    def get_repo(self, repo_id: int) -> Dict:
        repo = self.repo.get_repo_by_id(repo_id)
        if not repo:
            raise VCSError(f"Repository {repo_id} not found")
        return repo

    # ---------------- File Operations ----------------
    def add_file(self, repo_id: int, filename: str, content: str) -> Dict:
        file = self.file.create_file(repo_id, filename, content)
        if not file:
            raise VCSError("Failed to add file")
        return file

    def list_files_in_repo(self, repo_id: int) -> List[Dict]:
        return self.file.list_files_in_repo(repo_id)

    def update_file(self, file_id: int, new_filename: str = None) -> Dict:
        updated_file = self.file.update_file(file_id, new_filename=new_filename)
        if not updated_file:
            raise VCSError(f"Failed to update file {file_id}")
        return updated_file

    # ---------------- Commit Operations ----------------
    def make_commit(self, repo_id: int, message: str) -> Dict:
        commit = self.commit.create_commit(repo_id, message)
        if not commit:
            raise VCSError("Failed to create commit")

        files = self.file.list_files_in_repo(repo_id)
        for f in files:
            self.commitfile.add_file_to_commit(
                commit_id=commit["commit_id"],
                file_id=f["file_id"],
                version_number=1,  
                content=f["content"]
            )
        return commit

    def list_commits(self, repo_id: int) -> List[Dict]:
        return self.commit.list_commits(repo_id)

    # ---------------- Rollback Operation ----------------
    def rollback_commit(self, commit_id: int) -> bool:
        commit = self.commit.get_commit_by_id(commit_id)
        if not commit:
            raise VCSError(f"Commit {commit_id} not found")

    def rollback_files(self,commit_id,content):
        commit_files = self.commitfile.get_files_by_commit(commit_id)
        if not commit_files:
            raise VCSError(f"No files found for commit {commit_id}")

        for cf in commit_files:
            file_id = cf["file_id"]
            content = cf["content"]
            self.file.update_file(file_id, new_content=content)
        return True


