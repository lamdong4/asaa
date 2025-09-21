"""
Basic functionality tests for the ASAA application
"""
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from src.asaa.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to ASAA - AWS SA Agent"}


def test_user_registration_and_authentication():
    """Test user registration and authentication flow"""
    
    # Test user registration
    user_data = {
        "email": "testuser2@example.com",  # Different email to avoid conflicts
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    
    user_response = response.json()
    assert user_response["email"] == user_data["email"]
    assert user_response["full_name"] == user_data["full_name"]
    assert user_response["is_active"] is True
    assert "id" in user_response
    assert "created_at" in user_response
    
    # Test user login
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    
    token_response = response.json()
    assert "access_token" in token_response
    assert token_response["token_type"] == "bearer"
    
    # Test accessing protected endpoint
    headers = {"Authorization": f"Bearer {token_response['access_token']}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    
    me_response = response.json()
    assert me_response["email"] == user_data["email"]
    
    return token_response["access_token"], user_response["id"]


def test_thread_management():
    """Test thread CRUD operations"""
    
    # First register and login a user
    token, user_id = test_user_registration_and_authentication()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test creating a thread
    thread_data = {"title": "Test Thread"}
    response = client.post("/threads/", json=thread_data, headers=headers)
    assert response.status_code == 201
    
    thread_response = response.json()
    assert thread_response["title"] == thread_data["title"]
    assert "id" in thread_response
    thread_id = thread_response["id"]
    
    # Test getting all threads
    response = client.get("/threads/", headers=headers)
    assert response.status_code == 200
    threads = response.json()
    assert len(threads) >= 1  # May have multiple threads from other tests
    
    # Test getting specific thread
    response = client.get(f"/threads/{thread_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == thread_id
    
    # Test updating thread
    update_data = {"title": "Updated Thread Title"}
    response = client.put(f"/threads/{thread_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]
    
    return token, thread_id


def test_chat_functionality():
    """Test chat messaging functionality"""
    
    # Setup: create user and thread
    token, thread_id = test_thread_management()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test sending a message
    message_data = {"content": "Hello, what can you tell me about AWS Lambda?"}
    response = client.post(f"/chat/{thread_id}/messages", json=message_data, headers=headers)
    assert response.status_code == 200
    
    messages = response.json()
    assert len(messages) == 2  # User message + AI response
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == message_data["content"]
    assert messages[1]["role"] == "assistant"
    assert len(messages[1]["content"]) > 0  # AI should respond with something
    
    # Test getting messages
    response = client.get(f"/chat/{thread_id}/messages", headers=headers)
    assert response.status_code == 200
    retrieved_messages = response.json()
    assert len(retrieved_messages) == 2
    
    # Test getting thread with messages
    response = client.get(f"/chat/{thread_id}", headers=headers)
    assert response.status_code == 200
    thread_with_messages = response.json()
    assert "messages" in thread_with_messages
    assert len(thread_with_messages["messages"]) == 2


def test_unauthorized_access():
    """Test that protected endpoints require authentication"""
    
    # Test accessing protected endpoints without token
    endpoints = [
        ("/auth/me", "GET"),
        ("/threads/", "GET"),
        ("/threads/", "POST"),
    ]
    
    for endpoint, method in endpoints:
        if method == "GET":
            response = client.get(endpoint)
        elif method == "POST":
            response = client.post(endpoint, json={})
        
        assert response.status_code == 401