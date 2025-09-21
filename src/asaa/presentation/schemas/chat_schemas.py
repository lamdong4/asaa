from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

from ...domain.entities.message import MessageRole


class ThreadCreateSchema(BaseModel):
    """Thread creation schema"""
    title: str


class ThreadUpdateSchema(BaseModel):
    """Thread update schema"""
    title: str


class ThreadSchema(BaseModel):
    """Thread schema"""
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime


class MessageSendSchema(BaseModel):
    """Message send schema"""
    content: str


class MessageSchema(BaseModel):
    """Message schema"""
    id: UUID
    role: MessageRole
    content: str
    created_at: datetime


class ThreadWithMessagesSchema(BaseModel):
    """Thread with messages schema"""
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageSchema]