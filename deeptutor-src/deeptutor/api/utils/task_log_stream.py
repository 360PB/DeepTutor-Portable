import asyncio
import contextlib
import json
import logging
import threading
from collections import deque
from collections.abc import AsyncGenerator
from typing import Any


def _format_sse(event: str, payload: dict[str, Any]) -> str:
    return f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False, default=str)}\n\n"


_PIPELINE_LOGGER_NAMES = [
    "deeptutor.LlamaIndexPipeline",
    "deeptutor.CustomEmbedding",
    "deeptutor.EmbeddingClient",
    "deeptutor.KnowledgeInit",
]


class _TaskStreamHandler(logging.Handler):
    """Forwards log records from pipeline loggers into a task's SSE stream."""

    def __init__(self, task_id: str, manager: "KnowledgeTaskStreamManager"):
        super().__init__(level=logging.INFO)
        self._task_id = task_id
        self._manager = manager

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self._manager.emit_log(self._task_id, record.getMessage())
        except Exception:
            pass


class KnowledgeTaskStreamManager:
    _instance: "KnowledgeTaskStreamManager | None" = None
    _instance_lock = threading.Lock()

    def __init__(self):
        self._lock = threading.Lock()
        self._buffers: dict[str, deque[dict[str, Any]]] = {}
        self._subscribers: dict[str, list[tuple[asyncio.Queue, asyncio.AbstractEventLoop]]] = {}

    @classmethod
    def get_instance(cls) -> "KnowledgeTaskStreamManager":
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def ensure_task(self, task_id: str):
        with self._lock:
            self._buffers.setdefault(task_id, deque(maxlen=500))
            self._subscribers.setdefault(task_id, [])

    def emit(self, task_id: str, event: str, payload: dict[str, Any]):
        event_payload = {"event": event, "payload": payload}
        with self._lock:
            self._buffers.setdefault(task_id, deque(maxlen=500)).append(event_payload)
            subscribers = list(self._subscribers.get(task_id, []))

        for queue, loop in subscribers:
            try:
                loop.call_soon_threadsafe(self._queue_event, queue, event_payload)
            except RuntimeError:
                continue

    def emit_log(self, task_id: str, line: str):
        self.emit(task_id, "log", {"line": line, "task_id": task_id})

    def emit_complete(self, task_id: str, detail: str = "Task completed"):
        self.emit(task_id, "complete", {"detail": detail, "task_id": task_id})

    def emit_failed(self, task_id: str, detail: str):
        self.emit(task_id, "failed", {"detail": detail, "task_id": task_id})

    def subscribe(
        self, task_id: str
    ) -> tuple[asyncio.Queue[dict[str, Any]], list[dict[str, Any]], asyncio.AbstractEventLoop]:
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=200)
        loop = asyncio.get_running_loop()
        with self._lock:
            self._buffers.setdefault(task_id, deque(maxlen=500))
            self._subscribers.setdefault(task_id, []).append((queue, loop))
            backlog = list(self._buffers[task_id])
        return queue, backlog, loop

    def unsubscribe(self, task_id: str, queue: asyncio.Queue[dict[str, Any]], loop: asyncio.AbstractEventLoop):
        with self._lock:
            subscribers = self._subscribers.get(task_id, [])
            self._subscribers[task_id] = [
                (subscriber_queue, subscriber_loop)
                for subscriber_queue, subscriber_loop in subscribers
                if subscriber_queue is not queue or subscriber_loop is not loop
            ]

    async def stream(self, task_id: str) -> AsyncGenerator[str, None]:
        queue, backlog, loop = self.subscribe(task_id)
        try:
            for item in backlog:
                yield _format_sse(item["event"], item["payload"])

            if backlog and backlog[-1]["event"] in {"complete", "failed"}:
                return

            while True:
                item = await queue.get()
                yield _format_sse(item["event"], item["payload"])
                if item["event"] in {"complete", "failed"}:
                    break
        finally:
            self.unsubscribe(task_id, queue, loop)

    @staticmethod
    def _queue_event(queue: asyncio.Queue[dict[str, Any]], payload: dict[str, Any]):
        try:
            queue.put_nowait(payload)
        except asyncio.QueueFull:
            pass


@contextlib.contextmanager
def capture_task_logs(task_id: str):
    """Capture logs from pipeline loggers and forward them to the task's SSE stream.

    Only loggers in ``_PIPELINE_LOGGER_NAMES`` are tapped so that unrelated
    concurrent request logs do not leak into the stream.  The handler is also
    safe to call from ``run_in_executor`` threads because Python logging
    handlers are global and ``emit_log`` uses ``call_soon_threadsafe``.
    """
    manager = KnowledgeTaskStreamManager.get_instance()
    manager.ensure_task(task_id)

    handler = _TaskStreamHandler(task_id, manager)
    attached: list[logging.Logger] = []

    for name in _PIPELINE_LOGGER_NAMES:
        lg = logging.getLogger(name)
        lg.addHandler(handler)
        attached.append(lg)

    try:
        yield
    finally:
        for lg in attached:
            lg.removeHandler(handler)


def get_task_stream_manager() -> KnowledgeTaskStreamManager:
    return KnowledgeTaskStreamManager.get_instance()
