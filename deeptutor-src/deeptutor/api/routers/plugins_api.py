"""
Plugins API Router
==================

Lists registered tools, capabilities, and playground plugins.
Provides direct tool execution for the Playground tester.
"""

import asyncio
import contextlib
import json
import logging
import re
import time
from typing import Any, AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from deeptutor.runtime.registry.capability_registry import get_capability_registry
from deeptutor.runtime.registry.tool_registry import get_tool_registry
from deeptutor.logging import ConsoleFormatter

logger = logging.getLogger(__name__)

router = APIRouter()
ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def _discover_plugins() -> list[Any]:
    try:
        from deeptutor.plugins.loader import discover_plugins
    except Exception:
        logger.debug("Plugin loader unavailable; returning no plugins.", exc_info=True)
        return []
    return discover_plugins()


class ToolExecuteRequest(BaseModel):
    params: dict[str, Any] = {}


class CapabilityExecuteRequest(BaseModel):
    content: str
    tools: list[str] = []
    knowledge_bases: list[str] = []
    language: str = "en"
    config: dict[str, Any] = {}
    attachments: list[dict[str, Any]] = []


@router.get("/list")
async def list_plugins():
    tool_registry = get_tool_registry()
    capability_registry = get_capability_registry()
    plugin_manifests = _discover_plugins()

    tools = [
        {
            "name": definition.name,
            "description": definition.description,
            "parameters": [
                {
                    "name": parameter.name,
                    "type": parameter.type,
                    "description": parameter.description,
                    "required": parameter.required,
                    "default": parameter.default,
                    "enum": parameter.enum,
                }
                for parameter in definition.parameters
            ],
        }
        for definition in tool_registry.get_definitions()
    ]

    capabilities = capability_registry.get_manifests()

    plugins = [
        {
            "name": plugin.name,
            "type": plugin.type,
            "description": plugin.description,
            "stages": plugin.stages,
            "version": plugin.version,
            "author": plugin.author,
        }
        for plugin in plugin_manifests
    ]

    return {
        "tools": tools,
        "capabilities": capabilities,
        "plugins": plugins,
    }


