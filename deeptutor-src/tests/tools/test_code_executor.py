from __future__ import annotations

from pathlib import Path

from deeptutor.services.path_service import PathService
from deeptutor.tools.code_executor import _resolve_task_workspace


def test_resolve_task_workspace_uses_feature_and_turn_id(tmp_path: Path) -> None:
    service = PathService.get_instance()
    original_root = service._project_root
    original_user_dir = service._user_data_dir

    try:
        service._project_root = tmp_path
        service._user_data_dir = tmp_path / "data" / "user"

        workspace = _resolve_task_workspace(
            feature="deep_research",
            task_id="",
            session_id="session_1",
            turn_id="turn_1",
        )

        assert workspace == (
            tmp_path
            / "data"
            / "user"
            / "workspace"
            / "chat"
            / "deep_research"
            / "turn_1"
            / "code_runs"
        )
    finally:
        service._project_root = original_root
        service._user_data_dir = original_user_dir


def test_resolve_task_workspace_requires_feature() -> None:
    assert (
        _resolve_task_workspace(
            feature="",
            task_id="task_1",
            session_id="session_1",
            turn_id="turn_1",
        )
        is None
    )
