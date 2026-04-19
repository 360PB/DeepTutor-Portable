"""Tests for FileTypeRouter classification and helper methods."""

from __future__ import annotations

from pathlib import Path

import pytest

from deeptutor.services.rag.file_routing import (
    DocumentType,
    FileTypeRouter,
)


class TestExtensionClassification:
    @pytest.mark.parametrize(
        "filename, expected",
        [
            ("doc.pdf", DocumentType.PDF),
            ("DOC.PDF", DocumentType.PDF),  # case-insensitive
            ("notes.md", DocumentType.TEXT),
            ("readme.MARKDOWN", DocumentType.TEXT),
            ("data.json", DocumentType.TEXT),
            ("script.py", DocumentType.TEXT),
            ("config.yaml", DocumentType.TEXT),
            ("paper.docx", DocumentType.DOCX),
            ("photo.png", DocumentType.IMAGE),
        ],
    )
    def test_known_extensions(self, filename: str, expected: DocumentType) -> None:
        assert FileTypeRouter.get_document_type(filename) == expected


class TestUnknownExtensionFallback:
    def test_unknown_extension_with_text_content_is_text(self, tmp_path: Path) -> None:
        path = tmp_path / "data.weirdext"
        path.write_text("hello world", encoding="utf-8")
        assert FileTypeRouter.get_document_type(str(path)) == DocumentType.TEXT

    def test_unknown_extension_with_binary_content_is_unknown(self, tmp_path: Path) -> None:
        path = tmp_path / "blob.bin"
        path.write_bytes(b"\x00\x01\x02\xff")
        assert FileTypeRouter.get_document_type(str(path)) == DocumentType.UNKNOWN


class TestClassifyFiles:
    def test_routes_pdf_to_parser_text_to_text(self, tmp_path: Path) -> None:
        pdf = tmp_path / "a.pdf"
        pdf.write_bytes(b"%PDF-1.4")
        txt = tmp_path / "a.txt"
        txt.write_text("hi")
        png = tmp_path / "a.png"
        png.write_bytes(b"\x89PNG\r\n")

        cls = FileTypeRouter.classify_files([str(pdf), str(txt), str(png)])
        assert cls.parser_files == [str(pdf)]
        assert cls.text_files == [str(txt)]
        assert cls.unsupported == [str(png)]

    def test_empty_input_yields_empty_groups(self) -> None:
        cls = FileTypeRouter.classify_files([])
        assert cls.parser_files == []
        assert cls.text_files == []
        assert cls.unsupported == []


class TestSupportedExtensionsAndGlobs:
    def test_get_supported_extensions_covers_pdf_and_text(self) -> None:
        exts = FileTypeRouter.get_supported_extensions()
        assert ".pdf" in exts
        assert ".md" in exts
        assert ".txt" in exts

    def test_glob_patterns_match_supported_extensions(self) -> None:
        exts = FileTypeRouter.get_supported_extensions()
        patterns = FileTypeRouter.get_glob_patterns()
        assert {f"*{ext}" for ext in exts} == set(patterns)
        # Glob output should be deterministic / sorted
        assert patterns == sorted(patterns)


class TestQuickHelpers:
    def test_needs_parser_for_pdf(self) -> None:
        assert FileTypeRouter.needs_parser("paper.pdf") is True

    def test_needs_parser_false_for_text(self) -> None:
        assert FileTypeRouter.needs_parser("notes.md") is False

    def test_is_text_readable_for_text(self) -> None:
        assert FileTypeRouter.is_text_readable("readme.md") is True

    def test_is_text_readable_false_for_pdf(self) -> None:
        assert FileTypeRouter.is_text_readable("doc.pdf") is False


@pytest.mark.asyncio
class TestReadTextFile:
    async def test_reads_utf8(self, tmp_path: Path) -> None:
        path = tmp_path / "u.txt"
        path.write_text("héllo", encoding="utf-8")
        content = await FileTypeRouter.read_text_file(str(path))
        assert content == "héllo"

    async def test_reads_gbk_fallback(self, tmp_path: Path) -> None:
        path = tmp_path / "g.txt"
        path.write_bytes("中文测试".encode("gbk"))
        content = await FileTypeRouter.read_text_file(str(path))
        assert "中文" in content
