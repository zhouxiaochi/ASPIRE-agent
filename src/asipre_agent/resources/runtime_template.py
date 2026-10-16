"""Generated workflow runtime contract; task-specific hooks are prompt-only."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from asipre_agent import AspenClient

def build_topology(client: AspenClient, task_key: str) -> None:
    """Generated code replaces this prompt-only hook."""
    raise RuntimeError("Prompt-only scaffold: topology was not generated")

def configure_material_feeds(client: AspenClient, task_key: str) -> None:
    """Generated code configures TP component-flow feeds here."""
    raise RuntimeError("Prompt-only scaffold: material feeds were not generated")

def configure(client: AspenClient, task_key: str) -> None:
    """Generated code replaces this prompt-only hook."""
    raise RuntimeError("Prompt-only scaffold: configuration was not generated")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--task-key", required=True); parser.add_argument("--server-url", default="http://127.0.0.1:5000"); parser.add_argument("--evidence-name", default="evidence/run"); parser.add_argument("--checkpoint", default="generated.bkp"); args = parser.parse_args()
    summary = {"task_key": args.task_key, "ok": False, "phase": "start"}; client = AspenClient(args.server_url)
    try:
        client.health(); client.start(args.task_key); build_topology(client, args.task_key); configure_material_feeds(client, args.task_key); configure(client, args.task_key); summary["phase"] = "preflight"; summary["next_gate_operation"] = "ui_check_next_completion_status"; summary["preflight"] = client.preflight(args.task_key); client.checkpoint(args.task_key, args.checkpoint); summary["phase"] = "run"; summary["run"] = client.run(args.task_key); summary["run_source"] = summary["run"].get("source", "engine_run"); summary["evidence"] = client.export_evidence(args.task_key, args.evidence_name); summary["ok"] = True; return 0
    except Exception as exc: summary["error"] = str(exc); return 1
    finally:
        try: client.close(args.task_key)
        except Exception as exc: summary["close_error"] = str(exc)
        Path("run-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8"); print(json.dumps(summary))

if __name__ == "__main__": sys.exit(main())
