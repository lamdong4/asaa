from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.thread import Thread


class ThreadRepository(ABC):
    """Abstract thread repository interface"""
    
    @abstractmethod
    async def create(self, thread: Thread) -> Thread:
        """Create a new thread"""
        pass
    
    @abstractmethod
    async def get_by_id(self, thread_id: UUID) -> Optional[Thread]:
        """Get thread by ID"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Thread]:
        """Get all threads for a user"""
        pass
    
    @abstractmethod
    async def update(self, thread: Thread) -> Thread:
        """Update thread"""
        pass
    
    @abstractmethod
    async def delete(self, thread_id: UUID) -> bool:
        """Delete thread"""
        pass