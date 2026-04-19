"""
Chat Module - Lightweight conversational AI with session management.

This module provides:
- ChatAgent: Legacy conversational agent with RAG/Web Search support
- AgenticChatPipeline: Four-stage chat orchestration with autonomous tool use
- SessionManager: Chat session persistence and management

Usage:
    from deeptutor.agents.chat import ChatAgent, SessionManager

    agent = ChatAgent(language="en")
    response = await agent.process(
        message="What is machine learning?",
        history=[],
        kb_name="ai_textbook",
        enable_rag=True,
        enable_web_search=False
    )
"""

from .agentic_pipeline import AgenticChatPipeline
from .chat_agent import ChatAgent
from .session_manager import SessionManager

__all__ = ["AgenticChatPipeline", "ChatAgent", "SessionManager"]
