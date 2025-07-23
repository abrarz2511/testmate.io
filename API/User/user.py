from fastapi import APIRouter, HTTPException, Depends, status
from supabase import Client
from pydantic import BaseModel
from typing import Optional



router = APIRouter()


class User(BaseModel):
    email: str
    password: str
    username: Optional[str] = None

def create_user_routes(supabase: Client):
    @router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dict)
    async def register_user(user: User):
        try:
            response = supabase.auth.sign_up({
                "email": user.email,
                "password": user.password,
                "username": user.username if user.username else None
            })
            return {
                "message": "User registered successfully",
                "user": response.user.email,
                "session": response.session
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/login", response_model=dict)
    async def login_user(user: User):
        try:
            response = supabase.auth.sign_in_with_password({
                "email": user.email,
                "password": user.password
            })
            return {
                "message": "User logged in successfully",
                "user": response.user.email,
                "session": response.session
            }
        except Exception:
            raise HTTPException(status_code=401, detail=str("Invalid credentials"))
        

    @router.get("/logout", response_model=dict)
    async def logout_user(user: User):
        try:
            response = supabase.auth.sign_out()
            return {"message": "User logged out successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str("e"))
    

    return router



