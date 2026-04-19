"""
File Type Router
================

Centralized file type classification and routing for the RAG pipeline.
Determines the appropriate processing method for each document type.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List

from deeptutor.logging import get_logger

logger = get_logger("FileTypeRouter")


class DocumentType(Enum):
    """Document type classification."""

    PDF = "pdf"
    TEXT = "text"
    MARKDOWN = "markdown"
    DOCX = "docx"
    IMAGE = "image"
    UNKNOWN = "unknown"


@dataclass
class FileClassification:
    """Result of file classification."""

    parser_files: List[str]
    text_files: List[str]
    unsupported: List[str]


class FileTypeRouter:
    """File type router for the RAG pipeline.

    Classifies files before processing to route them to appropriate handlers:
    - PDF files -> PDF parsing
    - Text files -> Direct read (fast, simple)
    - Unsupported -> Skip with warning
    """

    PARSER_EXTENSIONS = {".pdf"}

    TEXT_EXTENSIONS = {
        ".txt",
        ".text",
        ".log",
        ".md",
        ".markdown",
        ".rst",
        ".asciidoc",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".csv",
        ".tsv",
        ".tex",
        ".latex",
        ".bib",
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".go",
        ".rs",
        ".rb",
        ".php",
        ".swift",
        ".kt",
        ".scala",
        ".r",
        ".sql",
        ".sh",
        ".bash",
        ".zsh",
        ".ps1",
        ".html",
        ".htm",
        ".xml",
        ".css",
        ".scss",
        ".sass",
        ".less",
        ".ini",
        ".cfg",
        ".conf",
        ".env",
        ".properties",
    }

    DOCX_EXTENSIONS = {".docx", ".doc"}
    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".tif"}

    @classmethod
    def get_document_type(cls, file_path: str) -> DocumentType:
        """Classify a single file by its type."""
        ext = Path(file_path).suffix.lower()

        if ext in cls.PARSER_EXTENSIONS:
            return DocumentType.PDF
        elif ext in cls.TEXT_EXTENSIONS:
            return DocumentType.TEXT
        elif ext in cls.DOCX_EXTENSIONS:
            return DocumentType.DOCX
        elif ext in cls.IMAGE_EXTENSIONS:
            return DocumentType.IMAGE
        else:
            if cls._is_text_file(file_path):
                return DocumentType.TEXT
            return DocumentType.UNKNOWN

    @classmethod
    def _is_text_file(cls, file_path: str, sample_size: int = 8192) -> bool:
        """Detect if a file is text-based by examining its content."""
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(sample_size)

            if b"\x00" in chunk:
                return False

            chunk.decode("utf-8")
            return True
        except (UnicodeDecodeError, IOError, OSError):
            return False

    @classmethod
    def classify_files(cls, file_paths: List[str]) -> FileClassification:
        """Classify a list of files by processing method."""
        parser_files = []
        text_files = []
        unsupported = []

        for path in file_paths:
            doc_type = cls.get_document_type(path)

            if doc_type == DocumentType.PDF:
                parser_files.append(path)
            elif doc_type in (DocumentType.TEXT, DocumentType.MARKDOWN):
                text_files.append(path)
            else:
                unsupported.append(path)

        logger.debug(
            f"Classified {len(file_paths)} files: "
            f"{len(parser_files)} parser, {len(text_files)} text, {len(unsupported)} unsupported"
        )

        return FileClassification(
            parser_files=parser_files,
            text_files=text_files,
            unsupported=unsupported,
        )

    @classmethod
    async def read_text_file(cls, file_path: str) -> str:
        """Read a text file with automatic encoding detection."""
        encodings = ["utf-8", "utf-8-sig", "gbk", "gb2312", "gb18030", "latin-1", "cp1252"]

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue

        with open(file_path, "rb") as f:
            return f.read().decode("utf-8", errors="replace")

    @classmethod
    def needs_parser(cls, file_path: str) -> bool:
        """Quick check if a single file needs parser processing."""
        doc_type = cls.get_document_type(file_path)
        return doc_type in (DocumentType.PDF, DocumentType.DOCX, DocumentType.IMAGE)

    @classmethod
    def is_text_readable(cls, file_path: str) -> bool:
        """Check if a file can be read directly as text."""
        doc_type = cls.get_document_type(file_path)
        return doc_type in (DocumentType.TEXT, DocumentType.MARKDOWN)

    @classmethod
    def get_supported_extensions(cls) -> set[str]:
        """Get the set of all supported file extensions."""
        return cls.PARSER_EXTENSIONS | cls.TEXT_EXTENSIONS

    @classmethod
    def get_glob_patterns(cls) -> list[str]:
        """Get glob patterns for file searching."""
        return [f"*{ext}" for ext in sorted(cls.get_supported_extensions())]
