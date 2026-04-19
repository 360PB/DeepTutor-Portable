"""
Logging Configuration
=====================

Unified logging configuration for the entire DeepTutor system.
A single `level` parameter controls all logging (including RAG modules).
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class LoggingConfig:
    """Configuration for the logging system."""

    # Global log level (controls entire system including RAG modules)
    level: str = "DEBUG"

    # Output settings
    console_output: bool = True
    file_output: bool = True

    # Log directory (relative to project root or absolute)
    log_dir: Optional[str] = None

    # File rotation settings
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


def get_default_log_dir() -> Path:
    """Get the default log directory."""
    from deeptutor.services.path_service import get_path_service
    
    path_service = get_path_service()
    return path_service.get_logs_dir()


def get_global_log_level() -> str:
    """
    Get the global log level from config/main.yaml -> logging.level
    Default: DEBUG
    """
    try:
        from deeptutor.services.config import PROJECT_ROOT, load_config_with_main

        config = load_config_with_main("main.yaml", PROJECT_ROOT)
        logging_config = config.get("logging", {})
        return logging_config.get("level", "DEBUG").upper()
    except Exception:
        return "DEBUG"


def load_logging_config() -> LoggingConfig:
    """
    Load logging configuration from config files.

    Returns:
        LoggingConfig instance with loaded or default values.
    """
    try:
        from deeptutor.services.config import PROJECT_ROOT, get_path_from_config, load_config_with_main

        config = load_config_with_main("main.yaml", PROJECT_ROOT)

        logging_config = config.get("logging", {})
        level = get_global_log_level()

        return LoggingConfig(
            level=level,
            console_output=logging_config.get("console_output", True),
            file_output=logging_config.get("save_to_file", True),
            log_dir=get_path_from_config(config, "user_log_dir"),
        )
    except Exception:
        return LoggingConfig()
