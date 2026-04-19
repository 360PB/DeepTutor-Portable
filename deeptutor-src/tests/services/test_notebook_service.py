"""Notebook service regression tests."""

from __future__ import annotations

from deeptutor.services.notebook.service import NotebookManager, RecordType


def test_add_record_accepts_enum_record_type(tmp_path) -> None:
    manager = NotebookManager(base_dir=str(tmp_path))
    notebook = manager.create_notebook("CLI test notebook")

    result = manager.add_record(
        notebook_ids=[notebook["id"]],
        record_type=RecordType.CO_WRITER,
        title="Sample",
        user_query="Sample",
        output="# Sample",
    )

    assert result["record"]["type"] == RecordType.CO_WRITER

    stored = manager.get_notebook(notebook["id"])
    assert stored is not None
    assert stored["records"][0]["type"] == "co_writer"
