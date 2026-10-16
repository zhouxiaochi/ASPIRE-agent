import json
from pathlib import Path

from asipre_agent.agents import ExecutionResult, StaticAdapter, TaskAgent, ThesisAgent, read_runtime_input


def script(text):
    return f"---FILE: generated_task.py---\n{text}\n"


class QueueLLM:
    def __init__(self, responses): self.responses = list(responses); self.calls = 0; self.users = []
    def complete(self, system, user): self.calls += 1; self.users.append(user); return self.responses.pop(0)


class QueueExecutor:
    def __init__(self, results): self.results = list(results); self.calls = 0
    def run(self, command, cwd): self.calls += 1; return self.results.pop(0)


def canonical_receipt():
    return {
        "ok": True,
        "preflight": {"complete": True, "completion": {"input_complete": True}, "next_status": {"required_input_complete": True}},
        "run": {"success": True},
        "run_source": "engine_run",
        "evidence": {"rep": {"success": True}, "apw": {"success": True}},
    }


class ReceiptExecutor:
    def __init__(self, payload=None): self.payload = payload or canonical_receipt(); self.commands = []
    def run(self, command, cwd):
        self.commands.append(tuple(command))
        (cwd / "run-summary.json").write_text(json.dumps(self.payload), encoding="utf-8")
        return ExecutionResult(tuple(command), 0, "", "")


def test_task_iterative_execute_repair(tmp_path):
    llm = QueueLLM([script("print('first')"), script("print('fixed')")]); executor = QueueExecutor([ExecutionResult(("python",), 1, "", "boom"), ExecutionResult(("python",), 0, "ok", "")])
    diagnostic = TaskAgent(llm, executor).run(read_runtime_input(text="template request"), tmp_path, execute=True, max_repairs=1)
    assert diagnostic.ok and llm.calls == 2 and executor.calls == 2
    assert (tmp_path / "agent-summary.json").exists()


def test_no_model_is_explicit_scaffold_only(tmp_path):
    diagnostic = TaskAgent().run(read_runtime_input(text="template request"), tmp_path, execute=True)
    assert not diagnostic.ok and "scaffold-only" in diagnostic.summary and (tmp_path / "mode.json").exists()


def test_thesis_staged_execution_and_repair_state(tmp_path):
    manifest = tmp_path / "manifest.json"; manifest.write_text('{"request":"template workspace","stages":[{"name":"build","entry":"workflow.py"}]}', encoding="utf-8")
    llm = QueueLLM(["---FILE: workflow.py---\nprint('one')", "---FILE: workflow.py---\nprint('two')"]); executor = QueueExecutor([ExecutionResult(("python",), 1, "", "bad"), ExecutionResult(("python",), 0, "ok", "")])
    states = ThesisAgent(llm, executor).run(read_runtime_input(input_path=str(manifest)), tmp_path / "out", execute=True, max_repairs=1)
    assert states["build"].ok and (tmp_path / "out" / "plan.json").exists() and (tmp_path / "out" / "stage-build.json").exists()


def test_repair_prompt_contains_plan_audit_and_focus(tmp_path):
    llm = QueueLLM([script("print('first')"), script("print('fixed')")]); executor = QueueExecutor([ExecutionResult(("python",), 1, "", "boom"), ExecutionResult(("python",), 0, "ok", "")])
    TaskAgent(llm, executor).run(read_runtime_input(text="MIXER task"), tmp_path, execute=True, max_repairs=1)
    assert (tmp_path / "audit-task-attempt-0.json").exists() and (tmp_path / "repair-focus-task-attempt-0.json").exists()


def test_thesis_stops_after_failed_prerequisite(tmp_path):
    manifest = tmp_path / "manifest-deps.json"; manifest.write_text('{"request":"workspace","stages":[{"name":"build","entry":"build.py"},{"name":"run","entry":"run.py","dependencies":["build"]}]}', encoding="utf-8")
    states = ThesisAgent(QueueLLM(["---FILE: build.py---\nprint(1)"]), QueueExecutor([ExecutionResult(("python",), 4, "", "bad")])).run(read_runtime_input(input_path=str(manifest)), tmp_path / "deps", execute=True, max_repairs=0)
    assert list(states) == ["build"] and not states["build"].ok and not (tmp_path / "deps" / "run.py").exists()


def test_harness_passes_stable_runtime_arguments(tmp_path):
    request = read_runtime_input(text="MIXER task"); executor = ReceiptExecutor()
    assert TaskAgent(QueueLLM([script("print('ok')")]), executor).run(request, tmp_path, execute=True, max_repairs=0).ok
    command = executor.commands[0]
    assert command[0:2] == ("python", "generated_task.py") and command[2] == "--task-key" and command[3].startswith("asipre-task-")
    assert command[4:] == ("--evidence-name", "evidence/task", "--checkpoint", "task.bkp")


def test_task_preserves_canonical_runtime_receipt(tmp_path):
    receipt = canonical_receipt(); agent = TaskAgent(QueueLLM([script("print('ok')")]), ReceiptExecutor(receipt))
    assert agent.run(read_runtime_input(text="MIXER task"), tmp_path, execute=True, max_repairs=0).ok
    assert json.loads((tmp_path / "run-summary.json").read_text(encoding="utf-8")) == receipt
    assert json.loads((tmp_path / "runtime-receipt-task-attempt-0.json").read_text(encoding="utf-8")) == receipt
    assert (tmp_path / "agent-summary.json").exists()


def test_thesis_copies_fresh_stage_runtime_receipt(tmp_path):
    manifest = tmp_path / "thesis.json"; manifest.write_text('{"request":"MIXER workspace","stages":[{"name":"build","entry":"workflow.py"}]}', encoding="utf-8")
    out = tmp_path / "thesis-out"; receipt = canonical_receipt()
    states = ThesisAgent(QueueLLM(["---FILE: workflow.py---\nprint('ok')"]), ReceiptExecutor(receipt)).run(read_runtime_input(input_path=str(manifest)), out, execute=True, max_repairs=0)
    assert states["build"].ok and json.loads((out / "runtime-receipt-build-attempt-0.json").read_text(encoding="utf-8")) == receipt
    assert json.loads((out / "run-summary.json").read_text(encoding="utf-8")) == receipt


def test_stale_runtime_receipt_is_not_audited_or_copied(tmp_path):
    stale = canonical_receipt(); (tmp_path / "run-summary.json").write_text(json.dumps(stale), encoding="utf-8")
    agent = TaskAgent(QueueLLM([script("print('ok')")]), QueueExecutor([ExecutionResult(("python",), 0, "run-summary.json", "")]))
    assert agent.run(read_runtime_input(text="MIXER task"), tmp_path, execute=True, max_repairs=0).ok
    assert not (tmp_path / "runtime-receipt-task-attempt-0.json").exists()
    assert json.loads((tmp_path / "run-summary.json").read_text(encoding="utf-8"))["phase"] == "runtime-audit"


def test_generation_context_contains_only_selected_skills(tmp_path):
    llm = QueueLLM([script("print('ok')")]); TaskAgent(llm).generate(read_runtime_input(text="Build a MIXER"), tmp_path)
    context = json.loads(llm.users[0]); assert set(context["skills"]) == {"common-components", "mixer"}
    assert "ENERGY_BAL" in context["skills"]["mixer"] and "SPEC_OPT" not in context["skills"]["mixer"]
