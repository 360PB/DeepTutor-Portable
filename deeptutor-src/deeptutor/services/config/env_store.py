from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
import os
import tempfile
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

ENV_KEY_ORDER = (
    "BACKEND_PORT",
    "FRONTEND_PORT",
    "LLM_BINDING",
    "LLM_MODEL",
    "LLM_API_KEY",
    "LLM_HOST",
    "LLM_API_VERSION",
    "EMBEDDING_BINDING",
    "EMBEDDING_MODEL",
    "EMBEDDING_API_KEY",
    "EMBEDDING_HOST",
    "EMBEDDING_DIMENSION",
    "EMBEDDING_API_VERSION",
    "SEARCH_PROVIDER",
    "SEARCH_API_KEY",
    "SEARCH_BASE_URL",
    "SEARCH_PROXY",
)


def _parse_env_lines(lines: Iterable[str]) -> OrderedDict[str, str]:
    values: OrderedDict[str, str] = OrderedDict()
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def _safe_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


@dataclass(slots=True)
class ConfigSummary:
    backend_port: int
    frontend_port: int
    llm: dict[str, str]
    embedding: dict[str, str]
    search: dict[str, str]


class EnvStore:
    """Canonical `.env` reader/writer for local DeepTutor configuration."""

    def __init__(self, path: Path = ENV_PATH):
        self.path = path

    def load(self) -> OrderedDict[str, str]:
        if self.path.exists():
            values = _parse_env_lines(self.path.read_text(encoding="utf-8").splitlines())
        else:
            values = OrderedDict()
        for key, value in values.items():
            os.environ.setdefault(key, value)
        return values

    def get(self, key: str, default: str = "") -> str:
        values = self.load()
        return values.get(key, os.getenv(key, default))

    def as_summary(self) -> ConfigSummary:
        values = self.load()
        return ConfigSummary(
            backend_port=_safe_int(values.get("BACKEND_PORT") or os.getenv("BACKEND_PORT"), 8001),
            frontend_port=_safe_int(values.get("FRONTEND_PORT") or os.getenv("FRONTEND_PORT"), 3782),
            llm={
                "binding": values.get("LLM_BINDING", os.getenv("LLM_BINDING", "openai")),
                "model": values.get("LLM_MODEL", os.getenv("LLM_MODEL", "")),
                "api_key": values.get("LLM_API_KEY", os.getenv("LLM_API_KEY", "")),
                "host": values.get("LLM_HOST", os.getenv("LLM_HOST", "")),
                "api_version": values.get("LLM_API_VERSION", os.getenv("LLM_API_VERSION", "")),
            },
            embedding={
                "binding": values.get("EMBEDDING_BINDING", os.getenv("EMBEDDING_BINDING", "openai")),
                "model": values.get("EMBEDDING_MODEL", os.getenv("EMBEDDING_MODEL", "")),
                "api_key": values.get("EMBEDDING_API_KEY", os.getenv("EMBEDDING_API_KEY", "")),
                "host": values.get("EMBEDDING_HOST", os.getenv("EMBEDDING_HOST", "")),
                "dimension": values.get(
                    "EMBEDDING_DIMENSION", os.getenv("EMBEDDING_DIMENSION", "3072")
                ),
                "api_version": values.get(
                    "EMBEDDING_API_VERSION", os.getenv("EMBEDDING_API_VERSION", "")
                ),
            },
            search={
                "provider": values.get("SEARCH_PROVIDER", os.getenv("SEARCH_PROVIDER", "")),
                "api_key": values.get("SEARCH_API_KEY", os.getenv("SEARCH_API_KEY", "")),
                "base_url": values.get("SEARCH_BASE_URL", os.getenv("SEARCH_BASE_URL", "")),
                "proxy": values.get("SEARCH_PROXY", os.getenv("SEARCH_PROXY", "")),
            },
        )

    def write(self, values: dict[str, str]) -> None:
        current = self.load()
        current.update({key: value for key, value in values.items() if value is not None})
        ordered = OrderedDict()
        for key in ENV_KEY_ORDER:
            value = current.get(key, "")
            if key == "SEARCH_BASE_URL" and not value:
                continue
            ordered[key] = value

        rendered = "\n".join(f"{key}={value}" for key, value in ordered.items()) + "\n"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=str(self.path.parent),
            delete=False,
        ) as handle:
            handle.write(rendered)
            tmp_path = Path(handle.name)
        tmp_path.replace(self.path)
        for key, value in ordered.items():
            os.environ[key] = value

    def render_from_draft(self, draft: dict[str, object]) -> dict[str, str]:
        ports = draft.get("ports", {}) if isinstance(draft.get("ports"), dict) else {}
        llm = draft.get("llm", {}) if isinstance(draft.get("llm"), dict) else {}
        embedding = (
            draft.get("embedding", {}) if isinstance(draft.get("embedding"), dict) else {}
        )
        search = draft.get("search", {}) if isinstance(draft.get("search"), dict) else {}
        return {
            "BACKEND_PORT": str(ports.get("backend") or 8001),
            "FRONTEND_PORT": str(ports.get("frontend") or 3782),
            "LLM_BINDING": str(llm.get("binding") or "openai"),
            "LLM_MODEL": str(llm.get("model") or ""),
            "LLM_API_KEY": str(llm.get("api_key") or ""),
            "LLM_HOST": str(llm.get("host") or ""),
            "LLM_API_VERSION": str(llm.get("api_version") or ""),
            "EMBEDDING_BINDING": str(embedding.get("binding") or "openai"),
            "EMBEDDING_MODEL": str(embedding.get("model") or ""),
            "EMBEDDING_API_KEY": str(embedding.get("api_key") or ""),
            "EMBEDDING_HOST": str(embedding.get("host") or ""),
            "EMBEDDING_DIMENSION": str(embedding.get("dimension") or 3072),
            "EMBEDDING_API_VERSION": str(embedding.get("api_version") or ""),
            "SEARCH_PROVIDER": str(search.get("provider") or ""),
            "SEARCH_API_KEY": str(search.get("api_key") or ""),
            "SEARCH_BASE_URL": str(search.get("base_url") or ""),
            "SEARCH_PROXY": str(search.get("proxy") or ""),
        }

    def render_from_catalog(self, catalog: dict[str, Any]) -> dict[str, str]:
        services = catalog.get("services", {})
        llm_service = services.get("llm", {})
        embedding_service = services.get("embedding", {})
        search_service = services.get("search", {})

        llm_profile = self._get_active_profile(llm_service)
        llm_model = self._get_active_model(llm_service, llm_profile)
        embedding_profile = self._get_active_profile(embedding_service)
        embedding_model = self._get_active_model(embedding_service, embedding_profile)
        search_profile = self._get_active_profile(search_service)

        current = self.load()
        return {
            "BACKEND_PORT": current.get("BACKEND_PORT", os.getenv("BACKEND_PORT", "8001")),
            "FRONTEND_PORT": current.get("FRONTEND_PORT", os.getenv("FRONTEND_PORT", "3782")),
            "LLM_BINDING": str((llm_profile or {}).get("binding") or "openai"),
            "LLM_MODEL": str((llm_model or {}).get("model") or ""),
            "LLM_API_KEY": str((llm_profile or {}).get("api_key") or ""),
            "LLM_HOST": str((llm_profile or {}).get("base_url") or ""),
            "LLM_API_VERSION": str((llm_profile or {}).get("api_version") or ""),
            "EMBEDDING_BINDING": str((embedding_profile or {}).get("binding") or "openai"),
            "EMBEDDING_MODEL": str((embedding_model or {}).get("model") or ""),
            "EMBEDDING_API_KEY": str((embedding_profile or {}).get("api_key") or ""),
            "EMBEDDING_HOST": str((embedding_profile or {}).get("base_url") or ""),
            "EMBEDDING_DIMENSION": str((embedding_model or {}).get("dimension") or 3072),
            "EMBEDDING_API_VERSION": str((embedding_profile or {}).get("api_version") or ""),
            "SEARCH_PROVIDER": str((search_profile or {}).get("provider") or ""),
            "SEARCH_API_KEY": str((search_profile or {}).get("api_key") or ""),
            "SEARCH_BASE_URL": str((search_profile or {}).get("base_url") or ""),
            "SEARCH_PROXY": str((search_profile or {}).get("proxy") or ""),
        }

    def _get_active_profile(self, service: dict[str, Any]) -> dict[str, Any] | None:
        active_id = service.get("active_profile_id")
        profiles = service.get("profiles", [])
        for profile in profiles:
            if profile.get("id") == active_id:
                return profile
        return profiles[0] if profiles else None

    def _get_active_model(
        self,
        service: dict[str, Any],
        profile: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        if not profile:
            return None
        active_id = service.get("active_model_id")
        models = profile.get("models", [])
        for model in models:
            if model.get("id") == active_id:
                return model
        return models[0] if models else None


_env_store: EnvStore | None = None


def get_env_store() -> EnvStore:
    global _env_store
    if _env_store is None:
        _env_store = EnvStore()
    return _env_store


__all__ = ["ConfigSummary", "ENV_KEY_ORDER", "ENV_PATH", "EnvStore", "get_env_store"]
