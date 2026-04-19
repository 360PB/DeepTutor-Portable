"""Unit tests for TutorBotManager config persistence & merging."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from deeptutor.services.tutorbot.manager import BotConfig, TutorBotManager


@pytest.fixture
def manager(tmp_path: Path) -> TutorBotManager:
    """Return a TutorBotManager whose data dir is a fresh temp directory."""
    mgr = TutorBotManager()
    # Replace the path service with a stub so reads/writes stay sandboxed.
    mgr._path_service = SimpleNamespace(  # type: ignore[assignment]
        project_root=tmp_path,
        get_memory_dir=lambda: tmp_path / "memory",
    )
    return mgr


# ---------------------------------------------------------------------------
# load_bot_config / save_bot_config
# ---------------------------------------------------------------------------

class TestLoadAndSave:
    def test_load_returns_none_when_no_config(self, manager: TutorBotManager):
        assert manager.load_bot_config("nonexistent") is None

    def test_save_then_load_roundtrip(self, manager: TutorBotManager):
        cfg = BotConfig(
            name="My Bot",
            description="d",
            persona="p",
            channels={"telegram": {"enabled": True, "token": "tok"}},
            model="gpt-4o",
        )
        manager.save_bot_config("bot-a", cfg)

        loaded = manager.load_bot_config("bot-a")
        assert loaded == cfg

    def test_load_corrupt_yaml_returns_none(self, manager: TutorBotManager):
        bot_dir = manager._bot_dir("bad-bot")
        bot_dir.mkdir(parents=True, exist_ok=True)
        (bot_dir / "config.yaml").write_text(": not :: valid : yaml ::", encoding="utf-8")

        assert manager.load_bot_config("bad-bot") is None


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------

class TestAtomicWrite:
    def test_save_uses_temp_file_and_replace(self, manager: TutorBotManager, monkeypatch):
        """save_bot_config must write to a temp file then atomically replace.

        We assert that:
          1. A ``.tmp`` file is created during the write.
          2. After the call, only the final ``config.yaml`` exists (the temp
             file has been moved into place via Path.replace).
        """
        cfg = BotConfig(name="atomic", channels={"telegram": {"enabled": True}})

        observed: dict[str, list[Path]] = {"tmp_writes": [], "replaces": []}
        original_write_text = Path.write_text
        original_replace = Path.replace

        def tracked_write_text(self_path: Path, *args, **kwargs):
            if self_path.suffix == ".tmp":
                observed["tmp_writes"].append(Path(self_path))
            return original_write_text(self_path, *args, **kwargs)

        def tracked_replace(self_path: Path, target: Path):
            observed["replaces"].append((Path(self_path), Path(target)))
            return original_replace(self_path, target)

        monkeypatch.setattr(Path, "write_text", tracked_write_text)
        monkeypatch.setattr(Path, "replace", tracked_replace)

        manager.save_bot_config("atomic-bot", cfg)

        bot_dir = manager._bot_dir("atomic-bot")
        final = bot_dir / "config.yaml"
        tmp = bot_dir / "config.yaml.tmp"

        assert final.exists()
        assert not tmp.exists(), "Temp file must be moved away after save"
        assert observed["tmp_writes"], "Expected a write to a .tmp file"
        assert observed["replaces"], "Expected Path.replace to be called"

    def test_save_does_not_corrupt_existing_on_failed_write(
        self, manager: TutorBotManager, monkeypatch
    ):
        """If the write fails midway, the previous on-disk config must survive."""
        good_cfg = BotConfig(name="orig", channels={"telegram": {"enabled": True}})
        manager.save_bot_config("safe-bot", good_cfg)

        original_write_text = Path.write_text

        def boom(self_path: Path, *args, **kwargs):
            if self_path.suffix == ".tmp":
                raise OSError("disk full")
            return original_write_text(self_path, *args, **kwargs)

        monkeypatch.setattr(Path, "write_text", boom)

        with pytest.raises(OSError):
            manager.save_bot_config("safe-bot", BotConfig(name="new", channels={}))

        # Original config must still be intact.
        loaded = manager.load_bot_config("safe-bot")
        assert loaded == good_cfg


# ---------------------------------------------------------------------------
# merge_bot_config
# ---------------------------------------------------------------------------

class TestMergeBotConfig:
    def test_merge_with_no_existing_uses_defaults(self, manager: TutorBotManager):
        merged = manager.merge_bot_config("brand-new", {"name": "X"})
        assert merged.name == "X"
        assert merged.description == ""
        assert merged.channels == {}

    def test_merge_keeps_existing_when_overrides_omit_field(self, manager: TutorBotManager):
        manager.save_bot_config(
            "bot-1",
            BotConfig(name="Disk", description="dd", channels={"telegram": {}}),
        )

        merged = manager.merge_bot_config("bot-1", {"persona": "p"})
        assert merged.name == "Disk"
        assert merged.description == "dd"
        assert merged.persona == "p"
        assert merged.channels == {"telegram": {}}

    def test_merge_treats_none_as_not_provided(self, manager: TutorBotManager):
        manager.save_bot_config(
            "bot-2",
            BotConfig(name="Disk", description="dd"),
        )

        merged = manager.merge_bot_config(
            "bot-2", {"description": None, "name": "New"}
        )
        assert merged.name == "New"
        assert merged.description == "dd"

    def test_merge_treats_empty_string_and_dict_as_explicit_clear(
        self, manager: TutorBotManager
    ):
        manager.save_bot_config(
            "bot-3",
            BotConfig(
                name="Disk",
                description="dd",
                channels={"telegram": {"enabled": True}},
            ),
        )

        merged = manager.merge_bot_config(
            "bot-3", {"description": "", "channels": {}}
        )
        assert merged.description == ""
        assert merged.channels == {}

    def test_merge_ignores_unknown_keys(self, manager: TutorBotManager):
        merged = manager.merge_bot_config(
            "bot-4", {"name": "X", "unknown_field": "boom"}
        )
        assert merged.name == "X"
        assert not hasattr(merged, "unknown_field")
