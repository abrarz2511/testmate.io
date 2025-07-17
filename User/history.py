from fastapi import APIRouter, HTTPException
from supabase import Client
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class History(BaseModel):
    code: str
    action: str
    result: str

def create_history_routes(supabase: Client):
    @router.get("/history/{user_id}")
    async def save_history(user_id:str):
        try:
            history = supabase.table("user_history").select("*").eq("user_id", user_id).execute()
            return {"history": history}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/save-history/")
    async def save_history(history: History, user_id:str):
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