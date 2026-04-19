from __future__ import annotations

import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient
router = importlib.import_module("deeptutor.api.routers.solve").router
DeepSolveCapability = importlib.import_module("deeptutor.capabilities.deep_solve").DeepSolveCapability


class _DummyLogInterceptor:
    def __init__(self, *_args, **_kwargs) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> bool:
        return False


def _build_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    return app


def test_solve_router_uses_explicit_default_tools(monkeypatch, tmp_path) -> None:
    captured: dict[str, object] = {}

    class FakeMainSolver:
        def __init__(self, **kwargs) -> None:
            captured["init"] = kwargs
            self.logger = SimpleNamespace(logger=SimpleNamespace(), display_manager=None)
            self.token_tracker = None

        async def ainit(self) -> None:
            captured["ainit"] = True

        async def solve(self, *_args, **_kwargs):
            return {"final_answer": "done", "output_dir": str(tmp_path / "solve"), "metadata": {}}

    monkeypatch.setattr("deeptutor.api.routers.solve.MainSolver", FakeMainSolver)
    monkeypatch.setattr("deeptutor.api.routers.solve.LogInterceptor", _DummyLogInterceptor)
    monkeypatch.setattr(
        "deeptutor.api.routers.solve.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr(
        "deeptutor.api.routers.solve.get_path_service",
        lambda: SimpleNamespace(get_solve_dir=lambda: Path(tmp_path)),
    )
    monkeypatch.setattr("deeptutor.api.routers.solve.get_ui_language", lambda default="en": default)

    app = _build_app()

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/solve") as websocket:
            websocket.send_json({"question": "Solve x^2=4"})
            messages = [websocket.receive_json() for _ in range(4)]

    assert [message["type"] for message in messages] == ["session", "task_id", "status", "result"]
    assert captured["init"]["enabled_tools"] == list(DeepSolveCapability.manifest.tools_used)
    assert captured["init"]["kb_name"] == "ai-textbook"
    assert captured["init"]["disable_planner_retrieve"] is False


def test_solve_router_respects_disabled_tools(monkeypatch, tmp_path) -> None:
    captured: dict[str, object] = {}

    class FakeMainSolver:
        def __init__(self, **kwargs) -> None:
            captured["init"] = kwargs
            self.logger = SimpleNamespace(logger=SimpleNamespace(), display_manager=None)
            self.token_tracker = None

        async def ainit(self) -> None:
            captured["ainit"] = True

        async def solve(self, *_args, **_kwargs):
            return {"final_answer": "done", "output_dir": str(tmp_path / "solve"), "metadata": {}}

    monkeypatch.setattr("deeptutor.api.routers.solve.MainSolver", FakeMainSolver)
    monkeypatch.setattr("deeptutor.api.routers.solve.LogInterceptor", _DummyLogInterceptor)
    monkeypatch.setattr(
        "deeptutor.api.routers.solve.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr(
        "deeptutor.api.routers.solve.get_path_service",
        lambda: SimpleNamespace(get_solve_dir=lambda: Path(tmp_path)),
    )
    monkeypatch.setattr("deeptutor.api.routers.solve.get_ui_language", lambda default="en": default)

    app = _build_app()

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/solve") as websocket:
            websocket.send_json(
                {
                    "question": "Solve x^2=4",
                    "tools": [],
                    "kb_name": "algebra",
                }
            )
            messages = [websocket.receive_json() for _ in range(4)]

    assert [message["type"] for message in messages] == ["session", "task_id", "status", "result"]
    assert captured["init"]["enabled_tools"] == []
    assert captured["init"]["kb_name"] is None
    assert captured["init"]["disable_planner_retrieve"] is True
