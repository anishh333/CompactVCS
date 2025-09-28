import sys, os
sys.path.append(os.path.join(os.getcwd(), 'src')) 
from typing import Optional, List, Dict
from config import get_supabase
from supabase import Client # pyright: ignore[reportMissingImports]
class CommitFile:
    def __init__(self):
        self._sb : Client = get_supabase()

    def add_file_to_commit(self, commit_id: int, file_id: int, version_number: int, content: str) -> Optional[Dict]:
        """Add a file version to a commit."""
        payload = {
            "commit_id": commit_id,
            "file_id": file_id,
            "version_number": version_number,
            "content": content
        }
        resp = self._sb.table("commitfile").insert(payload).execute()
        return resp.data[0] if resp.data else None
    
    def get_files_by_commit(self, commit_id: int) -> List[Dict]:
        """Retrieve all files associated with a specific commit."""
        resp = self._sb.table("commitfile").select("*").eq("commit_id", commit_id).execute()
        return resp.data or []
    
    def get_file_version(self, commit_id: int, file_id: int) -> Optional[Dict]:
        """Get a specific file version in a commit."""
        resp = (
            self._sb.table("commitfile")
            .select("*")
            .eq("commit_id", commit_id)
            .eq("file_id", file_id)
            .execute()
        )
        return resp.data[0] if resp.data else None