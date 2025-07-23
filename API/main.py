from fastapi import FastAPI, Depends, Header
from .Test_generator.generate_tests import TestGenerator
from .Validation_engine.validate_conf import validate_content_with_schema
from supabase import create_client, Client
from .User.user import create_user_routes
from .User.history import create_history_routes
from .User.get_id import get_current_user_id
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse

load_dotenv()
# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

test_generator = TestGenerator(os.getenv("OPENAI_API_KEY"))
generate_tests = test_generator.generate_tests

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Include routers
user_router = create_user_routes(supabase)
history_router = create_history_routes(supabase)

app.include_router(user_router, prefix="/user")
app.include_router(history_router, prefix="/history")

@app.get("/", response_class=PlainTextResponse)
async def home():
    return "Welcome to Testmate.io"


@app.post("/generate-tests")
async def generate_tests_endpoint(
    code: str, 
    user_id: Optional[str] = Depends(lambda: get_current_user_id(supabase=supabase))
):
    result = generate_tests(code)
    
    # Save to history
    if user_id:
        history_data = {
            "user_id": user_id,  # Now this is the authenticated user's ID
            "code": code,
            "action": "test_generation",
            "result": str(result)
        }
        supabase.table("user_history").insert(history_data).execute()
    
    return result

@app.post("/validate-config")
async def validate_config_endpoint(
    config:str,  #json string formate
    schema:str,
    user_id: Optional[str] = Depends(lambda: get_current_user_id(supabase=supabase))
):
    result = validate_content_with_schema(config, schema)
    
    # Save to history
    if user_id:

        history_data = {
            "user_id": user_id,  # Now this is the authenticated user's ID
            "code": f"config: {config} schema:{schema}",
            "action": "validation",
            "result": str(result)
        }
        supabase.table("user_history").insert(history_data).execute()
    
    return result


