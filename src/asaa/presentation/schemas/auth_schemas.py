from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserRegisterSchema(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLoginSchema(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    """Token schema"""
    access_token: str
    token_type: str = "bearer"


class UserSchema(BaseModel):
    """User schema"""
    id: UUID
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime