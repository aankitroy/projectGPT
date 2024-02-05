from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_database
from app.schemas import TokenSchema, User, UserAuth, UserOut
from app.utils import create_access_token, create_refresh_token, get_hashed_password, verify_password
from uuid import uuid4
from app.deps import get_current_user
from motor.motor_asyncio import AsyncIOMotorCollection

user_router = APIRouter()

@user_router.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@user_router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user

@user_router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    db = get_database()
    users: AsyncIOMotorCollection = db['users']

    # querying database to check if user already exists
    user = await users.find_one({"email": data.email})
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # saving user to the database
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4()),
        'phone': data.phone,  # replace with actual phone number
        'type': data.type,  # replace with actual user type
        'two_factor': data.two_factor,  # replace with actual two factor authentication status
        'registrationDate': data.registrationDate,  # replace with actual registration date
        'approved': data.approved,  # replace with actual approved status
        'version': data.version,  # replace with actual version
        
    }
    result = await users.insert_one(user)
    user["_id"] = result.inserted_id
    return user



@user_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()
    
    print("--------------------------Logger-----------------")
    users: AsyncIOMotorCollection = db['users']

    # querying database to check if user already exists
    user = await users.find_one({"email": form_data.username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }