from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

@dataclass(frozen=True)
class StagePlan:
    name: str
    entry: str
    dependencies: tuple[str, ...] = ()
    skills: tuple[str, ...] = ()
    def as_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass(frozen=True)
class TaskPlan:
    request: str
    stages: tuple[StagePlan, ...]
    skills: tuple[str, ...]
    supported: bool = True
    scope_issues: tuple[str, ...] = ()
    def as_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass(frozen=True)
class AuditIssue:
    code: str
    message: str
    category: str
    physical: bool = False
    def as_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass(frozen=True)
class AuditReport:
    ok: bool
    phase: str
    summary: str
    issues: tuple[AuditIssue, ...] = ()
    receipt: str = "none"
    stdout: str = ""
    stderr: str = ""
    def as_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass(frozen=True)
class ChemicalReasoningInput:
    request: str
    audit: AuditReport
    stage: str
    def as_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass(frozen=True)
class ChemicalDiagnosis:
    category: str
    finding: str
    action: str
    confidence: str = "deterministic"
    def as_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass(frozen=True)
class RepairFocus:
    code: str
    instruction: str
    stage: str
    preserve: tuple[str, ...] = ()
    def as_dict(self) -> dict[str, Any]: return asdict(self)
