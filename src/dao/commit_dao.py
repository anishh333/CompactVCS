from typing import Optional, List, Dict
from src.config import get_supabase
from supabase import Client # pyright: ignore[reportMissingImports] 

class Commit:
    def __init__(self):
        self._sb : Client = get_supabase()

    def create_commit(self,repo_id:int,message:str,timestamp: str = None)->Optional[Dict]:
        payload={"repo_id":repo_id,"message":message}
        if timestamp:
            payload["timestamp"] = timestamp
        resp=self._sb.table("commit").insert(payload).execute()
        return resp.data[0] if resp.data else None
    
    def get_commit_by_id(self,commit_id:int)->Optional[Dict]:
        resp=self._sb.table("commit").select("*").eq("commit_id",commit_id).execute()
        return resp.data[0] if resp.data else None
    
    def list_commits(self,repo_id:int)->Optional[Dict]:
        resp=self._sb.table("commit").select("*").eq("repo_id",repo_id).order("timestamp",desc=True).execute()
        return resp.data or []
    