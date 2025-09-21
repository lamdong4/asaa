from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ...schemas.chat_schemas import MessageSendSchema, MessageSchema, ThreadWithMessagesSchema
from ....application.services.chat_service import ChatService
from ....domain.entities.user import User
from ..auth.auth_router import get_current_user
from ..dependencies import get_chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/{thread_id}/messages", response_model=List[MessageSchema])
async def send_message(
    thread_id: UUID,
    message_data: MessageSendSchema,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Send a message and get AI response"""
    try:
        messages = await chat_service.send_message(
            thread_id=thread_id,
            user_id=current_user.id,
            content=message_data.content,
        )
        return [
            MessageSchema(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at,
            )
            for msg in messages
        ]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/{thread_id}/messages", response_model=List[MessageSchema])
async def get_messages(
    thread_id: UUID,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Get all messages in a thread"""
    messages = await chat_service.get_thread_messages(thread_id, current_user.id)
    return [
        MessageSchema(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at,
        )
        for msg in messages
    ]


@router.get("/{thread_id}", response_model=ThreadWithMessagesSchema)
async def get_thread_with_messages(
    thread_id: UUID,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Get thread with all messages"""
    thread = await chat_service.get_thread(thread_id, current_user.id)
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found",
        )
    
    messages = await chat_service.get_thread_messages(thread_id, current_user.id)
    
    return ThreadWithMessagesSchema(
        id=thread.id,
        title=thread.title,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
        messages=[
            MessageSchema(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at,
            )
            for msg in messages
        ],
    )