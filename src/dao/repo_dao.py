import sys, os
sys.path.append(os.path.join(os.getcwd(), 'src')) 
from typing import Optional, List, Dict
from config import get_supabase
from supabase import Client # pyright: ignore[reportMissingImports] 

class Repo:
    def __init__(self):
        self._sb : Client = get_supabase()
    
    def create_repo(self,name:str)-> Optional[Dict]:
        payload={"name":name}
        self._sb.table("repository").insert(payload).execute()
        resp=self._sb.table("repository").select("*").execute()
        return resp.data[0] if resp.data else None
    
    def get_repo_by_id(self,repo_id:int)-> Optional[Dict]:
        resp=self._sb.table("repository").select("*").eq("repo_id",repo_id).execute()
        return resp.data[0] if resp.data else None
    
    def get_repo_by_name(self,name:str)->Optional[Dict]:
        resp=self._sb.table("repository").select("*").eq("name",name).execute()
        return resp.data or []
    
    def list_repos(self)-> Optional[Dict]:
        resp=self._sb.table("repository").select("*").order("repo_id",desc=True)
        q=resp.execute()
        return q.data or []
    
    def delete_repo(self,repo_id:int) -> bool:
        resp=self._sb.table("repository").delete().eq("repo_id",repo_id).execute()
        return bool(resp.data)
    
    def update_repo(self,repo_id:int,new_name:str)->Optional[Dict]:
        resp=self._sb.table("repository").update({"name":new_name}).eq("repo_id",repo_id).execute()
        return resp.data
    
