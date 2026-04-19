"""Research utility exports."""

from deeptutor.logging import Logger, get_logger
from deeptutor.logging import reset_logger

from .json_utils import (
    ensure_json_dict,
    ensure_json_list,
    ensure_keys,
    extract_json_from_text,
    json_to_text,
    safe_json_loads,
)
from .token_tracker import TokenTracker, get_token_tracker

def get_llm_logger(research_id: str = None, log_dir: str = None, agent_name: str = None):
    name = agent_name or "Research"
    return get_logger(name, log_dir=log_dir)


def reset_llm_logger():
    reset_logger()


__all__ = [
    "extract_json_from_text",
    "ensure_json_dict",
    "ensure_json_list",
    "ensure_keys",
    "safe_json_loads",
    "json_to_text",
    "get_token_tracker",
    "TokenTracker",
    "get_llm_logger",
    "reset_llm_logger",
    "Logger",
    "get_logger",
]
