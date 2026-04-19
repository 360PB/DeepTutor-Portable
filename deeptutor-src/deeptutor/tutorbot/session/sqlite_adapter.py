"""SessionManager adapter backed by DeepTutor's SQLite store.

Implements the SessionManager interface (get_or_create, save, list_sessions) but
reads/writes through DeepTutor's SQLiteSessionStore, unifying conversation history
for TutorBot and DeepTutor in a single database.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger

from deeptutor.tutorbot.session.manager import Session


class SQLiteSessionAdapter:
    """Drop-in replacement for SessionManager, backed by DeepTutor SQLite."""

    def __init__(self, store: Any) -> None:
        """
        Args:
            store: A DeepTutor SQLiteSessionStore instance.
        """
        self.store = store
        self._cache: dict[str, Session] = {}

    @property
    def sessions_dir(self) -> Path:
        """Compatibility stub — not used when persisting to SQLite."""
        return Path("/dev/null")

    @property
    def workspace(self) -> Path:
        return Path("/dev/null")

    def _session_id(self, key: str) -> str:
        """Derive a stable DeepTutor session_id from a TutorBot key (channel:chat_id)."""
        return f"tutorbot:{key}"

    def get_or_create(self, key: str) -> Session:
        """Get or create a session synchronously (loads from SQLite via event loop)."""
        if key in self._cache:
            return self._cache[key]

        session = self._load_sync(key)
        if session is None:
            session = Session(key=key)
            self._ensure_sqlite_session_sync(key)
        self._cache[key] = session
        return session

    def save(self, session: Session) -> None:
        """Persist session messages to SQLite synchronously."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._save_async(session))
        except RuntimeError:
            asyncio.run(self._save_async(session))

    def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)

    def list_sessions(self) -> list[dict[str, Any]]:
        try:
            loop = asyncio.get_running_loop()
            future = asyncio.ensure_future(self.store.list_sessions(limit=50))
            if loop.is_running():
                return []
            return loop.run_until_complete(future)
        except RuntimeError:
            return asyncio.run(self.store.list_sessions(limit=50))

    def _load_sync(self, key: str) -> Session | None:
        """Load a session from SQLite by running the coroutine."""
        session_id = self._session_id(key)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return None

        try:
            coro = self.store.get_messages_for_context(session_id)
            messages_raw = asyncio.run(coro) if not loop else loop.run_until_complete(coro)
        except Exception:
            return None

        if not messages_raw:
            return None

        messages = [
            {"role": m["role"], "content": m.get("content", ""), "timestamp": ""}
            for m in messages_raw
        ]
        return Session(key=key, messages=messages)

    def _ensure_sqlite_session_sync(self, key: str) -> None:
        """Ensure a corresponding DeepTutor session row exists."""
        session_id = self._session_id(key)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        coro = self.store.create_session(title=f"TutorBot: {key}", session_id=session_id)
        try:
            if loop and loop.is_running():
                loop.create_task(coro)
            elif loop:
                loop.run_until_complete(coro)
            else:
                asyncio.run(coro)
        except Exception:
            logger.debug("Session {} may already exist", session_id)

    async def _save_async(self, session: Session) -> None:
        """Write new messages to SQLite."""
        session_id = self._session_id(session.key)

        existing = await self.store.get_session(session_id)
        if existing is None:
            await self.store.create_session(
                title=f"TutorBot: {session.key}", session_id=session_id,
            )

        existing_msgs = await self.store.get_messages(session_id)
        existing_count = len(existing_msgs)

        for msg in session.messages[existing_count:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role in ("user", "assistant") and content:
                await self.store.add_message(
                    session_id=session_id,
                    role=role,
                    content=content,
                    capability="tutorbot",
                )
