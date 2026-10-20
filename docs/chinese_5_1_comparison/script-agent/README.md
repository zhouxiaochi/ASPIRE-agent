# Script Agent — CHN51

## Token usage

**2 main-control calls · 296,451 total tokens · $1.536879**

| Call | Operation | Input | Output | Total | Cost |
| ---: | --- | ---: | ---: | ---: | ---: |
| [1](calls/call-01.md) | `initial_codegen` | 134,570 | 13,482 | **148,052** | $1.060030 |
| [2](calls/call-02.md) | `static_feedback_retry` | 134,905 | 13,494 | **148,399** | $0.476849 |

[Download raw LLM calls](../raw/script_agent_main_control_calls.raw.jsonl)

## Result

- Full generation iterations: **1**
- Aspen HTTP calls: **251**
- Aspen result: **converged**, `PER_ERROR = 0`
- Final `PRODUCT` cyclohexane mole fraction: **0.99907**
- Final validation: **PASS**

## Generated code

- [`iteration_0_initial.py`](iteration_0_initial.py): rejected before execution because the liquid-recycle edge appeared twice in the static edge plan.
- [`iteration_0_static_revision.py`](iteration_0_static_revision.py): passed static checks and was executed against Aspen.

These are two code versions from the same generation iteration, not two Aspen execution iterations.

## Execution artifacts

- [`execution.jsonl`](execution.jsonl): ordered generation, audit, execution, readback, and validation events.
- [`metrics.json`](metrics.json): aggregate usage, timing, inventory, and result metrics.

[← Back to comparison](../README.md)
