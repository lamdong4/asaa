from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...domain.entities.message import Message, MessageRole
from ...domain.repositories.message_repository import MessageRepository
from ..database.models import MessageModel, MessageRoleEnum


class SQLAlchemyMessageRepository(MessageRepository):
    """SQLAlchemy implementation of message repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, message: Message) -> Message:
        """Create a new message"""
        db_message = MessageModel(
            id=message.id,
            thread_id=message.thread_id,
            role=self._to_db_role(message.role),
            content=message.content,
            created_at=message.created_at,
        )
        self.session.add(db_message)
        await self.session.commit()
        await self.session.refresh(db_message)
        return self._to_entity(db_message)
    
    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get message by ID"""
        result = await self.session.execute(
            select(MessageModel).where(MessageModel.id == message_id)
        )
        db_message = result.scalar_one_or_none()
        return self._to_entity(db_message) if db_message else None
    
    async def get_by_thread_id(self, thread_id: UUID) -> List[Message]:
        """Get all messages for a thread"""
        result = await self.session.execute(
            select(MessageModel)
            .where(MessageModel.thread_id == thread_id)
            .order_by(MessageModel.created_at.asc())
        )
        db_messages = result.scalars().all()
        return [self._to_entity(db_message) for db_message in db_messages]
    
    async def delete(self, message_id: UUID) -> bool:
        """Delete message"""
        result = await self.session.execute(
            select(MessageModel).where(MessageModel.id == message_id)
        )
        db_message = result.scalar_one_or_none()
        if db_message:
            await self.session.delete(db_message)
            await self.session.commit()
            return True
        return False
    
    def _to_entity(self, db_message: MessageModel) -> Message:
        """Convert database model to domain entity"""
        return Message(
            message_id=db_message.id,
            thread_id=db_message.thread_id,
            role=self._to_domain_role(db_message.role),
            content=db_message.content,
            created_at=db_message.created_at,
        )
    
    def _to_db_role(self, role: MessageRole) -> MessageRoleEnum:
        """Convert domain role to database enum"""
        return MessageRoleEnum(role.value)
    
    def _to_domain_role(self, role: MessageRoleEnum) -> MessageRole:
        """Convert database enum to domain role"""
        return MessageRole(role.value)