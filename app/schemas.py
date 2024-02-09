from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import Body

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    phone: str = Field(..., description="user phone number")
    type: str = Field(..., description="user type")
    two_factor: str = Field(..., description="user two factor authentication")
    registrationDate: datetime = Field(..., description="user registration date")
    approved: bool = Field(..., description="user approved status")
    version: int = Field(..., description="user version")
    

class UserOut(BaseModel):
    id: UUID
    email: str
    registrationDate: datetime
    phone: str  # add this line
    type: str  # add this line
    two_factor: str  # add this line
    approved: bool  # add this line
    version: int  # add this line

class User(UserOut):
    password: str
    
    
    
class Assistant(BaseModel):
    id: str
    name: str
    description: str
    version: str