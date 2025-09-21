# ASAA - AWS Solutions Architect Agent

A FastAPI-based Agentic chat application implemented with Clean Architecture principles. This application provides OAuth2 authentication and AI-powered chat functionality for AWS Solutions Architecture assistance.

## Features

- **OAuth2 Authentication**: Secure user registration and login with JWT tokens
- **Thread Management**: Full CRUD operations for conversation threads
- **AI Chat**: 1-on-1 conversations with an AWS Solutions Architect AI agent
- **Message History**: Persistent message storage and retrieval
- **Clean Architecture**: Separation of concerns with domain, infrastructure, application, and presentation layers

## Architecture

The application follows Clean Architecture principles:

```
src/asaa/
├── domain/              # Core business logic
│   ├── entities/        # Domain entities (User, Thread, Message)
│   ├── repositories/    # Repository interfaces
│   └── services/        # Domain services (AgentService)
├── infrastructure/      # External concerns
│   ├── database/        # Database models and connections
│   ├── repositories/    # Repository implementations
│   ├── auth/           # Authentication services
│   └── services/       # External service implementations
├── application/         # Use cases and application services
│   ├── services/       # Application services
│   └── dtos/           # Data Transfer Objects
└── presentation/        # API layer
    ├── api/            # FastAPI routers
    └── schemas/        # API schemas
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd asaa
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

The application will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user information

### Threads
- `GET /threads` - Get all threads for current user
- `POST /threads` - Create a new thread
- `GET /threads/{thread_id}` - Get specific thread
- `PUT /threads/{thread_id}` - Update thread title
- `DELETE /threads/{thread_id}` - Delete thread

### Chat
- `POST /chat/{thread_id}/messages` - Send message and get AI response
- `GET /chat/{thread_id}/messages` - Get all messages in thread
- `GET /chat/{thread_id}` - Get thread with messages

## Configuration

Key environment variables:

- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: JWT secret key
- `OPENAI_API_KEY`: OpenAI API key (optional, uses mock service if not provided)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)

## Development

### With OpenAI Integration
Set your OpenAI API key in the `.env` file:
```env
OPENAI_API_KEY=your-api-key-here
```

### Mock Mode (No API Key Required)
The application includes a mock agent service that works without an OpenAI API key, perfect for development and testing.

## Testing

Run tests with:
```bash
pytest
```

## License

MIT License - see LICENSE file for details.
