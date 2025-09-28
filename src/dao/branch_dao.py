import sys, os
sys.path.append(os.path.join(os.getcwd(), 'src')) 
from typing import Optional, List, Dict
from config import get_supabase
from supabase import Client # pyright: ignore[reportMissingImports]

class Branch:
    def __init__(self):
        self._sb : Client = get_supabase()
    
    def create_branch(self,repo_id:int,name:str,head_commit_id) -> Optional[Dict]:
        payload={"repo_id":repo_id,"name":name,"head_commit_id":head_commit_id}
        resp=self._sb.table("branch").insert(payload).execute()
        return resp.data[0] if resp.data else None
    
    def get_branch_by_id(self, branch_id: int) -> Optional[Dict]:
        resp = self._sb.table("branch").select("*").eq("branch_id", branch_id).execute()
        return resp.data[0] if resp.data else None

    def delete_branch(self,branch_id:int) -> bool:
        resp=self._sb.table("branch").delete().eq("branch_id",branch_id).execute()
        return bool(resp.data)
    
    def list_branches(self, repo_id: int) -> List[Dict]:
        """List all branches in a repository."""
        resp = (
            self._sb.table("branch")
            .select("*")
            .eq("repo_id", repo_id)
            .order("branch_id", desc=False)
            .execute()
        )
        return resp.data or []
    
    def update_head_commit(self, branch_id: int, head_commit_id: int) -> Optional[Dict]:
        """Update the head commit of a branch (useful after commit or merge)."""
        resp = (
            self._sb.table("branch")
            .update({"head_commit_id": head_commit_id})
            .eq("branch_id", branch_id)
            .execute()
        )
        return resp.data[0] if resp.data else None
    
    