#!/usr/bin/env python
"""Incrementally add documents to a llamaindex knowledge base."""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
from typing import List, Optional

from dotenv import load_dotenv

from deeptutor.logging import get_logger
from deeptutor.services.rag.factory import DEFAULT_PROVIDER
from deeptutor.services.rag.pipelines.llamaindex import LlamaIndexPipeline

logger = get_logger("KnowledgeInit")

DEFAULT_BASE_DIR = "./data/knowledge_bases"


class DocumentAdder:
    """Add documents to an existing llamaindex knowledge base."""

    def __init__(
        self,
        kb_name: str,
        base_dir: str = DEFAULT_BASE_DIR,
        api_key: str | None = None,
        base_url: str | None = None,
        progress_tracker=None,
        rag_provider: str | None = None,
    ):
        self.kb_name = kb_name
        self.base_dir = Path(base_dir)
        self.kb_dir = self.base_dir / kb_name

        if not self.kb_dir.exists():
            raise ValueError(f"Knowledge base does not exist: {kb_name}")

        self.raw_dir = self.kb_dir / "raw"
        self.llamaindex_storage_dir = self.kb_dir / "llamaindex_storage"
        self.legacy_rag_storage_dir = self.kb_dir / "rag_storage"
        self.metadata_file = self.kb_dir / "metadata.json"

        if not self.llamaindex_storage_dir.exists() and self.legacy_rag_storage_dir.exists():
            raise ValueError(
                f"Knowledge base '{kb_name}' uses legacy index format and requires reindex before incremental add"
            )

        if not self.llamaindex_storage_dir.exists():
            raise ValueError(f"Knowledge base not initialized (llamaindex): {kb_name}")

        if rag_provider and rag_provider != DEFAULT_PROVIDER:
            logger.warning(
                f"Requested provider '{rag_provider}' ignored. Using '{DEFAULT_PROVIDER}' for consistency."
            )

        self.api_key = api_key
        self.base_url = base_url
        self.progress_tracker = progress_tracker

        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_hash(self, file_path: Path) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def get_ingested_hashes(self) -> dict[str, str]:
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("file_hashes", {})
            except Exception:
                return {}
        return {}

    def add_documents(self, source_files: List[str], allow_duplicates: bool = False) -> List[Path]:
        """Validate and stage files into raw/ before indexing."""
        logger.info(f"Validating documents for '{self.kb_name}'...")

        ingested_hashes = self.get_ingested_hashes()
        files_to_process: list[Path] = []

        for source in source_files:
            source_path = Path(source)
            if not source_path.exists() or not source_path.is_file():
                logger.warning(f"Missing file: {source}")
                continue

            current_hash = self._get_file_hash(source_path)
            if current_hash in ingested_hashes.values() and not allow_duplicates:
                logger.info(f"Skipped (content already indexed): {source_path.name}")
                continue

            dest_path = self.raw_dir / source_path.name
            if dest_path.exists():
                dest_hash = self._get_file_hash(dest_path)
                if dest_hash == current_hash:
                    logger.info(f"Recovering staged file: {source_path.name}")
                    files_to_process.append(dest_path)
                    continue
                if not allow_duplicates:
                    logger.info(f"Skipped (filename collision): {source_path.name}")
                    continue

            shutil.copy2(source_path, dest_path)
            logger.info(f"Staged to raw: {source_path.name}")
            files_to_process.append(dest_path)

        return files_to_process

    async def process_new_documents(self, new_files: List[Path]) -> List[Path]:
        """Index staged files via llamaindex incremental add."""
        if not new_files:
            return []

        pipeline = LlamaIndexPipeline(kb_base_dir=str(self.base_dir))
        processed_files: list[Path] = []
        total_files = len(new_files)

        for idx, doc_file in enumerate(new_files, 1):
            try:
                if self.progress_tracker is not None:
                    from deeptutor.knowledge.progress_tracker import ProgressStage

                    self.progress_tracker.update(
                        ProgressStage.PROCESSING_FILE,
                        f"Indexing (LlamaIndex) {doc_file.name}",
                        current=idx,
                        total=total_files,
                    )

                success = await pipeline.add_documents(self.kb_name, [str(doc_file)])
                if success:
                    processed_files.append(doc_file)
                    self._record_successful_hash(doc_file)
                    logger.info(f"Processed (LlamaIndex): {doc_file.name}")
                else:
                    logger.error(f"Failed to index: {doc_file.name}")
            except Exception as e:
                logger.exception(f"Failed {doc_file.name}: {e}")

        return processed_files

    def _record_successful_hash(self, file_path: Path) -> None:
        file_hash = self._get_file_hash(file_path)

        metadata: dict = {}
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
            except Exception:
                metadata = {}

        metadata.setdefault("file_hashes", {})[file_path.name] = file_hash
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def extract_numbered_items_for_new_docs(self, processed_files: List[Path], batch_size: int = 20) -> None:
        """Compatibility no-op: numbered-item extraction is deprecated."""
        _ = batch_size
        if processed_files:
            logger.info("Skipping numbered items extraction for incremental add (feature removed)")

    def update_metadata(self, added_count: int) -> None:
        """Update metadata after incremental add."""
        metadata: dict = {}
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
            except Exception:
                metadata = {}

        metadata["rag_provider"] = DEFAULT_PROVIDER
        metadata["needs_reindex"] = False
        metadata["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        history = metadata.get("update_history", [])
        history.append(
            {
                "timestamp": metadata["last_updated"],
                "action": "incremental_add",
                "count": added_count,
                "provider": DEFAULT_PROVIDER,
            }
        )
        metadata["update_history"] = history

        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)


