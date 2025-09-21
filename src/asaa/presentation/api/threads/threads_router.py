from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ...schemas.chat_schemas import ThreadCreateSchema, ThreadUpdateSchema, ThreadSchema
from ....application.services.chat_service import ChatService
from ....domain.entities.user import User
from ..auth.auth_router import get_current_user
from ..dependencies import get_chat_service

router = APIRouter(prefix="/threads", tags=["threads"])


@router.post("/", response_model=ThreadSchema, status_code=status.HTTP_201_CREATED)
async def create_thread(
    thread_data: ThreadCreateSchema,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Create a new thread"""
    thread = await chat_service.create_thread(
        user_id=current_user.id,
        title=thread_data.title,
    )
    return ThreadSchema(
        id=thread.id,
        title=thread.title,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
    )


@router.get("/", response_model=List[ThreadSchema])
async def get_threads(
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Get all threads for current user"""
    threads = await chat_service.get_user_threads(current_user.id)
    return [
        ThreadSchema(
            id=thread.id,
            title=thread.title,
            created_at=thread.created_at,
            updated_at=thread.updated_at,
        )
        for thread in threads
    ]


@router.get("/{thread_id}", response_model=ThreadSchema)
async def get_thread(
    thread_id: UUID,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Get a specific thread"""
    thread = await chat_service.get_thread(thread_id, current_user.id)
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found",
        )
    return ThreadSchema(
        id=thread.id,
        title=thread.title,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
    )


@router.put("/{thread_id}", response_model=ThreadSchema)
async def update_thread(
    thread_id: UUID,
    thread_data: ThreadUpdateSchema,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Update a thread"""
    thread = await chat_service.update_thread(
        thread_id=thread_id,
        user_id=current_user.id,
        title=thread_data.title,
    )
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found",
        )
    return ThreadSchema(
        id=thread.id,
        title=thread.title,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
    )


@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thread(
    thread_id: UUID,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Delete a thread"""
    success = await chat_service.delete_thread(thread_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found",
        )