#!/usr/bin/env python
"""Migrate legacy runtime data into the new ``data/user`` layout."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def print_banner(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_step(message: str, status: str = ""):
    if status:
        print(f"  [OK] {message} - {status}")
    else:
        print(f"  ... {message}")


def move_directory(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        for item in src.iterdir():
            dst_item = dst / item.name
            if item.is_dir():
                move_directory(item, dst_item)
            elif not dst_item.exists():
                shutil.move(str(item), str(dst_item))
        if src.exists() and not any(src.iterdir()):
            src.rmdir()
    else:
        shutil.move(str(src), str(dst))
    return True


def move_file(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    shutil.move(str(src), str(dst))
    return True


def delete_file(path: Path) -> bool:
    if path.exists():
        path.unlink()
        return True
    return False
def create_structure(user_dir: Path) -> None:
    required_dirs = [
        user_dir / "settings",
        user_dir / "logs",
        user_dir / "workspace" / "memory",
        user_dir / "workspace" / "notebook",
        user_dir / "workspace" / "co-writer" / "audio",
        user_dir / "workspace" / "co-writer" / "tool_calls",
        user_dir / "workspace" / "chat" / "chat",
        user_dir / "workspace" / "chat" / "deep_solve",
        user_dir / "workspace" / "chat" / "deep_question",
        user_dir / "workspace" / "chat" / "deep_research" / "reports",
        user_dir / "workspace" / "chat" / "math_animator",
        user_dir / "workspace" / "chat" / "_detached_code_execution",
    ]
    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)
        print_step(f"Created {directory.relative_to(user_dir)}/")


def migrate() -> None:
    user_dir = project_root / "data" / "user"
    data_dir = project_root / "data"
    if not user_dir.exists():
        print("No user data directory found. Nothing to migrate.")
        return

    print_banner("User Data Migration")
    print(f"Source directory: {user_dir}")

    print_banner("Step 1: Creating New Directory Structure")
    create_structure(user_dir)

    print_banner("Step 2: Moving Chat History Database")
    legacy_chat_db = data_dir / "chat_history.db"
    new_chat_db = user_dir / "chat_history.db"
    if legacy_chat_db.exists() and not new_chat_db.exists():
        os.replace(legacy_chat_db, new_chat_db)
        print_step("Moved chat_history.db", "-> data/user/chat_history.db")
    else:
        print_step("chat_history.db", "not found or already migrated")

    print_banner("Step 3: Moving Session Files")
    session_moves = [
        (user_dir / "solver_sessions.json", user_dir / "workspace" / "chat" / "deep_solve" / "sessions.json"),
        (user_dir / "chat_sessions.json", user_dir / "workspace" / "chat" / "chat" / "sessions.json"),
    ]
    for src, dst in session_moves:
        if move_file(src, dst):
            print_step(f"Moved {src.name}", f"-> {dst.relative_to(user_dir)}")
        else:
            print_step(src.name, "not found, skipped")

    print_banner("Step 4: Moving Legacy Runtime Directories")
    moves = [
        (user_dir / "solve", user_dir / "workspace" / "chat" / "deep_solve"),
        (user_dir / "agent" / "solve", user_dir / "workspace" / "chat" / "deep_solve"),
        (user_dir / "chat", user_dir / "workspace" / "chat" / "chat"),
        (user_dir / "agent" / "chat", user_dir / "workspace" / "chat" / "chat"),
        (user_dir / "question", user_dir / "workspace" / "chat" / "deep_question"),
        (user_dir / "agent" / "question", user_dir / "workspace" / "chat" / "deep_question"),
        (user_dir / "research", user_dir / "workspace" / "chat" / "deep_research"),
        (user_dir / "agent" / "research", user_dir / "workspace" / "chat" / "deep_research"),
        (user_dir / "co-writer", user_dir / "workspace" / "co-writer"),
        (user_dir / "agent" / "co-writer", user_dir / "workspace" / "co-writer"),
        (user_dir / "workspace" / "logs", user_dir / "logs"),
        (user_dir / "logs", user_dir / "logs"),
        (user_dir / "agent" / "logs", user_dir / "logs"),
        (user_dir / "notebook", user_dir / "workspace" / "notebook"),
        (user_dir / "workspace" / "notebook", user_dir / "workspace" / "notebook"),
        (user_dir / "run_code_workspace", user_dir / "workspace" / "chat" / "_detached_code_execution"),
        (user_dir / "agent" / "run_code_workspace", user_dir / "workspace" / "chat" / "_detached_code_execution"),
        (user_dir / "agent" / "math_animator", user_dir / "workspace" / "chat" / "math_animator"),
    ]
    for src, dst in moves:
        if src == dst:
            continue
        if move_directory(src, dst):
            print_step(f"Moved {src.relative_to(user_dir)}/", f"-> {dst.relative_to(user_dir)}/")
        else:
            print_step(str(src.relative_to(user_dir)), "not found, skipped")

    print_banner("Step 5: Deleting Deprecated Files")
    deprecated_files = [
        "user_history.json",
        "settings.json",
        "llm_providers.json",
        "embedding_providers.json",
    ]
    for filename in deprecated_files:
        path = user_dir / filename
        if delete_file(path):
            print_step(f"Deleted {filename}")
        else:
            print_step(filename, "not found, skipped")

    print_banner("Migration Complete")
    print(
        """
New structure:
data/user/
├── chat_history.db
    ├── logs/
    ├── settings/
└── workspace/
    ├── memory/
    ├── notebook/
    ├── co-writer/
    ├── logs/
    └── chat/
        ├── chat/
        ├── deep_solve/
        ├── deep_question/
        ├── deep_research/
        ├── math_animator/
        └── _detached_code_execution/
"""
    )


def verify_migration() -> bool:
    print_banner("Verification")
    user_dir = project_root / "data" / "user"
    required = [
        "chat_history.db",
        "logs",
        "settings",
        "workspace/memory",
        "workspace/notebook",
        "workspace/co-writer/audio",
        "workspace/co-writer/tool_calls",
        "workspace/chat/chat",
        "workspace/chat/deep_solve",
        "workspace/chat/deep_question",
        "workspace/chat/deep_research/reports",
        "workspace/chat/math_animator",
        "workspace/chat/_detached_code_execution",
    ]

    all_ok = True
    for path in required:
        full_path = user_dir / path
        if full_path.exists():
            print_step(f"{path}/", "OK")
        else:
            print_step(f"{path}/", "MISSING!")
            all_ok = False

    deprecated = ["user_history.json", "settings.json", "llm_providers.json", "embedding_providers.json"]
    for filename in deprecated:
        path = user_dir / filename
        if path.exists():
            print_step(filename, "STILL EXISTS (should be deleted)")
            all_ok = False

    if all_ok:
        print("\n  [OK] All verifications passed!")
    else:
        print("\n  [FAIL] Some issues found. Please check above.")
    return all_ok


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate runtime data into data/user/")
    parser.add_argument("--verify", action="store_true", help="Only verify migration status")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    args = parser.parse_args()

    if args.verify:
        verify_migration()
    elif args.dry_run:
        print("DRY RUN - No changes will be made")
        print_banner("Would create settings/ + workspace/ structure and move legacy runtime files under data/user/")
    else:
        migrate()
        verify_migration()
