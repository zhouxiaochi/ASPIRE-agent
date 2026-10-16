import json
from pathlib import Path
from asipre_agent.agents import AuditAgent, ChemicalReasoningAgent, ExecutionResult, PlannerAgent, RepairDirector
from asipre_agent.agents.models import AuditIssue, AuditReport, ChemicalReasoningInput

def test_planner_serializes_and_preserves_dependencies():
    manifest = {"stages": [{"name": "build", "entry": "build.py"}, {"name": "run", "entry": "run.py", "dependencies": ["build"]}]}
    plan = PlannerAgent().plan("Create a MIXER and HEATER", manifest, thesis=True)
    assert plan.supported and plan.skills == ("common-components", "mixer", "heater")
    assert plan.stages[1].dependencies == ("build",)
    json.dumps(plan.as_dict())

def test_planner_rejects_obvious_out_of_scope_request():
    words = ["react" + "or", "rad" + "frac", "sep" + "2", "heat" + "x", "tur" + "bine", "ana" + "lysis"]
    for word in words:
        plan = PlannerAgent().plan(f"Create or configure {word}")
        assert not plan.supported and plan.scope_issues

def test_audit_hard_process_gate_and_process_only(tmp_path):
    agent = AuditAgent()
    failed = agent.audit_runtime(ExecutionResult(("python",), 2, "", "bad"), tmp_path)
    passed = agent.audit_runtime(ExecutionResult(("python",), 0, "ok", ""), tmp_path)
    assert not failed.ok and failed.issues[0].code == "PROCESS_EXIT"
    assert passed.ok and passed.receipt == "process-only"

def test_audit_requires_receipt_trust(tmp_path):
    (tmp_path / "summary.json").write_text(json.dumps({"ok": True, "trusted_run": False, "preflight": {"ok": True}, "evidence": True}), encoding="utf-8")
    report = AuditAgent().audit_runtime(ExecutionResult(("python",), 0, "", ""), tmp_path)
    assert not report.ok and report.issues[0].physical

def test_audit_accepts_complete_normalized_receipt(tmp_path):
    payload = {"ok": True, "trusted_run": True, "preflight": {"ok": True}, "evidence": {"ok": True}}
    (tmp_path / "summary.json").write_text(json.dumps(payload), encoding="utf-8")
    assert AuditAgent().audit_runtime(ExecutionResult(("python",), 0, "", ""), tmp_path).ok

def test_chemistry_is_selective_and_repair_is_bounded():
    agent = ChemicalReasoningAgent()
    syntax = AuditReport(False, "source-audit", "parse", (AuditIssue("PARSE", "parse", "syntax"),))
    physical = AuditReport(False, "runtime-audit", "pressure", (AuditIssue("P", "MIXER pressure evidence", "physical", True),))
    assert agent.diagnose(ChemicalReasoningInput("MIXER", syntax, "task")) is None
    diagnosis = agent.diagnose(ChemicalReasoningInput("MIXER", physical, "task"))
    focus = RepairDirector().select(physical, "task", diagnosis)
    assert diagnosis.category == "mixer-pressure-energy" and focus.code == "P"

def runtime_receipt(*, source="engine_run"):
    next_status = {"required_input_complete": True}
    run = {"success": True, "native_run_id": "run-1"}
    if source == "next_gate_short_circuit":
        next_status = {"success": True, "guardrail_reason": "non_gui_short_circuit_engine_run_success", "diagnostic_kind": "required_input_complete", "engine_run": run}
    return {
        "ok": True,
        "preflight": {"complete": True, "completion": {"input_complete": True}, "next_status": next_status},
        "run": run,
        "run_source": source,
        "evidence": {"rep": {"success": True, "rep_path": "case.rep"}, "apw": {"status": "success", "result": {"success": True, "apw_path": "case.apw"}}},
    }

def test_audit_accepts_runtime_template_receipt(tmp_path):
    (tmp_path / "run-summary.json").write_text(json.dumps(runtime_receipt()), encoding="utf-8")
    report = AuditAgent().audit_runtime(ExecutionResult(("python",), 0, "", ""), tmp_path)
    assert report.ok and report.receipt == "aspen-summary"

def test_audit_accepts_proven_next_gate_short_circuit(tmp_path):
    (tmp_path / "run-summary.json").write_text(json.dumps(runtime_receipt(source="next_gate_short_circuit")), encoding="utf-8")
    assert AuditAgent().audit_runtime(ExecutionResult(("python",), 0, "", ""), tmp_path).ok

def test_audit_rejects_each_canonical_receipt_gate(tmp_path):
    cases = []
    missing_completion = runtime_receipt(); missing_completion["preflight"]["completion"] = {"success": True}; cases.append((missing_completion, "COMPLETION_NOT_EXPLICIT"))
    failed_run = runtime_receipt(); failed_run["run"] = {"success": False}; cases.append((failed_run, "RUN_NOT_SUCCESSFUL"))
    bad_source = runtime_receipt(); bad_source["run_source"] = "unknown"; cases.append((bad_source, "RUN_SOURCE_INVALID"))
    missing_rep = runtime_receipt(); missing_rep["evidence"].pop("rep"); cases.append((missing_rep, "REP_EXPORT_FAILED"))
    failed_apw = runtime_receipt(); failed_apw["evidence"]["apw"] = {"success": False}; cases.append((failed_apw, "APW_EXPORT_FAILED"))
    unproven_short = runtime_receipt(source="next_gate_short_circuit"); unproven_short["preflight"]["next_status"] = {"required_input_complete": True}; cases.append((unproven_short, "SHORT_CIRCUIT_NOT_PROVEN"))
    for index, (payload, code) in enumerate(cases):
        folder = tmp_path / str(index); folder.mkdir(); (folder / "run-summary.json").write_text(json.dumps(payload), encoding="utf-8")
        report = AuditAgent().audit_runtime(ExecutionResult(("python",), 0, "", ""), folder)
        assert not report.ok and code in {issue.code for issue in report.issues}
