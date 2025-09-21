from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class MessageRole(Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message:
    """Chat message domain entity"""
    
    def __init__(
        self,
        thread_id: UUID,
        role: MessageRole,
        content: str,
        message_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = message_id or uuid4()
        self.thread_id = thread_id
        self.role = role
        self.content = content
        self.created_at = created_at or datetime.utcnow()
    
    def is_user_message(self) -> bool:
        """Check if message is from user"""
        return self.role == MessageRole.USER
    
    def is_assistant_message(self) -> bool:
        """Check if message is from assistant"""
        return self.role == MessageRole.ASSISTANT
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Message):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)