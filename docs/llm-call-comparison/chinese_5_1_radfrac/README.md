# CHN51 main-control LLM call comparison

Open the formatted call indexes to inspect each complete input and output in a browser:

<table>
<tr>
<th>Method</th><th>Main-control calls</th><th>Input tokens</th><th>Output tokens</th><th>Total tokens</th><th>Provider cost</th>
</tr>
<tr>
<td><a href="script-agent/"><strong>Script Agent →</strong></a></td><td>2</td><td>269,475</td><td>26,976</td><td><strong>296,451</strong></td><td>$1.536879</td>
</tr>
<tr>
<td><a href="react/"><strong>ReAct →</strong></a></td><td>10</td><td>1,309,384</td><td>10,602</td><td><strong>1,319,986</strong></td><td>$6.864980</td>
</tr>
</table>

> ReAct used **4.45×** as many main-control tokens. Its full task/context structure is repeated inside all ten call records, together with evolving memory and observation context.

## Browse the calls

- [Script Agent: 2 formatted calls](script-agent/)
- [ReAct: 10 formatted calls](react/)

## Raw JSONL downloads

- [Script Agent raw calls](script_agent_main_control_calls.raw.jsonl)
- [ReAct raw calls](react_main_control_calls.raw.jsonl)

## Translation and provenance

The original benchmark task and some injected context were written in Chinese. Those passages are faithfully translated into English in this public export. Code, identifiers, Aspen tokens, units, numbers, message boundaries, repeated context structure, raw English model output, and exact provider token/cost telemetry are retained.

Script Agent's initial input and both raw outputs were persisted exactly before translation. Its second input combines the persisted base messages with deterministic static-contract feedback.

ReAct persisted exact provider telemetry and raw outputs, but not literal per-step input message bodies. Its inputs are deterministically reconstructed from persisted task/context artifacts, memory update rules, prompt reducer, and prior observations, then translated where the source text was Chinese. Every ReAct record states this provenance. Local filesystem roots and run/session identifiers are redacted.
