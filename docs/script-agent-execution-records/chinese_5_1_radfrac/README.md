# Sanitized Script Agent Aspen execution record: `chinese_5_1_radfrac`

This directory contains a sanitized execution record and the two generated code versions from one successful Script-based ASPIRE research run.

## Run result

- Full generation iterations: **1**
- Code-generation calls: **2** â€” one initial generation and one pre-execution static revision
- Total recorded LLM calls in the execution-and-evidence pipeline: **5**
- Aspen HTTP calls: **251**
- Aspen result: **converged**, `PER_ERROR = 0`
- Final readback: `PRODUCT` mole fraction of `CYCLOHEX` = **0.99907**
- Final evidence validation: **PASS**

## Code versions

- [`iteration_0_initial.py`](iteration_0_initial.py): the first generated candidate. A deterministic source audit rejected it because the same liquid-recycle stream appeared twice in the static physical-edge plan. This version was never executed and made no Aspen-side changes.
- [`iteration_0_static_revision.py`](iteration_0_static_revision.py): the revised program. It removed the duplicate edge, passed source and Python checks, and was the only version executed against Aspen.

These are two code versions from the same full generation iteration, not two independent Aspen execution iterations.

The code depends on experimental internal runtime and helper modules that are not distributed by this public repository. It is published for research auditability, not as a directly runnable example of the packaged public API.

## LLM call record

- [`complete raw main-control LLM calls`](../../llm-call-comparison/chinese_5_1_radfrac/script_agent_main_control_calls.raw.jsonl): every call contains its complete input structure, raw output, and exact provider telemetry. **296,451 total tokens.**

## Other files

- [`execution.jsonl`](execution.jsonl): sanitized ordered events covering generation, pre-execution audit, deterministic Aspen execution, readback, and validation.
- [`metrics.json`](metrics.json): aggregate token, cost, timing, model-inventory, and result metrics.
