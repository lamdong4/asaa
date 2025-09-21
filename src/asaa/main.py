from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import get_settings
from .infrastructure.database.connection import DatabaseManager
from .infrastructure.auth.password_service import PasswordService
from .infrastructure.auth.jwt_service import JWTService
from .infrastructure.services.openai_agent_service import OpenAIAgentService
from .presentation.api.dependencies import init_dependencies
from .presentation.api.auth.auth_router import router as auth_router
from .presentation.api.threads.threads_router import router as threads_router
from .presentation.api.chat.chat_router import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    settings = get_settings()
    
    # Initialize database
    db_manager = DatabaseManager(settings.database_url)
    await db_manager.create_tables()
    
    # Initialize services
    password_service = PasswordService()
    jwt_service = JWTService(settings.secret_key, settings.algorithm)
    
    # Initialize agent service (with fallback if no API key)
    if settings.openai_api_key:
        agent_service = OpenAIAgentService(settings.openai_api_key, settings.openai_model)
    else:
        # Mock agent service for development
        from .infrastructure.services.mock_agent_service import MockAgentService
        agent_service = MockAgentService()
    
    # Initialize dependencies
    init_dependencies(db_manager, password_service, jwt_service, agent_service)
    
    yield
    
    # Cleanup
    await db_manager.close()


def create_app() -> FastAPI:
    """Create FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        description="FastAPI Agentic chat app with Clean architecture",
        version="0.1.0",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth_router)
    app.include_router(threads_router)
    app.include_router(chat_router)
    
    @app.get("/")
    async def root():
        return {"message": "Welcome to ASAA - AWS SA Agent"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app


app = create_app()