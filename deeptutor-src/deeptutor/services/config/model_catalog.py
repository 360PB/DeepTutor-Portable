from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from deeptutor.services.path_service import get_path_service

from .env_store import get_env_store

CATALOG_PATH = get_path_service().get_settings_file("model_catalog")


def _service_shell() -> dict[str, Any]:
    return {
        "active_profile_id": None,
        "active_model_id": None,
        "profiles": [],
    }


def _search_shell() -> dict[str, Any]:
    return {
        "active_profile_id": None,
        "profiles": [],
    }


def _default_catalog() -> dict[str, Any]:
    return {
        "version": 1,
        "services": {
            "llm": _service_shell(),
            "embedding": _service_shell(),
            "search": _search_shell(),
        },
    }


class ModelCatalogService:
    _instance: "ModelCatalogService | None" = None

    def __init__(self, path: Path | None = None):
        self.path = path or CATALOG_PATH

    @classmethod
    def get_instance(cls, path: Path | None = None) -> "ModelCatalogService":
        if cls._instance is None:
            cls._instance = cls(path)
        return cls._instance

    def load(self) -> dict[str, Any]:
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as handle:
                loaded = json.load(handle) or {}
            catalog = _default_catalog()
            catalog.update({k: v for k, v in loaded.items() if k != "services"})
            catalog["services"].update(loaded.get("services", {}))
            hydrated = self._hydrate_missing_services_from_env(catalog)
            synced = self._sync_active_services_from_env(catalog)
            self._normalize(catalog)
            if hydrated or synced:
                self.save(catalog)
            return catalog

        catalog = self._build_from_env()
        self.save(catalog)
        return catalog

    def save(self, catalog: dict[str, Any]) -> dict[str, Any]:
        normalized = deepcopy(catalog)
        self._normalize(normalized)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump(normalized, handle, indent=2, ensure_ascii=False)
        return normalized

    def apply(self, catalog: dict[str, Any] | None = None) -> dict[str, str]:
        current = self.save(catalog or self.load())
        rendered = get_env_store().render_from_catalog(current)
        get_env_store().write(rendered)
        return rendered

    def _build_from_env(self) -> dict[str, Any]:
        summary = get_env_store().as_summary()
        catalog = _default_catalog()
        self._hydrate_missing_services_from_env(catalog)
        return catalog

    def _hydrate_missing_services_from_env(self, catalog: dict[str, Any]) -> bool:
        summary = get_env_store().as_summary()
        services = catalog.setdefault("services", {})
        changed = False

        llm_service = services.setdefault("llm", _service_shell())
        if not llm_service.get("profiles") and (summary.llm["model"] or summary.llm["host"]):
            profile_id = "llm-profile-default"
            model_id = "llm-model-default"
            services["llm"] = {
                "active_profile_id": profile_id,
                "active_model_id": model_id,
                "profiles": [
                    {
                        "id": profile_id,
                        "name": "Default LLM Endpoint",
                        "binding": summary.llm["binding"] or "openai",
                        "base_url": summary.llm["host"],
                        "api_key": summary.llm["api_key"],
                        "api_version": summary.llm["api_version"],
                        "extra_headers": {},
                        "models": [
                            {
                                "id": model_id,
                                "name": summary.llm["model"] or "Default Model",
                                "model": summary.llm["model"],
                            }
                        ],
                    }
                ],
            }
            changed = True

        embedding_service = services.setdefault("embedding", _service_shell())
        if not embedding_service.get("profiles") and (summary.embedding["model"] or summary.embedding["host"]):
            profile_id = "embedding-profile-default"
            model_id = "embedding-model-default"
            services["embedding"] = {
                "active_profile_id": profile_id,
                "active_model_id": model_id,
                "profiles": [
                    {
                        "id": profile_id,
                        "name": "Default Embedding Endpoint",
                        "binding": summary.embedding["binding"] or "openai",
                        "base_url": summary.embedding["host"],
                        "api_key": summary.embedding["api_key"],
                        "api_version": summary.embedding["api_version"],
                        "extra_headers": {},
                        "models": [
                            {
                                "id": model_id,
                                "name": summary.embedding["model"] or "Default Embedding Model",
                                "model": summary.embedding["model"],
                                "dimension": summary.embedding["dimension"] or "3072",
                            }
                        ],
                    }
                ],
            }
            changed = True

        search_service = services.setdefault("search", _search_shell())
        if not search_service.get("profiles") and (
            summary.search["provider"] or summary.search["base_url"] or summary.search["api_key"]
        ):
            profile_id = "search-profile-default"
            services["search"] = {
                "active_profile_id": profile_id,
                "profiles": [
                    {
                        "id": profile_id,
                        "name": "Default Search Provider",
                        "provider": summary.search["provider"] or "brave",
                        "base_url": summary.search["base_url"],
                        "api_key": summary.search["api_key"],
                        "api_version": "",
                        "proxy": "",
                        "models": [],
                    }
                ],
            }
            changed = True

        return changed

    def _sync_active_services_from_env(self, catalog: dict[str, Any]) -> bool:
        """
        Sync active profile/model from `.env` when keys are present.

        This makes `.env` the default source of truth so users do not need to
        manually edit or delete `model_catalog.json` after changing env values.
        """
        env_values = get_env_store().load()
        if not env_values:
            return False

        summary = get_env_store().as_summary()
        services = catalog.setdefault("services", {})
        changed = False

        def ensure_llm_profile() -> tuple[dict[str, Any], dict[str, Any]]:
            service = services.setdefault("llm", _service_shell())
            profiles = service.setdefault("profiles", [])
            if not profiles:
                profile_id = "llm-profile-default"
                model_id = "llm-model-default"
                profile = {
                    "id": profile_id,
                    "name": "Default LLM Endpoint",
                    "binding": "openai",
                    "base_url": "",
                    "api_key": "",
                    "api_version": "",
                    "extra_headers": {},
                    "models": [{"id": model_id, "name": "Default Model", "model": ""}],
                }
                service["profiles"] = [profile]
                service["active_profile_id"] = profile_id
                service["active_model_id"] = model_id
            profile = self.get_active_profile(catalog, "llm") or service["profiles"][0]
            model = self.get_active_model(catalog, "llm") or (profile.setdefault("models", [{}])[0])
            return profile, model

        def ensure_embedding_profile() -> tuple[dict[str, Any], dict[str, Any]]:
            service = services.setdefault("embedding", _service_shell())
            profiles = service.setdefault("profiles", [])
            if not profiles:
                profile_id = "embedding-profile-default"
                model_id = "embedding-model-default"
                profile = {
                    "id": profile_id,
                    "name": "Default Embedding Endpoint",
                    "binding": "openai",
                    "base_url": "",
                    "api_key": "",
                    "api_version": "",
                    "extra_headers": {},
                    "models": [
                        {
                            "id": model_id,
                            "name": "Default Embedding Model",
                            "model": "",
                            "dimension": "3072",
                        }
                    ],
                }
                service["profiles"] = [profile]
                service["active_profile_id"] = profile_id
                service["active_model_id"] = model_id
            profile = self.get_active_profile(catalog, "embedding") or service["profiles"][0]
            model = self.get_active_model(catalog, "embedding") or (profile.setdefault("models", [{}])[0])
            return profile, model

        def ensure_search_profile() -> dict[str, Any]:
            service = services.setdefault("search", _search_shell())
            profiles = service.setdefault("profiles", [])
            if not profiles:
                profile_id = "search-profile-default"
                profile = {
                    "id": profile_id,
                    "name": "Default Search Provider",
                    "provider": "brave",
                    "base_url": "",
                    "api_key": "",
                    "api_version": "",
                    "proxy": "",
                    "models": [],
                }
                service["profiles"] = [profile]
                service["active_profile_id"] = profile_id
            return self.get_active_profile(catalog, "search") or service["profiles"][0]

        llm_keys = {
            "LLM_BINDING",
            "LLM_MODEL",
            "LLM_API_KEY",
            "LLM_HOST",
            "LLM_API_VERSION",
        }
        if llm_keys.intersection(env_values.keys()):
            profile, model = ensure_llm_profile()
            if "LLM_BINDING" in env_values and profile.get("binding") != summary.llm["binding"]:
                profile["binding"] = summary.llm["binding"]
                changed = True
            if "LLM_API_KEY" in env_values and profile.get("api_key") != summary.llm["api_key"]:
                profile["api_key"] = summary.llm["api_key"]
                changed = True
            if "LLM_HOST" in env_values and profile.get("base_url") != summary.llm["host"]:
                profile["base_url"] = summary.llm["host"]
                changed = True
            if "LLM_API_VERSION" in env_values and profile.get("api_version") != summary.llm["api_version"]:
                profile["api_version"] = summary.llm["api_version"]
                changed = True
            if "LLM_MODEL" in env_values:
                if model.get("model") != summary.llm["model"]:
                    model["model"] = summary.llm["model"]
                    changed = True
                if summary.llm["model"] and model.get("name") != summary.llm["model"]:
                    model["name"] = summary.llm["model"]
                    changed = True

        embedding_keys = {
            "EMBEDDING_BINDING",
            "EMBEDDING_MODEL",
            "EMBEDDING_API_KEY",
            "EMBEDDING_HOST",
            "EMBEDDING_DIMENSION",
            "EMBEDDING_API_VERSION",
        }
        if embedding_keys.intersection(env_values.keys()):
            profile, model = ensure_embedding_profile()
            if (
                "EMBEDDING_BINDING" in env_values
                and profile.get("binding") != summary.embedding["binding"]
            ):
                profile["binding"] = summary.embedding["binding"]
                changed = True
            if (
                "EMBEDDING_API_KEY" in env_values
                and profile.get("api_key") != summary.embedding["api_key"]
            ):
                profile["api_key"] = summary.embedding["api_key"]
                changed = True
            if (
                "EMBEDDING_HOST" in env_values
                and profile.get("base_url") != summary.embedding["host"]
            ):
                profile["base_url"] = summary.embedding["host"]
                changed = True
            if (
                "EMBEDDING_API_VERSION" in env_values
                and profile.get("api_version") != summary.embedding["api_version"]
            ):
                profile["api_version"] = summary.embedding["api_version"]
                changed = True
            if "EMBEDDING_MODEL" in env_values:
                if model.get("model") != summary.embedding["model"]:
                    model["model"] = summary.embedding["model"]
                    changed = True
                if summary.embedding["model"] and model.get("name") != summary.embedding["model"]:
                    model["name"] = summary.embedding["model"]
                    changed = True
            if (
                "EMBEDDING_DIMENSION" in env_values
                and model.get("dimension") != summary.embedding["dimension"]
            ):
                model["dimension"] = summary.embedding["dimension"]
                changed = True

        search_keys = {
            "SEARCH_PROVIDER",
            "SEARCH_API_KEY",
            "SEARCH_BASE_URL",
            "SEARCH_PROXY",
        }
        if search_keys.intersection(env_values.keys()):
            profile = ensure_search_profile()
            if (
                "SEARCH_PROVIDER" in env_values
                and profile.get("provider") != summary.search["provider"]
            ):
                profile["provider"] = summary.search["provider"]
                changed = True
            if (
                "SEARCH_API_KEY" in env_values
                and profile.get("api_key") != summary.search["api_key"]
            ):
                profile["api_key"] = summary.search["api_key"]
                changed = True
            if (
                "SEARCH_BASE_URL" in env_values
                and profile.get("base_url") != summary.search["base_url"]
            ):
                profile["base_url"] = summary.search["base_url"]
                changed = True
            if "SEARCH_PROXY" in env_values and profile.get("proxy") != summary.search["proxy"]:
                profile["proxy"] = summary.search["proxy"]
                changed = True

        return changed

    def _normalize(self, catalog: dict[str, Any]) -> None:
        services = catalog.setdefault("services", {})
        services.setdefault("llm", _service_shell())
        services.setdefault("embedding", _service_shell())
        services.setdefault("search", _search_shell())
        for service_name in ("llm", "embedding", "search"):
            service = services[service_name]
            profiles = service.setdefault("profiles", [])
            for profile in profiles:
                profile.setdefault("id", f"{service_name}-profile-{uuid4().hex[:8]}")
                profile.setdefault("name", "Untitled Profile")
                profile.setdefault("api_version", "")
                profile.setdefault("base_url", "")
                profile.setdefault("api_key", "")
                if service_name == "search":
                    profile.setdefault("provider", "brave")
                    profile.setdefault("proxy", "")
                    profile["models"] = []
                else:
                    profile.setdefault("binding", "openai")
                    profile.setdefault("extra_headers", {})
                    models = profile.setdefault("models", [])
                    for model in models:
                        model.setdefault("id", f"{service_name}-model-{uuid4().hex[:8]}")
                        model.setdefault("name", model.get("model") or "Untitled Model")
                        model.setdefault("model", "")
                        if service_name == "embedding":
                            model.setdefault("dimension", "3072")
            if profiles and not service.get("active_profile_id"):
                service["active_profile_id"] = profiles[0]["id"]
            if service_name in {"llm", "embedding"}:
                if not service.get("active_model_id"):
                    active_profile = self.get_active_profile(catalog, service_name)
                    if active_profile and active_profile.get("models"):
                        service["active_model_id"] = active_profile["models"][0]["id"]

    def get_active_profile(self, catalog: dict[str, Any], service_name: str) -> dict[str, Any] | None:
        service = catalog.get("services", {}).get(service_name, {})
        active_id = service.get("active_profile_id")
        for profile in service.get("profiles", []):
            if profile.get("id") == active_id:
                return profile
        profiles = service.get("profiles", [])
        return profiles[0] if profiles else None

    def get_active_model(self, catalog: dict[str, Any], service_name: str) -> dict[str, Any] | None:
        if service_name == "search":
            return None
        service = catalog.get("services", {}).get(service_name, {})
        active_model_id = service.get("active_model_id")
        profile = self.get_active_profile(catalog, service_name)
        if not profile:
            return None
        for model in profile.get("models", []):
            if model.get("id") == active_model_id:
                return model
        models = profile.get("models", [])
        return models[0] if models else None


def get_model_catalog_service() -> ModelCatalogService:
    return ModelCatalogService.get_instance()


__all__ = ["CATALOG_PATH", "ModelCatalogService", "get_model_catalog_service"]
