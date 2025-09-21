from typing import List
import openai

from ...domain.entities.message import Message
from ...domain.services.agent_service import AgentService


class OpenAIAgentService(AgentService):
    """OpenAI implementation of agent service"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate_response(self, messages: List[Message]) -> str:
        """Generate AI response based on conversation history"""
        # Convert domain messages to OpenAI format
        openai_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
        
        # Add system message for AWS SA context
        system_message = {
            "role": "system",
            "content": "You are an AWS Solutions Architect assistant. Help users with AWS-related questions, architecture design, best practices, and troubleshooting. Provide clear, accurate, and practical advice."
        }
        openai_messages.insert(0, system_message)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback response in case of API issues
            return f"I apologize, but I'm having trouble connecting to the AI service right now. Error: {str(e)}"
    
    async def generate_thread_title(self, first_message: str) -> str:
        """Generate a thread title based on the first message"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Generate a short, descriptive title (max 50 characters) for a conversation that starts with the given message. Focus on the main topic or question."
                    },
                    {
                        "role": "user",
                        "content": f"Generate a title for this message: {first_message}"
                    }
                ],
                max_tokens=20,
                temperature=0.5
            )
            title = response.choices[0].message.content.strip().strip('"')
            return title[:50]  # Ensure max 50 characters
        except Exception:
            # Fallback title generation
            return first_message[:50] + "..." if len(first_message) > 50 else first_message