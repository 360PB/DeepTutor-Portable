"""Path helpers for TutorBot — delegates to DeepTutor's PathService."""

from __future__ import annotations

from pathlib import Path

from deeptutor.tutorbot.utils.helpers import ensure_dir


def _base_dir() -> Path:
    from deeptutor.services.path_service import get_path_service
    return ensure_dir(get_path_service().project_root / "data" / "tutorbot")


def get_data_dir() -> Path:
    return _base_dir()


def get_runtime_subdir(name: str) -> Path:
    return ensure_dir(_base_dir() / name)


def get_media_dir(channel: str | None = None) -> Path:
    base = get_runtime_subdir("media")
    return ensure_dir(base / channel) if channel else base


def get_cron_dir() -> Path:
    return get_runtime_subdir("cron")


def get_logs_dir() -> Path:
    return get_runtime_subdir("logs")


def get_workspace_path(workspace: str | None = None) -> Path:
    if workspace:
        return ensure_dir(Path(workspace).expanduser())
    return ensure_dir(_base_dir() / "workspace")


def get_legacy_sessions_dir() -> Path:
    return _base_dir() / "sessions"


def get_shared_memory_dir() -> Path:
    """Public memory shared by DeepTutor and all bots: data/memory/."""
    from deeptutor.services.path_service import get_path_service
    return ensure_dir(get_path_service().project_root / "data" / "memory")


# ── Per-bot path helpers ──────────────────────────────────────────


def get_bot_dir(bot_id: str) -> Path:
    """data/tutorbot/{bot_id}/ — flat layout, no bots/ sub-directory."""
    return ensure_dir(_base_dir() / bot_id)


def get_bot_workspace(bot_id: str) -> Path:
    return ensure_dir(get_bot_dir(bot_id) / "workspace")


def get_bot_cron_dir(bot_id: str) -> Path:
    return ensure_dir(get_bot_dir(bot_id) / "cron")


def get_bot_logs_dir(bot_id: str) -> Path:
    return ensure_dir(get_bot_dir(bot_id) / "logs")


def get_bot_media_dir(bot_id: str, channel: str | None = None) -> Path:
    base = ensure_dir(get_bot_dir(bot_id) / "media")
    return ensure_dir(base / channel) if channel else base
