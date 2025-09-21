from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class User:
    """User domain entity"""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        user_id: Optional[UUID] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = user_id or uuid4()
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_profile(self, full_name: Optional[str] = None) -> None:
        """Update user profile"""
        if full_name is not None:
            self.full_name = full_name
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate user account"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)