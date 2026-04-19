"""Configuration module for TutorBot."""

from deeptutor.tutorbot.config.paths import (
    get_cron_dir,
    get_data_dir,
    get_legacy_sessions_dir,
    get_logs_dir,
    get_media_dir,
    get_runtime_subdir,
    get_workspace_path,
)
from deeptutor.tutorbot.config.schema import (
    ChannelsConfig,
    ExecToolConfig,
    ToolsConfig,
    WebSearchConfig,
)

__all__ = [
    "ChannelsConfig",
    "ExecToolConfig",
    "ToolsConfig",
    "WebSearchConfig",
    "get_cron_dir",
    "get_data_dir",
    "get_legacy_sessions_dir",
    "get_logs_dir",
    "get_media_dir",
    "get_runtime_subdir",
    "get_workspace_path",
]
