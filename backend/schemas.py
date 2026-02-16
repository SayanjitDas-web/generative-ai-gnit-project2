from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class InterviewSessionBase(BaseModel):
    topic: str
    difficulty: str

class InterviewSessionCreate(InterviewSessionBase):
    pass

class InterviewSessionResponse(InterviewSessionBase):
    id: int
    user_id: int
    status: str
    feedback: Optional[Dict[str, Any]] = None
    created_at: datetime
    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    role: str
    content: str

class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime
    class Config:
        from_attributes = True
