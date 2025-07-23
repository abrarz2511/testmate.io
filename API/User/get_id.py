from fastapi import HTTPException, Header
from typing import Optional
from supabase import Client


async def get_current_user_id(
    authorization: Optional[str] = Header(None),
    supabase: Client = None
) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    try:
        user = supabase.auth.get_user(token)
        return user.user.id
    except Exception: 
        raise HTTPException(status_code=401, detail="Invalid token")