from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...domain.entities.thread import Thread
from ...domain.repositories.thread_repository import ThreadRepository
from ..database.models import ThreadModel


class SQLAlchemyThreadRepository(ThreadRepository):
    """SQLAlchemy implementation of thread repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, thread: Thread) -> Thread:
        """Create a new thread"""
        db_thread = ThreadModel(
            id=thread.id,
            user_id=thread.user_id,
            title=thread.title,
            created_at=thread.created_at,
            updated_at=thread.updated_at,
        )
        self.session.add(db_thread)
        await self.session.commit()
        await self.session.refresh(db_thread)
        return self._to_entity(db_thread)
    
    async def get_by_id(self, thread_id: UUID) -> Optional[Thread]:
        """Get thread by ID"""
        result = await self.session.execute(
            select(ThreadModel).where(ThreadModel.id == thread_id)
        )
        db_thread = result.scalar_one_or_none()
        return self._to_entity(db_thread) if db_thread else None
    
    async def get_by_user_id(self, user_id: UUID) -> List[Thread]:
        """Get all threads for a user"""
        result = await self.session.execute(
            select(ThreadModel)
            .where(ThreadModel.user_id == user_id)
            .order_by(ThreadModel.updated_at.desc())
        )
        db_threads = result.scalars().all()
        return [self._to_entity(db_thread) for db_thread in db_threads]
    
    async def update(self, thread: Thread) -> Thread:
        """Update thread"""
        result = await self.session.execute(
            select(ThreadModel).where(ThreadModel.id == thread.id)
        )
        db_thread = result.scalar_one()
        
        db_thread.title = thread.title
        db_thread.updated_at = thread.updated_at
        
        await self.session.commit()
        await self.session.refresh(db_thread)
        return self._to_entity(db_thread)
    
    async def delete(self, thread_id: UUID) -> bool:
        """Delete thread"""
        result = await self.session.execute(
            select(ThreadModel).where(ThreadModel.id == thread_id)
        )
        db_thread = result.scalar_one_or_none()
        if db_thread:
            await self.session.delete(db_thread)
            await self.session.commit()
            return True
        return False
    
    def _to_entity(self, db_thread: ThreadModel) -> Thread:
        """Convert database model to domain entity"""
        return Thread(
            thread_id=db_thread.id,
            user_id=db_thread.user_id,
            title=db_thread.title,
            created_at=db_thread.created_at,
            updated_at=db_thread.updated_at,
        )