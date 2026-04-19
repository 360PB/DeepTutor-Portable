"""Question generation agents."""

from importlib import import_module
from typing import Any

__all__ = ["IdeaAgent", "Generator", "FollowupAgent"]


def __getattr__(name: str) -> Any:
    if name == "Generator":
        module = import_module("deeptutor.agents.question.agents.generator")
        return getattr(module, name)
    if name == "IdeaAgent":
        module = import_module("deeptutor.agents.question.agents.idea_agent")
        return getattr(module, name)
    if name == "FollowupAgent":
        module = import_module("deeptutor.agents.question.agents.followup_agent")
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
