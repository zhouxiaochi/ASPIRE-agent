from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
from .execution import ExecutionResult
from .models import AuditReport

@dataclass(frozen=True)
class Diagnostic:
    ok: bool
    phase: str
    summary: str
    stdout: str = ""
    stderr: str = ""
    def as_dict(self): return asdict(self)

def from_audit(report: AuditReport) -> Diagnostic:
    return Diagnostic(report.ok, report.phase, report.summary, report.stdout, report.stderr)

def from_execution(result: ExecutionResult, phase: str = "execute") -> Diagnostic:
    summary = "Execution succeeded" if result.ok else f"Execution failed with code {result.returncode}"
    return Diagnostic(result.ok, phase, summary, result.stdout, result.stderr)
