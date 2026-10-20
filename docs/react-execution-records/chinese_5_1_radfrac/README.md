# Sanitized ReAct Aspen operation trace: `chinese_5_1_radfrac`

This directory contains the ordered Aspen operation trace from one successful ReAct-controlled benchmark run. It is intended to show the actual Aspen calls made by the agent, not a reconstructed example.

## Run result

- Aspen HTTP calls: **325**
- Successful HTTP responses: **325/325**
- ReAct decision steps: **10**
- Aspen result: **converged**, `PER_ERROR = 0`
- Final readback: `PRODUCT` mole fraction of `CYCLOHEX` = **0.999122737**

## LLM call record

- [`complete English-only main-control LLM calls`](../../llm-call-comparison/chinese_5_1_radfrac/react_main_control_calls.english.jsonl): every call contains its complete input structure, raw output, and exact provider telemetry. **1,319,986 total tokens.**

## Files

- [`aspen_operations.jsonl`](aspen_operations.jsonl): all 325 Aspen calls in execution order.
- [`metrics.json`](metrics.json): aggregate execution and result metrics.

Each JSONL record contains the call sequence number, elapsed wall-clock position relative to session start, operation duration, Aspen operation, parameters, HTTP status, and sanitized operation result. Aspen block and stream names, ports, variable paths, configuration values, completion checks, run status, and result readbacks are retained.

Useful ranges include:

- 1–35: session start, components, property method, streams, and blocks
- 36–200: topology and detailed process configuration
- 201–275: convergence setup and pre-run completion checks
- 276–279: engine run, `PER_ERROR` readback, and evidence export
- 280–324: product, equipment, and live-port readbacks
- 325: session close

This research trace uses equipment beyond the packaged public `MIXER`/`HEATER` API scope described in the repository README. It documents an experimental execution and does not expand the supported public API.
