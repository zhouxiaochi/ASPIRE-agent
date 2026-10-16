from __future__ import annotations
from .models import AuditReport, ChemicalDiagnosis, RepairFocus

class RepairDirector:
    def select(self, audit: AuditReport, stage: str, diagnosis: ChemicalDiagnosis | None = None, preserve: tuple[str, ...] = ()) -> RepairFocus:
        issue = audit.issues[0] if audit.issues else None
        code = issue.code if issue else "NO_ISSUE"
        instruction = diagnosis.action if diagnosis else (issue.message if issue else "Keep the accepted implementation unchanged.")
        return RepairFocus(code, instruction, stage, preserve)
