from __future__ import annotations
import argparse
from pathlib import Path
from .agents import OpenAIAdapter, TaskAgent, ThesisAgent, read_runtime_input

def _run(kind: str) -> int:
    parser = argparse.ArgumentParser(prog=f"{kind}-agent")
    parser.add_argument("command", nargs="?", choices=("generate", "run"), default="generate")
    source = parser.add_mutually_exclusive_group(required=True); source.add_argument("--text"); source.add_argument("--input")
    parser.add_argument("--output", required=True); parser.add_argument("--model"); parser.add_argument("--base-url"); parser.add_argument("--execute", action="store_true"); parser.add_argument("--max-repairs", type=int, default=2)
    args = parser.parse_args(); runtime_input = read_runtime_input(text=args.text, input_path=args.input); adapter = OpenAIAdapter(args.model, args.base_url) if args.model else None; output = Path(args.output)
    agent = TaskAgent(adapter) if kind == "task" else ThesisAgent(adapter)
    if args.command == "generate": files = agent.generate(runtime_input, output); [print(path) for path in files]; return 0
    result = agent.run(runtime_input, output, execute=args.execute, max_repairs=args.max_repairs)
    ok = result.ok if kind == "task" else all(item.ok for item in result.values()); print(result); return 0 if ok else 1

def task_main() -> int: return _run("task")
def thesis_main() -> int: return _run("thesis")
