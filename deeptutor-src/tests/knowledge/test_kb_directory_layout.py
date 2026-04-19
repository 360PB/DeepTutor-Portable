from __future__ import annotations

from pathlib import Path

from deeptutor.knowledge.add_documents import DocumentAdder
from deeptutor.knowledge.initializer import KnowledgeBaseInitializer


def test_initializer_creates_llamaindex_only_layout(tmp_path: Path) -> None:
    initializer = KnowledgeBaseInitializer(kb_name="demo", base_dir=str(tmp_path))
    initializer.create_directory_structure()

    kb_dir = tmp_path / "demo"
    assert (kb_dir / "raw").exists()
    assert (kb_dir / "llamaindex_storage").exists()
    assert not (kb_dir / "images").exists()
    assert not (kb_dir / "content_list").exists()
    assert not (kb_dir / "rag_storage").exists()


def test_document_adder_does_not_create_compatibility_dirs(tmp_path: Path) -> None:
    kb_dir = tmp_path / "demo"
    (kb_dir / "raw").mkdir(parents=True, exist_ok=True)
    (kb_dir / "llamaindex_storage").mkdir(parents=True, exist_ok=True)

    DocumentAdder(kb_name="demo", base_dir=str(tmp_path))

    assert (kb_dir / "raw").exists()
    assert (kb_dir / "llamaindex_storage").exists()
    assert not (kb_dir / "images").exists()
    assert not (kb_dir / "content_list").exists()
