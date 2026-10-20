# CHN51: Script Agent vs ReAct

## Full-pipeline LLM usage

This is the primary scope used in Supplementary Table S11: all recorded LLM calls in each execution-and-evidence pipeline.

<table>
<tr><th>Method</th><th>All LLM calls</th><th>Input tokens</th><th>Output tokens</th><th>Total tokens</th><th>Provider cost</th></tr>
<tr><td><a href="script-agent/"><strong>Script Agent →</strong></a></td><td>5</td><td>368,522</td><td>37,009</td><td><strong>405,531</strong></td><td>$2.405207</td></tr>
<tr><td><a href="react/"><strong>ReAct →</strong></a></td><td>12</td><td>1,344,458</td><td>14,961</td><td><strong>1,359,419</strong></td><td>$7.093963</td></tr>
</table>

> **Script Agent used 70.2% fewer tokens and had 66.1% lower LLM cost than ReAct.**

- [Script Agent: calls, generated code, execution record, and full-pipeline ledger](script-agent/)
- [ReAct: calls, Aspen operation trace, and full-pipeline ledger](react/)

## Control-layer breakdown

The main control layer is a subset of the full pipeline. Script Agent made two code-generation calls; ReAct made ten action-selection calls.

| Method | Main-control calls | Input tokens | Output tokens | Total tokens | Provider cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| Script Agent | 2 | 269,475 | 26,976 | 296,451 | $1.536879 |
| ReAct | 10 | 1,309,384 | 10,602 | 1,319,986 | $6.864980 |

Script Agent's remaining three calls were REP readback, gate validation, and final reporting. ReAct's remaining two calls were REP readback and gate validation.

## Execution outcome

Both methods completed the Aspen Plus V14 case successfully. Script Agent obtained `PRODUCT` cyclohexane mole fraction ≈ 0.99907; ReAct obtained ≈ 0.99912.

The initial Script Agent candidate contained a duplicated `C4` material-stream connection. A **pre-execution source-contract check** detected it, and one **static revision** corrected the program before the first Aspen execution.

Provider token telemetry is unchanged from the original runs. Chinese source passages in the public call records are faithfully translated into English.

## Raw control-call data

- [Script Agent raw control calls](raw/script_agent_main_control_calls.raw.jsonl)
- [ReAct raw control calls](raw/react_main_control_calls.raw.jsonl)
