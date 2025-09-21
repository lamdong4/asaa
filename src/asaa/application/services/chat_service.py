from typing import List, Optional
from uuid import UUID

from ...domain.entities.thread import Thread
from ...domain.entities.message import Message, MessageRole
from ...domain.repositories.thread_repository import ThreadRepository
from ...domain.repositories.message_repository import MessageRepository
from ...domain.services.agent_service import AgentService


class ChatService:
    """Application service for chat operations"""
    
    def __init__(
        self,
        thread_repository: ThreadRepository,
        message_repository: MessageRepository,
        agent_service: AgentService,
    ):
        self.thread_repository = thread_repository
        self.message_repository = message_repository
        self.agent_service = agent_service
    
    async def create_thread(self, user_id: UUID, title: str) -> Thread:
        """Create a new chat thread"""
        thread = Thread(user_id=user_id, title=title)
        return await self.thread_repository.create(thread)
    
    async def get_user_threads(self, user_id: UUID) -> List[Thread]:
        """Get all threads for a user"""
        return await self.thread_repository.get_by_user_id(user_id)
    
    async def get_thread(self, thread_id: UUID, user_id: UUID) -> Optional[Thread]:
        """Get a specific thread if it belongs to the user"""
        thread = await self.thread_repository.get_by_id(thread_id)
        if thread and thread.user_id == user_id:
            return thread
        return None
    
    async def update_thread(self, thread_id: UUID, user_id: UUID, title: str) -> Optional[Thread]:
        """Update thread title"""
        thread = await self.get_thread(thread_id, user_id)
        if not thread:
            return None
        
        thread.update_title(title)
        return await self.thread_repository.update(thread)
    
    async def delete_thread(self, thread_id: UUID, user_id: UUID) -> bool:
        """Delete a thread"""
        thread = await self.get_thread(thread_id, user_id)
        if not thread:
            return False
        
        return await self.thread_repository.delete(thread_id)
    
    async def send_message(self, thread_id: UUID, user_id: UUID, content: str) -> List[Message]:
        """Send a message and get AI response"""
        # Verify thread belongs to user
        thread = await self.get_thread(thread_id, user_id)
        if not thread:
            raise ValueError("Thread not found or access denied")
        
        # Create user message
        user_message = Message(
            thread_id=thread_id,
            role=MessageRole.USER,
            content=content,
        )
        await self.message_repository.create(user_message)
        
        # Get conversation history
        messages = await self.message_repository.get_by_thread_id(thread_id)
        
        # Generate AI response
        ai_response = await self.agent_service.generate_response(messages)
        
        # Create assistant message
        assistant_message = Message(
            thread_id=thread_id,
            role=MessageRole.ASSISTANT,
            content=ai_response,
        )
        await self.message_repository.create(assistant_message)
        
        # Update thread timestamp
        thread.touch()
        await self.thread_repository.update(thread)
        
        # If this is the first message, generate a title
        if len(messages) == 1:  # Only user message exists
            title = await self.agent_service.generate_thread_title(content)
            thread.update_title(title)
            await self.thread_repository.update(thread)
        
        return [user_message, assistant_message]
    
    async def get_thread_messages(self, thread_id: UUID, user_id: UUID) -> List[Message]:
        """Get all messages in a thread"""
        # Verify thread belongs to user
        thread = await self.get_thread(thread_id, user_id)
        if not thread:
            return []
        
        return await self.message_repository.get_by_thread_id(thread_id)