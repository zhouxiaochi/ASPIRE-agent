# CHN51: Script Agent vs ReAct

## Main result

<table>
<tr><th>Method</th><th>Main-control calls</th><th>Input tokens</th><th>Output tokens</th><th>Total tokens</th><th>Provider cost</th></tr>
<tr><td><a href="script-agent/"><strong>Script Agent →</strong></a></td><td>2</td><td>269,475</td><td>26,976</td><td><strong>296,451</strong></td><td>$1.536879</td></tr>
<tr><td><a href="react/"><strong>ReAct →</strong></a></td><td>10</td><td>1,309,384</td><td>10,602</td><td><strong>1,319,986</strong></td><td>$6.864980</td></tr>
</table>

> **ReAct used 4.45× as many main-control tokens as Script Agent in the same CHN51 benchmark case.**

- [Browse the 2 Script Agent calls, generated code, and execution record](script-agent/)
- [Browse the 10 ReAct calls and Aspen operation trace](react/)

## Why the difference is visible

Script Agent used two large calls to generate and statically revise one executable program. ReAct made ten sequential action-selection calls, repeatedly carrying the large task/context block plus evolving memory and observations.

Both methods completed the Aspen Plus V14 case successfully. Provider token telemetry is unchanged from the original runs. Chinese source passages in the public call records are faithfully translated into English.

## Raw call data

- [Script Agent raw JSONL](raw/script_agent_main_control_calls.raw.jsonl)
- [ReAct raw JSONL](raw/react_main_control_calls.raw.jsonl)
