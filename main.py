from fastapi import FastAPI, Depends, Header
from Test_generator.generate_tests import generate_tests
from Validation_engine.validate_conf import validate_file_with_schema
from supabase import create_client, Client
from User.user import create_user_routes
from User.history import create_history_routes
from User.auth import get_current_user_id
import os
from typing import Optional

# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://tukehmqhitsbucchfdad.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1a2VobXFoaXRzYnVjY2hmZGFkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NjU3MjcsImV4cCI6MjA2ODI0MTcyN30.dfpK1d1M8Z199yI4IXCJ2epzRzKCOh1CoGXPdAvoWeU")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Include routers
user_router = create_user_routes(supabase)
history_router = create_history_routes(supabase)

app.include_router(user_router, prefix="/user")
app.include_router(history_router, prefix="/history")

@app.post("/generate-tests")
async def generate_tests_endpoint(
    code: str, 
    user_id: str = Depends(lambda: get_current_user_id(supabase=supabase))
):
    result = generate_tests(code)
    
    # Save to history
    history_data = {
        "user_id": user_id,  # Now this is the authenticated user's ID
        "code": code,
        "action": "test_generation",
        "result": str(result)
    }
    supabase.table("user_history").insert(history_data).execute()
    
    return result

@app.post("/validate-code")
async def validate_code_endpoint(
    file_path: str, 
    schema_path: str, 
    user_id: str = Depends(lambda: get_current_user_id(supabase=supabase))
):
    result = validate_file_with_schema(file_path, schema_path)
    
    # Save to history
    history_data = {
        "user_id": user_id,  # Now this is the authenticated user's ID
        "code": f"File: {file_path}, Schema: {schema_path}",
        "action": "validation",
        "result": str(result)
    }
    supabase.table("user_history").insert(history_data).execute()
    
    return result


