from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...infrastructure.database.connection import DatabaseManager
from ...infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from ...infrastructure.repositories.sqlalchemy_thread_repository import SQLAlchemyThreadRepository
from ...infrastructure.repositories.sqlalchemy_message_repository import SQLAlchemyMessageRepository
from ...infrastructure.auth.password_service import PasswordService
from ...infrastructure.auth.jwt_service import JWTService
from ...infrastructure.services.openai_agent_service import OpenAIAgentService
from ...application.services.auth_service import AuthService
from ...application.services.chat_service import ChatService
from ...config import get_settings


# Global instances (will be initialized in main.py)
_db_manager: DatabaseManager = None
_password_service: PasswordService = None
_jwt_service: JWTService = None
_agent_service: OpenAIAgentService = None


def init_dependencies(db_manager: DatabaseManager, password_service: PasswordService, 
                     jwt_service: JWTService, agent_service: OpenAIAgentService):
    """Initialize global dependencies"""
    global _db_manager, _password_service, _jwt_service, _agent_service
    _db_manager = db_manager
    _password_service = password_service
    _jwt_service = jwt_service
    _agent_service = agent_service


async def get_db_session() -> AsyncSession:
    """Get database session dependency"""
    async for session in _db_manager.get_session():
        yield session


async def get_auth_service(session: AsyncSession = Depends(get_db_session)) -> AuthService:
    """Get auth service dependency"""
    user_repository = SQLAlchemyUserRepository(session)
    return AuthService(user_repository, _password_service, _jwt_service)


async def get_chat_service(session: AsyncSession = Depends(get_db_session)) -> ChatService:
    """Get chat service dependency"""
    thread_repository = SQLAlchemyThreadRepository(session)
    message_repository = SQLAlchemyMessageRepository(session)
    return ChatService(thread_repository, message_repository, _agent_service)