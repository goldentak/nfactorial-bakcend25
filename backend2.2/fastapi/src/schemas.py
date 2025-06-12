from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    bio: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class SessionList(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MessageRead(BaseModel):
    id: int
    session_id: int
    sender: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True
