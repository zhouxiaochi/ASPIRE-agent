from __future__ import annotations
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Sequence

@dataclass(frozen=True)
class ExecutionResult:
    command: tuple[str, ...]; returncode: int; stdout: str; stderr: str
    @property
    def ok(self) -> bool: return self.returncode == 0

class Executor(Protocol):
    def run(self, command: Sequence[str], cwd: Path) -> ExecutionResult: ...

class SubprocessExecutor:
    def run(self, command: Sequence[str], cwd: Path) -> ExecutionResult:
        result = subprocess.run(list(command), cwd=cwd, text=True, capture_output=True, check=False)
        return ExecutionResult(tuple(command), result.returncode, result.stdout, result.stderr)
