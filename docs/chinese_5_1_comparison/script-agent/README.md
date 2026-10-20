# Script Agent — CHN51

## Full-pipeline LLM usage

**5 recorded LLM calls · 405,531 total tokens · $2.405207**

| Scope | Calls | Tokens | Cost |
| --- | ---: | ---: | ---: |
| Program generation and static revision | 2 | 296,451 | $1.536879 |
| REP readback | 1 | 25,326 | $0.325338 |
| Gate validation | 1 | 72,921 | $0.416700 |
| Final report | 1 | 10,833 | $0.126290 |
| **Total** | **5** | **405,531** | **$2.405207** |

[Full-pipeline machine-readable ledger](pipeline_llm_usage.json)

## Main-control calls

| Call | Operation | Input | Output | Total | Cost |
| ---: | --- | ---: | ---: | ---: | ---: |
| [1](calls/call-01.md) | `initial_codegen` | 134,570 | 13,482 | **148,052** | $1.060030 |
| [2](calls/call-02.md) | `static_feedback_retry` | 134,905 | 13,494 | **148,399** | $0.476849 |

[Raw control-call JSONL](../raw/script_agent_main_control_calls.raw.jsonl)

## Result

- Full generation iterations: **1**
- Aspen HTTP calls: **251**
- Aspen result: **converged**, `PER_ERROR = 0`
- Final `PRODUCT` cyclohexane mole fraction: **0.99907**
- Final validation: **PASS**

## Generated code

- [`iteration_0_initial.py`](iteration_0_initial.py): rejected before execution because the liquid-recycle edge appeared twice in the static edge plan.
- [`iteration_0_static_revision.py`](iteration_0_static_revision.py): passed the pre-execution source-contract check and Python checks, then executed successfully against Aspen.

The correction was one **pre-execution static revision**, not a post-run Audit Agent repair iteration. These are two code versions from the same generation iteration, not two Aspen execution iterations.

## Execution artifacts

- [`execution.jsonl`](execution.jsonl): ordered generation, pre-execution audit, execution, readback, and validation events.
- [`metrics.json`](metrics.json): aggregate usage, timing, inventory, and result metrics.

[← Back to comparison](../README.md)
