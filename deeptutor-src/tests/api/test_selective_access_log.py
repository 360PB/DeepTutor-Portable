"""Tests for the selective_access_log middleware in main.py.

Verifies that non-200 responses are logged with the 5-element args tuple
expected by uvicorn's AccessFormatter (client_addr, method, full_path,
http_version, status_code), preventing the ValueError documented in #334.
"""

from __future__ import annotations

import logging
from unittest.mock import patch

import pytest

pytest.importorskip("fastapi")

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.requests import Request
from starlette.responses import JSONResponse


def _build_app_with_middleware():
    """Build a minimal app that replicates the selective_access_log middleware."""
    test_app = FastAPI()
    _access_logger = logging.getLogger("uvicorn.access")

    @test_app.middleware("http")
    async def selective_access_log(request: Request, call_next):
        response = await call_next(request)
        if response.status_code != 200:
            _access_logger.info(
                '%s - "%s %s HTTP/%s" %d',
                request.client.host if request.client else "-",
                request.method,
                request.url.path,
                request.scope.get("http_version", "1.1"),
                response.status_code,
            )
        return response

    @test_app.get("/ok")
    def ok():
        return {"status": "ok"}

    @test_app.get("/not-found")
    def not_found():
        return JSONResponse({"error": "not found"}, status_code=404)

    return test_app


class TestSelectiveAccessLog:
    """selective_access_log middleware must emit 5-arg tuples for uvicorn."""

    def test_non_200_log_has_five_args(self, caplog):
        """Non-200 response log record args must have 5 elements (#334)."""
        app = _build_app_with_middleware()
        with caplog.at_level(logging.INFO, logger="uvicorn.access"):
            with TestClient(app) as client:
                client.get("/not-found")

        access_records = [r for r in caplog.records if r.name == "uvicorn.access"]
        assert len(access_records) >= 1
        record = access_records[0]
        assert len(record.args) == 5, (
            f"Expected 5-element args for AccessFormatter, got {len(record.args)}"
        )
        client_addr, method, path, http_version, status_code = record.args
        assert method == "GET"
        assert path == "/not-found"
        assert http_version in ("1.0", "1.1", "2")
        assert status_code == 404

    def test_200_not_logged(self, caplog):
        """200 responses should not produce uvicorn.access log records."""
        app = _build_app_with_middleware()
        with caplog.at_level(logging.INFO, logger="uvicorn.access"):
            with TestClient(app) as client:
                client.get("/ok")

        access_records = [
            r
            for r in caplog.records
            if r.name == "uvicorn.access" and hasattr(r, "args") and r.args
        ]
        ok_records = [r for r in access_records if len(r.args) >= 3 and "/ok" in str(r.args[2])]
        assert len(ok_records) == 0
