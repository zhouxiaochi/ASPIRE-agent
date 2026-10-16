# ASPIRE Agent

ASPIRE Agent is a focused research toolkit for generating, auditing, executing, and repairing Aspen Plus automation for MIXER and HEATER workflows. The Python distribution is `aspire-agent`, the import package is `aspire_agent`, and the command-line programs are `task-agent`, `thesis-agent`, and `aspire-server`. Source code and releases are available at <https://github.com/zhouxiaochi/ASPIRE-agent>.

## Demo

[![ASPIRE Agent demonstration](https://img.youtube.com/vi/6JDFBJ_Mo8Q/maxresdefault.jpg)](https://www.youtube.com/watch?v=6JDFBJ_Mo8Q)

The image opens the demonstration on YouTube.

## Scope

ASPIRE Agent supports:

- Aspen Plus `MIXER` and `HEATER` blocks only;
- material and heat streams;
- material feeds specified by temperature, pressure, and component molar or mass flows; and
- the ten compounds in the packaged registry.

Other process equipment and broader process-study workflows are outside the supported public scope. Unsupported requests are rejected by the planner. The project is a research automation layer, not a general Aspen Plus replacement, and generated code must still be reviewed before use.

## Architecture

A run passes through a bounded agent pipeline:

1. `PlannerAgent` checks scope, selects packaged skills, and produces serializable task or staged thesis plans.
2. `TaskAgent` generates one task workspace; `ThesisAgent` generates an ordered, dependency-aware multi-stage workspace.
3. `AuditAgent` parses generated Python and applies deterministic execution and evidence gates.
4. `ChemicalReasoningAgent` is invoked selectively for physical or configuration failures, not syntax or infrastructure failures.
5. `RepairDirector` chooses one focused repair for each bounded retry.

The typed `AspenClient` talks to the standalone HTTP service. The service owns Aspen Plus COM sessions and exposes the supported session, topology, configuration, completion, run, readback, checkpoint, and evidence operations.

## Supported compounds

| Name | Aspen ID | CAS number |
| --- | --- | --- |
| Water | `WATER` | 7732-18-5 |
| Methanol | `MEOH` | 67-56-1 |
| Ethanol | `ETHANOL` | 64-17-5 |
| Methane | `METHANE` | 74-82-8 |
| Carbon dioxide | `CO2` | 124-38-9 |
| Hydrogen | `HYDROGEN` | 1333-74-0 |
| Nitrogen | `NITROGEN` | 7727-37-9 |
| Ammonia | `AMMONIA` | 7664-41-7 |
| n-Hexane | `N-HEXANE` | 110-54-3 |
| Acetic acid | `ACETIC-ACID` | 64-19-7 |

Names, Aspen IDs, CAS numbers, formulas, and documented aliases resolve through `CompoundRegistry`. Arbitrary compounds are not accepted by the public API.

## Prerequisites

- Windows on the machine running `aspire-server`;
- a licensed Aspen Plus installation with working COM automation;
- Python 3.10 or newer; and
- an OpenAI-compatible chat-completions endpoint for model-backed generation.

The CLI/agent host may run separately from the HTTP service. This repository's standalone server must run on a Windows host where Aspen Plus COM works and must be reachable from the agent host.

## Installation

For development and all public optional features:

```console
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,windows,llm]"
```

A smaller Windows service installation is:

```console
python -m pip install ".[server,windows]"
```

A remote agent host does not need COM support:

```console
python -m pip install ".[http,llm]"
```

## Start the Aspen service

Run this on the Windows/Aspen COM host:

```console
aspire-server --host 127.0.0.1 --port 5000
```

Use an appropriate reachable interface instead of `127.0.0.1` only when the service must accept remote clients, and protect that network exposure. Verify startup with `GET http://127.0.0.1:5000/health`.

## Command-line use

Both agent CLIs accept either inline `--text` or an `--input` file, require `--output`, and default to the `generate` command. Without `--model`, generation intentionally writes a non-executable scaffold and prompt context. Model-backed generation uses the standard `OPENAI_API_KEY` environment variable used by the OpenAI Python client.

Set the key in PowerShell, then generate a task workspace:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
task-agent generate `
  --text "Create a MIXER followed by a HEATER using water and methanol feeds." `
  --output runs/task-demo `
  --model gpt-4.1
```

`--base-url` selects an OpenAI-compatible endpoint supported by the installed OpenAI client:

```console
task-agent generate --input examples/task-manifest.template.json --output runs/task-demo --model your-model --base-url https://example.invalid/v1
```

To generate, audit, and execute against the HTTP service at the generated runtime's default `http://127.0.0.1:5000`:

```console
task-agent run --input examples/task-manifest.template.json --output runs/task-run --model gpt-4.1 --execute --max-repairs 2
```

Omit `--execute` to generate and source-audit without launching the generated workflow. A custom runtime service URL can be supplied when invoking a generated stage directly with its `--server-url` option.

For a staged thesis workspace:

```console
thesis-agent generate --input thesis.json --output runs/thesis-demo --model gpt-4.1
thesis-agent run --input thesis.json --output runs/thesis-run --model gpt-4.1 --execute --max-repairs 2
```

Example `thesis.json`:

```json
{
  "request": "Build and verify a staged MIXER and HEATER workflow using registry compounds.",
  "stages": [
    {"name": "build", "entry": "workflow.py"},
    {"name": "verify", "entry": "verify.py", "dependencies": ["build"]}
  ]
}
```

Stage entry names become generated files. Thesis execution stops after a failed prerequisite and protects accepted earlier stage entry files from later generation.

## Artifacts and evidence

Agent output directories contain generated Python plus machine-readable planning and audit records. Depending on the path taken, these include `plan.json`, per-attempt audit reports, optional chemical diagnoses, repair focuses, `agent-summary.json`, and `run-summary.json`.

A trusted executed run requires explicit flowsheet and Next-gate completion, a successful Aspen engine result, and successful REP and APW exports from that run. Evidence names are server-relative; absolute paths and parent traversal are rejected. Aspen checkpoints and exported files can contain proprietary model information, so review them before sharing.

## Safety and operating constraints

- Generated code is untrusted until reviewed and audited.
- Execution is opt-in through `run --execute`; model-free output is scaffold-only.
- Only the packaged compounds, block types, stream roles, and configuration modes are supported.
- Live block ports are inspected before connections are made.
- Component landing is verified before downstream feed configuration.
- Completion and the Aspen Next gate are checked before an engine run.
- A caller timeout does not cancel Aspen work already running on the service; resolve or close the session before issuing conflicting operations.
- Keep the COM service on a trusted network and apply normal host, credential, and file-access controls.

## Testing and packaging

The test suite uses fake HTTP, subprocess, COM, and Aspen Tree objects; passing it does not claim that a real Aspen simulation has run.

```console
python -m pytest
python -m build
python -m twine check dist/*
```

## Project layout

```text
src/aspire_agent/       Public package, agents, client, COM service, and resources
skills/                 Public MIXER, HEATER, and common-compound guidance
tests/                  Unit and contract tests with test doubles
examples/               Task and thesis manifest templates
docs/architecture.md    Detailed execution and evidence architecture
```

## Citation

If you use ASPIRE Agent in academic work, cite the repository release or commit you used.

```text
Zhou, Xiaochi, and Yunhu Gao. ASPIRE Agent, version or commit, 2026. https://github.com/zhouxiaochi/ASPIRE-agent
```

## License

ASPIRE Agent is licensed under [CC BY-NC 4.0](LICENSE). Academic and noncommercial use is permitted with attribution. Commercial use requires separate permission.

## Aspen Plus notice

Aspen Plus is proprietary software of Aspen Technology, Inc. Aspen, Aspen Plus, AspenTech, and related names and marks are trademarks or registered trademarks of their respective owners. This project is independent, is not affiliated with or endorsed by Aspen Technology, and does not include Aspen Plus or grant any rights to it. Users must obtain and comply with their own Aspen Plus license.
