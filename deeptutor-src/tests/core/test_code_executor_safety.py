from __future__ import annotations

import pytest

from deeptutor.tools.code_executor import CodeExecutionError, ImportGuard


def test_import_guard_rejects_unsafe_builtin_calls() -> None:
    with pytest.raises(CodeExecutionError):
        ImportGuard.validate("print(open('secret.txt').read())", ["math"])


def test_import_guard_rejects_unsafe_module_access() -> None:
    with pytest.raises(CodeExecutionError):
        ImportGuard.validate("import math\nos.system('whoami')", ["math"])
