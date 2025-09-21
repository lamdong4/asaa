from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from .models import Base


class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self, database_url: str):
        # Use SQLite for simplicity - can be changed to PostgreSQL later
        if database_url.startswith("postgresql"):
            self.async_engine = create_async_engine(database_url.replace("postgresql", "postgresql+asyncpg"))
        else:
            # SQLite for development
            sqlite_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")
            self.async_engine = create_async_engine(sqlite_url)
        
        self.async_session_factory = sessionmaker(
            self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    async def create_tables(self):
        """Create database tables"""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session"""
        async with self.async_session_factory() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def close(self):
        """Close database connections"""
        await self.async_engine.dispose()