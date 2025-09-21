from abc import ABC, abstractmethod
from typing import List

from ..entities.message import Message


class AgentService(ABC):
    """Abstract agent service interface for AI interactions"""
    
    @abstractmethod
    async def generate_response(self, messages: List[Message]) -> str:
        """Generate AI response based on conversation history"""
        pass
    
    @abstractmethod
    async def generate_thread_title(self, first_message: str) -> str:
        """Generate a thread title based on the first message"""
        pass