from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_database
from app.schemas import Assistant, GenerateResponseInput, TokenSchema, User, UserAuth, UserOut
from app.utils import create_access_token, create_refresh_token, get_hashed_password, verify_password
from uuid import uuid4
from app.deps import get_current_user
from motor.motor_asyncio import AsyncIOMotorCollection
from app import helperAI
assistant_router = APIRouter()

@assistant_router.get("/get/{assistant_id}",response_model=Assistant)
async def get_assistant(assistant_id: str, user: User = Depends(get_current_user)):
    assistant = helperAI.get_assistant_by_id(assistant_id)
    if assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant


@assistant_router.post("/generate_response")
async def get_ai_response(input_data: GenerateResponseInput, user: User = Depends(get_current_user)):
    try:
        assistant = helperAI.get_assistant_by_id(input_data.assistant_id)
        new_message = helperAI.generate_response(input_data.message_body, input_data.thread_id, user['email'], assistant)
        return new_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@assistant_router.delete("/thread")
async def delete_thread(user: User = Depends(get_current_user)):
    try:
        return helperAI.remove_if_thread_exists(user['id'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))