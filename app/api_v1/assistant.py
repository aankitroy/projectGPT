from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_database
from app.schemas import Assistant, TokenSchema, User, UserAuth, UserOut
from app.utils import create_access_token, create_refresh_token, get_hashed_password, verify_password
from uuid import uuid4
from app.deps import get_current_user
from motor.motor_asyncio import AsyncIOMotorCollection
from app import helperAI
assistant_router = APIRouter()

@assistant_router.get("/assistant/get/{assistant_id}",response_model=Assistant)
async def get_assistant(assistant_id: str, user: User = Depends(get_current_user)):
    assistant = helperAI.get_assistant_by_id(assistant_id)
    if assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant