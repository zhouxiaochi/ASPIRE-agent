from __future__ import annotations
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from .audit import AuditAgent
from .chemical_reasoning import ChemicalReasoningAgent
from .diagnostics import Diagnostic, from_audit
from .execution import Executor, SubprocessExecutor
from .llm import LLMAdapter, load_resource
from .models import ChemicalReasoningInput, RepairFocus, StagePlan, TaskPlan
from .planner import PlannerAgent
from .repair import RepairDirector
from .schema import FileEdit, check_python, parse_edit_bundle
from ..skills import load_skill

@dataclass(frozen=True)
class RuntimeInput:
    text: str
    manifest: dict[str, Any]

def read_runtime_input(*, text: str | None = None, input_path: str | None = None) -> RuntimeInput:
    if bool(text) == bool(input_path): raise ValueError("Provide exactly one of text or input_path")
    raw = text if text is not None else Path(str(input_path)).read_text(encoding="utf-8")
    manifest = json.loads(raw) if input_path and Path(input_path).suffix.lower() == ".json" else {"request": raw}
    return RuntimeInput(str(manifest.get("request", "")), manifest)

def save_state(output: Path, name: str, payload: dict[str, Any]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / name).write_text(json.dumps(payload, indent=2), encoding="utf-8")

def write_edits(output: Path, edits: tuple[FileEdit, ...], protected: set[Path] | None = None) -> list[Path]:
    written = []; output.mkdir(parents=True, exist_ok=True); protected = protected or set()
    for edit in edits:
        check_python(edit); destination = output / edit.path
        if destination.resolve() in protected: continue
        destination.parent.mkdir(parents=True, exist_ok=True); destination.write_text(edit.content, encoding="utf-8"); written.append(destination)
    return written

class _Harness:
    prompt = ""
    def __init__(self, adapter: LLMAdapter | None = None, executor: Executor | None = None, *, planner: PlannerAgent | None = None, auditor: AuditAgent | None = None, chemistry: ChemicalReasoningAgent | None = None, repair: RepairDirector | None = None):
        self.adapter = adapter; self.executor = executor or SubprocessExecutor(); self.planner = planner or PlannerAgent(); self.auditor = auditor or AuditAgent(); self.chemistry = chemistry or ChemicalReasoningAgent(); self.repair = repair or RepairDirector()
    def _generate(self, request: RuntimeInput, output: Path, plan: TaskPlan, focus: RepairFocus | None = None, protected: set[Path] | None = None, audit: Any = None) -> list[Path]:
        skill_context = {name: load_skill(name) for name in plan.skills}
        context = {"request": request.text, "manifest": request.manifest, "plan": plan.as_dict(), "skills": skill_context, "audit_report": audit.as_dict() if audit else None, "repair_focus": focus.as_dict() if focus else None}
        if self.adapter: edits = parse_edit_bundle(self.adapter.complete(load_resource(self.prompt), json.dumps(context, indent=2))).files
        else:
            name = plan.stages[0].entry
            edits = (FileEdit(name, load_resource("runtime_template.py")), FileEdit("PROMPT.txt", load_resource(self.prompt) + "\n\n" + json.dumps(context, indent=2)))
        return write_edits(output, edits, protected)
    def _execution_command(self, request: RuntimeInput, stage: StagePlan) -> tuple[str, ...]:
        slug = re.sub(r"[^a-z0-9]+", "-", stage.name.casefold()).strip("-") or "stage"
        digest = hashlib.sha256(f"{request.text}\n{stage.name}".encode()).hexdigest()[:12]
        task_key = f"asipre-{slug[:24]}-{digest}"
        return ("python", stage.entry, "--task-key", task_key, "--evidence-name", f"evidence/{slug}", "--checkpoint", f"{slug}.bkp")
    def _audit_attempt(self, request: RuntimeInput, output: Path, stage: StagePlan, paths: list[Path], attempt: int, execute: bool, accepted: tuple[str, ...]) -> tuple[Diagnostic, RepairFocus | None, Any, bool]:
        report = self.auditor.audit_source(paths); receipt = None
        if report.ok and execute:
            if self.adapter is None:
                report = type(report)(False, "runtime-audit", "Deterministic output is scaffold-only and cannot execute")
            else:
                before = self.auditor.receipt_snapshot(output)
                result = self.executor.run(self._execution_command(request, stage), output)
                report = self.auditor.audit_runtime(result, output, before)
                receipt = self.auditor.fresh_receipt(output, before)
                if receipt is not None: save_state(output, f"runtime-receipt-{stage.name}-attempt-{attempt}.json", receipt)
        save_state(output, f"audit-{stage.name}-attempt-{attempt}.json", report.as_dict())
        diagnosis = self.chemistry.diagnose(ChemicalReasoningInput(request.text, report, stage.name))
        if diagnosis: save_state(output, f"chemical-reasoning-{stage.name}-attempt-{attempt}.json", diagnosis.as_dict())
        focus = None if report.ok else self.repair.select(report, stage.name, diagnosis, accepted)
        if focus: save_state(output, f"repair-focus-{stage.name}-attempt-{attempt}.json", focus.as_dict())
        return from_audit(report), focus, report, receipt is not None

class TaskAgent(_Harness):
    prompt = "task_agent.md"
    def generate(self, request: RuntimeInput, output: Path, *, feedback: str | None = None) -> list[Path]:
        plan = self.planner.plan(request.text, request.manifest); save_state(output, "plan.json", plan.as_dict())
        focus = RepairFocus("LEGACY_FEEDBACK", feedback, "task") if feedback else None
        paths = self._generate(request, output, plan, focus)
        if self.adapter is None: save_state(output, "mode.json", {"mode": "scaffold-only", "executable": False})
        return paths
    def run(self, request: RuntimeInput, output: Path, *, execute: bool = False, max_repairs: int = 2) -> Diagnostic:
        plan = self.planner.plan(request.text, request.manifest); save_state(output, "plan.json", plan.as_dict())
        if not plan.supported:
            diagnostic = Diagnostic(False, "plan", "; ".join(plan.scope_issues)); save_state(output, "agent-summary.json", diagnostic.as_dict()); save_state(output, "run-summary.json", diagnostic.as_dict()); return diagnostic
        focus = None; audit = None; canonical_receipt = False
        for attempt in range(max_repairs + 1):
            paths = self._generate(request, output, plan, focus, audit=audit)
            if self.adapter is None: save_state(output, "mode.json", {"mode": "scaffold-only", "executable": False})
            diagnostic, focus, audit, fresh_receipt = self._audit_attempt(request, output, plan.stages[0], paths, attempt, execute, ())
            canonical_receipt = canonical_receipt or fresh_receipt
            if diagnostic.ok or attempt == max_repairs or self.adapter is None: break
        outcome = {"attempt": attempt, **diagnostic.as_dict()}; save_state(output, "agent-summary.json", outcome)
        if not canonical_receipt: save_state(output, "run-summary.json", outcome)
        return diagnostic

class ThesisAgent(_Harness):
    prompt = "thesis_agent.md"
    def plan(self, request: RuntimeInput) -> list[dict[str, Any]]: return [stage.as_dict() for stage in self.planner.plan(request.text, request.manifest, thesis=True).stages]
    def generate(self, request: RuntimeInput, output: Path, feedback: str | None = None) -> list[Path]:
        plan = self.planner.plan(request.text, request.manifest, thesis=True); save_state(output, "plan.json", plan.as_dict())
        focus = RepairFocus("LEGACY_FEEDBACK", feedback, plan.stages[0].name) if feedback else None
        return self._generate(request, output, plan, focus)
    def run(self, request: RuntimeInput, output: Path, *, execute: bool = False, max_repairs: int = 2) -> dict[str, Diagnostic]:
        plan = self.planner.plan(request.text, request.manifest, thesis=True); save_state(output, "plan.json", plan.as_dict()); states = {}; protected: set[Path] = set()
        if not plan.supported:
            states = {stage.name: Diagnostic(False, "plan", "; ".join(plan.scope_issues)) for stage in plan.stages}
            outcome = {name: item.as_dict() for name, item in states.items()}; save_state(output, "agent-summary.json", outcome); save_state(output, "run-summary.json", outcome); return states
        canonical_receipt = False
        for stage in plan.stages:
            failed = [name for name in stage.dependencies if name not in states or not states[name].ok]
            if failed: states[stage.name] = Diagnostic(False, "dependency", f"Failed prerequisite: {', '.join(failed)}"); break
            focus = None; audit = None
            for attempt in range(max_repairs + 1):
                paths = self._generate(request, output, plan, focus, protected, audit); diagnostic, focus, audit, fresh_receipt = self._audit_attempt(request, output, stage, paths, attempt, execute, tuple(states))
                canonical_receipt = canonical_receipt or fresh_receipt
                if diagnostic.ok or attempt == max_repairs or self.adapter is None: break
            states[stage.name] = diagnostic; save_state(output, f"stage-{stage.name}-attempt-{attempt}.json", diagnostic.as_dict()); save_state(output, f"stage-{stage.name}.json", diagnostic.as_dict())
            if not diagnostic.ok: break
            protected.add((output / stage.entry).resolve())
        outcome = {name: item.as_dict() for name, item in states.items()}; save_state(output, "agent-summary.json", outcome)
        if not canonical_receipt: save_state(output, "run-summary.json", outcome)
        return states
