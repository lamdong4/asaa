from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

from ...domain.entities.message import MessageRole


class ThreadCreateRequest(BaseModel):
    """Thread creation request DTO"""
    title: str


class ThreadUpdateRequest(BaseModel):
    """Thread update request DTO"""
    title: str


class ThreadResponse(BaseModel):
    """Thread response DTO"""
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MessageSendRequest(BaseModel):
    """Message send request DTO"""
    content: str


class MessageResponse(BaseModel):
    """Message response DTO"""
    id: UUID
    role: MessageRole
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ThreadWithMessagesResponse(BaseModel):
    """Thread with messages response DTO"""
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True