from typing import Optional, List, Dict
from src.config import get_supabase
from supabase import Client # pyright: ignore[reportMissingImports] 

class File:
    def __init__(self):
        self._sb : Client = get_supabase()
    
    def create_file(self,repo_id:int,filename:str,content:str)->Optional[Dict]:
        payload={"repo_id":repo_id,"filename":filename,"content":content}
        resp=self._sb.table("file").insert(payload).execute()
        return resp.data[0] if resp.data else None
    
    def get_file_by_id(self,file_id:int)->Optional[Dict]:
        resp=self._sb.table("file").select("*").eq("file_id",file_id).execute()
        return resp.data[0] if resp.data else None
    
    def list_files(self)->Optional[Dict]:
        resp=self._sb.table("file").select("*").order("file_id",desc=True).execute()
        return resp.data or []
    
    def delete_file(self,file_id:int) -> bool:
        resp=self._sb.table("file").delete().eq("file_id",file_id).execute()
        return bool(resp.data)
    
    def update_file(self,file_id:int,new_name:str)->Optional[Dict]:
        resp=self._sb.table("file").update({"name":new_name}).eq("file_id",file_id).execute()
        return resp.data
    
    def list_files_in_repo(self, repo_id: int) -> Optional[Dict]:
        resp = self._sb.table("file").select("*").eq("repo_id", repo_id).order("file_id", desc=True).execute()
        return resp.data or []
    