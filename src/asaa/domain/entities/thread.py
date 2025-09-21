from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4


class Thread:
    """Chat thread domain entity"""
    
    def __init__(
        self,
        user_id: UUID,
        title: str,
        thread_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = thread_id or uuid4()
        self.user_id = user_id
        self.title = title
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_title(self, title: str) -> None:
        """Update thread title"""
        self.title = title
        self.updated_at = datetime.utcnow()
    
    def touch(self) -> None:
        """Update the updated_at timestamp (e.g., when a new message is added)"""
        self.updated_at = datetime.utcnow()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Thread):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)