async def add_documents(
    kb_name: str,
    source_files: list[str],
    base_dir: str = DEFAULT_BASE_DIR,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    allow_duplicates: bool = False,
) -> int:
    """Convenience function used by CLI wrappers."""
    from deeptutor.knowledge.manager import KnowledgeBaseManager

    manager = KnowledgeBaseManager(base_dir=base_dir)
    try:
        manager.update_kb_status(
            name=kb_name,
            status="processing",
            progress={
                "stage": "processing_documents",
                "message": "Processing uploaded documents...",
                "percent": 0,
                "current": 0,
                "total": max(len(source_files), 1),
                "file_name": "",
                "error": None,
                "timestamp": datetime.now().isoformat(),
            },
        )

        adder = DocumentAdder(
            kb_name=kb_name,
            base_dir=base_dir,
            api_key=api_key,
            base_url=base_url,
            rag_provider=DEFAULT_PROVIDER,
        )
        new_files = adder.add_documents(source_files, allow_duplicates=allow_duplicates)
        if not new_files:
            manager.update_kb_status(
                name=kb_name,
                status="ready",
                progress={
                    "stage": "completed",
                    "message": "No new unique documents to process.",
                    "percent": 100,
                    "current": 1,
                    "total": 1,
                    "file_name": "",
                    "error": None,
                    "timestamp": datetime.now().isoformat(),
                },
            )
            return 0
        processed = await adder.process_new_documents(new_files)
        adder.extract_numbered_items_for_new_docs(processed)
        adder.update_metadata(len(processed))

        manager.update_kb_status(
            name=kb_name,
            status="ready",
            progress={
                "stage": "completed",
                "message": f"Successfully processed {len(processed)} files!",
                "percent": 100,
                "current": len(processed),
                "total": max(len(new_files), 1),
                "file_name": "",
                "error": None,
                "timestamp": datetime.now().isoformat(),
            },
        )
        return len(processed)
    except Exception as exc:
        manager.update_kb_status(
            name=kb_name,
            status="error",
            progress={
                "stage": "error",
                "message": "Document upload failed",
                "percent": 0,
                "current": 0,
                "total": max(len(source_files), 1),
                "file_name": "",
                "error": str(exc),
                "timestamp": datetime.now().isoformat(),
            },
        )
        raise


async def main() -> None:
    parser = argparse.ArgumentParser(description="Incrementally add documents to a KB")
    parser.add_argument("kb_name", help="KB Name")
    parser.add_argument("--docs", nargs="+", help="Files")
    parser.add_argument("--docs-dir", help="Directory")
    parser.add_argument("--base-dir", default=DEFAULT_BASE_DIR)
    parser.add_argument("--api-key", default=os.getenv("LLM_API_KEY"))
    parser.add_argument("--base-url", default=os.getenv("LLM_HOST"))
    parser.add_argument("--allow-duplicates", action="store_true")

    args = parser.parse_args()
    load_dotenv()

    doc_files: list[str] = []
    if args.docs:
        doc_files.extend(args.docs)
    if args.docs_dir:
        p = Path(args.docs_dir)
        for ext in ["*.pdf", "*.txt", "*.md", "*.json", "*.csv"]:
            doc_files.extend([str(f) for f in p.glob(ext)])

    if not doc_files:
        logger.error("No documents provided.")
        return

    processed_count = await add_documents(
        kb_name=args.kb_name,
        source_files=doc_files,
        base_dir=args.base_dir,
        api_key=args.api_key,
        base_url=args.base_url,
        allow_duplicates=args.allow_duplicates,
    )

    if processed_count:
        logger.info(f"Done! Successfully added {processed_count} documents.")
    else:
        logger.info("No new unique documents to add.")


if __name__ == "__main__":
    asyncio.run(main())
