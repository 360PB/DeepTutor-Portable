"""
Utility module for the solve agent.
"""

from deeptutor.logging import Logger, LogLevel, get_logger, reset_logger
from .token_tracker import TokenTracker, calculate_cost, get_model_pricing

# Backwards compatibility alias used by API layer
SolveAgentLogger = Logger

__all__ = [
    # Logging
    "Logger",
    "get_logger",
    "reset_logger",
    "LogLevel",
    "SolveAgentLogger",
    # Token tracker
    "TokenTracker",
    "calculate_cost",
    "get_model_pricing",
]
