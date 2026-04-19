"""
Unified Context
===============

A single data object that flows through the orchestrator into every
tool / capability / plugin invocation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Attachment:
    """A file or image attached to the user message."""

    type: str  # "image" | "file" | "pdf"
    url: str = ""
    base64: str = ""
    filename: str = ""
    mime_type: str = ""


@dataclass
class UnifiedContext:
    """
    Everything a capability or tool needs to process a single user turn.

    Attributes:
        session_id: Persistent conversation identifier.
        user_message: The current user input.
        conversation_history: Previous messages in OpenAI format.
        enabled_tools: Tool names the user has toggled on (Level 1).
            ``None`` means "not specified", while ``[]`` means
            "explicitly disable all optional tools".
        active_capability: Capability name selected by the user, or None for plain chat.
        knowledge_bases: KB names to use for RAG.
        attachments: Images / files sent with the message.
        config_overrides: Per-request config tweaks (e.g. temperature).
        language: UI / response language ("en" | "zh").
        metadata: Catch-all for capability-specific extras.
    """

    session_id: str = ""
    user_message: str = ""
    conversation_history: list[dict[str, Any]] = field(default_factory=list)
    enabled_tools: list[str] | None = None
    active_capability: str | None = None
    knowledge_bases: list[str] = field(default_factory=list)
    attachments: list[Attachment] = field(default_factory=list)
    config_overrides: dict[str, Any] = field(default_factory=dict)
    language: str = "en"
    notebook_context: str = ""
    history_context: str = ""
    memory_context: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
