from __future__ import annotations
import ast
import json
from pathlib import Path
from typing import Any, Iterable, Mapping
from .execution import ExecutionResult
from .models import AuditIssue, AuditReport

_SUMMARY_NAMES = ("run-summary.json", "summary.json")
_RUN_SOURCES = {"engine_run", "next_gate_short_circuit"}

def _success(payload: Any) -> bool:
    if payload is True: return True
    if not isinstance(payload, Mapping): return False
    nested = payload.get("result")
    if payload.get("success") is False or payload.get("ok") is False: return False
    if isinstance(nested, Mapping) and not _success(nested): return False
    return payload.get("success") is True or payload.get("ok") is True or payload.get("status") == "success"

def _complete(payload: Any) -> bool:
    if not isinstance(payload, Mapping) or payload.get("success") is False: return False
    for key in ("complete", "input_complete", "required_input_complete", "workflow_ready_by_fallback", "fallback_ready"):
        if key in payload: return payload[key] is True
    state = str(payload.get("input_state") or "").strip().casefold()
    if state in {"complete", "input_complete", "required_input_complete"}: return True
    kind = str(payload.get("diagnostic_kind") or payload.get("feedback_window_kind") or "").strip().casefold()
    if payload.get("no_completion_issues") is True and kind == "required_input_complete": return True
    engine = payload.get("engine_run")
    return payload.get("guardrail_reason") == "non_gui_short_circuit_engine_run_success" and kind == "required_input_complete" and _success(engine)

class AuditAgent:
    def audit_source(self, paths: Iterable[Path]) -> AuditReport:
        issues = []
        for path in paths:
            if path.suffix != ".py": continue
            try: ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc: issues.append(AuditIssue("PYTHON_PARSE", str(exc), "syntax"))
        return self._report("source-audit", issues, "Python sources parsed")

    def receipt_snapshot(self, cwd: Path) -> dict[str, int]:
        return {name: (cwd / name).stat().st_mtime_ns for name in _SUMMARY_NAMES if (cwd / name).is_file()}

    def fresh_receipt(self, cwd: Path, before: dict[str, int] | None = None) -> dict[str, Any] | None:
        return self._find_summary("", cwd, before)

    def audit_runtime(self, result: ExecutionResult, cwd: Path, before: dict[str, int] | None = None) -> AuditReport:
        if result.returncode != 0:
            issue = AuditIssue("PROCESS_EXIT", f"Process exited with code {result.returncode}", "infrastructure")
            return AuditReport(False, "runtime-audit", issue.message, (issue,), "process", result.stdout, result.stderr)
        summary = self._find_summary(result.stdout, cwd, before)
        if summary is None:
            return AuditReport(True, "runtime-audit", "Process completed without an Aspen receipt", receipt="process-only", stdout=result.stdout, stderr=result.stderr)
        issues = self._summary_issues(summary)
        report = self._report("runtime-audit", issues, "Trusted run receipt accepted", "aspen-summary")
        return AuditReport(report.ok, report.phase, report.summary, report.issues, report.receipt, result.stdout, result.stderr)

    def _find_summary(self, stdout: str, cwd: Path, before: dict[str, int] | None) -> dict | None:
        explicit = [cwd / line.strip() for line in stdout.splitlines() if line.strip().endswith(".json")]
        for path in explicit + [cwd / name for name in _SUMMARY_NAMES]:
            if not path.is_file(): continue
            if before is not None and before.get(path.name) == path.stat().st_mtime_ns: continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, dict) and self._looks_like_receipt(data): return data
            except (OSError, json.JSONDecodeError): continue
        return None

    @staticmethod
    def _looks_like_receipt(data: dict) -> bool:
        return "ok" in data or any(key in data for key in ("trusted_run", "preflight", "run", "evidence"))

    @staticmethod
    def _summary_issues(data: dict) -> list[AuditIssue]:
        issues = []
        if data.get("ok") is not True: issues.append(AuditIssue("SUMMARY_NOT_OK", "Run receipt ok flag is not true", "evidence"))
        if "trusted_run" in data:
            normalized = (("trusted_run", "UNTRUSTED_RUN"), ("preflight", "UNTRUSTED_PREFLIGHT"), ("evidence", "UNTRUSTED_EVIDENCE"))
            for key, code in normalized:
                if not _success(data.get(key)): issues.append(AuditIssue(code, f"Normalized {key} receipt did not pass", "physical", True))
        else:
            AuditAgent._canonical_issues(data, issues)
        return issues

    @staticmethod
    def _canonical_issues(data: dict, issues: list[AuditIssue]) -> None:
        preflight = data.get("preflight")
        if not isinstance(preflight, Mapping):
            issues.append(AuditIssue("MISSING_PREFLIGHT", "Run receipt is missing preflight evidence", "physical", True))
        else:
            if preflight.get("complete") is not True: issues.append(AuditIssue("PREFLIGHT_NOT_COMPLETE", "Preflight complete flag is not true", "physical", True))
            if not _complete(preflight.get("completion")): issues.append(AuditIssue("COMPLETION_NOT_EXPLICIT", "Flowsheet completion is not explicit", "physical", True))
            if not _complete(preflight.get("next_status")): issues.append(AuditIssue("NEXT_NOT_COMPLETE", "Next completion is not explicit", "physical", True))
        source = data.get("run_source")
        run = data.get("run")
        if source not in _RUN_SOURCES: issues.append(AuditIssue("RUN_SOURCE_INVALID", "Run source is not canonical", "evidence"))
        if not _success(run): issues.append(AuditIssue("RUN_NOT_SUCCESSFUL", "Run result is not successful", "physical", True))
        if source == "next_gate_short_circuit" and isinstance(preflight, Mapping):
            next_status = preflight.get("next_status")
            if not isinstance(next_status, Mapping) or next_status.get("guardrail_reason") != "non_gui_short_circuit_engine_run_success":
                issues.append(AuditIssue("SHORT_CIRCUIT_NOT_PROVEN", "Next-gate run source lacks matching gate evidence", "evidence"))
        evidence = data.get("evidence")
        if not isinstance(evidence, Mapping):
            issues.append(AuditIssue("MISSING_EVIDENCE", "Run receipt is missing evidence exports", "physical", True))
        else:
            for key in ("rep", "apw"):
                if not _success(evidence.get(key)): issues.append(AuditIssue(f"{key.upper()}_EXPORT_FAILED", f"{key.upper()} export is not successful", "physical", True))

    @staticmethod
    def _report(phase: str, issues: list[AuditIssue], success: str, receipt: str = "none") -> AuditReport:
        return AuditReport(not issues, phase, success if not issues else issues[0].message, tuple(issues), receipt)
