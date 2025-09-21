from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserRegistrationRequest(BaseModel):
    """User registration request DTO"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLoginRequest(BaseModel):
    """User login request DTO"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response DTO"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response DTO"""
    id: UUID
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True