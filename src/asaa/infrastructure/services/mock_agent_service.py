from typing import List
import random

from ...domain.entities.message import Message
from ...domain.services.agent_service import AgentService


class MockAgentService(AgentService):
    """Mock agent service for development/testing"""
    
    def __init__(self):
        self.responses = [
            "I'm a mock AWS Solutions Architect assistant. In a real implementation, I would help you with AWS architecture, best practices, and troubleshooting.",
            "This is a mock response. With a real OpenAI API key, I would provide detailed AWS guidance based on your questions.",
            "Mock AWS SA Assistant: I can help with EC2, S3, Lambda, RDS, and other AWS services. Please provide your OpenAI API key for real responses.",
            "This is a demonstration response. For actual AWS solutions architecture advice, please configure the OpenAI API key in your environment.",
        ]
    
    async def generate_response(self, messages: List[Message]) -> str:
        """Generate mock AI response"""
        # Get the last user message for some context
        user_messages = [msg for msg in messages if msg.is_user_message()]
        if user_messages:
            last_message = user_messages[-1].content.lower()
            
            # Simple keyword-based responses
            if "ec2" in last_message:
                return "Mock response: EC2 (Elastic Compute Cloud) is Amazon's virtual server service. Key considerations include instance types, security groups, and auto-scaling."
            elif "s3" in last_message:
                return "Mock response: S3 (Simple Storage Service) is object storage. Consider bucket policies, versioning, and lifecycle management for optimal usage."
            elif "lambda" in last_message:
                return "Mock response: AWS Lambda is serverless compute. Key points: function timeouts, memory allocation, and cold starts."
            elif "rds" in last_message:
                return "Mock response: RDS is managed relational database service. Consider Multi-AZ deployment, backup strategies, and security groups."
        
        return random.choice(self.responses)
    
    async def generate_thread_title(self, first_message: str) -> str:
        """Generate mock thread title"""
        # Simple title generation based on keywords
        message_lower = first_message.lower()
        
        if "ec2" in message_lower:
            return "EC2 Discussion"
        elif "s3" in message_lower:
            return "S3 Configuration"
        elif "lambda" in message_lower:
            return "Lambda Function"
        elif "rds" in message_lower:
            return "Database Setup"
        elif "aws" in message_lower:
            return "AWS Architecture"
        else:
            # Fallback: use first few words
            words = first_message.split()[:4]
            title = " ".join(words)
            return title[:50] + "..." if len(title) > 50 else title