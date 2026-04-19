"""Tests for the public DeepTutor application facade."""

from __future__ import annotations

from pathlib import Path

from deeptutor.app import DeepTutorApp


class _FakeNotebookManager:
    def __init__(self) -> None:
        self.add_calls = []
        self.update_calls = []
        self.record = {
            "id": "rec-1",
            "type": "co_writer",
            "title": "Old",
            "output": "Old body",
            "metadata": {"source": "co_writer"},
        }

    def add_record(self, **kwargs):  # noqa: ANN003
        self.add_calls.append(kwargs)
        return {"record": {"id": "rec-new", **kwargs}, "added_to_notebooks": kwargs["notebook_ids"]}

    def get_record(self, notebook_id: str, record_id: str):  # noqa: ANN001
        if notebook_id == "nb1" and record_id == "rec-1":
            return dict(self.record)
        return None

    def update_record(self, notebook_id: str, record_id: str, **kwargs):  # noqa: ANN003
        self.update_calls.append((notebook_id, record_id, kwargs))
        return {"id": record_id, **kwargs}


def test_import_markdown_into_notebook_uses_co_writer_semantics(tmp_path: Path) -> None:
    markdown = tmp_path / "lesson.md"
    markdown.write_text("# Vectors\n\nSome content.", encoding="utf-8")

    app = DeepTutorApp()
    fake_manager = _FakeNotebookManager()
    app.notebooks = fake_manager

    result = app.import_markdown_into_notebook("nb1", markdown)

    assert result["record"]["id"] == "rec-new"
    add_call = fake_manager.add_calls[0]
    assert add_call["record_type"] == "co_writer"
    assert add_call["title"] == "Vectors"
    assert add_call["user_query"] == "Vectors"
    assert add_call["output"] == "# Vectors\n\nSome content."
    assert add_call["metadata"]["saved_via"] == "cli"
    assert add_call["metadata"]["source_path"] == str(markdown.resolve())


def test_replace_markdown_record_updates_existing_co_writer_record(tmp_path: Path) -> None:
    markdown = tmp_path / "updated.md"
    markdown.write_text("# Matrices\n\nUpdated body.", encoding="utf-8")

    app = DeepTutorApp()
    fake_manager = _FakeNotebookManager()
    app.notebooks = fake_manager

    result = app.replace_markdown_record("nb1", "rec-1", markdown)

    assert result["id"] == "rec-1"
    notebook_id, record_id, update_call = fake_manager.update_calls[0]
    assert notebook_id == "nb1"
    assert record_id == "rec-1"
    assert update_call["title"] == "Matrices"
    assert update_call["user_query"] == "Matrices"
    assert update_call["output"] == "# Matrices\n\nUpdated body."
    assert update_call["metadata"]["saved_via"] == "cli"
