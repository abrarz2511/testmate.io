from fastapi import APIRouter, HTTPException, Depends, Header
from supabase import Client
from pydantic import BaseModel
from typing import Optional
from .get_id import get_current_user_id

router = APIRouter()

class History(BaseModel):
    code: str
    action: str
    result: str


def create_history_routes(supabase: Client):
    def get_current_user_id_dep(supabase):
       async def dependency(authorization: Optional[str] = Header(None)):
           return await get_current_user_id(authorization=authorization, supabase=supabase)
       return dependency


    @router.get("/history")
    async def get_history(user_id: str = Depends(get_current_user_id_dep(supabase))):
        try:
            history = supabase.table("user_history").select("*").eq("user_id", user_id).execute()
            return {"history": history}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/save-history/")
    async def save_history(history: History, user_id: str = Depends(lambda: get_current_user_id(supabase=supabase))):
        try:
            data = {
                "user_id": user_id,
                "code": history.code,
                "action": history.action,
                "result": history.result,
            }
            supabase.table("user_history").insert(data).execute()
            return {"message": "History saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return router