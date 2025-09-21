from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ..database.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of user repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        """Create a new user"""
        db_user = UserModel(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return self._to_entity(db_user)
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def update(self, user: User) -> User:
        """Update user"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        db_user = result.scalar_one()
        
        db_user.email = user.email
        db_user.hashed_password = user.hashed_password
        db_user.full_name = user.full_name
        db_user.is_active = user.is_active
        db_user.updated_at = user.updated_at
        
        await self.session.commit()
        await self.session.refresh(db_user)
        return self._to_entity(db_user)
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete user"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        if db_user:
            await self.session.delete(db_user)
            await self.session.commit()
            return True
        return False
    
    def _to_entity(self, db_user: UserModel) -> User:
        """Convert database model to domain entity"""
        return User(
            user_id=db_user.id,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            full_name=db_user.full_name,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )