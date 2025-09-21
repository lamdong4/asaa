from typing import Optional
from uuid import UUID

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ...infrastructure.auth.password_service import PasswordService
from ...infrastructure.auth.jwt_service import JWTService


class AuthService:
    """Application service for authentication"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        jwt_service: JWTService,
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.jwt_service = jwt_service
    
    async def register_user(self, email: str, password: str, full_name: Optional[str] = None) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password and create user
        hashed_password = self.password_service.hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
        )
        
        return await self.user_repository.create(user)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[str]:
        """Authenticate user and return JWT token"""
        user = await self.user_repository.get_by_email(email)
        if not user or not user.is_active:
            return None
        
        if not self.password_service.verify_password(password, user.hashed_password):
            return None
        
        return self.jwt_service.create_access_token(user.id, user.email)
    
    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        payload = self.jwt_service.decode_access_token(token)
        if not payload:
            return None
        
        user_id = payload["user_id"]
        return await self.user_repository.get_by_id(user_id)