@router.post("/tools/{tool_name}/execute")
async def execute_tool(tool_name: str, body: ToolExecuteRequest):
    """Execute a single tool with explicit parameters (for Playground testing)."""
    registry = get_tool_registry()
    tool = registry.get(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    try:
        result = await tool.execute(**body.params)
        return {
            "success": result.success,
            "content": result.content,
            "sources": result.sources,
            "metadata": result.metadata,
        }
    except Exception as exc:
        logger.exception("Tool execution failed: %s", tool_name)
        raise HTTPException(status_code=500, detail=str(exc))


class _QueueLogHandler(logging.Handler):
    """Temporary handler that pushes formatted log records into an asyncio queue."""

    def __init__(self, queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
        super().__init__(level=logging.DEBUG)
        self._queue = queue
        self._loop = loop
        formatter = ConsoleFormatter(service_prefix=None)
        formatter.use_colors = False
        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord):
        line = ANSI_ESCAPE_RE.sub("", self.format(record)).strip()
        if line:
            self._loop.call_soon_threadsafe(self._queue.put_nowait, f"[Backend] {line}")


class _QueueTextStream:
    """Capture plain stdout/stderr writes and forward complete lines into the queue."""

    def __init__(self, queue: asyncio.Queue, loop: asyncio.AbstractEventLoop, stream):
        self._queue = queue
        self._loop = loop
        self._stream = stream
        self._buffer = ""

    def write(self, text: str) -> int:
        if self._stream is not None:
            self._stream.write(text)
            self._stream.flush()

        self._buffer += text
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            line = line.rstrip("\r")
            if line.strip():
                self._loop.call_soon_threadsafe(
                    self._queue.put_nowait, f"[Backend] {ANSI_ESCAPE_RE.sub('', line)}"
                )
        return len(text)

    def flush(self):
        if self._stream is not None:
            self._stream.flush()

    def isatty(self) -> bool:
        return False


def _collect_project_loggers() -> list[logging.Logger]:
    """Collect active project loggers because many do not propagate to the root logger."""
    candidates: list[logging.Logger] = []

    for parent_name in ("deeptutor", "src"):
        parent_logger = logging.getLogger(parent_name)
        if isinstance(parent_logger, logging.Logger):
            candidates.append(parent_logger)

    for name, logger_obj in logging.root.manager.loggerDict.items():
        if not (name.startswith("deeptutor") or name.startswith("src")):
            continue
        if isinstance(logger_obj, logging.Logger):
            candidates.append(logger_obj)

    unique: list[logging.Logger] = []
    seen: set[int] = set()
    for logger_obj in candidates:
        key = id(logger_obj)
        if key in seen:
            continue
        seen.add(key)
        unique.append(logger_obj)
    return unique


async def _execute_stream(tool_name: str, params: dict[str, Any]) -> AsyncGenerator[str, None]:
    """Run a tool while capturing all deeptutor.* logs and yielding SSE events."""
    registry = get_tool_registry()
    tool = registry.get(tool_name)
    if not tool:
        yield f"event: error\ndata: {json.dumps({'detail': f'Tool {tool_name!r} not found'})}\n\n"
        return

    log_queue: asyncio.Queue[str] = asyncio.Queue()
    loop = asyncio.get_running_loop()
    handler = _QueueLogHandler(log_queue, loop)
    stdout_stream = _QueueTextStream(log_queue, loop, stream=None)
    stderr_stream = _QueueTextStream(log_queue, loop, stream=None)

    attached_loggers = _collect_project_loggers()
    for logger_obj in attached_loggers:
        logger_obj.addHandler(handler)

    result_holder: dict[str, Any] = {}
    error_holder: dict[str, str] = {}
    done = asyncio.Event()

    async def _run():
        try:
            import sys

            stdout_stream._stream = sys.stdout
            stderr_stream._stream = sys.stderr
            with contextlib.redirect_stdout(stdout_stream), contextlib.redirect_stderr(
                stderr_stream
            ):
                result = await tool.execute(**params)
            result_holder["data"] = {
                "success": result.success,
                "content": result.content,
                "sources": result.sources,
                "metadata": result.metadata,
            }
        except Exception as exc:
            error_holder["detail"] = str(exc)
        finally:
            done.set()

    task = asyncio.create_task(_run())
    t0 = time.monotonic()

    try:
        while not done.is_set():
            try:
                line = await asyncio.wait_for(log_queue.get(), timeout=0.15)
                yield f"event: log\ndata: {json.dumps({'line': line})}\n\n"
            except asyncio.TimeoutError:
                pass

        while not log_queue.empty():
            line = log_queue.get_nowait()
            yield f"event: log\ndata: {json.dumps({'line': line})}\n\n"

        elapsed_ms = round((time.monotonic() - t0) * 1000)

        if error_holder:
            yield f"event: error\ndata: {json.dumps({'detail': error_holder['detail'], 'elapsed_ms': elapsed_ms})}\n\n"
        else:
            payload = {**result_holder.get("data", {}), "elapsed_ms": elapsed_ms}
            yield f"event: result\ndata: {json.dumps(payload, default=str)}\n\n"
    finally:
        for logger_obj in attached_loggers:
            if handler in logger_obj.handlers:
                logger_obj.removeHandler(handler)
        if not task.done():
            task.cancel()


@router.post("/tools/{tool_name}/execute-stream")
async def execute_tool_stream(tool_name: str, body: ToolExecuteRequest):
    """Execute a tool and stream logs + result as SSE."""
    return StreamingResponse(
        _execute_stream(tool_name, body.params),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


async def _execute_capability_stream(
    capability_name: str,
    body: CapabilityExecuteRequest,
) -> AsyncGenerator[str, None]:
    """Run a capability while streaming logs, trace events, and the final result."""
    from deeptutor.core.context import Attachment, UnifiedContext
    from deeptutor.runtime.orchestrator import ChatOrchestrator

    orch = ChatOrchestrator()
    if capability_name not in orch.list_capabilities():
        yield (
            f"event: error\ndata: "
            f"{json.dumps({'detail': f'Capability {capability_name!r} not found'})}\n\n"
        )
        return

    attachments = [
        Attachment(
            type=a.get("type", "file"),
            url=a.get("url", ""),
            base64=a.get("base64", ""),
            filename=a.get("filename", ""),
            mime_type=a.get("mime_type", ""),
        )
        for a in body.attachments
    ]

    ctx = UnifiedContext(
        user_message=body.content,
        enabled_tools=body.tools,
        active_capability=capability_name,
        knowledge_bases=body.knowledge_bases,
        attachments=attachments,
        config_overrides=body.config,
        language=body.language,
    )

    log_queue: asyncio.Queue[str] = asyncio.Queue()
    loop = asyncio.get_running_loop()
    handler = _QueueLogHandler(log_queue, loop)
    stdout_stream = _QueueTextStream(log_queue, loop, stream=None)
    stderr_stream = _QueueTextStream(log_queue, loop, stream=None)

    attached_loggers = _collect_project_loggers()
    for logger_obj in attached_loggers:
        logger_obj.addHandler(handler)

    final_result: dict[str, Any] | None = None
    error_holder: dict[str, str] = {}
    done = asyncio.Event()

    async def _run():
        nonlocal final_result
        try:
            import sys

            stdout_stream._stream = sys.stdout
            stderr_stream._stream = sys.stderr
            with contextlib.redirect_stdout(stdout_stream), contextlib.redirect_stderr(
                stderr_stream
            ):
                async for event in orch.handle(ctx):
                    if event.type.value == "result":
                        final_result = dict(event.metadata)
                        continue
                    await log_queue.put(
                        "__STREAM_EVENT__" + json.dumps(event.to_dict(), default=str)
                    )
        except Exception as exc:
            error_holder["detail"] = str(exc)
        finally:
            done.set()

    task = asyncio.create_task(_run())
    t0 = time.monotonic()

    try:
        while not done.is_set():
            try:
                line = await asyncio.wait_for(log_queue.get(), timeout=0.15)
                if line.startswith("__STREAM_EVENT__"):
                    payload = line.removeprefix("__STREAM_EVENT__")
                    yield f"event: stream\ndata: {payload}\n\n"
                else:
                    yield f"event: log\ndata: {json.dumps({'line': line})}\n\n"
            except asyncio.TimeoutError:
                pass

        while not log_queue.empty():
            line = log_queue.get_nowait()
            if line.startswith("__STREAM_EVENT__"):
                payload = line.removeprefix("__STREAM_EVENT__")
                yield f"event: stream\ndata: {payload}\n\n"
            else:
                yield f"event: log\ndata: {json.dumps({'line': line})}\n\n"

        elapsed_ms = round((time.monotonic() - t0) * 1000)
        if error_holder:
            yield (
                f"event: error\ndata: "
                f"{json.dumps({'detail': error_holder['detail'], 'elapsed_ms': elapsed_ms})}\n\n"
            )
        else:
            yield (
                f"event: result\ndata: "
                f"{json.dumps({'success': True, 'data': final_result or {}, 'elapsed_ms': elapsed_ms}, default=str)}\n\n"
            )
    finally:
        for logger_obj in attached_loggers:
            if handler in logger_obj.handlers:
                logger_obj.removeHandler(handler)
        if not task.done():
            task.cancel()


@router.post("/capabilities/{capability_name}/execute-stream")
async def execute_capability_stream(
    capability_name: str,
    body: CapabilityExecuteRequest,
):
    """Execute a capability and stream logs + trace + final result as SSE."""
    return StreamingResponse(
        _execute_capability_stream(capability_name, body),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
