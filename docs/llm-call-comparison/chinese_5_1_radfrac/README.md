# CHN51 main-control LLM call comparison

These English-only exports repeat the complete input structure and output inside every call record so the difference in call count and token usage is directly inspectable.

| Method | Calls | Input tokens | Output tokens | Total tokens | Provider cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| Script Agent | 2 | 269,475 | 26,976 | **296,451** | $1.536879 |
| ReAct | 10 | 1,309,384 | 10,602 | **1,319,986** | $6.864980 |

ReAct used **4.45×** as many main-control tokens. Its full task/context block is repeated inside all ten records, together with the evolving memory and observation context.

## Files

- [`script_agent_main_control_calls.raw.jsonl`](script_agent_main_control_calls.raw.jsonl) — two code-generation calls.
- [`react_main_control_calls.raw.jsonl`](react_main_control_calls.raw.jsonl) — ten sequential action-selection calls.

Raw download links:

- [Script Agent calls](https://raw.githubusercontent.com/zhouxiaochi/ASPIRE-agent/main/docs/llm-call-comparison/chinese_5_1_radfrac/script_agent_main_control_calls.raw.jsonl)
- [ReAct calls](https://raw.githubusercontent.com/zhouxiaochi/ASPIRE-agent/main/docs/llm-call-comparison/chinese_5_1_radfrac/react_main_control_calls.raw.jsonl)

## Export policy and provenance

The original benchmark task and some injected context were written in Chinese. Each contiguous CJK passage is replaced by the explicit marker `[NON-ENGLISH REDACTED]`; no machine translation is presented as original model input. All message boundaries, English content, repeated context structure, raw English model output, and exact provider token/cost telemetry are retained.

Script Agent's initial input and both raw outputs were persisted exactly before the English-only replacement. The second Script input combines the persisted base messages with deterministic static-contract feedback.

ReAct persisted exact provider telemetry and raw outputs, but not literal per-step input message bodies. Its inputs are deterministically reconstructed from persisted task/context artifacts, memory update rules, prompt reducer, and prior observations. Every ReAct record states this provenance. Local filesystem roots and run/session identifiers are redacted.
