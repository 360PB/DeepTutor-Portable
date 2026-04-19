from pathlib import Path

from deeptutor.services.config.env_store import EnvStore
from deeptutor.services.config.model_catalog import ModelCatalogService


def test_load_hydrates_empty_catalog_from_env(tmp_path: Path, monkeypatch):
    env_path = tmp_path / ".env"
    env_path.write_text(
        "\n".join(
            [
                "LLM_BINDING=google",
                "LLM_MODEL=gemini-3-flash-preview",
                "LLM_API_KEY=test-llm-key",
                "LLM_HOST=https://example-llm.test/v1",
                "EMBEDDING_BINDING=openai",
                "EMBEDDING_MODEL=text-embedding-3-large",
                "EMBEDDING_API_KEY=test-emb-key",
                "EMBEDDING_HOST=https://example-emb.test/v1",
                "EMBEDDING_DIMENSION=3072",
                "SEARCH_PROVIDER=perplexity",
                "SEARCH_API_KEY=test-search-key",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    catalog_path = tmp_path / "model_catalog.json"
    catalog_path.write_text(
        """{
  "version": 1,
  "services": {
    "llm": {"active_profile_id": null, "active_model_id": null, "profiles": []},
    "embedding": {"active_profile_id": null, "active_model_id": null, "profiles": []},
    "search": {"active_profile_id": null, "profiles": []}
  }
}
""",
        encoding="utf-8",
    )

    env_store = EnvStore(path=env_path)
    monkeypatch.setattr("deeptutor.services.config.model_catalog.get_env_store", lambda: env_store)

    service = ModelCatalogService(path=catalog_path)
    catalog = service.load()

    assert catalog["services"]["llm"]["profiles"][0]["binding"] == "google"
    assert catalog["services"]["llm"]["profiles"][0]["extra_headers"] == {}
    assert catalog["services"]["llm"]["profiles"][0]["models"][0]["model"] == "gemini-3-flash-preview"
    assert catalog["services"]["embedding"]["profiles"][0]["models"][0]["dimension"] == "3072"
    assert catalog["services"]["search"]["profiles"][0]["provider"] == "perplexity"
    assert catalog["services"]["search"]["profiles"][0]["proxy"] == ""


def test_load_syncs_existing_active_profiles_from_env(tmp_path: Path, monkeypatch):
    env_path = tmp_path / ".env"
    env_path.write_text(
        "\n".join(
            [
                "LLM_BINDING=dashscope",
                "LLM_MODEL=qwen3.5-plus",
                "LLM_API_KEY=new-llm-key",
                "LLM_HOST=https://dashscope.aliyuncs.com/compatible-mode/v1",
                "EMBEDDING_BINDING=dashscope",
                "EMBEDDING_MODEL=text-embedding-v4",
                "EMBEDDING_API_KEY=new-emb-key",
                "EMBEDDING_HOST=https://dashscope.aliyuncs.com/compatible-mode/v1",
                "EMBEDDING_DIMENSION=2048",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    catalog_path = tmp_path / "model_catalog.json"
    catalog_path.write_text(
        """{
  "version": 1,
  "services": {
    "llm": {
      "active_profile_id": "llm-profile-default",
      "active_model_id": "llm-model-default",
      "profiles": [
        {
          "id": "llm-profile-default",
          "name": "Default LLM Endpoint",
          "binding": "openai",
          "base_url": "https://old-llm.example/v1",
          "api_key": "old-llm-key",
          "api_version": "",
          "extra_headers": {},
          "models": [
            {"id": "llm-model-default", "name": "old-model", "model": "old-model"}
          ]
        }
      ]
    },
    "embedding": {
      "active_profile_id": "embedding-profile-default",
      "active_model_id": "embedding-model-default",
      "profiles": [
        {
          "id": "embedding-profile-default",
          "name": "Default Embedding Endpoint",
          "binding": "openai",
          "base_url": "https://old-emb.example/v1",
          "api_key": "old-emb-key",
          "api_version": "",
          "extra_headers": {},
          "models": [
            {
              "id": "embedding-model-default",
              "name": "old-embedding",
              "model": "old-embedding",
              "dimension": "3072"
            }
          ]
        }
      ]
    },
    "search": {"active_profile_id": null, "profiles": []}
  }
}
""",
        encoding="utf-8",
    )

    env_store = EnvStore(path=env_path)
    monkeypatch.setattr("deeptutor.services.config.model_catalog.get_env_store", lambda: env_store)

    service = ModelCatalogService(path=catalog_path)
    catalog = service.load()

    llm_profile = catalog["services"]["llm"]["profiles"][0]
    llm_model = llm_profile["models"][0]
    emb_profile = catalog["services"]["embedding"]["profiles"][0]
    emb_model = emb_profile["models"][0]

    assert llm_profile["binding"] == "dashscope"
    assert llm_profile["base_url"] == "https://dashscope.aliyuncs.com/compatible-mode/v1"
    assert llm_profile["api_key"] == "new-llm-key"
    assert llm_model["model"] == "qwen3.5-plus"
    assert llm_model["name"] == "qwen3.5-plus"
    assert emb_profile["binding"] == "dashscope"
    assert emb_profile["base_url"] == "https://dashscope.aliyuncs.com/compatible-mode/v1"
    assert emb_profile["api_key"] == "new-emb-key"
    assert emb_model["model"] == "text-embedding-v4"
    assert emb_model["name"] == "text-embedding-v4"
    assert emb_model["dimension"] == "2048"
