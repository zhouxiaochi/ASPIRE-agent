# ReAct call 2 of 10

[← Call 1](call-01.md) · [ReAct call index](README.md) · [Call 3 →](call-03.md) · [Raw JSONL](../react_main_control_calls.raw.jsonl)
## Call metadata

| Field | Value |
| --- | --- |
| Method | `react` |
| Operation | `select_action` |
| Model | `gpt-5.5` |
| Recorded at | `2026-10-18T20:59:10.439` |
| Input provenance | `deterministically_reconstructed_from_persisted_task_context_memory_and_observations` |
| Input tokens | **130,421** |
| Output tokens | **5,208** |
| Total tokens | **135,629** |
| Provider cost | **$0.808345** |
| Recorded prompt characters | 506,538 |
| Reconstructed prompt characters | 508,369 |

## Input messages

<details><summary>Message 1: <code>system</code> · 2,482 characters</summary>

<pre><code>You are a ReAct baseline agent for Aspen Plus through an MCP-like HTTP tool surface.

You are not writing a Python script. You must solve the task by repeatedly choosing one JSON action.
Use the provided skills/context as operational policy. Prefer high-level documented operations when available.

Return exactly one JSON object, no markdown fences:
{
  &quot;thought&quot;: &quot;brief private working note&quot;,
  &quot;action&quot;: &quot;mcp_tool&quot; | &quot;mcp_plan&quot; | &quot;finalize&quot;,
  &quot;operation&quot;: &quot;Aspen operation name when action=mcp_tool&quot;,
  &quot;parameters&quot;: {&quot;name&quot;: &quot;value&quot;},
  &quot;final_summary&quot;: {&quot;case_id&quot;: &quot;...&quot;, &quot;ok&quot;: true, &quot;evidence&quot;: {}, &quot;results&quot;: {}, &quot;self_validation&quot;: {}}
}

Rules:
- Use action=mcp_tool to call one ReAct tool from the catalog.
- Use action=finalize only when you have enough evidence or are blocked.
- Prefer shared-core virtual helpers for streams, completion/export, and property-method setup.
- Prefer block_family-specific virtual helpers when present (Flash2 specs, HEATX ports/targets, heat-stream duty maps, RadFrac topology, condensate streams, readbacks).
- Do not call low-level Aspen tree write tools such as set_variable or set_block_input. Use typed setters and facade helpers so block-specific policy can run.
- Prefer create_block(block_family=..., block_name=...) or typed create_* names (create_flash2, create_radfrac, create_material_stream). Both are valid; create_block matches own-agent safe.create_block.
- For Aspen Next/completion probing, use ui_check_next_completion_status rather than check_next_completion_status.
- Keep final_summary honest. Do not claim convergence, evidence files, or targets unless observations prove them.
- If a tool fails, inspect translated_operations/partial_failures in the observation and repair with a targeted next tool call.
- When a plan stops on error, preserve its successful prefix, repair the failed action, then resume the reported pending_actions instead of rebuilding the whole flowsheet.
- Do not refer to hidden baseline scripts, case metadata notes, or ground truth.

Causal-ablation plan treatment:
- You may use action=mcp_plan with an `actions` JSON array containing as many items as are useful within the provider/context-window response. Each item must contain operation and parameters. Batch as much useful work as possible.
- The runner executes actions in order, stops on the first failure, and returns every observation.
- A plan is one main-model decision but every item is counted as a separate facade action.
</code></pre>

</details>

<details><summary>Message 2: <code>user</code> · 544,615 characters</summary>

<pre><code>CASE_ID: chinese_5_1_radfrac

TASK_TEXT:
# [NON-ENGLISH REDACTED] 5.1

![[NON-ENGLISH REDACTED] 5.1 [NON-ENGLISH REDACTED]](./images/exercise_5_1_flow.png)

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `Aspen Plus` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] `RK-SOAVE`。

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]：

`C6H6([NON-ENGLISH REDACTED]) + 3H2([NON-ENGLISH REDACTED]) -&gt; C6H12([NON-ENGLISH REDACTED])`
[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] `99.8%`，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。

## [NON-ENGLISH REDACTED]

- [NON-ENGLISH REDACTED] `H2IN`：[NON-ENGLISH REDACTED] `50℃`，[NON-ENGLISH REDACTED] `2.5 MPa`，[NON-ENGLISH REDACTED] `330 kmol/h`，[NON-ENGLISH REDACTED] `H2`、`N2`、`CH4` [NON-ENGLISH REDACTED] `0.975`、`0.005` [NON-ENGLISH REDACTED] `0.02`
- [NON-ENGLISH REDACTED] `BZIN`：[NON-ENGLISH REDACTED] `40℃`，[NON-ENGLISH REDACTED] `0.1 MPa`，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `100 kmol/h`
- [NON-ENGLISH REDACTED] `FEED-MIX`（`Heater` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `150℃`，[NON-ENGLISH REDACTED] `2.3 MPa`
- [NON-ENGLISH REDACTED] `REACT`（`Rstoic` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `200℃`，[NON-ENGLISH REDACTED] `0.1 MPa`，[NON-ENGLISH REDACTED] `0.998`
- [NON-ENGLISH REDACTED] `VFLOW`（`FSplit` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `H2RCY` [NON-ENGLISH REDACTED] `92%`
- [NON-ENGLISH REDACTED] `LFLOW`（`FSplit` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `CHRCY` [NON-ENGLISH REDACTED] `30%`
- [NON-ENGLISH REDACTED] `HP-SEP`（`Flash2` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `50℃`，[NON-ENGLISH REDACTED] `0.05 MPa`
- [NON-ENGLISH REDACTED] `COLUMN`（`RadFrac` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `12`，[NON-ENGLISH REDACTED] `1.2`，[NON-ENGLISH REDACTED] `8` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `1.5 MPa`，[NON-ENGLISH REDACTED] `99 kmol/h`，[NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] `FEEDPUMP`（`Pump` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `0.6`，[NON-ENGLISH REDACTED] `0.9`
- [NON-ENGLISH REDACTED] `PIPE`（`Pipe` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `40`，[NON-ENGLISH REDACTED] `1 in`，[NON-ENGLISH REDACTED] `25 m`
- [NON-ENGLISH REDACTED] `PUMP`（`Pump HI`）：[NON-ENGLISH REDACTED] `2.6 MPa`
- [NON-ENGLISH REDACTED] `COMP`（`Compr` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `0.4 MPa`
- [NON-ENGLISH REDACTED] `VALVE`（`Valve` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `2 MPa`，[NON-ENGLISH REDACTED] `V810 equal percent flow` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `1.5 in`

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] `FEEDPUMP`，[NON-ENGLISH REDACTED] `BZIN → FEEDPUMP → BZIN2`，[NON-ENGLISH REDACTED] `PUMP`。

- `FEEDPUMP` [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
- `FEEDPUMP` [NON-ENGLISH REDACTED] `0.6`，[NON-ENGLISH REDACTED] `0.9`；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `FEED-MIX` [NON-ENGLISH REDACTED] `2.3 MPa` [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] `PUMP` [NON-ENGLISH REDACTED] `2.6 MPa`，[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] `m3/h` [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] SI [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `FEEDPUMP` [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] ID [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] 1 | [NON-ENGLISH REDACTED] 2 | [NON-ENGLISH REDACTED] 3 | [NON-ENGLISH REDACTED] 4 |
| --- | --- | --- | --- | --- |
| [NON-ENGLISH REDACTED] / (m3/h) | 20 | 10 | 5 | 3 |
| [NON-ENGLISH REDACTED] | 40 | 250 | 300 | 400 |

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]。


CONTEXT_AND_SKILLS:
### FILE: tasks/test/chn/chapter_05/exercise_5_1.md
Reason: target task statement
```text
# [NON-ENGLISH REDACTED] 5.1

![[NON-ENGLISH REDACTED] 5.1 [NON-ENGLISH REDACTED]](./images/exercise_5_1_flow.png)

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `Aspen Plus` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] `RK-SOAVE`。

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]：

`C6H6([NON-ENGLISH REDACTED]) + 3H2([NON-ENGLISH REDACTED]) -&gt; C6H12([NON-ENGLISH REDACTED])`
[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] `99.8%`，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。

## [NON-ENGLISH REDACTED]

- [NON-ENGLISH REDACTED] `H2IN`：[NON-ENGLISH REDACTED] `50℃`，[NON-ENGLISH REDACTED] `2.5 MPa`，[NON-ENGLISH REDACTED] `330 kmol/h`，[NON-ENGLISH REDACTED] `H2`、`N2`、`CH4` [NON-ENGLISH REDACTED] `0.975`、`0.005` [NON-ENGLISH REDACTED] `0.02`
- [NON-ENGLISH REDACTED] `BZIN`：[NON-ENGLISH REDACTED] `40℃`，[NON-ENGLISH REDACTED] `0.1 MPa`，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `100 kmol/h`
- [NON-ENGLISH REDACTED] `FEED-MIX`（`Heater` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `150℃`，[NON-ENGLISH REDACTED] `2.3 MPa`
- [NON-ENGLISH REDACTED] `REACT`（`Rstoic` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `200℃`，[NON-ENGLISH REDACTED] `0.1 MPa`，[NON-ENGLISH REDACTED] `0.998`
- [NON-ENGLISH REDACTED] `VFLOW`（`FSplit` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `H2RCY` [NON-ENGLISH REDACTED] `92%`
- [NON-ENGLISH REDACTED] `LFLOW`（`FSplit` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `CHRCY` [NON-ENGLISH REDACTED] `30%`
- [NON-ENGLISH REDACTED] `HP-SEP`（`Flash2` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `50℃`，[NON-ENGLISH REDACTED] `0.05 MPa`
- [NON-ENGLISH REDACTED] `COLUMN`（`RadFrac` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `12`，[NON-ENGLISH REDACTED] `1.2`，[NON-ENGLISH REDACTED] `8` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `1.5 MPa`，[NON-ENGLISH REDACTED] `99 kmol/h`，[NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] `FEEDPUMP`（`Pump` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `0.6`，[NON-ENGLISH REDACTED] `0.9`
- [NON-ENGLISH REDACTED] `PIPE`（`Pipe` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `40`，[NON-ENGLISH REDACTED] `1 in`，[NON-ENGLISH REDACTED] `25 m`
- [NON-ENGLISH REDACTED] `PUMP`（`Pump HI`）：[NON-ENGLISH REDACTED] `2.6 MPa`
- [NON-ENGLISH REDACTED] `COMP`（`Compr` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `0.4 MPa`
- [NON-ENGLISH REDACTED] `VALVE`（`Valve` [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] `2 MPa`，[NON-ENGLISH REDACTED] `V810 equal percent flow` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `1.5 in`

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] `FEEDPUMP`，[NON-ENGLISH REDACTED] `BZIN → FEEDPUMP → BZIN2`，[NON-ENGLISH REDACTED] `PUMP`。

- `FEEDPUMP` [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
- `FEEDPUMP` [NON-ENGLISH REDACTED] `0.6`，[NON-ENGLISH REDACTED] `0.9`；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `FEED-MIX` [NON-ENGLISH REDACTED] `2.3 MPa` [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] `PUMP` [NON-ENGLISH REDACTED] `2.6 MPa`，[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] `m3/h` [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] SI [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `FEEDPUMP` [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] ID [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] 1 | [NON-ENGLISH REDACTED] 2 | [NON-ENGLISH REDACTED] 3 | [NON-ENGLISH REDACTED] 4 |
| --- | --- | --- | --- | --- |
| [NON-ENGLISH REDACTED] / (m3/h) | 20 | 10 | 5 | 3 |
| [NON-ENGLISH REDACTED] | 40 | 250 | 300 | 400 |

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]。

```

### FILE: generated/react_v2_task_figure_grounding.md
Reason: reviewed V2 figure grounding reused for React
```text
# V2 Figure Grounding

This is the reviewed cached figure grounding for the current case.

## subfigure_scope_and_authority
[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]：1 [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] 5.1 [NON-ENGLISH REDACTED]”，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”。[NON-ENGLISH REDACTED]。

Visual evidence:
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、(a)/(b)、part_a/part_b、[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。
- [NON-ENGLISH REDACTED]：BZIN、H2IN、BZIN2、H2RCY2、RXIN、RXOUT、VAP、H2RCY、PURGE、PURGE2、LIQ、COLFD、CHRCY、CHRCY2、CHRCY3、LTENDS、PRODUCT。
- [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] BZIN/H2IN [NON-ENGLISH REDACTED] FEED-MIX，[NON-ENGLISH REDACTED] REACT、HP-SEP [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] VFLOW [NON-ENGLISH REDACTED] H2RCY [NON-ENGLISH REDACTED] PURGE，[NON-ENGLISH REDACTED] LFLOW [NON-ENGLISH REDACTED] COLUMN [NON-ENGLISH REDACTED] FEED-MIX。

## labels_and_topology
{&#x27;visible_modules_or_equipment&#x27;: [{&#x27;visible_label&#x27;: &#x27;FEEDPUMP&#x27;, &#x27;type_from_context&#x27;: &#x27;Pump&#x27;}, {&#x27;visible_label&#x27;: &#x27;FEED-MIX&#x27;, &#x27;type_from_context&#x27;: &#x27;Heater&#x27;}, {&#x27;visible_label&#x27;: &#x27;REACT&#x27;, &#x27;type_from_context&#x27;: &#x27;Rstoic&#x27;}, {&#x27;visible_label&#x27;: &#x27;HP-SEP&#x27;, &#x27;type_from_context&#x27;: &#x27;Flash2&#x27;}, {&#x27;visible_label&#x27;: &#x27;VFLOW&#x27;, &#x27;type_from_context&#x27;: &#x27;FSplit&#x27;}, {&#x27;visible_label&#x27;: &#x27;VALVE&#x27;, &#x27;type_from_context&#x27;: &#x27;Valve&#x27;}, {&#x27;visible_label&#x27;: &#x27;COMP&#x27;, &#x27;type_from_context&#x27;: &#x27;Compr&#x27;}, {&#x27;visible_label&#x27;: &#x27;LFLOW&#x27;, &#x27;type_from_context&#x27;: &#x27;FSplit&#x27;}, {&#x27;visible_label&#x27;: &#x27;PUMP&#x27;, &#x27;type_from_context&#x27;: &#x27;Pump HI&#x27;}, {&#x27;visible_label&#x27;: &#x27;PIPE&#x27;, &#x27;type_from_context&#x27;: &#x27;Pipe&#x27;}, {&#x27;visible_label&#x27;: &#x27;COLUMN&#x27;, &#x27;type_from_context&#x27;: &#x27;RadFrac&#x27;}], &#x27;visible_stream_labels&#x27;: [&#x27;BZIN&#x27;, &#x27;H2IN&#x27;, &#x27;BZIN2&#x27;, &#x27;H2RCY2&#x27;, &#x27;RXIN&#x27;, &#x27;RXOUT&#x27;, &#x27;VAP&#x27;, &#x27;H2RCY&#x27;, &#x27;PURGE&#x27;, &#x27;PURGE2&#x27;, &#x27;LIQ&#x27;, &#x27;COLFD&#x27;, &#x27;CHRCY&#x27;, &#x27;CHRCY2&#x27;, &#x27;CHRCY3&#x27;, &#x27;LTENDS&#x27;, &#x27;PRODUCT&#x27;], &#x27;directly_visible_connections_as_edges&#x27;: [{&#x27;stream_label&#x27;: &#x27;BZIN&#x27;, &#x27;connection&#x27;: &#x27;external left feed -&gt; into FEEDPUMP&#x27;}, {&#x27;stream_label&#x27;: &#x27;BZIN2&#x27;, &#x27;connection&#x27;: &#x27;FEEDPUMP -&gt; into FEED-MIX&#x27;}, {&#x27;stream_label&#x27;: &#x27;H2IN&#x27;, &#x27;connection&#x27;: &#x27;external left feed -&gt; into FEED-MIX&#x27;}, {&#x27;stream_label&#x27;: &#x27;H2RCY2&#x27;, &#x27;connection&#x27;: &#x27;COMP -&gt; into FEED-MIX&#x27;}, {&#x27;stream_label&#x27;: &#x27;CHRCY3&#x27;, &#x27;connection&#x27;: &#x27;PIPE -&gt; into FEED-MIX&#x27;}, {&#x27;stream_label&#x27;: &#x27;RXIN&#x27;, &#x27;connection&#x27;: &#x27;FEED-MIX -&gt; into REACT&#x27;}, {&#x27;stream_label&#x27;: &#x27;RXOUT&#x27;, &#x27;connection&#x27;: &#x27;REACT -&gt; into HP-SEP&#x27;}, {&#x27;stream_label&#x27;: &#x27;VAP&#x27;, &#x27;connection&#x27;: &#x27;HP-SEP -&gt; into VFLOW&#x27;}, {&#x27;stream_label&#x27;: &#x27;H2RCY&#x27;, &#x27;connection&#x27;: &#x27;VFLOW -&gt; into COMP&#x27;}, {&#x27;stream_label&#x27;: &#x27;PURGE&#x27;, &#x27;connection&#x27;: &#x27;VFLOW -&gt; into VALVE&#x27;}, {&#x27;stream_label&#x27;: &#x27;PURGE2&#x27;, &#x27;connection&#x27;: &#x27;VALVE -&gt; external right outlet&#x27;}, {&#x27;stream_label&#x27;: &#x27;LIQ&#x27;, &#x27;connection&#x27;: &#x27;HP-SEP -&gt; into LFLOW&#x27;}, {&#x27;stream_label&#x27;: &#x27;COLFD&#x27;, &#x27;connection&#x27;: &#x27;LFLOW -&gt; into COLUMN&#x27;}, {&#x27;stream_label&#x27;: &#x27;CHRCY&#x27;, &#x27;connection&#x27;: &#x27;LFLOW -&gt; into PUMP&#x27;}, {&#x27;stream_label&#x27;: &#x27;CHRCY2&#x27;, &#x27;connection&#x27;: &#x27;PUMP -&gt; into PIPE&#x27;}, {&#x27;stream_label&#x27;: &#x27;LTENDS&#x27;, &#x27;connection&#x27;: &#x27;COLUMN -&gt; external right outlet&#x27;}, {&#x27;stream_label&#x27;: &#x27;PRODUCT&#x27;, &#x27;connection&#x27;: &#x27;COLUMN -&gt; external right outlet&#x27;}], &#x27;visible_node_fan_in_fan_out_summary&#x27;: [{&#x27;node&#x27;: &#x27;FEEDPUMP&#x27;, &#x27;fan_in&#x27;: [&#x27;BZIN&#x27;], &#x27;fan_out&#x27;: [&#x27;BZIN2&#x27;]}, {&#x27;node&#x27;: &#x27;FEED-MIX&#x27;, &#x27;fan_in&#x27;: [&#x27;BZIN2&#x27;, &#x27;H2IN&#x27;, &#x27;H2RCY2&#x27;, &#x27;CHRCY3&#x27;], &#x27;fan_out&#x27;: [&#x27;RXIN&#x27;]}, {&#x27;node&#x27;: &#x27;REACT&#x27;, &#x27;fan_in&#x27;: [&#x27;RXIN&#x27;], &#x27;fan_out&#x27;: [&#x27;RXOUT&#x27;]}, {&#x27;node&#x27;: &#x27;HP-SEP&#x27;, &#x27;fan_in&#x27;: [&#x27;RXOUT&#x27;], &#x27;fan_out&#x27;: [&#x27;VAP&#x27;, &#x27;LIQ&#x27;]}, {&#x27;node&#x27;: &#x27;VFLOW&#x27;, &#x27;fan_in&#x27;: [&#x27;VAP&#x27;], &#x27;fan_out&#x27;: [&#x27;H2RCY&#x27;, &#x27;PURGE&#x27;]}, {&#x27;node&#x27;: &#x27;COMP&#x27;, &#x27;fan_in&#x27;: [&#x27;H2RCY&#x27;], &#x27;fan_out&#x27;: [&#x27;H2RCY2&#x27;]}, {&#x27;node&#x27;: &#x27;VALVE&#x27;, &#x27;fan_in&#x27;: [&#x27;PURGE&#x27;], &#x27;fan_out&#x27;: [&#x27;PURGE2&#x27;]}, {&#x27;node&#x27;: &#x27;LFLOW&#x27;, &#x27;fan_in&#x27;: [&#x27;LIQ&#x27;], &#x27;fan_out&#x27;: [&#x27;COLFD&#x27;, &#x27;CHRCY&#x27;]}, {&#x27;node&#x27;: &#x27;PUMP&#x27;, &#x27;fan_in&#x27;: [&#x27;CHRCY&#x27;], &#x27;fan_out&#x27;: [&#x27;CHRCY2&#x27;]}, {&#x27;node&#x27;: &#x27;PIPE&#x27;, &#x27;fan_in&#x27;: [&#x27;CHRCY2&#x27;], &#x27;fan_out&#x27;: [&#x27;CHRCY3&#x27;]}, {&#x27;node&#x27;: &#x27;COLUMN&#x27;, &#x27;fan_in&#x27;: [&#x27;COLFD&#x27;], &#x27;fan_out&#x27;: [&#x27;LTENDS&#x27;, &#x27;PRODUCT&#x27;]}]}

Visual evidence:
- [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]：&quot;FEEDPUMP&quot;, &quot;FEED-MIX&quot;, &quot;REACT&quot;, &quot;HP-SEP&quot;, &quot;VFLOW&quot;, &quot;VALVE&quot;, &quot;COMP&quot;, &quot;LFLOW&quot;, &quot;PUMP&quot;, &quot;PIPE&quot;, &quot;COLUMN&quot;。
- [NON-ENGLISH REDACTED] &quot;BZIN&quot; [NON-ENGLISH REDACTED] &quot;FEEDPUMP&quot;，[NON-ENGLISH REDACTED] &quot;BZIN2&quot; [NON-ENGLISH REDACTED] &quot;FEED-MIX&quot;。
- &quot;FEED-MIX&quot; [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] &quot;H2IN&quot;, &quot;BZIN2&quot;, &quot;H2RCY2&quot;, &quot;CHRCY3&quot; [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] &quot;RXIN&quot; [NON-ENGLISH REDACTED] &quot;REACT&quot;。
- &quot;REACT&quot; [NON-ENGLISH REDACTED] &quot;RXOUT&quot; [NON-ENGLISH REDACTED] &quot;HP-SEP&quot;。
- &quot;HP-SEP&quot; [NON-ENGLISH REDACTED] &quot;VAP&quot; [NON-ENGLISH REDACTED] &quot;VFLOW&quot;，[NON-ENGLISH REDACTED] &quot;LIQ&quot; [NON-ENGLISH REDACTED] &quot;LFLOW&quot;。
- &quot;VFLOW&quot; [NON-ENGLISH REDACTED] &quot;H2RCY&quot;，[NON-ENGLISH REDACTED] &quot;COMP&quot;；[NON-ENGLISH REDACTED] &quot;PURGE&quot; [NON-ENGLISH REDACTED] &quot;VALVE&quot; [NON-ENGLISH REDACTED] &quot;PURGE2&quot;。
- &quot;LFLOW&quot; [NON-ENGLISH REDACTED] &quot;COLFD&quot; [NON-ENGLISH REDACTED] &quot;COLUMN&quot;；[NON-ENGLISH REDACTED] &quot;CHRCY&quot; [NON-ENGLISH REDACTED] &quot;PUMP&quot;，[NON-ENGLISH REDACTED] &quot;CHRCY2&quot; [NON-ENGLISH REDACTED] &quot;PIPE&quot;，[NON-ENGLISH REDACTED] &quot;CHRCY3&quot; [NON-ENGLISH REDACTED] &quot;FEED-MIX&quot;。
- &quot;COLUMN&quot; [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] &quot;LTENDS&quot;，[NON-ENGLISH REDACTED] &quot;PRODUCT&quot;。

Uncertainties:
- [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] COLUMN [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] &quot;COLUMN&quot; [NON-ENGLISH REDACTED]。
- &quot;type_from_context&quot; [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。

## numbers_and_constraints
{&#x27;[NON-ENGLISH REDACTED]&#x27;: [], &#x27;[NON-ENGLISH REDACTED]&#x27;: [], &#x27;[NON-ENGLISH REDACTED]&#x27;: [], &#x27;[NON-ENGLISH REDACTED]&#x27;: [], &#x27;[NON-ENGLISH REDACTED]&#x27;: [], &#x27;[NON-ENGLISH REDACTED]&#x27;: [&#x27;FEEDPUMP&#x27;, &#x27;FEED-MIX&#x27;, &#x27;REACT&#x27;, &#x27;HP-SEP&#x27;, &#x27;VFLOW&#x27;, &#x27;VALVE&#x27;, &#x27;COMP&#x27;, &#x27;LFLOW&#x27;, &#x27;PUMP&#x27;, &#x27;PIPE&#x27;, &#x27;COLUMN&#x27;], &#x27;[NON-ENGLISH REDACTED]&#x27;: [&#x27;BZIN&#x27;, &#x27;H2IN&#x27;, &#x27;BZIN2&#x27;, &#x27;H2RCY2&#x27;, &#x27;RXIN&#x27;, &#x27;RXOUT&#x27;, &#x27;VAP&#x27;, &#x27;H2RCY&#x27;, &#x27;PURGE&#x27;, &#x27;PURGE2&#x27;, &#x27;LIQ&#x27;, &#x27;COLFD&#x27;, &#x27;CHRCY&#x27;, &#x27;CHRCY2&#x27;, &#x27;CHRCY3&#x27;, &#x27;LTENDS&#x27;, &#x27;PRODUCT&#x27;], &#x27;[NON-ENGLISH REDACTED]_[NON-ENGLISH REDACTED]_[NON-ENGLISH REDACTED]_[NON-ENGLISH REDACTED]&#x27;: {&#x27;PRODUCT&#x27;: &#x27;COLUMN [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]&#x27;, &#x27;LTENDS&#x27;: &#x27;COLUMN [NON-ENGLISH REDACTED]&#x27;, &#x27;H2RCY&#x27;: &#x27;VFLOW [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] COMP&#x27;, &#x27;H2RCY2&#x27;: &#x27;COMP [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] FEED-MIX&#x27;, &#x27;CHRCY&#x27;: &#x27;LFLOW [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] PUMP&#x27;, &#x27;CHRCY2&#x27;: &#x27;PUMP [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] PIPE&#x27;, &#x27;CHRCY3&#x27;: &#x27;PIPE [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] FEED-MIX&#x27;, &#x27;PURGE&#x27;: &#x27;VFLOW [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] VALVE&#x27;, &#x27;PURGE2&#x27;: &#x27;VALVE [NON-ENGLISH REDACTED]&#x27;}, &#x27;[NON-ENGLISH REDACTED]_Aspen_[NON-ENGLISH REDACTED]&#x27;: [&#x27;BZIN [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] FEEDPUMP；FEEDPUMP [NON-ENGLISH REDACTED] BZIN2。&#x27;, &#x27;H2IN [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] FEED-MIX。&#x27;, &#x27;FEED-MIX [NON-ENGLISH REDACTED] 4 [NON-ENGLISH REDACTED]：BZIN2、H2IN、H2RCY2、CHRCY3；[NON-ENGLISH REDACTED] RXIN。&#x27;, &#x27;RXIN [NON-ENGLISH REDACTED] REACT；REACT [NON-ENGLISH REDACTED] RXOUT。&#x27;, &#x27;RXOUT [NON-ENGLISH REDACTED] HP-SEP；HP-SEP [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] VAP、[NON-ENGLISH REDACTED] LIQ。&#x27;, &#x27;VAP [NON-ENGLISH REDACTED] VFLOW；VFLOW [NON-ENGLISH REDACTED] H2RCY [NON-ENGLISH REDACTED] PURGE [NON-ENGLISH REDACTED]。&#x27;, &#x27;H2RCY [NON-ENGLISH REDACTED] COMP [NON-ENGLISH REDACTED] H2RCY2，[NON-ENGLISH REDACTED] FEED-MIX，[NON-ENGLISH REDACTED]。&#x27;, &#x27;PURGE [NON-ENGLISH REDACTED] VALVE [NON-ENGLISH REDACTED] PURGE2，[NON-ENGLISH REDACTED]。&#x27;, &#x27;LIQ [NON-ENGLISH REDACTED] LFLOW；LFLOW [NON-ENGLISH REDACTED] COLFD [NON-ENGLISH REDACTED] CHRCY [NON-ENGLISH REDACTED]。&#x27;, &#x27;COLFD [NON-ENGLISH REDACTED] COLUMN。&#x27;, &#x27;CHRCY [NON-ENGLISH REDACTED] PUMP、PIPE，[NON-ENGLISH REDACTED] CHRCY、CHRCY2、CHRCY3，[NON-ENGLISH REDACTED] FEED-MIX，[NON-ENGLISH REDACTED]。&#x27;, &#x27;COLUMN [NON-ENGLISH REDACTED] COLFD，[NON-ENGLISH REDACTED]：LTENDS [NON-ENGLISH REDACTED] PRODUCT。&#x27;, &#x27;[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]。&#x27;]}

Visual evidence:
- [NON-ENGLISH REDACTED]：&quot;FEEDPUMP&quot;, &quot;FEED-MIX&quot;, &quot;REACT&quot;, &quot;HP-SEP&quot;, &quot;VFLOW&quot;, &quot;VALVE&quot;, &quot;COMP&quot;, &quot;LFLOW&quot;, &quot;PUMP&quot;, &quot;PIPE&quot;, &quot;COLUMN&quot;。
- [NON-ENGLISH REDACTED] &quot;BZIN&quot; [NON-ENGLISH REDACTED] &quot;FEEDPUMP&quot;，[NON-ENGLISH REDACTED] &quot;BZIN2&quot;。
- &quot;H2IN&quot;, &quot;BZIN2&quot;, &quot;H2RCY2&quot;, &quot;CHRCY3&quot; [NON-ENGLISH REDACTED] &quot;FEED-MIX&quot;，&quot;FEED-MIX&quot; [NON-ENGLISH REDACTED] &quot;RXIN&quot;。
- &quot;RXIN&quot; [NON-ENGLISH REDACTED] &quot;REACT&quot;，&quot;REACT&quot; [NON-ENGLISH REDACTED] &quot;RXOUT&quot;，[NON-ENGLISH REDACTED] &quot;HP-SEP&quot;。
- &quot;HP-SEP&quot; [NON-ENGLISH REDACTED] &quot;VAP&quot;，[NON-ENGLISH REDACTED] &quot;LIQ&quot;。
- &quot;VAP&quot; [NON-ENGLISH REDACTED] &quot;VFLOW&quot;；&quot;VFLOW&quot; [NON-ENGLISH REDACTED] &quot;H2RCY&quot;，[NON-ENGLISH REDACTED] &quot;PURGE&quot;。
- &quot;H2RCY&quot; [NON-ENGLISH REDACTED] &quot;COMP&quot;，[NON-ENGLISH REDACTED] &quot;H2RCY2&quot; [NON-ENGLISH REDACTED] &quot;FEED-MIX&quot;。
- &quot;PURGE&quot; [NON-ENGLISH REDACTED] &quot;VALVE&quot; [NON-ENGLISH REDACTED] &quot;PURGE2&quot;，[NON-ENGLISH REDACTED]。
- &quot;LIQ&quot; [NON-ENGLISH REDACTED] &quot;LFLOW&quot;；&quot;LFLOW&quot; [NON-ENGLISH REDACTED] &quot;COLFD&quot;，[NON-ENGLISH REDACTED] &quot;COLUMN&quot;；[NON-ENGLISH REDACTED] &quot;CHRCY&quot;。
- &quot;CHRCY&quot; [NON-ENGLISH REDACTED] &quot;PUMP&quot;，[NON-ENGLISH REDACTED] &quot;CHRCY2&quot;，[NON-ENGLISH REDACTED] &quot;PIPE&quot;，[NON-ENGLISH REDACTED] &quot;CHRCY3&quot; [NON-ENGLISH REDACTED] &quot;FEED-MIX&quot;。
- &quot;COLUMN&quot; [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] &quot;LTENDS&quot;，[NON-ENGLISH REDACTED] &quot;PRODUCT&quot;。

Uncertainties:
- [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]。
- COLUMN [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]。

## stream_types_and_coupling
{&#x27;stream_type_classification&#x27;: {&#x27;material_streams_solid_line&#x27;: [&#x27;BZIN&#x27;, &#x27;H2IN&#x27;, &#x27;BZIN2&#x27;, &#x27;H2RCY2&#x27;, &#x27;RXIN&#x27;, &#x27;RXOUT&#x27;, &#x27;VAP&#x27;, &#x27;H2RCY&#x27;, &#x27;PURGE&#x27;, &#x27;PURGE2&#x27;, &#x27;LIQ&#x27;, &#x27;COLFD&#x27;, &#x27;CHRCY&#x27;, &#x27;CHRCY2&#x27;, &#x27;CHRCY3&#x27;, &#x27;LTENDS&#x27;, &#x27;PRODUCT&#x27;], &#x27;heat_streams_dashed_line_with_C&#x27;: [], &#x27;work_streams_dashed_line_with_W&#x27;: [], &#x27;power_streams_dashed_line_with_I&#x27;: []}, &#x27;block_unit_symbols_separate_from_stream_labels&#x27;: [&#x27;FEEDPUMP&#x27;, &#x27;FEED-MIX&#x27;, &#x27;REACT&#x27;, &#x27;HP-SEP&#x27;, &#x27;VFLOW&#x27;, &#x27;VALVE&#x27;, &#x27;COMP&#x27;, &#x27;LFLOW&#x27;, &#x27;PUMP&#x27;, &#x27;PIPE&#x27;, &#x27;COLUMN&#x27;], &#x27;summary&#x27;: &#x27;All visible labeled streams in the task figure are drawn as solid material-flow lines. No dashed heat/work/power coupling lines with C, W, or I symbols are visible.&#x27;}

Uncertainties:
- The figure is low-resolution, but the visible stream lines appear consistently solid; no dashed heat/work/power stream symbols are discernible.
- Block/unit symbols are listed as visible block labels only; the provided reference legend is for stream types, not for detailed equipment-icon classification.

## multi_effect_evaporation_port_contract
{&#x27;is_active_figure_multi_effect_evaporation_flowsheet&#x27;: False, &#x27;reason&#x27;: &#x27;The active figure is a cyclohexane production/reaction-separation flowsheet, not a multi-effect evaporation flowsheet. No evaporator effects, condensers, Q1/Q2/Q3/Q4 heat labels, or heat-cascade lines are visible.&#x27;, &#x27;aspen_topology_contract_from_active_subfigure_only&#x27;: {&#x27;liquid_or_concentrate_material_path&#x27;: {&#x27;status&#x27;: &#x27;not a multi-effect evaporation liquid/concentrate path&#x27;, &#x27;visible_material_edges&#x27;: [&#x27;BZIN -&gt; FEEDPUMP -&gt; BZIN2 -&gt; FEED-MIX&#x27;, &#x27;FEED-MIX -&gt; RXIN -&gt; REACT&#x27;, &#x27;REACT -&gt; RXOUT -&gt; HP-SEP&#x27;, &#x27;HP-SEP -&gt; LIQ -&gt; LFLOW&#x27;, &#x27;LFLOW -&gt; COLFD -&gt; COLUMN&#x27;, &#x27;COLUMN -&gt; PRODUCT&#x27;, &#x27;LFLOW -&gt; CHRCY -&gt; PUMP -&gt; CHRCY2 -&gt; PIPE -&gt; CHRCY3 -&gt; FEED-MIX&#x27;]}, &#x27;secondary_vapor_or_heating_material_path&#x27;: {&#x27;status&#x27;: &#x27;no multi-effect secondary-vapor/heating-material cascade is visible&#x27;, &#x27;visible_vapor_or_gas_material_edges&#x27;: [&#x27;HP-SEP -&gt; VAP -&gt; VFLOW&#x27;, &#x27;VFLOW -&gt; H2RCY -&gt; COMP -&gt; H2RCY2 -&gt; FEED-MIX&#x27;, &#x27;VFLOW -&gt; PURGE -&gt; VALVE -&gt; PURGE2&#x27;, &#x27;H2IN -&gt; FEED-MIX&#x27;], &#x27;material_vapor_streams_feeding_heater_or_exchanger_symbols_separate_from_Q&#x27;: [{&#x27;stream&#x27;: &#x27;H2IN&#x27;, &#x27;visible_connection&#x27;: &#x27;external feed -&gt; FEED-MIX&#x27;, &#x27;note&#x27;: &#x27;This is a material stream, not a Q heat stream.&#x27;}, {&#x27;stream&#x27;: &#x27;H2RCY2&#x27;, &#x27;visible_connection&#x27;: &#x27;COMP -&gt; FEED-MIX&#x27;, &#x27;note&#x27;: &#x27;This is a material recycle stream, not a Q heat stream.&#x27;}]}, &#x27;condensate_or_water_path&#x27;: {&#x27;status&#x27;: &#x27;none visible&#x27;, &#x27;visible_edges&#x27;: []}, &#x27;heat_or_energy_coupling_path&#x27;: {&#x27;status&#x27;: &#x27;none visible&#x27;, &#x27;visible_Q_heat_stream_rows&#x27;: [], &#x27;unresolved_Q_heat_stream_rows&#x27;: [], &#x27;note&#x27;: &#x27;No visible heat labels such as Q1, Q2, Q3, or Q4 appear in the active figure, so no Aspen heat-port contract of the form source.HS(OUT) -&gt; Q* -&gt; sink.HS(IN) can be completed or even proposed from this figure.&#x27;}}}

Visual evidence:
- Visible equipment/module labels are: FEEDPUMP, FEED-MIX, REACT, HP-SEP, VFLOW, VALVE, COMP, LFLOW, PUMP, PIPE, COLUMN.
- Visible stream labels include: BZIN, H2IN, BZIN2, H2RCY2, RXIN, RXOUT, VAP, H2RCY, PURGE, PURGE2, LIQ, COLFD, CHRCY, CHRCY2, CHRCY3, LTENDS, PRODUCT.
- The only visibly labeled flash-like unit is HP-SEP, with RXOUT entering and VAP/LIQ leaving.
- The vapor/gas path shown is HP-SEP -&gt; VAP -&gt; VFLOW, then split to H2RCY through COMP back to FEED-MIX and PURGE through VALVE to PURGE2.
- No labels Q1, Q2, Q3, Q4, no dashed heat streams, and no evaporator-effect labels are visible in the active figure.

Uncertainties:
- The figure does not show any heat-stream labels or explicit Aspen energy ports; therefore heat coupling endpoints cannot be resolved.
- FEED-MIX is identified in the task context as a Heater module, but the visible figure does not show a separate Q heat stream into or out of it.
- The active figure is not a multi-effect evaporation flowsheet, so evaporation-specific path classes are not directly applicable.

## label_semantics_and_mapping
[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。[NON-ENGLISH REDACTED]：BZIN、H2IN、BZIN2、H2RCY2、RXIN、RXOUT、VAP、H2RCY、PURGE、PURGE2、LIQ、COLFD、CHRCY、CHRCY2、CHRCY3、LTENDS、PRODUCT。

[NON-ENGLISH REDACTED]：BZIN2、H2RCY2、PURGE2、CHRCY2、CHRCY3；[NON-ENGLISH REDACTED] H2IN、H2RCY、H2RCY2 [NON-ENGLISH REDACTED]“H2”[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]2[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]2[NON-ENGLISH REDACTED]”。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、LFLOW、COLUMN、PIPE、PUMP、COMP、VALVE [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] H2IN、BZIN、H2RCY、CHRCY、PRODUCT [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]：COLUMN [NON-ENGLISH REDACTED]“12 [NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] 8 [NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] COLFD [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] 1、[NON-ENGLISH REDACTED] 2、[NON-ENGLISH REDACTED] 3、[NON-ENGLISH REDACTED] 4”[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] FEEDPUMP [NON-ENGLISH REDACTED] PUMP [NON-ENGLISH REDACTED]；BZIN2、H2RCY2、PURGE2、CHRCY2、CHRCY3 [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]“PUMP”[NON-ENGLISH REDACTED]“FEEDPUMP”[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。

Visual evidence:
- [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]：&quot;FEEDPUMP&quot;, &quot;FEED-MIX&quot;, &quot;REACT&quot;, &quot;HP-SEP&quot;, &quot;VFLOW&quot;, &quot;VALVE&quot;, &quot;COMP&quot;, &quot;LFLOW&quot;, &quot;PUMP&quot;, &quot;PIPE&quot;, &quot;COLUMN&quot;。
- [NON-ENGLISH REDACTED]：&quot;BZIN&quot;, &quot;H2IN&quot;, &quot;BZIN2&quot;, &quot;H2RCY2&quot;, &quot;RXIN&quot;, &quot;RXOUT&quot;, &quot;VAP&quot;, &quot;H2RCY&quot;, &quot;PURGE&quot;, &quot;PURGE2&quot;, &quot;LIQ&quot;, &quot;COLFD&quot;, &quot;CHRCY&quot;, &quot;CHRCY2&quot;, &quot;CHRCY3&quot;, &quot;LTENDS&quot;, &quot;PRODUCT&quot;。
- &quot;BZIN&quot; [NON-ENGLISH REDACTED] &quot;FEEDPUMP&quot;，[NON-ENGLISH REDACTED] &quot;BZIN2&quot;，[NON-ENGLISH REDACTED] BZIN2 [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
- &quot;H2RCY&quot; [NON-ENGLISH REDACTED] &quot;COMP&quot; [NON-ENGLISH REDACTED] &quot;H2RCY2&quot; [NON-ENGLISH REDACTED] &quot;FEED-MIX&quot;；[NON-ENGLISH REDACTED]。
- &quot;PURGE&quot; [NON-ENGLISH REDACTED] &quot;VALVE&quot; [NON-ENGLISH REDACTED] &quot;PURGE2&quot;；[NON-ENGLISH REDACTED]。
- &quot;CHRCY&quot; [NON-ENGLISH REDACTED] &quot;PUMP&quot; [NON-ENGLISH REDACTED] &quot;CHRCY2&quot;，[NON-ENGLISH REDACTED] &quot;PIPE&quot; [NON-ENGLISH REDACTED] &quot;CHRCY3&quot;，[NON-ENGLISH REDACTED] &quot;FEED-MIX&quot;；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
- &quot;COLUMN&quot; [NON-ENGLISH REDACTED] &quot;COLFD&quot; [NON-ENGLISH REDACTED] &quot;LTENDS&quot;、&quot;PRODUCT&quot;；[NON-ENGLISH REDACTED] 1–12、[NON-ENGLISH REDACTED] 8 [NON-ENGLISH REDACTED]。

Uncertainties:
- [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] BZIN2、PURGE2、CHRCY2、CHRCY3，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
- COLUMN [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] 1–4”[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。
- FEEDPUMP [NON-ENGLISH REDACTED] PUMP [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。

## icon_unit_family
[{&#x27;symbol_id&#x27;: &#x27;S1&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;far left on the lower incoming material line&#x27;, &#x27;icon_candidates&#x27;: [&#x27;Pump&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;Pump&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The symbol is a small circular rotating-equipment icon with a short connected line and base-like shading, matching the supplied Pump icon more closely than vessel, valve, or column icons.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context describes this left-side pressure-raising unit as a pump.&#x27;, &#x27;confidence&#x27;: &#x27;high&#x27;, &#x27;uncertainty&#x27;: &#x27;Low-resolution shading makes fine details indistinct, but the round pump-like shape is distinctive.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S2&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;left-center where several incoming lines join before the reactor-like vessel&#x27;, &#x27;icon_candidates&#x27;: [&#x27;Heater&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;Heater&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The remaining non-text symbol is a small round icon with internal diagonal/zigzag-like markings. This is closest to the supplied Heater icon, not to the triangular Mixer or FSplit icons.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context states that this feed conditioning/mixing point is modeled with a heater-type module.&#x27;, &#x27;confidence&#x27;: &#x27;medium&#x27;, &#x27;uncertainty&#x27;: &#x27;The internal markings are small and blurred; the symbol also functions topologically as a mixing point, but its shape does not match the supplied triangular Mixer icon.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S3&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;center-left, immediately downstream of the round multi-inlet symbol&#x27;, &#x27;icon_candidates&#x27;: [&#x27;RStoic&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;RStoic&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The symbol is a horizontal cylindrical vessel with internal crosshatched/packed-looking shading, closely matching the supplied RStoic reactor icon.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context describes this step as the stoichiometric reaction section.&#x27;, &#x27;confidence&#x27;: &#x27;high&#x27;, &#x27;uncertainty&#x27;: &#x27;The hatch pattern is somewhat low-resolution, but the horizontal crosshatched reactor vessel is visually distinctive.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S4&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;center-right vertical vessel receiving material from the reactor-like symbol and sending one line upward and one downward&#x27;, &#x27;icon_candidates&#x27;: [&#x27;Flash2&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;Flash2&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The symbol is a simple vertical rounded vessel without column trays or external condenser/reboiler attachments, matching the supplied Flash2 icon.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context describes this vessel as a two-phase flash separator.&#x27;, &#x27;confidence&#x27;: &#x27;high&#x27;, &#x27;uncertainty&#x27;: &#x27;It could be generically interpreted as a vertical separator from shape alone, but among the supplied icons Flash2 is the closest match.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S5&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;upper middle, small filled square on the upward vapor/gas path where the line divides left and right&#x27;, &#x27;icon_candidates&#x27;: [&#x27;FSplit&#x27;, &#x27;Dupl&#x27;, &#x27;Mult&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;FSplit&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The visible symbol is only a small filled square junction with one incoming line and two outgoing lines. It does not closely match the supplied wedge-shaped FSplit icon or the boxed Mult/Dupl icons, so the match is a simplified splitter-marker ambiguity rather than a distinctive icon match.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context identifies this upper gas-path divider as a fractional splitter.&#x27;, &#x27;confidence&#x27;: &#x27;medium-low&#x27;, &#x27;uncertainty&#x27;: &#x27;Shape alone is not a close match to any supplied splitter icon; the candidate ranking depends strongly on the non-text split topology and task context.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S6&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;upper left of the vapor/gas recycle loop, on the line returning toward the central feed-conditioning area&#x27;, &#x27;icon_candidates&#x27;: [&#x27;Compr&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;Compr&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The symbol is a tapered wedge/trapezoid rotating-equipment icon, visually matching the supplied compressor icon.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context describes this recycle-gas pressure-changing unit as a compressor.&#x27;, &#x27;confidence&#x27;: &#x27;high&#x27;, &#x27;uncertainty&#x27;: &#x27;No significant ambiguity from the remaining shape.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S7&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;upper right on the outlet branch after the upper splitter marker&#x27;, &#x27;icon_candidates&#x27;: [&#x27;Valve&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;Valve&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The symbol is an inline valve/bowtie-like mark with a small stem-like feature, matching the supplied Valve icon.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context describes this outlet pressure-changing unit as a valve.&#x27;, &#x27;confidence&#x27;: &#x27;high&#x27;, &#x27;uncertainty&#x27;: &#x27;The icon is small, but its inline valve geometry is recognizable.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S8&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;lower middle, small filled square below the vertical flash-like vessel where the liquid path divides&#x27;, &#x27;icon_candidates&#x27;: [&#x27;FSplit&#x27;, &#x27;Dupl&#x27;, &#x27;Mult&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;FSplit&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The visible symbol is a small filled square junction with one incoming line and two outgoing lines. It is not a distinctive match to the supplied wedge-shaped FSplit icon, so the geometry-only identification remains ambiguous among simplified splitter-type blocks.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context identifies this lower liquid-path divider as a fractional splitter.&#x27;, &#x27;confidence&#x27;: &#x27;medium-low&#x27;, &#x27;uncertainty&#x27;: &#x27;The square marker shape is not a close geometry match to the supplied Aspen splitter icons; context is needed to prefer FSplit.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S9&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;lower center-left on the recycle line leaving the lower splitter marker&#x27;, &#x27;icon_candidates&#x27;: [&#x27;Pump&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;Pump&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The symbol is a circular rotating-equipment icon with connected inlet/outlet lines, matching the supplied Pump icon.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context describes this lower recycle pressure-raising unit as a pump.&#x27;, &#x27;confidence&#x27;: &#x27;high&#x27;, &#x27;uncertainty&#x27;: &#x27;Low-resolution shading limits fine-detail comparison, but the pump-like circle is clear.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S10&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;lower left-of-center, horizontal tubular element downstream of the lower pump-like symbol&#x27;, &#x27;icon_candidates&#x27;: [&#x27;Pipe&#x27;, &#x27;Pipeline&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;Pipe&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The symbol is a short horizontal cylindrical tube. This geometry is closest to the supplied Pipe and Pipeline icons, which are visually similar in the legend.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context describes this recycle-line element as a pipe section.&#x27;, &#x27;confidence&#x27;: &#x27;medium-high&#x27;, &#x27;uncertainty&#x27;: &#x27;The supplied Pipe and Pipeline icons are very similar; the figure’s simplified tube shape does not distinguish them by geometry alone.&#x27;}, {&#x27;symbol_id&#x27;: &#x27;S11&#x27;, &#x27;symbol_location_without_using_text&#x27;: &#x27;right side, tall vertical tower with side connection from the lower splitter path and two product-side exits&#x27;, &#x27;icon_candidates&#x27;: [&#x27;DSTWU&#x27;, &#x27;Distl&#x27;, &#x27;RadFrac&#x27;], &#x27;preferred_candidate_from_task_context&#x27;: &#x27;RadFrac&#x27;, &#x27;visual_reason_from_shape_only&#x27;: &#x27;The symbol is a vertical distillation-column-like vessel with small top and bottom auxiliary round features. The supplied DSTWU, Distl, and RadFrac column icons are visually very similar, so the simplified shape alone does not uniquely distinguish among them.&#x27;, &#x27;semantic_reason_from_task_context&#x27;: &#x27;The task context describes this tower as a rigorous distillation column modeled with a RadFrac-type block.&#x27;, &#x27;confidence&#x27;: &#x27;medium&#x27;, &#x27;uncertainty&#x27;: &#x27;The icon geometry alone is ambiguous among several distillation-column icons in the reference legend.&#x27;}]

Visual evidence:
- All rectangular callout boxes and text were mentally masked before matching.
- The remaining process symbols include two round pump-like icons, one round heater-like multi-inlet icon, one horizontal crosshatched reactor-like vessel, one simple vertical flash-like vessel, two small filled square splitter markers, one tapered compressor-like wedge, one inline valve symbol, one short horizontal tube, and one tall column-like tower.
- The two small filled square splitter markers are not close geometric matches to the supplied wedge or boxed splitter icons, so they are reported as simplified ambiguous splitter symbols rather than distinctive icon matches.

Uncertainties:
- The figure is low-resolution, so small internal markings are blurry.
- The splitter symbols appear as filled squares, whereas the provided reference splitter icons use other geometries; context is needed to prefer a specific splitter block type.
- The distillation-column icon is simplified and visually compatible with multiple supplied column-type icons.
- The short horizontal tube cannot be distinguished geometrically between Pipe and Pipeline from the supplied icons alone.

```

### FILE: generated/react_v2_target_priority_judgment.md
Reason: reviewed V2 target-priority context reused for React
```text
# Target Priority Judgment

Use this as a priority guide when planning repairs and interpreting target-related validation.
Primary semantic targets and topology hard gates are blocking. Secondary fidelity targets should be evidenced and reported, but they should not override primary targets or topology when conflicts are documented.

Source artifact: `&lt;REPOSITORY_ROOT&gt;\experiments\script_agent_experiment\iter0_context_packs\v2\cases\chinese_5_1_radfrac\target_priority_judgment.json`

## Primary Semantic Targets
- P1_product_cyclohexane_mole_fraction: Report the mole fraction of cyclohexane/C6H12 in the final PRODUCT material stream.
  Evidence policy: The stated objective is to[NON-ENGLISH REDACTED]. This is the main deliverable of the task.
- P2_aspen_flowsheet_result_path: The reported PRODUCT C6H12 mole fraction must come from a solved Aspen Plus flowsheet, not from a hand calculation or an input-only restatement.
  Evidence policy: The task asks to use Aspen Plus to create the cyclohexane production process and determine the product composition. A result not derived from the Aspen flowsheet would not satisfy the central request.
- P3_core_process_semantics: Model the intended cyclohexane production chemistry and separations: benzene hydrogenation C6H6 + 3 H2 -&gt; C6H12 with 99.8% benzene conversion, cooling/flash light-gas separation, vapor purge/recycle, liquid recycle/column feed split, and RadFrac stabilization column producing PRODUCT.
  Evidence policy: These features define the process whose product composition is requested. Omitting or replacing them changes the semantic meaning of the requested PRODUCT composition.
- P4_fixed_feed_and_major_operating_specs: Use the task-stated feed compositions/flow rates and major reactor, flash, split, and column operating specifications as the basis for the Aspen calculation.
  Evidence policy: The requested mole fraction is meaningful only for the given problem conditions, including H2IN, BZIN, reactor conversion/conditions, flash conditions, split fractions, and RadFrac conditions.

## Topology Hard Gates
- T1_visible_nodes_and_block_identities: The flowsheet must contain the figure-visible named process nodes FEEDPUMP, FEED-MIX, REACT, HP-SEP, VFLOW, VALVE, COMP, LFLOW, PUMP, PIPE, and COLUMN, with the text-specified Aspen block families where applicable.
  Evidence policy: The task asks to create the Aspen Plus flowsheet shown in the figure, and the text names the module families for these blocks. Removing, renaming, splitting, or substituting visible nodes changes the required flowsheet identity.
- T2_feed_mixing_and_reactor_path: The feed/recycle path must preserve the visible topology: BZIN -&gt; FEEDPUMP -&gt; BZIN2 -&gt; FEED-MIX; H2IN -&gt; FEED-MIX; H2RCY2 -&gt; FEED-MIX; CHRCY3 -&gt; FEED-MIX; FEED-MIX -&gt; RXIN -&gt; REACT -&gt; RXOUT -&gt; HP-SEP.
  Evidence policy: This is the figure-backed inlet and reactor topology leading to the process whose product is requested.
- T3_separator_vapor_recycle_and_purge_topology: HP-SEP vapor outlet must feed VFLOW; VFLOW must split to H2RCY -&gt; COMP -&gt; H2RCY2 -&gt; FEED-MIX and PURGE -&gt; VALVE -&gt; PURGE2.
  Evidence policy: The vapor recycle/purge loop is visible in the figure and described in the text as part of the cyclohexane production process.
- T4_separator_liquid_column_and_liquid_recycle_topology: HP-SEP liquid outlet must feed LFLOW; LFLOW must split to COLFD -&gt; COLUMN and CHRCY -&gt; PUMP -&gt; CHRCY2 -&gt; PIPE -&gt; CHRCY3 -&gt; FEED-MIX.
  Evidence policy: The liquid split to the stabilizer column and liquid recycle loop is figure-backed and text-backed. It determines the stream that enters the final product column.
- T5_column_product_identity: COLUMN must have COLFD as feed and LTENDS and PRODUCT as its two material outlets, with PRODUCT treated as the final product stream.
  Evidence policy: The requested result is specifically the product-stream composition; figure evidence identifies PRODUCT as the column outlet, not the purge, light ends, separator liquid, or column feed.
- T6_material_stream_not_heat_or_work_substitution: All visible labeled streams in the figure topology must be represented as material streams, not replaced by heat, work, or power streams.
  Evidence policy: The figure-grounding explicitly classifies the visible labeled streams as solid material-flow lines. Substituting nonmaterial connections would violate the flowsheet topology.

## Secondary Fidelity Targets
- S1_property_method_rk_soave: Use and/or document RK-SOAVE as the Aspen property method.
  Evidence policy: The task states RK-SOAVE, so this is important engineering fidelity. However, property-method readback/disclosure is a fidelity/reporting item and should not be merged with topology or the primary product-composition deliverable unless the wrong method demonstrably invalidates the reported Aspen result.
- S2_pressure_changing_unit_detailed_specs: Enter and report detailed pressure-changing unit specifications for FEEDPUMP, PUMP/Pump HI, COMP, PIPE, and VALVE, including efficiencies, outlet pressures/pressure increment, pipe material/schedule/diameter/length, valve type/diameter, and pump curve where applicable.
  Evidence policy: The problem explicitly highlights pressure-changing units, so these details are high-value fidelity. But exact pump-curve/valve/pipe reporting should not be allowed to swamp the primary target when implementation constraints arise, provided the visible pressure-unit topology and main Aspen product calculation are preserved.
- S3_component_material_balance_table: Provide component flow/composition material-balance tables for key streams including feeds, reactor/flash outlets, purge, recycle, column feed, light ends, and product.
  Evidence policy: A material-balance table helps validate the model, but the task’s main requested deliverable is the PRODUCT cyclohexane mole fraction.
- S4_convergence_and_rep_reporting: Report Aspen run/convergence status, recycle convergence status, block solved status, and nonempty PRODUCT composition results.
  Evidence policy: Successful solution is necessary evidence for an Aspen-derived result, but duplicate convergence/REP narration is marked scoring_only and should be treated as reporting fidelity unless failure also proves that no valid PRODUCT result exists.
- S5_product_composition_basis_documentation: Document that the reported C6H12 mole fraction is the raw full-material-stream mole fraction in PRODUCT including all present components.
  Evidence policy: Composition basis documentation improves reproducibility. The hard requirement is that the result be the PRODUCT stream C6H12 mole fraction; overly strict denominator narration should not be merged with topology or model construction gates.
- S6_exact_block_readback_and_numeric_tolerance_reporting: Provide exact readbacks/tolerance-level matching for all task-stated numeric conditions and stream pressures around equipment.
  Evidence policy: Detailed readbacks help validate fidelity, but exact narration of every numeric acceptance metric is not itself the primary deliverable. Major feed/reaction/flash/split/column deviations can fail the primary semantics, while minor reporting/readback omissions should not.

## Known Or Potential Secondary Conflicts

## Gate Mixing Assessment
Separate validation into: hard topology/identity gates for visible nodes, material-stream connections, and PRODUCT identity; primary semantic gates for Aspen-derived PRODUCT C6H12 mole fraction and core reaction/separation/column semantics; and secondary fidelity gates for RK-SOAVE disclosure, pressure-unit detailed readbacks, material-balance tables, exact reporting basis, and convergence/REP narration. Remove or ignore the erroneous phenol/solvent recycle_closure_contract for this case.

```

### FILE: generated/react_v2_planner_initial_context.md
Reason: reviewed V2 planner context reused for React
```text
# Planner Initial Context

This context was selected for the React run from the shared task planner.
Treat explicit task facts as hard requirements.

## Explicit Blocks
- name=FEEDPUMP; block_type=PUMP; specs=[NON-ENGLISH REDACTED] `0.6`，[NON-ENGLISH REDACTED] `0.9` Numeric table `[NON-ENGLISH REDACTED]` assigned to this block:
| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] 1 | [NON-ENGLISH REDACTED] 2 | [NON-ENGLISH REDACTED] 3 | [NON-ENGLISH REDACTED] 4 |
| --- | --- | --- | --- | --- |
| [NON-ENGLISH REDACTED] / (m3/h) | 20 | 10 | 5 | 3 |
| [NON-ENGLISH REDACTED] | 40 | 250 | 300 | 400 |
- name=FEED-MIX; block_type=HEATER; specs=Temperature 150℃, pressure 2.3 MPa.
- name=REACT; block_type=RSTOIC; specs=Temperature 200℃, pressure drop 0.1 MPa; reaction C6H6 + 3H2 -&gt; C6H12; benzene conversion 0.998.
- name=VFLOW; block_type=FSPLIT; specs=Fraction of stream H2RCY is 92%.
- name=LFLOW; block_type=FSPLIT; specs=Fraction of stream CHRCY is 30%.
- name=HP-SEP; block_type=FLASH2; specs=Temperature 50℃, pressure drop 0.05 MPa.
- name=COLUMN; block_type=RADFRAC; specs=12 theoretical stages; reflux ratio 1.2; feed on stage 8; column pressure 1.5 MPa; distillate rate 99 kmol/h; partial condenser with vapor distillate only.
- name=PIPE; block_type=PIPE; specs=Carbon steel; schedule 40; diameter 1 in; length 25 m.
- name=PUMP; block_type=PUMP; specs=[NON-ENGLISH REDACTED] `2.6 MPa`
- name=COMP; block_type=COMPR; specs=Isentropic compressor; pressure increase 0.4 MPa.
- name=VALVE; block_type=VALVE; specs=Outlet pressure 2 MPa; V810 equal percent flow globe valve; nominal diameter 1.5 in.

## Explicit Streams
- name=H2IN; kind=material; specs=Temperature 50℃, pressure 2.5 MPa, total flow 330 kmol/h; mole fractions H2 0.975, N2 0.005, CH4 0.02.
- name=BZIN; kind=material; specs=Temperature 40℃, pressure 0.1 MPa; pure benzene; flow 100 kmol/h.
- name=BZIN2; kind=material; specs=(none)
- name=H2RCY2; kind=material; specs=(none)
- name=RXIN; kind=material; specs=(none)
- name=RXOUT; kind=material; specs=(none)
- name=VAP; kind=material; specs=(none)
- name=H2RCY; kind=material; specs=(none)
- name=PURGE; kind=material; specs=(none)
- name=PURGE2; kind=material; specs=(none)
- name=LIQ; kind=material; specs=(none)
- name=COLFD; kind=material; specs=(none)
- name=CHRCY; kind=material; specs=(none)
- name=CHRCY2; kind=material; specs=(none)
- name=CHRCY3; kind=material; specs=(none)
- name=LTENDS; kind=material; specs=(none)
- name=PRODUCT; kind=material; specs=(none)

## Initial Plan Steps
- Create base Aspen session, components, property method, blocks, and figure topology; phase=workflow_build; blocks=[&#x27;FP&#x27;, &#x27;FM&#x27;, &#x27;R1&#x27;, &#x27;HS&#x27;, &#x27;VF&#x27;, &#x27;VALVE&#x27;, &#x27;CP&#x27;, &#x27;LF&#x27;, &#x27;PUMP&#x27;, &#x27;PIPE&#x27;, &#x27;CO&#x27;]; streams=[&#x27;B1&#x27;, &#x27;H1&#x27;, &#x27;B2&#x27;, &#x27;H3&#x27;, &#x27;R2&#x27;, &#x27;R3&#x27;, &#x27;V1&#x27;, &#x27;H4&#x27;, &#x27;P1&#x27;, &#x27;P2&#x27;, &#x27;L1&#x27;, &#x27;C3&#x27;, &#x27;C4&#x27;, &#x27;C5&#x27;, &#x27;C6&#x27;, &#x27;L3&#x27;, &#x27;P5&#x27;]
- Configure fresh feed material streams; phase=stream_variable_config; blocks=[]; streams=[&#x27;H1&#x27;, &#x27;B1&#x27;]
- Configure Pump blocks FEEDPUMP and PUMP; phase=block_variable_config; blocks=[&#x27;FP&#x27;, &#x27;PUMP&#x27;]; streams=[]
- Configure FEED-MIX Heater block; phase=block_variable_config; blocks=[&#x27;FM&#x27;]; streams=[]
- Configure RStoic core operating specs; phase=block_variable_config; blocks=[&#x27;R1&#x27;]; streams=[]
- Write RStoic stoichiometry rows; phase=block_variable_config; blocks=[&#x27;R1&#x27;]; streams=[]
- Apply RStoic conversion and selectivity metadata; phase=block_variable_config; blocks=[&#x27;R1&#x27;]; streams=[]
- Configure HP-SEP Flash2 block; phase=block_variable_config; blocks=[&#x27;HS&#x27;]; streams=[]
- Configure VFLOW and LFLOW FSplit blocks; phase=block_variable_config; blocks=[&#x27;VF&#x27;, &#x27;LF&#x27;]; streams=[]
- Configure COMP compressor block; phase=block_variable_config; blocks=[&#x27;CP&#x27;]; streams=[]
- Configure VALVE block; phase=block_variable_config; blocks=[&#x27;VALVE&#x27;]; streams=[]
- Configure PIPE block; phase=block_variable_config; blocks=[&#x27;PIPE&#x27;]; streams=[]
- Configure COLUMN RadFrac block; phase=block_variable_config; blocks=[&#x27;CO&#x27;]; streams=[]
- Complete missing required variables and verify readiness; phase=completion_repair; blocks=[&#x27;FP&#x27;, &#x27;FM&#x27;, &#x27;R1&#x27;, &#x27;HS&#x27;, &#x27;VF&#x27;, &#x27;VALVE&#x27;, &#x27;CP&#x27;, &#x27;LF&#x27;, &#x27;PUMP&#x27;, &#x27;PIPE&#x27;, &#x27;CO&#x27;]; streams=[&#x27;B1&#x27;, &#x27;H1&#x27;, &#x27;B2&#x27;, &#x27;H3&#x27;, &#x27;R2&#x27;, &#x27;R3&#x27;, &#x27;V1&#x27;, &#x27;H4&#x27;, &#x27;P1&#x27;, &#x27;P2&#x27;, &#x27;L1&#x27;, &#x27;C3&#x27;, &#x27;C4&#x27;, &#x27;C5&#x27;, &#x27;C6&#x27;, &#x27;L3&#x27;, &#x27;P5&#x27;]
- Solve flowsheet and report PRODUCT cyclohexane mole fraction; phase=analysis_tuning; blocks=[]; streams=[&#x27;P5&#x27;]

```

### FILE: experiments/script_agent_experiment/iter0_context_packs/v2/cases/chinese_5_1_radfrac/task_profile.json
Reason: LLM-selected task profile from task text
```text
{
  &quot;case_id&quot;: &quot;chinese_5_1_radfrac&quot;,
  &quot;task_profile_path&quot;: &quot;&quot;,
  &quot;task_markdown&quot;: &quot;tasks/test/chn/chapter_05/exercise_5_1.md&quot;,
  &quot;script_stem&quot;: &quot;chinese_5_1&quot;,
  &quot;baseline_script&quot;: &quot;tool_side_generation/healthcheck/full_evaluation/chinese_5_1.py&quot;,
  &quot;notes&quot;: &quot;Cyclohexane production flowsheet (Chi-5.1 BKP); chapter 5 skill applies.&quot;,
  &quot;gate_contract_path&quot;: &quot;experiments/script_agent_experiment/generated_context/chinese_5_1_radfrac_gate_contract.json&quot;,
  &quot;forbidden_paths&quot;: [
    &quot;tool_side_generation/healthcheck/full_evaluation/chinese_5_1.py&quot;,
    &quot;tool_side_generation/healthcheck/full_evaluation/&quot;,
    &quot;tool_side_generation/healthcheck/full_example/homework/&quot;,
    &quot;chinese_5_1_agent_generated.py&quot;,
    &quot;chinese_5_1_fresh_gpt54.py&quot;,
    &quot;chinese_5_1_own_agent.py&quot;
  ],
  &quot;block_families&quot;: [
    &quot;PROPERTY_METHODS&quot;,
    &quot;HEATER&quot;,
    &quot;RSTOIC&quot;,
    &quot;FLASH2&quot;,
    &quot;FSPLIT&quot;,
    &quot;RADFRAC&quot;,
    &quot;PUMP&quot;,
    &quot;COMPR&quot;,
    &quot;PIPE&quot;,
    &quot;VALVE&quot;
  ],
  &quot;planning_validator_families&quot;: [
    &quot;PROPERTY_METHODS&quot;,
    &quot;HEATER&quot;,
    &quot;RSTOIC&quot;,
    &quot;FLASH2&quot;,
    &quot;FSPLIT&quot;,
    &quot;RADFRAC&quot;,
    &quot;PUMP&quot;,
    &quot;COMPR&quot;,
    &quot;PIPE&quot;,
    &quot;VALVE&quot;
  ],
  &quot;surface_docs&quot;: [
    &quot;docs/hardcoded_script_plan/block_type_inject/property_methods.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/heater.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/rstoic.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/flash2.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/fsplit.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/radfrac.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/pump.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/compr.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/pipe.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/valve.md&quot;
  ],
  &quot;skill_names&quot;: [
    &quot;aspen-task-execution-order&quot;,
    &quot;aspen-property-method-selection&quot;,
    &quot;aspen-material-stream-composition-must-be-specified&quot;,
    &quot;functional-role-semantics-validation&quot;,
    &quot;aspen-generic-readbacks&quot;,
    &quot;reactor-reaction-setup-high-level&quot;,
    &quot;sequential-reaction-topology&quot;,
    &quot;native-reactor-module-comparison&quot;,
    &quot;flash-control-chain&quot;,
    &quot;prefer-direct-component-splits&quot;,
    &quot;shared-material-port-topology&quot;,
    &quot;radfrac-absorber-like-configuration&quot;,
    &quot;radfrac-standard-column-pressure-basis&quot;,
    &quot;aspen-completion-error-hints&quot;,
    &quot;aspen-component-radfrac-evidence-repair&quot;,
    &quot;aspen-pump-outlet-specification&quot;,
    &quot;compr-analysis-variable-selection&quot;,
    &quot;aspen-custom-unit-set&quot;,
    &quot;solvent-recycle-closure-semantics&quot;,
    &quot;radfrac-extractive-distillation-solvent&quot;,
    &quot;optimization-constrained-feed-and-recycle-evidence&quot;,
    &quot;split-handoff-inheritance-boundary&quot;,
    &quot;rep-derived-metric-consistency&quot;
  ],
  &quot;requires_design_spec_chain&quot;: false,
  &quot;validator_gates&quot;: [
    &quot;hard_metrics_contract&quot;,
    &quot;recycle_topology&quot;
  ],
  &quot;task_semantics&quot;: {
    &quot;source&quot;: &quot;LLM task profile&quot;,
    &quot;validator_policy&quot;: {
      &quot;allow_equivalent_model&quot;: false,
      &quot;allow_equivalent_column_model&quot;: false,
      &quot;stagewise_column_required&quot;: true,
      &quot;external_blackbox_optimization_ok&quot;: false,
      &quot;native_analysis_required_kinds&quot;: [],
      &quot;native_analysis_optional_kinds&quot;: [],
      &quot;design_spec_target_kind&quot;: &quot;none&quot;,
      &quot;workflow_gates&quot;: [],
      &quot;family_validators&quot;: [],
      &quot;reactor_module_families&quot;: []
    },
    &quot;uncertainties&quot;: [
      &quot;The figure shows FEED-MIX as the single visible convergence/feed-conditioning node, while the written task specifies it as a Heater module; the topology should preserve one visible FEED-MIX node rather than silently splitting it into a separate mixer and heater.&quot;,
      &quot;The figure itself does not show the COLUMN condenser/reboiler details; the partial condenser with vapor distillate and the stated RadFrac operating specifications come from the written task.&quot;,
      &quot;The pump characteristic curve table heading does not name a specific module even though two pump-class modules are present; dataset attachment follows the supplied table-attachment rule rather than relying on proximity, subtype wording, or the block label PUMP.&quot;,
      &quot;The visible figure contains only solid material streams and no dashed heat, work, or power streams.&quot;
    ],
    &quot;dataset_attachments&quot;: [
      {
        &quot;heading&quot;: &quot;[NON-ENGLISH REDACTED]&quot;,
        &quot;block&quot;: &quot;FEEDPUMP&quot;,
        &quot;excluded_blocks&quot;: [
          &quot;PUMP&quot;
        ]
      }
    ],
    &quot;figure_context_used&quot;: true,
    &quot;figure_image_references&quot;: [
      &quot;./images/exercise_5_1_flow.png&quot;
    ],
    &quot;figure_resolved_image_paths&quot;: [
      &quot;tasks/test/chn/chapter_05/images/exercise_5_1_flow.png&quot;
    ]
  }
}
```

### FILE: experiments/script_agent_experiment/generated_context/chinese_5_1_radfrac_gate_contract.json
Reason: LLM-selected validation gate contract from task text
```text
{
  &quot;case_id&quot;: &quot;chinese_5_1_radfrac&quot;,
  &quot;required_gates&quot;: [
    {
      &quot;kind&quot;: &quot;property_method_contract&quot;,
      &quot;required&quot;: false,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED] RK-SOAVE；[NON-ENGLISH REDACTED] Aspen Plus [NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;Aspen Properties/Setup readback shows global property method RK-SOAVE.&quot;,
        &quot;Final reported PRODUCT composition is from a run using RK-SOAVE, not from a different method or hand calculation.&quot;
      ],
      &quot;scoring_only&quot;: true
    },
    {
      &quot;kind&quot;: &quot;recycle_topology&quot;,
      &quot;required&quot;: true,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;The task requires physical material recycle return paths; accounting-only declarations cannot replace those connections.&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;Final live material-port/stream readbacks prove every task-stated recycle return path reaches its upstream process unit, including task/figure intermediate equipment and branch splits.&quot;,
        &quot;Final same-run Aspen results prove the physically connected recycle loops converged and participated in the reported product result; a declared recovery or makeup balance alone is insufficient.&quot;,
        &quot;Recycle identities, destinations, and split specifications follow the authoritative task and figure, not recycled gate prose or inherited solution values.&quot;
      ],
      &quot;closure_semantics&quot;: {
        &quot;closure_type&quot;: &quot;numerical_recycle_tear&quot;,
        &quot;accepted_topology&quot;: &quot;task-stated physical material return paths into upstream process units&quot;,
        &quot;physical_recycle_required&quot;: true
      }
    },
    {
      &quot;kind&quot;: &quot;reaction_separator_splitter_contract&quot;,
      &quot;required&quot;: true,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED]、Rstoic [NON-ENGLISH REDACTED]、Flash2 [NON-ENGLISH REDACTED] FSplit [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;REACT is implemented as an Rstoic block or Aspen-equivalent stoichiometric reactor for C6H6 + 3 H2 -&gt; C6H12.&quot;,
        &quot;REACT has temperature 200 °C, pressure drop 0.1 MPa, and benzene conversion 0.998.&quot;,
        &quot;HP-SEP is implemented as Flash2 with temperature 50 °C and pressure drop 0.05 MPa.&quot;,
        &quot;VFLOW is an FSplit or equivalent vapor splitter with H2RCY split fraction 0.92 of VAP.&quot;,
        &quot;LFLOW is an FSplit or equivalent liquid splitter with CHRCY split fraction 0.30 of LIQ.&quot;,
        &quot;Final stream readbacks confirm VAP and LIQ originate from HP-SEP and feed the specified splitters.&quot;
      ]
    },
    {
      &quot;kind&quot;: &quot;stagewise_column&quot;,
      &quot;required&quot;: true,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED] COLUMN；[NON-ENGLISH REDACTED] COLUMN [NON-ENGLISH REDACTED] RadFrac，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;COLUMN is a RadFrac block or Aspen native rigorous column block with 12 theoretical stages.&quot;,
        &quot;COLFD feeds stage 8.&quot;,
        &quot;Column pressure is 1.5 MPa.&quot;,
        &quot;Reflux ratio is 1.2.&quot;,
        &quot;Distillate withdrawal rate is 99 kmol/h.&quot;,
        &quot;Condenser is a partial condenser with vapor-only distillate/light-end withdrawal, consistent with LTENDS as light-end outlet and PRODUCT as product outlet.&quot;,
        &quot;Final Aspen stream readbacks identify which column outlet is PRODUCT and provide its composition.&quot;
      ]
    },
    {
      &quot;kind&quot;: &quot;pressure_transform_unit_fidelity&quot;,
      &quot;required&quot;: true,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] FEEDPUMP、PUMP、COMP、VALVE、PIPE [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] recycle [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;FEEDPUMP is located only on the fresh benzene branch BZIN -&gt; FEEDPUMP -&gt; BZIN2.&quot;,
        &quot;Recycle liquid PUMP is located only on CHRCY -&gt; PUMP -&gt; CHRCY2 and uses fixed outlet pressure 2.6 MPa.&quot;,
        &quot;COMP is located on H2RCY -&gt; COMP -&gt; H2RCY2 and uses isentropic compressor semantics with pressure increase 0.4 MPa.&quot;,
        &quot;VALVE is located on PURGE -&gt; VALVE -&gt; PURGE2 and has outlet pressure 2 MPa with V810 equal-percent globe valve, nominal diameter 1.5 in.&quot;,
        &quot;PIPE is located on CHRCY2 -&gt; PIPE -&gt; CHRCY3 and has carbon steel, schedule 40, diameter 1 in, length 25 m.&quot;,
        &quot;Final Aspen block and stream readbacks confirm pressure changes on each pressure-transform unit from calculated outlet streams, not merely configured helper values.&quot;
      ]
    },
    {
      &quot;kind&quot;: &quot;pump_curve_fidelity&quot;,
      &quot;required&quot;: true,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED] FEEDPUMP，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] PUMP。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;FEEDPUMP actual specification mode/readback shows pump-curve mode active after all inputs are written.&quot;,
        &quot;FEEDPUMP pump efficiency is 0.6 and driver efficiency is 0.9.&quot;,
        &quot;FEEDPUMP curve table contains flow entries 20, 10, 5, 3 m3/h.&quot;,
        &quot;FEEDPUMP curve table contains corresponding head entries 40, 250, 300, 400 after explicitly documented unit interpretation and conversion into Aspen-native curve units.&quot;,
        &quot;FEEDPUMP outlet state is Aspen-calculated from the curve and actual flow; evidence does not replace it with downstream FEED-MIX pressure 2.3 MPa or a fixed pump outlet pressure.&quot;,
        &quot;PUMP on the CHRCY recycle branch has no copied FEEDPUMP curve and instead uses fixed outlet pressure 2.6 MPa.&quot;,
        &quot;Readbacks show FEEDPUMP connects BZIN -&gt; BZIN2 and PUMP connects CHRCY -&gt; CHRCY2.&quot;
      ]
    },
    {
      &quot;kind&quot;: &quot;result_path_no_surrogate&quot;,
      &quot;required&quot;: true,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] Aspen Plus [NON-ENGLISH REDACTED] PRODUCT [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;Final run status is converged with recycle closure.&quot;,
        &quot;Reported value is read from Aspen results for stream PRODUCT, component C6H12/cyclohexane, mole-fraction basis.&quot;,
        &quot;Evidence includes Aspen result path or tabular readback identifying stream PRODUCT and component cyclohexane.&quot;,
        &quot;No direct input specification fixes PRODUCT cyclohexane mole fraction to the reported value.&quot;,
        &quot;No hand stoichiometric calculation, feed composition, reactor conversion alone, or column input specification is used as the final answer.&quot;
      ]
    },
    {
      &quot;kind&quot;: &quot;convergence_and_rep_evidence&quot;,
      &quot;required&quot;: false,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;Aspen run status indicates successful completion/convergence.&quot;,
        &quot;Recycle tear streams, if any, are converged within Aspen tolerances.&quot;,
        &quot;No required block reports fatal errors or unexecuted status.&quot;,
        &quot;PRODUCT stream flow and composition are available in final results.&quot;
      ],
      &quot;scoring_only&quot;: true
    }
  ],
  &quot;optional_fidelity_gates&quot;: [
    {
      &quot;kind&quot;: &quot;component_material_balance&quot;,
      &quot;required&quot;: false,
      &quot;scoring_only&quot;: true,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] PRODUCT [NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;Report component molar flow table for BZIN, H2IN, RXIN, RXOUT, VAP, LIQ, COLFD, LTENDS, PRODUCT, H2RCY2, and CHRCY3.&quot;,
        &quot;Show benzene consumption and cyclohexane formation are consistent with Rstoic conversion within simulation tolerance.&quot;
      ]
    },
    {
      &quot;kind&quot;: &quot;pressure_profile_report&quot;,
      &quot;required&quot;: false,
      &quot;scoring_only&quot;: true,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;Report inlet/outlet pressures for FEEDPUMP, FEED-MIX, REACT, HP-SEP, COMP, VALVE, PUMP, PIPE, COLUMN, and associated streams.&quot;,
        &quot;Highlight pressure changes caused by pump curve, fixed-pressure pump, compressor pressure increment, valve outlet pressure, pipe pressure behavior, and separator/reactor pressure drops.&quot;
      ]
    },
    {
      &quot;kind&quot;: &quot;composition_basis_writeup&quot;,
      &quot;required&quot;: false,
      &quot;scoring_only&quot;: true,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED] PRODUCT [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;State that the reported cyclohexane value is the raw full-stream mole fraction in PRODUCT unless an explicitly separate normalized diagnostic is also shown.&quot;,
        &quot;Identify Aspen stream-result table, component ID, and mole-fraction basis used.&quot;
      ]
    },
    {
      &quot;kind&quot;: &quot;property_method_contract&quot;,
      &quot;required&quot;: false,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED] RK-SOAVE；[NON-ENGLISH REDACTED] Aspen Plus [NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;Aspen Properties/Setup readback shows global property method RK-SOAVE.&quot;,
        &quot;Final reported PRODUCT composition is from a run using RK-SOAVE, not from a different method or hand calculation.&quot;
      ],
      &quot;scoring_only&quot;: true
    },
    {
      &quot;kind&quot;: &quot;convergence_and_rep_evidence&quot;,
      &quot;required&quot;: false,
      &quot;allowed_surrogate&quot;: false,
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]。&quot;,
      &quot;deterministic_evidence&quot;: [
        &quot;Aspen run status indicates successful completion/convergence.&quot;,
        &quot;Recycle tear streams, if any, are converged within Aspen tolerances.&quot;,
        &quot;No required block reports fatal errors or unexecuted status.&quot;,
        &quot;PRODUCT stream flow and composition are available in final results.&quot;
      ],
      &quot;scoring_only&quot;: true
    }
  ],
  &quot;required_analysis_objects&quot;: [],
  &quot;optional_analysis_objects&quot;: [],
  &quot;analysis_object_adjudication&quot;: {
    &quot;mode&quot;: &quot;llm_soft_judgment&quot;,
    &quot;native_required_kinds&quot;: [],
    &quot;optional_bonus_kinds&quot;: [],
    &quot;not_required_kinds&quot;: [
      {
        &quot;kind&quot;: &quot;design_spec&quot;,
        &quot;why_not_required&quot;: &quot;[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] PRODUCT [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] Aspen Design Spec [NON-ENGLISH REDACTED]。&quot;,
        &quot;confidence&quot;: &quot;high&quot;
      },
      {
        &quot;kind&quot;: &quot;sensitivity&quot;,
        &quot;why_not_required&quot;: &quot;[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] Aspen Sensitivity [NON-ENGLISH REDACTED]。&quot;,
        &quot;confidence&quot;: &quot;high&quot;
      },
      {
        &quot;kind&quot;: &quot;optimization&quot;,
        &quot;why_not_required&quot;: &quot;[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] Aspen Optimization；[NON-ENGLISH REDACTED]。&quot;,
        &quot;confidence&quot;: &quot;high&quot;
      }
    ],
    &quot;review_needed&quot;: false,
    &quot;review_reason&quot;: &quot;[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。&quot;
  },
  &quot;result_path_requirements&quot;: [
    {
      &quot;result&quot;: &quot;PRODUCT stream cyclohexane mole fraction&quot;,
      &quot;must_derive_from&quot;: [
        &quot;Converged Aspen Plus results&quot;,
        &quot;Stream PRODUCT composition table&quot;,
        &quot;Component cyclohexane/C6H12 mole fraction&quot;,
        &quot;Full flowsheet containing FEEDPUMP, FEED-MIX, REACT, HP-SEP, VFLOW, COMP, VALVE, LFLOW, PUMP, PIPE, and COLUMN&quot;,
        &quot;Closed gas recycle H2RCY/H2RCY2 and liquid recycle CHRCY/CHRCY2/CHRCY3&quot;,
        &quot;RK-SOAVE property method&quot;
      ],
      &quot;forbid_sources&quot;: [
        &quot;Feed composition alone&quot;,
        &quot;Stoichiometric hand calculation from 99.8% benzene conversion&quot;,
        &quot;Assumed pure cyclohexane product&quot;,
        &quot;Column distillate rate or reflux ratio used as a proxy for product composition&quot;,
        &quot;Any direct PRODUCT composition input specification&quot;,
        &quot;Unconverged or open-loop flowsheet results&quot;
      ],
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] RadFrac [NON-ENGLISH REDACTED]。&quot;
    },
    {
      &quot;result&quot;: &quot;FEEDPUMP outlet state and pressure contribution to BZIN2&quot;,
      &quot;must_derive_from&quot;: [
        &quot;FEEDPUMP active pump-curve mode&quot;,
        &quot;Actual BZIN flow through FEEDPUMP&quot;,
        &quot;Pump curve flow/head table with documented head-unit interpretation and conversion&quot;,
        &quot;FEEDPUMP efficiency and driver efficiency readbacks&quot;,
        &quot;Final BZIN2 stream readback&quot;
      ],
      &quot;forbid_sources&quot;: [
        &quot;Directly setting FEEDPUMP fixed outlet pressure&quot;,
        &quot;Using FEED-MIX pressure 2.3 MPa as FEEDPUMP outlet pressure&quot;,
        &quot;Copying the curve to recycle PUMP instead of FEEDPUMP&quot;,
        &quot;Using the raw head numbers in an SI curve table without unit conversion documentation&quot;
      ],
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED] FEEDPUMP [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。&quot;
    },
    {
      &quot;result&quot;: &quot;Recycle-closed PRODUCT composition&quot;,
      &quot;must_derive_from&quot;: [
        &quot;Aspen converged recycle solution&quot;,
        &quot;H2 recycle from VFLOW through COMP back to FEED-MIX&quot;,
        &quot;Liquid recycle from LFLOW through PUMP and PIPE back to FEED-MIX&quot;
      ],
      &quot;forbid_sources&quot;: [
        &quot;Single-pass reactor/separator calculation without recycles&quot;,
        &quot;Disconnected recycle streams with guessed makeup values&quot;,
        &quot;Manual iteration not reflected in final Aspen results&quot;
      ],
      &quot;why&quot;: &quot;[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。&quot;
    }
  ],
  &quot;numeric_acceptance_metrics&quot;: [
    {
      &quot;metric&quot;: &quot;H2IN temperature&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 50,
      &quot;unit&quot;: &quot;degC&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] H2IN：[NON-ENGLISH REDACTED] 50℃。&quot;
    },
    {
      &quot;metric&quot;: &quot;H2IN pressure&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 2.5,
      &quot;unit&quot;: &quot;MPa&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] H2IN：[NON-ENGLISH REDACTED] 2.5 MPa。&quot;
    },
    {
      &quot;metric&quot;: &quot;H2IN total molar flow&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 330,
      &quot;unit&quot;: &quot;kmol/h&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] H2IN：[NON-ENGLISH REDACTED] 330 kmol/h。&quot;
    },
    {
      &quot;metric&quot;: &quot;H2IN mole fractions&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: &quot;H2 0.975, N2 0.005, CH4 0.02&quot;,
      &quot;unit&quot;: &quot;mole fraction&quot;,
      &quot;evidence&quot;: &quot;H2、N2、CH4 [NON-ENGLISH REDACTED] 0.975、0.005 [NON-ENGLISH REDACTED] 0.02。&quot;
    },
    {
      &quot;metric&quot;: &quot;BZIN temperature&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 40,
      &quot;unit&quot;: &quot;degC&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] BZIN：[NON-ENGLISH REDACTED] 40℃。&quot;
    },
    {
      &quot;metric&quot;: &quot;BZIN pressure&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 0.1,
      &quot;unit&quot;: &quot;MPa&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] BZIN：[NON-ENGLISH REDACTED] 0.1 MPa。&quot;
    },
    {
      &quot;metric&quot;: &quot;BZIN molar flow&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 100,
      &quot;unit&quot;: &quot;kmol/h&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] BZIN：[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] 100 kmol/h。&quot;
    },
    {
      &quot;metric&quot;: &quot;BZIN composition&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: &quot;pure benzene&quot;,
      &quot;unit&quot;: &quot;component basis&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] BZIN：[NON-ENGLISH REDACTED]。&quot;
    },
    {
      &quot;metric&quot;: &quot;FEED-MIX temperature&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 150,
      &quot;unit&quot;: &quot;degC&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] FEED-MIX（Heater [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 150℃。&quot;
    },
    {
      &quot;metric&quot;: &quot;FEED-MIX pressure&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 2.3,
      &quot;unit&quot;: &quot;MPa&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] FEED-MIX（Heater [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 2.3 MPa。&quot;
    },
    {
      &quot;metric&quot;: &quot;REACT temperature&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 200,
      &quot;unit&quot;: &quot;degC&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] REACT（Rstoic [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 200℃。&quot;
    },
    {
      &quot;metric&quot;: &quot;REACT pressure drop&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 0.1,
      &quot;unit&quot;: &quot;MPa&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] REACT（Rstoic [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 0.1 MPa。&quot;
    },
    {
      &quot;metric&quot;: &quot;Benzene conversion in REACT&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 0.998,
      &quot;unit&quot;: &quot;fraction&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] 99.8%；REACT [NON-ENGLISH REDACTED] 0.998。&quot;
    },
    {
      &quot;metric&quot;: &quot;VFLOW H2RCY split fraction&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 0.92,
      &quot;unit&quot;: &quot;fraction of VAP&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] VFLOW（FSplit [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] H2RCY [NON-ENGLISH REDACTED] 92%。&quot;
    },
    {
      &quot;metric&quot;: &quot;LFLOW CHRCY split fraction&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 0.3,
      &quot;unit&quot;: &quot;fraction of LIQ&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] LFLOW（FSplit [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] CHRCY [NON-ENGLISH REDACTED] 30%。&quot;
    },
    {
      &quot;metric&quot;: &quot;HP-SEP temperature&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 50,
      &quot;unit&quot;: &quot;degC&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] HP-SEP（Flash2 [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 50℃。&quot;
    },
    {
      &quot;metric&quot;: &quot;HP-SEP pressure drop&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 0.05,
      &quot;unit&quot;: &quot;MPa&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] HP-SEP（Flash2 [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 0.05 MPa。&quot;
    },
    {
      &quot;metric&quot;: &quot;COLUMN theoretical stages&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 12,
      &quot;unit&quot;: &quot;stages&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] COLUMN（RadFrac [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 12。&quot;
    },
    {
      &quot;metric&quot;: &quot;COLUMN reflux ratio&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 1.2,
      &quot;unit&quot;: &quot;dimensionless&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] COLUMN（RadFrac [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 1.2。&quot;
    },
    {
      &quot;metric&quot;: &quot;COLUMN feed stage&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 8,
      &quot;unit&quot;: &quot;stage number&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] COLUMN（RadFrac [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 8 [NON-ENGLISH REDACTED]。&quot;
    },
    {
      &quot;metric&quot;: &quot;COLUMN pressure&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 1.5,
      &quot;unit&quot;: &quot;MPa&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] COLUMN（RadFrac [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 1.5 MPa。&quot;
    },
    {
      &quot;metric&quot;: &quot;COLUMN distillate withdrawal rate&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 99,
      &quot;unit&quot;: &quot;kmol/h&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] COLUMN（RadFrac [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 99 kmol/h。&quot;
    },
    {
      &quot;metric&quot;: &quot;COLUMN condenser type&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: &quot;partial condenser with vapor-only distillate withdrawal&quot;,
      &quot;unit&quot;: &quot;configuration&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED]。&quot;
    },
    {
      &quot;metric&quot;: &quot;FEEDPUMP pump efficiency&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 0.6,
      &quot;unit&quot;: &quot;fraction&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] FEEDPUMP：[NON-ENGLISH REDACTED] 0.6；[NON-ENGLISH REDACTED] FEEDPUMP [NON-ENGLISH REDACTED] 0.6。&quot;
    },
    {
      &quot;metric&quot;: &quot;FEEDPUMP driver efficiency&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 0.9,
      &quot;unit&quot;: &quot;fraction&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] FEEDPUMP：[NON-ENGLISH REDACTED] 0.9。&quot;
    },
    {
      &quot;metric&quot;: &quot;FEEDPUMP curve flow points&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: &quot;20, 10, 5, 3&quot;,
      &quot;unit&quot;: &quot;m3/h&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] / (m3/h) [NON-ENGLISH REDACTED] 20、10、5、3。&quot;
    },
    {
      &quot;metric&quot;: &quot;FEEDPUMP curve head points&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: &quot;40, 250, 300, 400 with documented unit interpretation and Aspen-native conversion&quot;,
      &quot;unit&quot;: &quot;head units unspecified in source&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] 40、250、300、400；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]。&quot;
    },
    {
      &quot;metric&quot;: &quot;Recycle liquid PUMP outlet pressure&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 2.6,
      &quot;unit&quot;: &quot;MPa&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] PUMP（Pump HI）：[NON-ENGLISH REDACTED] 2.6 MPa。&quot;
    },
    {
      &quot;metric&quot;: &quot;COMP pressure increase&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 0.4,
      &quot;unit&quot;: &quot;MPa&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] COMP（Compr [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] 0.4 MPa。&quot;
    },
    {
      &quot;metric&quot;: &quot;VALVE outlet pressure&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 2,
      &quot;unit&quot;: &quot;MPa&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] VALVE（Valve [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 2 MPa。&quot;
    },
    {
      &quot;metric&quot;: &quot;VALVE specification&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: &quot;V810 equal percent flow globe valve, nominal diameter 1.5 in&quot;,
      &quot;unit&quot;: &quot;valve configuration&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] V810 equal percent flow [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] 1.5 in。&quot;
    },
    {
      &quot;metric&quot;: &quot;PIPE material&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: &quot;carbon steel&quot;,
      &quot;unit&quot;: &quot;material&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] PIPE（Pipe [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED]。&quot;
    },
    {
      &quot;metric&quot;: &quot;PIPE schedule&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 40,
      &quot;unit&quot;: &quot;schedule number&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] PIPE（Pipe [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 40。&quot;
    },
    {
      &quot;metric&quot;: &quot;PIPE diameter&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 1,
      &quot;unit&quot;: &quot;in&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] PIPE（Pipe [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 1 in。&quot;
    },
    {
      &quot;metric&quot;: &quot;PIPE length&quot;,
      &quot;operator&quot;: &quot;=&quot;,
      &quot;value&quot;: 25,
      &quot;unit&quot;: &quot;m&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED] PIPE（Pipe [NON-ENGLISH REDACTED]）：[NON-ENGLISH REDACTED] 25 m。&quot;
    },
    {
      &quot;metric&quot;: &quot;PRODUCT cyclohexane mole fraction&quot;,
      &quot;operator&quot;: &quot;report&quot;,
      &quot;value&quot;: &quot;Aspen-calculated value&quot;,
      &quot;unit&quot;: &quot;mole fraction&quot;,
      &quot;evidence&quot;: &quot;[NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED]。&quot;
    }
  ],
  &quot;component_role_contract&quot;: {
    &quot;feed_components&quot;: [
      {
        &quot;name&quot;: &quot;benzene / C6H6&quot;,
        &quot;role&quot;: &quot;fresh reactant feed in BZIN; hydrogenation reactant converted in REACT&quot;,
        &quot;source_text&quot;: &quot;[NON-ENGLISH REDACTED] BZIN：[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] 100 kmol/h；[NON-ENGLISH REDACTED] C6H6 + 3H2 -&gt; C6H12。&quot;
      },
      {
        &quot;name&quot;: &quot;hydrogen / H2&quot;,
        &quot;role&quot;: &quot;fresh reactant feed in H2IN and main gas recycle component&quot;,
        &quot;source_text&quot;: &quot;[NON-ENGLISH REDACTED] H2IN：H2 [NON-ENGLISH REDACTED] 0.975；[NON-ENGLISH REDACTED] H2；[NON-ENGLISH REDACTED]。&quot;
      },
      {
        &quot;name&quot;: &quot;nitrogen / N2&quot;,
        &quot;role&quot;: &quot;inert/light-gas component in H2IN&quot;,
        &quot;source_text&quot;: &quot;[NON-ENGLISH REDACTED] H2IN：N2 [NON-ENGLISH REDACTED] 0.005。&quot;
      },
      {
        &quot;name&quot;: &quot;methane / CH4&quot;,
        &quot;role&quot;: &quot;inert/light-gas component in H2IN&quot;,
        &quot;source_text&quot;: &quot;[NON-ENGLISH REDACTED] H2IN：CH4 [NON-ENGLISH REDACTED] 0.02。&quot;
      }
    ],
    &quot;product_components&quot;: [
      {
        &quot;name&quot;: &quot;cyclohexane / C6H12&quot;,
        &quot;role&quot;: &quot;desired product component whose mole fraction in PRODUCT is the requested result&quot;,
        &quot;source_text&quot;: &quot;[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED]。&quot;
      }
    ],
    &quot;solvents_or_auxiliaries&quot;: [],
    &quot;recycle_components&quot;: [
      {
        &quot;name&quot;: &quot;hydrogen / H2&quot;,
        &quot;role&quot;: &quot;gas recycle component in H2RCY/H2RCY2 returned to FEED-MIX/reactor feed&quot;,
        &quot;source_text&quot;: &quot;[NON-ENGLISH REDACTED]；VFLOW [NON-ENGLISH REDACTED] H2RCY [NON-ENGLISH REDACTED] 92%。&quot;
      },
      {
        &quot;name&quot;: &quot;cyclohexane / C6H12&quot;,
        &quot;role&quot;: &quot;liquid recycle component in CHRCY/CHRCY2/CHRCY3 used to help control reactor temperature&quot;,
        &quot;source_text&quot;: &quot;[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]；LFLOW [NON-ENGLISH REDACTED] CHRCY [NON-ENGLISH REDACTED] 30%。&quot;
      },
      {
        &quot;name&quot;: &quot;light gases&quot;,
        &quot;role&quot;: &quot;may be present in vapor recycle/purge and are separated in HP-SEP/COLUMN&quot;,
        &quot;source_text&quot;: &quot;[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。&quot;
      }
    ],
    &quot;semantic_conflicts&quot;: []
  },
  &quot;immutability_classification&quot;: {
    &quot;immutable_task_specs&quot;: [
      &quot;Component set includes benzene/C6H6, hydrogen/H2, nitrogen/N2, methane/CH4, and cyclohexane/C6H12.&quot;,
      &quot;Reaction is C6H6 + 3H2 -&gt; C6H12.&quot;,
      &quot;Property method is RK-SOAVE.&quot;,
      &quot;H2IN conditions: 50 °C, 2.5 MPa, 330 kmol/h, mole fractions H2 0.975, N2 0.005, CH4 0.02.&quot;,
      &quot;BZIN conditions: 40 °C, 0.1 MPa, pure benzene, 100 kmol/h.&quot;,
      &quot;FEED-MIX is specified as Heater module with 150 °C and 2.3 MPa.&quot;,
      &quot;REACT is specified as Rstoic with 200 °C, 0.1 MPa pressure drop, benzene conversion 0.998.&quot;,
      &quot;HP-SEP is specified as Flash2 with 50 °C and 0.05 MPa pressure drop.&quot;,
      &quot;VFLOW is specified as FSplit with H2RCY fraction 92%.&quot;,
      &quot;LFLOW is specified as FSplit with CHRCY fraction 30%.&quot;,
      &quot;COLUMN is specified as RadFrac with 12 theoretical stages, reflux ratio 1.2, feed stage 8, pressure 1.5 MPa, distillate withdrawal rate 99 kmol/h, and partial condenser with vapor-only distillate withdrawal.&quot;,
      &quot;FEEDPUMP belongs to BZIN -&gt; FEEDPUMP -&gt; BZIN2 fresh benzene branch and must use pump-curve mode.&quot;,
      &quot;FEEDPUMP pump efficiency is 0.6 and driver efficiency is 0.9.&quot;,
      &quot;FEEDPUMP curve flow points are 20, 10, 5, 3 m3/h and head entries are 40, 250, 300, 400 with explicit unit interpretation before Aspen entry.&quot;,
      &quot;Recycle liquid PUMP belongs to CHRCY branch and uses fixed outlet pressure 2.6 MPa; the FEEDPUMP curve must not be assigned to it.&quot;,
      &quot;COMP is an isentropic compressor with pressure increase 0.4 MPa.&quot;,
      &quot;VALVE outlet pressure is 2 MPa with V810 equal percent flow globe valve, nominal diameter 1.5 in.&quot;,
      &quot;PIPE is carbon steel, schedule 40, diameter 1 in, length 25 m.&quot;,
      &quot;Visible topology and stream labels from the figure: FEEDPUMP, FEED-MIX, REACT, HP-SEP, VFLOW, VALVE, COMP, LFLOW, PUMP, PIPE, COLUMN; streams BZIN, BZIN2, H2IN, H2RCY, H2RCY2, RXIN, RXOUT, VAP, PURGE, PURGE2, LIQ, COLFD, PRODUCT, LTENDS, CHRCY, CHRCY2, CHRCY3.&quot;,
      &quot;Requested result is PRODUCT stream cyclohexane mole fraction.&quot;
    ],
    &quot;provisional_model_assumptions&quot;: [
      &quot;Interpretation of the pump-curve head unit is not specified by the source text and must be explicitly documented before conversion to Aspen-native curve units.&quot;,
      &quot;Aspen component databank IDs and aliases for benzene, hydrogen, nitrogen, methane, and cyclohexane may be chosen by the modeler if chemically unambiguous.&quot;,
      &quot;Numerical convergence settings, tear-stream initial guesses, and recycle initialization values are modeler choices.&quot;,
      &quot;If Aspen requires additional RadFrac condenser/reboiler options not specified beyond the given condenser, reflux ratio, stages, pressure, feed stage, and distillate rate, those detailed settings are modeler assumptions consistent with the task.&quot;,
      &quot;If block aliases are used, they must preserve branch ownership and topology even if IDs differ from the task labels.&quot;
    ],
    &quot;exploration_dimensions&quot;: [
      &quot;Recycle tear stream selection and initial estimates may be varied to obtain convergence.&quot;,
      &quot;Numerical solver methods and tolerances may be adjusted without changing task specifications.&quot;,
      &quot;Documented pump-head unit interpretation can be checked for consistency, but raw curve ownership and flow/head data cannot be reassigned.&quot;,
      &quot;Aspen implementation details for pressure-drop calculations in PIPE may be adjusted only within the specified material, schedule, diameter, and length constraints.&quot;,
      &quot;RadFrac numerical initialization may be varied while preserving all specified column conditions.&quot;
    ],
    &quot;classification_notes&quot;: [
      &quot;The pump curve is immutable in branch assignment and data values, but its unspecified head unit creates a required documented interpretation rather than a free numerical target.&quot;,
      &quot;The task does not provide an expected numeric cyclohexane mole fraction; the accepted result is a reported Aspen output value with proper evidence path.&quot;,
      &quot;Figure-derived topology is authoritative for visible stream connections and confirms that FEEDPUMP and PUMP are distinct devices on different branches.&quot;
    ]
  },
  &quot;uncertainties&quot;: [
    &quot;The pump-curve head unit is not stated; validation must require an explicit unit interpretation and conversion before Aspen entry.&quot;,
    &quot;The task states COLUMN distillate withdrawal rate 99 kmol/h and a partial condenser with vapor-only distillate withdrawal; the final model must clearly map LTENDS and PRODUCT to RadFrac outlets and show PRODUCT is the requested product stream.&quot;,
    &quot;The figure contains no numeric conditions; numeric specifications come from the written task text.&quot;,
    &quot;The PRODUCT cyclohexane mole fraction has no target numeric value in the task and must be reported from final Aspen results rather than compared to a preset acceptance number.&quot;
  ],
  &quot;figure_context_used&quot;: true,
  &quot;figure_image_references&quot;: [
    &quot;./images/exercise_5_1_flow.png&quot;
  ],
  &quot;figure_resolved_image_paths&quot;: [
    &quot;tasks/test/chn/chapter_05/images/exercise_5_1_flow.png&quot;
  ],
  &quot;figure_grounding_summary&quot;: &quot;## Figure-Derived Supplement\n\nFor topology, visible stream labels, stream types, and figure-shown coupling, the figure evidence below is the highest-priority task source.\nTreat the `labels_and_topology` answer as the visible topology contract. Icon-family candidates are only block-type hints and must not split, remove, rename, or invent visible nodes.\nUse written text/tables for numeric conditions or semantics that are not visible in the figure, but do not silently overwrite a visible figure fact.\nIf any figure note conflicts with the written markdown or a generated split-task description, keep the conflict visible as a blocker until resolved.\n\n### Image: `tasks/test/chn/chapter_05/images/exercise_5_1_flow.png`\n\n- Question `subfigure_scope_and_authority`: [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] blocking uncertainty，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、parallel、co-current、cross-flow；[NON-ENGLISH REDACTED] part_a、part_b [NON-ENGLISH REDACTED] split id [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] split id [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。\n  - Direct answer: [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] Aspen Plus [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] 5.1 [NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]。\n  - Visual evidence: [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、(a)/(b)、part_a/part_b、[NON-ENGLISH REDACTED]。\n  - Visual evidence: [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。\n  - Visual evidence: [NON-ENGLISH REDACTED]：BZIN、BZIN2、H2IN、H2RCY、H2RCY2、RXIN、RXOUT、VAP、PURGE、PURGE2、LIQ、COLFD、PRODUCT、LTENDS、CHRCY、CHRCY2、CHRCY3。\n  - Visual evidence: [NON-ENGLISH REDACTED]：BZIN [NON-ENGLISH REDACTED] FEEDPUMP [NON-ENGLISH REDACTED] FEED-MIX；H2IN [NON-ENGLISH REDACTED] H2RCY2 [NON-ENGLISH REDACTED] FEED-MIX；REACT [NON-ENGLISH REDACTED] RXOUT [NON-ENGLISH REDACTED] HP-SEP；[NON-ENGLISH REDACTED] VAP [NON-ENGLISH REDACTED] VFLOW [NON-ENGLISH REDACTED] H2RCY [NON-ENGLISH REDACTED] PURGE [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] LIQ [NON-ENGLISH REDACTED] LFLOW [NON-ENGLISH REDACTED] COLUMN [NON-ENGLISH REDACTED] COLFD [NON-ENGLISH REDACTED] CHRCY [NON-ENGLISH REDACTED]。\n  - Visual evidence: [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”、“[NON-ENGLISH REDACTED]”、“parallel”、“co-current”、“cross-flow”[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。\n  - Uncertainty: [NON-ENGLISH REDACTED]；“[NON-ENGLISH REDACTED] 5.1 [NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]。\n  - Uncertainty: [NON-ENGLISH REDACTED] blocking conflict。\n- Question `labels_and_topology`: [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] from -&gt; through/into -&gt; to。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] fan-in/fan-out，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] Aspen block type，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] visible_label [NON-ENGLISH REDACTED] type_from_context [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]。\n  - Direct answer: {&#x27;visible_modules_or_equipment_nodes&#x27;: [{&#x27;visible_label&#x27;: &#x27;FEEDPUMP&#x27;, &#x27;type_from_context&#x27;: &#x27;Pump&#x27;}, {&#x27;visible_label&#x27;: &#x27;FEED-MIX&#x27;, &#x27;type_from_context&#x27;: &#x27;Heater&#x27;}, {&#x27;visible_label&#x27;: &#x27;REACT&#x27;, &#x27;type_from_context&#x27;: &#x27;Rstoic&#x27;}, {&#x27;visible_label&#x27;: &#x27;HP-SEP&#x27;, &#x27;type_from_context&#x27;: &#x27;Flash2&#x27;}, {&#x27;visible_label&#x27;: &#x27;VFLOW&#x27;, &#x27;type_from_context&#x27;: &#x27;FSplit&#x27;}, {&#x27;visible_label&#x27;: &#x27;VALVE&#x27;, &#x27;type_from_context&#x27;: &#x27;Valve&#x27;}, {&#x27;visible_label&#x27;: &#x27;COMP&#x27;, &#x27;type_from_context&#x27;: &#x27;Compr&#x27;}, {&#x27;visible_label&#x27;: &#x27;LFLOW&#x27;, &#x27;type_from_context&#x27;: &#x27;FSplit&#x27;}, {&#x27;visible_label&#x27;: &#x27;PUMP&#x27;, &#x27;type_from_context&#x27;: &#x27;Pump HI&#x27;}, {&#x27;visible_label&#x27;: &#x27;PIPE&#x27;, &#x27;type_from_context&#x27;: &#x27;Pipe&#x27;}, {&#x27;visible_label&#x27;: &#x27;COLUMN&#x27;, &#x27;type_from_context&#x27;: &#x27;RadFrac&#x27;}], &#x27;visible_stream_edges_and_connections&#x27;: [{&#x27;stream_label&#x27;: &#x27;BZIN&#x27;, &#x27;connection&#x27;: &#x27;external source -&gt; FEEDPUMP&#x27;}, {&#x27;stream_label&#x27;: &#x27;BZIN2&#x27;, &#x27;connection&#x27;: &#x27;FEEDPUMP -&gt; FEED-MIX&#x27;}, {&#x27;stream_label&#x27;: &#x27;H2IN&#x27;, &#x27;connection&#x27;: &#x27;external source -&gt; FEED-MIX&#x27;}, {&#x27;stream_label&#x27;: &#x27;H2RCY2&#x27;, &#x27;connection&#x27;: &#x27;COMP -&gt; FEED-MIX&#x27;}, {&#x27;stream_label&#x27;: &#x27;CHRCY3&#x27;, &#x27;connection&#x27;: &#x27;PIPE -&gt; FEED-MIX&#x27;}, {&#x27;stream_label&#x27;: &#x27;RXIN&#x27;, &#x27;connection&#x27;: &#x27;FEED-MIX -&gt; REACT&#x27;}, {&#x27;stream_label&#x27;: &#x27;RXOUT&#x27;, &#x27;connection&#x27;: &#x27;REACT -&gt; HP-SEP&#x27;}, {&#x27;stream_label&#x27;: &#x27;VAP&#x27;, &#x27;connection&#x27;: &#x27;HP-SEP -&gt; VFLOW&#x27;}, {&#x27;stream_label&#x27;: &#x27;H2RCY&#x27;, &#x27;connection&#x27;: &#x27;VFLOW -&gt; COMP&#x27;}, {&#x27;stream_label&#x27;: &#x27;PURGE&#x27;, &#x27;connection&#x27;: &#x27;VFLOW -&gt; VALVE&#x27;}, {&#x27;stream_label&#x27;: &#x27;PURGE2&#x27;, &#x27;connection&#x27;: &#x27;VALVE -&gt; external sink&#x27;}, {&#x27;stream_label&#x27;: &#x27;LIQ&#x27;, &#x27;connection&#x27;: &#x27;HP-SEP -&gt; LFLOW&#x27;}, {&#x27;stream_label&#x27;: &#x27;CHRCY&#x27;, &#x27;connection&#x27;: &#x27;LFLOW -&gt; PUMP&#x27;}, {&#x27;stream_label&#x27;: &#x27;CHRCY2&#x27;, &#x27;connection&#x27;: &#x27;PUMP -&gt; PIPE&#x27;}, {&#x27;stream_label&#x27;: &#x27;COLFD&#x27;, &#x27;connection&#x27;: &#x27;LFLOW -&gt; COLUMN&#x27;}, {&#x27;stream_label&#x27;: &#x27;LTENDS&#x27;, &#x27;connection&#x27;: &#x27;COLUMN -&gt; external sink&#x27;}, {&#x27;stream_label&#x27;: &#x27;PRODUCT&#x27;, &#x27;connection&#x27;: &#x27;COLUMN -&gt; external sink&#x27;}], &#x27;visible_node_fan_in_fan_out&#x27;: [{&#x27;node&#x27;: &#x27;FEEDPUMP&#x27;, &#x27;fan_in&#x27;: [&#x27;BZIN&#x27;], &#x27;fan_out&#x27;: [&#x27;BZIN2&#x27;]}, {&#x27;node&#x27;: &#x27;FEED-MIX&#x27;, &#x27;fan_in&#x27;: [&#x27;BZIN2&#x27;, &#x27;H2IN&#x27;, &#x27;H2RCY2&#x27;, &#x27;CHRCY3&#x27;], &#x27;fan_out&#x27;: [&#x27;RXIN&#x27;]}, {&#x27;node&#x27;: &#x27;REACT&#x27;, &#x27;fan_in&#x27;: [&#x27;RXIN&#x27;], &#x27;fan_out&#x27;: [&#x27;RXOUT&#x27;]}, {&#x27;node&#x27;: &#x27;HP-SEP&#x27;, &#x27;fan_in&#x27;: [&#x27;RXOUT&#x27;], &#x27;fan_out&#x27;: [&#x27;VAP&#x27;, &#x27;LIQ&#x27;]}, {&#x27;node&#x27;: &#x27;VFLOW&#x27;, &#x27;fan_in&#x27;: [&#x27;VAP&#x27;], &#x27;fan_out&#x27;: [&#x27;H2RCY&#x27;, &#x27;PURGE&#x27;]}, {&#x27;node&#x27;: &#x27;COMP&#x27;, &#x27;fan_in&#x27;: [&#x27;H2RCY&#x27;], &#x27;fan_out&#x27;: [&#x27;H2RCY2&#x27;]}, {&#x27;node&#x27;: &#x27;VALVE&#x27;, &#x27;fan_in&#x27;: [&#x27;PURGE&#x27;], &#x27;fan_out&#x27;: [&#x27;PURGE2&#x27;]}, {&#x27;node&#x27;: &#x27;LFLOW&#x27;, &#x27;fan_in&#x27;: [&#x27;LIQ&#x27;], &#x27;fan_out&#x27;: [&#x27;CHRCY&#x27;, &#x27;COLFD&#x27;]}, {&#x27;node&#x27;: &#x27;PUMP&#x27;, &#x27;fan_in&#x27;: [&#x27;CHRCY&#x27;], &#x27;fan_out&#x27;: [&#x27;CHRCY2&#x27;]}, {&#x27;node&#x27;: &#x27;PIPE&#x27;, &#x27;fan_in&#x27;: [&#x27;CHRCY2&#x27;], &#x27;fan_out&#x27;: [&#x27;CHRCY3&#x27;]}, {&#x27;node&#x27;: &#x27;COLUMN&#x27;, &#x27;fan_in&#x27;: [&#x27;COLFD&#x27;], &#x27;fan_out&#x27;: [&#x27;LTENDS&#x27;, &#x27;PRODUCT&#x27;]}]}\n  - Visual evidence: [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。\n  - Visual evidence: [NON-ENGLISH REDACTED]：BZIN、BZIN2、H2IN、H2RCY、H2RCY2、RXIN、RXOUT、VAP、PURGE、PURGE2、LIQ、COLFD、PRODUCT、LTENDS、CHRCY、CHRCY2、CHRCY3。\n  - Visual evidence: FEED-MIX [NON-ENGLISH REDACTED]：BZIN2、H2IN、H2RCY2、CHRCY3，[NON-ENGLISH REDACTED] RXIN。\n  - Visual evidence: HP-SEP [NON-ENGLISH REDACTED] VAP [NON-ENGLISH REDACTED] VFLOW，[NON-ENGLISH REDACTED] LIQ [NON-ENGLISH REDACTED] LFLOW。\n  - Visual evidence: VFLOW [NON-ENGLISH REDACTED] H2RCY [NON-ENGLISH REDACTED] COMP，[NON-ENGLISH REDACTED] PURGE [NON-ENGLISH REDACTED] VALVE；VALVE [NON-ENGLISH REDACTED] PURGE2。\n  - Visual evidence: LFLOW [NON-ENGLISH REDACTED] COLFD [NON-ENGLISH REDACTED] COLUMN，[NON-ENGLISH REDACTED] CHRCY [NON-ENGLISH REDACTED] PUMP；PUMP、PIPE [NON-ENGLISH REDACTED] FEED-MIX [NON-ENGLISH REDACTED] CHRCY3。\n  - Visual evidence: COLUMN [NON-ENGLISH REDACTED] COLFD [NON-ENGLISH REDACTED]，LTENDS [NON-ENGLISH REDACTED] PRODUCT [NON-ENGLISH REDACTED]。\n  - Uncertainty: [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] from -&gt; to [NON-ENGLISH REDACTED]。\n  - Uncertainty: type_from_context [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] visible_label。\n  - Uncertainty: [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] external source [NON-ENGLISH REDACTED] external sink [NON-ENGLISH REDACTED]。\n- Question `numbers_and_constraints`: [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]。\n  - Direct answer: {&#x27;[NON-ENGLISH REDACTED]&#x27;: &#x27;[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]“2”“3”[NON-ENGLISH REDACTED] H2IN、H2RCY2、BZIN2、CHRCY2、CHRCY3、PURGE2 [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。&#x27;, &#x27;[NON-ENGLISH REDACTED]&#x27;: &#x27;[NON-ENGLISH REDACTED]。&#x27;, &#x27;[NON-ENGLISH REDACTED]&#x27;: &#x27;[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。&#x27;, &#x27;[NON-ENGLISH REDACTED]&#x27;: &#x27;[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]。&#x27;, &#x27;[NON-ENGLISH REDACTED]&#x27;: &#x27;[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。&#x27;, &#x27;[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]&#x27;: {&#x27;[NON-ENGLISH REDACTED]&#x27;: &#x27;COLUMN [NON-ENGLISH REDACTED] PRODUCT；[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] LTENDS。&#x27;, &#x27;[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]&#x27;: &#x27;HP-SEP [NON-ENGLISH REDACTED] VAP [NON-ENGLISH REDACTED] VFLOW；VFLOW [NON-ENGLISH REDACTED] PURGE，[NON-ENGLISH REDACTED] VALVE [NON-ENGLISH REDACTED] PURGE2，[NON-ENGLISH REDACTED]。&#x27;, &#x27;[NON-ENGLISH REDACTED]&#x27;: &#x27;VFLOW [NON-ENGLISH REDACTED] H2RCY [NON-ENGLISH REDACTED] COMP，[NON-ENGLISH REDACTED] H2RCY2，[NON-ENGLISH REDACTED] FEED-MIX。&#x27;, &#x27;[NON-ENGLISH REDACTED]&#x27;: &#x27;HP-SEP [NON-ENGLISH REDACTED] LIQ [NON-ENGLISH REDACTED] LFLOW；LFLOW [NON-ENGLISH REDACTED] CHRCY，[NON-ENGLISH REDACTED] PUMP [NON-ENGLISH REDACTED] CHRCY2，[NON-ENGLISH REDACTED] PIPE [NON-ENGLISH REDACTED] CHRCY3，[NON-ENGLISH REDACTED] FEED-MIX。&#x27;, &#x27;[NON-ENGLISH REDACTED]&#x27;: &#x27;LFLOW [NON-ENGLISH REDACTED] COLFD [NON-ENGLISH REDACTED] COLUMN。&#x27;}, &#x27;[NON-ENGLISH REDACTED]_Aspen_[NON-ENGLISH REDACTED]&#x27;: [&#x27;FEEDPUMP [NON-ENGLISH REDACTED] BZIN [NON-ENGLISH REDACTED]：BZIN -&gt; FEEDPUMP -&gt; BZIN2。&#x27;, &#x27;FEED-MIX [NON-ENGLISH REDACTED]：BZIN2、H2IN、H2RCY2、CHRCY3；[NON-ENGLISH REDACTED] RXIN。&#x27;, &#x27;[NON-ENGLISH REDACTED]：FEED-MIX -&gt; RXIN -&gt; REACT -&gt; RXOUT -&gt; HP-SEP。&#x27;, &#x27;HP-SEP [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] VAP，[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] LIQ。&#x27;, &#x27;VFLOW [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] VAP，[NON-ENGLISH REDACTED] H2RCY [NON-ENGLISH REDACTED] PURGE。&#x27;, &#x27;H2RCY [NON-ENGLISH REDACTED] COMP [NON-ENGLISH REDACTED] H2RCY2 [NON-ENGLISH REDACTED] FEED-MIX。&#x27;, &#x27;PURGE [NON-ENGLISH REDACTED] VALVE [NON-ENGLISH REDACTED] PURGE2 [NON-ENGLISH REDACTED]。&#x27;, &#x27;LFLOW [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] LIQ，[NON-ENGLISH REDACTED] COLFD [NON-ENGLISH REDACTED] CHRCY。&#x27;, &#x27;CHRCY [NON-ENGLISH REDACTED] PUMP [NON-ENGLISH REDACTED] PIPE [NON-ENGLISH REDACTED] CHRCY3 [NON-ENGLISH REDACTED] FEED-MIX。&#x27;, &#x27;COLFD [NON-ENGLISH REDACTED] COLUMN；COLUMN [NON-ENGLISH REDACTED] LTENDS [NON-ENGLISH REDACTED] PRODUCT。&#x27;, &#x27;[NON-ENGLISH REDACTED] COLUMN [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。&#x27;, &#x27;[NON-ENGLISH REDACTED] FEEDPUMP [NON-ENGLISH REDACTED] PUMP [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] BZIN [NON-ENGLISH REDACTED] CHRCY [NON-ENGLISH REDACTED]。&#x27;]}\n  - Visual evidence: [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。\n  - Visual evidence: [NON-ENGLISH REDACTED]：BZIN、BZIN2、H2IN、H2RCY、H2RCY2、RXIN、RXOUT、VAP、PURGE、PURGE2、LIQ、COLFD、PRODUCT、LTENDS、CHRCY、CHRCY2、CHRCY3。\n  - Visual evidence: BZIN [NON-ENGLISH REDACTED] FEEDPUMP，FEEDPUMP [NON-ENGLISH REDACTED] BZIN2。\n  - Visual evidence: BZIN2、H2IN、H2RCY2、CHRCY3 [NON-ENGLISH REDACTED] FEED-MIX，FEED-MIX [NON-ENGLISH REDACTED] RXIN。\n  - Visual evidence: RXIN [NON-ENGLISH REDACTED] REACT，REACT [NON-ENGLISH REDACTED] RXOUT [NON-ENGLISH REDACTED] HP-SEP。\n  - Visual evidence: HP-SEP [NON-ENGLISH REDACTED] VAP [NON-ENGLISH REDACTED] VFLOW；[NON-ENGLISH REDACTED] LIQ [NON-ENGLISH REDACTED] LFLOW。\n  - Visual evidence: VFLOW [NON-ENGLISH REDACTED] PURGE，[NON-ENGLISH REDACTED] VALVE [NON-ENGLISH REDACTED] PURGE2；[NON-ENGLISH REDACTED] H2RCY，[NON-ENGLISH REDACTED] COMP [NON-ENGLISH REDACTED] H2RCY2 [NON-ENGLISH REDACTED] FEED-MIX。\n  - Visual evidence: LFLOW [NON-ENGLISH REDACTED] COLFD [NON-ENGLISH REDACTED] COLUMN；[NON-ENGLISH REDACTED] CHRCY [NON-ENGLISH REDACTED] PUMP、CHRCY2、PIPE、CHRCY3 [NON-ENGLISH REDACTED] FEED-MIX。\n  - Uncertainty: [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。\n  - Uncertainty: COLUMN [NON-ENGLISH REDACTED] LTENDS [NON-ENGLISH REDACTED] PRODUCT [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。\n  - Uncertainty: [NON-ENGLISH REDACTED] COLUMN [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]。\n  - Uncertai&quot;,
  &quot;source&quot;: &quot;LLM gate contract&quot;,
  &quot;model&quot;: &quot;gpt-5.5&quot;,
  &quot;analysis_policy_version&quot;: &quot;analysis_optional_bonus_v2&quot;,
  &quot;input_scope&quot;: &quot;task text only; no cases.yaml block_family or baseline script&quot;,
  &quot;_usage&quot;: {
    &quot;model&quot;: &quot;gpt-5.5&quot;,
    &quot;prompt_tokens&quot;: 15266,
    &quot;completion_tokens&quot;: 9275,
    &quot;total_tokens&quot;: 24541
  },
  &quot;recycle_closure_contract&quot;: {
    &quot;closure_type&quot;: &quot;numerical_recycle_tear&quot;,
    &quot;accepted_topology&quot;: &quot;task-stated physical material return paths into upstream process units&quot;,
    &quot;physical_recycle_required&quot;: true
  },
  &quot;requirement_registration&quot;: {
    &quot;status&quot;: &quot;task_specific_dynamic&quot;,
    &quot;task_specific_kinds&quot;: [
      &quot;pressure_transform_unit_fidelity&quot;,
      &quot;pump_curve_fidelity&quot;,
      &quot;reaction_separator_splitter_contract&quot;
    ],
    &quot;permission_granted&quot;: false,
    &quot;validation_route&quot;: &quot;generic_gate_adjudication&quot;
  }
}
```

### FILE: docs/hardcoded_script_plan/guide-for-hardcoded-script.md
Reason: core hardcoded script/runtime contract
```text
# Hardcoded Script [NON-ENGLISH REDACTED]

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] `hardcoded script` [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED] session [NON-ENGLISH REDACTED] checkpoint [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]：`REP`、`APW`、`BKP`。
- [NON-ENGLISH REDACTED] `hardcoded-script-[NON-ENGLISH REDACTED].md`。
- [NON-ENGLISH REDACTED] `PER_ERROR`，[NON-ENGLISH REDACTED] completion / warning / [NON-ENGLISH REDACTED]。

## [NON-ENGLISH REDACTED]

### 1. [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：

1. `tool_side_generation/healthcheck/full_evaluation/*.py`
2. `tool_side_generation/healthcheck/full_example/*.py`
3. `tool_side_generation/healthcheck/full_example/homework/*.py`
4. `scripts/*.py`
5. [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]？
- [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]？
- [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]？[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。

### 2. [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] Aspen-safe [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] setter / readback / REP [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]”。

### 3. [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：

1. [NON-ENGLISH REDACTED]
2. completion [NON-ENGLISH REDACTED]
3. `PER_ERROR` [NON-ENGLISH REDACTED]
4. [NON-ENGLISH REDACTED]
5. [NON-ENGLISH REDACTED]
6. [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] hardcoded script [NON-ENGLISH REDACTED] `healthcheck/full_evaluation` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]：

1. [NON-ENGLISH REDACTED]：`TASK_SET`、`TASK_ID`、`SCRIPT_STEM`
2. [NON-ENGLISH REDACTED]
3. [NON-ENGLISH REDACTED]
4. `_build_*` / `_configure_*` / `_run_*` [NON-ENGLISH REDACTED]
5. `main_async()`
6. [NON-ENGLISH REDACTED] `summary.json`

[NON-ENGLISH REDACTED]：

- `default_task_output_dir_for_script`
- `default_task_bkp_subdir_for_script`
- `export_evidence_bundle`
- `read_per_error_best_effort`
- `resolve_server_url`
- `check_server_health_or_exit`

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：

```text
data/file/output/hardcoded/tasks/&lt;task_set&gt;/&lt;task_id&gt;/&lt;script_stem&gt;/
```

[NON-ENGLISH REDACTED]：

- `REP`
- `APW`
- `BKP`
- `summary.json`

`summary.json` [NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]
- completion [NON-ENGLISH REDACTED]
- `PER_ERROR`
- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]

## [NON-ENGLISH REDACTED]

### 1. [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] builder、[NON-ENGLISH REDACTED] readback [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] JSDoc，[NON-ENGLISH REDACTED] JSDoc [NON-ENGLISH REDACTED]；Python [NON-ENGLISH REDACTED] docstring，[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]

### 2. [NON-ENGLISH REDACTED] inline comment

[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] workaround [NON-ENGLISH REDACTED] Aspen/MCP [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：

- “[NON-ENGLISH REDACTED]”
- “[NON-ENGLISH REDACTED]”
- “[NON-ENGLISH REDACTED] Aspen”

[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”，[NON-ENGLISH REDACTED]：

- “[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `PRES` [NON-ENGLISH REDACTED] `DELT`。”
- “[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `FSplit` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。”
- “[NON-ENGLISH REDACTED] REP [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。”

## Aspen [NON-ENGLISH REDACTED]

### 1. [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] sweep

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]：

1. `Sensitivity Analysis`
2. `Design Spec`
3. `Optimization`
4. [NON-ENGLISH REDACTED] + [NON-ENGLISH REDACTED]
5. [NON-ENGLISH REDACTED] Python [NON-ENGLISH REDACTED] sweep

[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] UI / MCP / [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] Aspen”[NON-ENGLISH REDACTED]

### 2. [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] hardcoded script [NON-ENGLISH REDACTED]：

- `Sensitivity Analysis`：[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]
- `Design Spec`：[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”
- `Optimization`：[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] Python [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] GUI / REP [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] MCP、[NON-ENGLISH REDACTED] UI [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] hardcoded script [NON-ENGLISH REDACTED]：

1. [NON-ENGLISH REDACTED]？[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `Sensitivity Analysis`
2. [NON-ENGLISH REDACTED]？[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `Design Spec`
3. [NON-ENGLISH REDACTED]？[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `Optimization`
4. [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]

### 3.5 `Design Spec` [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”

[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。Design Spec helper [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”，**[NON-ENGLISH REDACTED]** Aspen [NON-ENGLISH REDACTED] block [NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] block [NON-ENGLISH REDACTED] materialize”，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]：

```text
ERROR WHILE CHECKING INPUT SPECIFICATIONS FOR VARIED VARIABLE IN DESIGN-SPEC
THIS VARIABLE IS NOT SPECIFIED IN THE BLOCK.
YOU CAN PROVIDE AN INITIAL VALUE IN THE BLOCK OR USE ANOTHER VARIABLE.
```

[NON-ENGLISH REDACTED]：

1. [NON-ENGLISH REDACTED]。
2. [NON-ENGLISH REDACTED] block setter [NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED] block [NON-ENGLISH REDACTED]**，[NON-ENGLISH REDACTED] flowsheet [NON-ENGLISH REDACTED]。
3. [NON-ENGLISH REDACTED] `Design Spec` [NON-ENGLISH REDACTED] `helper-managed manipulated-variable field`。

[NON-ENGLISH REDACTED] `RadFrac` [NON-ENGLISH REDACTED]：

- `Design Spec` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] **Aspen [NON-ENGLISH REDACTED]**，[NON-ENGLISH REDACTED] flowsheet [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] flowsheet [NON-ENGLISH REDACTED] `V1`，[NON-ENGLISH REDACTED] `helper-managed manipulated-variable field` [NON-ENGLISH REDACTED] `MOLE-L1`、`MOLE-VN`、`MOLE-D` [NON-ENGLISH REDACTED] token。
- [NON-ENGLISH REDACTED] block [NON-ENGLISH REDACTED] `Data\Blocks\&lt;BLK&gt;\Input\PROD_FLOW\&lt;stream&gt;`，[NON-ENGLISH REDACTED] `V1` [NON-ENGLISH REDACTED] `helper-managed manipulated-variable field` [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED] **[NON-ENGLISH REDACTED] token** [NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED] helper readback、`probe_model_state` [NON-ENGLISH REDACTED] block [NON-ENGLISH REDACTED] collector，[NON-ENGLISH REDACTED] block [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `null` / [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] capability（[NON-ENGLISH REDACTED] `set_prod_flow`、`set_radfrac_distillate_rate`），[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] `Design Spec` [NON-ENGLISH REDACTED] `helper-managed manipulated-variable field` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] token。
- [NON-ENGLISH REDACTED] `helper-managed manipulated-variable field` [NON-ENGLISH REDACTED] `helper-managed manipulated-variable field`，[NON-ENGLISH REDACTED] `HAP_PROMPT` [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] flowsheet [NON-ENGLISH REDACTED] `ID1`。

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”，[NON-ENGLISH REDACTED] `LOWER/UPPER`、`ASKED` [NON-ENGLISH REDACTED] sweep。[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]“Design Spec [NON-ENGLISH REDACTED]”。

### 3. [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，hardcoded script [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”，[NON-ENGLISH REDACTED]：

- `Sensitivity Analysis` / `Design Spec` / `Optimization` [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] hardcoded script [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] sweep [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”
- [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]”

### 4. [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]：

1. [NON-ENGLISH REDACTED] `Sensitivity Analysis` [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]
2. [NON-ENGLISH REDACTED] `Design Spec` [NON-ENGLISH REDACTED]
3. [NON-ENGLISH REDACTED] `Optimization` [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”。[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。

### 5. [NON-ENGLISH REDACTED] sweep

[NON-ENGLISH REDACTED] sweep：

- [NON-ENGLISH REDACTED] MCP / HTTP [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] sweep [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] sweep，[NON-ENGLISH REDACTED] `summary.json` [NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED] `Sensitivity Analysis` / `Design Spec` / `Optimization`
- [NON-ENGLISH REDACTED] sweep [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]

## Headless [NON-ENGLISH REDACTED]

### 1. [NON-ENGLISH REDACTED] GUI [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] hardcoded script [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] Aspen GUI”。[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。

### 2. [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] `session/start` [NON-ENGLISH REDACTED] `show_gui` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] CLI [NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]：

- `show_gui=true`：[NON-ENGLISH REDACTED] Aspen GUI
- `show_gui=false`：[NON-ENGLISH REDACTED] session
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] `AspenHttpClient.ensure_session()` [NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED] `show_gui=false`
- [NON-ENGLISH REDACTED] `ASPEN_HARDCODED_SHOW_GUI=0/1` [NON-ENGLISH REDACTED] hardcoded [NON-ENGLISH REDACTED] session [NON-ENGLISH REDACTED]

### 3. [NON-ENGLISH REDACTED] GUI

[NON-ENGLISH REDACTED] GUI：

- [NON-ENGLISH REDACTED] `ui_check_next_completion_status`
- [NON-ENGLISH REDACTED] `Sensitivity Analysis / Design Spec / Optimization` [NON-ENGLISH REDACTED] GUI [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] completion [NON-ENGLISH REDACTED] UI [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：

```text
--show-gui
```

[NON-ENGLISH REDACTED]：

```python
client.ensure_session(show_gui=bool(args.show_gui) or None)
```

[NON-ENGLISH REDACTED] headless [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `False`，[NON-ENGLISH REDACTED] GUI。

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：

1. [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
2. [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]”。
3. [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
4. [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
5. [NON-ENGLISH REDACTED] Aspen-safe [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。
6. [NON-ENGLISH REDACTED]。
7. [NON-ENGLISH REDACTED] `completion`、`PER_ERROR`、`REP/APW/BKP`。
8. [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `Sensitivity Analysis` / `Design Spec` / `Optimization`。
9. [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
9. [NON-ENGLISH REDACTED] `summary.json`。
10. [NON-ENGLISH REDACTED] `hardcoded-script-[NON-ENGLISH REDACTED].md`。

## [NON-ENGLISH REDACTED]

- [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] recycle、purge、pressure-change [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED]、setter [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] `INSET=SI`、REP [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]”。
- [NON-ENGLISH REDACTED] sweep [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]。
- GUI [NON-ENGLISH REDACTED] headless [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] inline comment
- [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] sweep
- [NON-ENGLISH REDACTED] `Sensitivity Analysis` / `Design Spec` / `Optimization` [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED]
- `REP/APW/BKP` [NON-ENGLISH REDACTED]
- `completion` [NON-ENGLISH REDACTED]
- `PER_ERROR` [NON-ENGLISH REDACTED]
- [NON-ENGLISH REDACTED] `summary.json`
- [NON-ENGLISH REDACTED]

## [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] hardcoded script [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] Aspen”，[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。

```

### FILE: docs/hardcoded_script_plan/script_agent_http_api_contract.md
Reason: core hardcoded script/runtime contract
```text
# Script Agent Aspen HTTP API Contract

This file is compact context for the local script-authoring agent. It is not a
task solution. It lists stable operation names and parameter shapes that
generated hardcoded scripts should use through `AspenHttpClient.invoke(...)`.
The name of this document describes the native transport, not a requirement for
generated code to choose between HTTP and local Python helpers.

## Default Unified Invocation Contract

`client.invoke(&quot;capability&quot;, **params)` is the default for registered capabilities
and returns a `status`/`result` envelope. Registered local helpers and native HTTP
operations share one registry; generated code need not classify them by transport.
`safe.call(client, &quot;capability&quot;, **params)` strictly checks the routed outcome and
unwraps its result payload. `safe.probe_call(client, &quot;capability&quot;, **params)` uses
the same registry but preserves diagnostic payloads, including incomplete
completion evidence. Existing typed `safe.func(client, ...)` helpers remain valid.
`client.execute(...)` is a compatibility entry into this unified route.
`client.execute_http(...)` is internal native-only transport, not a generated-code
shortcut or fallback.

Use exact supported names and parameter shapes. Unqualified registered names
follow registry `default_route` metadata. Same-name native forwarders retain the
HTTP default; there is no universal local-first rule. `local:name` explicitly
selects the registered Python helper, while `http:name` selects a valid native
identity and rejects local-only helpers. Unknown `local:` names fail;
unregistered unqualified names retain legacy HTTP dispatch. This is identity
selection, not error-driven fallback: bad local parameters and local-helper
failures are never retried as HTTP. Inspect the actual local helper signature;
it may differ from the native-default parameter contract. Do not assume all
aliases are registered or portable.
This contract does not permit raw tree or atomic analysis calls: the safe
raw-operation policy still applies regardless of entry point or namespace.

## Prefer The Helper Module

Generated scripts may import:

```python
import script_agent_exp.safe_aspen_calls as safe
```

Or use the existing typed imports:

```python
from script_agent_exp.safe_aspen_calls import (
    add_components_by_cas,
    assert_completion_ready,
    call,
    check_block_completion,
    check_flowsheet_completion,
    check_stream_completion,
    configure_calculator_stream_component_makeup_balance,
    configure_block_property_method,
    configure_recycle_convergence_options,
    ensure_property_method,
    configure_requil_equilibrium_reactions,
    configure_rstoic_calculated_heat_reference,
    configure_rstoic_flash,
    configure_rstoic_fractional_conversions,
    configure_rstoic_stoichiometry,
    connect_material_inlet_outlet,
    connect_material_ports_by_order,
    connect_stream,
    create_block,
    create_material_streams,
    export_standard_evidence,
    list_block_ports,
    probe_model_state,
    run_completion_engine_and_export,
    run_stage,
    set_material_stream,
    write_summary,
)
```

Use the helpers when possible. They enforce the exact parameter names below and
raise useful diagnostics when Aspen or HTTP rejects a call. Prefer block-family
helpers (`configure_heatx_shortcut_target`, `configure_heatx_detailed_shell_tube_rating`,
`configure_radfrac_total_condenser`, ...) over ad hoc sequences of raw `set_*`
calls when a helper covers the task.

**Important:** `create_block` is a local typed Python helper, not a registered
HTTP capability. Generated slim source must never call `client.invoke(&quot;create_block&quot;, ...)`;
prefer family-specific registered routes such as `create_heater`, `create_mixer`,
or `create_rstoic`, and use `safe.create_block(client, family, block_name)` only
when no family-specific route is available. `create_material_streams` is likewise
a local helper; the server exposes the native `create_material_stream` route.
`add_components_by_cas` names both a local helper and a native route: use explicit
`local:add_components_by_cas` for the Python helper or
`http:add_components_by_cas` for the native operation. Its unqualified name
retains the HTTP default through native-forwarder metadata; do not assume
identical parameter shapes or a local-first default.
Do not invent `create_stream` or `create_component` capability aliases.

For `run_standard_probe_matrix` row setters, documented registered helpers such as
`configure_heat_stream_duty_map` and `configure_heatx_shortcut_target` are valid
`operation` names. `probe_call`, `safe.call`, and `client.invoke` use the same
registry, so these registered helpers are also valid in main script logic. They
remain local helpers, not native HTTP wire routes. Never bypass routing with
`execute_http` to send a helper name or retry a failed helper.

For recycle-loop inventory closure, prefer
`configure_calculator_stream_component_makeup_balance(...)` over raw
Calculator `helper-managed sampled-variable field*` tree writes. For tear/recycle settings, prefer
`configure_recycle_convergence_options(...)` over direct `Conv-Options` writes.

Do not copy or reimplement `AspenHttpClient`, `JsonlRecorder`,
`resolve_server_url`, `check_server_health_or_exit`, or REP parser helpers.
Import them from the generic helper files already provided in context.

## Required CLI Contract

The harness runs generated scripts with these arguments:

```text
--section-out-dir &lt;path&gt;
--bkp-subdir &lt;server-relative-subdir&gt;
--task-key &lt;stable-task-key&gt;
--server-url &lt;url&gt;       # optional
--port &lt;int&gt;             # optional
--show-gui              # optional flag
```

Every generated script must accept all of them. Write `summary.json` at:

```python
Path(args.section_out_dir) / SCRIPT_STEM / &quot;summary.json&quot;
```

Use `args.bkp_subdir` for evidence exports when present, and use
`args.task_key` for the Aspen HTTP task hash/name seed when present.

## Staged Script Shape

The harness currently runs one generated Python script per case. To make complex
work easier, write that script as small stages instead of one large `main` body:

```python
def setup_components(client): ...
def build_topology(client): ...
def set_specs(client): ...
def run_and_export(client, args): ...
```

Record stage diagnostics in `summary.json` under a top-level `stages` key. Rerun
the deterministic script from scratch on every repair iteration. Do not depend
on BKP/checkpoint handoff as normal state transfer; it is cheap to rebuild from
the script.

## Probe As You Build

Generated scripts should not be open-loop. After each major stage, probe Aspen
state and log it into `summary.json`:

```python
topology_probe = probe_model_state(
    client,
    stream_names=[&quot;F1&quot;, &quot;P1&quot;],
    block_names=[&quot;M1&quot;, &quot;R1&quot;],
    include_flowsheet=True,
    include_ui_next=False,
)
```

Use focused probes when repairing:

```python
check_stream_completion(client, &quot;F1&quot;)
check_block_completion(client, &quot;R1&quot;)
check_flowsheet_completion(client)
```

Intermediate flowsheet probes do not open GUI by default. Do not loop on UI
Next. For `probe_sweep_matrix` only, if non-UI probes show the initial sweep
state has no input-incomplete streams, blocks, or flowsheet state, skip UI Next
entirely for the exploratory sweep rows. If readiness is incomplete, use at most
one bounded completion repair before the sweep. Use
`run_completion_engine_and_export(...)` for the final selected evidence row, not
for every exploratory candidate when the candidate only changes already-complete
operating inputs. If a generated script calls UI Next twice without a
create/set/connect/engine action in between, the helper returns a skipped
diagnostic instead of opening Aspen GUI again.

Never run/export while required input is incomplete. Immediately before engine
run, probe required feed streams and blocks and gate execution:

```python
ready_probe = probe_model_state(
    client,
    stream_names=[&quot;F1&quot;],
    block_names=[&quot;C1&quot;],
    include_flowsheet=True,
)
assert_completion_ready(ready_probe, require_streams=[&quot;F1&quot;], require_blocks=[&quot;C1&quot;])
```

If a feed stream says `input_incomplete`, call `ui_next_completion(...)` once and
fix the missing stream state before running. A common error is setting
`mixed_spec=&quot;TP&quot;` while only setting pressure and vapor fraction; Aspen then
reports `SUBSTREAM not complete: SSID = MIXED` and `Two of Temperature,
Pressure, and Vapor Fraction must be specified`.

## Aspen-Safe Names

This project server enforces short Aspen object names:

```text
^[A-Za-z][A-Za-z0-9:-]{0,15}$
```

Use names such as `F1`, `P2`, `V1`, `L1`, `H1`, `R1`, `D1`, `S1`, `C-1`,
`FL`, or `HX`. Do not use long semantic stream names like `FEED`, `PROD`,
`VAPOR`, `LIQUID`, `PRODUCT`, `PUMPED`, or names with underscores/spaces.
Explain the mapping in `summary.json`, for example `F1 = feed`, `P2 = product`.

## Canonical Operations

Component setup:

```python
client.invoke(
    &quot;add_components_by_cas&quot;,
    components=[
        {&quot;component_id&quot;: &quot;ETOH&quot;, &quot;cas&quot;: &quot;64-17-5&quot;},
        {&quot;component_id&quot;: &quot;H2O&quot;, &quot;cas&quot;: &quot;7732-18-5&quot;},
    ],
)
client.invoke(&quot;list_component_ids&quot;)
```

Recycle Calculator and convergence operations:

```python
client.invoke(&quot;create_calculator&quot;, calculator_name=&quot;C-1&quot;)

client.invoke(
    &quot;calculator_define_stream_component_flow&quot;,
    calculator_name=&quot;C-1&quot;,
    variable_name=&quot;A&quot;,
    stream_name=&quot;M1&quot;,
    component=&quot;COMP-01&quot;,
    unit=&quot;kmol/hr&quot;,
    substream=&quot;MIXED&quot;,
    vartype=&quot;MOLE-FLOW&quot;,
)

client.invoke(
    &quot;calculator_set_fortran_exec&quot;,
    calculator_name=&quot;C-1&quot;,
    statements=&quot;A = 120 - B&quot;,
    method=&quot;FORTRAN&quot;,
)

client.invoke(
    &quot;calculator_set_execute_before_block&quot;,
    calculator_name=&quot;C-1&quot;,
    block_name=&quot;MX&quot;,
    block_type=&quot;BLOCK&quot;,
)

client.invoke(
    &quot;set_convergence_options&quot;,
    tolerance=1e-4,
    tear_method=&quot;WEGSTEIN&quot;,
)

client.invoke(
    &quot;set_wegstein_options&quot;,
    max_iterations=100,      # WEG_MAXIT
    wait=1,                  # WEG_WAIT
    direct_steps=0,          # ACCELERATE
    acceleration_steps=1,    # NACCELERATE
    lower_bound=-5.0,        # WEG_QMIN
    upper_bound=0.0,         # WEG_QMAX
)
client.invoke(&quot;read_recycle_convergence_setup&quot;, calculator_name=&quot;C-1&quot;)
```

These raw HTTP operations exist so the helper module can express robust
Calculator and convergence workflows. Generated scripts should use
`configure_calculator_stream_component_makeup_balance(...)` and
`configure_recycle_convergence_options(...)` when those semantics match the
task.

`calculator_set_fortran_exec` pads executable statements to Aspen fixed-form
Fortran before writing `FORTRAN_EXEC`; callers may pass `A = 120 - B`, but the
stored statement must read back with leading label-field blanks.

An empty explicit Tear Streams table is not by itself an error for a closed
recycle model. If the reference or live GUI shows no tear rows, preserve that
pattern and configure the Calculator/makeup balance plus global Conv-Options
instead of inventing a manual tear stream row.

Do not call `add_component` with `component_name`, `cas`, `cas_number`,
`specification`, or `specification_type`. The built-in `add_component` accepts
only `component_id` and is not the preferred route for real chemicals.

Property method:

```python
ensure_property_method(client, method=&quot;NRTL&quot;)
```

`ensure_property_method(...)` is idempotent. If Aspen reports
`OPTION-SETS (...) already exists`, the helper still sets and reads back the
global `GBASEOPSET` / `GOPSETNAME` fields before returning success.

Block-wise property method / local option set:

```python
configure_block_property_method(client, block_name=&quot;A1&quot;, method=&quot;UNIQUAC&quot;)
configure_block_property_method(client, block_name=&quot;A2&quot;, method=&quot;NRTL&quot;)
configure_block_property_method(client, block_name=&quot;A3&quot;, method=&quot;WILSON&quot;)
```

This writes and reads back `\Data\Blocks\&lt;BLOCK&gt;\Input\OPSETNAME`. Do not call
nonexistent operations such as `set_block_property_method`.

Streams and blocks:

```python
client.invoke(&quot;create_material_stream&quot;, stream_name=&quot;F1&quot;)
client.invoke(&quot;create_material_stream&quot;, stream_name=&quot;P2&quot;)
client.invoke(&quot;create_heater&quot;, block_name=&quot;H1&quot;)
client.invoke(&quot;create_flash2&quot;, block_name=&quot;FL&quot;)
client.invoke(&quot;create_pump&quot;, block_name=&quot;P1&quot;)
```

Topology:

The unwrapped `list_block_ports` payload is
`{&quot;success&quot;: true, &quot;block_name&quot;: &quot;H1&quot;, &quot;ports&quot;: {&quot;F(IN)&quot;: [], &quot;P(OUT)&quot;: []}}`.
Direct routed client calls return that payload in a `status`/`result` envelope.
Port names are dictionary keys; an empty connected-stream list means a port
exists but is currently unwired. Normalize either form with the existing pure
`safe.extract_block_ports` helper, not a local response-shape parser.

```python
block_name = &quot;H1&quot;
ports = safe.extract_block_ports(client.invoke(&quot;list_block_ports&quot;, block_name=block_name))
for name in (&quot;F(IN)&quot;, &quot;P(OUT)&quot;):
    if name not in ports:
        raise RuntimeError(f&quot;Required port {name} missing on {block_name}&quot;)
client.invoke(&quot;connect_stream&quot;, block_name=block_name, stream_name=&quot;F1&quot;, port_name=&quot;F(IN)&quot;)
client.invoke(&quot;connect_stream&quot;, block_name=block_name, stream_name=&quot;P2&quot;, port_name=&quot;P(OUT)&quot;)
wired = safe.extract_block_ports(client.invoke(&quot;list_block_ports&quot;, block_name=block_name))
if &quot;F1&quot; not in wired.get(&quot;F(IN)&quot;, []) or &quot;P2&quot; not in wired.get(&quot;P(OUT)&quot;, []):
    raise RuntimeError(&quot;Intended stream wiring was not confirmed by live readback&quot;)
```

Use `name in ports`, not `bool(ports[name])`, for availability. Port presence
alone does not prove connection or completion. Keep post-connect wiring and
completion checks separate from creation/discovery stage verification.
For source-only preflight, `script_agent_exp.core.port_source_contract` exposes
`inspect_port_source_contract(source)` and `require_port_source_contract(source)`;
these report AST dataflow violations without rewriting/executing candidates.
Canonical-extractor delegation and semantic-success wrappers remain legal;
local function names alone must not be blacklisted.

Do not use `from_block`, `to_block`, `source`, `destination`, or `name` for
`connect_stream`; this server expects `block_name`, `stream_name`, `port_name`.
Do not use semantic words such as `FEED`, `PRODUCT`, `INLET`, or `OUTLET` as
`port_name` unless `list_block_ports` actually returned those exact keys.

For common one-feed/one-product material blocks, prefer the helper:

```python
connect_material_inlet_outlet(client, block_name=&quot;P1&quot;, inlet_stream=&quot;F1&quot;, outlet_stream=&quot;P2&quot;)
```

It calls `list_block_ports` and uses live material ports such as `F(IN)` and
`P(OUT)`.

For multi-feed/multi-product material blocks, never invent ports such as `IN1`,
`F2(IN)`, or heat ports such as `HS(IN)`. Prefer:

```python
connect_material_ports_by_order(
    client,
    block_name=&quot;M1&quot;,
    inlet_streams=[&quot;F1&quot;, &quot;F2&quot;],
    outlet_streams=[&quot;S1&quot;],
)
```

It calls `list_block_ports`, filters out heat/work ports, connects by live
material-port order, and returns the port evidence for `summary.json`.

Material stream state and composition:

```python
client.invoke(&quot;set_mixed_spec_mixed&quot;, stream_name=&quot;F1&quot;, value=&quot;TP&quot;)
client.invoke(&quot;set_basis_mixed&quot;, stream_name=&quot;F1&quot;, value=&quot;MOLE-FLOW&quot;)
client.invoke(&quot;set_temp_mixed&quot;, stream_name=&quot;F1&quot;, value=25.0, unit=&quot;C&quot;)
client.invoke(&quot;set_pres_mixed&quot;, stream_name=&quot;F1&quot;, value=1.0, unit=&quot;atm&quot;)
client.invoke(&quot;set_flow_mixed&quot;, stream_name=&quot;F1&quot;, component_name=&quot;ETOH&quot;, value=50.0, unit=&quot;kmol/hr&quot;)
```

Use `component_name` and `value` for `set_flow_mixed`. Do not use
`component_id`, `flow_rate`, or total-only flow when component flow/fraction is
required.

The selected `mixed_spec` must match exactly two state variables:

```python
# Normal T/P feed:
set_material_stream(..., mixed_spec=&quot;TP&quot;, temperature=25.0, temperature_unit=&quot;C&quot;, pressure=1.0, pressure_unit=&quot;atm&quot;)

# Saturated liquid/vapor at pressure:
set_material_stream(..., mixed_spec=&quot;PV&quot;, pressure=1.0, pressure_unit=&quot;atm&quot;, vapor_fraction=0.0)
```

Do not use `mixed_spec=&quot;TP&quot;` with only pressure + vapor fraction. That leaves
temperature unset and makes the stream incomplete.

Component-specific probe readback:

```python
purity = call(
    client,
    &quot;read_stream_output&quot;,
    stream_name=&quot;P2&quot;,
    variable=&quot;mole_fraction&quot;,
    component_name=&quot;ETOH&quot;,
)
```

`read_stream_output` is a registered local helper, not an HTTP wire route. A
state snapshot with no explicit component fraction cannot supply purity evidence.
Preserve units/basis and trusted-run evidence; final scored metrics still use the
final REP readback contract.

Common block specs:

```python
# HEATER / FLASH2
client.invoke(&quot;set_spec_opt&quot;, block_name=&quot;H1&quot;, value=&quot;TP&quot;)
client.invoke(&quot;set_temp&quot;, block_name=&quot;H1&quot;, value=80.0, unit=&quot;C&quot;)
client.invoke(&quot;set_pres&quot;, block_name=&quot;H1&quot;, value=1.0, unit=&quot;atm&quot;)
client.invoke(&quot;set_duty&quot;, block_name=&quot;H1&quot;, value=0.0, unit=&quot;kW&quot;)

# PUMP
client.invoke(&quot;set_opt_spec&quot;, block_name=&quot;P1&quot;, value=&quot;DELP&quot;)
client.invoke(&quot;set_delp&quot;, block_name=&quot;P1&quot;, value=2.0, unit=&quot;bar&quot;)
client.invoke(&quot;set_pres&quot;, block_name=&quot;P1&quot;, value=5.0, unit=&quot;bar&quot;)
```

For `FLASH2`, legal `set_spec_opt` values include `TP`, `TV`, `PV`, `TD`, and
`PD`. If `TP` is selected, set both `set_temp` and `set_pres`.

Completion and run:

```python
completion = client.invoke(&quot;ui_check_next_completion_status&quot;, close_window=True, status_timeout_s=8.0)
final = run_completion_engine_and_export(
    client,
    server_subdir=args.bkp_subdir,
    script_stem=SCRIPT_STEM,
    task_key=args.task_key,
    export_bkp=False,
)
per_error = final.get(&quot;per_error&quot;)
run = final.get(&quot;engine_run&quot;)
```

Before `engine_run`, call `ui_check_next_completion_status` at least once and
store the payload in `summary.json`.

For generated scripts, prefer the final-stage helper:

```python
final = run_completion_engine_and_export(
    client,
    server_subdir=args.bkp_subdir,
    script_stem=SCRIPT_STEM,
    task_key=args.task_key,
    export_bkp=False,
)
```

It returns `completion`, `engine_run`, `per_error`, and REP/APW `evidence`.

Common RStoic helpers:

```python
configure_rstoic_stoichiometry(
    client,
    block_name=&quot;R1&quot;,
    reaction_number=1,
    reactants={&quot;BENZ&quot;: 1.0, &quot;H2&quot;: 3.0},
    products={&quot;CH&quot;: 1.0},
)
configure_rstoic_fractional_conversions(
    client,
    block_name=&quot;R1&quot;,
    conversions=[{&quot;reaction_number&quot;: 1, &quot;component_id&quot;: &quot;BENZ&quot;, &quot;conversion&quot;: 0.75}],
)
configure_rstoic_calculated_heat_reference(
    client,
    block_name=&quot;R1&quot;,
    rows=[
        {
            &quot;reaction_number&quot;: 1,
            &quot;reference_component_id&quot;: &quot;BENZ&quot;,
            &quot;reference_phase&quot;: &quot;V&quot;,
        },
    ],
    reference_temperature=298.15,
    reference_temperature_unit=&quot;K&quot;,
    reference_pressure=1.0,
    reference_pressure_unit=&quot;atm&quot;,
)
configure_rstoic_flash(
    client,
    block_name=&quot;R1&quot;,
    spec_opt=&quot;TP&quot;,
    temperature=200.0,
    temperature_unit=&quot;C&quot;,
    pressure=20.0,
    pressure_unit=&quot;bar&quot;,
)
```

Pass positive magnitudes to `reactants`; the helper sends negative Aspen
stoichiometric coefficients for reactants and positive coefficients for
products.

Common REquil helper:

```python
configure_requil_equilibrium_reactions(
    client,
    block_name=&quot;R1&quot;,
    nphase=2,
    spec_opt=&quot;TP&quot;,
    temperature=450.0,
    temperature_unit=&quot;F&quot;,
    pressure=1.0,
    pressure_unit=&quot;atm&quot;,
    reactions=[
        {
            &quot;reaction_number&quot;: 1,
            &quot;reactants&quot;: {&quot;MEOH&quot;: 1.0},
            &quot;products&quot;: {&quot;CO&quot;: 1.0, &quot;H2&quot;: 2.0},
            &quot;delta&quot;: 0.0,
        },
        {
            &quot;reaction_number&quot;: 2,
            &quot;reactants&quot;: {&quot;CO&quot;: 1.0, &quot;H2O&quot;: 1.0},
            &quot;products&quot;: {&quot;CO2&quot;: 1.0, &quot;H2&quot;: 1.0},
            &quot;delta&quot;: 0.0,
        },
    ],
)
```

For REquil, never set only `set_opt_ext_delt` / `set_delt`. The reaction
stoichiometry table must be written with `set_block_reaction_stoichiometry`
first, otherwise the block stays input-incomplete and will block the flowsheet.
Prefer `SPEC_OPT=&quot;TP&quot;` when the task states reactor temperature and pressure.
Using `PD` with arbitrary zero duty can pass input completion but fail at runtime
with `UNABLE TO FIND OUTLET TEMPERATURE`.
After REquil reaction setup, probe `check_block_completion(client, &quot;R1&quot;)` and do
not bypass an incomplete REquil by exporting only a separate RGibbs block.

Evidence export:

```python
client.invoke(&quot;export_rep&quot;, filename=&quot;output/subdir/run.rep&quot;, export_format=2)
client.invoke(&quot;export_apw&quot;, filename=&quot;output/subdir/run.apw&quot;)
# Optional debug evidence only; not required for script-agent success:
# client.checkpoint(filename=&quot;output/subdir/run.bkp&quot;)
```

`summary.json` should include a top-level `evidence` dict with non-empty
`rep_path` and `apw_path` after successful export. `bkp_path` may be null.

```

### FILE: docs/hardcoded_script_plan/evidence_finalization_tools.md
Reason: core hardcoded script/runtime contract
```text
# Evidence Finalization Tools

Use this note when generated hardcoded scripts need trusted Aspen evidence.

## Preferred Finalization Helper

Generated scripts should prefer `run_completion_engine_and_export(...)` from
`runtime/script_agent_experiment/script_agent_exp/safe_aspen_calls/`.

The runtime parent owns canonical import roots. Generated code must not scan
repository parents, mutate `sys.path`, or fall back to the legacy experiments
package. In slim mode, declare `TASK_SPEC` and use `configure(runtime)`;
`run_slim_task` owns finalization rather than a generated finalizer scaffold.

Typical per-case call:

```python
from script_agent_exp.safe_aspen_calls import run_completion_engine_and_export

final = run_completion_engine_and_export(
    client,
    server_subdir=f&quot;script_agent_experiment/{SCRIPT_STEM}/{case_key}&quot;,
    script_stem=f&quot;{SCRIPT_STEM}_{case_key}&quot;,
    task_key=f&quot;{task_key}_{case_key}&quot;,
    required_streams=[&quot;F1&quot;],
    required_blocks=[&quot;H1&quot;, &quot;PF&quot;, &quot;H2&quot;, &quot;AD&quot;, &quot;H3&quot;, &quot;V1&quot;, &quot;V2&quot;],
)
```

Record the returned object directly in the case summary:

- `case[&quot;engine_run&quot;] = final[&quot;engine_run&quot;]`
- `case[&quot;per_error&quot;] = final[&quot;per_error&quot;]`
- `case[&quot;run_status&quot;] = final[&quot;run_status&quot;]`
- `case[&quot;evidence&quot;] = final[&quot;evidence&quot;]`
- `case[&quot;completion&quot;] = final[&quot;completion&quot;]`

Then derive gates from the returned fields:

- `PER_ERROR=0`: `final[&quot;per_error&quot;][&quot;value&quot;] == 0`
- REP exists: `final[&quot;evidence&quot;][&quot;rep_path&quot;]`
- APW exists: `final[&quot;evidence&quot;][&quot;apw_path&quot;]`
- REP convergence: parse `final[&quot;evidence&quot;][&quot;rep_path&quot;]` with `rep_parser.parse_problem_status`.

## Why This Helper

`engine_run.success=true` only means the COM call returned. It does not prove the
Aspen Results Summary was populated or that a REP can be exported. The helper
centralizes:

- required-input readiness probing,
- one UI Next completion pass,
- engine run,
- trusted Run-Status / `PER_ERROR` readback,
- bounded REP export,
- APW export.

## Rules

- Do not hand-write repeated `export_rep` loops. The helper already performs a bounded export policy.
- Do not pass `export_bkp=True` to final run/export helpers. APW is the evidence handoff artifact; BKP/checkpoint export is reserved for explicit qualified base-input or diagnostic workflows.
- Treat APW export as the final tolerant artifact step. REP/run-status/PER_ERROR diagnostics must be captured before APW `SaveAs`; an APW COM/RPC failure should be recorded as `evidence.apw_export_error` or `evidence.infrastructure_blocker`, not used to discard earlier run evidence.
- Skip APW export for untrusted runs (`PER_ERROR` unavailable/nonzero or severe translator/history errors). Record `evidence.apw_export_skipped_reason`; do not force `SaveAs` on a failed COM session for diagnostic rows.
- If APW export fails after an engine run, do not call `engine_run` again on the same client/session. Aspen COM may already be unhealthy; preserve the existing `engine_run`, `run_status`, `per_error`, and history payloads.
- Do not treat `APW` as a substitute for `REP` when the task gate requires REP evidence.
- If `REP export produced no file`, keep the case failing and record `evidence.rep_export_error`; do not synthesize a placeholder `.rep`.
- For Optimization that changes manipulated feed/solvent flow, export REP **after**
  `collect_optimization_results(...)` (or an equivalent final `engine_run`) on the
  same topology. Do not validate product/recycle purities from a pre-optimization
  base-case REP.
- When the task gives minimum stream purities, verify them with
  `collect_rep_stream_purity_evidence(...)` or equivalent REP stream-table
  parsing on that final REP.
- For multi-case sweeps, call the helper once per case after the numeric case inputs are updated and the engine is reinitialized if needed.
- For numeric-only case changes after proven topology, skip repeated UI Next outside this helper. The helper itself may run one final completion check per case.
- Use unique `server_subdir`, `script_stem`, and `task_key` per case so APW/REP artifacts do not overwrite or mix.

## Summary Shape

For a three-case thesis task, write:

```json
{
  &quot;cases&quot;: [
    {
      &quot;case_key&quot;: &quot;araby&quot;,
      &quot;crude&quot;: &quot;Araby&quot;,
      &quot;engine_run&quot;: {},
      &quot;per_error&quot;: {&quot;value&quot;: 0},
      &quot;run_status&quot;: {},
      &quot;evidence&quot;: {
        &quot;rep_path&quot;: &quot;...&quot;,
        &quot;apw_path&quot;: &quot;...&quot;
      },
      &quot;rep_converged&quot;: true,
      &quot;product_streams_m3_d&quot;: {},
      &quot;column_readbacks&quot;: {}
    }
  ],
  &quot;evidence_gate&quot;: {
    &quot;all_cases_have_rep_apw&quot;: true,
    &quot;all_cases_per_error_zero&quot;: true,
    &quot;all_cases_rep_converged&quot;: true
  }
}
```

The top-level `summary[&quot;evidence&quot;]` may point to the final case or contain
`case_evidence`, but each case must still carry its own evidence paths.

## MD-first base-case readback (own-agent)

After a trusted `run_completion_engine_and_export(...)` / `PER_ERROR=0` run:

1. Declare `rep_readback_targets` for every task-critical stream/block/derived/profile metric.
2. Call **`finalize_task_summary_with_llm_rep_readback(...)` once** with `final_bundle=final`.
3. Write `summary.json`; artifacts should include `artifacts/rep_readback_evidence.md`.

Do **not**:

- call `collect_llm_rep_readback_evidence(...)` before merging `final_bundle` (causes `run_not_trusted`);
- hand-populate `summary.readbacks` / structured `summary.results` as the scored answer;
- maintain `final_results_completeness_gate` manually — framework sets `evidence_gate.rep_readback_complete`.
- run a second direct `read_stream_output` / `typed readback helper such as read_stream_output(...)` evidence path for final scored stream or block metrics after REP evidence is collected. If those direct calls fail, keep their payloads as diagnostics only; do not recursively extract numeric values from failure payloads or let them override REP Markdown.
- compute final derived gates, such as feed `q=(H_Vsat-H_F)/(H_Vsat-H_Lsat)`, from direct readback attempts when the raw inputs are present in `rep_readback_evidence`. Use the REP-read raw targets and record the formula/source request IDs.

Validator authority for base-case display/numeric checks is
`validate_rep_readback_evidence_gate` reading the Markdown. Probe matrices and
native SA/OPT/DS evidence chains are unchanged.

```

### FILE: docs/hardcoded_script_plan/rep_parser_helper_contract.md
Reason: core hardcoded script/runtime contract
```text
# REP Parser Helper Contract

Generated scripts should not copy or reimplement REP parsers. Import the stable
helpers from `script_agent_exp.safe_aspen_calls`, which re-exports the parser
implementation from `healthcheck.full_example.rep_parser`.

```python
from script_agent_exp.safe_aspen_calls import (
    build_agent_visible_rep_text,
    load_rep,
    parse_block_heat_duty_watt,
    parse_block_theoretical_stages,
    parse_problem_status,
    parse_radfrac_liquid_x_profile,
    parse_stream_section,
)
```

## Core Calls

### `load_rep(path: str) -&gt; str`

Read a textual Aspen `.rep` file. Use this for the `evidence.rep_path` produced
by `run_completion_engine_and_export(...)` or `finalize_task_summary(...)`.

### `parse_problem_status(rep_text: str) -&gt; dict`

Return a convergence summary:

```python
status = parse_problem_status(rep_text)
converged = bool(status.get(&quot;converged&quot;))
hints = status.get(&quot;hints&quot;) or []
```

Use this to support final `rep_converged` / problem-status evidence.

### `parse_stream_section(rep_text: str) -&gt; dict[str, RepStreamRow]`

Parse Aspen stream summary tables, including paginated stream tables. Each row
has fields such as:

- `stream_id`
- `components_kmol_s`
- `total_kmol_s`
- `total_kg_s`
- `temp_k`
- `pres_n_sqm`
- `vfrac`
- `enthalpy_watt`
- `phase`

Example:

```python
rep_text = load_rep(final[&quot;evidence&quot;][&quot;rep_path&quot;])
streams = parse_stream_section(rep_text)
outlet = streams.get(&quot;P1&quot;)
water_kmol_s = (outlet.components_kmol_s or {}).get(&quot;WATER&quot;) if outlet else None
```

## Task-Specific Helpers

### `parse_block_heat_duty_watt(rep_text: str) -&gt; dict[str, float | None]`

Best-effort block heat-duty extraction from the U-O-S block section. Use for
HeatX, Heater, condenser/reboiler, and similar duty readbacks when direct Aspen
tree readbacks are unavailable or need REP corroboration.

### `parse_block_theoretical_stages(rep_text: str, *, block_name: str) -&gt; float | None`

Best-effort stage/tray count extraction for shortcut or column blocks. Use for
DSTWU/RadFrac comparison evidence when the task asks for theoretical stages.

### `parse_radfrac_liquid_x_profile(rep_text: str, *, block_name: str, component_ids: list[str]) -&gt; dict`

Best-effort RadFrac liquid mole-fraction profile extraction. Use when the task
asks for composition profiles or stagewise liquid composition evidence.

### `build_agent_visible_rep_text(rep_text: str, *, max_chars: int = 18000) -&gt; str`

Create a compact REP excerpt with the flowsheet, block, stream, and problem
status sections. Use it only for bounded diagnostics or report snippets; keep
large raw REP text out of `summary.json`.

## Rules

- Do not paste parser source code into generated scripts.
- Do not implement ad hoc stream-table parsers unless a required value is not
  covered by these helpers; record a blocker if the helper cannot read it.
- Keep final evidence tied to the same REP/APW generated by the final Aspen run.
- Prefer parsed REP values or direct Aspen readbacks over hard-coded textbook
  answers.

```

### FILE: docs/hardcoded_script_plan/safe_aspen_calls_core_helpers.md
Reason: descriptor-selected safe Aspen helper catalog
```text
# Safe Aspen Calls Core Helper Catalog

This catalog is always safe to include in own-agent init prompts. It contains
generic helper contracts used by most generated scripts. Specialized RadFrac,
analysis, probe, and heat-cascade helpers live in separate complete catalogs.

## Unified Capability Invocation

Default to `client.invoke(&quot;capability&quot;, **params)` for registered capabilities.
It returns a `status`/`result` envelope. Local Python helpers and native HTTP
operations use the same capability registry; generated code need not decide
which transport implements a registered capability.

Use `safe.call(client, &quot;capability&quot;, **params)` for strict execution: it checks
the routed outcome and unwraps the result payload. Use
`safe.probe_call(client, &quot;capability&quot;, **params)` for diagnostics through the
same registry; incomplete completion probes are evidence, not automatically
fatal setup exceptions. Existing typed `safe.func(client, ...)` calls remain
supported. `client.execute(...)` is a compatibility entry into the unified
route. `client.execute_http(...)` is internal native-only transport, never a
generated-script shortcut.

Use exact supported names and parameter shapes. Unqualified registered names
follow registry `default_route` metadata: same-name native forwarders retain an
HTTP default, not a universal local-first rule. `local:name` explicitly selects
the registered Python helper; `http:name` selects a valid native identity and
rejects local-only helpers. Unknown `local:` names fail. Unregistered unqualified
names retain legacy HTTP dispatch; that is identity selection, not fallback
after failure. Bad local parameters and local-helper failures never retry as
HTTP. Do not assume every alias is registered, portable, or available on every
deployment. Inspect the registered helper signature before calling a local
identity; native-default parameter contracts may differ.
Python-only helper documentation still describes implementation, not an HTTP
wire operation; it does not forbid unified invocation of a registered helper.

Routing does not bypass the safe raw-operation policy. Generated scripts must
not access raw tree or atomic analysis operations through any spelling or
namespace; prefer high-level transactions or record a blocker.

## Pure REP Declarations And Summary Ownership

`stream_rep_targets` / `block_rep_targets` belong to `script_agent_exp.slim_task_runtime`.
They take no client and create request declarations, not operations. Lazy `safe` exports
support existing generated imports only; these names are rejected by capability/HTTP routing.
Do not remove required evidence or retry arbitrary unknown helpers over HTTP.

`finalize_task_summary` returns a detached complete summary. Replace the caller summary,
not a stage child; never insert a live summary into itself. Local capability results also
snapshot containers before returning an envelope. Cyclic inputs are contract failures with
edge/ancestor paths, not JSON values to stringify; preserve the underlying model failure.

## Session And Recorder

Use `AspenHttpClient(server_url=server_url, task_hash=task_hash, task_name=task_name, recorder=recorder)`.
Keep one `JsonlRecorder` in the same output subtree as `summary.json`.

Call `client.ensure_session(...)` before model mutation. Use `inset=&quot;SI&quot;` or
another legal built-in unit set through `ensure_session`; do not write INSET
through raw tree access.

## Components And Properties

Use CAS-based component landing helpers when real chemicals are known. After
adding components, verify the visible component table before writing stream
composition, reactions, or downstream specs.

Use documented property-method helpers. Do not invent raw tree writes for global
or block-local property methods.

After `ensure_property_method(..., method=&quot;SRK&quot;)`, call registered
`safe.configure_srk_free_water_steamnbs(client)` for STEAMNBS/default-STEAM-TA.
Local Python helper, callable through unified invocation when registered, not
an HTTP wire operation. The helper internally uses `typed helper write surface`/`typed readback helper such as read_stream_output(...)` on
`\Data\Properties\Specifications\Input\GFREE_WATER`. Require setter success +
STEAMNBS readback; `FREE_WATER` returns `AE_UNDERSPEC`. Preserve live options.
SRK overrides fail: trusted raw zero/cleared warning, export, cold-reload.
Expected local-property comparison policy stays unchanged.

## Stream State And Completion

Material streams must specify exactly two of temperature, pressure, and vapor
fraction, plus one flow/composition basis. Choose `TP`, `PV`, or `TV` to match
the actual pair.

Use completion probes after setup stages. Completion probe payloads are evidence
even when they report incomplete input; do not raise only because a probe found
missing fields.

## Component-Specific Probe Readbacks

For product-purity probes, request the actual component fraction explicitly:

```python
purity = client.invoke(
    &quot;read_stream_output&quot;,
    stream_name=&quot;P1&quot;,
    variable=&quot;mole_fraction&quot;,
    component_name=&quot;ETOH&quot;,
)
```

A default stream-state snapshot (temperature, pressure, vapor fraction, total
flow) is not component-purity evidence. Preserve the readback unit/basis and
trusted-run provenance; final scored evidence still follows the final REP
readback contract below.

## Run And Export

For final evidence, prefer:

```python
final = client.invoke(&quot;run_completion_engine_and_export&quot;,
    required_streams=REQUIRED_STREAMS,
    required_blocks=REQUIRED_BLOCKS,
    server_subdir=args.bkp_subdir,
    script_stem=SCRIPT_STEM,
    task_key=args.task_key,
    export_bkp=False,
)
```

`engine_run.success=true` is not enough. Trusted success requires run-status
evidence, `PER_ERROR`, REP/APW paths when required, and convergence/problem
status from the same run.

## Final Summary

Use `safe.finalize_task_summary(...)` or
`safe.finalize_task_summary_with_llm_rep_readback(...)` after the final run
bundle is available. Keep final evidence structured; do not write human-readable
answer Markdown from generated scripts.

For scored final metrics after a trusted run, declare readback targets and call
`finalize_task_summary_with_llm_rep_readback(...)` once after merging the final
bundle. Do not hand-populate scored numeric readback fields from raw parser code.

```

### FILE: docs/hardcoded_script_plan/safe_aspen_calls_analysis_helpers.md
Reason: descriptor-selected safe Aspen helper catalog
```text
# Safe Aspen Calls Analysis Helper Catalog

Use this complete catalog when the task profile explicitly includes native
Design Spec, Sensitivity, Optimization, or Constraint families.

## Design Spec Helpers

Use high-level helpers only:

- `configure_design_spec_stream_var_vs_stream_var(...)`
- `configure_design_spec_stream_var_vs_block_var(...)`
- `configure_design_spec_block_var(...)`
- `configure_design_spec_block_var_with_options(...)`
- `ds_configure_stream_massfrac_vs_stream_massflow(...)`
- `collect_design_spec_results(...)`

Do not call raw Design Spec HTTP operations or table setters from generated
scripts. Final reported target and manipulated values must come from the
post-Design-Spec Aspen run, not from seeds or setter receipts.

## Sensitivity Helpers

For decision exploration, prefer:

```python
suite = client.invoke(&quot;configure_sensitivity_exploration_suite&quot;,  suite_name=suite_name, sweeps=sweeps, summary=summary,
    collect=True, decision_basis=decision_basis,
)
# The suite owns collection and records per-Sensitivity evidence in summary.
# Inspect configuration_status separately if whole-request success is false.
```

Use stream-variable sweeps for material stream feed, solvent, makeup, or utility
flow handles. Use block-variable sweeps only when the manipulated surface is
actually block-owned.

The suite returns `schema_version=&quot;sensitivity_configuration_transaction.v1&quot;`.
`configuration_status` is `configured`, `partial`, or `failed`; inspect
`configuration_success`, `required_steps`, and `configuration_errors` for required
configuration/Fill failures. `success` retains whole-request semantics (including
collection/selection/replay when requested). All legacy keys remain available.
A legacy setter batch without top-level `success` requires explicit success on
all expected setters; required false/unknown/missing results fail. Optional diagnostic
false values are not recursively aggregated. `collect=False` supports zero-LLM
configuration probes, not proof of populated output or solver participation.

Sensitivity evidence is useful only when output rows/artifacts exist and the
reported decision cites those rows or their canonical Markdown evidence.
`native_output_status` and `solver_participation_status` are separate from
configuration; solver participation remains `not_verified` until same-run evidence
establishes it. These are API/evidence semantics, not an iteration/retry policy.

## Optimization Helpers

Use high-level optimization helpers:

- `configure_optimization_block_var(...)`
- `configure_optimization_block_var_with_options(...)`
- `configure_optimization_multi_block_var_objective(...)`
- `configure_optimization_constrained_stream_var_minimize_flow(...)`
- `collect_optimization_results(...)`
- `attach_optimization_results_to_summary(summary, collected)`
- `collect_rep_stream_purity_evidence(...)`

When optimization selects a manipulated variable, preserve helper payloads such
as `selected_manipulated.success` and `result_source_contract`.

Do not pass unsupported keyword aliases such as `target_block` to optimization
helpers. Use the documented helper signature fields only.

## Optional offline configure/bind preflight

`script_agent_exp.native_analysis_preflight.preflight_native_analysis_configuration(contract, enabled=True)`
is a pure, opt-in configuration evidence check, not an Aspen operation. Its default
is disabled. It never launches COM, executes a model, or calls an LLM. Supply the
task-required family (`DESIGN_SPEC`, `SENSITIVITY`, or `OPTIMIZATION`), task intent,
current task/session context, high-level configure/group receipts, active readback,
and every sampled/objective/manipulated binding. Each binding records the owner,
VARTYPE, exact native live options/source, selected token/readback, unit
options/readback, and discovered Sentence/ID1 requirements/options/readbacks.
Block-setter aliases are not native option evidence. Missing unit evidence stays
unresolved; use the existing quantity registry for numeric conversion upstream.

`resolve_selected_live_option(options, requested=..., patterns=...)` accepts exact
live tokens or a unique match to explicitly supplied task patterns; ambiguous
matches and unmatched synonyms fail. The stream-target/block-vary DS helper uses
this resolver before setting the pair. No fallback-first option or answer-based
alias map is introduced. Keep using the existing high-level DS/SA/OPT helpers;
this preflight does not replace their setters, helper-managed Sensitivity tabulation, or collectors.

In slim own-agent only, required native configuration failures with hash-verified
current-run artifacts are selected before convergence/probe planning. With explicit
`SCRIPT_AGENT_SLIM_NATIVE_BIND_REPAIR_MAX=1` authorization, the execution boundary
(seed/initial/repair/source-only continuation) routes known structured binding
codes to `native_analysis_variable_contract`, a paid subtype of the in-iteration
Ruff repair infrastructure, not fabricated lint. Load the dedicated
`aspen_agent_skills/guides/native-analysis-variable-contract-repair/SKILL.md`.
The ordinary mini remains capped at one response; this specialist has its own
one-request durable claim, usage ledger, receipt and separate strict-identity
replay root. Provider/parse/apply/replay failure stops with no reissue or second
generic mini. The default specialist cap is zero; ordinary own-agent is unchanged.
No fresh discovery/model execution is launched merely by importing this module.
A successful preflight proves only configuration binding, never native solver
participation or target/optimum attainment. Next completion, trusted active run,
and native postsolve output/result-use validation remain mandatory.

## Final Evidence Chain

Native analysis setup is not final evidence by itself. The final path is:

1. configure the native object through helpers;
2. run Aspen or collect helper-owned run evidence;
3. collect native outputs/readbacks;
4. run/export the selected final state when required;
5. bind reported results to native output and trusted final readbacks.

```

### FILE: docs/hardcoded_script_plan/safe_aspen_calls_radfrac_helpers.md
Reason: descriptor-selected safe Aspen helper catalog
```text
# Safe Aspen Calls RadFrac Helper Catalog

Use this complete catalog when the task profile explicitly includes `RADFRAC`.

## Standard Column Setup

For ordinary total-condenser/kettle columns, prefer:

```python
client.invoke(&quot;configure_radfrac_total_condenser&quot;,
    block_name=&quot;D1&quot;,
    feed_stream=&quot;F1&quot;,
    nstage=20,
    feed_stage=10,
    reflux_ratio=1.5,
    distillate_flow=1.0,
    distillate_flow_unit=&quot;kmol/hr&quot;,
    top_pressure=1.0,
    pressure_unit=&quot;atm&quot;,
)
```

Use the declared keyword names `nstage`, `distillate_flow`, and `top_pressure`;
`feed_stream` is required. The flow unit belongs in `distillate_flow_unit`, and
column pressure uses `pressure_unit`. These illustrative values are not task
answers. Do not invent aliases or raw tree paths when a helper owns the setup.
The runtime parent supplies canonical imports; do not generate a `sys.path`
bootstrap or use legacy experiments-package fallbacks.

If a task, reference BKP, or live readback shows explicit `PRES1` / `PRES2`
pressure rows, use `bottom_pressure_mode=&quot;pres2&quot;` with
`configure_radfrac_total_condenser(...)`, or call `client.execute(&quot;set_pres2&quot;,
...)` directly after `set_pres1`. The default helper behavior keeps historical
`DP-COL` semantics for `bottom_pressure`; it is not a substitute for probing
`PRES2` when the Aspen file&#x27;s pressure surface is TOP-BOTTOM / P-SPEC2.

For all-fail RadFrac probes, pressure profile is a first-class axis:
`set_pres1`-only, explicit `set_pres1` + `set_pres2`, and `DP-COL` can be
distinct Aspen models. Record `read_pressure_state(...)` or REP pressure-profile
evidence before claiming that a stage/feed/recycle probe exhausted the space.

## Extractive And Absorber-Like Columns

For extractive distillation, use
`configure_radfrac_extractive_distillation_pair(...)` when the task requires a
solvent/extractive RadFrac pair.

For no-condenser or absorber-like service, use the corresponding high-level
helpers and role-specific skills. Preserve condenser/reboiler semantics from the
task instead of adding end effects only to converge.

## Feed Convention

After setting feed stages, configure per-feed convention with the Python helper:

```python
client.invoke(&quot;configure_radfrac_feed_convention&quot;,
    block_name=&quot;D1&quot;,
    stream_name=&quot;F1&quot;,
    convention=&quot;ON-STAGE&quot;,
)
```

It is not an Aspen HTTP operation; do not call it through `client.execute(...)`.

Treat feed convention as part of the probe surface, not just a fixed afterthought.
For difficult RadFrac convergence or translation failures, test stage/convention
bundles such as `ON-STAGE` versus `ABOVE-STAGE`, plus `VAPOR` / `LIQUID`
or generated-token equivalents such as `ON-STAGE-VAP` / `ON-STAGE-LIQ` when the
live legal-values response supports them. Do this with a small headless matrix;
do not put GUI/F4/Next checks inside each row.

## Profile And Product Evidence

For profile tables, use `collect_radfrac_profile_markdown_evidence(...)`. When a
plot is required, use `collect_radfrac_profile_plot_evidence(...)` or provide a
real generated plot artifact path.

Final product compositions, reflux ratio, internal flows, condenser metrics, and
derived ratios must come from trusted current-run output or REP evidence.

```

### FILE: docs/hardcoded_script_plan/safe_aspen_calls_heat_cascade_helpers.md
Reason: descriptor-selected safe Aspen helper catalog
```text
# Safe Aspen Calls Heat-Cascade Helper Catalog

Use this complete catalog when explicit task-profile families or descriptors
select heat-stream, HeatX, MHeatX, Flash2 evaporator, or multi-effect heat-duty
work.

## Heat Stream Duty

Heat streams created by `create_heat_stream` live under `Data\Streams\&lt;Q&gt;` with
heat-stream semantics. Use helper calls for duty writes:

```python
client.invoke(&quot;configure_heat_stream_duty&quot;,
    stream_name=&quot;Q1&quot;,
    duty=1.5e7,
    unit=&quot;Watt&quot;,
)
```

For cascades:

```python
client.invoke(&quot;configure_heat_stream_duty_map&quot;,
    duties_by_stream={&quot;Q1&quot;: 2.0e7, &quot;Q2&quot;: 1.5e7},
    unit=&quot;Watt&quot;,
)
```

Do not use temperature setters as duty substitutes.

## HeatX And MHeatX

For shortcut HeatX targets, use `configure_heatx_shortcut_target(...)`. For
detailed shell-and-tube rating tasks, use
`configure_heatx_detailed_shell_tube_rating(...)`.

For one hot stream and multiple cold streams, use `configure_mheatx_multi_stream(...)`.
Do not parse human-readable port messages as port names.

After run, use `collect_heatx_result_evidence(...)` for duty, U, area, and side
result evidence.

Use `read_heatx_side_film_coefficients(...)` when side-specific film coefficient
evidence is required, `read_heater_duty(...)` for heater duty readback, and
`read_dstwu_shortcut_basis(...)` only when a shortcut-column comparison is
explicitly part of the same task.

## Multi-Effect Evidence

Use `validate_heat_cascade_connected(...)` to prove heat-stream connectivity and,
when required, nonzero duty participation.

Use `collect_multi_effect_case_evidence(...)` to record product water fraction,
per-effect duty, optional HeatX evidence, and heat-cascade participation in a
single structured result.

```

### FILE: docs/hardcoded_script_plan/block_type_inject/streams_globals.md
Reason: generic stream/global Aspen surface
```text
# Block-Type [NON-ENGLISH REDACTED]：Streams &amp; Globals（[NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED]）
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] completion [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] `docs/hardcoded_script_plan/block_type_inject/heat_stream.md`。

---

## 0. Helper

| Helper | [NON-ENGLISH REDACTED] |
|--------|--------|
| `configure_block_property_method(...)` | [NON-ENGLISH REDACTED]（block-wise property） |
| `ensure_property_method(...)` / `read_global_property_method(...)` | [NON-ENGLISH REDACTED] ensure + readback |
| `configure_inset_unit_system(...)` | [NON-ENGLISH REDACTED] INSET（**[NON-ENGLISH REDACTED]**；**Python-only**，[NON-ENGLISH REDACTED] `client.execute(...)`） |
| [NON-ENGLISH REDACTED] helper | `set_mixed_spec_mixed` + `set_basis_mixed` + [NON-ENGLISH REDACTED]/TP [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED] material stream MCP） |

**`configure_inset_unit_system` [NON-ENGLISH REDACTED]**：

```python
# [NON-ENGLISH REDACTED] A：session [NON-ENGLISH REDACTED] ensure_session [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED]）
client.ensure_session(show_gui=False, inset=&quot;SI&quot;)   # [NON-ENGLISH REDACTED] inset=&quot;ENG&quot;

# [NON-ENGLISH REDACTED] B：[NON-ENGLISH REDACTED] helper
client.invoke(&quot;configure_inset_unit_system&quot;,  value=&quot;SI&quot;)
# path: Data\Setup\Global\Input\INSET
# [NON-ENGLISH REDACTED]：SI | ENG | ENGUS | MET | SI-CHEM | MET-CHEM
# [NON-ENGLISH REDACTED] Data\Setup\System-Options\Input\INSET [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]
```

---

## 1. [NON-ENGLISH REDACTED]（CRITICAL）

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| `set_property_method` / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] + [NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] TP/[NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] Input | [NON-ENGLISH REDACTED] completion [NON-ENGLISH REDACTED] |
| `check_next_completion_status` | `engine_run` | [NON-ENGLISH REDACTED] workflow [NON-ENGLISH REDACTED] |

---

## 2. Core MCP / HTTP Operations

### 2.1 [NON-ENGLISH REDACTED]

| MCP operation | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|---------------|------|------|
| `add_components_by_cas` | `components: [{cas, component_id}]` | **[NON-ENGLISH REDACTED]** [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED] benchmark [NON-ENGLISH REDACTED]） |
| `set_property_method` | `method: str` | [NON-ENGLISH REDACTED] |

### 2.2 [NON-ENGLISH REDACTED]

| MCP operation | Aspen [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|---------------|------------|---------------|------|
| `create_material_stream` | — | `stream_name` | [NON-ENGLISH REDACTED] |
| `set_mixed_spec_mixed` | [NON-ENGLISH REDACTED] | `TP`/`TV`/`PV`/… | [NON-ENGLISH REDACTED] T/P/[NON-ENGLISH REDACTED] |
| `set_basis_mixed` | [NON-ENGLISH REDACTED] | `MOLE-FLOW`/`MASS-FLOW`/… | [NON-ENGLISH REDACTED] |
| `set_temp_mixed` | TEMP | float + unit | [NON-ENGLISH REDACTED] |
| `set_pres_mixed` | PRES | float + unit | [NON-ENGLISH REDACTED] |
| `set_flow_mixed` | [NON-ENGLISH REDACTED] | component + value + unit | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] |
| `set_vfrac_mixed` | VFRAC | float | [NON-ENGLISH REDACTED]（TV/PV [NON-ENGLISH REDACTED]） |

### 2.3 [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]：`docs/hardcoded_script_plan/block_type_inject/heat_stream.md`。[NON-ENGLISH REDACTED] heat stream / heat duty / utility heat topology / [NON-ENGLISH REDACTED]。

### 2.4 [NON-ENGLISH REDACTED]

| MCP operation | [NON-ENGLISH REDACTED] |
|---------------|------|
| `set_property_method` | [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED] §2.1） |
| `engine_reinit` / `engine_run` | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] |
| `ui_check_next_completion_status` | Next/completion [NON-ENGLISH REDACTED] |
| `export_rep` / `export_bkp` | [NON-ENGLISH REDACTED] |
| `table_dump` / `table_insert_label` | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] |

---

## 3. [NON-ENGLISH REDACTED] MCP

[NON-ENGLISH REDACTED] inject；[NON-ENGLISH REDACTED] `list_block_ports`、`connect_stream`。

---

## 4. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| [NON-ENGLISH REDACTED] T/P/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | `Data\Streams\&lt;S&gt;\Output\...` [NON-ENGLISH REDACTED] REP |
| [NON-ENGLISH REDACTED] | `ensure_property_method` / `read_global_property_method` readback payload |
| INSET | `safe.configure_inset_unit_system(client, value=...)` readback；[NON-ENGLISH REDACTED] `client.ensure_session(..., inset=&quot;SI&quot;)` |


---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] inject [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] stream setter [NON-ENGLISH REDACTED] core |

```

### FILE: docs/hardcoded_script_plan/aspen_component_id_hints.md
Reason: generic stream/global Aspen surface
```text
# Aspen Component ID Hints

This file centralizes small component naming hints for script-agent prompts.
Treat it as non-authoritative assistance: the task statement and Aspen
component/CAS lookup evidence remain the source of truth.

## Prefer Native Aspen Component IDs (Required)

When adding real chemicals through `add_components_by_cas`, use the **native
Aspen databank / CAS-lookup ID** as `component_id` whenever the lookup returns
one. Do **not** invent task-derived short aliases such as `ME`, `WA`, `GL`,
`ET`, or `EG`-style abbreviations for common species that Aspen already exposes
as `MEOH`, `H2O`, `WATER`, `ETHANOL`, `EG`, etc.

Rules:

- **Stream/block names** may follow Aspen-safe short patterns such as `H1`, `C1`,
  `HX`. That naming rule does **not** apply to component IDs.
- After `add_components_by_cas`, verify the visible component table and
  molecular-weight metadata before writing stream composition. If a custom alias
  lands without MW, retry with the native ID from this table or the CAS lookup
  result instead of proceeding.
- Local short IDs such as `BZ` or `TOL` are allowed only when the task or CAS
  landing evidence proves Aspen accepted that alias with full metadata. They are
  not a substitute for native IDs on common databank components.

## Common Direct IDs

Use these IDs when the task names the corresponding common component and Aspen
accepts the component:

| Component | Aspen ID | CAS |
| --- | --- | --- |
| Hydrogen | `H2` | `1333-74-0` |
| Nitrogen | `N2` | `7727-37-9` |
| Ammonia | `NH3` | `7664-41-7` |
| Water | `H2O` | `7732-18-5` |
| Methanol | `MEOH` | `67-56-1` |
| Benzene | `BENZENE` or local short ID `BZ` | `71-43-2` |
| Toluene | `TOLUENE` or local short ID `TOL` | `108-88-3` |
| Ethanol | `ETHANOL` or `ETOH` | `64-17-5` |
| n-Hexane | `N-HEXANE` | `110-54-3` |
| p-Xylene / paraxylene | `P-XYLEN` (databank name `P-XYLENE`) | `106-42-3` |
| Acetic acid | `ACETI-01` (databank name `ACETIC-ACID`) | `64-19-7` |
| Ethyl acetate | `ETHYL-01` (databank name `ETHYL-ACETATE`) | `141-78-6` |

## Task-Specific Component Sets

Task-specific CAS tables live in
`docs/hardcoded_script_plan/task_specific_component_cas.md`. Keep this file for
common reusable IDs and generic usage rules.

## Usage Rules

- Prefer native Aspen IDs from CAS lookup and the table above over guessed
  abbreviations from task text (`Water` -&gt; `H2O`, not `WA`; `Methanol` -&gt; `MEOH`,
  not `ME`).
- Prefer task-visible component names and CAS lookup helpers over guessing.
- If the generated script uses local short IDs such as `BZ` or `TOL`, record the
  mapping in `summary.json`.
- Do not silently substitute a different component just to satisfy completion.
- If a task needs pseudo-components or missing metadata repair, record the
  formula/molecular-weight assumption and prove the final Aspen evidence still
  matches the task intent.

```

### FILE: docs/hardcoded_script_plan/block_type_inject/property_methods.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：Property Methods（[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`PROPERTY_METHODS`（[NON-ENGLISH REDACTED]）
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]。

---

## 0. Helper

| Helper | [NON-ENGLISH REDACTED] |
|--------|--------|
| `ensure_property_method(...)` | [NON-ENGLISH REDACTED] ensure + readback |
| `read_global_property_method(...)` | [NON-ENGLISH REDACTED] GBASEOPSET/GOPSETNAME |
| `configure_block_property_method(...)` | [NON-ENGLISH REDACTED] UNIQUAC/NRTL/WILSON [NON-ENGLISH REDACTED]；**Python-only**，[NON-ENGLISH REDACTED] `client.execute(...)` |

---

## 1. [NON-ENGLISH REDACTED]（CRITICAL）

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| [NON-ENGLISH REDACTED] `set_property_method` | [NON-ENGLISH REDACTED] run | [NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | cas-lookup → add_components |
| [NON-ENGLISH REDACTED] OPSETNAME | [NON-ENGLISH REDACTED] Input | block-wise [NON-ENGLISH REDACTED] |

---

## 2. Core MCP / HTTP Operations

| MCP operation | Aspen [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|---------------|------------|---------------|------|
| `set_property_method` | [NON-ENGLISH REDACTED] | NRTL/UNIQUAC/WILSON/… | Setup [NON-ENGLISH REDACTED] |
| `set_opsetname` | `OPSETNAME` | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] Property Specification |

[NON-ENGLISH REDACTED] ensure/readback [NON-ENGLISH REDACTED] `safe.configure_block_property_method(client, block_name=..., method=...)`，[NON-ENGLISH REDACTED] §0。

---

## 3. [NON-ENGLISH REDACTED] MCP

[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] **distinct configured cases** + [NON-ENGLISH REDACTED] REP。

---

## 4. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| [NON-ENGLISH REDACTED] | block/global readback |
| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] case REP，[NON-ENGLISH REDACTED] bkp [NON-ENGLISH REDACTED] |


---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| [NON-ENGLISH REDACTED] helper | `configure_block_property_method` |
| [NON-ENGLISH REDACTED] skill | block-wise-property-methods |

```

### FILE: docs/hardcoded_script_plan/block_type_inject/heater.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：HEATER（[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`HEATER`
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] TP / PV [NON-ENGLISH REDACTED]。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper

[NON-ENGLISH REDACTED] helper；[NON-ENGLISH REDACTED] §2 MCP operation。

---

## 1. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| `set_heater_flash_spec` | `TEMP` / `PRES` / `VFRAC` | [NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] | Input | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] |

---

## 2. Core MCP / HTTP Operations

| MCP operation | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|---------------|------|---------------|------|
| `set_heater_flash_spec` | `SPEC_OPT` | [NON-ENGLISH REDACTED] §2.1 | [NON-ENGLISH REDACTED] gate |
| `set_heater_temperature` | `TEMP` | float + unit | [NON-ENGLISH REDACTED] |
| `set_heater_pressure` | `PRES` | float + unit | [NON-ENGLISH REDACTED]（&gt;0 [NON-ENGLISH REDACTED]；≤0 [NON-ENGLISH REDACTED]） |
| `set_heater_vapor_fraction` | `VFRAC` | float | **`SPEC_OPT=PV`** [NON-ENGLISH REDACTED] |
| `set_heater_duty` | `DUTY` | float + unit | `TQ`/`PQ`/`TD`/`PD` [NON-ENGLISH REDACTED] duty/heat [NON-ENGLISH REDACTED] |

### 2.1 `SPEC_OPT` / Operating Specification

**[NON-ENGLISH REDACTED] `set_heater_flash_spec`，[NON-ENGLISH REDACTED]**；selector [NON-ENGLISH REDACTED] setter [NON-ENGLISH REDACTED]。

| `SPEC_OPT` | [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED]） | [NON-ENGLISH REDACTED] |
|------------|-----------------|-------------|
| `TP` | Temperature + pressure | `TEMP` + `PRES` |
| `TV` | Temperature + vapor fraction | `TEMP` + `VFRAC` |
| `TD` | Temperature + heat duty | `TEMP` + `DUTY` |
| `TDPPARM` | Temperature + duty parameter | `TEMP` + duty-parameter [NON-ENGLISH REDACTED]/leaf |
| `PV` | Pressure + vapor fraction | `PRES` + `VFRAC` |
| `PD` | Pressure + heat duty | `PRES` + `DUTY` |
| `PDT` | Pressure + temperature change | `PRES` + [NON-ENGLISH REDACTED] leaf |
| `PDEGSUP` | Pressure + degrees superheat | `PRES` + [NON-ENGLISH REDACTED] |
| `PDEGSUB` | Pressure + degrees subcooling | `PRES` + [NON-ENGLISH REDACTED] |
| `VDPPARM` | Vapor fraction + duty parameter | `VFRAC` + duty-parameter |
| `DDPPARM` | Duty parameter（[NON-ENGLISH REDACTED] duty [NON-ENGLISH REDACTED]） | duty-parameter [NON-ENGLISH REDACTED] leaf |
| `DTV` | Temperature change + vapor fraction | [NON-ENGLISH REDACTED] + `VFRAC` |
| `DTD` | Temperature change + heat duty | [NON-ENGLISH REDACTED] + `DUTY` |
| `DTDPPARM` | Temperature change + duty parameter | [NON-ENGLISH REDACTED] + duty-parameter |
| `DEGSUPDPPARM` | Degrees superheat + duty parameter | [NON-ENGLISH REDACTED] + duty-parameter |
| `DEGSUBDPPARM` | Degrees subcooling + duty parameter | [NON-ENGLISH REDACTED] + duty-parameter |
| `PQ` | Pressure + heat/duty | `PRES` + heat stream / `DUTY` |
| `TQ` | Temperature + heat/duty | `TEMP` + heat stream / `DUTY` |
| `DTQ` | Temperature change + heat/duty | [NON-ENGLISH REDACTED] + heat stream / `DUTY` |
| `DPPARMQ` | Duty parameter + heat/duty | duty-parameter + heat/duty path |

**[NON-ENGLISH REDACTED]**：

- [NON-ENGLISH REDACTED] T、P → `TP`；[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] → `PV` + `set_vfrac=0` + `set_heater_pressure`。
- [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] → `PDEGSUP` / `PDEGSUB` [NON-ENGLISH REDACTED] `DEGSUP*` / `DEGSUB*` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `TP`。
- [NON-ENGLISH REDACTED] duty/[NON-ENGLISH REDACTED] → `TD`/`PD`/`TQ`/`PQ`/`DTQ` [NON-ENGLISH REDACTED] **Q [NON-ENGLISH REDACTED] D [NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] P* [NON-ENGLISH REDACTED] `TEMP`，[NON-ENGLISH REDACTED] T* [NON-ENGLISH REDACTED] `PRES`。
- `*PPARM` / `DPPARMQ` [NON-ENGLISH REDACTED] parameterized duty [NON-ENGLISH REDACTED]。

**[NON-ENGLISH REDACTED]**：`set_spec_opt=TP` [NON-ENGLISH REDACTED] `set_heater_temperature` [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED] Heater）。

**[NON-ENGLISH REDACTED]**：`set_spec_opt=PV` + `set_vfrac=0` + `set_heater_pressure`。

---

## 3. [NON-ENGLISH REDACTED] MCP

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| `create_heater` | `block_name` |
| `connect_stream` | [NON-ENGLISH REDACTED] `F(IN)` / `P(OUT)`；[NON-ENGLISH REDACTED] `HS(IN)`/`HS(OUT)` [NON-ENGLISH REDACTED] |
| `engine_run` | — |

Live `list_block_ports` [NON-ENGLISH REDACTED]：

```text
F(IN), HS(IN), P(OUT), WD(OUT), HS(OUT)
```

- `HS(IN): []` / `HS(OUT): []` [NON-ENGLISH REDACTED] heat port [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] heat stream。
- [NON-ENGLISH REDACTED] Heater [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] block duty，[NON-ENGLISH REDACTED] block-owned setter（`set_heater_flash_spec` + `set_heater_temperature`/`set_heater_pressure`/`set_heater_vapor_fraction`/`set_heater_duty`）[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] Q stream。
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `create_heat_stream` [NON-ENGLISH REDACTED] live `HS(IN)`/`HS(OUT)`，[NON-ENGLISH REDACTED] heat stream readback [NON-ENGLISH REDACTED] block duty/enthalpy change [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] Heater；[NON-ENGLISH REDACTED] energy topology，[NON-ENGLISH REDACTED] heat stream [NON-ENGLISH REDACTED] native duty path [NON-ENGLISH REDACTED] run，[NON-ENGLISH REDACTED] outlet temperature narrative。

---

## 5. [NON-ENGLISH REDACTED]

- [NON-ENGLISH REDACTED] Heater [NON-ENGLISH REDACTED] heat stream [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] duty / enthalpy change [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] **Compr** [NON-ENGLISH REDACTED]（`compr.md`）。

---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| Core setter | 4 |
| [NON-ENGLISH REDACTED] helper | — |

```

### FILE: docs/hardcoded_script_plan/block_type_inject/rstoic.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：RSTOIC（[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`RSTOIC`
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED] + [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

| Helper | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|--------|----------|------|
| `configure_rstoic_stoichiometry(...)` | `block_name`, [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] inline [NON-ENGLISH REDACTED] |
| `configure_rstoic_fractional_conversions(...)` | `block_name`, conversion rows | [NON-ENGLISH REDACTED] |
| `configure_rstoic_calculated_heat_reference(...)` | `block_name`, reaction rows, reference state | [NON-ENGLISH REDACTED] reference-condition bundle |
| `configure_rstoic_flash(...)` | `block_name`, [NON-ENGLISH REDACTED] `SPEC_OPT` [NON-ENGLISH REDACTED] | TP/TD/TV/PD/PV/DV |

---

## 1. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| `configure_rstoic_stoichiometry(...)` | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
| `SPEC_OPT` | [NON-ENGLISH REDACTED] TP/TD/TV/PD/PV/DV | [NON-ENGLISH REDACTED] PQ/TQ/VQ |

---

## 2. Core MCP / HTTP Operations

| MCP operation | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] |
|---------------|------|---------------|
| `set_rstoic_flash_spec` | `SPEC_OPT` | [NON-ENGLISH REDACTED] §2.1（**[NON-ENGLISH REDACTED]**） |
| `set_rstoic_temperature` | `TEMP` | float + unit |
| `set_rstoic_pressure` | `PRES` | float + **unit required**. Legal tokens include **`bar`**, `bara`, `barg`, `MPa`, `kPa`, `psia`, `mmHg`, … |
| `set_rstoic_duty` | `DUTY` | float + unit（`PD`/`DV` [NON-ENGLISH REDACTED]） |
| `set_heatopt` | `HEATOPT` | [NON-ENGLISH REDACTED] §2.2 |
| `set_heat_of_reac` | `HEAT_OF_REAC` | [NON-ENGLISH REDACTED] §2.3 |
| `set_opt_ext_conv` | `OPT_EXT_CONV` | **`CONVERSION`** \| `EXTENT` |
| `set_key_cid` | `KEY_CID` | [NON-ENGLISH REDACTED] ID（[NON-ENGLISH REDACTED]） |
| `set_conv` | `CONV` | float (0–1) |

### 2.1 `SPEC_OPT` / Flash Operating Specification

**[NON-ENGLISH REDACTED]**（Aspen RStoic Setup → Specifications）；**[NON-ENGLISH REDACTED]** `PQ` / `TQ` / `VQ` [NON-ENGLISH REDACTED] Flash2 [NON-ENGLISH REDACTED] token：

| token | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|-------|------|-------------|
| `TP` | Temperature + pressure | `TEMP` + `PRES` |
| `TD` | Temperature + duty | `TEMP` + `DUTY` |
| `TV` | Temperature + vapor fraction | `TEMP` + `VFRAC` |
| `PD` | Pressure + duty | `PRES` + `DUTY` |
| `PV` | Pressure + vapor fraction | `PRES` + `VFRAC` |
| `DV` | Duty + vapor fraction | `DUTY` + `VFRAC` |

Pressure + duty [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED]「0.3 MPa + 0 kW duty」）[NON-ENGLISH REDACTED] **`PD`**，[NON-ENGLISH REDACTED] `PQ`。[NON-ENGLISH REDACTED] COM [NON-ENGLISH REDACTED] GUI [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] HTTP `ui_set_rstoic_flash_spec_pq`（legacy [NON-ENGLISH REDACTED]）[NON-ENGLISH REDACTED] GUI [NON-ENGLISH REDACTED] `PD`。

**Bar-scale `PRES`（[NON-ENGLISH REDACTED] INSET [NON-ENGLISH REDACTED]）**：`set_pres(..., unit=&quot;bar&quot;)` [NON-ENGLISH REDACTED]。Meta [NON-ENGLISH REDACTED] `PRES = -0.1` [NON-ENGLISH REDACTED] **`unit=&quot;bar&quot;`**（absolute bar [NON-ENGLISH REDACTED] = [NON-ENGLISH REDACTED]）。[NON-ENGLISH REDACTED] bar [NON-ENGLISH REDACTED] MPa。[NON-ENGLISH REDACTED] `aspen-custom-unit-set` [NON-ENGLISH REDACTED] `bar_pressure_write_probe.py`。

### 2.2 `HEATOPT` / Heat Transfer Option

| token | [NON-ENGLISH REDACTED] |
|-------|------|
| `CONST-DUTY` | Constant duty |
| `CONST-TEMP` | Constant temperature |
| `LMTD` | Log mean temperature difference |
| `CONDENSING` | Condensing service |
| `EVAPORATING` | Evaporating service |
| `DYNAMIC` | Dynamic heat transfer |

### 2.3 `HEAT_OF_REAC` / Heat of Reaction

| token | [NON-ENGLISH REDACTED] |
|-------|------|
| `CALCULATE` | Aspen [NON-ENGLISH REDACTED] |
| `SPECIFY` | [NON-ENGLISH REDACTED] |
| `NO-CALC-SPEC` | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] |

When calculated heat is needed, do not call low-level reference-condition
setters directly. Use `configure_rstoic_calculated_heat_reference(...)` after
stoichiometry and conversion helper calls, then verify Next/completion clears
the Heat of Reaction page.

---

## 3. [NON-ENGLISH REDACTED] MCP

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| `create_rstoic` | `block_name` |
| `connect_stream` | F(IN), P(OUT) |
| `engine_run` | — |

---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| Core setter | §2 |
| [NON-ENGLISH REDACTED] helper | §0 [NON-ENGLISH REDACTED] |

```

### FILE: docs/hardcoded_script_plan/block_type_inject/flash2.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：FLASH2（[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`FLASH2`
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]；`SPEC_OPT` [NON-ENGLISH REDACTED] TP/TV/PV/TD/PD/TQ [NON-ENGLISH REDACTED]。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper

[NON-ENGLISH REDACTED] helper；[NON-ENGLISH REDACTED] §2 MCP operation。

---

## 1. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| `set_flash2_flash_spec` | T/P/Duty | [NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] | Input | F(IN), V(OUT), L(OUT)；heat stream [NON-ENGLISH REDACTED] live `HS(IN)`/`HS(OUT)` |

---

## 2. Core MCP / HTTP Operations

| MCP operation | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] |
|---------------|------|---------------|
| `set_flash2_flash_spec` | `SPEC_OPT` | [NON-ENGLISH REDACTED] §2.1 |
| `set_flash2_temperature` | `TEMP` | float + unit（`TP`/`TD`/`TQ`） |
| `set_flash2_pressure` | `PRES` | float + **unit required**. Legal tokens include **`bar`**, `bara`, `barg`, `MPa`, `kPa`, `psia`, `mmHg`, `atm`, … (`TP`/`PD`) |
| `set_flash2_duty` | `DUTY` | float + unit（`TD`/`PD`/`TQ` [NON-ENGLISH REDACTED] duty/heat [NON-ENGLISH REDACTED]） |
| `set_flash2_vapor_fraction` | `VFRAC` | float（`TV`/`PV`） |
| `set_energy_bal` | `ENERGY_BAL` | `YES` \| `NO` |

### 2.1 `SPEC_OPT` option [NON-ENGLISH REDACTED]

| token | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|-------|------|-------------|
| `TP` | Temperature + pressure | `TEMP` + `PRES` |
| `TV` | Temperature + vapor fraction | `TEMP` + `VFRAC` |
| `PV` | Pressure + vapor fraction | `PRES` + `VFRAC` |
| `TD` | Temperature + duty | `TEMP` + `DUTY` |
| `PD` | Pressure + duty | `PRES` + `DUTY` |
| `TQ` | Temperature + heat/duty | `TEMP` + connected heat stream / duty path |

**[NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED] T+P [NON-ENGLISH REDACTED] `TP` [NON-ENGLISH REDACTED] `TEMP`+`PRES`；[NON-ENGLISH REDACTED] P+duty [NON-ENGLISH REDACTED] `PD` [NON-ENGLISH REDACTED] `PRES`+`DUTY`；**[NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED] `PRES+DUTY` [NON-ENGLISH REDACTED] `PQ`（Flash2 [NON-ENGLISH REDACTED] `PQ` token）。

### 2.2 Bar-scale / near-atmospheric `PRES`

- **`unit=&quot;bar&quot;` [NON-ENGLISH REDACTED]**（[NON-ENGLISH REDACTED] INSET [NON-ENGLISH REDACTED]）；`set_flash2_pressure` [NON-ENGLISH REDACTED] Literal [NON-ENGLISH REDACTED] `bar` / `bara` / `barg`。
- [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]：meta [NON-ENGLISH REDACTED] **`PRES = -0.05`** [NON-ENGLISH REDACTED] **`unit=&quot;bar&quot;`**（absolute bar [NON-ENGLISH REDACTED] = [NON-ENGLISH REDACTED]）。
- **[NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED] bar [NON-ENGLISH REDACTED] **`MPa`**（[NON-ENGLISH REDACTED] `-0.05 bar` → `2.15 MPa` [NON-ENGLISH REDACTED]）。
- [NON-ENGLISH REDACTED] readback [NON-ENGLISH REDACTED]；readback [NON-ENGLISH REDACTED] display unit [NON-ENGLISH REDACTED] `psia` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] display label [NON-ENGLISH REDACTED] `unit=`。

```python
client.invoke(&quot;set_flash2_pressure&quot;, block_name=&quot;F&quot;, value=-0.05, unit=&quot;bar&quot;)
```

[NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] Flash2 [NON-ENGLISH REDACTED] `set_flash2_temperature` + `set_flash2_pressure`。[NON-ENGLISH REDACTED] `SPEC_OPT` [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、duty、vapor fraction [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、utility requirement [NON-ENGLISH REDACTED]。

### 2.1 Heat Stream / Duty [NON-ENGLISH REDACTED]

Flash2 [NON-ENGLISH REDACTED] live `list_block_ports` [NON-ENGLISH REDACTED] `HS(IN)` / `HS(OUT)`，[NON-ENGLISH REDACTED]：

```text
F(IN), HS(IN), V(OUT), L(OUT), WD(OUT), HS(OUT)
```

- `HS(IN): []` [NON-ENGLISH REDACTED] `HS(OUT): []` [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] heat port。
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `create_heat_stream(&lt;heat_stream&gt;)`，[NON-ENGLISH REDACTED] `connect_stream(block_name=&lt;flash&gt;, stream_name=&lt;heat_stream&gt;, port_name=&quot;HS(IN)&quot;)` [NON-ENGLISH REDACTED] live [NON-ENGLISH REDACTED] heat port。[NON-ENGLISH REDACTED] port readback、heat stream duty/readback、REP/APW [NON-ENGLISH REDACTED] run。
- [NON-ENGLISH REDACTED] duty / fixed heat balance [NON-ENGLISH REDACTED] Flash2，[NON-ENGLISH REDACTED] heat stream；[NON-ENGLISH REDACTED] block-owned `set_flash2_flash_spec` + `set_flash2_duty` / `set_flash2_temperature` / `set_flash2_pressure`。
- `TQ` [NON-ENGLISH REDACTED] Flash2 [NON-ENGLISH REDACTED] + heat/duty [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] heat stream / duty path [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]/heat stream [NON-ENGLISH REDACTED]，`set_spec_opt(..., &quot;TQ&quot;)` + `set_temp(...)`，[NON-ENGLISH REDACTED] heat stream / block duty path [NON-ENGLISH REDACTED] run [NON-ENGLISH REDACTED]。
- `set_flash2_vapor_fraction` [NON-ENGLISH REDACTED] Flash2 [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] heat/duty path [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `set_flash2_vapor_fraction` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] heat stream [NON-ENGLISH REDACTED] native duty path [NON-ENGLISH REDACTED] run。
- [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] `TQ` [NON-ENGLISH REDACTED] **Flash2** [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] RStoic [NON-ENGLISH REDACTED] block family；[NON-ENGLISH REDACTED] RStoic [NON-ENGLISH REDACTED] `SPEC_OPT` [NON-ENGLISH REDACTED] `TQ`。

---

## 3. [NON-ENGLISH REDACTED] MCP

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| `create_flash2` | `block_name` |
| `connect_stream` | [NON-ENGLISH REDACTED]：`F(IN)`, `V(OUT)`, `L(OUT)`；[NON-ENGLISH REDACTED]：live `HS(IN)`/`HS(OUT)` |
| `engine_run` | — |

---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| Core setter | 5 |

```

### FILE: docs/hardcoded_script_plan/block_type_inject/fsplit.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：FSPLIT（[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`FSPLIT`
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]。

---

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

| Helper | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|--------|----------|------|
| `configure_fsplit_shared_outlets(...)` | `block_name`, `inlet_stream`, `outlet_streams`, `split_fractions` | **Python-only** helper；[NON-ENGLISH REDACTED] `P(OUT)`，[NON-ENGLISH REDACTED] `set_frac` |

`configure_fsplit_shared_outlets(...)` [NON-ENGLISH REDACTED] Aspen HTTP operation。[NON-ENGLISH REDACTED]
`safe.configure_fsplit_shared_outlets(client, ...)` [NON-ENGLISH REDACTED]
`call_helper(&quot;configure_fsplit_shared_outlets&quot;, client, ...)` [NON-ENGLISH REDACTED]；**[NON-ENGLISH REDACTED]**
`client.execute(&quot;configure_fsplit_shared_outlets&quot;, ...)` [NON-ENGLISH REDACTED]
`do_op(client, &quot;configure_fsplit_shared_outlets&quot;, ...)`.

```python
client.invoke(&quot;configure_fsplit_shared_outlets&quot;,
    block_name=&quot;VF&quot;,
    inlet_stream=&quot;V2&quot;,
    outlet_streams=[&quot;V4&quot;, &quot;V3&quot;],
    split_fractions={&quot;V4&quot;: 0.92},
)
```

[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED] **`inlet_stream`**，[NON-ENGLISH REDACTED] `feed_stream`。
- [NON-ENGLISH REDACTED] **`outlet_streams`**（[NON-ENGLISH REDACTED]）[NON-ENGLISH REDACTED] **`split_fractions`**（dict），[NON-ENGLISH REDACTED] `outlet_fractions`。
- `outlet_streams` [NON-ENGLISH REDACTED] 2 [NON-ENGLISH REDACTED]；`split_fractions` [NON-ENGLISH REDACTED] **[NON-ENGLISH REDACTED] 1 [NON-ENGLISH REDACTED] closure stream [NON-ENGLISH REDACTED]** [NON-ENGLISH REDACTED]。Aspen [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] HTTP [NON-ENGLISH REDACTED] `connect_stream` + `set_frac`；[NON-ENGLISH REDACTED] helper [NON-ENGLISH REDACTED] HTTP op。

---

## 1. [NON-ENGLISH REDACTED]（CRITICAL）

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| [NON-ENGLISH REDACTED] | Input | [NON-ENGLISH REDACTED] `list_block_ports` + helper [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `set_frac` |

---

## 2. Core MCP / HTTP Operations

| MCP operation | Aspen [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|---------------|------------|---------------|------|
| `set_frac` | `FRAC` | float 0..1 | [NON-ENGLISH REDACTED] outlet stream [NON-ENGLISH REDACTED]；closure stream [NON-ENGLISH REDACTED] |

---

## 3. [NON-ENGLISH REDACTED] MCP

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|------|
| `create_fsplit` | `block_name` | [NON-ENGLISH REDACTED] FSPLIT [NON-ENGLISH REDACTED] |
| `create_material_stream` | `stream_name` | [NON-ENGLISH REDACTED] |
| `list_block_ports` | `block_name` | [NON-ENGLISH REDACTED] |
| `connect_stream` | `block_name`, `stream_name`, `port_name` | [NON-ENGLISH REDACTED] helper [NON-ENGLISH REDACTED] |
| `check_block_completion` | `block_name` | [NON-ENGLISH REDACTED] completion |
| `check_next_completion_status` | — | run [NON-ENGLISH REDACTED] |
| `engine_run` | — | [NON-ENGLISH REDACTED] |

---

## 4. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | REP、helper readback payload |
| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] Input [NON-ENGLISH REDACTED] null |

---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| Core operations | `set_frac` |
| [NON-ENGLISH REDACTED] helper | `configure_fsplit_shared_outlets(...)` via `safe_aspen_calls` |

```

### FILE: docs/hardcoded_script_plan/block_type_inject/radfrac.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：RADFRAC（[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`RADFRAC`
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED] MESH [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] DSTWU [NON-ENGLISH REDACTED]。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

| Helper | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|--------|----------|------|
| `configure_radfrac_total_condenser(...)` | `block_name`, `feed_stream`, `nstage`, `feed_stage`, `reflux_ratio`, `distillate_flow`, `distillate_flow_unit`, `top_pressure`, `bottom_pressure`, `pressure_unit` | [NON-ENGLISH REDACTED] + [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `BASIS_RR` + `BASIS_D` |
| `configure_radfrac_bottom_vapor_feed(...)` | `feed_stream`, `nstage`, `feed_stage`, `top_pressure`, `pressure_unit`, `column_dp`, `reflux_ratio`, `distillate_flow`, `d_over_f` | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] **[NON-ENGLISH REDACTED]**；[NON-ENGLISH REDACTED] `PRES1` + `FEED_CONVEN=ON-STAGE-VAP` |
| `configure_radfrac_no_condenser_absorber(...)` | `nstage`, `feed_stages: dict`, `feed_conventions: dict`, `top_pressure`, `pressure_unit`, `bottom_pressure`, `column_dp` | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `PRES1`，[NON-ENGLISH REDACTED] `PRES2` [NON-ENGLISH REDACTED] `DP_COL`，[NON-ENGLISH REDACTED] |
| `configure_radfrac_no_condenser_reboiled_bottoms(...)` | `reboiler_type`, `feed_stages`, `top_pressure`, `pressure_unit`, … | [NON-ENGLISH REDACTED] + [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `PRES1` / `PRES2` / `DP_COL` |
| `configure_radfrac_feed_convention(...)` | `block_name`, `stream_name`, `convention` | **Python-only** helper；[NON-ENGLISH REDACTED] `FEED_CONVEN` + `FEED_CONVE2` [NON-ENGLISH REDACTED]；**[NON-ENGLISH REDACTED]** `client.execute(&quot;configure_radfrac_feed_convention&quot;, ...)` |
| `configure_radfrac_extractive_distillation_pair(...)` | [NON-ENGLISH REDACTED] + [NON-ENGLISH REDACTED] + [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] + [NON-ENGLISH REDACTED] |
| `connect_radfrac_feed_distillate_bottoms(...)` | `block_name`, `inlet_streams`, `distillate_stream`, `bottoms_stream` | [NON-ENGLISH REDACTED] RadFrac：[NON-ENGLISH REDACTED] `F(IN)`，[NON-ENGLISH REDACTED] `LD(OUT)`，[NON-ENGLISH REDACTED] `B(OUT)`；[NON-ENGLISH REDACTED] evidence |
| `scan_radfrac_bottoms_for_component_recovery(...)` | `column_block`, `feed_stream`, `bottoms_stream`, `component_name`, `flow_values`, `flow_unit`, `target_recovery` | [NON-ENGLISH REDACTED] RadFrac `BASIS_B` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]”[NON-ENGLISH REDACTED] |
| `collect_radfrac_profile_markdown_evidence(...)` | keyword-only: `rep_text`, `block_name`, `component_ids`, `output_dir`, optional `profile_name`, `source_rep_path` | [NON-ENGLISH REDACTED] REP [NON-ENGLISH REDACTED] canonical Markdown [NON-ENGLISH REDACTED] profile [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `client` [NON-ENGLISH REDACTED] |

Use `inlet_streams=[feed]`, not `feed_stream=`, for `connect_radfrac_feed_distillate_bottoms`. WRONG: `feed_stream=F1`; CORRECT: `inlet_streams=[F1]`.

### 0.1 [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] helper）

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] |
|------|----------|-----------------|
| [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] + [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] | `configure_radfrac_total_condenser(...)` | `set_condenser(TOTAL)`、`set_reboiler(KETTLE)`、`BASIS_RR`、`BASIS_D`、`PRES1` |
| [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] | `configure_radfrac_no_condenser_absorber(...)` | [NON-ENGLISH REDACTED] `feed_stages` **[NON-ENGLISH REDACTED]** `feed_conventions`；[NON-ENGLISH REDACTED] `VD(OUT)`，[NON-ENGLISH REDACTED] `B(OUT)` |
| [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | `configure_radfrac_no_condenser_reboiled_bottoms(...)` | [NON-ENGLISH REDACTED] absorber [NON-ENGLISH REDACTED] `REBOILER=NONE`；[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] / packing-height perturbation | [NON-ENGLISH REDACTED] packed-section/HETP/height [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] stage surrogate，[NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] base [NON-ENGLISH REDACTED] modified [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]；stage surrogate [NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] textbook base target [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] base，[NON-ENGLISH REDACTED] | base outlet [NON-ENGLISH REDACTED] target；[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] surrogate [NON-ENGLISH REDACTED] |

**[NON-ENGLISH REDACTED]**：

- `configure_radfrac_no_condenser_absorber(...)` [NON-ENGLISH REDACTED] `feed_conventions` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] Bottom Stage / Reboiler=None [NON-ENGLISH REDACTED] Next gate。
- [NON-ENGLISH REDACTED]，`feed_conventions[gas_stream]` [NON-ENGLISH REDACTED] `ON-STAGE-VAP`；[NON-ENGLISH REDACTED]，`feed_conventions[solvent_stream]` [NON-ENGLISH REDACTED] `ON-STAGE-LIQ`。helper [NON-ENGLISH REDACTED] `FEED_CONVEN` [NON-ENGLISH REDACTED] `FEED_CONVE2`。
- `REBOILER=NONE` [NON-ENGLISH REDACTED]，Bottom Stage [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] `ON-STAGE-VAP`，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED] `NSTAGE+1` above-stage vapor/liquid [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] feed stage [NON-ENGLISH REDACTED] convention。
- [NON-ENGLISH REDACTED] `list_block_ports`。[NON-ENGLISH REDACTED] `VD(OUT)`，[NON-ENGLISH REDACTED] `D(OUT)`。
- [NON-ENGLISH REDACTED] Aspen / UI Next [NON-ENGLISH REDACTED]：
  - `FEEDS not complete: SID = &lt;stream&gt;`
  - `Stage must be specified.`
  - `A feed or pumparound stream to the top stage must be specified when Condenser=None or condenser duty is zero.`
  - `A feed or pumparound stream to the bottom stage must be specified when Reboiler=None or reboiler duty is zero.`
  [NON-ENGLISH REDACTED] `FEEDS\&lt;stream&gt;\STAGE` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]：`set_feed_stage(...)` + `FEED_CONVEN` + `FEED_CONVE2` + `set_pres1(...)`，[NON-ENGLISH REDACTED] `configure_radfrac_no_condenser_absorber(...)`。

---

## 1. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| `set_radfrac_condenser_type` / `set_radfrac_reboiler_type` | `set_radfrac_stage_count` | [NON-ENGLISH REDACTED] |
| `set_radfrac_stage_count` | `set_radfrac_feed_stage` | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] |
| `set_radfrac_feed_stage` | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] `FEED_CONVEN` + `FEED_CONVE2` |
| [NON-ENGLISH REDACTED] profile | [NON-ENGLISH REDACTED] `set_pres_mixed` | [NON-ENGLISH REDACTED] ≥ feed [NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] | Input | `list_block_ports` → `D(OUT)` / `VD(OUT)` / `B(OUT)` |

### 1.1 [NON-ENGLISH REDACTED] profile（[NON-ENGLISH REDACTED] `PRES1`，[NON-ENGLISH REDACTED]）

| [NON-ENGLISH REDACTED] | MCP | [NON-ENGLISH REDACTED] |
|------|-----|----------|
| [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | `set_radfrac_top_pressure` | [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] RadFrac [NON-ENGLISH REDACTED]；`PRES1` [NON-ENGLISH REDACTED] Stage 1 / Condenser / top reference pressure |
| TOP-BOTTOM | `set_radfrac_top_pressure` + `set_radfrac_bottom_pressure` | [NON-ENGLISH REDACTED] top/bottom pressure，[NON-ENGLISH REDACTED]；`PRES2` [NON-ENGLISH REDACTED] pressure anchor / bottom-side pressure，[NON-ENGLISH REDACTED] `PRES1` [NON-ENGLISH REDACTED] |
| DP-COL | `set_opt_pres(DP-COL)` + `set_radfrac_top_pressure` + `set_radfrac_column_pressure_drop` | [NON-ENGLISH REDACTED]；`DP_COL = bottom_pressure - top_pressure` |

[NON-ENGLISH REDACTED] BKP / APW [NON-ENGLISH REDACTED] RadFrac [NON-ENGLISH REDACTED] `P-SPEC2: PRES1=... PRES2=...`，
[NON-ENGLISH REDACTED] `PRES1` [NON-ENGLISH REDACTED] recycle、feed stage [NON-ENGLISH REDACTED] solver。`PRES2`
[NON-ENGLISH REDACTED] probe [NON-ENGLISH REDACTED]；`configure_radfrac_total_condenser(...)`
[NON-ENGLISH REDACTED] `bottom_pressure_mode=&quot;pres2&quot;` [NON-ENGLISH REDACTED] TOP-BOTTOM/P-SPEC2 [NON-ENGLISH REDACTED]。

`PRES1` [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] Next / completion [NON-ENGLISH REDACTED]
`Top Stage Pressure must be specified when Top/Bottom or Section Pressure Drop is selected.`
[NON-ENGLISH REDACTED] GUI [NON-ENGLISH REDACTED] `Stage 1 / Condenser pressure`，[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]
`set_pres1(block_name=&lt;BLK&gt;, value=&lt;top pressure&gt;, unit=&lt;unit&gt;)`。

[NON-ENGLISH REDACTED]：

- [NON-ENGLISH REDACTED] **bottom pressure**，[NON-ENGLISH REDACTED] `set_radfrac_bottom_pressure`，[NON-ENGLISH REDACTED] `DP_COL`
  [NON-ENGLISH REDACTED] DP-COL；[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] **column pressure drop**，[NON-ENGLISH REDACTED] `OPT_PRES=DP-COL` + `set_radfrac_column_pressure_drop`。
- [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `PRES1`；[NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED] bottom”[NON-ENGLISH REDACTED]。
- `bottom_pressure &gt;= top_pressure` [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]。`psig/barg/kPag`
  [NON-ENGLISH REDACTED] `psia/bar/kPa` [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `kPa`。
- [NON-ENGLISH REDACTED]：`kPa`, `bar`, `atm`, `mmHg`, `MPa`, `psi`, `psia`, `psig`。
  [NON-ENGLISH REDACTED] `set_radfrac_top_pressure` / `set_radfrac_bottom_pressure` [NON-ENGLISH REDACTED]；`set_radfrac_column_pressure_drop`
  [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `kPa`, `bar`, `psi`, `mmHg`, `MPa` [NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] `set_radfrac_top_pressure` / `set_radfrac_bottom_pressure` / `set_radfrac_column_pressure_drop`。[NON-ENGLISH REDACTED] RadFrac [NON-ENGLISH REDACTED]、helper [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] live option/readback [NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]：

1. `read_pressure_state(block_name, unit=&lt;same_unit&gt;)` [NON-ENGLISH REDACTED]
   `Data\Blocks\&lt;BLK&gt;\Input\PRES1`, `PRES2`, `OPT_PRES`, `DP_COL`。
2. [NON-ENGLISH REDACTED] `PRES1` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `set_radfrac_top_pressure`。
3. [NON-ENGLISH REDACTED] `OPT_PRES=DP-COL`，[NON-ENGLISH REDACTED] `DP_COL` [NON-ENGLISH REDACTED] bottom absolute pressure。
4. [NON-ENGLISH REDACTED] `set_radfrac_bottom_pressure`，[NON-ENGLISH REDACTED] `PRES2` [NON-ENGLISH REDACTED] `PRES1` [NON-ENGLISH REDACTED]。
5. [NON-ENGLISH REDACTED]；feed stream pressure [NON-ENGLISH REDACTED] feed stage [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] REP/PER_ERROR [NON-ENGLISH REDACTED] feed pressure too low。

### 1.2 [NON-ENGLISH REDACTED]（Python helper，[NON-ENGLISH REDACTED] HTTP operation）

`configure_radfrac_feed_convention(...)` [NON-ENGLISH REDACTED] `script_agent_exp.safe_aspen_calls`
[NON-ENGLISH REDACTED] **Python helper**，[NON-ENGLISH REDACTED] Aspen HTTP `/execute` operation。[NON-ENGLISH REDACTED]
`safe.configure_radfrac_feed_convention(client, ...)` [NON-ENGLISH REDACTED]
`call_helper(&quot;configure_radfrac_feed_convention&quot;, client, ...)` [NON-ENGLISH REDACTED]；**[NON-ENGLISH REDACTED]**
`client.execute(&quot;configure_radfrac_feed_convention&quot;, ...)` [NON-ENGLISH REDACTED]
`do_op(client, &quot;configure_radfrac_feed_convention&quot;, ...)`。

| helper | token [NON-ENGLISH REDACTED] |
|--------|-------------|
| `configure_radfrac_feed_convention(client, block_name=..., stream_name=..., convention=...)` | `ON-STAGE`, `ABOVE-STAGE`, `VAPOR`, `LIQUID`, `ON-STAGE-VAP`, `ON-STAGE-LIQ`（[NON-ENGLISH REDACTED] live legal values [NON-ENGLISH REDACTED]；UI [NON-ENGLISH REDACTED] Vapor/Liquid，[NON-ENGLISH REDACTED] `ON-STAGE-VAP`/`ON-STAGE-LIQ`） |
| [NON-ENGLISH REDACTED] `FEED_CONVEN` + `FEED_CONVE2` **[NON-ENGLISH REDACTED]** | [NON-ENGLISH REDACTED] `legal_values` |

```python
client.invoke(&quot;configure_radfrac_feed_convention&quot;,
    block_name=&quot;CO&quot;,
    stream_name=&quot;CF&quot;,
    convention=&quot;ON-STAGE-LIQ&quot;,
)
```

[NON-ENGLISH REDACTED] RadFrac feed stage [NON-ENGLISH REDACTED] `Data\Blocks\&lt;BLK&gt;\Input\FEEDS\&lt;stream&gt;\STAGE` [NON-ENGLISH REDACTED] `...\FEEDS\&lt;stream&gt;\FEED_STAGE` [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] surface。[NON-ENGLISH REDACTED] **stage** [NON-ENGLISH REDACTED] HTTP `set_feed_stage(...)`；[NON-ENGLISH REDACTED] **convention** [NON-ENGLISH REDACTED] Python helper。

[NON-ENGLISH REDACTED] RadFrac probe [NON-ENGLISH REDACTED] `PER_ERROR=1` [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]
`feed_stage` [NON-ENGLISH REDACTED]。`ABOVE-STAGE` / `ON-STAGE` / `VAPOR` / `LIQUID`
（[NON-ENGLISH REDACTED] `ON-STAGE-VAP` / `ON-STAGE-LIQ` [NON-ENGLISH REDACTED] token）[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]、
[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] L1 [NON-ENGLISH REDACTED] stage [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED] bundle，
[NON-ENGLISH REDACTED] `(stage=40, convention=ON-STAGE)`、`(stage=40, convention=ABOVE-STAGE)`、
`(stage=40, convention=VAPOR)`、`(stage=40, convention=LIQUID)`，[NON-ENGLISH REDACTED] stage。

### 1.2.1 Bottom-vapor-feed operating specs

`BASIS_D` (molar distillate flow) and `D:F` (distillate/feed ratio) are alternative
operating-spec selections. Numeric writes can change active `COL-SPECS` membership;
do not append `set_d_f` after a successful `set_radfrac_reflux_ratio` + `set_radfrac_distillate_rate` bundle.
For `reboiler != &quot;NONE&quot;`, a call with `reflux_ratio` must also pass exactly one draw specification: `distillate_flow` plus explicit `distillate_flow_unit`, or `d_over_f`. RR alone is structurally under-specified and must be rejected before Aspen execution.

`configure_radfrac_bottom_vapor_feed` keeps explicit `distillate_flow` when both
arguments are supplied and records `d_over_f` as inactive evidence. Ratio-only
calls retain `set_d_f`. The order remains end effects -&gt; stage/pressure -&gt; feed
stage/convention -&gt; reflux -&gt; one draw spec. This is not a mechanism for clearing
old specs on inherited columns: inspect active UI/COL-SPECS rows before a basis
switch; do not guess selector paths or suppress a selected setter failure.
A saturated-vapor bottom feed does not imply `CONDENSER=NONE`: preserve a stated
total condenser and its `LD(OUT)` product role.

### 1.3 [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| [NON-ENGLISH REDACTED] | `F(IN)` | [NON-ENGLISH REDACTED] material feed collection；[NON-ENGLISH REDACTED] `F2(IN)` |
| [NON-ENGLISH REDACTED] | `LD(OUT)` / `D(OUT)` | [NON-ENGLISH REDACTED] `LD(OUT)`；[NON-ENGLISH REDACTED] live ports [NON-ENGLISH REDACTED] `D(OUT)` [NON-ENGLISH REDACTED] `D(OUT)` |
| [NON-ENGLISH REDACTED] | `VD(OUT)` / `V(OUT)` | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] vapor overhead [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `LD(OUT)` |
| [NON-ENGLISH REDACTED] | `B(OUT)` | [NON-ENGLISH REDACTED] bottoms material outlet |
| [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | `CHS(OUT)`, `CWS(IN/OUT)`, `HS(IN/OUT)` [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] material stream |

Generated slim source treats `list_block_ports` as opaque cross-iteration evidence: record it directly in `runtime.stage(..., required=False)` and do not assign, normalize, parse, or branch on the payload. Use a registered role-aware RadFrac topology capability for connection work; framework internals own any port normalization. Complete topology before product-rate, pressure, condenser, or reboiler specifications.

---

## 2. Core MCP / HTTP Operations

### 2.1 [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]

| MCP operation | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] |
|---------------|------|---------------|
| `set_radfrac_condenser_type` | `CONDENSER` | `NONE` \| `TOTAL` \| `PARTIAL-V` \| `PARTIAL-V-L` |
| `set_radfrac_reboiler_type` | `REBOILER` | `NONE` \| `KETTLE` \| `THERMOSYPHON` |
| `set_radfrac_stage_count` | `NSTAGE` | int |
| `set_radfrac_top_pressure` | `PRES1` | Stage 1 / Condenser / top reference pressure；float + pressure unit |
| `set_radfrac_bottom_pressure` | `PRES2` | [NON-ENGLISH REDACTED] pressure anchor / bottom-side pressure；float + pressure unit；[NON-ENGLISH REDACTED] |
| `set_radfrac_pressure_mode` | `OPT_PRES` | `DP-STAGE` \| `DP-COL`；[NON-ENGLISH REDACTED] `DP-COL` |
| `set_radfrac_column_pressure_drop` | `DP_COL` | [NON-ENGLISH REDACTED]；**float + unit [NON-ENGLISH REDACTED]**（[NON-ENGLISH REDACTED] `atm`, `kPa`, `bar`）；[NON-ENGLISH REDACTED] = bottom pressure − top pressure；[NON-ENGLISH REDACTED] `unit` [NON-ENGLISH REDACTED] HTTP [NON-ENGLISH REDACTED] |
| `read_pressure_state` | `OPT_PRES/PRES1/PRES2/DP_COL/...` | [NON-ENGLISH REDACTED] pressure mode [NON-ENGLISH REDACTED] |

### 2.2 [NON-ENGLISH REDACTED]

Generated code must use the family-specific semantic names below. Native names `set_basis_d` and `set_basis_b` are framework-internal because they collide with PetroFrac/MultiFrac signatures.

| MCP operation | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] |
|---------------|------|---------------|
| `set_radfrac_feed_stage` | `FEED_STAGE` | exact kwargs: `block_name`, `stream_name`, `value`; `value` is the Aspen stage int (including condenser/reboiler stages). **Do not use `stage=`, `stage_number=`, or `feed_stage=`.** |
| `set_radfrac_reflux_ratio` | `BASIS_RR` | float |
| `set_radfrac_distillate_rate` | `BASIS_D` | float + unit（**[NON-ENGLISH REDACTED]**：`kmol/hr`, `mol/hr`） |
| `set_radfrac_bottoms_rate` | `BASIS_B` | float + unit |
| `set_basis_br` | `BASIS_BR` | float（[NON-ENGLISH REDACTED]） |
| `set_d_f` | `D:F` | float |
| `set_prod_phase` | **`(block_name, value, stream_name)`** | [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `set_reactor_prod_phase` |
| `set_prod_stage` / `set_prod_flow` | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / **[NON-ENGLISH REDACTED]** |

Exact direct-call form for an additional or special RadFrac feed:

```python
client.invoke(
    &quot;set_radfrac_feed_stage&quot;,
    block_name=&quot;D1&quot;,
    stream_name=&quot;S1&quot;,
    value=5,
)
```

The public capability retains the native setter&#x27;s generic numeric keyword `value`. The semantic name does **not** imply a `stage` keyword. Prefer `configure_radfrac_total_condenser(..., feed_stage=...)` for the standard single-feed bundle; use the direct capability above only for per-feed additions.

### 2.2.0 Partial-Vapor + Distillate rate [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] GUI/[NON-ENGLISH REDACTED] `Condenser = Partial-Vapor`、`Reboiler = Kettle`，[NON-ENGLISH REDACTED]
Operating specifications [NON-ENGLISH REDACTED] `Reflux ratio` + `Distillate rate` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]
`Distillate rate` [NON-ENGLISH REDACTED] RadFrac [NON-ENGLISH REDACTED]：

```python
Application.Tree.FindNode(r&quot;\Data\Blocks\D1\Input\BASIS_D&quot;)
```

[NON-ENGLISH REDACTED] MCP/helper [NON-ENGLISH REDACTED] `client.invoke(&quot;set_radfrac_distillate_rate&quot;, block_name=&quot;D1&quot;, value=&lt;rate&gt;, unit=&lt;molar-flow-unit&gt;)`。
[NON-ENGLISH REDACTED] `BASIS_RDV` / `set_basis_rdv`，[NON-ENGLISH REDACTED] `D:F` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]
live UI [NON-ENGLISH REDACTED] vapor distillate fraction / D:F [NON-ENGLISH REDACTED]。
[NON-ENGLISH REDACTED] `BASIS_RR` [NON-ENGLISH REDACTED] `BASIS_D`；`BASIS_D` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] operating specs
[NON-ENGLISH REDACTED]。

### 2.2.1 [NON-ENGLISH REDACTED] vs [NON-ENGLISH REDACTED]

- [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED] `50 mol/hr bottoms is required`），[NON-ENGLISH REDACTED]
  RadFrac [NON-ENGLISH REDACTED]：write `BASIS_B` or `BASIS_D` through `set_radfrac_bottoms_rate` / `set_radfrac_distillate_rate`，[NON-ENGLISH REDACTED] converged REP /
  stream readback [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]“report recovery”[NON-ENGLISH REDACTED]
  [NON-ENGLISH REDACTED] Design Spec。
- [NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED]，
  [NON-ENGLISH REDACTED] `scan_radfrac_bottoms_for_component_recovery(...)` [NON-ENGLISH REDACTED] active native
  Design Spec。scan [NON-ENGLISH REDACTED] converged [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]
  [NON-ENGLISH REDACTED]，scan [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]。
- [NON-ENGLISH REDACTED] `BASIS_B` seed [NON-ENGLISH REDACTED] proof-only recovery [NON-ENGLISH REDACTED]“[NON-ENGLISH REDACTED]
  workflow”。[NON-ENGLISH REDACTED] scan/DS [NON-ENGLISH REDACTED] post-adjustment run；[NON-ENGLISH REDACTED]
  [NON-ENGLISH REDACTED] final run [NON-ENGLISH REDACTED] native spec readback [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] evidence。

### 2.2.2 RadFrac profile Markdown evidence

`collect_radfrac_profile_markdown_evidence(...)` [NON-ENGLISH REDACTED] helper，[NON-ENGLISH REDACTED]
Aspen client。[NON-ENGLISH REDACTED] trusted REP [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] keyword-only [NON-ENGLISH REDACTED]：

```python
rep_text = Path(rep_path).read_text(encoding=&quot;utf-8&quot;, errors=&quot;replace&quot;)
profile = safe.collect_radfrac_profile_markdown_evidence(
    rep_text=rep_text,
    block_name=&quot;D1&quot;,
    component_ids=[&quot;MEOH&quot;, &quot;ETOH&quot;, &quot;H2O&quot;],
    output_dir=artifact_dir,
    profile_name=&quot;MOLE-X-PROFILE&quot;,
    source_rep_path=rep_path,
)
```

[NON-ENGLISH REDACTED] `profile_name` [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] `MOLE-X-PROFILE`，[NON-ENGLISH REDACTED]
`MOLE-Y-PROFILE`。[NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] §2.4 [NON-ENGLISH REDACTED]
`export_radfrac_composition_profile_plot`，`basis` [NON-ENGLISH REDACTED] profile [NON-ENGLISH REDACTED]
（[NON-ENGLISH REDACTED] `mole_y`，[NON-ENGLISH REDACTED] `mole_x`）。[NON-ENGLISH REDACTED] helper [NON-ENGLISH REDACTED] `row_count=0`，
[NON-ENGLISH REDACTED] trusted REP [NON-ENGLISH REDACTED] profile，[NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED]）：

```python
configure_radfrac_no_condenser_absorber(
    client,
    block_name=&quot;D1&quot;,
    nstage=12,
    feed_stages={&quot;W1&quot;: 1, &quot;G1&quot;: 12},
    feed_conventions={&quot;W1&quot;: &quot;ON-STAGE-LIQ&quot;, &quot;G1&quot;: &quot;ON-STAGE-VAP&quot;},
    top_pressure=101.325,
    pressure_unit=&quot;kPa&quot;,
)
```

[NON-ENGLISH REDACTED] helper [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]：

1. `set_condenser(D1, NONE)` + `set_reboiler(D1, NONE)` + `set_nstage(D1, 12)`。
2. `set_pres1(D1, 101.325, &quot;kPa&quot;)`，[NON-ENGLISH REDACTED] `set_radfrac_bottom_pressure` [NON-ENGLISH REDACTED] `OPT_PRES=DP-COL` + `set_radfrac_column_pressure_drop`。
3. `set_feed_stage(D1, W1, 1)`、`set_feed_stage(D1, G1, 12)`。
4. `safe.configure_radfrac_feed_convention(client, block_name=&quot;D1&quot;, stream_name=..., convention=...)`；[NON-ENGLISH REDACTED] `ON-STAGE-VAP`，[NON-ENGLISH REDACTED] `ON-STAGE-LIQ`。

### 2.3 [NON-ENGLISH REDACTED]

| MCP operation | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|---------------|------|--------|
| `set_conv_meth` | `CONV_METH` | `STANDARD` \| … \| `AZEOTROPIC` |
| `set_maxol` | `MAXOL` | float |
| [NON-ENGLISH REDACTED] | helper [NON-ENGLISH REDACTED] | `INIT_OPTION`/`RESTART` [NON-ENGLISH REDACTED] helper [NON-ENGLISH REDACTED]，agent [NON-ENGLISH REDACTED] raw tree [NON-ENGLISH REDACTED] |
| `read_pressure_state` | — | `block_name`, `unit` → [NON-ENGLISH REDACTED] |

### 2.4 [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]
`export_radfrac_composition_profile_plot(client, block_name=..., components=[...], basis=...)`。
`basis` [NON-ENGLISH REDACTED] `mole_y`（[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]「[NON-ENGLISH REDACTED]」）、`mole_x`（[NON-ENGLISH REDACTED]）、`mass_y`、`mass_x`。
[NON-ENGLISH REDACTED] PNG，[NON-ENGLISH REDACTED] `summary[&quot;plots&quot;]`。
`MOLE-Y-PROFILE` / `MOLE-X-PROFILE` [NON-ENGLISH REDACTED] Markdown [NON-ENGLISH REDACTED]。

| MCP operation | [NON-ENGLISH REDACTED] |
|---------------|------|
| `export_radfrac_composition_profile_plot` | [NON-ENGLISH REDACTED] PNG |
| `ui_export_radfrac_profile_plot` | [NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] |

---

## 3. [NON-ENGLISH REDACTED] MCP

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| `create_radfrac` | `block_name` |
| `list_block_ports` | `block_name` |
| `connect_stream` | `block_name`, `stream_name`, `port_name` |
| `engine_run` | — |

---

## 4. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | REP / stream Output |
| [NON-ENGLISH REDACTED] | `export_radfrac_composition_profile_plot` [NON-ENGLISH REDACTED] PNG；[NON-ENGLISH REDACTED] `MOLE-X-PROFILE` / `MOLE-Y-PROFILE` |

---

## 5. [NON-ENGLISH REDACTED]

- [NON-ENGLISH REDACTED] → **DSTWU**（`dstwu.md`）
- DS/SA/OPT [NON-ENGLISH REDACTED] token → `design_spec.md` / `sensitivity.md` / `optimization.md`

---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| Core setter | §2 [NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] helper | §0 [NON-ENGLISH REDACTED] |

```

### FILE: docs/hardcoded_script_plan/block_type_inject/pump.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：PUMP（[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`PUMP`（Aspen [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] “Pump HI” [NON-ENGLISH REDACTED]）
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `OPT_SPEC` [NON-ENGLISH REDACTED]。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper

[NON-ENGLISH REDACTED] helper；[NON-ENGLISH REDACTED] §2 MCP operation。

---

## 1. [NON-ENGLISH REDACTED]（CRITICAL）

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| `set_pump_outlet_spec` | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | **[NON-ENGLISH REDACTED] completion [NON-ENGLISH REDACTED] Outlet Specification must be specified** |
| [NON-ENGLISH REDACTED] bundle | `USE-CURVE` [NON-ENGLISH REDACTED] | `OPT_CTYPE` → `OPT_CFORMAT` → `DEP_VAR` / `INDEP_VAR` → `set_pump_curve_table` |
| [NON-ENGLISH REDACTED] | Input | F(IN)/P(OUT) [NON-ENGLISH REDACTED] |

---

## 2. Core MCP / HTTP Operations

| MCP operation | Aspen [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|---------------|------------|---------------|------|
| `set_pump_outlet_spec` | `OPT_SPEC` | [NON-ENGLISH REDACTED] §2.1 | **[NON-ENGLISH REDACTED] completion [NON-ENGLISH REDACTED] Outlet Specification must be specified** |
| `set_pump_outlet_pressure` | `PRES` | float + unit | `OPT_SPEC=PRES` [NON-ENGLISH REDACTED] |
| `set_delp` | `DELP` | float + unit | `OPT_SPEC=DELP` [NON-ENGLISH REDACTED] |
| `set_pratio` | `PRATIO` | float | `OPT_SPEC=PRATIO` [NON-ENGLISH REDACTED] |
| `set_power` | `POWER` | float + unit | `OPT_SPEC=POWER` [NON-ENGLISH REDACTED] |
| `set_eff` | `EFF` | float | [NON-ENGLISH REDACTED] |
| `set_deff` | `DEFF` | float | [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] 1 |
| `set_opt_ctype` | `OPT_CTYPE` | `SINGLE-OPER` \| `SINGLE-REFE` \| `MULTIP` | [NON-ENGLISH REDACTED] |
| `set_opt_cformat` | `OPT_CFORMAT` | `TABLE` \| `POLY` \| `USER-CURVES` | [NON-ENGLISH REDACTED] |
| `set_dep_var` | `DEP_VAR` | `HEAD` \| `HEAD-COEF` \| `POWER` \| `PRES` \| `PRAT` \| `DELP` | [NON-ENGLISH REDACTED] |
| `set_indep_var` | `INDEP_VAR` | `VOL-FLOW` \| `MASS-FLOW` | [NON-ENGLISH REDACTED] |
| `set_pump_curve_table` | （[NON-ENGLISH REDACTED]） | [NON-ENGLISH REDACTED] | HEAD_DATA + H_FLOW [NON-ENGLISH REDACTED] |

### 2.1 `OPT_SPEC` / Outlet Specification

| token | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|-------|------|----------|
| `PRES` | Discharge pressure | `set_pres(..., unit=...)` |
| `DELP` | Pressure increase | `set_delp` |
| `PRATIO` | Pressure ratio | `set_pratio` |
| `POWER` | Power required | `set_power` |
| `USE-CURVE` | Performance curve | [NON-ENGLISH REDACTED] bundle（§2.2） |

**[NON-ENGLISH REDACTED] `USE-CURVE`。**

### 2.2 [NON-ENGLISH REDACTED]（`OPT_SPEC=USE-CURVE`）

1. `set_opt_spec(USE-CURVE)`
2. `set_opt_ctype(SINGLE-OPER)`（[NON-ENGLISH REDACTED]）
3. `set_opt_cformat(TABLE)`
4. `set_dep_var(HEAD)` + `set_indep_var(VOL-FLOW)`
5. `set_pump_curve_table(curve_points=[{flow, head}, ...])`
6. [NON-ENGLISH REDACTED] `set_eff` / `set_deff`

---

## 3. [NON-ENGLISH REDACTED] MCP

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|------|
| `create_pump` | `block_name` | [NON-ENGLISH REDACTED] PUMP [NON-ENGLISH REDACTED] |
| `create_material_stream` | `stream_name` | [NON-ENGLISH REDACTED] |
| `list_block_ports` | `block_name` | [NON-ENGLISH REDACTED] |
| `connect_stream` | `block_name`, `stream_name`, `port_name` | [NON-ENGLISH REDACTED] Input |
| `check_block_completion` | `block_name` | [NON-ENGLISH REDACTED] completion |
| `check_next_completion_status` | — | run [NON-ENGLISH REDACTED] |
| `engine_run` | — | [NON-ENGLISH REDACTED] |

---

## 4. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | REP、helper readback payload |
| [NON-ENGLISH REDACTED] | REP [NON-ENGLISH REDACTED] `OPT_SPEC`、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] |

---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| Core operations | 12+ |
| [NON-ENGLISH REDACTED] skill | `aspen-pump-outlet-specification` |

```

### FILE: docs/hardcoded_script_plan/block_type_inject/compr.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：COMPR（[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`COMPR`
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] **PRES**、**DELP**、[NON-ENGLISH REDACTED]。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

```text
configure_compr_pressure_rise(
    client, *, block_name, delta_pressure, pressure_unit=None,
    compressor_type=&quot;ISENTROPIC&quot;,
)
```

---

## 1. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| `set_type` | `set_compr_outlet_spec` | [NON-ENGLISH REDACTED] |
| `set_compr_outlet_spec` | `set_compr_outlet_pressure` / `set_delp` / `set_pratio` | [NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | `set_peff`, `set_meff`（[NON-ENGLISH REDACTED]/ASME [NON-ENGLISH REDACTED]） |

---

## 2. Core MCP / HTTP Operations

| MCP operation | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|---------------|------|---------------|------|
| `set_type` | `TYPE` | [NON-ENGLISH REDACTED] §2.1 | [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `OPT_SPEC` |
| `set_compr_outlet_spec` | `OPT_SPEC` | [NON-ENGLISH REDACTED] §2.2 | [NON-ENGLISH REDACTED] |
| `set_compr_outlet_pressure` | `PRES` | float + unit | **`OPT_SPEC=PRES`** [NON-ENGLISH REDACTED] |
| `set_delp` | `DELP` | float + unit | **`OPT_SPEC=DELP`** [NON-ENGLISH REDACTED] |
| `set_pratio` | `PRATIO` | float | **`OPT_SPEC=PRATIO`** [NON-ENGLISH REDACTED] |
| `set_power` | `POWER` | float + unit | **`OPT_SPEC=POWER`** [NON-ENGLISH REDACTED] |
| `set_peff` | `PEFF` | float (0–1) | [NON-ENGLISH REDACTED] |
| `set_meff` | `MEFF` | float (0–1) | [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] 1.0 |

### 2.1 `TYPE` / Compressor Model

| token | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|-------|------|----------|
| `ISENTROPIC` | Isentropic | [NON-ENGLISH REDACTED] |
| `ASME-POLYTROP` | Polytropic (ASME) | [NON-ENGLISH REDACTED]（tya [NON-ENGLISH REDACTED]） |
| `GPSA-POLYTROP` | Polytropic (GPSA) | GPSA [NON-ENGLISH REDACTED] |
| `ASME-ISENTROP` | Isentropic (ASME) | ASME [NON-ENGLISH REDACTED] |
| `GPSA-ISENTROP` | Isentropic (GPSA) | GPSA [NON-ENGLISH REDACTED] |
| `INT-POLYTROP` | Polytropic, piecewise integration | [NON-ENGLISH REDACTED] |
| `POS-DISP` | Positive displacement | [NON-ENGLISH REDACTED] |
| `INT-POS-DISP` | Positive displacement, piecewise | [NON-ENGLISH REDACTED] |

### 2.2 `OPT_SPEC` / Outlet Specification

| token | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|-------|------|----------|
| `PRES` | Discharge pressure | `set_compr_outlet_pressure` |
| `DELP` | Pressure increase | `set_delp` |
| `PRATIO` | Pressure ratio | `set_pratio` |
| `POWER` | Power required | `set_power` |
| `USE-CURVE` | Performance curve | [NON-ENGLISH REDACTED] |

**[NON-ENGLISH REDACTED] `set_compr_outlet_spec`，[NON-ENGLISH REDACTED]**；[NON-ENGLISH REDACTED] Pump [NON-ENGLISH REDACTED] `OPT_SPEC` [NON-ENGLISH REDACTED] token [NON-ENGLISH REDACTED]。

### 2.1 [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED]）

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| C1 | `ASME-POLYTROP`, `OPT_SPEC=PRES`, `set_peff`, `set_meff`, `set_compr_outlet_pressure` |
| IC (Heater) | `set_compr_temperature` [NON-ENGLISH REDACTED] |
| C2 | [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `set_compr_outlet_pressure` |

Sensitivity [NON-ENGLISH REDACTED] **C1 `PRES`**，[NON-ENGLISH REDACTED] **C1/C2 [NON-ENGLISH REDACTED]**（`WNET`/`BRAKEHP` [NON-ENGLISH REDACTED] BLOCK-VAR）。

---

## 3. [NON-ENGLISH REDACTED] MCP

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| `create_compr` | `block_name` |
| `connect_stream` | INLET / OUTLET |
| `engine_run` | — |

---

## 5. [NON-ENGLISH REDACTED]

[NON-ENGLISH REDACTED] → **Heater**（`heater.md`），[NON-ENGLISH REDACTED] Compr [NON-ENGLISH REDACTED]。

---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| Core setter | 6 |
| [NON-ENGLISH REDACTED] helper | `configure_compr_pressure_rise` |

```

### FILE: docs/hardcoded_script_plan/block_type_inject/pipe.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：PIPE（[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`PIPE`
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]（schedule）[NON-ENGLISH REDACTED]。

---

## 0. Helper

[NON-ENGLISH REDACTED] **`safe.configure_pipe_schedule_sizing(...)`**。Agent [NON-ENGLISH REDACTED] pipe sizing HTTP operation。

---

## 1. [NON-ENGLISH REDACTED]（CRITICAL）

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] `list_block_ports` + `connect_stream` |
| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] `configure_pipe_schedule_sizing(...)`（helper [NON-ENGLISH REDACTED]） |

---

## 2. Agent [NON-ENGLISH REDACTED]

### `configure_pipe_schedule_sizing` — [NON-ENGLISH REDACTED]

Aspen **PIPE + OSCHED（[NON-ENGLISH REDACTED]）** [NON-ENGLISH REDACTED] Input [NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED] schedule [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] → [NON-ENGLISH REDACTED] → [NON-ENGLISH REDACTED] → [NON-ENGLISH REDACTED]。Agent [NON-ENGLISH REDACTED] setter，[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] completion [NON-ENGLISH REDACTED]（chn-9-1 [NON-ENGLISH REDACTED]）。

[NON-ENGLISH REDACTED] helper [NON-ENGLISH REDACTED]：

1. **[NON-ENGLISH REDACTED] OSCHED [NON-ENGLISH REDACTED]**，[NON-ENGLISH REDACTED] agent [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] planner/codegen [NON-ENGLISH REDACTED] HTTP op。
2. **[NON-ENGLISH REDACTED]** `OPT_DIAM` / `MATERIAL` / `SCHEDULE` / `NOMINAL_DIAM` / `LENGTH`，[NON-ENGLISH REDACTED] `check_ok`、`readbacks`、`summary`，[NON-ENGLISH REDACTED] `summary.json` [NON-ENGLISH REDACTED] validator/score [NON-ENGLISH REDACTED]。
3. **[NON-ENGLISH REDACTED] skill [NON-ENGLISH REDACTED]**：skill [NON-ENGLISH REDACTED] helper，[NON-ENGLISH REDACTED] agent [NON-ENGLISH REDACTED] setter [NON-ENGLISH REDACTED]。

### [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|--------|
| [NON-ENGLISH REDACTED] | `PIPE` | `Pipeline`、[NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] | `OPT_DIAM=OSCHED`（[NON-ENGLISH REDACTED]） | `OINNER` [NON-ENGLISH REDACTED]、`USER-SUBR` |
| [NON-ENGLISH REDACTED] | `OPT_DIAM`、`MATERIAL`、`SCHEDULE`、`NOMINAL_DIAM`、`LENGTH` | [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] Input [NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] | `material`（`CARBON-STEEL` / `STAINLESS`）；`schedule`（10/20/40/80/120/160）；`nominal_diam`（[NON-ENGLISH REDACTED] `1-IN`）；`length` + `length_unit` | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] token |
| [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED] `create_pipe` [NON-ENGLISH REDACTED]） | `create_pipe`、`connect_stream`、[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] |
| [NON-ENGLISH REDACTED] | chn-9-1：`PIPE` [NON-ENGLISH REDACTED] Sch-40、1 in、25 m | [NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] schedule [NON-ENGLISH REDACTED] PIPE [NON-ENGLISH REDACTED] |

### [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| `configure_pipe_schedule_sizing` | OSCHED [NON-ENGLISH REDACTED]（agent [NON-ENGLISH REDACTED] safe helper） |

### [NON-ENGLISH REDACTED] option list

helper [NON-ENGLISH REDACTED]：

```python
safe.configure_pipe_schedule_sizing(
    client,
    *,
    block_name: str,
    material: str = &quot;CARBON-STEEL&quot;,
    schedule: int = &lt;number&gt;,
    nominal_diam: str = &quot;1-IN&quot;,
    length: float =&lt;float number&gt;,
    length_unit: str = &quot;meter&quot;,
)
```

| [NON-ENGLISH REDACTED] | Aspen [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] |
|------|------------|---------------|
| `block_name` | — | [NON-ENGLISH REDACTED] `PIPE` [NON-ENGLISH REDACTED] |
| `material` | `MATERIAL` | `CARBON-STEEL` \| `STAINLESS` |
| `schedule` | `SCHEDULE` | `10` \| `20` \| `40` \| `80` \| `120` \| `160` |
| `nominal_diam` | `NOMINAL_DIAM` | [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED] token，[NON-ENGLISH REDACTED] `-IN` [NON-ENGLISH REDACTED]） |
| `length` | `LENGTH` | [NON-ENGLISH REDACTED] |
| `length_unit` | `LENGTH` [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] `meter`；[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED] |

### 2.1 [NON-ENGLISH REDACTED] `OPT_DIAM` [NON-ENGLISH REDACTED]

`PIPE` [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] schedule token [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]
`Data\Blocks\&lt;BLK&gt;\Input\LENGTH`；[NON-ENGLISH REDACTED] `PI` [NON-ENGLISH REDACTED]
`Data\Blocks\PI\Input\LENGTH`。

[NON-ENGLISH REDACTED] `OPT_DIAM`：

| `OPT_DIAM` [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|-----------------|-------------------|------|
| `OSCHED` schedule [NON-ENGLISH REDACTED] | `MATERIAL`、`SCHEDULE`、`NOMINAL_DIAM`、`LENGTH` | [NON-ENGLISH REDACTED] `configure_pipe_schedule_sizing(...)` [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `IN_DIAM` |
| direct inner-diameter / `OINNER` [NON-ENGLISH REDACTED] | `IN_DIAM`、`LENGTH` | `IN_DIAM` [NON-ENGLISH REDACTED] `Data\Blocks\&lt;BLK&gt;\Input\IN_DIAM`，[NON-ENGLISH REDACTED] `Data\Blocks\PI\Input\IN_DIAM` |

[NON-ENGLISH REDACTED] completion [NON-ENGLISH REDACTED] UI Next [NON-ENGLISH REDACTED] pipe length，[NON-ENGLISH REDACTED] `LENGTH`；[NON-ENGLISH REDACTED]
`OPT_DIAM` [NON-ENGLISH REDACTED] direct inner-diameter [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `IN_DIAM` [NON-ENGLISH REDACTED]。

**`nominal_diam` [NON-ENGLISH REDACTED] option list：**

`0.25-IN`, `0.375-IN`, `0.5-IN`, `0.75-IN`, `1-IN`, `1.5-IN`, `2-IN`, `3-IN`, `4-IN`, `5-IN`, `6-IN`, `8-IN`, `10-IN`, `12-IN`, `14-IN`, `16-IN`, `18-IN`, `20-IN`, `24-IN`, `30-IN`, `36-IN`, `42-IN`, `48-IN`, `54-IN`, `60-IN`, `66-IN`, `72-IN`, `78-IN`, `84-IN`, `90-IN`, `96-IN`


helper [NON-ENGLISH REDACTED]（[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]）：`OPT_DIAM=OSCHED` → `MATERIAL` → `SCHEDULE` → `NOMINAL_DIAM` → `LENGTH`。

[NON-ENGLISH REDACTED] skill `aspen-pipe-material-and-schedule`。

---

## 3. [NON-ENGLISH REDACTED] MCP

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|------|
| `create_pipe` | `block_name` | [NON-ENGLISH REDACTED] PIPE [NON-ENGLISH REDACTED] |
| `create_material_stream` | `stream_name` | [NON-ENGLISH REDACTED] |
| `list_block_ports` | `block_name` | [NON-ENGLISH REDACTED] |
| `connect_stream` | `block_name`, `stream_name`, `port_name` | [NON-ENGLISH REDACTED] Input |
| `check_block_completion` | `block_name` | [NON-ENGLISH REDACTED] completion |
| `check_next_completion_status` | — | run [NON-ENGLISH REDACTED] |
| `engine_run` | — | [NON-ENGLISH REDACTED] |

---

## 4. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| [NON-ENGLISH REDACTED] | REP [NON-ENGLISH REDACTED] `OPT-DIAM`、`MATERIAL`、`SCHEDULE`、`NOMINAL-DIAM`、`LENGTH`；[NON-ENGLISH REDACTED] helper [NON-ENGLISH REDACTED] `readbacks` / `check_ok` |
| [NON-ENGLISH REDACTED] | REP [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] |

---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| Agent [NON-ENGLISH REDACTED] | `configure_pipe_schedule_sizing` |
| [NON-ENGLISH REDACTED] skill | `aspen-pipe-material-and-schedule` |

```

### FILE: docs/hardcoded_script_plan/block_type_inject/valve.md
Reason: block-family Aspen surface selected from task profile
```text
# Block-Type [NON-ENGLISH REDACTED]：VALVE（[NON-ENGLISH REDACTED]）

- **[NON-ENGLISH REDACTED]**：`VALVE`
- **Aspen [NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] vendor preset [NON-ENGLISH REDACTED]。

---

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

| Helper | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|--------|----------|------|
| `configure_valve_pressure_changer_outlet(...)` | `block_name`, `outlet_pressure`, `pressure_unit` | **[NON-ENGLISH REDACTED] / pressure changer**：`MODE=ADIAB-FLASH` → `OPT_DESIGN=P-OUT` → `P_OUT+unit` |
| `configure_valve_pressure_changer_pressure_drop(...)` | `block_name`, `pressure_drop`, `pressure_unit` | **pressure changer + [NON-ENGLISH REDACTED]**：`MODE=ADIAB-FLASH` → `OPT_DESIGN=P-DROP` → `P_DROP+unit` |
| `configure_valve_outlet_pressure_design(...)` | `block_name`, `outlet_pressure`, `pressure_unit`, [NON-ENGLISH REDACTED] `vendor_preset_id` | **[NON-ENGLISH REDACTED]**：`MODE=SET-PRESSURE` → `OPT_DESIGN=P-OUT` → `P_OUT+unit`；[NON-ENGLISH REDACTED] vendor [NON-ENGLISH REDACTED] `vendor_preset_id` |
| `list_valve_vendor_presets(client)` | — | [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] `(VAL_TYPE, MFGR, SERIES, SIZE)` [NON-ENGLISH REDACTED] |
| `apply_valve_vendor_preset(client, block_name=..., preset_id=...)` | `preset_id` | **[NON-ENGLISH REDACTED]** agent [NON-ENGLISH REDACTED] commercial geometry [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] |

**[NON-ENGLISH REDACTED] helper，[NON-ENGLISH REDACTED] `set_mode` / `set_opt_design` [NON-ENGLISH REDACTED] `P_OUT` [NON-ENGLISH REDACTED] `unit`。**

**Pressure changer**（GUI Calculation type = *Adiabatic flash for specified outlet pressure*）：`MODE=ADIAB-FLASH` [NON-ENGLISH REDACTED]，**Pressure specification** [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED]+[NON-ENGLISH REDACTED]：

| GUI [NON-ENGLISH REDACTED] | `OPT_DESIGN` | [NON-ENGLISH REDACTED] leaf | Helper |
|----------|--------------|-----------|--------|
| Outlet pressure | `P-OUT` | `P_OUT + unit` | `configure_valve_pressure_changer_outlet` |
| Pressure drop | `P-DROP` | `P_DROP + unit` | `configure_valve_pressure_changer_pressure_drop` |

[NON-ENGLISH REDACTED] — [NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED]**（[NON-ENGLISH REDACTED] VA1–VA4 [NON-ENGLISH REDACTED]）：

```python
outlet_pressure_value = ...  # effect pressure basis from task/table
client.invoke(&quot;configure_valve_pressure_changer_outlet&quot;,
    block_name=&quot;VA1&quot;,
    outlet_pressure=outlet_pressure_value,
    pressure_unit=&quot;kPa&quot;,
)
```

[NON-ENGLISH REDACTED] — [NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED] / ΔP**：

```python
delta_p_value = ...  # pressure drop from task
client.invoke(&quot;configure_valve_pressure_changer_pressure_drop&quot;,
    block_name=&quot;VA1&quot;,
    pressure_drop=delta_p_value,
    pressure_unit=&quot;kPa&quot;,
)
```

**[NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED] `set_val_type` / `set_mfgr` / `set_series` / `set_size`：[NON-ENGLISH REDACTED] script-agent **core MCP [NON-ENGLISH REDACTED]**（`main_core.py`），[NON-ENGLISH REDACTED] `apply_valve_vendor_preset` [NON-ENGLISH REDACTED]。

[NON-ENGLISH REDACTED] **design**（[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED] vendor [NON-ENGLISH REDACTED]，`MODE=SET-PRESSURE`）：

```python
outlet_pressure_value = ...  # numeric value from the task
client.invoke(&quot;configure_valve_outlet_pressure_design&quot;,
    block_name=&quot;VA&quot;,
    outlet_pressure=outlet_pressure_value,
    pressure_unit=&quot;MPa&quot;,
)
```

[NON-ENGLISH REDACTED] vendor / series / characteristic / nominal size [NON-ENGLISH REDACTED]，**[NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED] §2.4 catalog [NON-ENGLISH REDACTED] `preset_id`，[NON-ENGLISH REDACTED]：

```python
outlet_pressure_value = ...  # numeric value from the task
selected_preset_id = &quot;...&quot;  # from list_valve_vendor_presets / §2.4 catalog
client.invoke(&quot;configure_valve_outlet_pressure_design&quot;,
    block_name=&quot;VA&quot;,
    outlet_pressure=outlet_pressure_value,
    pressure_unit=&quot;MPa&quot;,
    vendor_preset_id=selected_preset_id,
)
```

[NON-ENGLISH REDACTED] design [NON-ENGLISH REDACTED] preset：

```python
client.invoke(&quot;apply_valve_vendor_preset&quot;,
    block_name=&quot;VA&quot;,
    preset_id=selected_preset_id,
)
```

[NON-ENGLISH REDACTED]-only [NON-ENGLISH REDACTED] vendor preset；[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、[NON-ENGLISH REDACTED]、nominal size [NON-ENGLISH REDACTED] commercial geometry [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] `vendor_preset_id` [NON-ENGLISH REDACTED] `safe.apply_valve_vendor_preset(...)`。

---

## 1. [NON-ENGLISH REDACTED]（CRITICAL）

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|----------|------|
| [NON-ENGLISH REDACTED] | Input | [NON-ENGLISH REDACTED] `list_block_ports` + `connect_stream`，[NON-ENGLISH REDACTED] |
| `MODE` | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | `MODE` [NON-ENGLISH REDACTED] Valve [NON-ENGLISH REDACTED] calculation type gate，[NON-ENGLISH REDACTED] |
| `OPT_DESIGN` | `P_OUT` / `P_DROP` | **`P-OUT`** → `set_p_out(..., unit=...)`；**`P-DROP`** → `set_p_drop(..., unit=...)` |
| [NON-ENGLISH REDACTED] + unit | Fill / run | [NON-ENGLISH REDACTED] `OPT_DESIGN` [NON-ENGLISH REDACTED] leaf [NON-ENGLISH REDACTED] **unit**；[NON-ENGLISH REDACTED] unit [NON-ENGLISH REDACTED] TypeError |
| commercial geometry | completion [NON-ENGLISH REDACTED] Manufacturer/Series/Size | **[NON-ENGLISH REDACTED]** `list_valve_vendor_presets` → `apply_valve_vendor_preset`；[NON-ENGLISH REDACTED] |

**Commercial valve geometry [NON-ENGLISH REDACTED]。** Aspen [NON-ENGLISH REDACTED] option list；`apply_valve_vendor_preset` [NON-ENGLISH REDACTED] `VAL_TYPE → MFGR → SERIES → SIZE` [NON-ENGLISH REDACTED]。

---

## 2. Core MCP / HTTP Operations

| MCP operation | Aspen [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|---------------|------------|---------------|------|
| `set_mode` | `MODE` | ADIAB-FLASH / SET-PRESSURE / CALC-PRESSURE | **Calculation type gate**。[NON-ENGLISH REDACTED] §2.1；[NON-ENGLISH REDACTED] pressure/design/rating/vendor [NON-ENGLISH REDACTED]。 |
| `set_opt_design` | `OPT_DESIGN` | `P-OUT` / `P-DROP` | GUI **Pressure specification**；[NON-ENGLISH REDACTED] §2.2 |
| `set_p_out` | `P_OUT` | **`value` + `unit`** | **`OPT_DESIGN=P-OUT`** → `\Data\Blocks\&lt;ID&gt;\Input\P_OUT` |
| `set_p_drop` | `P_DROP` | **`value` + `unit`** | **`OPT_DESIGN=P-DROP`** → `\Data\Blocks\&lt;ID&gt;\Input\P_DROP` |
| `set_check_choke` | `CHECK_CHOKE` | NO / YES | [NON-ENGLISH REDACTED] choking [NON-ENGLISH REDACTED] `NO`。 |
| `set_pdrp_fac` | `PDRP_FAC` | float | [NON-ENGLISH REDACTED] rating factor；[NON-ENGLISH REDACTED]。 |
| `set_prec_fac` | `PREC_FAC` | float | [NON-ENGLISH REDACTED] rating factor；[NON-ENGLISH REDACTED]。 |
| `list_valve_vendor_presets` | — | read-only | [NON-ENGLISH REDACTED] preset [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `safe.list_valve_vendor_presets`。 |
| `apply_valve_vendor_preset` | `VAL_TYPE/MFGR/SERIES/SIZE` | `preset_id` | **[NON-ENGLISH REDACTED]** commercial geometry [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `safe.apply_valve_vendor_preset`。 |

`vendor_preset_id` [NON-ENGLISH REDACTED] `PDRP_FAC` / `PREC_FAC` [NON-ENGLISH REDACTED]：Aspen [NON-ENGLISH REDACTED] commercial
Library Valve [NON-ENGLISH REDACTED] pressure/recovery factors [NON-ENGLISH REDACTED]。[NON-ENGLISH REDACTED]
`configure_valve_outlet_pressure_design(..., vendor_preset_id=...)` [NON-ENGLISH REDACTED]
`set_pdrp_fac` / `set_prec_fac`；helper [NON-ENGLISH REDACTED] rating factors [NON-ENGLISH REDACTED]
`rating_factors_skipped_due_to_vendor_preset`。

### 2.1 `MODE` / Calculation Type

`Data\Blocks\&lt;B&gt;\Input\MODE` [NON-ENGLISH REDACTED] GUI [NON-ENGLISH REDACTED] **Calculation type**，[NON-ENGLISH REDACTED] Valve [NON-ENGLISH REDACTED] function gate：

| `MODE` [NON-ENGLISH REDACTED] | GUI [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
| --- | --- | --- | --- |
| `ADIAB-FLASH` | Adiabatic flash for specified outlet pressure (pressure changer) | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] valve coefficient | [NON-ENGLISH REDACTED] `OPT_DESIGN=P-OUT` + `P_OUT` |
| `SET-PRESSURE` | Calculate valve flow coefficient for specified outlet pressure (design) | [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | `OPT_DESIGN=P-OUT` + `set_p_out(..., unit=...)` + [NON-ENGLISH REDACTED] vendor [NON-ENGLISH REDACTED] `apply_valve_vendor_preset` |
| `CALC-PRESSURE` | Calculate outlet pressure for specified valve (rating) | [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]/flow coefficient，[NON-ENGLISH REDACTED] Aspen [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] rating [NON-ENGLISH REDACTED]，[NON-ENGLISH REDACTED] vendor geometry、`OPT_RATING`、`VAL_POSN` [NON-ENGLISH REDACTED] `FLO_COEF` |

`MODE` [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] design [NON-ENGLISH REDACTED] rating，Aspen [NON-ENGLISH REDACTED] valve vendor/size/position；[NON-ENGLISH REDACTED] rating [NON-ENGLISH REDACTED] pressure changer，[NON-ENGLISH REDACTED]。

### 2.2 `OPT_DESIGN` / Pressure Specification（option + value）

GUI [NON-ENGLISH REDACTED] **Pressure specification** [NON-ENGLISH REDACTED] **[NON-ENGLISH REDACTED] radio + [NON-ENGLISH REDACTED]** [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] option，[NON-ENGLISH REDACTED] leaf。

| `OPT_DESIGN` | GUI [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] tree leaf | MCP [NON-ENGLISH REDACTED] |
|--------------|---------|---------------|----------|
| `P-OUT` | Outlet pressure | `\Data\Blocks\&lt;ID&gt;\Input\P_OUT` | `set_opt_design(..., value=&quot;P-OUT&quot;)` [NON-ENGLISH REDACTED] `set_p_out(..., value=..., unit=...)` |
| `P-DROP` | Pressure drop | `\Data\Blocks\&lt;ID&gt;\Input\P_DROP` | `set_opt_design(..., value=&quot;P-DROP&quot;)` [NON-ENGLISH REDACTED] `set_p_drop(..., value=..., unit=...)` |

**[NON-ENGLISH REDACTED]**：

- [NON-ENGLISH REDACTED] **[NON-ENGLISH REDACTED]** → `P-OUT` + `P_OUT`（`configure_valve_outlet_pressure_design` [NON-ENGLISH REDACTED]）。
- [NON-ENGLISH REDACTED] **[NON-ENGLISH REDACTED]**（inlet − outlet）→ `P-DROP` + `P_DROP`；**[NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED] `P-DROP` [NON-ENGLISH REDACTED] `P_OUT`。
- [NON-ENGLISH REDACTED] **unit**（[NON-ENGLISH REDACTED] `bar`、`MPa`）；[NON-ENGLISH REDACTED] float [NON-ENGLISH REDACTED] TypeError。

### 2.3 Rating [NON-ENGLISH REDACTED] enum（`MODE=CALC-PRESSURE` [NON-ENGLISH REDACTED]）

| MCP / [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] token | [NON-ENGLISH REDACTED] |
|------------|-----------|------|
| `set_opt_rating` / `OPT_RATING` | `VAL-POSN` \| `FLOW-COEF` | Rating [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] |
| `set_char_eq` / `CHAR_EQ` | `LINEAR` \| `PARABOLIC` \| `HYPERBOLIC` \| `SQUARE-ROOT` \| `QUICK-OPENING` \| `EQUAL-PERCENTAGE` | [NON-ENGLISH REDACTED] |
| `set_opt_min_pres` / `OPT_MIN_PRES` | `GLOBAL` \| `SPECIFY` \| `CHOKING` | Rating [NON-ENGLISH REDACTED] |

### 2.4 Commercial Geometry Presets（[NON-ENGLISH REDACTED]）

[NON-ENGLISH REDACTED] **[NON-ENGLISH REDACTED]** [NON-ENGLISH REDACTED] agent [NON-ENGLISH REDACTED] MCP [NON-ENGLISH REDACTED]；[NON-ENGLISH REDACTED] `preset_id`：

| [NON-ENGLISH REDACTED] | Tree path [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
| --- | --- | --- |
| `VAL_TYPE` | `Data\Blocks\B1\Input\VAL_TYPE` | [NON-ENGLISH REDACTED] `apply_valve_vendor_preset` |
| `MFGR` | `Data\Blocks\B1\Input\MFGR` | [NON-ENGLISH REDACTED] `apply_valve_vendor_preset` |
| `SERIES` | `Data\Blocks\B1\Input\SERIES` | [NON-ENGLISH REDACTED] `apply_valve_vendor_preset` |
| `SIZE` | `Data\Blocks\B1\Input\SIZE` | [NON-ENGLISH REDACTED] `apply_valve_vendor_preset` |

[NON-ENGLISH REDACTED]（`data/code/set_valve_variables/set_valve_variables.py` → `_VALVE_VENDOR_PRESETS`）：

| `preset_id` | `VAL_TYPE` | `MFGR` | `SERIES` | `SIZE` |
| --- | --- | --- | --- | --- |
| `neles_ball_v810_equal_pct_2in` | `BALL` | `NELES-JAMESBURY` | `V810_EQUAL_PERCENT_FLOW` | `2-IN` |
| `neles_butterfly_v810_equal_pct_3in` | `BUTTERFLY` | `NELES-JAMESBURY` | `V810_EQUAL_PERCENT_FLOW` | `3-IN` |
| `neles_globe_v500_equal_pct_1p5in` | `GLOBE` | `NELES-JAMESBURY` | `V500_EQUAL_PERCENT_FLOW` | `1.5-IN` |
| `neles_globe_v500_linear_1p5in` | `GLOBE` | `NELES-JAMESBURY` | `V500_LINEAR_FLOW` | `1.5-IN` |
| `neles_globe_v810_equal_pct_1p5in` | `GLOBE` | `NELES-JAMESBURY` | `V810_EQUAL_PERCENT_FLOW` | `1.5-IN` |
| `neles_globe_v810_linear_1p5in` | `GLOBE` | `NELES-JAMESBURY` | `V810_LINEAR_FLOW` | `1.5-IN` |

[NON-ENGLISH REDACTED] → preset [NON-ENGLISH REDACTED]：

| [NON-ENGLISH REDACTED] | `preset_id` |
| --- | --- |
| V810 equal percent flow globe 1.5 in | `neles_globe_v810_equal_pct_1p5in` |
| V810 linear flow globe 1.5 in | `neles_globe_v810_linear_1p5in` |
| V500 equal percent globe 1.5 in | `neles_globe_v500_equal_pct_1p5in` |

Agent [NON-ENGLISH REDACTED]：

- **Design [NON-ENGLISH REDACTED]**：`configure_valve_outlet_pressure_design(...)`；[NON-ENGLISH REDACTED] `unit`。
- **[NON-ENGLISH REDACTED] vendor/[NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED]**：[NON-ENGLISH REDACTED] helper [NON-ENGLISH REDACTED] `vendor_preset_id`，[NON-ENGLISH REDACTED] `apply_valve_vendor_preset`；**[NON-ENGLISH REDACTED]**[NON-ENGLISH REDACTED] `set_val_type` / `set_mfgr` / `set_series` / `set_size`。
- completion [NON-ENGLISH REDACTED] Manufacturer/Series/Size [NON-ENGLISH REDACTED]：[NON-ENGLISH REDACTED] `apply_valve_vendor_preset`，[NON-ENGLISH REDACTED] `MODE` [NON-ENGLISH REDACTED] `CALC-PRESSURE`。

---

## 3. [NON-ENGLISH REDACTED] MCP

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|------|
| `create_valve` | `block_name` | [NON-ENGLISH REDACTED] VALVE [NON-ENGLISH REDACTED] |
| `create_material_stream` | `stream_name` | [NON-ENGLISH REDACTED] |
| `list_block_ports` | `block_name` | [NON-ENGLISH REDACTED] |
| `connect_stream` | `block_name`, `stream_name`, `port_name` | [NON-ENGLISH REDACTED] Input |
| `check_block_completion` | `block_name` | [NON-ENGLISH REDACTED] completion |
| `check_next_completion_status` | — | run [NON-ENGLISH REDACTED] |
| `engine_run` | — | [NON-ENGLISH REDACTED] |

---

## 4. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|
| [NON-ENGLISH REDACTED]/[NON-ENGLISH REDACTED] | REP、helper readback payload |
| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] Input [NON-ENGLISH REDACTED] null；`P_OUT` [NON-ENGLISH REDACTED] `unit` [NON-ENGLISH REDACTED] |
| vendor [NON-ENGLISH REDACTED] | `apply_valve_vendor_preset` [NON-ENGLISH REDACTED] `readback` [NON-ENGLISH REDACTED] helper readback on `VAL_TYPE/MFGR/SERIES/SIZE` |

---

## 5. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|------|------|------|
| completion [NON-ENGLISH REDACTED] Valve Operation，Outlet pressure [NON-ENGLISH REDACTED] | `MODE=ADIAB-FLASH` + `P-OUT` [NON-ENGLISH REDACTED] `P_OUT` | `configure_valve_pressure_changer_outlet(...)` |
| completion [NON-ENGLISH REDACTED] Valve Operation，Pressure drop [NON-ENGLISH REDACTED] | `MODE=ADIAB-FLASH` + `P-DROP` [NON-ENGLISH REDACTED] `P_DROP` | `configure_valve_pressure_changer_pressure_drop(...)` |
| `set_p_out() missing 1 required positional argument: &#x27;unit&#x27;` | [NON-ENGLISH REDACTED] `set_p_out` [NON-ENGLISH REDACTED] value | [NON-ENGLISH REDACTED] `configure_valve_pressure_changer_outlet` / `configure_valve_outlet_pressure_design` [NON-ENGLISH REDACTED] `unit=&quot;MPa&quot;` |
| completion [NON-ENGLISH REDACTED] Manufacturer/Series/Size | [NON-ENGLISH REDACTED] vendor [NON-ENGLISH REDACTED] preset | [NON-ENGLISH REDACTED] §2.4 [NON-ENGLISH REDACTED] `preset_id`，[NON-ENGLISH REDACTED] `vendor_preset_id` [NON-ENGLISH REDACTED] `apply_valve_vendor_preset` |
| completion [NON-ENGLISH REDACTED] Manufacturer/Series/Size | `MODE=CALC-PRESSURE` [NON-ENGLISH REDACTED] rating | [NON-ENGLISH REDACTED] `SET-PRESSURE` + `P-OUT`，[NON-ENGLISH REDACTED] vendor preset |
| vendor [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] | **[NON-ENGLISH REDACTED]** `apply_valve_vendor_preset(preset_id=...)` |

---

## 9. [NON-ENGLISH REDACTED]

| [NON-ENGLISH REDACTED] | [NON-ENGLISH REDACTED] |
|----|------|
| Core operations | 6 pressure/design setters + 2 vendor preset helpers |
| [NON-ENGLISH REDACTED] helper | `configure_valve_pressure_changer_outlet` / `configure_valve_pressure_changer_pressure_drop`（[NON-ENGLISH REDACTED]）；`configure_valve_outlet_pressure_design`（design）；vendor **[NON-ENGLISH REDACTED]** `apply_valve_vendor_preset` |
| [NON-ENGLISH REDACTED] | `ADIAB-FLASH` [NON-ENGLISH REDACTED] calculation type [NON-ENGLISH REDACTED]；`P-OUT` [NON-ENGLISH REDACTED] `P_OUT+unit`，`P-DROP` [NON-ENGLISH REDACTED] `P_DROP+unit` |

```

### FILE: aspen_agent_skills/guides/aspen-task-execution-order/SKILL.md
Reason: selected skill for task block family
```text
---
name: aspen-task-execution-order
description: Core execution order for generated Aspen scripts. Use for every Aspen task to sequence setup, topology, analysis objects, engine runs, and final evidence without hiding failures behind later steps.
---

# Aspen Task Execution Order

## Unified Capability Call Contract

- Generated Aspen model operations use exactly `client.invoke(&quot;capability&quot;, **keyword_parameters)`.
- The capability name is a static, unqualified registry name. All business parameters are keywords matching the registered signature. Do not pass `client=`.
- `client.invoke` always returns `capability_result.v1` with root `success`, `capability`, `result`, `error`, and `diagnostics`. The registry owns local-versus-HTTP implementation; generated code never selects transport or retries another namespace.
- Put required calls inside `runtime.stage(name, lambda: client.invoke(...), required=True)`. Use `required=False` only for optional diagnostics. A failed required capability is upgraded by the runtime to `SlimStageFailure`.
- Generated slim source must not call `safe.call`, `safe.probe_call`, client-first `safe.*` Aspen helpers, `client.execute`, `client.execute_http`, `local:`, or `http:`. Those are framework-internal compatibility/transport surfaces.
- Unknown capability names, policy-blocked operations, dynamic names, positional business arguments, missing required keywords, and unknown keywords fail before Aspen HTTP/COM.
- `read_stream_output` without `variable` returns a state summary, not purity or a scalar. Component metrics require an explicit supported `variable` and `component_name`.

## Core Rule

Every generated Aspen script should follow this order unless the task explicitly proves a different order is required:

1. Components and property methods.
2. Create all task-visible blocks and material/energy streams.
3. Connect the complete task-visible topology and verify live port readback.
4. Stream state/composition inputs and block specifications, with object-level completion.
5. Native analysis objects such as Design Spec, Sensitivity, and Optimization, including field-level readback.
6. Workflow-level completion / Next gate.
7. Engine run and REP/APW/BKP export.
8. Stream/result readback from the same trusted run.
9. Summary finalization from the same session and current run.

## Why This Matters

Aspen can accept many writes before the model is actually runnable. A later engine run cannot fix a missing upstream topology/specification problem, and a Design Spec that is never configured cannot be recovered by summary text.

Topology is the first real Aspen-state transaction after components/property method. Create blocks and streams, connect all required inlet/outlet/energy ports, and record live port readback before writing block variables such as pressures, reflux ratios, duties, geometry, stage counts, or reaction/analysis rows. Many valid setters fail or write to the wrong surface when the owning block has not yet materialized its feed/product context; do not “repair” those failures by changing the requested specification. Repair the missing topology first.

In particular:

- Design Spec, Sensitivity, and Optimization objects must be configured and read back before the final run/export if the task requires them to participate in the run.
- For any DS/SA/OPT task, follow `aspen_agent_skills/guides/analysis-object-transaction-finalization/SKILL.md`: object configuration, field readbacks, post-analysis run/export, native output collection, and final decision evidence are one transaction.
- For two-phase base→analysis tasks, follow `aspen_agent_skills/guides/base-analysis-handoff-contract/SKILL.md` before leaving base. A base phase without checkpoint, workflow readiness, target/manipulated candidates, readback plan, and artifact plan is not ready for analysis repair.
- If an analysis object is proof-only, configure and read it back before finalization and state clearly that it is proof-only.
- Do not place native analysis setup only after `run_completion_engine_and_export(...)`; if completion/export fails first, the analysis evidence will never be produced.
- Do not let final summary text claim an analysis object was configured unless successful tool calls or tree readbacks exist.

## Property Method Ensure Pattern

Property method setup is an idempotent ensure step, not a one-shot create step.

Use:

```python
client.invoke(&quot;ensure_property_method&quot;,  method=&quot;UNIQUAC&quot;)
```

This must set and read back the active global option-set fields. If Aspen reports `OPTION-SETS (...) already exists`, treat that as non-fatal only when the global method readback still matches the requested method.

For block-local methods, use:

```python
client.invoke(&quot;configure_block_property_method&quot;,  block_name=&quot;A1&quot;, method=&quot;UNIQUAC&quot;)
```

Then read back `\Data\Blocks\&lt;BLOCK&gt;\Input\OPSETNAME` for each block.

## Gating Discipline

- Gate feed/input streams as inputs; do not require calculated product streams to be input-complete before run.
- Gate required blocks only after all mandatory outlet streams and specifications have been written.
- If a Mixer or shared-port block stays incomplete, read live ports and completion diagnostics before running.
- Run `check_next_completion_status` or equivalent workflow completion before `engine_run`.
- Do not wrap Aspen engine execution in a fixed overall timeout. GUI discovery/click steps and small diagnostic probes may be bounded, but once an Aspen engine run has started, wait for Aspen to finish and then read `PER_ERROR` / REP status.
- Treat `engine_run.success` as necessary but not sufficient: also read `PER_ERROR`, parse REP status, and verify result values from current-run artifacts. Follow `aspen_agent_skills/guides/trusted-run-evidence-gate/SKILL.md` when Run-Status, REP, current history, or result readbacks are missing.
- For material-stream output values after a trusted run: **final scored** metrics use `rep_readback_targets` + `collect_llm_rep_readback_evidence`. **Probe/scaffold matrices** (`run_standard_probe_matrix`, per-row readbacks) keep `read_stream_output` — see probe-sweep-decision-readback.

## Slim Runtime Session Ownership

- In `own-agent-slim`, import `SlimTaskSpec`, `SlimTaskOutcome`, `run_slim_task`, `stream_rep_targets`, and `block_rep_targets` from `script_agent_exp.slim_task_runtime`, and model helpers as `import script_agent_exp.safe_aspen_calls as safe`. Define `TASK_SPEC` plus `configure(runtime)`, use `runtime.client`, and enter through `run_slim_task(spec=TASK_SPEC, configure=configure)`.
- Runtime uniquely owns common fixed session/setup parameters, task identity, GUI policy, health, recorder and CLI. Set units through `TASK_SPEC.inset`; do not generate `AspenHttpClient`, session/setup wrappers or calls, custom CLI, signature filtering/probing, or local-exception HTTP fallback. This restriction is specific to common lifecycle operations, not legitimate model/REP readback wrappers.
- Legacy `ensure_session(initial_bkp=None, show_gui=None, inset=None)` returns `None` on success and raises on failure; never classify `None` as a failed envelope. `task_name`/`task_key` are not session-method arguments: invalid signatures fail clearly, never silently drop identity. Slim runtime uses its canonical `ensure_runtime_session(*, show_gui=False, inset=&quot;SI&quot;)` receipt without changing regular consumers.
- Initial inherited legacy seeds may execute their existing direct void session call unchanged, with explicit `migration_required` source-contract metadata. New slim generation must use the runtime template; any seed migration is an explicit semantics-preserving edit or a recorded blocker, not a silent process algorithm change. Initial, mini and resume source contracts run before model imports/HTTP/COM.

## Slim Parent Evidence Ownership

- Newly generated or repaired slim code must retain the runtime template. Never call, alias, store, test, or wrap `ensure_session` / `ensure_runtime_session`, including required-step lambdas or capability dispatch. Unchanged legacy seed compatibility is not a code-generation template.
- Parent alone registers and observes service evidence. Do not import parent transaction/observer internals, implement registration, seed/write receipts, guess `/session/evidence` POST endpoints, patch server routes, or fabricate identities, hashes, run/trust status, or evidence documents.
- Missing routes, registration, observer receipts, and infrastructure failures are parent blockers, not model configuration repairs. Preserve the original operation, exception, and diagnostic context for the parent; never convert failure to success or substitute generated evidence. Runtime owns exception persistence and summary writing.
- `runtime.stage`, `runtime.attach_artifact`, and `SlimTaskOutcome` carry actual model/helper facts and semantic handoff fields, not parent trust receipts. Legal model/REP readback helpers remain supported.

## Pure Declarations And Snapshot Ownership

- Import `stream_rep_targets` and `block_rep_targets` from `script_agent_exp.slim_task_runtime`; they construct REP requests without a client. Lazy `safe` aliases are compatibility only, not registered capabilities or HTTP operations. Never route declarations through `call`, `invoke`, `execute`, or an HTTP fallback; preserve required targets when correcting imports.
- `finalize_task_summary` returns a detached whole-summary snapshot. Replace the current summary with that return; never nest it under its own stages/readbacks. Do not pass a live summary into its own artifact. Shared sibling evidence is legal, ancestor/self references are not; record the circular edge and original failure separately rather than stringify or suppress it.

## Summary Contract

The final `summary.json` should expose:

- top-level `completion`, `engine_run`, `per_error`, `run_status`, and `evidence`;
- REP/APW/BKP paths or explicit unavailable-artifact reasons;
- analysis object evidence under `analysis_objects`;
- validation checks that cite `rep_readback_evidence`, `rep_readback_targets`, or current-run REP/APW artifacts.

Do not use prose-only claims, stale call logs, or placeholder artifact paths as evidence.

## Analytic Tasks Under Slim Runtime Finalization

A task may have an authoritative analytic answer (for example, a supplied constant-relative-volatility Rayleigh calculation) and require no Aspen unit-operation result. The slim runtime still owns one final Aspen `engine_run` and evidence export. Therefore the generated script must not leave an empty Aspen document. Before returning `SlimTaskOutcome`, establish at least a runnable Aspen evidence state:

1. add every task component through `add_components_by_cas`;
2. verify landed component IDs;
3. set a task-compatible property method; and
4. ensure workflow completion can reach the final runtime run without `NO COMPONENTS HAVE BEEN DEFINED`.

Do not replace the task-provided analytic equation with Aspen thermodynamics. The Aspen state is execution/evidence support; the declared analytic calculation remains the result source.

## Figure-grounded topology contract

When the current task contains a process figure, the visible labeled equipment and streams are an authoritative topology contract unless the task text or explicit user authority resolves an ambiguity. Generated topology must account for every required visible node/edge and must not add, remove, split, or reroute visible process objects merely to make completion easier.

In cached/codegen-only execution, figure grounding may be reused only when it is tied to the same task image. If a task contains a figure but no parent-scoped or same-image leaf grounding is available, fail closed before code generation rather than silently infer topology from prose alone. A cached figure artifact is useful only when its summary is actually injected into the model context; copying or hashing the file without prompt injection is not grounding.

## Complex Sensitivity collection boundary

For RadFrac or recycle Sensitivity with `collect=True`, insert a same-base preflight between base specifications and analysis collection: workflow completion, trusted base run, checkpoint, and handoff provenance must all refer to the complete topology being swept. Partial row dry-up/nonconvergence is a `partial_row_solver_failure`; preserve row coordinates/counts and deep engine/history codes for mini repair. Whole-engine failure is `engine_failure`. Both remain failed collection outcomes even when configuration and Fill succeeded.

```

### FILE: aspen_agent_skills/guides/aspen-property-method-selection/SKILL.md
Reason: selected skill for task block family
```text
---
name: aspen-property-method-selection
description: Selects and verifies Aspen global thermodynamic/property methods. Use when a task mentions property method, thermodynamic method, option set, VLE, relative volatility, alpha, NRTL, UNIQUAC, WILSON, IDEAL, Peng-Robinson, SRK, or when results are sensitive to phase equilibrium/property-package assumptions.
---

# Aspen Property Method Selection

## Selection Order

Choose the property method from the strongest available evidence:

1. Use an explicit task instruction first, such as NRTL, UNIQUAC, WILSON, IDEAL, Peng-Robinson, SRK, ELECNRTL, or another named option set.
   Treat the exact Aspen option-set token as task data. Do not collapse `RK-SOAVE` into `SRK`, or vice versa, merely because both are Soave-family cubic EOS names. Verify the exact requested token through live available methods/readback; if rejected, report that capability/token mismatch rather than silently substituting another option set.
2. If a trusted base case, standard BKP/APW, or provided reference model is part of the task evidence, match its global property method unless the task explicitly asks for a different one.
3. If the task gives VLE data such as relative volatility, activity-coefficient model, azeotrope/LLE behavior, electrolyte behavior, or equation-of-state assumptions, choose a method consistent with that evidence and document the limitation.
4. If none of the above exists, choose a conservative common method for the component class and state that it is an assumption. Do not silently default to IDEAL for non-ideal liquid systems.

## Phase-Model Overlay Is Part Of The Task Method

A liquid activity-coefficient method and a vapor EOS are separate requirements. Selecting UNIFAC alone does not establish ideal-gas vapor: Aspen&#x27;s default UNIFAC option set can retain REDLICH-KWONG vapor. When the task explicitly requests UNIFAC liquid plus ideal-gas vapor (IG), call the existing `safe.configure_unifac_ideal_vapor(client)` rather than only `ensure_property_method(..., method=&quot;UNIFAC&quot;)`. Require helper success and its readbacks `GMODIFY=YES`, `GVAPOREOS=ESIG`, and retained `GLIQGAMMA=GMUFAC`. Do not replace the whole method with IDEAL or silently preserve RK to obtain convergence.

After the trusted run, request the effective liquid and vapor models from the current native REP property-method/block sections and verify UNIFAC / IDEAL GAS for the task-relevant blocks. Include method and phase-model REP targets in the normal final readback transaction; the global option-set name, setter success, or separation targets alone do not prove the vapor overlay participated. Preserve conflicting REP evidence as a blocker (including local option-set overrides), export the checkpoint, and verify the overlay survives reload. If the helper or effective-model evidence is unavailable, report a capability boundary; do not invent an operation or declare task completion from a method label.

## Candidate Exploration

When the task does not name a fixed property method and the target results are
phase-equilibrium-sensitive, do not treat the first plausible method as settled.
Record a small candidate set and compare it with the same topology and operating
handles before final selection.

Use this as a generic pattern:

- Pick candidates from the component class and task wording, not from a previous
  case&#x27;s numeric optimum.
- Run the same base topology under each candidate method when Aspen can converge
  it.
- Compare task-level responses from REP/Markdown evidence: product quality,
  recovery/yield, phase split, duty/load, convergence status, and any objective
  or constraint metrics.
- Keep failed methods in the comparison table with the Aspen blocker instead of
  silently dropping them.
- Select the final method only after documenting why it is task-consistent or
  why its response table is preferable. If the task explicitly fixes the method,
  do not override it during exploration.

For complex optimization tasks, property-method candidates are a search dimension
alongside operating/design handles such as feed or solvent rates, reflux/boilup,
product-rate specs, stage count, and feed locations.

## Global Method Setup

Set the flowsheet-level method before the first run and before relying on stream/block results:

```python
pm = client.invoke(&quot;ensure_property_method&quot;,  method=&quot;NRTL&quot;)
if not pm.get(&quot;success&quot;):
    raise RuntimeError(pm)
```

or, when using raw operations:

```python
pm = client.invoke(&quot;set_property_method&quot;, method=&quot;NRTL&quot;)
if not (pm.get(&quot;result&quot;) or {}).get(&quot;success&quot;):
    raise RuntimeError(pm)
```

Treat an `OPTION-SETS already exists` response as non-fatal only when readback confirms the requested method.

## PER_ERROR and property-method routing

When raw `PER_ERROR` is nonzero and the current-run diagnostic mentions a property method, free-water method, phase-equilibrium warning, or an input-translation error around thermodynamic specifications, treat the active global property method as an unresolved causal input until it is read back. Use this order:

1. Read the current global method/option-set token from Aspen.
2. Compare the exact token against the task and trusted same-case evidence; do not normalize family names or silently substitute a related EOS.
3. If the diagnostic is method-specific, apply only the helper documented for that exact active method, then rerun and require raw `PER_ERROR=0` plus current REP evidence.
4. If method readback is missing or ambiguous, keep the case unresolved and repair/read back the method before changing flowsheet physics.

Do not route every `PER_ERROR=1` to a property-method change: topology, specification ownership, missing inputs, and numerical convergence remain separate failure classes. Property-method routing requires current-run diagnostic evidence, not magnitude or method-family similarity.

## SRK Free-Water Setup And Warning Repair

Only after successful readback proves the active global method is exactly `SRK`,
and a current-run diagnostic requires the SRK free-water correction, call
`safe.configure_srk_free_water_steamnbs(client)` for SRK/free-water setup.
Map `FREE-WATER METHOD SHOULD BE STEAMNBS WHEN THE MAIN PROPERTY METHOD IS SRK`
and `DEFAULT FREE-WATER METHOD IS STEAM-TA` to this same helper, not an override.
The helper is registered Python/ReAct tooling backed by HTTP `typed helper write surface` /
`typed readback helper such as read_stream_output(...)`; it is not a standalone native HTTP operation. Prefer
`client.invoke(&quot;configure_srk_free_water_steamnbs&quot;)` for its registered local
transaction; compatible execute shares the registry and typed
`safe.configure_srk_free_water_steamnbs(client)` remains valid. Invoke returns
an envelope; typed helpers return direct payloads. Never retry through native transport.

Require successful setter and readback of
`\Data\Properties\Specifications\Input\GFREE_WATER=STEAMNBS`.
Do not substitute `FREE_WATER`: it has options but direct writes return
`AE_UNDERSPEC`. Preserve failed payloads and actual live returned options;
missing helper/field evidence is a capability boundary, not permission to invent
fields or tokens. A matching old readback cannot waive setter failure.

Keep raw nonzero SRK status blocking even if an old service reports effective
zero. Rerun to trusted raw `PER_ERROR=0` and cleared advisory, export the final
checkpoint/REP, then cold-reload and verify persisted method, free-water setting,
and trusted status. Preserve requested SRK; do not switch methods to hide the
warning. Expected block-local property comparison warning policy is unchanged.

## Token / Alias Repair Contract

Aspen property methods are exact option-set IDs, not prose names. Many IDs are
limited to eight characters. For example, the paper wording `Braun K10` should
land as Aspen token `BK10`; `BRAUN-K10` is a descriptive alias and can be
rejected with `ID must be eight characters or less`.

When `set_property_method` / `ensure_property_method` fails, treat the response
as a repair surface, not a reason to try a broad timeout loop:

- Preserve the full failed helper response in `summary.json` / call logs.
- Require `repair_hint`, `suggested_methods`, `available_methods`, and
  `available_methods_count` when the setter rejects a token.
- In runtime ruff repair, replace only the property token with the first
  task-consistent `suggested_methods` entry or one exact token from
  `available_methods`.
- Do not write `GBASEOPSET` / `GOPSETNAME` directly as a workaround until a
  listed token has succeeded through the helper and readback has been checked.
- Do not continue through a long candidate list after the first response gives
  a valid-token repair hint; fix the token and rerun.

## Verification

A property-method write is complete only when global readbacks match the intended method:

```text
\Data\Properties\Specifications\Input\GBASEOPSET
\Data\Properties\Specifications\Input\GOPSETNAME
```

Report the method in final evidence when phase equilibrium, vapor/liquid split, column separation, flash composition, or reaction equilibrium results depend on it.

## Binary Interaction Parameters

When a task explicitly asks to check binary interaction parameters, call the
compact helper after components and the global property method are in place:

```python
client.invoke(&quot;add_components_by_cas&quot;,  components=[...])
client.invoke(&quot;ensure_property_method&quot;,  method=&quot;NRTL&quot;)
bip = client.invoke(&quot;check_binary_interaction_parameters&quot;)
```

No inputs are required. The helper auto-discovers component IDs from the live
Aspen component table and uses the active global property method when `method`
is omitted. You may still pass `method=` or `components=` when the task names a
non-default subset.

Treat the compact result as the normal evidence surface:

- `check_ok`: True when the method parameter set exists with `PER_ERROR=0`, or
  when pair rows are visible in the bounded COM preview.
- `summary`: one-line explanation for summary.json / validator evidence.
- `verdict`: `pass` | `partial` | `fail`.
- `method_parameter_set.per_error_values`: primary structural completeness signal.

Pass `include_details=True` only when debugging; the default response omits
large COM table dumps and per-pair rows. Do not invent REP-text heuristics or
claim BIP completeness from `set_property_method` alone.

## Relative Volatility Tasks

When a task supplies a constant relative volatility:

- Do not assume the Aspen default property method reproduces that alpha.
- Either use the task&#x27;s constant-alpha calculation as a separate analytic reference, or use a trusted Aspen base/standard model property method and state that the Aspen result is a property-package approximation.
- If scoring or validation is tied to a standard BKP/APW, prefer matching the standard model&#x27;s property method over inventing a method from the case id.

## Block-Local Methods

This skill covers the global property method. If different blocks or cases must use different methods, also use `block-wise-property-methods` and verify each block&#x27;s `OPSETNAME` independently.

```

### FILE: aspen_agent_skills/guides/aspen-material-stream-composition-must-be-specified/SKILL.md
Reason: selected skill for task block family
```text
---
name: aspen-material-stream-composition-must-be-specified
description: &gt;-
  Choose MATERIAL stream state specs (TP/TV/PV) from task variables, set
  MASS-FLOW basis before kg/h component flows, and map Component Flow,
  Fraction, or Concentration must be specified to incomplete stream
  composition on Data\Streams\&lt;StreamName&gt;.
---

# Stream State Spec Selection

Use this skill when a task describes stream state with different variable combinations.

- When using the high-level helper, the signature is
  `safe.set_material_stream(client, *, stream_name, mixed_spec, basis,
  component_flows, flow_unit, temperature/pressure/vapor_fraction...)`. The
  `basis` keyword is mandatory. For molar component flows use
  `basis=&quot;MOLE-FLOW&quot;` with `flow_unit=&quot;kmol/hr&quot;`; for mass component flows use
  `basis=&quot;MASS-FLOW&quot;` with an explicit mass unit such as `kg/hr`.
- **Task feed in kg/h (mass flow):** After components exist, set the MATERIAL stream mixed spec and state (`TP` / `TV` / `PV` as required), then call `set_basis_mixed(MASS-FLOW)` **before** component flow writes. Use `set_flow_mixed` with the task&#x27;s numeric mass-flow rates, **canonical component IDs**, and an explicit mass-flow unit such as `unit=&quot;kg/hr&quot;` (the tool normalizes exact `kg/h` input to `kg/hr`). Do **not** rely on `MASS-FLOW` basis alone and do **not** omit `unit` for component-flow values; the tool should reject flow-basis writes without a unit. Do **not** convert kg/h to kmol/h unless the only live tool path is truly molar-flow and you document the molecular-weight conversion.
- **Unit continuity:** Prefer the units stated in the task for stream flow setters and probe axes whenever the live tool accepts them. If the task gives `kg/hr`, keep `unit=&quot;kg/hr&quot;` rather than switching to `kg/sec`, `lb/hr`, or `kmol/hr` unless there is a documented conversion reason and a `unit_reconciliation` entry. Always pass the `unit` keyword explicitly on component-flow setters.
- Choose the spec mode from the variables explicitly provided for each stream.
- Default mapping when the task wording is clear: `T + P -&gt; TP`, `T + vapor fraction -&gt; TV`, `P + vapor fraction or a defensible saturated-pressure statement -&gt; PV`.
- Handle each stream independently if the task mixes different state-spec styles.
- Preserve independent feed partitions, component amounts and phase/state even at equal T/P: equal T/P does not imply thermodynamic equivalence. A summed-composition TP stream can flash differently and change total inlet enthalpy. Use verified shared material inlets or a real adiabatic Mixer carrying its computed outlet state, not a fresh TP reset. Any permitted feed aggregation requires current-run phase/enthalpy readbacks, explicit units/property scope, total enthalpy-flow and energy-balance evidence; otherwise retain the separate feeds.
- For MATERIAL stream object-level completion, set the chosen mixed spec first, then the minimum state fields for that mode, then the first accepted component flow.
- In the validated minimal probes, `TP` completion needed basis plus `TEMP` and `PRES`, while `TV` and `PV` completion both succeeded with basis plus one named state variable and one component flow; `set_vfrac_mixed` was not required in those probes.
- Treat `set_vfrac_mixed` as a good follow-up candidate for `TV` or `PV`, not as an automatic first-pass requirement, unless the task or Aspen evidence clearly promotes it.

## Completion diagnostics (Material streams)

If **Material Stream Config** / stream input completion or Next shows **`Component Flow, Fraction, or Concentration must be specified.`**, the **stream&#x27;s composition/amount specification is incomplete** on **`Data\Streams\&lt;StreamName&gt;\Input\...`** (at least one of component flow, fraction, or concentration, consistent with the chosen basis). This is a **hard workflow gate**: the flowsheet will not advance until that stream is finished—fix the landed stream&#x27;s basis + state + component-side specs before downstream blocks.

## Material stream completion messages

| Aspen message (typical) | Meaning | First fix |
| --- | --- | --- |
| `Component Flow, Fraction, or Concentration must be specified.` | Composition/flow side not closed for this MATERIAL stream. | On **`Data\Streams\&lt;StreamName&gt;`**, complete basis + (as required) total flow and component flow / fraction / concentration per the active spec; re-run `check_stream_completion` / workflow Next. |

## Task mass flow (kg/h) and `material_stream_variables`

When the problem statement gives **per-component flow rates in kg/h** (or otherwise clearly as **mass flow**):

1. Complete stream spec order for MATERIAL streams still applies: mixed spec mode first (`set_mixed_spec_mixed`), then basis, then intensive state for that mode, then flows.
2. Set **`set_basis_mixed(MASS-FLOW)`** so Aspen treats subsequent flow entries in a **mass-flow** sense for that stream.
3. Call **`set_flow_mixed`** once per component with the **numeric values from the task**, **canonical `component_name` IDs** from the live component table, and an explicit mass-flow unit such as `unit=&quot;kg/hr&quot;` (or `unit=&quot;kg/h&quot;`, normalized by the tool).

**Schema vs chemistry:** Inspecting `set_flow_mixed` should show `kg/hr` (and may show `kg/h`) in the `unit` enum. If a stale schema lists only molar or standard-volumetric units, refresh the tool surface or call the HTTP operation with explicit `unit=&quot;kg/hr&quot;` if available; do **not** omit `unit` and rely on basis semantics. If the only safe path is truly molar flow, then document a **defensible kg/h → kmol/h** conversion using molecular weights and set **`MOLE-FLOW`** basis instead—do not guess.

**Validation:** Prefer `check_stream_completion` / readback on the stream after writes. Treat any **`unit_warning`** on a flow setter as evidence of wrong basis or wrong unit, not as a success.

## Decision tree

- If the task clearly gives temperature and pressure, `TP` is usually the best first guess.
- If the task clearly gives temperature and vapor fraction, `TV` is usually the best first guess.
- If the task clearly gives pressure and vapor fraction, or describes a saturated condition at a specified pressure that can defensibly map to vapor-fraction logic, `PV` is usually the best first guess.
- If the text is ambiguous, record the interpretation and let Aspen completion/readback decide whether extra state fields are still needed.

## Minimal completion bundles

- `TP` MATERIAL stream:
  - `create_material_stream`
  - add components successfully
  - `set_mixed_spec_mixed(TP)`
  - `set_basis_mixed(MOLE-FLOW)` **or** `set_basis_mixed(MASS-FLOW)` when the task specifies mass flows (e.g. kg/h); match basis to the task&#x27;s stated quantity type.
  - `set_temp_mixed`
  - `set_pres_mixed`
  - one accepted `set_flow_mixed` with explicit `unit` when basis is a flow basis
- `TV` MATERIAL stream:
  - `create_material_stream`
  - add components successfully
  - `set_mixed_spec_mixed(TV)`
  - `set_basis_mixed(MOLE-FLOW)`
  - `set_temp_mixed`
  - one accepted `set_flow_mixed` with explicit `unit` when basis is a flow basis
  - only add `set_vfrac_mixed` if completion still remains false
- `PV` MATERIAL stream:
  - `create_material_stream`
  - add components successfully
  - `set_mixed_spec_mixed(PV)`
  - `set_basis_mixed(MOLE-FLOW)`
  - `set_pres_mixed`
  - one accepted `set_flow_mixed` with explicit `unit` when basis is a flow basis
  - only add `set_vfrac_mixed` if completion still remains false

## Guardrails

- Prefer the variables explicitly stated in the task over hidden assumptions.
- When the task has an internal inconsistency, choose the most defensible interpretation and record it clearly.
- Treat `TV` and `PV` vapor-fraction writes as follow-up candidates when the validated completion probes already closed without them.
- If the task truly depends on an explicit phase fraction, or Aspen completion/readback keeps pointing there, promote `set_vfrac_mixed` immediately.

## Anti-patterns

- Forcing all streams into a single familiar state mode.
- Ignoring a direct saturation or vapor-fraction statement.
- Writing component flow before component IDs have landed successfully in the current task session.

## Canonical component IDs after CAS landing

Component names in task prose are not stream-table keys. Resolve by CAS, choose the intended Aspen `component_id`, add by CAS, verify the live component table, and then use that same canonical ID in every `component_flows` / `set_flow_mixed` key. Do not switch back to the prose name after landing.

For common normal paraffins, use the established canonical IDs when the task names these compounds: propane `C3` (CAS 74-98-6), n-butane `NC4` (CAS 106-97-8), n-pentane `NC5` (CAS 109-66-0), and n-hexane `NC6` (CAS 110-54-3). In particular, after adding n-pentane as `NC5`, write stream composition with `component_name=&quot;NC5&quot;`, not `N-PENTANE`. If the live table does not contain the intended ID, stop before composition writes and repair component landing; do not rely on runtime alias guessing.

```

### FILE: aspen_agent_skills/guides/functional-role-semantics-validation/SKILL.md
Reason: selected skill for task block family
```text
---
name: functional-role-semantics-validation
description: &gt;-
  Validates process-functional roles before or during Aspen repair work. Covers
  hot/cold sides, feed/product intent, absorber/stripper direction, extract/raffinate
  meaning, and similar role semantics that topology or completion alone cannot prove.
  Use when a block or flowsheet can be wired and even run but still behaves against
  the intended process role, or when REP / PER_ERROR mentions energy-direction,
  wrong side, wrong product role, or other semantic conflicts.
---

# Functional Role Semantics Validation

## When this skill applies

Use this skill when Aspen work has moved beyond &quot;does the node exist&quot; and into
&quot;does this object play the intended process role&quot;.

Typical triggers:

- a block is connected and mostly complete, but behavior still looks wrong
- REP / `PER_ERROR` mentions wrong hot/cold sides, losing heat, wrong phase/product role, or similar semantic conflicts
- the task wording is functional (`absorber`, `stripper`, `extract`, `recycle recovery`, `cold side`, `distillate`, `bottoms`) and the agent risks treating it as generic wiring only
- repeated numeric tweaking is not resolving a warning that sounds like a role mismatch

## Core rule

Do **not** assume any of the following proves the process semantics are correct:

- ports are connected
- tree nodes exist
- object-level completion is green
- `Required Input Complete` appears
- the model runs once

Those only prove a **surface configuration** exists. They do **not** prove the object is fulfilling the intended process function.

## Vapor/liquid phase-product contract

Stream IDs and local VAPOR/LIQUID constants are arbitrary, not role evidence. Bind quantities to `block -&gt; native port -&gt; connected stream -&gt; same-run phase/vapor_fraction`; reconcile native BKP topology/stored phase results with trusted REP outlet declarations. Flash2 uses `F(IN)`, `V(OUT)` and `L(OUT)`; verify actual landing, never ordered outlet assignment. Discover Flash3/REquil family-native ports instead of inventing tokens. Names-only mismatches require consistent answer/target/formula remapping; task-bound or downstream physical mismatches require reconnection and rerun. Renaming is not physical repair. Missing/conflicting phase evidence remains unresolved. See `vapor-liquid-outlet-role-validation` for the dedicated readback contract.

## Three-layer validation model

For any role-sensitive block or flowsheet section, validate in this order:

1. **Topology**: the intended objects are present and connected on the correct faces / ports.
2. **Ownership**: each inlet, outlet, product, stage, or branch is assigned to the intended counterpart.
3. **Role semantics**: the connected objects actually behave like the intended service or product role.

If layer 3 is in doubt, do not spend many rounds on numeric tuning first.

## Generic role-consistency pass

Run this pass before the first serious simulation and again whenever semantic warnings appear:

1. Read the task / PFD in functional terms, not just node names:
   - which stream is the hot side or cold side?
   - which stream is the extract, raffinate, distillate, bottoms, recycle, purge, absorbent, or stripped gas?
2. Check that the live topology matches that intended role.
3. Check that ownership setters (`set_out`, product mapping, feed stage, split target, stage/product assignment, etc.) reinforce the same role instead of contradicting it.
4. Check that specs are attached to the branch / product / stage that owns the intended role.
5. Sanity-check the expected direction:
   - cold side should not be configured to give up heat
   - absorber-like service should not be wired/spec&#x27;d like a stripper
   - extract/raffinate products should not be swapped just because both outlets exist
   - top/bottom products should still match the intended column service
   - if product composition readbacks show the target component is enriched in
     the opposite outlet from the declared product label, treat the label as a
     hypothesis failure and remap roles from readbacks before tuning numbers
   - unless the task explicitly binds a product target to a named stream,
     outlet, or port, agent-created stream labels such as `P2 = HEP product`
     are not reliable validation evidence; judge product purity by readback-
     derived unordered/permutation role assignment across plausible outlets
   - when solvent or inert components affect raw fractions, report both raw
     and task-appropriate normalized bases (for example hydrocarbon-normalized)
     before deciding whether a product purity target is met

## What to do when a semantic warning appears

Treat it as evidence of a **functional mismatch**, not as a prompt to blindly tune numbers.

Preferred recovery order:

1. Re-check the intended role assignment from the task.
2. Re-check live topology and port family.
3. Re-check ownership mapping (`set_out`, product target, stage assignment, outlet identity).
4. Re-check where specs are attached.
5. Only then adjust numeric values.

## Common semantic-warning families

These warnings often belong to the same class:

- `COLD SIDE STREAM ... IS LOSING HEAT.`
- `WRONG SPEC OF HOT &amp; COLD SIDES`
- top/bottom product or phase-role inconsistencies
- absorber / stripper configuration contradictions
- extraction products behaving opposite to the task wording
- repeated probe rows where the &quot;target product&quot; stream is consistently lean in
  the target component while another product stream is rich

The exact text is less important than the pattern: **the model can execute, but the configured role contradicts the intended process function**.

## Cross-family examples

- **MHeatX / HEATX**: hot/cold faces, branch ownership, heat-direction consistency
- **Paired Heater heat transfer**: separate hot-side and cold-side Heater blocks connected by one heat stream must prove both sides of the duty, not just one outlet state
- **RadFrac / absorber-like columns**: condenser/reboiler mode, top/bottom service, product-phase role
- **Extractors / separators**: which outlet is the actual target product versus the reject / secondary stream
- **Recycle or purge sections**: which stream is meant to return versus leave the system

### Paired Heater duty-balance consistency

For tasks that ask for &quot;two Heater blocks with a heat stream transferring heat between the blocks&quot;, treat the heat stream as the shared contract between the blocks:

- Model the hot process stream and cold process stream through separate Heater blocks.
- Connect a heat stream from the hot-side Heater energy outlet to the cold-side Heater energy inlet.
- Specify the hot-side outlet target that determines released heat; do not independently specify the cold-side outlet temperature when the task asks Aspen to calculate the cold outlet state from transferred heat.
- Validate both sides after the run. Read or derive signed hot-side and cold-side duties from block duty, heat-stream duty, or stream enthalpy deltas. A successful run is not enough unless both duties are present and approximately equal/opposite within engineering tolerance.
- If one side is `null`, missing, or not opposite in sign, repair the heat-stream connection or readback path before declaring the task complete.

### RadFrac condenser/product-role consistency

For RadFrac, treat condenser mode and top-product phase as one semantic bundle:

- A `TOTAL` condenser implies the distillate product is liquid-phase distillate semantics. Do not assign a vapor or total-vapor distillate role to the top product while `Condenser=TOTAL`.
- A vapor overhead/top product implies a partial/no-condenser style configuration whose outlet role and product phase match the vapor product. Do not keep `TOTAL` condenser just because the setter succeeds.
- If Aspen says a distillate stream phase is not allowed for the current condenser mode, repair condenser mode, top-product outlet ownership, or product phase before changing numeric column specs.
- Do not advance to sensitivity, optimization, or recycle tuning while a RadFrac product-role warning remains unresolved.

## How this skill should influence agent behavior

- Prefer one deliberate role-consistency pass over many blind run-fix loops.
- If a warning sounds semantic, widen the search from &quot;what variable is missing&quot; to &quot;what function is this object meant to serve&quot;.
- Use family-specific skills afterward for the concrete fix; this skill is the generic decision layer that tells the agent **where to look first**.

```

### FILE: aspen_agent_skills/guides/aspen-generic-readbacks/SKILL.md
Reason: selected skill for task block family
```text
---
name: aspen-generic-readbacks
description: LLM REP readback for unit sets, block duty, HeatX, RadFrac profiles, DSTWU, stream flows, and derived conversion after PER_ERROR=0 and trusted engine_run/REP evidence.
---

# Aspen Generic Readbacks (LLM REP)

Use **after** a trusted run (`PER_ERROR=0`, current-run REP). Own-agent raw final values come from **`rep_readback_targets` + LLM full-REP extraction**. Derived metrics that combine multiple raw values must be computed deterministically in script logic; see `rep-derived-metric-consistency`.

Helpers live in `script_agent_exp.safe_aspen_calls`:

- `finalize_task_summary_with_llm_rep_readback` (**preferred** — merge `final_bundle` then collect once)
- `collect_llm_rep_readback_evidence` (low-level; do not call before finalize)

Required finalize call shape:

```python
summary = safe.finalize_task_summary_with_llm_rep_readback(
    summary,
    final_bundle=final,
    rep_readback_targets=targets,
    llm_rep_readback_artifact_dir=out / &quot;artifacts&quot;,
)
```

`final_bundle` is mandatory and must come from the trusted engine/export step.
Do not pass `summary_path=`; do not call this helper before final evidence
exists.

## Validator contract

- **Final raw scored** metrics: call **`finalize_task_summary_with_llm_rep_readback(...)` once** after the trusted run bundle is merged.
- Validator LLM gate reads `rep_readback_evidence` Markdown; empty `summary.readbacks` is OK when md covers targets.
- Do **not** replace raw LLM REP extraction with stale COM/tree reads. Do compute recovery, conversion, weighted averages, objective sums, and material balances deterministically from raw values and units.
- Do **not** add a second direct COM/tree readback path for final stream/block/derived metrics after REP evidence exists. If `read_stream_output` or `typed readback helper such as read_stream_output(...)` fails, the failure payload is diagnostic only; never recursively extract numbers from errors, paths, stream names, or `available_numeric_candidates` and use them in final gates.
- For derived quantities such as feed thermal condition `q=(H_Vsat-H_F)/(H_Vsat-H_Lsat)`, declare the raw REP targets (`H_F`, `H_Lsat`, `H_Vsat`) and compute the derived value from those REP-read values. Do not compute the derived value from direct readback attempts when REP Markdown contains the needed raw values.
- For HeatX geometry/film-coefficient methods, overall U/area/duty plus geometry/fouling evidence can prove the method. Declare tube/shell side-film coefficient targets only when the task explicitly requires those numeric side coefficients; if REP does not print them, record the boundary instead of proxying them with overall U.

## Target schema

Each target is a dict:

- `request_id` — stable key (also used in `results`)
- `kind` — `stream` | `block` | `derived` | `profile`
- `object_name` — stream or block ID
- `quantity` — semantic name (see table below)
- Optional: `component`, `inlet_stream`, `outlet_stream`, `reactant_component`, `profile_phase`, `stage`, `basis_hint`, `notes`

Store the list on `summary[&quot;rep_readback_targets&quot;]` before collection.

## Quantity map (REP-readable)

| kind | quantity examples | notes |
|------|-------------------|-------|
| stream | `temperature`, `pressure`, `vapor_fraction`, `total_flow`, `component_flow` | component for flows/fractions |
| block | `heatx_area`, `heatx_duty`, `block_heat_duty`, `dstwu_theoretical_stages`, `dstwu_minimum_reflux`, `reflux_ratio`, `distillate_flow`, `reflux_flow`, `condenser_condensation` | block U-O-S / rating tables |
| profile | `profile_composition`, `radfrac_flow_profile`, `internal_liquid_vapor_ratio` | RadFrac MOLE-Y / MOLE-X and liquid/vapor flow profiles |
| derived | `conversion`, `reflux_plus_distillate`, `dstwu_reboiler_vaporization`, `internal_liquid_vapor_ratio`, DSTWU top-down feed plate | script records formula and raw REP inputs. DSTWU `NUMBER OF ACTUAL STAGES ABOVE FEED` is the rectifying-stage count. With the condenser as stage 1, the top-down feed plate is `1 + that number`. Do not subtract it from total stages and call the remainder the top-down plate. |

## DSTWU reboiler vaporization

DSTWU REP prints `REBOILER HEAT DUTY` and `ACTUAL REFLUX RATIO`. It does not print a line named boilup or [NON-ENGLISH REDACTED]. When the task asks for reboiler vaporization, boilup amount, or [NON-ENGLISH REDACTED]:

1. Read the distillate stream molar `TOTAL FLOW` and `ACTUAL REFLUX RATIO` from the same REP.
2. For a total condenser (`DISTILLATE VAPOR FRACTION` is 0), the constant-molal-overflow vaporization is `distillate_molar_flow * (1 + actual_reflux_ratio)`.
3. Store that as derived quantity `dstwu_reboiler_vaporization`, with the formula and the two raw request ids. Report the molar flow. Do not substitute reboiler duty for the vaporization amount.

## Example: HeatX + streams

```python
targets = [
    {&quot;request_id&quot;: &quot;hx_area&quot;, &quot;kind&quot;: &quot;block&quot;, &quot;object_name&quot;: &quot;HX&quot;, &quot;quantity&quot;: &quot;heatx_area&quot;},
    {&quot;request_id&quot;: &quot;hx_duty&quot;, &quot;kind&quot;: &quot;block&quot;, &quot;object_name&quot;: &quot;HX&quot;, &quot;quantity&quot;: &quot;heatx_duty&quot;},
    {&quot;request_id&quot;: &quot;h2_out_temp&quot;, &quot;kind&quot;: &quot;stream&quot;, &quot;object_name&quot;: &quot;H2&quot;, &quot;quantity&quot;: &quot;temperature&quot;},
]
safe.finalize_task_summary_with_llm_rep_readback(
    summary,
    final_bundle=final,
    rep_readback_targets=targets,
    llm_rep_readback_artifact_dir=out / &quot;artifacts&quot;,
)
```

## Example: conversion

```python
{
    &quot;request_id&quot;: &quot;r1_bz_conv&quot;,
    &quot;kind&quot;: &quot;derived&quot;,
    &quot;object_name&quot;: &quot;R1&quot;,
    &quot;quantity&quot;: &quot;conversion&quot;,
    &quot;reactant_component&quot;: &quot;BZ&quot;,
    &quot;inlet_stream&quot;: &quot;F2&quot;,
    &quot;outlet_stream&quot;: &quot;P1&quot;,
}
```

## Unit sets (setup only)

Custom unit sets use COM helpers during **setup** (`configure_custom_unit_set`, `read_active_unit_set`, `verify_custom_unit_set`). **INSET routing, METCBAR template default, bar-scale `set_pres`, and INSET-switch hazards** are in **`aspen-custom-unit-set`** (default-injected).

Common setup mistakes: `configure_inset_unit_system(&quot;METCBAR&quot;)` (use `activate_custom_unit_set`); task **bar** written as **MPa** (use `unit=&quot;bar&quot;` — legal under any INSET). Re-read critical `PRES` after any INSET change.

Final displayed stream/block numbers for scoring use LLM REP readback after the trusted run. Derived metrics use those raw readbacks as inputs and must store the formula and source `request_id`s.

## RadFrac Operating Metrics

For final RadFrac/distillation scoring metrics, use LLM REP readback after the
selected replay run. Do not rely on stale probe-row direct reads or parse COM
diagnostics as final answers.

Recommended targets:

```python
targets = [
    {&quot;request_id&quot;: &quot;c1_reflux_ratio&quot;, &quot;kind&quot;: &quot;block&quot;, &quot;object_name&quot;: &quot;C1&quot;, &quot;quantity&quot;: &quot;reflux_ratio&quot;},
    {&quot;request_id&quot;: &quot;c1_reflux_flow&quot;, &quot;kind&quot;: &quot;block&quot;, &quot;object_name&quot;: &quot;C1&quot;, &quot;quantity&quot;: &quot;reflux_flow&quot;},
    {&quot;request_id&quot;: &quot;c1_distillate_flow&quot;, &quot;kind&quot;: &quot;block&quot;, &quot;object_name&quot;: &quot;C1&quot;, &quot;quantity&quot;: &quot;distillate_flow&quot;},
    {
        &quot;request_id&quot;: &quot;c1_internal_lv_basis&quot;,
        &quot;kind&quot;: &quot;profile&quot;,
        &quot;object_name&quot;: &quot;C1&quot;,
        &quot;quantity&quot;: &quot;internal_liquid_vapor_ratio&quot;,
        &quot;basis_hint&quot;: &quot;Use an internal stage/profile basis away from a total-condenser stage where vapor flow is zero.&quot;,
    },
    {
        &quot;request_id&quot;: &quot;c1_condenser_condensed_vapor&quot;,
        &quot;kind&quot;: &quot;derived&quot;,
        &quot;object_name&quot;: &quot;C1&quot;,
        &quot;quantity&quot;: &quot;reflux_plus_distillate&quot;,
        &quot;basis_hint&quot;: &quot;For a total condenser, total vapor condensed is reflux plus distillate/top liquid product on a common molar-flow unit basis.&quot;,
    },
]
```

For total condensers, the condenser/top stage may print zero vapor flow; do not
compute internal L/V as stage-1 liquid divided by zero vapor. Use a meaningful
internal stage/profile row or report a clearly labeled normalized basis if the
task only asks for an operating ratio. For condenser condensation, do not report
distillate alone when the requested value is total vapor condensed; compute
`reflux + distillate` from LLM REP raw readbacks with explicit units.

## Probe / scaffold exception

`run_standard_probe_matrix` and per-row probe readbacks keep **`read_stream_output`** (many rows — not LLM REP). See `probe-sweep-decision-readback`. After selecting a final replay case, use LLM REP once for task scoring metrics.

## Boundaries

- Only quantities **printed in the `.rep`** for the converged run are supported as raw LLM readbacks.
- Not a substitute for Aspen tree paths absent from REP.
- Analysis-object tables (native SA/OPT) still use their dedicated collection helpers; stream/block **physical** results use LLM REP targets.
- Multi-stream or weighted derived metrics are outside the LLM readback boundary. Compute them in code from the extracted raw values and preserve units/common basis.

```

### FILE: aspen_agent_skills/guides/reactor-reaction-setup-high-level/SKILL.md
Reason: selected skill for task block family
```text
---
name: reactor-reaction-setup-high-level
description: &gt;-
  Guides Aspen reactor reaction setup through high-level helpers. Use when a
  task configures RYield, RStoic, REquil, RPlug, RCSTR, component yield tables, reaction stoichiometry,
  conversion rows, equilibrium reactions, or reactor reaction sets.
---

# Reactor Reaction Setup

Use high-level reaction helpers whenever they exist. Do not write generated
examples around low-level row setters, raw table cells, or direct Aspen tree
paths unless no high-level helper exists for that reaction family.

## Complete RYield MASS Bundle

Use `derive_ryield_mass_yield_bundle(...)` for pure offline preflight and
`configure_ryield_mass_yield_bundle(...)` for the authorized native write.
Pass explicit annotated `feed_flows`, exactly one complete `product_flows` or
`mass_yields` map, and the full verified native `component_ids` inventory.
Include zero products and all excess unreacted components. Declare inerts
separately: unchanged inert mass is excluded from the non-inert denominator
and from native yield rows; it is never silently treated as a product yield.
For percentage input use the exact `percent` token; the bundle divides once
and records the original percentage. It never renormalizes incomplete mass.

Molar flows require `molecular_weights` records with `quantity`, matching
`component_id`, `cas`, `identity_verified=True`, `identity_source`, `source`,
and `source_kind=&#x27;external_given&#x27;` or `&#x27;native_component_property&#x27;`.
`verify_ryield_molecular_weights(...)` accepts explicit external reference MW
only after native identity is independently verified. Native property records
also need matching annotated `native_readback`. Use registered MW units
(`kg/kmol`, `g/mol`, `kg/mol`), not handwritten component constants. This
validates provenance and unit conversion, not an external source&#x27;s accuracy.
An independent non-reacting property-only native run may supply
`source_kind=&#x27;native_nonreactive_flow_ratio&#x27;` with annotated `mass_flow`,
`mole_flow`, and `nonreactive_evidence` containing `nonreactive=True`, raw-zero
status, owned task hash, native run ID and current REP SHA256. Convert both
flows through UNIT_REGISTRY and retain identity/source readbacks. This is
component MW diagnosis, never a combustion task target or final product.
A failed-run reacting product mass/amount ratio is not accepted as MW source
or final product evidence. Do not copy solved reference-file output values.

The writer reuses `configure_ryield_component_yield(...)`, retains existing
aliases, checks both setter `after` values, then dumps/verifies `BASIS`,
`MOLE_YIELD`, and their visible Input-root surfaces. Unexpected rows, missing
rows, hash-only labels, and mismatched basis/value cells fail closed. Inerts
currently require a preconfigured native `INERT` table with verified `YES`
rows; unavailable or differently shaped inert surfaces are a capability gap,
not permission to guess a setter. The offline derivation itself supports
explicit inert mass balance independently of that live surface.

The plan/table probe is **not final run evidence**. Preserve raw generated
scripts; an authorized narrow repair is a separate provenance transaction.
The parent must separately complete topology/Next, current-run REP/BKP and
unit-safe product/balance checks. The zero-LLM probe script
`runtime/script_agent_experiment/scripts/probe_ryield_mass_bundle.py` defaults
to offline derivation. `--live` requires an existing parent-owned session and
completed external identity/MW verification; it performs no engine run/save.

## Preferred Helpers

- For RStoic stoichiometry, use `configure_rstoic_stoichiometry(...)`.
- For RStoic conversion rows, use `configure_rstoic_fractional_conversions(...)`.
- For RStoic calculated heat of reaction, use
  `configure_rstoic_calculated_heat_reference(...)`. It configures the complete
  Heat of Reaction reference-condition bundle for all requested reaction rows.
- For REquil equilibrium reactions, use `configure_requil_equilibrium_reactions(...)`.
- For kinetic reactor families such as RPlug or RCSTR, use
  `configure_reversible_powerlaw_pair(...)` and
  `bind_reactor_powerlaw_reactions(...)` for liquid PowerLaw kinetics. Do not
  call raw `create_powerlaw_reaction` without `reaction_name`.
- For RPlug/RCSTR, also follow `rplug-rcstr-native-reaction-setup`: the native
  reaction set, kinetic parameters, reaction-set assignment, and reactor sizing
  are all required evidence. If no high-level kinetic helper exists for the
  requested family, keep the missing native setup visible instead of silently
  falling back to RStoic.

## RStoic Pattern

Count physical vessels, not reaction equations. Several reactions in one named reactor or one figure icon are several `reaction_number` rows on one block. A second block is a second vessel. Do not add a heat stream unless the figure or the task shows one.

```python
from script_agent_exp import safe_aspen_calls as safe

rstoic_stoich = client.invoke(&quot;configure_rstoic_stoichiometry&quot;,
    block_name=&quot;R1&quot;,
    reaction_number=1,
    reactants={&quot;TOLUENE&quot;: 1.0, &quot;H2&quot;: 1.0},
    products={&quot;BENZENE&quot;: 1.0, &quot;METHANE&quot;: 1.0},
)
rstoic_conversion = client.invoke(&quot;configure_rstoic_fractional_conversions&quot;,
    block_name=&quot;R1&quot;,
    conversions=[
        {&quot;reaction_number&quot;: 1, &quot;component_id&quot;: &quot;TOLUENE&quot;, &quot;conversion&quot;: 0.75},
    ],
)
summary.setdefault(&quot;results&quot;, {})[&quot;rstoic_reaction_setup&quot;] = {
    &quot;stoichiometry&quot;: rstoic_stoich,
    &quot;conversion&quot;: rstoic_conversion,
}
```

Pass positive magnitudes in `reactants` and `products`; the helper handles Aspen&#x27;s
signed coefficient convention. Preserve the helper return payload in
`summary.json` so validators/scorers can inspect conversion rows and readbacks.

## RStoic Calculated Heat Bundle

Treat calculated heat of reaction as a bundled mode, not a single flag. When the
task needs reactor heat duty or Aspen explicitly lands on the Heat of Reaction
reference-condition page, call `configure_rstoic_calculated_heat_reference(...)`
after stoichiometry and conversion rows are in place. Use the same reactant as
the conversion key unless the task gives a different heat-reference component.

The Aspen Next message `Reference Component must be specified for all reactions
defined (Setup | Reactions sheet)` maps to an incomplete calculated-heat
reference-condition bundle, not to the conversion key component. Do not repair
that message by rewriting conversion rows or by guessing low-level row setters.

If the task does not require heat duty or calculated heat of reaction, prefer
leaving calculated heat disabled instead of creating the extra required input
bundle. After enabling the calculated heat bundle, run `ui_next_completion(...)`
or another trusted completion gate before `engine_run`; do not trust a global
flowsheet-complete override if the RStoic block itself still reports
`input_incomplete`.

Example for calculated heat with two reaction rows:

```python
rstoic_heat_ref = client.invoke(&quot;configure_rstoic_calculated_heat_reference&quot;,
    block_name=&quot;R1&quot;,
    rows=[
        {
            &quot;reaction_number&quot;: 1,
            &quot;reference_component_id&quot;: &quot;TOLUENE&quot;,
            &quot;reference_phase&quot;: &quot;V&quot;,
        },
        {
            &quot;reaction_number&quot;: 2,
            &quot;reference_component_id&quot;: &quot;BENZENE&quot;,
            &quot;reference_phase&quot;: &quot;V&quot;,
        },
    ],
    reference_temperature=298.15,
    reference_temperature_unit=&quot;K&quot;,
    reference_pressure=1.0,
    reference_pressure_unit=&quot;atm&quot;,
)
summary.setdefault(&quot;results&quot;, {})[&quot;rstoic_reaction_setup&quot;][&quot;heat_reference&quot;] = rstoic_heat_ref
```

For any reaction-mode switch that creates follow-through rows or table cells
(conversion component, stoichiometric coefficients, heat reference component,
rate basis, or phase basis), treat the write as complete only after the visible
table-facing path can read back both the component identity and the numeric/mode
cell. Hash-only component leaves or a successful wrapper response are not enough
when Next/completion still names the reaction sheet.

## REquil Pattern

```python
from script_agent_exp import safe_aspen_calls as safe

requil_reactions = client.invoke(&quot;configure_requil_equilibrium_reactions&quot;,
    block_name=&quot;R1&quot;,
    nphase=2,
    spec_opt=&quot;TP&quot;,
    temperature=450.0,
    temperature_unit=&quot;F&quot;,
    pressure=1.0,
    pressure_unit=&quot;atm&quot;,
    reactions=[
        {
            &quot;reaction_number&quot;: 1,
            &quot;reactants&quot;: {&quot;MEOH&quot;: 1.0},
            &quot;products&quot;: {&quot;CO&quot;: 1.0, &quot;H2&quot;: 2.0},
            &quot;delta&quot;: 0.0,
        },
        {
            &quot;reaction_number&quot;: 2,
            &quot;reactants&quot;: {&quot;CO&quot;: 1.0, &quot;H2O&quot;: 1.0},
            &quot;products&quot;: {&quot;CO2&quot;: 1.0, &quot;H2&quot;: 1.0},
            &quot;delta&quot;: 0.0,
        },
    ],
)
summary.setdefault(&quot;results&quot;, {})[&quot;requil_reaction_setup&quot;] = requil_reactions
```

After REquil reaction setup, keep the existing REquil skill&#x27;s round-trip and
product-readback gates: completion must be trusted after BKP/reload evidence, and
product values must come from Aspen outlet/REP readbacks.

## RYield Complete Component-Yield Configuration Bundle

A `RYield` block needs an actual numeric component-yield table, not just operating
conditions. Configure and verify the following dependency bundle before running
or declaring input completeness. Iteration scheduling belongs to the runtime:
verified components and topology -&gt; legal flash selector and its complete input
pair -&gt; `set_user_yield=NO` -&gt; one high-level yield helper call for every intended
non-inert product component -&gt; per-row readback -&gt; block completion and Next.
`NO` selects built-in Component yields; `YES/NO2/NO3` selects a user-subroutine
route and is not an &quot;enable yield table&quot; flag.

Use `client.invoke(&quot;configure_ryield_component_yield&quot;, block_name=..., component_id=...,
substream=&#x27;MIXED&#x27;, basis=&#x27;MASS&#x27;, mass_yield=..., mass_yield_unit=&#x27;1&#x27;)` for an
explicit mass ratio. Explicit task mass percentages are divided by 100 exactly
once. MASS yield is product mass/non-inert feed mass, not outlet mole fraction.
For MOLE supply `mole_yield`, `mole_yield_unit`, verified
`aspen_mole_yield_unit`, and `native_yield_unit_source`: its native basis is
product amount/non-inert feed mass, not product amount/total product amount.
Do not pass `kmol/hr` or `kg/hr` to either yield branch or normalize an outlet
molar ratio directly into native yield cells.

The helper owns materialization of the visible component row in **both**
`Data\Blocks\&lt;block&gt;\Input\BASIS` and
`Data\Blocks\&lt;block&gt;\Input\MOLE_YIELD`. The latter is the native table name
also when the row basis is MASS; do not invent a `MASS_YIELD` tree leaf.
Do not replace the helper with `COMP_LIST` labels, guessed `#component` leaves,
or `set_yield` (that sets the user subroutine name).

For each intended row require helper `success=True`, then verify
`basis_result.after` matches the requested basis and
`mole_yield_result.after` matches the helper&#x27;s reconciled `yield_value_written`, with
matching component/substream and actual row/value-cell evidence. Preserve these
payloads. Also use `table_dump` on the BASIS and MOLE_YIELD roots to verify
logical component/substream rows and numeric cells; do not guess component leaf
paths. For persisted delivery, verify both tables after BKP cold reload without
rewriting them. The wrapper can echo an intended value without proving the visible
cell changed. An empty GUI Component yields table is input-incomplete even if
TP writes succeeded. `get_yield_label` may remain null under `USER_YIELD=NO`;
that is not a reason to skip numeric yield rows. `COMP_LIST` emptiness alone
cannot negate concrete visible row evidence.

Write and check the complete distribution, with inert/excess-feed accounting
explicit. A yield-normalization warning is a repair requirement, not acceptable
closure. Required row failures must stop the configuration stage with detailed
payloads rather than being swallowed; final results still require trusted REP.

## Anti-Patterns

- Do not expose low-level row setters as the default recipe when a high-level
  helper already covers the reaction setup.
- Do not use RStoic stoichiometry/conversion helpers to satisfy RPlug or RCSTR
  tasks unless the task explicitly asks for an RStoic surrogate.
- Do not record stoichiometry only in notes; the reaction rows must be configured
  in the native Aspen object.
- Do not treat `PER_ERROR=0` after an input-incomplete RStoic run as success if
  no current `.his` or REP is produced; repair the missing RStoic input first.
- Do not treat a successful reaction helper call as final result evidence; run
  completion and collect product/readback evidence after the full flowsheet run.

## Exact generated capability signatures

Use these literal keyword shapes; the helper owns all lower-level family-specific setters:

- `configure_rstoic_fractional_conversions`: `block_name`, `conversions` where each row has `reaction_number`, `component_id`, and `conversion` (or `value`).
- `configure_requil_equilibrium_reactions`: `block_name`, nonempty `reactions`, optional `nphase`, `spec_opt`, `temperature`/`temperature_unit`, `pressure`/`pressure_unit`, `duty`/`duty_unit`, `default_delta`, `delta_unit`. Invalid reaction schema fails before any Aspen write.
- `configure_ryield_component_yield`: `block_name`, `component_id`, `basis`; MASS uses `mass_yield` + dimensionless `mass_yield_unit`; MOLE uses `mole_yield`, `mole_yield_unit`, verified `aspen_mole_yield_unit`, and `native_yield_unit_source`.

Do not call the underlying `set_key_cid`, `set_conv`, `set_delt`, `set_basis`, or `set_mole_yield` from generated source.

```

### FILE: aspen_agent_skills/guides/sequential-reaction-topology/SKILL.md
Reason: selected skill for task block family
```text
---
name: sequential-reaction-topology
description: &gt;-
  Counts Aspen reactor blocks from physical vessels in the task and figure, not
  from the number of reaction equations. Use when a task has a main reaction and
  a side reaction, series reactions inside one reactor, or more than one reactor
  vessel.
---

# Sequential Reaction Topology

## Core Rule

Count physical vessels, not reaction equations.

A vessel is a reactor the task names or the figure draws: &quot;the reactor&quot;, &quot;the first reactor&quot;, &quot;the second reactor&quot;, or one reactor icon. Every equation the task places in that vessel is a `reaction_number` row on that one block. RStoic applies those rows in order. &quot;The side reaction consumes a product of the main reaction&quot; and &quot;after the first reaction&quot;, when both belong to the same vessel, are the next row on that block. They are not a new block.

Create another reactor block only when the task or the figure shows another vessel. That is a second named reactor, a stream that leaves one reactor and enters the next, or a temperature and pressure the task assigns to a different reactor. Do not create one block per equation.

Do not add a heat stream because a reactor has a duty, a heat of reaction, or a quench temperature. Add a heat stream only when the figure shows a heat line or the task names a heat stream. A quench the task describes as a material stream stays a material stream.

## RStoic Pattern

Same vessel:

1. Create one RStoic for that vessel.
2. Write each reaction with `configure_rstoic_stoichiometry(..., reaction_number=N)` and the matching conversion row on that same block.
3. Set that block&#x27;s temperature and pressure once.

Separate vessels:

1. Create one RStoic per vessel the task or figure shows.
2. Connect those blocks with the intermediate material stream the task shows.
3. Put on each block only the reactions that belong to that vessel.
4. Prefer `configure_rstoic_stoichiometry(...)` plus `configure_rstoic_fractional_conversions(...)` and preserve their return payloads in `summary.json`. Do not expand the default recipe into low-level row setters or raw `KEY_COMP` paths.
5. Preserve downstream thermal, flash, splitter, and pump topology. Do not replace those blocks with heater surrogates unless the task explicitly allows an approximation.

## Design Spec Interaction

When a downstream Design Spec controls quench, recycle, or another scalar flow:

- The manipulated stream is the material stream the task names.
- Expose that stream as `MOLE-FRAC` composition plus one total-flow scalar.
- Use the helper-returned accepted stream-total manipulated token, not a guessed alternate token.
- Validate that the Design Spec result, manipulated variable readback, and final stream target come from Aspen after the final engine run.

## Failure Signal

If `engine_run.success=true` but REP export, `PER_ERROR`, or target readbacks are missing, inspect topology before treating it as a finalization-only problem. An extra RStoic created only to hold an extra reaction row, or a heat stream the figure does not show, is a topology defect.

```

### FILE: aspen_agent_skills/guides/native-reactor-module-comparison/SKILL.md
Reason: selected skill for task block family
```text
---
name: native-reactor-module-comparison
description: &gt;-
  Guides own-agent scripts for tasks that compare Aspen native reactor modules
  such as REquil, RGibbs, RStoic, RPlug, and RCSTR without substituting runnable
  stoichiometric surrogates.
---

# Native Reactor Module Comparison

Use this skill when a task asks to compare multiple Aspen reactor modules or
gives module-specific geometry, volume, conversion, or kinetic data.

## Model Fidelity

- Use the native reactor family requested by the task for each comparison
  branch: for example `REQUIL`, `RGIBBS`, `RSTOIC`, `RPLUG`, and `RCSTR`.
- Do not represent `RPLUG` or `RCSTR` with a runnable `RSTOIC` branch while only
  recording geometry or kinetic intent in notes.
- Keep evidence for each branch separate enough that REP/APW/BKP or summary
  readbacks prove the native family used.
- If the task figure places comparison branches together, preserve them in one
  live simulation and one integrated BKP, including every reactor family shown
  in the figure even when prose supplies parameters for only some families.
  Do not split sibling branches into independent simulations and claim the
  original figure topology is complete. A task-visible feed duplicator gives
  each comparison branch the full same feed basis; an ordinary splitter that
  divides the feed amount is not equivalent. Validate all branch ports,
  reactor-specific specifications, and outputs from the same final run.

## Parent Figure And Scope Ownership

- Extract the authoritative parent figure as explicit nodes, directed stream edges, native families, and role ownership before assembling comparison context. Cover the original feed-to-copy node edge, each independent copied-feed-to-reactor edge, and every product edge; listing native family names alone is insufficient.
- Bind cached facts to their source subtask and current task hash. A sibling exclusion or deferred comparison in one leaf is not a global parent prohibition. Preserve independently evidenced full-task exclusions; quarantine unknown ownership as a blocking review, including mixed rules that combine leaf-only exclusions with real physical restrictions.
- Repair conflicting grounding, topology, plan steps, gate clauses, and validator routing in their original sections before initialization. A final prompt override cannot clean contradictory active context. Prefer a canonical full-parent planner only when its authoritative task hash is current; invalidate changed-task caches.
- Include every required native family in profile, metadata/validator families, surface documents, and generic skills. Figure labels determine node/edge ownership; text supplies conditions that the figure does not show. Explicit user clarification governs specification ownership without importing historical numerical answers.
- Do not initialize from task-specific rerun skills containing solved product values, tuned dimensions, or reference-answer ranges. Keep generic configuration contracts separate from historical solution/probe evidence.

## Stoichiometry, Phase, And Kinetics

- Preserve the task reaction stoichiometry and reaction phase.
- When the task provides kinetic expressions, bind those reactions to the
  kinetic reactor families instead of replacing them with hidden conversion-only
  equivalents.
- For RGibbs-style equilibrium evidence, prove reaction direction through
  component generation/readback evidence, not only through a setter echo.

## REquil / RGibbs Comparison Pattern

For tasks such as methanol reforming / shift equilibrium comparisons, keep the two
reactor branches separate and make the product-component readback validator-friendly:

```python
from pathlib import Path

from script_agent_exp.script_runtime.rep_parser import load_rep
from script_agent_exp import safe_aspen_calls as safe


def sum_component_kmol_hr_from_rep(rep_path: Path, stream_ids: list[str], component_id: str) -&gt; dict[str, object]:
    rep_text = load_rep(str(rep_path))
    tables = safe.extract_all_stream_tables_from_rep_text(rep_text)
    component = component_id.strip().upper()
    total_kmol_s = 0.0
    contributing: dict[str, float] = {}
    for stream_id in stream_ids:
        row = tables.get(stream_id.strip().upper())
        if not row:
            continue
        value = (row.get(&quot;components_kmol_s&quot;) or {}).get(component)
        if value is None:
            continue
        contributing[stream_id.strip().upper()] = float(value)
        total_kmol_s += float(value)
    return {
        &quot;success&quot;: bool(contributing),
        &quot;component_id&quot;: component,
        &quot;stream_ids&quot;: [stream_id.strip().upper() for stream_id in stream_ids],
        &quot;components_kmol_s&quot;: contributing,
        &quot;total_kmol_s&quot;: total_kmol_s if contributing else None,
        &quot;total_kmol_hr&quot;: total_kmol_s * 3600.0 if contributing else None,
        &quot;source&quot;: &quot;current-run REP stream table component flow&quot;,
    }


requil_h2 = sum_component_kmol_hr_from_rep(rep_path, [&quot;V1&quot;, &quot;L1&quot;], &quot;H2&quot;)
rgibbs_h2 = sum_component_kmol_hr_from_rep(rep_path, [&quot;V2&quot;], &quot;H2&quot;)

summary[&quot;results&quot;][&quot;product_h2_kmol_hr&quot;] = requil_h2[&quot;total_kmol_hr&quot;]
summary[&quot;results&quot;][&quot;product_hydrogen_kmol_hr&quot;] = requil_h2[&quot;total_kmol_hr&quot;]
summary[&quot;results&quot;][&quot;requil_product_h2_readback&quot;] = requil_h2
summary[&quot;results&quot;][&quot;rgibbs_product_h2_readback&quot;] = rgibbs_h2
summary[&quot;results&quot;][&quot;result_source&quot;] = (
    &quot;H2 product flow is summed from current-run Aspen REP outlet stream tables; &quot;
    &quot;REquil uses both material outlets V1 and L1, RGibbs uses V2.&quot;
)
```

Use the exact keys `product_h2_kmol_hr` or `product_hydrogen_kmol_hr` for the primary product-component result. Human-friendly variants such as `hydrogen_product_kmol_hr` or generic `product_component_kmol_hr` are useful supporting evidence, but they may not satisfy generic product-component validation by themselves.

## Module-Specific Inputs

- RStoic conversion values must match the task.
- For RStoic, put conversion evidence in a structured summary key, not only in prose. A good shape is:
  `results.rstoic_conversion_evidence = [{&quot;block_name&quot;: &quot;R1&quot;, &quot;reaction_number&quot;: 1, &quot;key_component&quot;: &quot;TOLUENE&quot;, &quot;conversion_fraction&quot;: 0.75, &quot;source&quot;: &quot;configure_rstoic_fractional_conversions/readback&quot;}]`.
- When using `configure_rstoic_fractional_conversions(...)`, preserve its returned `rows[*].conversion`, `rows[*].component_id`, and `rows[*].readback` in the final summary so validator/scorer can identify the native conversion setting.
- RPlug geometry such as length and diameter must be configured and evidenced.
- RCSTR volume must be configured and evidenced.
- If a property-method warning is accepted as a narrow PER_ERROR exception,
  record raw and effective status; otherwise do not change the task&#x27;s property
  method merely to make the scalar status clean.

```

### FILE: aspen_agent_skills/guides/flash-control-chain/SKILL.md
Reason: selected skill for task block family
```text
---
name: flash-control-chain
description: Handle flash tasks by choosing topology from real phase structure, locking SPEC_OPT first, using compatible mode pairs, and using heat-coupled modes such as TQ when heat duty should participate in vaporization or product composition.
---

# Flash Control Chain

- Choose topology from the real phase structure: `Flash2`, `Flash3`, `Mixer`, and `Dupl` have different jobs.
- **Independent-feed energy boundary:** Preserve each task-specified feed&#x27;s composition, amount, T/P, and phase/state independently. Equal feed temperature and pressure do **not** make a summed-composition `TP` stream thermodynamically equivalent: phase equilibrium and nonideal mixing enthalpy depend on composition. A fresh combined `TP` stream can change total inlet enthalpy and therefore an adiabatic flash result.
- Inspect `list_block_ports` before wiring multiple feeds; a single material inlet can be a shared collection, not a one-stream limit. Use verified collection connections or an upstream adiabatic `Mixer`, preserving all independent inlet states; never invent numbered ports or replace the mixer outlet with a specified total-flow `TP` feed.
- For property-method comparisons, keep feed partition/state identical across branches and verify each branch&#x27;s property scope; if upstream mixers are used, verify their method basis too. Before trusting outputs, record live feed ownership plus current-run inlet phase/enthalpy evidence and energy-balance closure. Convergence and summed component balances alone do not prove feed-state fidelity.
- Set `SPEC_OPT` before writing dependent pressure, temperature, or duty values.
- After changing `SPEC_OPT`, write the full dependent variable set explicitly. Do not assume Aspen or the wrapper will keep an old `TEMP`, `PRES`, or `DUTY` value consistent with the new mode.
- If completion still asks for flash temperature or pressure, verify `SPEC_OPT` readback before changing numeric values. A successful setter call does not prove Aspen actually left the old flash mode.
- When completion or required-input dialogs name an exact flash input node, treat that node as missing until a readback proves otherwise.
- For adiabatic constant-pressure flash, use a pressure-plus-heat pattern and write the full compatible pair explicitly instead of hard-coding the solved-for temperature.
- For object-level completion on a plain `Flash2`, start with the compatible pair for the chosen mode before promoting stream-side setters or fallback variables from another mode.
- One equilibrium flash is one `Flash2`: vapor and liquid in equilibrium at one condition or one vapor fraction. Connect the vapor product with `connect_flash2_vapor_liquid_ports` to `V(OUT)` and the liquid product to `L(OUT)`. Do not use `connect_material_ports_by_order` for Flash2 outlets; port order can attach the stream named vapor to the liquid port.
- Differential simple distillation of a finite charge is a sequence of equilibrium `Flash2` steps, not one flash and not a column. A stated fraction of the charge is vaporized, and both the remaining liquid and the accumulated vapor are required. Each step removes a small vapor cut on a `PV` spec; the liquid outlet feeds the next step; the vapor outlets are mixed into the accumulated vapor product. Use enough equal cuts that the product of the remaining-liquid fractions matches the requested residual fraction. Connect each vapor stream to the vapor outlet port and each liquid stream to the liquid outlet port. An analytical constant-relative-volatility integration may be kept as a reference; it does not replace the flash sequence.
- **Heat-driven flash / evaporation stages:** If a `Flash2` has a material feed plus a connected inlet heat stream, `TP` is an invalid final `SPEC_OPT` route. `TP` pins temperature and pressure and makes the heat stream non-causal; code-side setters must reject it with `flash2_heat_stream_tp_invalid` / `flash2_heat_stream_spec_error` so runtime ruff repair can switch the route.
- **Inlet heat stream SPEC_OPT rule:** For `Flash2` with `HS(IN)`/heat-stream inlet, do not use `TP`. If the task fixes effect temperature while heat duty, steam flow, or an upstream heat cascade should determine the split, use `TQ` and write only `TEMP`. For pressure-controlled routes, use `PQ`, `PV`, or `PD` as appropriate and write only `PRES`.
- With an inlet heat stream, temperature-family routes such as `TQ`, `TV`, and `TD` mean &quot;write `TEMP` only&quot;. Do **not** write `PRES`, `DUTY`, or `VFRAC` after selecting one of these routes; Aspen may accept the setter call but export/read back an inconsistent `SPEC-OPT=TQ` plus residual pressure state.
- With an inlet heat stream, pressure-family routes such as `PQ` and `PV` mean &quot;write `PRES` only&quot;. Do **not** write `TEMP`, `DUTY`, or `VFRAC` after selecting one of these routes; temperature/vapor fraction become responses.
- The same rule applies even if a wrapper says `set_pres(...)` succeeded. For heat-stream-fed `Flash2`, successful dependent setters are not enough; the script must preserve the one-variable route semantics before run/export.
- If a task fixes effect temperatures in an evaporator cascade, use `TQ`, write only `TEMP`, and let pressure/composition be response variables. If the task fixes pressure instead, use a pressure-family route and write only `PRES`.
- If a heat-driven evaporator fails in one fixed-variable route, probe the other block variable, especially a small temperature or pressure bracket, before declaring the heat cascade infeasible.
- **Idle manipulated variable diagnostic:** If changing heat duty, steam flow, or heat-stream inputs does not move product composition while affected Flash2 blocks still read back as `TP`, treat this as a model-fidelity / route mistake first. Re-read `SPEC_OPT` and replan onto a heat-coupled flash route before concluding the task has no solution.
- If material split readbacks look physically right but run status or `PER_ERROR` is still bad, keep the run-status/setup-state problem visible. Do not &quot;repair&quot; by changing the reported split until you have checked completion, `SPEC_OPT`, unit basis, and current REP/export trust.
- Use REP stream evidence to confirm outlet phases, interstage connections, and property-method comparisons.

## Vapor/liquid ownership proof

Stream IDs are arbitrary. After connecting, verify `F(IN)` and actual `V(OUT)`/`L(OUT)` connected streams, then match same-run REP outlet declarations and stream PHASE/vapor_fraction before reporting compositions. A successful helper or inherited BKP stream order is not role proof. Names-only mismatches need consistent answer/target/formula mapping; task-bound or downstream physical mismatches require reconnection and rerun, not renaming. For Flash3/REquil discover family-native phase ports; do not assume Flash2 tokens. See `vapor-liquid-outlet-role-validation`.

## Compatible pairs

- Plain `TP` =&gt; `TEMP` + `PRES` only when no inlet heat-stream limitation is active; with inlet heat stream, `TP` is invalid and must be rejected.
- `PV` =&gt; `PRES` + `VFRAC` only when no inlet heat-stream limitation is active; with inlet heat stream, `PV` is a pressure route and only `PRES` should be written.
- `PD` =&gt; `PRES` + `DUTY`
- `TQ` =&gt; `TEMP` + heat-stream participation; write only `TEMP` on heat-stream-fed `Flash2`.
- `PQ` =&gt; `PRES` + heat-stream participation; write only `PRES` on heat-stream-fed `Flash2`.

## Aspen HTTP setter order for TQ

```python
client.invoke(&quot;set_spec_opt&quot;, block_name=&quot;A1&quot;, value=&quot;TQ&quot;)
client.invoke(&quot;set_temp&quot;, block_name=&quot;A1&quot;, value=50.0, unit=&quot;C&quot;)
# verify readback on SPEC_OPT and TEMP before run/export
```

Connecting a heat stream is topology only; it does not replace block-side `SPEC_OPT=TQ` or prove duty participation.

## Bar-scale pressure on `set_pres` (Flash2 / near-atmospheric flash)

When task text or standard meta gives **bar-scale** flash pressure (e.g. `PRES = -0.05 bar`), write it with an explicit **`unit=&quot;bar&quot;`** on `set_pres`. This is **legal under any INSET** (SI/ENG/MET/METCBAR).

```python
client.invoke(&quot;set_spec_opt&quot;, block_name=&quot;F&quot;, value=&quot;TP&quot;)
client.invoke(&quot;set_temp&quot;, block_name=&quot;F&quot;, value=50.0, unit=&quot;C&quot;)
client.invoke(&quot;set_pres&quot;, block_name=&quot;F&quot;, value=-0.05, unit=&quot;bar&quot;)
```

Rules:

- **`bar` / `bara` / `barg`** are accepted setter units — see block-type inject `flash2.md` / `rstoic.md` and `aspen-custom-unit-set`.
- Do **not** convert bar-scale numbers to **`MPa`** unless the task truly specifies MPa.
- With **absolute** bar units, a **negative** `PRES` means **pressure drop** (Aspen Flash help), not “set MPa outlet pressure”.
- After `set_pres`, verify `SPEC_OPT` + numeric readback; display unit on readback may differ from the write token.
- If the flowsheet also uses **SI-only equipment tables** (pump curves, etc.), prefer **`INSET=SI` + `unit=&quot;bar&quot;`** on flash pressure — do not write bar under METCBAR then switch INSET mid-build (rescales stored `PRES`). See `aspen-custom-unit-set`.

Live probe: `python tool_side_generation/healthcheck/bar_pressure_write_probe.py`


```

### FILE: aspen_agent_skills/guides/prefer-direct-component-splits/SKILL.md
Reason: selected skill for task block family
```text
---
name: prefer-direct-component-splits
description: Prefers direct component-to-product split surfaces for shortcut Aspen separation tasks. Use when the task gives explicit component destinations, when multiple separator families or setter surfaces are possible, or when an indirect route would require component groups, substream lists, or STR_COMPS-style indirection.
---

# Prefer Direct Component Splits

## When To Use
Use this skill when a task already says where named components should go, for example:

- all hydrogen leaves in one outlet
- all benzene and toluene leave as product
- all unreacted reactant returns as recycle

Use it when there are multiple plausible separator families or setter surfaces and the agent must choose the most stable shortcut route.

## Core Rule
When the task gives explicit component destinations, prefer the narrowest stable route that writes component-to-product behavior directly.

Prefer:

- per-component split fractions
- per-component recoveries
- per-component stream assignment on a validated direct surface

Avoid introducing extra abstraction layers unless the task or the verified tool surface truly requires them.

## Preferred Modeling Order
1. Choose a block family that exposes the required true material ports.
2. Prefer a setter surface that writes direct component routing on those ports.
3. Only if direct component routing is unavailable, consider indirect routes such as component groups or substream lists.
4. If you must use an indirect route, verify the intermediate objects are fully populated before treating the model as configured.

## Surface Selection Heuristics

### 1. Direct component routing beats component-group indirection
If one route lets you say:

- component `H2` -&gt; outlet A
- component `NC7` -&gt; outlet B
- component `TOLUENE` -&gt; outlet B

directly, prefer that over a route that requires:

- creating component groups
- populating each group
- attaching groups to substreams
- attaching substreams to outlet behavior

The extra layer is only worth it when the problem statement or the verified Aspen surface actually depends on that structure.

### 2. Prefer validated hardcoded-style surfaces
If a nearby hardcoded script already proves a stable route for the same duty, prefer the same block family and setter surface unless live evidence contradicts it.

Examples of stable evidence:

- `Sep2` plus per-component `set_fracs`
- a direct splitter with explicit per-component product assignment

Do not replace a validated direct route with a more abstract route just because the more abstract tool names sound more general.

### 3. Treat component groups as real objects, not labels
If an indirect route uses component groups, stream groups, or substream component lists, the route is not complete until you verify that those objects are populated.

Do not assume success just because:

- the group name exists
- a setter accepted a symbolic value
- the flowsheet-level readiness looks better

Require evidence that the intermediate object contains the intended components.

### 4. Guard against translation-only failures
If the model appears input-complete but Aspen later fails during input translation, suspect unresolved indirect separator inputs such as:

- empty component groups
- missing substream component lists
- symbolic group names that were referenced but not populated

Before changing unrelated blocks, inspect whether the separator route depends on hidden intermediate objects that were never fully materialized.

### 5. For shortcut teaching problems, prefer the smallest faithful expression
When the task is a pedagogical shortcut problem and the intended behavior is idealized, prefer the smallest faithful surface that encodes the routing.

Do not escalate from:

- direct component fractions on a shortcut splitter

to:

- generic separator plus component-group machinery

unless the simpler route is proven unavailable.

## Practical Workflow
For each separation duty:

1. Restate the component destinations explicitly.
2. Identify candidate block families that satisfy the material-port semantics.
3. Among those families, prefer the setter surface that writes direct component routing with the fewest hidden intermediate objects.
4. If using an indirect route, verify every intermediate object before proceeding.
5. If translation fails later, revisit the indirect objects first.

## Generic Examples

### Example A: complete hydrogen removal
Task semantics:

- one feed enters
- hydrogen leaves separately
- all other components stay together

Preferred route:

- choose a family with two real material outlets
- use direct per-component splits if available
- avoid component groups unless the verified surface forces them

### Example B: aromatics product plus reactant recycle
Task semantics:

- benzene and toluene leave as product
- unreacted paraffin returns as recycle

Preferred route:

- use a shortcut splitter that can assign fractions or recoveries directly by component
- avoid a generic separator route that requires extra group objects just to express the same destinations

## Stop Conditions
Stop and replan when any of the following becomes true:

- the chosen route requires component groups or substream lists, but you do not have evidence they are populated
- a direct component-routing surface exists in hardcoded evidence, but the current plan drifted to a more abstract route without justification
- translation fails after a flowsheet-level completion pass, suggesting hidden separator inputs are unresolved
- the only reason for the current route is that it sounded more general, not that it was validated

## Output Expectations
When this skill changes a plan, explain:

- the explicit component destinations from the task
- which block family satisfies the material-port semantics
- which setter surface writes the routing most directly
- why any more indirect component-group route was rejected

```

### FILE: aspen_agent_skills/guides/shared-material-port-topology/SKILL.md
Reason: selected skill for task block family
```text
---
name: shared-material-port-topology
description: Handles Aspen blocks that expose shared material collection ports. Use when a Mixer, FSplit, reactor, or other block seems to have too few material ports, when agents are tempted to invent numbered ports, or when recycle/product branches are being kept only as aliases instead of physical connections.
---

# Shared Material Port Topology

## Core Rule
Some Aspen blocks expose one collection port for many material streams. A single live port can accept multiple streams through `Elements.Add(...)`.

Do not assume &quot;one process branch = one visible port&quot;.

## Common Cases
- Mixer-like blocks may expose one shared `F(IN)` and one `P(OUT)`. Connect every material feed to `F(IN)`, then connect the mixed product to `P(OUT)`.
- A connected Mixer may still need a minimal input paragraph before export/run.
  If history says `BLOCK: &quot;M1&quot; APPEARS IN THE FLOWSHEET, BUT NO BLOCK
  PARAGRAPH HAS BEEN ENTERED FOR IT`, keep the topology and write a coherent
  Mixer spec bundle such as `MTYPE=INSTANTANEOUS`, `NPHASE=1`, `ENERGY_BAL=YES`,
  `MIN_PRES=YES`, and an explicit outlet pressure via `set_pres`. Re-check
  `check_block_completion` before running.
- Ports such as `WS(IN)`, `PS(IN)`, `HS(IN)`, and related OUT ports are work,
  pressure, or heat/utility ports; never use them for material recycle/feed
  streams just because a second material feed is needed.
- FSplit may expose one shared `F(IN)` and one shared `P(OUT)`. Connect the feed to `F(IN)` and all product streams to `P(OUT)`.
- RadFrac may expose one shared `F(IN)` for multiple feed streams while still
  using role-specific product ports such as `LD(OUT)`, `VD(OUT)`, and `B(OUT)`.
  For RadFrac, use role-aware helpers such as
  `configure_radfrac_extractive_distillation_pair(...)` or
  `configure_radfrac_no_condenser_reboiled_bottoms(..., configure_topology=True)`
  instead of requiring one feed port per feed stream.
- For FSplit, set split fractions for all product streams except one closure stream. Aspen rejects specifying every outlet fraction.
- Flash2 is not a one-product block. It usually exposes `V(OUT)` and `L(OUT)` phase products instead of `P(OUT)`.

## Phase-specific outlets are not interchangeable

Stream IDs are arbitrary: prove vapor/liquid identity by native port ownership plus same-run phase/vapor_fraction, not names or port/list order. Flash2 `F(IN)`, `V(OUT)` and `L(OUT)` must be read back after the role-aware helper. Discover Flash3/REquil native ports rather than inventing Flash2 tokens. A names-only mismatch needs consistent answer mapping; task-bound/downstream physical mismatches require reconnecting and rerunning, not renaming. See `vapor-liquid-outlet-role-validation`.

## Generated-script port evidence contract

For strict slim generated source, `list_block_ports` is an **opaque diagnostic evidence capability**. Its payload belongs to the runtime and the next repair iteration, not to current-iteration model logic.

Generated code must:

1. Record a bounded port probe directly through `runtime.stage(..., required=False)` before or after a topology operation when live evidence may help the next iteration.
2. Leave the returned payload unassigned and uninterpreted. Do not inspect `result`, `ports`, keys, values, connection lists, status-derived port meaning, or any nested field.
3. Never branch, choose a port, retry, or rewrite topology in the same execution based on the probe result. The current source has a fixed topology plan; an Aspen rejection remains a failing fact for the next iteration.
4. Use a registered role-aware/high-level topology capability for actual connection work. If no such capability expresses the intended topology, preserve the blocker instead of writing a generated port router.
5. Let `runtime.stage` persist the complete opaque payload as an artifact. The repair context must expose the relevant probe and connection failure to the next iteration.
6. Keep static topology safeguards: one unique material stream ID per physical edge, Aspen-safe short IDs, no block/stream token collision, and `validate_material_edge_plan(...)` before mutation.
7. Keep all required blocks and streams in completion/evidence gates. An alias, mapping, shadow stream, or diagnostic-only object is not a physical connection.

Canonical generated form:

```python
runtime.stage(
    &quot;C1_ports_before_connect&quot;,
    lambda: client.invoke(
        &quot;list_block_ports&quot;,
        block_name=&quot;C1&quot;,
    ),
    required=False,
)

runtime.stage(
    &quot;connect_C1&quot;,
    lambda: client.invoke(
        &quot;connect_material_inlet_outlet&quot;,
        block_name=&quot;C1&quot;,
        inlet_stream=&quot;F1&quot;,
        outlet_stream=&quot;P1&quot;,
    ),
    required=True,
)

runtime.stage(
    &quot;C1_ports_after_connect&quot;,
    lambda: client.invoke(
        &quot;list_block_ports&quot;,
        block_name=&quot;C1&quot;,
    ),
    required=False,
)
```

The script does not assign any of these port-probe results. The full artifacts are evidence for runtime/parent review and the next repair iteration.

## Framework boundary

`safe.extract_block_ports(...)` remains a framework/internal deterministic utility for implementing and testing registered high-level topology transactions. It is not part of the strict generated-source recommendation surface. Generated scripts must not call it.

When real-time port-dependent selection is necessary, implement that behavior once inside a registered high-level capability such as a role-aware connector. That capability may normalize ports, select legal native roles, connect, read back, and return the complete before/after evidence. Generated code only declares intent through the semantic capability name.

## Preferred topology capabilities

- Use `connect_shared_material_port_block(...)` for shared-inlet/shared-outlet blocks such as mixers.
- Use `configure_fsplit_shared_outlets(...)` for FSplit blocks with multiple product streams on shared `P(OUT)`.
- Use role-aware RadFrac topology capabilities because vapor distillate, liquid distillate, and bottoms are not interchangeable.
- Use `connect_flash2_vapor_liquid_ports(...)` for Flash2 feed, vapor product, and liquid product wiring.
- Use `connect_material_inlet_outlet(...)` for ordinary one-feed/one-product material blocks.
- Use `validate_material_edge_plan(...)` before topology mutation.

## Anti-Patterns
- Assigning `list_block_ports` to a variable, returning it from a custom wrapper, passing it to a generated parser, or inspecting any field in the current script.
- Calling `safe.extract_block_ports(...)` from generated source.
- Choosing `F(IN)`, `P(OUT)`, or another port conditionally from a live probe during the same execution.
- Treating a successful port probe as proof that the intended stream is connected.
- Inventing ports such as `P1(OUT)`, `P2(OUT)`, `F2(IN)`, or `S(OUT)` when live ports do not show them.
- Reusing one material stream across multiple unrelated block edges, especially in recycle flowsheets.
- Naming streams `P1`, `P2`, etc. when those names are also used for pump blocks.
- Using descriptive stream IDs such as `BZIN`, `H2RCY`, or `PRODUCT`; those violate the script-agent Aspen naming rule even if they are semantically clear.
- Dropping recycle, purge, or product branches because only one material port is visible.
- Marking a required stream as &quot;logical only&quot; or &quot;retained in name mapping&quot; after failing to connect it physically.

```

### FILE: aspen_agent_skills/guides/radfrac-absorber-like-configuration/SKILL.md
Reason: selected skill for task block family
```text
---
name: radfrac-absorber-like-configuration
description: Configure RadFrac for absorber-like, stripper-like, or bottom-fed vapor service when the column is not a plain condenser-plus-reboiler distillation setup. Use when Condenser=None, Reboiler=None, side draws, non-distillate top products, saturated vapor enters near the bottom, or completion/REP/PER_ERROR mentions product phase, dry column, product completeness, or bottom-stage feed requirements.
---

# RadFrac Absorber-Like Configuration

## When To Use
Use this skill when a tower is being approximated with `RadFrac` but its service is closer to an absorber, stripper, or side-draw column than a standard distillation column.

## Core Rules
1. Match each physical product to the right outlet role. Prefer `LD(OUT)` for standard total-condenser liquid distillate, `VD(OUT)` only for true top vapor / partial-condenser service, `B(OUT)` for bottoms, and `SP(OUT)` for recycle or intermediate withdrawals that are not true distillate products.
2. Keep end effects and product phases consistent. If `Condenser=Total`, the distillate must use liquid-distillate semantics; do not leave the only top product as vapor/total-vapor on `VD(OUT)`. If `Condenser=None` or `PARTIAL-V`, do not assume a liquid distillate is valid. If `Reboiler=None`, verify the bottom-side feed definition before tuning operating specs.
3. For `PARTIAL-V` columns with a vapor distillate/top product and a bottoms product, connect the vapor top product to `VD(OUT)` and the bottoms product to `B(OUT)`. Do not pre-connect `LD(OUT)` unless Aspen completion or the task explicitly requires a liquid distillate side product; an existing `LD(OUT)` stream can make `set_condenser(PARTIAL-V)` fail.
4. When `CONDENSER=PARTIAL-V` and the top product is vapor, keep the product
   outlet on `VD(OUT)` but choose the operating-spec variable from the visible
   UI/spec row. If the row says `Distillate rate`, write **`BASIS_D`**
   (`Data\Blocks\&lt;BLK&gt;\Input\BASIS_D`) with the task molar-flow unit. Use
   **`BASIS_RDV`** / `set_basis_rdv` only when the task or live UI explicitly
   exposes a vapor-distillate fraction/rate spec rather than the ordinary
   `Distillate rate` row. In generated scripts prefer a helper that preserves
   this mapping instead of `set_condenser(PARTIAL-V)` alone.
5. Treat side products as explicit side draws, not as disguised distillate or bottoms. Set side-draw stage, phase, and flow explicitly, then read them back.
6. When the bottom feed is intended to satisfy a no-reboiler configuration or a saturated-vapor feed enters near the column bottom, verify both `FEED_STAGE` and feed convention. Do not assume a last-stage feed defaults to `ON-STAGE`.
7. Use completion messages as a topology-and-spec checklist. Fix port roles, phase consistency, and feed conventions before changing reflux, boilup, or solver settings.
8. Validate column intent with readback and completion, not with setter success alone.

## Probe-Backed Product Role Map

Evidence: `scripts/probe_radfrac_product_role_matrix.py`, last verified at
`runtime/radfrac_product_role_matrix_probe/20260628_122147/summary.json`
using a minimal BENZENE/TOLUENE RadFrac with default vapor-liquid valid phases
and no free water.

| `CONDENSER` | Top product port map | Required/validated spec surface | Probe result |
| --- | --- | --- | --- |
| `TOTAL` | top liquid product on `LD(OUT)`, bottoms on `B(OUT)` | `BASIS_RR` + `BASIS_D` | `PER_ERROR=0` |
| `TOTAL` | only top vapor product on `VD(OUT)` | `BASIS_RR` + `BASIS_D` | Fails: `&quot;RDV&quot; IS LESS THAN 1. A LIQUID DISTILLATE STREAM IS NEEDED BUT NOT SPECIFIED.` |
| `PARTIAL-V` | top vapor product on `VD(OUT)`, bottoms on `B(OUT)` | `BASIS_RR` + `BASIS_D` when the visible row is ordinary `Distillate rate`; also valid with `BASIS_RDV` + `BASIS_RR` + `BASIS_B` when vapor-distillate fraction is explicitly intended | `PER_ERROR=0` |
| `PARTIAL-V` | only top liquid product on `LD(OUT)` | any ordinary distillate-rate setup | Fails: `&quot;RDV&quot; IS GREATER THAN 0. A VAPOR DISTILLATE STREAM IS NEEDED BUT NOT SPECIFIED.` |
| `PARTIAL-V-L` | both `VD(OUT)` and `LD(OUT)` connected | `BASIS_RDV` + `BASIS_RR` + `BASIS_B` | `PER_ERROR=0` |
| `PARTIAL-V-L` | only `LD(OUT)` with `RDV=0` | `BASIS_RDV=0` + `BASIS_RR` + `BASIS_D` | `PER_ERROR=0`, but prefer `TOTAL` for true liquid-only service |
| `PARTIAL-V-L` | only `VD(OUT)` with `RDV=1` | `BASIS_RDV=1` + `BASIS_RR` + `BASIS_B` | `PER_ERROR=0`, but prefer `PARTIAL-V`/`NONE` for true vapor-only service |
| `PARTIAL-V-L` | any top-port arrangement without `BASIS_RDV` | `BASIS_RR` + `BASIS_D`, or stream `PROD_FLOW` alone | Fails: `&quot;T1&quot; OR &quot;RDV&quot; NEEDS TO BE SPECIFIED.` |
| `NONE` with reboiler | top vapor product on `VD(OUT)`, bottoms on `B(OUT)`, feed or pumparound enters stage 1 | Bottoms/boilup-style handles such as `BASIS_B`; no condenser reflux/distillate semantics | `PER_ERROR=0` in the probe with top-stage feed |
| `NONE` with reboiler | only top liquid product on `LD(OUT)` | bottoms/boilup-style handles | Fails: `&quot;RDV&quot; IS GREATER THAN 0. A VAPOR DISTILLATE STREAM IS NEEDED BUT NOT SPECIFIED.` |
| `NONE` with reboiler | `VD(OUT)` but no feed/pumparound to top stage when `Q1=0` | bottoms/boilup-style handles | Fails: `WHEN &quot;Q1=0&quot;... THERE MUST BE A FEED/PUMPAROUND ENTERING THE TOP STAGE.` |

Do not collapse this map to &quot;`Condenser=None` or `PARTIAL-V` means `VD(OUT)`&quot;.
`PARTIAL-V-L` is governed by `RDV`; `RDV=0` and `RDV=1` are legal boundary
cases, while mixed vapor-liquid service needs both top ports and an explicit
`BASIS_RDV`. `NONE` also has an independent top-stage feed/pumparound
requirement when condenser duty is zero.

## Bottom Vapor Feed Pattern
For tasks that say a saturated vapor feed enters at or near the bottom of a RadFrac column:

1. Put the feed on the intended bottom-side stage, often `NSTAGE`.
2. Set feed convention explicitly with `FEED_CONVEN/&lt;stream&gt;` and `FEED_CONVE2/&lt;stream&gt;` as `ON-STAGE-VAP`.
3. Align feed pressure with the column pressure profile. If using pressure drop, set `OPT_PRES=DP-COL` and `DP_COL`, then choose feed pressure consistent with the feed stage.
4. Choose one distillate operating spec: material-balance molar flow (`BASIS_D`) **or** distillate/feed ratio (`D:F`), never both. Writing these numeric leaves can change the active `COL-SPECS` selection; `D:F` is not a harmless annotation after `BASIS_RR + BASIS_D`. In `configure_radfrac_bottom_vapor_feed`, explicit `distillate_flow` takes precedence when both arguments are present; `d_over_f` is recorded as inactive evidence, not sent to Aspen. Use only `d_over_f` to request the ratio route. The helper preserves the existing end-effect -&gt; stage/pressure -&gt; feed convention -&gt; reflux -&gt; selected draw write order; it does not clear old specs on an inherited column. Verify active UI/COL-SPECS rows before switching an inherited basis, and do not invent selector paths.
5. If the REP says `COLUMN DRIES UP OR COLUMN FLOWS VIOLATE BUILT-IN LIMITS`, re-check feed convention, pressure profile, product draw basis, stage count, and product outlet roles before changing solver tolerances.

In generated hardcoded scripts, prefer `configure_radfrac_bottom_vapor_feed(...)`
from `runtime/script_agent_experiment/script_agent_exp/safe_aspen_calls/`
when this pattern applies. The runtime parent owns canonical import roots;
generated scripts must not modify `sys.path` or scan legacy experiments paths.

## End-Mode-Aware Operating Specification Budget

`TOTAL/NONE` is not an ordinary two-numerical-spec distillation column. Aspen counts `Reboiler=None` as an operating specification, so only one additional numerical operating spec remains. `BASIS_RR + BASIS_D` can therefore be overspecified even when no `D:F` setter exists. Keep the requested `NONE`; do not introduce a kettle reboiler to make the pair fit. With reflux ratio as the chosen handle, a material-balance distillate estimate belongs in diagnostic/target evidence, not another setter.

Use `configure_radfrac_operating_spec_bundle(..., condenser=&quot;TOTAL&quot;, reboiler=&quot;NONE&quot;, reflux_ratio=...)` after end effects and feed conventions are landed. The bottom-vapor-feed helper delegates to this bundle; explicit flow still precedes ratio for the ordinary `TOTAL/KETTLE` case. In `TOTAL/NONE`, reflux takes precedence over supplied draw estimates; the unused values and reason are recorded explicitly. The total-condenser helper accepts `reboiler=&quot;NONE&quot;` rather than forcing its default kettle representation. No helper clears inherited specs or writes a guessed selector. Setter rejection remains fatal. Inspect the actual `COL-SPECS` table, end-mode readback, completion and current-run evidence: populated numeric leaves alone do not prove active specification membership. `BASIS_RDV=0` in a total-condenser backup is a product-phase condition, not proof of an extra independent operating spec. For inherited or utility-exchanger configurations, live active rows remain authoritative. `COL-SPECS` is a serialized BKP/UI section and is not necessarily an Aspen tree node: a failed tree-table lookup must remain visible rather than trigger guessed selector paths. `collect_radfrac_operating_spec_state` records native numerical-leaf values and `node_props` prompts, end modes and completion. In verified `TOTAL/NONE` readback, the draw-leaf prompt explicitly states that only one Operating Specification is allowed; RR is populated while the unselected draw leaves remain unset. Combine this with same-session exported BKP `COL-SPECS`, setter rejection and run evidence; do not label it as a successful GUI active-row table readback.

## No-Condenser / No-Reboiler Absorbers

When the task explicitly says `Condenser=None` and `Reboiler=None`, preserve that process intent. Do not silently change the model to `PARTIAL-V` plus `KETTLE` just to make completion easier; that turns an absorber into a distillation surrogate and can converge to the wrong product semantics. A generated script that records `PARTIAL-V`/`KETTLE` as a &quot;runnable representation&quot; for this kind of task should remain failing until the no-condenser/no-reboiler configuration has been repaired.

Do not infer `Reboiler=None` from &quot;no condenser&quot; alone. If only the condenser is absent and the task gives a bottom-product temperature target, keep `Condenser=None` but allow a real reboiler or bottom operating specification. A cold-feed column with both `Condenser=None` and `Reboiler=None` may be physically unable to reach a warm bottoms-temperature target by varying solvent flow, vapor draw, or a bottom vapor stub.

For no-condenser absorber-like tasks with cold feeds, a warm bottoms-temperature target, and a requested top vapor product flow/composition, use `radfrac-no-condenser-reboiled-bottoms` instead of this no-reboiler repair pattern unless the task explicitly says no reboiler. The required settings are `Condenser=None`, `Reboiler=KETTLE`, `ABSORBER=NO`, a true overhead vapor outlet stream, a bottoms stream, and a bottom energy/spec handle such as boilup ratio or reboiler duty for the Design Spec. Do not set `ABSORBER=YES`, do not use a near-top side draw as the only vapor outlet, and do not vary the top vapor stream flow to satisfy a bottoms-temperature target.

For no-reboiler RadFrac absorbers, Aspen may require a bottom-side vapor/on-stage feed convention even when the physical bulk feed belongs on an upper stage. Use this repair order before changing condenser/reboiler mode:

1. Keep the absorbent as an on-stage liquid feed at its stated upper stage.
2. Keep the main gas feed at the stated stage, and explicitly set `FEED_CONVEN/&lt;stream&gt;` and `FEED_CONVE2/&lt;stream&gt;` to vapor/on-stage tokens such as `ON-STAGE-VAP`.
3. If Aspen still needs bottom-stage vapor traffic for `Reboiler=None`, split a small documented fraction of the gas feed to a separate Aspen-safe stream on stage `NSTAGE`; preserve total feed composition and flow across the main and bottom-stub streams.
4. Set the bottom-stub feed convention with `FEED_CONVEN` / `FEED_CONVE2` as `ON-STAGE-VAP`.
5. For top gas products, use the true top vapor outlet where possible. If Aspen forbids writing product flow on a top/bottom outlet, use a documented near-top vapor side draw only for the initial product-flow guess, and report the actual top-gas evidence from REP/readbacks.

In generated scripts, prefer `configure_radfrac_no_condenser_absorber(...)` from `script_agent_exp.safe_aspen_calls` for the end effects, feed-stage rows, and feed-convention writes. It keeps `Condenser=None` and `Reboiler=None` instead of drifting to `PARTIAL-V`/`KETTLE`.

If a repeated helper call reports `Variable CONDENSER not found` or `Variable REBOILER not found` after an earlier successful `NONE` write in the same session, treat this as a possible Aspen option-tree/idempotency collapse, not as permission to skip condenser/reboiler setup. Keep using `configure_radfrac_no_condenser_absorber(...)`; the helper should record structured idempotent evidence only when a prior accepted write or readback proves the target no-condenser/no-reboiler mode. A first-attempt missing node without prior evidence remains a blocker.

### `set_dp_col` requires a pressure unit

The HTTP/MCP `set_dp_col` operation **always** requires `unit` (e.g. `atm`, `kPa`,
`bar`, `mmHg`). Calling `set_dp_col(block_name=&quot;C1&quot;, value=0.0)` without `unit`
fails at the server with `missing 1 required positional argument: &#x27;unit&#x27;`.

- Prefer `configure_radfrac_no_condenser_absorber(..., column_dp=0.0, pressure_unit=&quot;atm&quot;)` — the helper passes `unit=pressure_unit` (or `column_dp_unit`) automatically.
- If writing `set_dp_col` directly: `set_dp_col(block_name=&quot;C1&quot;, value=0.0, unit=&quot;atm&quot;)`.
- `DP_COL` is **pressure drop** (bottom − top), not bottom absolute pressure. For equal top/bottom pressure, use `column_dp=0.0` with a unit; do not skip `set_dp_col` when `OPT_PRES=DP-COL` is selected.

Do not add reflux ratio, distillate flow, boilup, or reboiler duty specs while claiming no-condenser/no-reboiler absorber semantics. If REP says the column dries up or has large final relative errors, revisit feed conventions, the bottom-stub fraction, pressure profile, and product outlet roles before adding a reboiler/condenser.

## Workflow
1. Choose ports from physical meaning, not from convenience.
2. Set `CONDENSER` and `REBOILER` mode before dependent product assumptions.
3. Materialize side draws and bottom-feed conventions explicitly.
4. Read back critical variables and run completion checks.
5. Only after topology is valid, tune operating specs or run.

## Additional Resources
- For workflow details and conditioned caveats, see [reference.md](reference.md)
- For abstract examples, see [examples.md](examples.md)

```

### FILE: aspen_agent_skills/guides/radfrac-standard-column-pressure-basis/SKILL.md
Reason: selected skill for task block family
```text
---
name: radfrac-standard-column-pressure-basis
description: Configures standard RadFrac distillation-column pressure basis and pressure-drop direction. Use when a task mentions RadFrac, rigorous distillation, column at 1 atm, top/bottom pressure, pressure drop across the column, mmHg/psi/kPa pressure conversion, or when comparing RadFrac cases against DSTWU pressure basis.
---

# RadFrac Standard Column Pressure Basis

Use this for ordinary RadFrac distillation columns with a condenser/top product
and a reboiler/bottoms product. Do not use it to override absorber-like,
no-condenser, no-reboiler, side-draw, or bottom-vapor-feed service; those cases
need their role-specific RadFrac skills.

## Pressure Anchor

When a task says a column operates at `P` with a pressure drop across the column,
treat `P` as the top/condenser pressure unless the task explicitly says the
bottom/reboiler is the reference.

For a normal distillation column:

- Top/condenser pressure is the lower pressure.
- Bottom/reboiler pressure is the higher pressure.
- A positive pressure drop means `P_bottom = P_top + deltaP`.
- Do not implement the same statement as `P_bottom = P` and `P_top = P - deltaP`
  unless the task explicitly anchors the bottom pressure.

Examples for &quot;1 atm column, 1 psi pressure drop&quot;:

- Correct top-anchored basis: `top = 1 atm = 760 mmHg = 101325 Pa`;
  `bottom = top + 1 psi = 811.715 mmHg = 108220 Pa`.
- Wrong for the usual wording: `bottom = 1 atm`, `top = 1 atm - 1 psi`.

## RadFrac Setup

Use RadFrac pressure fields consistently with the chosen helper/tool contract.
For direct tree writes, prove the final REP pressure profile rather than trusting
the setter names alone. The REP should show stage 1/top at the anchor pressure
and lower stages at the anchor plus drop for a normal top-anchored case.

## Product Spec Surface

For an ordinary RadFrac with `Condenser = Partial-Vapor`, `Reboiler = Kettle`,
and operating specs shown as `Reflux ratio` plus `Distillate rate`, the
distillate-rate cell is the native product-rate spec:

- Write `Data\Blocks\&lt;BLK&gt;\Input\BASIS_D`, e.g.
  `Application.Tree.FindNode(&quot;\Data\Blocks\D1\Input\BASIS_D&quot;)`.
- Use the task&#x27;s molar-flow unit for the visible `Distillate rate` row; for
  kmol/h tasks the value belongs on `BASIS_D` with a compatible kmol/time unit.
- Do not route this GUI combination to `BASIS_RDV` / `set_basis_rdv` or to a
  fractional `D:F` surface unless the task or live UI explicitly changes the
  operating-spec row away from `Distillate rate`.

Read back `BASIS_RR` and `BASIS_D` before trusting the column setup; a blank
`BASIS_D` under this spec pair means the column operating specs are incomplete.

## Partial-Condenser Temperature

For RadFrac partial condensers, Aspen&#x27;s required condenser-temperature input is
the `T1` node, not PetroFrac-style `T_COND`. If history says `&quot;T1&quot; OR &quot;RDV&quot;
NEEDS TO BE SPECIFIED`, use the RadFrac `set_t1` operation, or the compatibility
alias `set_t_cond` which writes `Data\Blocks\&lt;BLK&gt;\Input\T1`.

Do not spend repair time searching for `OPT_COND` / `T_COND` under RadFrac unless
live UI evidence proves that this specific case exposes those nodes. A
`PARTIAL-V-L` RadFrac can satisfy the translator with `T1=&lt;temperature&gt;` plus the
normal operating specs, or with `BASIS_RDV` when a vapor-fraction spec is intended.

## Native RadFrac Pressure Modes

Do not flatten every RadFrac pressure-drop task into explicit top/bottom endpoint
pressures. Some validated Aspen files use RadFrac&#x27;s native pressure-option modes,
and those modes carry semantics that are not obvious from `PRES1` / `PRES2` names
alone.

- If the task, reference BKP, or known benchmark template already uses a native
  RadFrac mode, preserve that mode unless there is clear evidence it is wrong.
- If a reference BKP/APW explicitly shows `P-SPEC2` or `PRES1` plus `PRES2`,
  treat `PRES2` as a required second pressure anchor. Do not replace it with a
  `PRES1`-only setup, and do not spend a repair probe only on stages, feed
  locations, reflux, product draw, or recycle solver settings before testing the
  reference pressure surface.
- `OPT-PRES=DP-COL` means the block is using a column pressure-drop option. Keep
  the mode and its paired pressure/spec rows together; do not rewrite it as a
  simple bottom-at-`P` or top-at-`P` endpoint model without REP readback.
- `OPT-PRES=DP-STAGE` means the block is using a staged pressure specification.
  Preserve companion fields such as `OPT-PRES-TOP` and the corresponding
  `P-SPEC` rows; verify the stage pressure profile in the REP.
- `PRES1` and `PRES2` are mode-dependent RadFrac inputs. In `DP-COL` /
  `DP-STAGE` cases, do not assume they are always raw top and bottom endpoint
  pressures. Check the selected `OPT-PRES` mode first.

For the standard RadFrac Pressure tab in `Top / Bottom` view:

- `Data\Blocks\&lt;BLK&gt;\Input\OPT_PRES_TOP` selects the top-of-column pressure
  option. `STAGE-2` pairs with `Data\Blocks\&lt;BLK&gt;\Input\PRES2`; `DP-COND`
  pairs with `Data\Blocks\&lt;BLK&gt;\Input\DP_COND`.
- `Data\Blocks\&lt;BLK&gt;\Input\OPT_PRES` selects the pressure-drop option for the
  rest of the column. `DP-STAGE` pairs with
  `Data\Blocks\&lt;BLK&gt;\Input\DP_STAGE`; `DP-COL` pairs with
  `Data\Blocks\&lt;BLK&gt;\Input\DP_COL`.
- Unit-bearing pressure leaves must be written through unit-aware setters or
  COM unit APIs. A raw `typed helper write surface` write is suitable for enum leaves such as
  `OPT_PRES_TOP`, but not sufficient when the value&#x27;s unit must be selected on
  the same Aspen node.
- For a per-stage pressure-drop task, the usual direct expression is
  `OPT_PRES_TOP=STAGE-2`, `PRES2=PRES1 + deltaP_per_stage`,
  `OPT_PRES=DP-STAGE`, and `DP_STAGE=deltaP_per_stage`, followed by REP
  pressure-profile verification.

Treat reference BKP pressure settings as evidence for the current task only, not
as reusable global rules. If a reference file uses a native RadFrac pressure mode,
mirror the mode and verify the resulting pressure profile; do not record the
case name, task number, or benchmark-specific numeric pattern in this skill.

For ordinary new tasks that only say &quot;column at `P` with pressure drop `deltaP`&quot;
and give no reference BKP or native mode, keep the default top-anchored basis:
`P_bottom = P_top + deltaP`.

Required final evidence:

- Read back or REP evidence for top and bottom pressures in one unit basis.
- When using generated scripts, `set_pres2` is the curated operation for direct
  `Data\Blocks\&lt;BLK&gt;\Input\PRES2` writes. The safe helper
  `configure_radfrac_total_condenser(..., bottom_pressure=...,
  bottom_pressure_mode=&quot;pres2&quot;)` preserves explicit `PRES2`; its default
  `bottom_pressure_mode=&quot;dp_col&quot;` keeps legacy pressure-drop behavior.
- A statement of which end was anchored and why.
- Feed pressure consistent with the feed stage, not silently copied from the
wrong end of the column.
- Comparison tasks must use the same pressure anchor across shortcut and
rigorous cases unless the task asks for different operating cases.

If a comparison report has to set `basis_consistent=false` solely because one
RadFrac node used bottom-at-1-atm while another used top-at-1-atm, repair and
rerun the inconsistent RadFrac node before producing the final comparison.

## Feed-Stage Pressure Follow-Through

When RadFrac reports `FEED PRESSURE IS LOWER THAN STAGE PRESSURE`, treat that
advisory as a hard run error. `PER_ERROR` stays 1 until the warning is gone.
Do not accept the column or silently change a task-fixed feed state. First classify
feed pressure, temperature and phase/saturation as fixed or adjustable from task
evidence. A warning does not authorize raising a fixed pressure or re-solving PV
at a new pressure (which also changes temperature and enthalpy). Repair coupling:

1. Keep the task-selected feed stage unless live evidence proves it did not
   stick.
2. Read the column pressure profile or the native RadFrac pressure mode that
   determines the pressure at that stage.
3. Only if the task permits adjusting the feed state, set its pressure consistently
   using AnnotatedQuantity/UNIT_REGISTRY conversions and verify the complete state.
   For fixed boundary feeds preserve P/T/phase. If permitted, connect the original
   feed through a real conditioning block; prove live paths and same-run inlet/outlet
   P/T/vapor fraction/enthalpy, work/duty and energy balance. Otherwise report the
   conflict as a blocker; do not replace the feed with an altered duplicate.
4. Rerun and require current `PER_ERROR=0` / REP evidence plus fixed-state and live
   topology preservation before trusting column results.

A feed stage setting is incomplete until the feed stream pressure is compatible
with that stage&#x27;s pressure.

## Total-condenser helper signature

`configure_radfrac_total_condenser` uses `pressure_unit=` for pressures and `distillate_flow_unit=` for the product-rate specification. Do not pass a generic `unit=` keyword. The helper owns family-specific `set_pres1`/`set_pres2`/`set_dp_col` and `set_basis_d` routing.

## Exact direct feed-stage signature

For a RadFrac feed that is not already owned by a standard high-level column bundle, use exactly:

```python
client.invoke(&quot;set_radfrac_feed_stage&quot;, block_name=&quot;D1&quot;, stream_name=&quot;F1&quot;, value=20)
```

`set_radfrac_feed_stage` accepts `block_name`, `stream_name`, and `value`. Never pass `stage=`, `stage_number=`, or `feed_stage=` to this capability. `feed_stage=` belongs to high-level helpers such as `configure_radfrac_total_condenser`, which translate it internally to `value`.

```

### FILE: aspen_agent_skills/guides/aspen-completion-error-hints/SKILL.md
Reason: selected skill for task block family
```text
---
name: aspen-completion-error-hints
description: Maps common Aspen completion, Next-gate, REP, and PER_ERROR messages to generic repair actions. Use when generated Aspen scripts fail with input_incomplete, FEEDS not complete, HeatX temperature crossover, zero feed, invalid temperature specifications, solver nonconvergence, or when turning Aspen error text into reusable hints.
---

# Aspen Completion Error Hints

## PER_ERROR property-method routing

For raw `PER_ERROR` accompanied by a property-method, phase-equilibrium, or free-water diagnostic, route first to exact active-method readback. `RK-SOAVE` and `SRK` are distinct option-set tokens. The SRK-only `GFREE-WATER=STEAMNBS` repair is forbidden unless current readback proves `SRK` and the current warning requires it. Do not infer a method from a family name, unit set, numerical magnitude, or stale REP.

## Use Error Text As The Driver

Treat Aspen messages as the primary repair signal. Do not patch numeric specs, solver settings, or topology until the message has been mapped to the missing Aspen input surface.

Keep the repair generic: record the block type, the exact Aspen message, the operation/helper to try first, and the readback proving the message is cleared.

## PER_ERROR Ownership Before Probing

Global `PER_ERROR` is a run-health signal, not proof that the task&#x27;s manipulated
block caused the problem. If the current REP says calculations completed with
warnings and names one or more warning-owning blocks, repair those blocks first.
Do not change task-fixed inputs on unrelated equipment.

- For PIPE text such as `NON-THERMAL OPTION SPECIFIED BUT SINGLE COMPONENT
  PRESENT`, set `TYPE=THERMAL` (`Perform energy balance`). That radio button
  leaves `CHK_BALANC` and `CHK_FLUX` at `YES`, which then require `TAMB_IN`,
  `TAMB_OUT`, `H_T_COEFF`, and `FLUX`. When the task gives none of those
  values, also set `CHK_BALANC=NO` and `CHK_FLUX=NO`. Read `TYPE`,
  `CHK_BALANC`, and `CHK_FLUX` back before rerunning. Do not invent ambient
  temperatures, a heat-transfer coefficient, or a heat flux.
- Keep raw `PER_ERROR=1` blocking until the owning-block warning clears; do not
  turn this routing rule into a warning-only PER_ERROR override.
- Only start a broad convergence probe when current-run block/REP evidence
  implicates the probed block and the proposed axes are not task-fixed.
- `FEED PRESSURE IS LOWER THAN STAGE PRESSURE` on RadFrac is a hard error.
  Keep the task feed stage. Raise that material feed stream pressure to at
  least the pressure of the stage it enters, then rerun until the warning is
  absent and `PER_ERROR=0`. Do not treat the advisory as a passed run.

## Heat-Cascade `PER_ERROR=1`: Classify Before Routing

For multi-effect evaporation and other phase-change heat cascades, raw
`PER_ERROR=1` is a run-health result, not a diagnosis and not an automatic
`configuration_binding` blocker. Distinguish three classes from the current-run
REP/history before choosing the next repair focus:

1. **Input/configuration:** Aspen names missing or illegal inputs, incomplete
   streams/blocks, an invalid option token, or input translation failure. Repair
   that surface and rerun; a sweep cannot repair an incomplete model.
2. **Physical/specification ownership:** all objects are input-complete, but
   Heater/Flash/HeatX modes assign the same energy or phase state to conflicting
   owners. Compare the complete operating-mode bundle against task-visible constraints and current live readbacks. In a temperature-controlled Flash2 cascade, `TQ`
   lets the connected heat stream determine duty; a pressure-controlled
   condenser commonly uses `PV` with `VFRAC=0`. Do not silently replace that
   condenser with `TV` plus invented outlet temperatures: `PV` and `TV` are
   different physical boundaries even when both yield liquid.
3. **Numerical/target closure:** topology and operating-mode ownership match,
   completion is clean, and the run reaches the solver but a tear or equality
   target is not closed. Route this class to native Design Spec or a bounded
   Aspen-backed probe on one responsive, non-task-fixed handle. Do not suppress
   `probe_sweep_matrix` merely because raw `PER_ERROR=1` is present.
4. **Input translation after completion:** `Required Input Complete` followed by `SEVERE ERROR in Aspen input translation` is not tear nonconvergence. Preserve the current engine-run history and extract the first translator message with its owning block/path/token/value/unit. Repair that exact input bundle before any convergence tuning. If the history cannot be tied to the current run, record the provenance failure and obtain a fresh current-run diagnostic; do not guess from an older `.his` or repeat the last ownership patch.

Generic repair transaction for a heat cascade:

- Preserve task-visible adjacency and verify it with live ports.
- Inventory each heat edge: source phase-control mode, calculated duty, sink
  mode, fixed inputs, and the single manipulated handle.
- Compare full bundles, not isolated numbers: Flash2 `SPEC_OPT` plus its paired
  inputs; Heater `SPEC_OPT` plus pressure/temperature and phase; HeatX target,
  U option/U, flow arrangement, and program mode.
- Treat numeric values as causal configuration, not incidental tuning. In `PV`, pressure determines condensation temperature and exported duty; a pressure that was reverse-engineered from an assumed approach can be wrong by an order of magnitude while setter and completion checks still succeed. Use task-stated values or a bounded Aspen probe, and verify explicit-unit readback; never import hidden answer/reference values.
- Compare topology at physical-edge fidelity. Missing a task-visible FSplit and replacing one of its products with an independent boundary stream changes mass/energy accounting even if the downstream Mixer is input-complete.
- Restore a moderate seed inside the allowed bounds. If product concentration is
  the equality target, vary live-steam/utility flow only when it is physically
  responsive; otherwise probe a supported energy/equilibrium handle.
- Prefer native Design Spec when its variable contract is available; otherwise
  use a bounded sweep. Neither method is intrinsically superior. Require the
  selected/final row to retain nonzero downstream liquid and condensate paths.
- Finish only on a new run with raw `PER_ERROR=0`, converged REP Problem Status,
  solved target/residual, and final manipulated value from DS output/REP rather
  than the original stream seed.

Proven generic pattern: a four-effect cascade with Flash2 effects at fixed
cascade temperatures using `TQ`, condensing Heaters using `PV` and `VFRAC=0`, a
shortcut HeatX approach target with explicit constant U, and a product-water
Design Spec varying live-steam mass flow can converge normally. Therefore a
failed variant that changed the condensers to `TV` plus guessed temperatures
must first restore phase-control ownership; raising iteration limits or routing
straight to topology repair is not evidence-based.
## SRK Free-Water Advisory: Repair, Never Override

`FREE-WATER METHOD SHOULD BE STEAMNBS WHEN THE MAIN PROPERTY METHOD IS SRK`
with `DEFAULT FREE-WATER METHOD IS STEAM-TA` maps to the registered Python/ReAct
helper `safe.configure_srk_free_water_steamnbs(client)` (HTTP-backed
`typed helper write surface` / `typed readback helper such as read_stream_output(...)`, not a new standalone native HTTP operation).
Prefer `client.invoke(&quot;configure_srk_free_water_steamnbs&quot;)`; compatible execute
shares the registry, and typed safe helpers remain client-first direct-payload
calls. Invoke supplies the client and returns a status/result envelope. Never
retry missing helpers or local errors through native transport.
Call it proactively after successful `ensure_property_method(..., method=&quot;SRK&quot;)`.
Require setter success plus
`\Data\Properties\Specifications\Input\GFREE_WATER=STEAMNBS` readback.
`FREE_WATER` is not the writable global surface; direct writes return
`AE_UNDERSPEC`. Preserve exact setter failure and actual returned live options;
never invent missing fields/tokens or waive failure because an old value matches.

Raw nonzero SRK `PER_ERROR` remains blocking even with a historical service&#x27;s
effective-zero classification. Rerun until trusted raw `PER_ERROR=0` and the
advisory disappears, export, and cold-reload to verify persisted setup/status.
Do not switch the requested method or tune unrelated equipment to hide the
warning. The expected block-local property-comparison exception is unchanged.

## Setter Errors Must Carry Repair Hints

For small local errors, the generated script should fail with a repairable
payload instead of hiding the failure behind a broad retry loop:

- Preserve exact helper responses with `success: false`, `error`, `traceback`,
  `repair_hint`, `allowed_options`, `suggested_*`, or catalog fields.
- Do not reduce Aspen COM text to a generic `returncode=1`; runtime ruff repair
  needs the original rejected operation and legal alternatives.
- If a setter knows the legal tokens/options, return them in the payload and let
  the next mini repair change only that token/keyword.
- If no legal token is known, return the exact Aspen message and stop at that
  boundary rather than continuing through unrelated candidate operations.

## Property Method Token Errors

Property-method names are exact Aspen option-set tokens. A descriptive paper
name can fail even when the intended Aspen token is available.

| Message | Repair |
| --- | --- |
| `ID must be eight characters or less` while setting `BRAUN-K10` / `Braun K10` | Use `BK10` through `ensure_property_method` / `set_property_method`, then verify `GBASEOPSET` or `GOPSETNAME`. |
| `Invalid symbol value` for a property method | Use one exact token from the setter&#x27;s `suggested_methods` / `available_methods`; do not write `GBASEOPSET` directly with the rejected alias. |
| repeated 300s timeouts after a token rejection | Stop the loop and repair the token first; do not interpret the timeout series as physical property infeasibility. |

Evidence after repair: setter response `success: true`, readback of
`\Data\Properties\Specifications\Input\GBASEOPSET` or `...\GOPSETNAME`, and the
chosen token recorded in `summary.json`.

## Pressure / unit basis: semantic setter error (Class B)

These patterns often trace to **wrong `unit=` on a pressure setter**, not to â€œAspen cannot use barâ€ or a missing custom INSET:

| Symptom | Likely mistake | Repair |
|---|---|---|
| Flash/RStoic runs but V/L split wrong; column feed composition off | Task/meta **bar** written as **`MPa`** (e.g. `-0.05 bar` â†’ `2.15 MPa`) | `set_pres(..., unit=&quot;bar&quot;)` with task numeric value |
| Tree `PRES` readback orders of magnitude wrong after INSET change | Wrote bar under METCBAR, then switched global **`INSET` to SI** mid-build | Re-write bar pressures after SI switch, or use **SI + `unit=&quot;bar&quot;`** throughout â€” see `aspen-custom-unit-set` |
| Pump `DELTA P` / outlet pressure ~1e18; downstream **ZERO FEED** | Pump curve / table validated under **SI** while session stayed on another INSET | Force coherent INSET for equipment tables; re-read upstream `PRES` |

**`set_pres(..., unit=&quot;bar&quot;)` is legal under SI/ENG/MET/METCBAR.** Do not â€œfixâ€ bar tasks by forcing METCBAR unless the task is about display INSET.

Load **`aspen-custom-unit-set`** for INSET routing, template default, and live probes.

## Mixer: `input_incomplete`

If a `MIXER` block remains `input_incomplete` while topology and feeds look connected, suspect missing mixer pressure before rebuilding streams.

Repair hint:

- Write `set_pres(block_name=&lt;MIXER&gt;, value=&lt;pressure&gt;, unit=&lt;unit&gt;)` using the intended outlet/downstream pressure basis.
- Then rerun `check_block_completion(&lt;MIXER&gt;)`.
- For collection mixers, do not gate final engine/export on `required_blocks` until pressure has been written or the mixer has been excluded intentionally.

## RStoic: Reference Component Required

For RStoic blocks, the Next-gate message below usually points to an incomplete
**Heat of Reaction â†’ Reference condition** row on the Reactions sheet, not a
missing conversion key component:

- `Reference Component must be specified for all reactions defined (Setup | Reactions sheet).`

Aspen UI when calculated heat of reaction is enabled expects one populated
reference-condition row per inline reaction. Treat the whole visible row as the
missing input bundle:

| UI column | Meaning |
|-----------|---------|
| Rxn No. | The inline reaction row |
| Reference component | The heat-reference component for that reaction |
| Heat of reaction | Calculated by Aspen; do not hand-write |
| Reference Temperature | The heat-reference temperature |
| Reference Pressure | The heat-reference pressure |
| Reference Phase | The heat-reference phase |

Repair hint:

- Prefer `configure_rstoic_calculated_heat_reference(...)` from
  `script_agent_exp.safe_aspen_calls` after stoichiometry and conversion rows are
  written. Pass one `rows` entry for each reaction row and include the shared
  reference temperature and pressure when the task or visible UI requires them.
- Do not fix this message by rewriting conversion rows or guessing low-level
  reference-condition setters; those can produce plausible readbacks while Aspen
  still lacks the Heat of Reaction reference-condition row.
- Rerun `ui_next_completion(...)` and require the RStoic block itself to clear
  `input_incomplete` before `engine_run` or REP export.
- If calculated heat of reaction was not required by the task, prefer leaving it
  disabled instead of creating the extra reference-row obligation.

## RadFrac: Phase-Equilibrium Fugacity Warning

Aspen messages such as:

```text
INLET/OUTLET PHASES ARE NOT IN EQUILIBRIUM
COMPONENT &#x27;&lt;id&gt;&#x27; IN STREAM &#x27;&lt;stream&gt;&#x27; IS NOT IN PHASE EQUILIBRIUM
RELATIVE ERROR IN VL FUGACITY ...
```

are real thermodynamic boundary-state errors. At vapor-liquid equilibrium, each
component must approximately satisfy `f_i^V = f_i^L`; a reported vapor/liquid
fugacity mismatch means the proposed temperature, pressure, composition, phase
roles, and property method do not define a mutually consistent equilibrium
state. Do not classify this as an ordinary solver-tolerance problem, a display
artifact, or a Sensitivity-only failure.

### Owner And Cause

- The direct error owner is the live block that produces or consumes the named
  stream at the reported phase boundary. Establish ownership with current REP
  inlet/outlet rows and live port readback; never infer it from stream names.
- The upstream cause may still be elsewhere: feed temperature/pressure/phase,
  pressure conditioning, feed convention, condenser/reboiler mode, product
  phase, conflicting operating specifications, or global/block-local property
  method. Keep direct owner and upstream cause distinct in diagnostics.
- A surrounding Design Spec, Sensitivity, or Optimization object may expose the
  bad point, but `SOME ROWS COMPLETED WITH ERRORS` is only the outer symptom when
  current REP/history contains a more specific component/stream fugacity error.

### Generic Diagnostic Order

1. Preserve the exact current-run message, block, stream, component, vapor and
   liquid fugacities, relative error, and run identity.
2. Verify the named stream&#x27;s live owner and physical port role. For a column,
   confirm vapor versus liquid product ownership from native ports and REP phase
   evidence, not names.
3. Read back condenser/reboiler mode, product phase, feed stage/convention, and
   the active operating-spec pair. Reject mixed or overspecified configurations.
4. Read feed, block, and product pressure with explicit units and reconcile all
   values to one absolute-pressure basis through `AnnotatedQuantity` and
   `UNIT_REGISTRY`. Do not compare raw BKP numbers or infer gauge/absolute basis
   from magnitude or the global unit set.
5. Read temperature, vapor fraction, phase compositions, and component flows at
   the named boundary and at the immediately upstream conditioning block.
6. Verify the effective global and block-local property methods from current-run
   readback/REP. Preserve a task-fixed method; do not switch methods merely to
   hide the warning.
7. If analysis is present, preserve its table and selected input, then replay the
   selected point as fixed base inputs. If no analysis is present, diagnose the
   ordinary fixed base directly.

### Repair Transaction

Repair the first verified inconsistent surface while preserving task physics:
correct unit/basis errors, pressure or phase conditioning, native port/phase
roles, feed convention, condenser/reboiler/product-phase compatibility,
conflicting active specs, or an incorrectly landed property method. Do not tune
convergence tolerances before these state and specification checks clear.

For analysis workflows, do not copy a successful neighboring row over the
selected point. Keep the native analysis evidence, replay the actual selected
input in a fixed-base transaction, and only resume DS/SA/OPT after that fixed
base is clean.

### Forbidden Shortcuts

- Do not delete or disable analysis and call the physical warning repaired.
- Do not waive the warning because some analysis rows or product readbacks exist.
- Do not copy a neighboring successful analysis row as final evidence.
- Do not change task-fixed feeds, compositions, reaction conversions, bounds, or
  selected input merely to suppress the message.
- Do not guess pressure units/reference from BKP text or numeric magnitude.
- Do not tune solver methods/tolerances to mask a fugacity-state inconsistency.
- Do not trust setter success without same-run boundary and REP evidence.

### Evidence Gate

Treat the repair as complete only when a new current-session run proves all of:

- `check_next_completion_status` was called before the final `engine_run`;
- live topology and phase roles match the intended process;
- corrected values have explicit-unit readback;
- the owning block no longer reports the phase-equilibrium warning;
- the named component/stream fugacity warning is absent from current REP/history;
- raw `PER_ERROR=0`; and
- any required analysis is rerun afterward and produces its own decision-grade
  output without reintroducing the warning.

## Analysis-Derived Base-Point Repair Before Clean Finalization

A nonzero global `PER_ERROR` must not by itself prevent repair of the base input
that caused an owning Unit Operation warning when a native analysis object has
already produced usable, role-bound successful rows. This is a repair
transaction before clean finalization, not a claim that the analysis run was
globally clean.

Use this route only when current-run evidence separates both layers:

- the analysis table contains explicit successful and failed row statuses, with
  a typed varied coordinate and units; and
- the final/base pass has a distinct block, stream, phase, convergence, or
  specification warning tied to the current seed/base value of that same
  manipulated handle.

Then preserve the full analysis object and its table, identify an accepted
feasible coordinate from named native rows or an Aspen-backed refinement, and
write that coordinate back through the documented typed setter for the
underlying physical input. Exact selection still requires the task policy or an
external acceptance contract; do not pick the nearest, first, last, or largest
successful row by convenience. Prefer an accepted task-optimal row already proven by the native grid. Only when the task explicitly requires tighter boundary resolution may the caller run a bounded Aspen-backed refinement and preserve its provenance.

The repair focus must say which underlying input should be adjusted and why; it
must not stop at `PER_ERROR must be zero`, because that creates a deadlock when
the bad base value itself prevents entry into clean finalization. After
writeback, rerun with the original analysis object and full grid retained unless
actual readbacks prove supported isolation is necessary.

Keep the evidence layers separate:

- preserve raw global `PER_ERROR` and analysis row failures unchanged;
- require the owning Unit Operation warning/error to disappear at the repaired
  base point;
- allow expected infeasible analysis rows to remain explicit boundary evidence;
- do not call the overall analysis transaction clean while raw global
  `PER_ERROR` remains nonzero; and
- require a later selected-base replay to provide its own run, input readback,
  REP/BKP, and reload evidence when the task needs a clean final operating point.

Never delete or disable the analysis object merely to obtain a clean base run,
and never copy an arbitrary successful neighboring row over the seed. With no
accepted row, unresolved units, or no causal binding from varied coordinate to
physical input, publish a structured blocker instead of guessing a writeback.

## HeatX Detailed Geometry: Input Translation Errors

Messages such as `TUBE LENGTH CANNOT BE LESS THAN THE BAFFLED FLOW LENGTH`,
`0.0 &lt; LBC &lt; 0.5*TUBE-LENGTH`, or inlet/outlet baffle-spacing bounds are detailed
HeatX geometry input errors, not convergence failures.

Repair hint:

- Prefer `configure_heatx_detailed_shell_tube_rating(...)` so geometry is written
  as a coherent bundle.
- Enforce tube length greater than baffled flow length; mid spacing strictly below
  half the tube length; inlet and outlet spacing each within Aspen&#x27;s reported
  multiplier bounds relative to mid spacing.
- Preserve task-specified tube count/diameter/material/fouling values. If the task
  does not provide baffle spacings, use helper defaults or leave the unsupported
  detailed option unset; do not invent an isolated enum/value.
- Re-run completion/input translation before engine solve and require the geometry
  warnings to disappear.

## HeatX: Temperature Crossover / Zero Feed / Invalid Temperatures

Messages such as these are physical/specification errors, not evidence results:

- `ZERO FEED`
- `invalid temperature specifications`
- `&quot;COLD&quot; stream is hotter than &quot;HOT&quot; stream`
- `MINIMUM APPROACH TEMPERATURE USED DUE TO TEMPERATURE CROSSOVER`
- `$OLVER` / solver block did not converge after HeatX blocks report errors

Repair hint:

- First verify live HeatX port roles with `list_block_ports` and connection readback: hot stream on `H(IN)/H(OUT)`, cold stream on `C(IN)/C(OUT)`.
- Verify every HeatX feed stream has nonzero flow before changing exchanger specs.
- Check target semantics: `T-HOT` specifies hot outlet temperature; `T-COLD` specifies cold outlet temperature. Do not use terminal approach as a shortcut outlet-temperature `VALUE`.
- For single overall U tasks, use `configure_heatx_shortcut_target(...)` or explicitly set `U_OPTION=CONSTANT` before `set_u`.
- In multi-effect evaporation, preserve heat cascade direction and condenser/boiler roles. A downstream vapor cannot heat a colder/warmer side if readback makes the cold outlet hotter than the hot inlet/outlet.
- If the message persists, report the infeasible HeatX case with REP evidence instead of tuning feed rates, U, or target temperatures to manufacture convergence.

## Tear / Recycle Convergence Blocks

When current-run REP/history names a convergence block such as `$OLVERnn` as `NOT CONVERGED`, separate global method settings from block/unit-operation iteration leaves. Do not guess paths such as `Data\Convergence\Convergence\$OLVERnn\Input\MAXIT` or `Data\Flowsheeting Options\Convergence\Input\$OLVERnn\MAXIT`; a visible `$OLVERnn` label does not prove either path is writable.

Use the registered high-level capability:

```python
client.invoke(
    &quot;configure_recycle_convergence_options&quot;,
    tolerance=1e-5,
    tear_method=&quot;WEGSTEIN&quot;,
    wegstein_max_iterations=300,
)
```

The helper writes Aspen global `Data\Convergence\Conv-Options` fields, including `TEAR_METHOD` and `WEG_MAXIT`, then calls `read_recycle_convergence_setup`. Treat the repair as applied only when setter operations succeed and readback shows the requested values. `wegstein_max_iterations` is the legal keyword; `max_iterations` is not. Do not confuse automatic block `Input\MAXIT` raising with tear-solver convergence settings.

Preserve the process topology and task-fixed operating specifications while changing only convergence controls. After readback, rerun once and require current-run `PER_ERROR=0`, convergence-block normal completion, and disappearance of any downstream mass-balance symptom before trusting results. If method/readback evidence says the active solver is not WEGSTEIN, stop or use an explicitly supported method; do not write WEGSTEIN-only fields blindly.

## RadFrac: No Condenser / No Reboiler Feed Completion

For absorber-like `RadFrac` with `CONDENSER=NONE` and `REBOILER=NONE`, these Aspen messages map to feed-stage and feed-convention repair:

- `FEEDS not complete: SID = &lt;stream&gt;`
- `Stage must be specified.`
- `A feed or pumparound stream to the top stage must be specified when Condenser=None or condenser duty is zero.`
- `A feed or pumparound stream to the bottom stage must be specified when Reboiler=None or reboiler duty is zero.`
- Next-gate text such as `Feed to the Bottom Stage must be specified when Reboiler=None`.

Repair hint:

- Prefer `configure_radfrac_no_condenser_absorber(...)`.
- Provide both `feed_stages` and `feed_conventions`.
- Use `set_pres1(...)` for the top/stage-1 pressure before final completion.
- Gas feeds near the bottom usually need `ON-STAGE-VAP`; liquid absorbent feeds near the top usually need `ON-STAGE-LIQ`.
- Write both `Data\Blocks\&lt;BLK&gt;\Input\FEED_CONVEN\&lt;stream&gt;` and `Data\Blocks\&lt;BLK&gt;\Input\FEED_CONVE2\&lt;stream&gt;` when not using the helper.
- Do not guess table paths like `Data\Blocks\&lt;BLK&gt;\Input\FEEDS\&lt;stream&gt;\STAGE`; use `set_feed_stage(...)` or verified live paths.
- Also load `aspen_agent_skills/guides/radfrac-absorber-like-configuration/SKILL.md` for bottom-stub and product-outlet semantics.

Only tune reflux, boilup, product flows, or convergence methods after the no-condenser/no-reboiler feed completion messages are gone.

## PetroFrac: Pseudo Streams Page (`PSEUDO-STR`)

When Next or flowsheet completion reports:

- `PSEUDO-STR not complete: STREAM = &lt;name&gt; Stage must be specified.`
- Multiple streams in one message, e.g. `STREAM = PA1 ... STREAM = PA2 ...`

Repair hint:

- The stream `&lt;name&gt;` is a **pseudo-side stream** on PetroFrac block `&lt;blk&gt;`, not an ordinary product stream.
- Extract **all** `STREAM = &lt;name&gt;` entries from the same Next message and repair every one; completion is not cleared until every listed pseudo stream has its token-specific required fields.
- Classify pseudo ownership first. For `PA`, call `set_petrofrac_pumparound_specs`; for `STRIPPER`, call `set_petrofrac_side_stripper_specs`; for true `MAINCOL`, call `set_petrofrac_pseudo_stream(block_name=&lt;blk&gt;, stream_name=&lt;name&gt;, pseudo_kind=&#x27;MAINCOL&#x27;, stage=&lt;tray&gt;, phase=&#x27;L&#x27;|&#x27;V&#x27;|&#x27;TV&#x27;|&#x27;TL&#x27;, app=app)`.
- Compatible fields are branch-specific: `MAINCOL` writes `PS2_STAGE` + `PS2_PHASE`; `PA` writes `PS2_PANO` + `PS2_STATE`; `STRIPPER` writes `PS2_STRNO` + `PS2_SOURCE` + `PS2_S_STAGE` + `PS2_S_PHASE` + `PS2_S_STATE`.
- Option lists: `OPT_PSEUDO` â†’ `MAINCOL` | `PA` | `STRIPPER`; `PS2_PHASE` â†’ `L` | `V` | `TV` | `TL`.
- **`Pumparound ID must be specified`** on a PA pseudo stream â†’ the pumparound subobject is missing or `PS2_PANO` is empty. Repair with **`set_petrofrac_pumparound_specs`**, not pseudo page alone.
- **Side-stripper product streams** â†’ use `set_petrofrac_side_stripper_specs` / `configure_petrofrac_side_stripper_bundle` with a native `Subobjects\Strippers\S-n` row, product flow, reboiler duty, and two independent Liquid Return specs such as `return_flow` + `return_duty`.
- Real PetroFrac AD probe result: after full native stripper setup, `OPT_PSEUDO\&lt;stream&gt;` and `PS2_*\&lt;stream&gt;` may be absent/null because Aspen stores the complete stripper through `Subobjects\Strippers\S-n` plus `PSTRS_*` linkage. If the stripper subobject exists, indexed leaves are written, Liquid Return specs are complete, and block/global completion is input-complete, do not treat missing `OPT_PSEUDO\&lt;stream&gt;` as a remaining `PSEUDO-STR` failure.
- Do not set pumparound pseudo streams to `MAINCOL`, and do not write `PS2_STAGE`/`PS2_PHASE` after selecting `PA`; those fields belong to the `MAINCOL` radio branch.
- Vacuum/main product columns with `NPA=0` and no `OPT_PSEUDO` labeled children (typical V1/V2) do **not** need this page.
- Also load `aspen_agent_skills/guides/petrofrac-native-internals/SKILL.md`.

## RadFrac / Column: Dry-Up Or Built-In Flow Limits

Messages such as these indicate a physically inconsistent column specification or feed/traffic setup, not a solver-tolerance problem:

- `COLUMN DRIES UP OR COLUMN FLOWS VIOLATE BUILT-IN LIMITS`
- `stage &lt;n&gt; dries up`
- `dry column`
- severe final relative errors tied to a dry stage, missing liquid traffic, or missing vapor traffic

Repair direction:

- Verify live topology first: feed streams land on the intended stages, product streams use roles consistent with their physical phase, and abandoned/replacement streams are not still connected.
- Verify feed traffic before changing column specs: feed flows are nonzero, stream state specs are complete, feed phase/convention matches the intended tray service, and **upstream flash/reactor/heater pressure-temperature-unit basis** is physically consistent with the column pressure profile (**check Class B bar vs MPa** â€” see pressure section above).
- Check end effects and degrees of freedom as a bundle. `CONDENSER`, `REBOILER`, product phases, reflux/boilup, and product-flow or split specs must describe one coherent column, not a mixed partial setup.
- For `PARTIAL-V` vapor-overhead columns, do not stop at
  `set_condenser(PARTIAL-V)`: provide a coherent product-flow/reflux spec pair.
  If the visible operating-spec row is `Distillate rate`, write
  **`BASIS_D`** (`Data\Blocks\&lt;BLK&gt;\Input\BASIS_D`) with the task molar-flow
  unit. Use **`BASIS_RDV`** (`set_basis_rdv`) only when the task or live UI
  explicitly exposes a vapor-distillate fraction/rate spec; its readback path is
  `Data\Blocks\&lt;BLK&gt;\Input\BASIS_RDV`.
- For no-condenser/no-reboiler or absorber-like service, repair feed-stage/feed-convention/product-outlet semantics before adding reflux, boilup, or distillate-flow specs.
- If dry-up persists after topology and specs are coherent, reassess whether the requested separation, pressure profile, stage count, or product draw basis is physically feasible. Report infeasibility with REP/history evidence instead of masking it with solver settings.

Evidence to require after repair:

- `list_block_ports` or connection readback for feeds/products.
- Readback of feed stage/convention, pressure profile, condenser/reboiler mode, and active column specs.
- Upstream Flash/RStoic **`PRES`** vs task/meta pressure basis.
- A trusted `engine_run` plus REP/history evidence showing the dry-up message is gone.
## RadFrac: Negative Reflux Ratio / `BASIS_RR` Range Error

When Aspen rejects a RadFrac reflux specification with a message such as:

```text
Value is out of range; it must be between 1e-15 and 1e+10
```

and the rejected `BASIS_RR`/reflux value is negative or zero, treat this as an upstream operating-spec calculation error, not as an Aspen convergence failure or a generic input-incomplete message. A reflux ratio is positive; do not clamp the value to a small positive number or replace it with an arbitrary feasible value.

Repair direction:

- Preserve the exact rejected operation, block, value, and Aspen range in the failure payload.
- Trace the value back to the minimum-reflux/q-line/equilibrium calculation. For constant-relative-volatility initialization, evaluate both q-line/equilibrium roots and select the physical root: finite, `0 &lt; x &lt; 1`, compatible with the target distillate composition and pinch direction, and yielding `Rmin &gt; 0`.
- Before calling `set_radfrac_reflux_ratio` or writing `Data\\Blocks\\&lt;BLK&gt;\\Input\\BASIS_RR`, require a finite positive value and record the calculation inputs (`q`, equilibrium basis, target composition, selected root, `Rmin`, and multiplier).
- Write the repaired positive value through the high-level RadFrac helper, then read `BASIS_RR` back and require `0 &lt; RR &lt; 1e10` before checking block completion or running Aspen.
- Keep feed, product, topology, condenser/reboiler, and task-fixed separation targets unchanged while repairing the root-selection calculation.

A negative `BASIS_RR` proves that the proposed configuration transaction is invalid; it does not prove that the column is physically infeasible. Stop at this boundary and expose the exact intermediate calculation instead of continuing with unrelated repairs.

```

### FILE: aspen_agent_skills/guides/aspen-component-radfrac-evidence-repair/SKILL.md
Reason: selected skill for task block family
```text
---
name: aspen-component-radfrac-evidence-repair
description: Guides generic Aspen repairs for pseudo-component metadata, reaction mass balance, RadFrac distillate-flow units, paginated REP stream-table parsing, and trustworthy run evidence. Use when Aspen reports missing component molecular weight, RStoic mass-balance errors, RadFrac mass-balance errors after distillate specs, missing stream readbacks from REP, or untrusted REP/HIS evidence.
---

# Aspen Component RadFrac Evidence Repair

Use this skill only for reusable Aspen modeling lessons. Do not encode case-specific targets, block names, task ids, tuned numeric solutions, or thesis-specific product requirements here.

## Component Metadata

- A successful component-add call does not prove Aspen has complete physical-property metadata. Verify the landed component table before writing material streams, reactions, or downstream specs.
- If Aspen accepts a component ID but later reports missing molecular weight, replace it with a databank-resolvable surrogate that preserves the required formula or molecular weight.
- For pseudo-components used in stoichiometric reactions, choose surrogates whose molecular weights make the reaction mass-balanced. A chemically similar but wrong-formula surrogate can make RStoic reject otherwise correct stoichiometry.
- Record the surrogate choice and basis in `summary.json` under modeling choices or assumptions.

## Family-specific column rate capabilities

Generated scripts must use semantic public names, not ambiguous native tree tokens:

- `client.invoke(&quot;set_radfrac_distillate_rate&quot;, block_name=&quot;C1&quot;, value=99.0, unit=&quot;kmol/hr&quot;)`
- `client.invoke(&quot;set_radfrac_bottoms_rate&quot;, block_name=&quot;C1&quot;, value=40.0, unit=&quot;kmol/hr&quot;)`
- PetroFrac uses `set_petrofrac_distillate_rate` / `set_petrofrac_bottoms_rate`.
- MultiFrac uses `set_multifrac_distillate_rate` / `set_multifrac_bottoms_rate`; its registered signature intentionally has no `unit` keyword.

Do not use generated-facing `set_basis_d` or `set_basis_b`: those native names collide across column families and have different signatures. Framework internals may retain them for backward compatibility.

## RadFrac Distillate Specs

- Confirm the basis of any RadFrac flow spec before writing it. Aspen `BASIS_D` / `set_radfrac_distillate_rate` is a molar distillate-flow specification.
- If the task gives distillate rate as mass flow, convert it to molar flow before calling the RadFrac helper. Record the assumed average molecular weight and converted value.
- A RadFrac column that reports severe mass-balance errors immediately after setting distillate rate often has a basis/unit mismatch, not necessarily bad topology.

## Reactor Readbacks

- Reaction conversion/yield/selectivity should come from Aspen results, preferably REP or direct stream readbacks after a trusted engine run.
- When computing conversion across a reactor, parse or read both inlet and outlet stream component flows. If either stream is missing from the first REP stream table, inspect later tables before reporting `None`.

## REP Stream Tables

- Aspen REP stream sections can be paginated across multiple `STREAM ID` tables. A parser that stops at the first table may silently miss later streams.
- For result extraction, parse all stream tables and merge by stream ID, including component `KMOL/SEC` rows and total `KG/SEC` / `KMOL/SEC` rows.
- Mass fractions derived from REP component molar flows require a trusted molecular-weight map. If a component MW is missing, fix component metadata first.

## Evidence Trust

- Do not treat `engine_run.success=true` as sufficient proof of a completed simulation. Require current-run status evidence such as `PER_ERROR=0`, converged REP problem status, and real APW/REP/BKP or HIS artifacts.
- In headless Aspen sessions, `PER_ERROR` may be unavailable even after a successful engine run. Treat &quot;PER_ERROR node not found&quot; as missing evidence, not as convergence. Export and parse the current REP; accept the run only if REP Problem Status says the calculations completed normally and no real nonzero PER_ERROR is reported.
- If APW export destabilizes a headless rerun, preserve REP plus BKP/DEF evidence and make APW export opt-in rather than blocking summary generation.
- Avoid broad REP-export retry loops after Aspen cannot produce a REP. Use the bounded evidence helper once, preserve diagnostics, and fail clearly if evidence remains untrusted.

```

### FILE: aspen_agent_skills/guides/aspen-pump-outlet-specification/SKILL.md
Reason: selected skill for task block family
```text
---
name: aspen-pump-outlet-specification
description: &gt;-
  Configure Aspen PUMP blocks (pressure, curve, or power mode), set Compr type
  early, preserve efficiency semantics, and map Pump completion text such as
  Outlet Specification must be specified to unset OPT_SPEC.
---

# Rotating Equipment Setup

Use this skill for **Aspen `PUMP` blocks** and `Compr` tasks where the answer depends on block mode, outlet specification, curve data, or efficiency semantics.

## Block family note (important)

Aspen exposes **one pump block family: `PUMP`**. Textbook labels such as “Pump HI” in problem statements refer to **operating/spec context**, not a separate Aspen block type. Always use `create_pump` and configure through `Data\Blocks\&lt;BlockName&gt;\Input\OPT_SPEC` and the dependent inputs below.

## `OPT_SPEC` option list (`Data\Blocks\&lt;BlockName&gt;\Input\OPT_SPEC`)

| Token | Meaning | Follow-up writes |
| --- | --- | --- |
| `PRES` | Discharge pressure | `set_pres(..., unit=...)` |
| `DELP` | Pressure increase | `set_delp(..., unit=...)` |
| `PRATIO` | Pressure ratio | `set_pratio(...)` |
| `POWER` | Required power | `set_power(..., unit=...)` |
| `USE-CURVE` | Performance curve drives outlet | Curve bundle below |

**Curve mode requires `USE-CURVE`.** Do not leave `OPT_SPEC=PRES` and also write a curve table.

## Pump curve workflow (`OPT_SPEC=USE-CURVE`)

Write in order after topology is connected:

1. `set_opt_spec(block_name, &quot;USE-CURVE&quot;)`
2. `set_opt_ctype(block_name, &quot;SINGLE-OPER&quot;)` — or `SINGLE-REFE` / `MULTIP` per task
3. `set_opt_cformat(block_name, &quot;TABLE&quot;)` — for tabulated head vs flow
4. `set_dep_var(block_name, &quot;HEAD&quot;)` — dependent axis for TABLE curves
5. `set_indep_var(block_name, &quot;VOL-FLOW&quot;)` — or `MASS-FLOW` if task uses mass flow
6. `set_pump_curve_table(block_name, curve_points=[{&quot;flow&quot;: …, &quot;head&quot;: …}, …], flow_unit=&quot;m3/hr&quot;, head_unit=&quot;m&quot;, curve_idx=1)`. This call sets `OPT_SPEC=USE-CURVE` itself. A previous `PRES`, `DELP`, `PRATIO`, or `POWER` does not remain the outlet specification.
7. Optional fidelity: `set_eff`, `set_deff`

`set_pump_curve_table` requires explicit `flow_unit` and `head_unit`. Pass the units printed with the curve. Accepted `flow_unit` values include `m3/hr`, `cum/hr`, `l/min`, `gpm`, and `cuft/min`. Accepted `head_unit` values include `m`, `ft`, `cm`, and `in`. Point values use those API units. Aspen&#x27;s block-level `HEAD_UNITS` enum is `METER` or `FT`; the helper writes that token. Do not write `HEAD_UNITS` directly. The worked example below is the verified call.

A missing or illegal unit returns `success: false` with `error_code` `PUMP_CURVE_UNIT` and a message that starts `ERROR_CODE=PUMP_CURVE_UNIT`. That is the runtime ruff repair. Add or replace only `flow_unit` and `head_unit` on the existing call. Keep `curve_points`, `curve_idx`, and the pump mode.

The curve-table operation replaces the target `curve_idx` rows. Repeating the same call does not append a second copy of the points.

### Generic worked example (not tied to any scored case)

Cooling-water circulation pump `CW-P` on `FEED → CW-P → TO-TWR`:

```python
client.invoke(&quot;set_opt_spec&quot;, block_name=&quot;CW-P&quot;, value=&quot;USE-CURVE&quot;)
client.invoke(&quot;set_opt_ctype&quot;, block_name=&quot;CW-P&quot;, value=&quot;SINGLE-OPER&quot;)
client.invoke(&quot;set_opt_cformat&quot;, block_name=&quot;CW-P&quot;, value=&quot;TABLE&quot;)
client.invoke(&quot;set_dep_var&quot;, block_name=&quot;CW-P&quot;, value=&quot;HEAD&quot;)
client.invoke(&quot;set_indep_var&quot;, block_name=&quot;CW-P&quot;, value=&quot;VOL-FLOW&quot;)
client.invoke(
    &quot;set_pump_curve_table&quot;,
    block_name=&quot;CW-P&quot;,
    curve_idx=1,
    flow_unit=&quot;m3/hr&quot;,
    head_unit=&quot;m&quot;,
    curve_points=[
        {&quot;flow&quot;: 18.0, &quot;head&quot;: 22.0},
        {&quot;flow&quot;: 12.0, &quot;head&quot;: 28.0},
        {&quot;flow&quot;: 8.0, &quot;head&quot;: 31.0},
        {&quot;flow&quot;: 5.0, &quot;head&quot;: 34.0},
    ],
)
client.invoke(&quot;set_eff&quot;, block_name=&quot;CW-P&quot;, value=0.72)
client.invoke(&quot;set_deff&quot;, block_name=&quot;CW-P&quot;, value=0.95)
```

Verify with REP/U-O-S readback that curve rows and `OPT_SPEC=USE-CURVE` appear under the pump input section.

## Pressure-target pump workflow (`OPT_SPEC=PRES`)

1. Connect `F(IN)` / `P(OUT)`.
2. `set_opt_spec(block_name, &quot;PRES&quot;)`
3. `set_pres(block_name, value=..., unit=...)` — match task unit set
4. Add `set_eff` / `set_deff` only when task or REP requires them.

### Generic example

Booster pump `B-P` with 450 kPa discharge:

```python
client.invoke(&quot;set_opt_spec&quot;, block_name=&quot;B-P&quot;, value=&quot;PRES&quot;)
client.invoke(&quot;set_pres&quot;, block_name=&quot;B-P&quot;, value=450.0, unit=&quot;kPa&quot;)
```

## Completion diagnostics (Pump)

If completion / Next shows **`Outlet Specification must be specified.`**, `OPT_SPEC` is unset. Set a valid token from the table above before debugging numeric targets.

## Compressor workflow

- Set `TYPE` early on `Compr` blocks.
- Then `OPT_SPEC` + dependent pressure target.
- Keep `PEFF` and `MEFF` separate; confirm both in REP when task requires.

## Anti-patterns

- Inventing a non-existent `Pump HI` block type instead of configuring `PUMP`.
- Writing `set_pres` before `set_opt_spec`.
- Configuring a curve table while `OPT_SPEC` is still `PRES`.
- Configuring the curve before inlet/outlet streams are connected (curve unit tables are session-sensitive).

```

### FILE: aspen_agent_skills/guides/compr-analysis-variable-selection/SKILL.md
Reason: selected skill for task block family
```text
---
name: compr-analysis-variable-selection
description: &gt;-
  Selects Aspen COMPR block variables for native Design Spec, Sensitivity, and
  Optimization objects. Use when compressor work, power, pressure, pressure
  ratio, or two-stage/intercooled compression appears in DS/SA/OPT tasks.
---

# COMPR Analysis Variable Selection

This is a block-specific companion to the generic DS/SA/OPT skills. Keep the
analysis workflow generic, but use COMPR-specific variable tokens and coupling
rules when the sampled or manipulated object is a compressor.

## Work And Power Tokens

- For compressor work or power objectives, prefer the live COMPR option
  `IND-POWER` with an explicit unit such as `hp` when it is available.
- Do not guess `POWER` as the Optimization sampled variable. It may be accepted
  by raw table writes/readbacks but still fail to produce meaningful O1 output
  rows such as `FINAL_VAL\1`.
- If `IND-POWER` is not available, inspect `opt_prepare_block_var_options` /
  `opt_get_field_options` and choose a live compressor work token that produces
  non-status Optimization or Sensitivity output rows.

## Selected Pressure And Power Identity

Bind every selected numeric cell to its source row, object, variable token, actual exported/readback unit and physical role. A pressure axis (absolute/gauge pressure or pressure ratio) is not a compressor work column; indicated, brake and net power are distinct quantities. Never identify these roles by column position, field suffix, magnitude, or configured `helper-managed manipulated-variable field`/`helper-managed sampled-variable field` alone. Convert actual `AnnotatedQuantity` readbacks through `UNIT_REGISTRY`, keep unknown units unresolved, and replay the accepted manipulated pressure on its owning block with input verification. The final REP/BKP must agree with that selected row&#x27;s pressure and same-role work terms; summed power requires converted, compatible terms, not a mislabeled pressure value.

## Serial Compression Optimization

For a total-work or total-power objective across more than one compressor, build
the objective terms from the actual compressor sequence in the task/model. Do
not hardcode example block names or assume there are exactly two compressors.
Use expression-safe labels generated from the term order, and require readback
for every label referenced by the expression.

Use only the high-level multi-term Optimization helper for this pattern. Do not
write `helper-managed sampled-variable field*`, `helper-managed manipulated-variable field*`, `LOWER`, `UPPER`, `helper-managed analysis expression`, or Constraint rows with
low-level `configure_optimization_* helper` / `configure_optimization_* helper` calls from generated scripts. If
`configure_optimization_multi_block_var_objective(...)` returns `success=false`,
store its `repair_feedback` and `agent_instruction`, then stop before
`engine_run`.

```python
compressor_terms = [
    {&quot;label&quot;: f&quot;W{i}&quot;, &quot;block_name&quot;: block_name, &quot;variable&quot;: &quot;IND-POWER&quot;, &quot;uom&quot;: work_unit}
    for i, block_name in enumerate(serial_compressor_blocks, start=1)
]
optimization_config = safe.configure_optimization_multi_block_var_objective(
    client,
    optimization_name=&quot;OPT-COMP&quot;,
    objective_terms=compressor_terms,
    expression=&quot;+&quot;.join(term[&quot;label&quot;] for term in compressor_terms),
    vary_block=&lt;compressor_or_upstream_block_that_owns_the_decision&gt;,
    vary_variable=&lt;live_pressure_or_ratio_token&gt;,
    vary_uom=&lt;task_pressure_unit&gt;,
    lower=&lt;physically_valid_lower_bound&gt;,
    upper=&lt;physically_valid_upper_bound&gt;,
    constraints=[
        {
            &quot;constraint_name&quot;: f&quot;C{i}&quot;,
            &quot;type&quot;: &quot;block_var_bound&quot;,
            &quot;block_name&quot;: term[&quot;block_name&quot;],
            &quot;variable&quot;: term[&quot;variable&quot;],
            &quot;operator&quot;: &quot;GE&quot;,
            &quot;target&quot;: minimum_work_value,
            &quot;unit&quot;: work_unit,
            &quot;label&quot;: f&quot;C{i}&quot;,
        }
        for i, term in enumerate(compressor_terms, start=1)
    ] if minimum_work_value is not None else None,
    direction=&quot;MINIMIZE&quot;,
)
if not optimization_config.get(&quot;success&quot;):
    summary.setdefault(&quot;analysis_objects&quot;, {}).setdefault(&quot;optimization&quot;, {})[&quot;OPT-COMP&quot;] = optimization_config
    raise RuntimeError(&quot;compressor Optimization configuration failed; see repair_feedback&quot;)
final = safe.run_completion_engine_and_export(client, ...)
targets = [
    {
        &quot;request_id&quot;: &quot;opt_objective_total&quot;,
        &quot;kind&quot;: &quot;derived&quot;,
        &quot;object_name&quot;: &quot;OPT-COMP&quot;,
        &quot;quantity&quot;: &quot;optimization_objective&quot;,
        &quot;notes&quot;: &quot;FINAL OBJECTIVE FUNCTION VALUE from the native Optimization object&quot;,
    },
    {
        &quot;request_id&quot;: &quot;opt_manipulated_pres&quot;,
        &quot;kind&quot;: &quot;block&quot;,
        &quot;object_name&quot;: vary_block,
        &quot;quantity&quot;: &quot;outlet_pressure&quot;,
        &quot;notes&quot;: &quot;FINAL VALUE for manipulated pressure in MANIPULATED VARIABLES&quot;,
    },
]
for term in compressor_terms:
    targets.append(
        {
            &quot;request_id&quot;: f&quot;w_{term[&#x27;block_name&#x27;]}&quot;,
            &quot;kind&quot;: &quot;block&quot;,
            &quot;object_name&quot;: term[&quot;block_name&quot;],
            &quot;quantity&quot;: &quot;indicated_power&quot;,
            &quot;notes&quot;: f&quot;{term[&#x27;label&#x27;]} / IND-POWER from OPTIMIZATION sampled variables or COMPR block section&quot;,
        }
    )
    targets.extend(
        [
            {
                &quot;request_id&quot;: f&quot;{term[&#x27;block_name&#x27;]}_polytropic_method&quot;,
                &quot;kind&quot;: &quot;block&quot;,
                &quot;object_name&quot;: term[&quot;block_name&quot;],
                &quot;quantity&quot;: &quot;polytropic_method&quot;,
                &quot;notes&quot;: &quot;POLYTROPIC COMPRESSOR USING ... METHOD from COMPR INPUT DATA (e.g. ASME)&quot;,
            },
            {
                &quot;request_id&quot;: f&quot;{term[&#x27;block_name&#x27;]}_polytropic_efficiency&quot;,
                &quot;kind&quot;: &quot;block&quot;,
                &quot;object_name&quot;: term[&quot;block_name&quot;],
                &quot;quantity&quot;: &quot;polytropic_efficiency&quot;,
                &quot;notes&quot;: &quot;POLYTROPIC EFFICIENCY from COMPR INPUT DATA&quot;,
            },
            {
                &quot;request_id&quot;: f&quot;{term[&#x27;block_name&#x27;]}_mechanical_efficiency&quot;,
                &quot;kind&quot;: &quot;block&quot;,
                &quot;object_name&quot;: term[&quot;block_name&quot;],
                &quot;quantity&quot;: &quot;mechanical_efficiency&quot;,
                &quot;notes&quot;: &quot;MECHANICAL EFFICIENCY from COMPR INPUT DATA&quot;,
            },
        ]
    )
safe.finalize_task_summary_with_llm_rep_readback(
    summary,
    final_bundle=final,
    rep_readback_targets=targets,
    llm_rep_readback_artifact_dir=artifact_dir,
    readbacks={&quot;optimization_config&quot;: optimization_config},
)
```

If the task states a minimum allowable work/power for each compressor, represent
that as native Constraint rows linked to Optimization unless a live Constraint
probe proves the block-work variable cannot be constrained in this case. A
post-run readback check is useful supporting evidence, but it is not the same as
a constrained native Optimization.

Pass only when all of these hold:

- every label in the objective expression has successful `helper-managed sampled-variable field` and
  `helper-managed sampled-variable field` readback from the configure helper;
- any stated work/power lower bounds are configured as Constraint rows and
  linked through `CONID`, or the summary explicitly marks native constraint
  configuration unavailable;
- `rep_readback_evidence.parsed_sections` contains numeric objective total hp,
  each compressor work term, manipulated pressure, and COMPR polytropic method /
  polytropic efficiency / mechanical efficiency when the task specifies them.

Do not use `collect_optimization_results`; native tree `FINAL_VAL` rows are
status-only or ambiguous for multi-term objectives and are not scoreable evidence.

## Sensitivity Sweeps

When a Sensitivity object sweeps an intermediate compressor outlet or discharge
pressure and reads compression work:

| Role | Prefer | Avoid |
|------|--------|-------|
| **Vary** | COMPR pressure token, with helper unit selection/readback from the task pressure basis | A cooler/heater pressure unless the task explicitly varies that block |
| **Sampled objective** | COMPR work tokens on each relevant compressor, with helper unit selection/readback from the reporting basis | A heater duty or unrelated utility token as a proxy for compressor work |

Known COMPR work-style tokens are hyphenated; live options may include
`IND-POWER`, `BRAKE-POWER`, or `NET-WORK`. Prefer `IND-POWER` for native
Optimization work objectives when available, and verify Sensitivity output is
non-empty before reporting a trend.

For direct COMPR result readback in generated scripts, prefer
`safe.collect_compr_power_readback(client, block_name=&quot;CP&quot;, output_unit=&quot;W&quot;)`.
This helper tries native output leaves such as `IND_POWER`, `BRAKE_POWER`, and
`WNET`, then returns both `value` and `numeric_value`. Do not build custom
attempt rows that copy the successful Aspen payload under `payload.result.value`
while leaving the evidence row&#x27;s own `numeric_value` as `None`; validators treat
that as no numeric compressor power evidence.

```python
power = client.invoke(&quot;collect_compr_power_readback&quot;,  block_name=&quot;CP&quot;, output_unit=&quot;W&quot;)
summary.setdefault(&quot;results&quot;, {})[&quot;compressor_power&quot;] = power
checks.append({
    &quot;name&quot;: &quot;compressor_power_read_from_compr_output&quot;,
    &quot;passed&quot;: bool(power.get(&quot;success&quot;)),
    &quot;evidence&quot;: power,
})
```

## Pressure Coupling

When the Optimization varies the first compressor outlet pressure, any
intercooler/heater between compressor stages must preserve that pressure by
using zero pressure drop or a pressure-following setup. Do not fix the
intercooler outlet pressure to an analytic seed such as the equal-pressure-ratio
estimate; that decouples the second compressor from the manipulated variable.

If an intermediate pressure estimate is useful, use it only as a seed or bounds
hint. The reported optimum must come from native analysis output or final Aspen
readback after the analysis object has run.

```

### FILE: aspen_agent_skills/guides/aspen-custom-unit-set/SKILL.md
Reason: selected skill for task block family
```text
---
name: aspen-custom-unit-set
description: Creates and activates Aspen Plus custom or preset unit sets; routes INSET vs setter unit= correctly. Use when tasks need mixed display units, preset names like METCBAR, bar-scale block pressures, or any INSET outside the six built-in global tokens.
---

# Aspen Custom Unit Set

## Two failure classes (do not confuse them)

| Class | Symptom | Root cause | Fix |
|---|---|---|---|
| **A. INSET / unit-set routing** | `invalid_inset_value`, preset name missing, REP display units wrong | Wrong helper (`configure_inset_unit_system(&quot;METCBAR&quot;)`), set not created/activated | Paths below + `read_active_unit_set` |
| **B. Setter semantic unit** | Flash/RStoic runs but V/L wrong; RadFrac dry-up; absurd pump ΔP | Task/meta says **bar** but script writes **MPa** or omits `unit=` | **`unit=&quot;bar&quot;`** (or task token) on `set_pres` / `set_pres_mixed` — legal under **any** INSET |

Class B is **not** “Aspen blocks bar”. Live probes confirm `set_pres(..., unit=&quot;bar&quot;)` under SI/ENG/MET/METCBAR.

When history/REP shows **stage dry-up**, **zero upstream feed**, or **pump/compressor pressure ~1e18**, check Class B and INSET-switch hazards below — not only solver settings. See `aspen-completion-error-hints`.

## Three INSET paths

| Path | When | Helper |
|---|---|---|
| **Built-in globals** | Task accepts SI/ENG/MET only | `configure_inset_unit_system` or `ensure_session(..., inset=...)` |
| **Preset / saved names** | Unit set already under `Data\Setup\Units-Sets` (BKP or HTTP template) | `activate_custom_unit_set` |
| **New mixed sets** | Derive from ENG/SI and override Unit-Types | `configure_custom_unit_set` |

Built-in tokens for `configure_inset_unit_system`:

`ENG`, `ENGUS`, `MET`, `MET-CHEM`, `SI`, `SI-CHEM`

Any other INSET (`MX`, `METCBAR`, …) → **`activate_custom_unit_set`** or **`configure_custom_unit_set`** — not `configure_inset_unit_system(&quot;MX&quot;)` (`invalid_inset_value`).

Do **not** edit BKP files to inject unit sets.

## Default blank session (HTTP template)

Aspen HTTP loads `tasks/standards/template_with_metcbar.apt` by default (`ASPEN_DEFAULT_SESSION_TEMPLATE`; `=off` disables). Fresh sessions expose `Units-Sets\METCBAR` and **`INSET=METCBAR`**.

- **`ensure_session()`** without `inset=` → preserves template INSET.
- **`ensure_session(..., inset=&quot;SI&quot;)`** → intentional override.
- Match task/reference INSET; do not force METCBAR on every flowsheet.

## Choosing an INSET strategy

| Task shape | Recommended approach |
|---|---|
| Display/reporting only (METCBAR or custom MX) | Preserve template or activate/configure custom set; verify `unit_types` |
| **Bar-scale** Flash/RStoic specs **and** SI-validated equipment (pump curves, some legacy tables) | Prefer **`INSET=SI`** + explicit **`unit=&quot;bar&quot;`** on pressure setters — avoid METCBAR for the whole build then a late SI switch |
| Custom °C + mmHg on ENG base | `configure_custom_unit_set` → `MX` (works on template or built-in sessions) |
| Reference BKP at `INSET=METCBAR` | Load BKP; avoid global INSET rewrite unless task requires it |

## INSET switching hazard (mid-session)

**Verified:** Flash/RStoic `PRES` written with `unit=&quot;bar&quot;` under **METCBAR**, then global **`INSET` switched to SI** later (e.g. pump performance table), can **rescale stored block pressures** (e.g. `-0.05` → `-5000` in tree readback) and break downstream traffic.

Rules:

- Choose strategy from the table **before** bulk writes.
- If SI-only tables are required, use **SI throughout** with explicit `unit=&quot;bar&quot;` on pressures, **or** re-write bar pressures **after** the SI switch with `unit=&quot;bar&quot;`.
- After any INSET change, re-read Flash/RStoic/feed **`PRES`** before `engine_run`.

## Mixed unit set (typical: ENG base, °C + mmHg display)

```python
import script_agent_exp.safe_aspen_calls as safe

result = client.invoke(&quot;configure_custom_unit_set&quot;,
    unit_set_name=&quot;MX&quot;,
    base_set=&quot;ENG&quot;,
    quantity_units={&quot;TEMPERATURE&quot;: &quot;C&quot;, &quot;PRESSURE&quot;: &quot;mmHg&quot;},
    set_active=True,
)
safe.require_success(result, label=&quot;configure_custom_unit_set&quot;)

verified = client.invoke(&quot;verify_custom_unit_set&quot;,
    unit_set_name=&quot;MX&quot;,
    expected_temperature=&quot;C&quot;,
    expected_pressure=&quot;mmHg&quot;,
    require_active_inset=True,
)
```

Step-by-step equivalent:

```python
client.invoke(&quot;create_unit_set_from_base&quot;,  unit_set_name=&quot;MX&quot;, base_set=&quot;ENG&quot;)
client.invoke(&quot;set_unit_set_quantity&quot;,  unit_set_name=&quot;MX&quot;, quantity=&quot;TEMPERATURE&quot;, unit=&quot;C&quot;)
client.invoke(&quot;set_unit_set_quantity&quot;,  unit_set_name=&quot;MX&quot;, quantity=&quot;PRESSURE&quot;, unit=&quot;mmHg&quot;)
client.invoke(&quot;activate_custom_unit_set&quot;,  unit_set_name=&quot;MX&quot;)
bundle = client.invoke(&quot;read_active_unit_set&quot;,  unit_set_name=&quot;MX&quot;)
```

## Preset names (e.g. METCBAR)

Reference BKPs and the default HTTP template ship **`METCBAR`** (`Data\Setup\Units-Sets\METCBAR`, often `INSET=METCBAR`). It is **not** a built-in token for `configure_inset_unit_system`.

When the set exists in the live session:

```python
client.invoke(&quot;activate_custom_unit_set&quot;,  unit_set_name=&quot;METCBAR&quot;)
bundle = client.invoke(&quot;read_active_unit_set&quot;,  unit_set_name=&quot;METCBAR&quot;)
```

If `METCBAR` is absent (template disabled, old server): load a BKP that defines it, or use **`INSET=SI/MET`** with explicit **`unit=&quot;bar&quot;`** on pressure setters — process specs stay correct even when display defaults differ.

Other named sets use the same **activate** path when listed under `Units-Sets`.

## Writing pressure with `unit=&quot;bar&quot;` (INSET-independent)

**Verified:** `set_pres(..., unit=&quot;bar&quot;)` on Flash2 and RStoic under `INSET=SI`, `ENG`, `MET`, and template **METCBAR**.

| Fact | Detail |
|---|---|
| Legal setter tokens | `bar`, `bara`, `barg`, `MPa`, `kPa`, `psia`, `mmHg`, … on `set_pres` / `set_pres_mixed` |
| INSET independence | Pass **`unit=&quot;bar&quot;` explicitly**; INSET does not auto-pick setter units |
| Common mistake | Rewriting bar-scale targets as **`MPa`** (e.g. `-0.05 bar` → `2.15 MPa`) — ~40× error |
| Negative absolute bar | On Flash2/RStoic with **absolute** bar units, **negative value = pressure drop** (near-atmospheric specs) |

```python
# Near-atmospheric flash (meta often PRES = -0.05 bar)
client.invoke(&quot;set_spec_opt&quot;, block_name=&quot;F&quot;, value=&quot;TP&quot;)
client.invoke(&quot;set_temp&quot;, block_name=&quot;F&quot;, value=50.0, unit=&quot;C&quot;)
client.invoke(&quot;set_pres&quot;, block_name=&quot;F&quot;, value=-0.05, unit=&quot;bar&quot;)

# Reactor flash (meta often PRES = -0.1 bar)
client.invoke(&quot;set_spec_opt&quot;, block_name=&quot;R&quot;, value=&quot;TP&quot;)
client.invoke(&quot;set_temp&quot;, block_name=&quot;R&quot;, value=200.0, unit=&quot;C&quot;)
client.invoke(&quot;set_pres&quot;, block_name=&quot;R&quot;, value=-0.1, unit=&quot;bar&quot;)
```

Readback may show another display label (e.g. `psia`) while the numeric matches the bar write — trust **setter + task unit**, not REP label alone.

See also block-type inject `flash2.md` / `rstoic.md` and `flash-control-chain`.

## HTTP operations (Aspen server COM)

| Operation | Purpose |
|---|---|
| `unitset_create_from_base` | Create custom set from ENG/SI/etc. |
| `unitset_set_quantity` | Set one Unit-Type row |
| `unitset_activate` | Activate custom/preset set on INSET |
| `unitset_read` | Read Unit-Types and Input metadata |

## Verification checklist

- `read_active_unit_set` → `active_inset` matches intent
- `unit_types.TEMPERATURE` / `unit_types.PRESSURE` match task when overridden
- Critical **`PRES`** readback after any INSET change (Flash/RStoic/feeds)
- REP display units align after trusted run
- Convergence **does not** prove unit-set or pressure-basis correctness

## Live probes (Aspen HTTP at `http://127.0.0.1:5000/health`)

```bash
# Full reform suite (quick: skip heavy ch91 build)
python tool_side_generation/healthcheck/unit_set_reform_experiment.py
python tool_side_generation/healthcheck/unit_set_reform_experiment.py --skip-heavy

python tool_side_generation/healthcheck/bar_pressure_write_probe.py
python tool_side_generation/healthcheck/metcbar_fresh_session_probe.py
python tool_side_generation/healthcheck/full_evaluation/custom_unit_set_probe.py --fresh --unit-set-name MX

# Mixed flowsheet: SI inset + bar PRES + partial-V RDV (regression)
python tool_side_generation/healthcheck/ch91_unit_set_reform_probe.py --si-inset
```

```

### FILE: aspen_agent_skills/guides/solvent-recycle-closure-semantics/SKILL.md
Reason: selected skill for task block family
```text
---
name: solvent-recycle-closure-semantics
description: &gt;-
  Distinguishes process accounting closure from numerical recycle-tear closure for
  solvent recovery, makeup, and auxiliary-feed tasks. Use when a task has solvent
  recycle, recovery bottoms, makeup streams, fixed circulation targets, calculator
  closure, or mixer-plus-recycle topology that may be declared rather than physically
  looped back to an upstream unit.
---

# Solvent Recycle Closure Semantics

## Core Principle

When a task involves **solvent recycle**, **recovery bottoms**, **makeup streams**, or **fixed auxiliary-feed targets**, do **not** automatically convert the recovered stream into a live upstream feed.

For split-task continuation flowsheets, this is a hard first-pass rule:

- If an upstream node has already selected a fixed solvent/auxiliary circulation amount, keep that upstream feed specification as the protected design contract.
- If the recovery column bottoms are a solvent-rich candidate recycle stream, first close the process by **accounting/declaration**: report recovered solvent, fresh makeup required to maintain the protected feed target, and final product/recycle purity evidence.
- Do **not** build a physical `recovery bottoms -&gt; mixer -&gt; upstream column feed` tear loop on the first pass merely because the task says &quot;connect&quot;, &quot;recycle&quot;, or &quot;return&quot;. In this skill, those words are process-intent words until a reference model or explicit task requirement proves a numerical tear is required.
- A physical tear loop that destabilizes a previously converged open-loop design is a topology-semantics failure, not a reason to keep tuning RadFrac specs blindly.

First distinguish:

| Closure type | Meaning | Typical Aspen pattern |
|--------------|---------|----------------------|
| **Process accounting closure** | Material balance is closed by a declared feed target plus makeup/recovery accounting | Fixed solvent feed (`S=120`), calculator for makeup, mixer outlet **not** wired back to upstream column |
| **Numerical recycle-tear closure** | A physical recycle loop is torn and solved by Wegstein/Broyden | Mixer outlet → upstream unit feed, explicit tear stream, circulation solved iteratively |

Both can be chemically valid. Pick the one the **task wording** and any **verified reference model** actually require.

Use a strict machine-readable enum in generated evidence:

- `closure_semantics.closure_type = &quot;process_accounting&quot;`
- `closure_semantics.closure_type = &quot;numerical_recycle_tear&quot;`

Do not invent hybrid closure types such as &quot;accounting-first physical recycle&quot;. If a mixer outlet feeds an upstream unit, classify it as `numerical_recycle_tear` and prove the physical-tear prerequisites. If recovered material and makeup are only reported against a protected upstream target, classify it as `process_accounting`.

## Makeup Feed Semantics

A **makeup feed** is an external compensating feed that replaces material lost from the process through products, purge, vents, or waste streams. It is not, by itself, evidence that Aspen must solve a numerical recycle tear.

When a task says &quot;provide a makeup feed&quot;, &quot;make up losses&quot;, or &quot;account for losses&quot;:

- Treat the makeup stream as a **loss-accounting handle** unless the task explicitly says the recovered stream replaces the protected upstream feed.
- Preserve any upstream fixed solvent/auxiliary circulation target as the primary feed contract; compute or report makeup as the difference between that protected target and recovered solvent plus outlet losses.
- Do not use the makeup stream as a reason to convert a previously fixed solvent feed into a mixer outlet that must be torn back to the upstream unit.
- If the task asks for losses &quot;from each column&quot; or &quot;from each outlet&quot;, report per-column/per-outlet loss evidence and the makeup formula. This is stronger evidence for process accounting than for physical tear topology.
- A physical recycle tear still needs independent evidence: a reference topology, explicit numerical recycle convergence requirement, tear stream, purge/circulation policy, and stable initialization basis.

## Required Decision Order

1. **Read the task for a fixed circulation or auxiliary-feed target.**
   If an upstream step already established a target amount (for example a fixed solvent, carrier, or auxiliary-feed circulation rate), preserve that target as the upstream feed specification unless the task explicitly says the recovered stream replaces it.

2. **Check whether recycle is physical or declarative.**
   Before wiring `recovery bottoms → mixer outlet → upstream feed`, verify the intended semantics:
   - Does the reference BKP/APW show the mixer outlet feeding the upstream unit?
   - Or does the upstream unit take a **fixed makeup/solvent stream** while recovery + calculator only close losses?

3. **Use calculator/makeup for losses, not as a substitute for wrong topology.**
   A calculator that sets makeup from a recovery stream is compatible with **accounting closure**. It does **not** prove that a physical recycle edge (`MX.P(OUT) → D1.F(IN)`) is required.

4. **Build a physical recycle loop only when all of these are identified:**
   - explicit task or verified reference evidence that a numerical tear is required
   - tear stream
   - controlled circulation target or purge policy
   - makeup degree of freedom
   - stable initialization basis (open-loop or seeded tear guess)

If any item is missing, use accounting closure and record the missing physical-tear prerequisites as `physical_recycle_not_attempted_reason` or `physical_recycle_deferred_reason`.

## Topology Rules

### Prefer accounting closure when

- The task states a **fixed** solvent/auxiliary feed rate to the upstream unit.
- A prior subtask/handoff fixed the circulation amount and the current subtask only closes recovery + makeup.
- Reference BKP shows upstream feed as a standalone stream, with mixer/recovery branches **not** returning to that feed port.
- Repeated physical recycle attempts produce `mass balance`, `$OLVER01`, or Wegstein failures while fixed-feed + calculator variants converge.
- The upstream open-loop recovery column already proves a solvent- or auxiliary-rich recovery stream and the remaining duty is loss accounting plus makeup reporting.
- The proposed physical loop would feed a solvent-rich stream into a column spec basis that was selected for a fixed auxiliary feed, causing RadFrac mass-balance or column-spec errors.

### Prefer physical recycle when

- The task explicitly requires a **numerical recycle-tear convergence** result, not just process recycle accounting.
- Reference BKP/APW shows the mixer outlet connected to the upstream unit feed port.
- The acceptance target is recycle purity/flow after tear convergence, not a declared fixed circulation alone.
- A stable initialization basis is available and the loop does not invalidate protected upstream column specs.

Plain words such as &quot;connect bottoms&quot;, &quot;return recycle&quot;, or &quot;provide makeup&quot; are not enough by themselves to prefer physical recycle when a fixed upstream solvent target already exists.

## Wiring Checklist

Before first `engine_run`:

1. Write the material edge plan and name each stream&#x27;s **functional role** (fresh feed, fixed solvent, recovery bottoms, makeup, tear, product).
2. Confirm which edges are **physical** vs **accounting-only**.
3. If using accounting closure:
   - keep the fixed upstream feed stream on the upstream unit
   - route recovery to mixer/product/makeup as required
   - do **not** add `mixer outlet → upstream feed` just because a recycle concept exists in the task text
   - record a top-level `closure_semantics` object in `summary.json`:
     - `closure_type: &quot;process_accounting&quot;`
     - protected upstream solvent/feed target and unit
     - recovered solvent stream flow/composition
     - fresh makeup amount and formula
     - statement that physical tear closure was not required or was deferred
   - include APW/REP evidence from the converged accounting-closure run
4. If using physical recycle:
   - set `closure_semantics.closure_type: &quot;numerical_recycle_tear&quot;`; never use a hybrid closure type
   - record `physical_tear_prerequisites` with explicit evidence for task/reference requirement, tear stream, circulation or purge policy, makeup degree of freedom, and stable initialization basis
   - record `missing_physical_tear_prerequisites` as an empty list only when all prerequisites are actually satisfied
   - connect the tear loop completely before run
   - seed tear stream and makeup consistently
   - verify `list_block_ports` readback matches the intended loop
   - if the first run fails with RadFrac mass-balance or `$OLVER01`, stop widening numeric specs and pivot back to accounting closure unless the task explicitly requires numerical tear convergence

## Probe / Repair Guidance

When RadFrac or recycle loops fail to converge:

- Treat **topology semantics** as an L0 axis alongside pressure (`PRES1`/`PRES2`), feed stage, and feed convention.
- If physical recycle fails but fixed-feed + makeup converges, pivot to accounting closure before widening numeric search.
- Record in `summary.json` which closure type was chosen and the port readback that proves it.

## Continuation Pattern

For staged flowsheet tasks where an earlier step fixes an auxiliary, solvent, or carrier circulation target and a later step adds recovery or makeup accounting:

1. Treat the earlier selected circulation/feed amount as a protected upstream design contract unless the task explicitly reopens that decision.
2. Treat the recovered stream as a candidate source of material for inventory accounting before treating it as a mandatory live tear stream.
3. First preserve the protected upstream feed target and compute/report:
   - recovered material from the downstream recovery stream,
   - fresh makeup needed to maintain the protected target or replace measured outlet losses,
   - product/recycle purity evidence on the chosen accounting basis.

Only after this declared/accounting closure is complete should a numerical tear loop be attempted, and only if the task or verified reference model explicitly requires it.

## Related Skills

- `radfrac-extractive-distillation-solvent` — column roles and extractive/recovery column pairing
- `optimization-constrained-feed-and-recycle-evidence` — optimum feed + recycle evidence after topology is correct
- `shared-material-port-topology` — shared `F(IN)` wiring when multiple feeds are real
- `functional-role-semantics-validation` — prove stream roles before tuning

## Generic Rule (English)

When a task involves solvent recycle, recovery bottoms, or makeup streams, do not automatically convert the recovery stream into a live upstream feed. First distinguish between **process accounting closure** and **numerical recycle-tear closure**. If an upstream design step has already established a target circulation rate or auxiliary-feed amount, preserve that feed target and use the recovered stream plus makeup calculation to close the material balance unless the task or verified reference model clearly shows the mixer outlet feeding back into the upstream unit and a numerical tear convergence result is required. A physical recycle loop should only be built after identifying the tear stream, controlled circulation target, makeup degree of freedom, and stable initialization basis; otherwise record accounting closure evidence and defer physical tear closure.

```

### FILE: aspen_agent_skills/guides/radfrac-extractive-distillation-solvent/SKILL.md
Reason: selected skill for task block family
```text
---
name: radfrac-extractive-distillation-solvent
description: Guides RadFrac extractive-distillation and solvent-recovery flowsheets. Use when a task mentions extractive distillation, auxiliary solvent/feed, solvent recycle, makeup solvent, purity targets, or two-column solvent recovery.
---

# RadFrac Extractive Distillation Solvent

## Core Semantics

Extractive distillation is not just two ordinary columns. The solvent must be a functional feed to the extractive column, and the solvent recovery column must return a solvent-rich bottoms stream.

Validate these roles before numeric tuning:

1. The hydrocarbon feed and solvent/feed-recycle streams are distinct material feeds to the first column.
2. The solvent feed enters the extractive column at an appropriate stage above or near the hydrocarbon feed, not only as an unconnected stream object.
3. The first column has distinct top and bottom product roles, but do not infer
   the target hydrocarbon solely from `overhead`, `distillate`, `bottoms`, or
   stream names. Map product roles from the task/PFD and confirm them with
   component readbacks.
4. If a second solvent-recovery column is required, its recovered-product and
   solvent-rich recycle roles must likewise be proved from readbacks, not from
   outlet labels alone.
5. If the recovery bottoms is recycled to the first column, add a makeup solvent stream for losses and avoid pretending recycle exists when topology is absent.
6. Before wiring recovery bottoms or mixer outlet back to an upstream feed, read `solvent-recycle-closure-semantics`: distinguish **process accounting closure** (fixed upstream feed + makeup) from **numerical recycle-tear closure** (physical loop).

## Helper Pattern

Prefer `configure_radfrac_extractive_distillation_pair(...)` for the two native
RadFrac columns. The helper now uses role-based RadFrac topology:

- multiple extractive-column feeds, such as hydrocarbon feed plus solvent, may
  share the live `F(IN)` material feed port;
- distillate/top-product streams are connected to distillate/top-product
  ports such as `LD(OUT)` / `D(OUT)` rather than invented `P(OUT)` ports;
- solvent-rich bottoms/intermediate streams are connected to `B(OUT)`;
- feed-stage specs are still separate Aspen inputs and must be written for each
  feed stream after the physical connections exist.

Do not fall back to manual `P(OUT)` product wiring for RadFrac when this helper
fails. First inspect `list_block_ports(...)`; a single `F(IN)` with
`LD(OUT)`/`B(OUT)` is normal RadFrac topology, not evidence that the flowsheet
needs a different block family.

## Validation

Do not accept convergence alone. Check product roles:

- first-column top and bottom product compositions match their intended roles
- second-column recovered-product and solvent-recycle compositions match their intended roles, when a recovery column is present
- solvent-rich recycle/return streams are actually solvent-rich
- solvent/feed/recycle streams are connected to material feed ports and have feed-stage specs

If product purities look like a simple hydrocarbon split and solvent stays absent from the relevant products, repair solvent feed/recycle topology and feed-stage assignment before changing reflux ratios.

During exploration, do not treat stream names or initial role labels as fixed
truth. Read both hydrocarbon components in the first-column distillate and
bottoms (and solvent in the bottoms) for every candidate row. If increasing
solvent, reflux, stages, or feed-stage changes consistently make the declared
product stream leaner in the named target while the opposite outlet becomes
richer, pivot to product-role remapping before widening the same numeric search.
For example, an extractive column may send the solvent-associated hydrocarbon to
the bottoms with solvent; a low top-stream mole fraction can be a role-mapping
signal rather than proof that the candidate is infeasible.

## Sensitivity Response Semantics

For first-column extractive distillation with an auxiliary solvent/feed stream
(or a solvent circulation stream), the solvent flow is a causal separation
handle, not just another feed amount:

- Increasing solvent circulation/feed to the extractive column usually changes
  relative volatility/selectivity and should improve the target hydrocarbon
  product purity until diminishing returns appear.
- The response should be measured on the physical stream/block role named by the
  task, not on a surrogate stream label. If the task asks for a solvent-amount
  study, a valid native Sensitivity should vary the solvent stream `MOLE-FLOW`
  and sample responses that map to the stated objective, constraints, and
  tradeoffs.
- Include a cost/load or operating-burden response when the task implies a
  tradeoff, not only a quality response. Extra solvent, reflux, stages, or feed
  relocation can trade separation quality against utility load, equipment
  burden, flowrate, or convergence margin. A flat or physically implausible
  trend is a warning that the response role, feed stage, manipulated range, or
  units are wrong.
- Stage count and feed locations are structural design handles. Solvent feed
  should enter above or near the hydrocarbon feed so it can alter the liquid
  phase through the rectifying/extractive region. If the problem asks to select
  stages or feed locations, do not report fixed constants as an optimum; vary or
  justify those structural handles with Aspen-backed evidence.
- For exploratory probe matrices, use decoupled sparse axes rather than tied
  bundles where solvent flow, stages, feed locations, and reflux all increase
  together. Prefer a broad multi-variable matrix under about 1000 rows that can
  reveal basic trends, then let the validator judge product roles and optimum
  from the fact table.
- A native SA table alone does not prove an optimum. The selected solvent amount
  must be chosen from a stated objective/constraint basis (for example minimum
  solvent satisfying product purity, or a purity/duty tradeoff), then reapplied
  in a final converged run with REP/APW evidence.

Unit trap: Aspen&#x27;s native Sensitivity CSV/REP may export stream flow rows in a
default reporting basis that differs from the configured `helper-managed manipulated-variable field`. Preserve
raw rows, but normalize the semantic decision table back to the configured or
read-back unit before comparing with task values.

## Completion Before Analysis

For extractive-distillation optimization tasks, the base flowsheet is not ready
for native Optimization until the recycle/makeup topology and both columns are
input-complete:

- The solvent makeup/recycle mixer should use shared material ports when Aspen
  exposes one `F(IN)` and one `P(OUT)`; do not connect recycle material to
  `WS(IN)` or other utility ports.
- Required blocks should include the mixer and both RadFrac columns in
  `run_completion_engine_and_export(..., required_blocks=[...])`.
- If completion flags mixer `M1`, valve `V1`, or RadFrac `D1`/`D2` incomplete,
  record the completion payload and repair the missing topology/spec before
  creating Optimization. Optimization evidence is meaningless when the base
  extractive/recovery loop has not run once with trusted REP/APW evidence.

## Recycle, Tear, And Makeup Semantics

For solvent-recovery extractive distillation, distinguish these three roles:

- **Solvent circulation/feed to the extractive column**: the stream whose flow
  determines the solvent-to-feed ratio and separation behavior in the first
  column.
- **Recovered solvent recycle**: the solvent-rich bottoms from the recovery
  column.
- **Makeup solvent**: the fresh solvent required to replace solvent losses in
  product streams or purge/loss routes.

Do not treat fixed makeup flow as interchangeable with the circulating solvent
feed. Makeup is usually an inventory-closure variable, not the primary
solvent-circulation decision. A large fixed makeup stream added to recovered
recycle can over-specify or accumulate solvent in the loop and make recycle
convergence fragile.

When closing a solvent recycle loop, prefer this reasoning order:

1. Prove the extractive column can run open-loop with a real solvent feed.
2. Prove the recovery column can run open-loop from the first-column bottoms.
3. Close the loop by identifying the logical circulation stream and makeup stream.
4. Balance makeup against solvent losses or against a target solvent
   circulation, rather than guessing makeup as the total solvent feed.
5. Only then optimize product purities or minimum solvent amount.

Common valid patterns include:

- The extractive-column solvent feed is the logical circulation stream. The
  recovery bottoms and makeup stream are mixed downstream, and Aspen&#x27;s
  convergence system closes the loop. A standard solved case may leave the
  explicit Tear Streams table empty, relying on automatic sequencing plus
  convergence options instead of a manually listed tear stream.
- Some valid Aspen examples model solvent recycle as an accounting closure
  rather than a physically wired material loop. In that pattern, the extractive
  column receives a circulation/tear feed stream, while the recovered solvent
  and fresh makeup enter a downstream mixer whose outlet is used for balance
  evidence but is not necessarily wired back to the extractive-column inlet.
  Do not &quot;repair&quot; this by forcing the mixer outlet into the column if the
  standard topology or task diagram shows a separate circulation feed plus a
  makeup/recovery mixer.
- A calculator, design spec, or equivalent inventory-balance relation computes
  makeup from recovered solvent and the desired circulation or losses. For
  example, conceptually: `makeup = target_circulation - recovered_solvent`.
- When using the script-agent helper surface, prefer
  `configure_calculator_stream_component_makeup_balance(...)` for this
  Calculator pattern and `configure_recycle_convergence_options(...)` for
  global tear/convergence settings. These helpers preserve the semantic
  distinction between circulation, recovered recycle, and makeup better than
  raw `typed helper write surface` writes.
- A purge/loss route is explicit, and makeup compensates that measured loss.

Common invalid or high-risk patterns:

- Replacing the circulating solvent feed with a fixed makeup stream and then
  calling that value the optimum solvent amount.
- Adding recovered recycle plus an arbitrary fixed makeup flow directly into the
  first column without controlling total solvent circulation.
- Reporting open-loop solvent sweep results as closed-loop recycle evidence.
- Repairing recycle nonconvergence by changing already-converged column
  topology/specs before checking circulation/makeup balance, convergence
  options, and recycle initialization.

Treat recycle convergence as a separate model-structure gate from product
purity. Nonconverged recycle rows may still diagnose tear/makeup problems, but
their product purities should not be used as final target evidence.

## Task-text naming traps

When feed prose and product gates use inconsistent component names, record the
mapping in assumptions and keep feeds/products/reactions consistent. This does
not change the optimization decision: manipulate the task-stated auxiliary
solvent/feed handle, with purities enforced by native Optimization constraints,
Sensitivity result gates, or final REP evidence as requested. Do not add an
extra policy Design Spec on column reflux unless the task explicitly asks for
Design Spec.

```

### FILE: aspen_agent_skills/guides/optimization-constrained-feed-and-recycle-evidence/SKILL.md
Reason: selected skill for task block family
```text
---
name: optimization-constrained-feed-and-recycle-evidence
description: &gt;-
  Closes the gap between native Aspen Optimization setup and scoreable optimum/recycle
  evidence. Use when O1 lands on STREAM-VAR but FINAL_VAL contradicts reported design
  inputs, bare MINIMIZE feed hits lower bound without purity constraints, recycle/makeup
  is added post-run without a converged REP, or G2 fails on optimum amount plus completed
  recycle loop semantics (extractive distillation, solvent recovery, auxiliary feed tasks).
---

# Optimization: Constrained Feed Decisions and Recycle Evidence

## What this skill fixes

Three generic failure modes (not case-specific):

1. **Unconstrained feed minimization** — O1 MINIMIZE stream MOLE-FLOW with no CON/DS purity rows → optimizer drives feed to lower bound (`FINAL_VAL≈0`) while the answer still cites a seed like `100 kmol/hr`.
2. **Decision/evidence split** — `selected_design` / `answer.md` reads from hardcoded `DESIGN_INPUTS`, not from O1 output or post-run stream readback.
3. **Post-run recycle proof** — mixer/makeup/recycle streams wired **after** the converged REP export; score treats part (c) as unsolved.

Apply this skill **after** manipulated-variable selection (`aspen_agent_skills/guides/optimization-manipulated-variable-selection/SKILL.md`) and **with** analysis finalization (`aspen_agent_skills/guides/analysis-tools-single-pass-finalization/SKILL.md`).

---

## Execution order (mandatory for optimum + recycle tasks)

```
1. Components + property method
2. Build **closed** material topology (including recycle + makeup **before** first real run)
3. Seed all feeds to input-complete (manipulated streams inside O1/DS bounds)
4. Configure Design Spec / Optimization (complete pairs + constraints)
5. engine_run on the **same** flowsheet topology
6. Export REP/APW from that final run
7. Populate results ONLY from step 5–6 readbacks / analysis output
```

**Never** export base-case REP, then append recycle edges, then claim the recycle loop converged.

---

## O1 formulation: minimum feed with specs

When the task asks for *optimum / minimum / best amount* of an **auxiliary, solvent, or makeup feed**:

| Layer | Rule |
|-------|------|
| Manipulated | STREAM-VAR on the owning feed stream (`F2`, `SF1`, `MU1`, …) — see optimization-manipulated-variable-selection |
| Objective | Minimize that stream&#x27;s mole-flow or mass-flow through the constrained stream-feed Optimization helper |
| Constraints | **Required** unless the task explicitly has no purity/spec gate — otherwise the solver only finds the lower bound |
| Reported optimum | From LLM REP readback on optimized stream/block after final run — **not** the initial seed |

The selected O1 value must be provenance-backed: preserve
`rep_readback_evidence.parsed_sections` for the manipulated stream/block and
report `request_id`, `normalized_value`, `unit`, and `source_section`. A seed
flow, makeup-closure iterate, or configure readback alone is not the part (a)
auxiliary/solvent optimum unless the role contract says that is the requested
decision.

### Constraint strategies (pick one coherent path)

**A. Optimization CON rows (preferred when HTTP path is available)**

- Add native **Constraint** objects (`C1`, `C2`, …) for each purity/spec the task states.
- Link them into Optimization through the high-level constraint/Optimization helper payload.
- Use **`configure_constraint_stream_composition_ge`** / composite **`configure_optimization_constrained_stream_var_minimize_flow`** for stream purity ≥ targets.
- **Tree caveat (verified):** Use the high-level stream-composition constraint helper for purity rows; do not hand-code purity rows as generic stream-variable entries, which exposes the wrong variable family and rejects fraction tokens.
- Do not treat object creation plus bare MINIMIZE as complete when CON rows are empty.

**B. Design Spec + Optimization split**

- DS holds purity/feasibility (e.g. product MCH mole fraction ≥ 0.95 by varying a column DOF or feed).
- O1 minimizes auxiliary feed **after** DS surface is legal, or O1 manipulates feed while DS holds a product spec.
- Both must participate in the **same** final `engine_run` evidence session.

**C. Sensitivity minimum search (fallback only)**

- Sweep feed flow; select the **lowest** feed with all purity checks passing in structured SA/REP output.
- Still report `decision_basis` from SA rows.
- **If the gate contract requires native Optimization, do not substitute SA or a manual grid as the reported optimum.** Use SA only as a diagnostic when native OPT output is empty or status-only.

### Auxiliary feed vs makeup (extractive distillation)

| Decision | Typical stream | Role |
|----------|----------------|------|
| Part (a) optimum phenol/solvent **auxiliary feed to Dist1** | `F2`, `SF1`, combined solvent feed before Dist1 | **O1 manipulated variable** for the task decision |
| Recycle-loop **makeup** after losses | `MU1`, `MK1`, … | Closes phenol inventory in part (c); **not** a substitute for part (a) when native Optimization is required |

Do not report a fixed-point makeup iteration result as the part (a) optimum unless optimization output and stream readbacks prove the same decision surface.

### Anti-pattern

```
MINIMIZE F2 MOLE-FLOW, vary F2, bounds 20–250, no CON/DS  →  FINAL_VAL ≈ lower bound
answer.md: &quot;optimum phenol = 100 kmol/hr (design input)&quot;     →  G2 FAIL
```

### Required readbacks after O1

- helper readback identifies the intended feed stream
- helper readback identifies stream-flow minimization with the task direction
- Manipulated final value inside `[LOWER, UPPER]` **and** consistent with `summary.results.selected_*` or `rep_readback_evidence`
- `rep_readback_evidence` contains optimized feed flow and purity gates with `found: yes`

Use `configure_optimization_stream_var_minimize_flow` / `configure_optimization_stream_var` for HTTP landing; omit nonexistent active leaves from strict helper success checks.

- For constrained O1 on feed minimization with product/recycle purities:

```python
configure_optimization_constrained_stream_var_minimize_flow(
    client,
    optimization_name=&quot;O1&quot;,
    objective_stream=&quot;&lt;auxiliary_or_solvent_feed&gt;&quot;,
    purity_constraints=[
        {
            &quot;constraint_name&quot;: &quot;C1&quot;,
            &quot;stream_name&quot;: &quot;&lt;product_or_recycle_stream&gt;&quot;,
            &quot;component_name&quot;: &quot;&lt;key_component&gt;&quot;,
            &quot;lower_bound&quot;: 0.95,
        },
    ],
    lower=&lt;lower_bound&gt;,
    upper=&lt;upper_bound&gt;,
    step_size=&lt;step_size&gt;,
    max_step_size=&lt;max_step_size&gt;,
    vary_uom=&quot;kmol/hr&quot;,
    fvn_uom=&quot;kmol/hr&quot;,
)
final = run_completion_engine_and_export(...)
targets = [
    {
        &quot;request_id&quot;: &quot;opt_feed_flow&quot;,
        &quot;kind&quot;: &quot;stream&quot;,
        &quot;object_name&quot;: &quot;&lt;auxiliary_or_solvent_feed&gt;&quot;,
        &quot;quantity&quot;: &quot;total_flow&quot;,
        &quot;notes&quot;: &quot;Optimized manipulated feed flow from MANIPULATED VARIABLES or stream table&quot;,
    },
    {&quot;request_id&quot;: &quot;gate_1_purity&quot;, &quot;kind&quot;: &quot;stream&quot;, &quot;object_name&quot;: &quot;&lt;stream&gt;&quot;, &quot;quantity&quot;: &quot;component_flow&quot;, &quot;component&quot;: &quot;&lt;cid&gt;&quot;},
]
safe.finalize_task_summary_with_llm_rep_readback(
    summary,
    final_bundle=final,
    rep_readback_targets=targets,
    llm_rep_readback_artifact_dir=artifact_dir,
)
```

Before any constraint configuration, call **`list_constraint_recipes(block_types=[...], task_keywords=[&quot;purity&quot;])`** and use recipe **`stream_mole_fraction_ge`** through the helper route; do not hand-code purity rows.

---

## Recycle / makeup: integrated topology

When the task requires *connect bottoms/recycle back to the column*, *makeup for losses*, or *execute until convergence*:

### Build in-loop (generic pattern)

```
column-2 bottoms (recycle stream RC*) ──┐
makeup stream (MU*) ────────────────────┼──► mixer (MX*) ──► solvent/aux feed (SF*) ──► column-1
fresh process feed (F*) ───────────────────────────────────► column-1 (separate port)
```

- Name streams/blocks from the task; roles are **recycle**, **makeup**, **mixed solvent feed**, **fresh feed**.
- Do **not** use a parallel `F2` direct feed **and** a recycle loop that only exists after REP export unless the task explicitly allows open-loop + proof.

### Closing makeup balance

If native recycle convergence is fragile:

1. Run fixed-point iteration on makeup phenol/solvent flow: `makeup_{k+1} = damp * losses_k + (1-damp) * makeup_k` from product-stream loss readbacks in REP.
2. Each iteration: set makeup flow → `engine_run` → parse REP → update makeup.
3. Final REP must come from the **last** iteration on the **closed** topology.

Recycle-closure pattern only (not a scoreable native Optimization substitute): fixed-point makeup iteration on the makeup stream after a converged recycle loop. Use this for part (c) inventory closure, not as the part (a) optimum when the gate contract requires native Optimization.

### Post-run topology proof is not enough

Patterns that score agents reject:

- `create_recycle_proof_topology` after `export_rep`
- Connecting `S1 → M1 → R1 → D1` only in calls.jsonl with no post-connection `engine_run`
- Asserting recycle purity from `S1` while products were computed on an open-loop model

---

## Results and summary.json alignment

Before marking success:

| Field | Must come from |
|-------|----------------|
| `results.selected_design.*_kmol_hr` (feed/makeup) | LLM REP `rep_readback_targets` on the optimized stream after final run |
| `results.decision_basis` | Explicit: `rep_readback_evidence`, converged Design Spec manipulated readback, Sensitivity row selection, etc. |
| `results.result_source_contract` | `rep_readback_evidence`, `native_sensitivity_selected_row`, `design_spec_manipulated_readback`, or explicit infeasibility |
| `optimization_decision_contract.*` | Requested role, optimized role, final reported role, and `role_match` |
| `task_spec_inputs` / `actual_model_inputs` | Task-given fixed inputs and the actual values used in the final evidence run |
| `results.result_source` | `current REP evidence` on the **final** topology |
| `validation_contract` check `optimization_result_used_for_decision` | true only if REP readback or optimized stream readback drove the number |

**Hard rule:** If O1 reports `1e-5` and design input says `100`, fix formulation or reporting — do not ship both.

---

## Checklist (copy before finalize)

```
Recycle/makeup
- [ ] Recycle + makeup + mixer wired before final engine_run
- [ ] Final REP exported after closed-loop topology run (PER_ERROR=0 if claimed)
- [ ] Makeup/recycle purities read via `rep_readback_targets` + LLM REP on final closed-loop REP (not deterministic REP parsers)

Optimization
- [ ] Manipulated stream matches task decision (STREAM-VAR readback)
- [ ] At least one purity/spec constraint active (CON or DS), unless task has none
- [ ] Reported optimum equals REP/DS/SA/fixed-point evidence, not DESIGN_INPUTS seed
- [ ] `rep_readback_evidence`: optimized feed/manipulated + objective documented with `found: yes`

Evidence
- [ ] No &quot;post-run proof only&quot; language in final answer without a converged rerun
- [ ] analysis_objects.optimization.success reflects readbacks + usable output, not object creation alone
```

---

## Related helpers and skills

- `configure_optimization_constrained_stream_var_minimize_flow` — CON purity rows + O1 MINIMIZE + CONID link (composite)
- `configure_constraint_stream_composition_ge`, `link_optimization_constraints`
- `collect_llm_rep_readback_evidence`, `finalize_task_summary_with_llm_rep_readback` — **final scored** stream purity/flow/objective from full `.rep`
- `configure_optimization_stream_var_minimize_flow`, `configure_optimization_stream_var`
- `configure_optimization_block_var_with_options` (column DOF objectives/constraints)
- `configure_design_spec_stream_var_vs_stream_var`, `ds_configure_stream_massfrac_vs_stream_massflow`
- `collect_sensitivity_decision_results`
- `run_standard_probe_matrix`, `read_stream_output` — **probe/scaffold per-row only** (not final OPT scoring)
- Skills: `optimization-manipulated-variable-selection`, `analysis-tools-single-pass-finalization`, `design-spec-manipulated-surface-selection`, `flowsheet-topology-ui-next-completion`, `evidence-finalization-tools`, `stream-output-readback`, `probe-sweep-decision-readback`

---

## Workshop-style example (illustrative pattern only)

**Task fragments:** &quot;optimum auxiliary/solvent feed&quot;, &quot;≥95% product purity&quot;,
&quot;≥99.5% recycle purity&quot;, &quot;connect recovery bottoms back with makeup&quot;.

| Step | Action |
|------|--------|
| Topology | Recovery-column bottoms → recycle stream; makeup + recycle → mixer → solvent feed → first column; process feed → first column |
| Seed | Solvent/auxiliary feed inside O1 `[LOWER, UPPER]` |
| Specs | Native Constraint rows and/or Design Spec on product/recycle purities |
| O1 | MINIMIZE solvent/auxiliary stream MOLE-FLOW via STREAM-VAR + linked CONID rows |
| Final | One post-optimization REP; report optimum from REP readback/manipulated stream, not seed inputs |

Use the task&#x27;s actual stream and block names. This table is a **pattern**, not a mandate to hardcode any particular flow rate or label set.

```

### FILE: aspen_agent_skills/guides/split-handoff-inheritance-boundary/SKILL.md
Reason: selected skill for task block family
```text
---
name: split-handoff-inheritance-boundary
description: &gt;-
  Reminds agents that split-task handoff inheritance is not blind numeric
  inheritance. Use when a downstream task continues, extends, or repairs an
  upstream flowsheet, checkpoint, or handoff.
---

# Split Handoff Inheritance Boundary

## Core Rule

In split or staged tasks, inherit **meaning before numbers**.

Preserve upstream process roles, component identities, stream/block intent, and useful evidence. Do not blindly freeze every upstream numeric parameter as immutable.

## Inherit By Default

Downstream tasks should inherit and protect:

- **process meaning:** feed/product/recycle/utility roles, block intent, and the physical train order
- **topology intent:** which streams connect to which blocks/ports, bundle-owned surfaces, and deferred-vs-materialized feature boundaries
- **component/property basis:** component slate, assay or petroleum-curve basis, and global/block property assumptions unless downstream evidence proves a repair is required
- **role mapping:** which handoff stream or block is the feed, product, recovery, makeup, purge, or utility for the active downstream scope
- **trusted evidence:** qualified checkpoints, readback locations, artifact paths, and proven scaffold rows from the upstream stage
- **qualified checkpoints** as starting points, not as proof that every downstream target is already satisfied

## Paper-Locked vs Adjustable Boundary

Treat the handoff contract as two layers:

### Paper-locked facts — do not change without explicit downstream task authority

- task-given topology, stream/block identity, and port role mapping
- assay, petroleum-curve, component slate, or property-method facts explicitly required by the task
- stage counts, feed-stage locations, or side-stripper ownership when the task or figure fixes them
- hard operating targets, validation metrics, or product identities explicitly named in the downstream contract
- evidence that a value is part of the downstream scoreable target, not merely an upstream scaffold seed

### Adjustable closure/spec parameters — may change when downstream evidence requires it

Treat these as **seeds** unless the downstream task or handoff explicitly says they are fixed:

- duty, boilup, reflux, reflux ratio, or distillate/product draw rates
- operating-spec pair choice such as `D + QREB` versus `B + RR`
- seed product estimates, side-draw flows, PA circulation, or small scaffold flows used only to complete input
- pressure pairs, split/recovery fractions, and probe-selected numeric rows
- upstream closure choices that preserve process meaning but restore downstream mass balance or convergence

Changing an adjustable parameter is allowed when the process role is preserved and the reason is documented. Changing a paper-locked fact is not a normal downstream repair path.

## Downstream Evidence Triggers

Adjust upstream-inherited numeric closure/spec values only when at least one downstream evidence trigger is present:

- completion or Next-gate text that points to closure/spec mismatch rather than missing topology
- **feed-scale gate:** inherited feed flow is orders of magnitude below task/product-slate closure
- **mass-closure gate:** product-flow-exceeds-feed, zero-feed bypass, block-not-in-mass-balance, or tiny inherited bottoms/product streams
- **nonconvergence signature:** dry column, disappearing liquid/vapor, repeated column iteration failure, or severe operating-pair instability
- **target-readback mismatch:** downstream result readbacks prove the inherited handoff cannot satisfy the active task target even after topology is correct

Do not change upstream numbers preemptively. First record whether the failure is semantic (wrong stream role, missing port, wrong block identity) or numeric (closure/spec/seed scale).

## Protected Numeric Values

A numeric value is protected only when it is supported by trusted upstream evidence, explicitly required by the downstream task or handoff, and still compatible with downstream completion, convergence, and target evidence.

If any part is unclear, record it as an initial seed, not a fixed contract.

## Practical Note

Before continuing a flowsheet, record:

```json
{
  &quot;handoff_inheritance&quot;: {
    &quot;semantic_roles_inherited&quot;: [],
    &quot;topology_intent_inherited&quot;: [],
    &quot;component_property_basis_inherited&quot;: [],
    &quot;numeric_values_used_as_seeds&quot;: [],
    &quot;numeric_values_protected&quot;: [],
    &quot;paper_locked_facts_preserved&quot;: [],
    &quot;values_changed_for_downstream_reason&quot;: [],
    &quot;change_triggers&quot;: [],
    &quot;handoff_requalified_after_change&quot;: false
  }
}
```

For every changed upstream handoff spec, the summary must also record:

- what was inherited unchanged
- what was protected as paper-locked
- which inherited numbers were used only as seeds
- which upstream closure/spec values were changed
- which downstream evidence trigger forced the change
- whether the repaired handoff stream/block re-qualified against the active gate after the change

## Generic Rule

Do not equate &quot;continue from upstream&quot; with &quot;freeze all upstream numbers&quot;. Continue the process meaning first; protect numeric parameters only when they are explicitly part of the downstream contract. When downstream evidence shows the inherited numeric closure is wrong, repair the handoff boundary before widening optional downstream features.

For downstream analysis/optimization tasks, also do not equate &quot;fresh Aspen
session&quot; with &quot;rediscover the train from a minimum prefix&quot;. Reuse the upstream
qualified topology and scaffold evidence; requalify once, then analyze.

Cross-scenario setup descriptions must cover the immediate dependency&#x27;s full
proven scope (for example T02 → T03 hands off PF+CDU+VDU). Prefer
`producer_setup_description.md` from the upstream handoff bundle; do not treat a
nested earlier-hop PF-only note as the T02→T03 authority.

```

### FILE: aspen_agent_skills/guides/rep-derived-metric-consistency/SKILL.md
Reason: selected skill for task block family
```text
---
name: rep-derived-metric-consistency
description: Requires deterministic calculation of derived metrics from trusted Aspen REP/readback raw values. Use when reporting recovery, conversion, weighted averages, material balances, split fractions, or objective expressions derived from multiple streams or rows.
---

# REP Derived Metric Consistency

LLM REP readback is for extracting raw Aspen values and units. Script logic must
calculate derived metrics that combine, compare, or weight those values.

## Raw vs Derived Boundary

- Use LLM REP readback for raw stream/block/profile values printed in the current
  converged `.rep`: temperatures, pressures, flows, compositions, duties, areas,
  stages, and profile rows.
- Use deterministic script calculations for recovery, conversion, selectivity,
  weighted averages, material balance closure, objective sums, and any metric
  involving more than one raw value.
- Do not ask the LLM to compute a final weighted metric from prose when the raw
  values can be parsed from `rep_readback_evidence` or saved structured rows.

## Calculation Contract

For every derived metric, persist:

- raw input values and units;
- conversion factors or common basis;
- formula;
- computed value and unit/basis;
- source rows or `request_id`s;
- tolerance/check used by validation.

If any raw input is missing or unit-ambiguous, keep the derived metric unresolved
instead of filling a plausible number.

## Engineering Tolerance And Equality

A converged engineering equality is not bitwise floating-point equality. Record the target, explicit unit/basis, measured residual and task/externally accepted absolute or relative tolerance. Convert both quantities to the same basis through `AnnotatedQuantity` / `UNIT_REGISTRY` before evaluating the residual. Keep solver convergence tolerance, engineering acceptance tolerance and report rounding distinct. If no acceptance tolerance is specified, leave acceptance to the external decision owner; do not invent a case-specific epsilon, tighten to exact equality, round before checking, or widen a tolerance to turn a miss into a pass.

## Examples

- Component recovery = product component flow / feed component flow.
- Weighted average property = sum(flow_i * property_i) / sum(flow_i).
- Objective = sum of converted duties/powers/cost terms in a common unit.
- Material balance closure = outlet total / inlet total, with common flow basis.

```

### FILE: aspen_agent_skills/guides/analysis-method-selection/SKILL.md
Reason: selected skill for task block family
```text
---
name: analysis-method-selection
description: Selects between Aspen Design Spec, Optimization, Sensitivity, and Aspen-backed candidate tables from task semantics. Use when a task asks to hit a target, choose an optimum, build a response curve, or repair an analysis route that overuses SA/OPT/DS.
---

# Analysis Method Selection

Use the smallest native analysis method that matches the task&#x27;s decision
semantics. Do not choose Sensitivity just because it is easy to configure, and do
not force Optimization when the objective cannot be represented by the available
native helper surface.

## Method Choice

- **Design Spec first** for equality targets: make a product quality, recovery,
  component fraction, outlet temperature, flow, required utility/feed/reflux, or
  similar result hit a numeric target by varying one physical input.
- **Optimization first** for constrained optima: minimize/maximize an objective
  under bounds or constraints, when objective, manipulated handles, and
  constraints can be represented by native Optimization helpers.
- **Sensitivity first** for response evidence: response curves, trends, tradeoff
  tables, and rows that will be ranked by deterministic post-processing. Configure
  the native Sensitivity object and select from its tabulated output.
- **Candidate table only after native failure.** A procedural sweep or candidate
  table is allowed after native Design Spec, Sensitivity, or Optimization cannot
  bind the sampled variable, objective, or manipulated handle. It is not the
  first method for an equality, a response study, or a constrained optimum.
  Every fallback row must still be Aspen-backed, converged, and unit-annotated.

## Role Contract

Before configuring DS/SA/OPT, name these roles in the summary or helper payload:

- `task_metric`: the physical result to hit, optimize, compare, or plot.
- `manipulated_handle`: the Aspen input allowed to move.
- `fixed_anchors`: specifications that must stay fixed while solving.
- `constraints`: feasibility limits, if any.
- `selection_rule`: how the final value or row will be chosen.

The sampled/FVN/objective side must match `task_metric`, not a convenient block
proxy. The manipulated side must be a real input, not the target result.

## Do Not Overuse SA

Native Sensitivity is exploration evidence unless the task asks for a response
table, curve, trend, or row ranking. It should not replace:

- a Design Spec when the task is an equality target with one causal knob;
- an Optimization when the task asks for a constrained optimum and native OPT can
  represent the objective;
- final evidence when the populated table does not contain the target metric.

## Do Not Force Empty OPT

If native Optimization cannot bind the objective, constraints, or manipulated
variables, do not create a placeholder object and report its seed values. Use an
Aspen-backed candidate table or Sensitivity sweep plus deterministic objective
calculation, and record that native OPT was not the selected route.

## Required Evidence

- DS: active object, target readback, final manipulated value, residual/error,
  post-DS run evidence.
- OPT: objective value, manipulated movement, constraint status, solver
  participation, selected optimum source.
- SA/candidate table: populated rows with distinct x/y values, unit readbacks,
  selected row and deterministic selection rule.

```

### FILE: aspen_agent_skills/guides/analysis-object-output-repair/SKILL.md
Reason: selected skill for task block family
```text
---
name: analysis-object-output-repair
description: Repairs Aspen Design Spec, Sensitivity, and Optimization objects that configure successfully but produce missing, empty, unused, or non-decision output. Use in repair loops after DS/SA/OPT setup, output collection, or summary evidence failures.
---

# Analysis Object Output Repair

Use this in repair loops. A configured analysis object is not useful until the
same post-analysis run produces native output that is used for the decision.

## Trigger Signals

- DS/SA/OPT object exists, but native output rows are missing or empty.
- Summary reports seed inputs, selected rows, or manual calculations instead of
  native DS/SA/OPT output.
- Validation says `results_not_used_for_decision`, missing selected row, missing
  objective value, missing `FINAL_VAL`, empty Sensitivity table, or no manipulated
  movement.
- The final run/export happened before the analysis object was configured.

## Repair Order

1. Keep or restore a trusted base run.
2. Verify the object is complete and active before the final engine run.
3. Run Aspen after the object is configured.
4. Collect native output from that same run.
5. Write summary fields from native output, not from seeds or setter receipts.

Do not switch methods just because output collection failed once. First repair
the transaction and output surface for the selected method.

## Family-Specific Gates

- **Design Spec**: require target value, residual/error, final manipulated value,
  and target readback. If `FINAL_VAL` or residual is missing, repair DS output
  collection or rerun the active DS; do not report the manipulated seed.
- **Optimization**: require objective value, final manipulated values, constraint
  statuses, and solver participation. If objective or manipulated movement is
  missing, repair OPT configuration/output; do not report an optimum.
- **Sensitivity**: require filled table rows with distinct varied coordinates and
  task-relevant responses. If rows are empty, self-referential, all zero, or unit
  ambiguous, repair vary/response/unit selection; do not report a trend.

## Evidence Contract

Persist under `analysis_objects.&lt;family&gt;`:

- object name and helper used;
- readbacks for manipulated and sampled/objective/constraint sides;
- post-run REP/APW/history identity;
- native output values and units;
- decision source row/value;
- unresolved blocker when output remains unavailable.

```

### FILE: generated/task_profile_planning_validators.md
Reason: task-profile helper signatures for planning validators
```text
# Task Profile: Planning Validator Helper Signatures

This section is generated from the LLM-selected task profile.
Use your actual Aspen block/stream IDs from the task statement; the placeholders below are generic.

- case_id: `chinese_5_1_radfrac`
- planning_validator_families: PROPERTY_METHODS, HEATER, RSTOIC, FLASH2, FSPLIT, RADFRAC, PUMP, COMPR, PIPE, VALVE

## validate_material_edge_plan

Validate a static material topology before mutating Aspen.

Signature:

```python
validate_material_edge_plan(
    edges,
    *,
    block_names=None,
    stream_names=None,
)
```

Rules:

- Pass the edge list as the **first positional** argument named `edges`.
- Do **not** pass `edge_plan=`, `topology=`, or other invented keyword aliases.
- Edge tuples `(stream, source, destination)` are case-insensitively unique: write each physical edge once, never silently deduplicate, and keep connection calls in one-to-one correspondence with the plan.
- **PRE-SUBMIT MATERIAL EDGE CHECKLIST (mechanical, before outputting Python):** inspect the complete static `MATERIAL_EDGES`/`edges` list and count rows by case-insensitive stream ID.
- Every physical material stream must have exactly one edge row, including feeds/products whose `source` or `destination` is `None`; a recycle is still one `source -&gt; destination` edge.
- Never duplicate a connection merely to show it in multiple process groups. Do not use a `set` or `dict` to silently deduplicate; if any stream count exceeds one, rewrite the list.
- Verify one-to-one correspondence in both directions: each connection call has exactly one edge row, and each edge row has exactly one connection call.
- Each edge item uses `{&quot;stream&quot;: &quot;&lt;stream_id&gt;&quot;, &quot;source&quot;: &lt;block_id | None&gt;, &quot;destination&quot;: &lt;block_id | None&gt;}`.
- Feeds have `source=None`; products have `destination=None`.
- Aspen stream IDs must match `^[A-Za-z]{1,2}[0-9]{0,2}$` (examples: `F1`, `D1`, `S3`). Long semantic names such as `NAP`/`KERO`/`HNAP` are invalid; map them with `allocate_aspen_short_stream_names(...)` and `rewrite_material_edge_plan_streams(...)` before validation.
- Optional `block_names` / `stream_names` declare IDs you expect in the plan; missing declared streams raise.

Placeholder edge-plan shape:

```python
validate_material_edge_plan(
    [
        {&quot;stream&quot;: &quot;&lt;feed_stream&gt;&quot;, &quot;source&quot;: None, &quot;destination&quot;: &quot;&lt;first_block&gt;&quot;},
        {&quot;stream&quot;: &quot;&lt;intermediate_stream&gt;&quot;, &quot;source&quot;: &quot;&lt;upstream_block&gt;&quot;, &quot;destination&quot;: &quot;&lt;downstream_block&gt;&quot;},
        {&quot;stream&quot;: &quot;&lt;product_stream&gt;&quot;, &quot;source&quot;: &quot;&lt;last_block&gt;&quot;, &quot;destination&quot;: None},
    ],
    block_names=[&quot;&lt;first_block&gt;&quot;, &quot;&lt;upstream_block&gt;&quot;, &quot;&lt;downstream_block&gt;&quot;, &quot;&lt;last_block&gt;&quot;],
    stream_names=[&quot;&lt;feed_stream&gt;&quot;, &quot;&lt;intermediate_stream&gt;&quot;, &quot;&lt;product_stream&gt;&quot;],
)
```

If the helper raises, fix the stream/block mapping before creating or connecting Aspen objects.

## Recycle convergence helper

Hard signature rule:

```python
client.invoke(&quot;configure_recycle_convergence_options&quot;, tolerance=1e-5, tear_method=&quot;WEGSTEIN&quot;, wegstein_max_iterations=100)
```

Never pass `max_iterations`; it is an incorrect alias, not a supported parameter.

Design Spec block-var rule: `BASIS_*` input leaves are forbidden in both `vary_variable` and `vary_patterns`. Resolve the exact token from live options; when unknown omit `vary_variable` and pass only semantic `vary_patterns`. `max_step_size` is a dimensionless 0..1 fraction.

## validate_required_native_blocks_plan

Validate that required native process blocks stay on the evidence-bearing path.

Signature:

```python
validate_required_native_blocks_plan(
    required_blocks_by_family,
    *,
    created_blocks_by_family,
    finalization_required_blocks,
)
```

Rules:

- Pass `required_blocks_by_family` as the **only positional** argument.
- Pass `created_blocks_by_family` and `finalization_required_blocks` as **keyword-only** arguments.
- Family keys are uppercase tokens such as `PUMP`, `RSTOIC`, `RADFRAC`. Values are lists of your block IDs.
- Do **not** pass a second positional argument.
- Rejected keyword aliases include `planned_native_blocks`, `planned_blocks`, `block_plan`, `required_blocks`, and `native_blocks`.
- `TypeError: ... takes 1 positional argument but 2 were given` usually means a block list was passed positionally instead of inside `required_blocks_by_family`.
- Model Analysis objects (Design Spec, Sensitivity, Optimization) are **not** block families for this helper.

### Block families for this case

- `PROPERTY_METHODS` → map to your script&#x27;s block ID (placeholder `&lt;block_id&gt;`)
- `HEATER` → map to your script&#x27;s block ID (placeholder `&lt;heater_block&gt;`)
- `RSTOIC` → map to your script&#x27;s block ID (placeholder `&lt;reactor_block&gt;`)
- `FLASH2` → map to your script&#x27;s block ID (placeholder `&lt;flash_block&gt;`)
- `FSPLIT` → map to your script&#x27;s block ID (placeholder `&lt;split_block&gt;`)
- `RADFRAC` → map to your script&#x27;s block ID (placeholder `&lt;column_block&gt;`)
- `PUMP` → map to your script&#x27;s block ID (placeholder `&lt;pump_block&gt;`)
- `COMPR` → map to your script&#x27;s block ID (placeholder `&lt;compressor_block&gt;`)
- `PIPE` → map to your script&#x27;s block ID (placeholder `&lt;pipe_block&gt;`)
- `VALVE` → map to your script&#x27;s block ID (placeholder `&lt;valve_block&gt;`)

Placeholder call shape for this case&#x27;s block families:

```python
validate_required_native_blocks_plan(
    {&quot;PROPERTY_METHODS&quot;: [&quot;&lt;block_id&gt;&quot;], &quot;HEATER&quot;: [&quot;&lt;heater_block&gt;&quot;], &quot;RSTOIC&quot;: [&quot;&lt;reactor_block&gt;&quot;], &quot;FLASH2&quot;: [&quot;&lt;flash_block&gt;&quot;], &quot;FSPLIT&quot;: [&quot;&lt;split_block&gt;&quot;], &quot;RADFRAC&quot;: [&quot;&lt;column_block&gt;&quot;], &quot;PUMP&quot;: [&quot;&lt;pump_block&gt;&quot;], &quot;COMPR&quot;: [&quot;&lt;compressor_block&gt;&quot;], &quot;PIPE&quot;: [&quot;&lt;pipe_block&gt;&quot;], &quot;VALVE&quot;: [&quot;&lt;valve_block&gt;&quot;]},
    created_blocks_by_family={&quot;PROPERTY_METHODS&quot;: [&quot;&lt;block_id&gt;&quot;], &quot;HEATER&quot;: [&quot;&lt;heater_block&gt;&quot;], &quot;RSTOIC&quot;: [&quot;&lt;reactor_block&gt;&quot;], &quot;FLASH2&quot;: [&quot;&lt;flash_block&gt;&quot;], &quot;FSPLIT&quot;: [&quot;&lt;split_block&gt;&quot;], &quot;RADFRAC&quot;: [&quot;&lt;column_block&gt;&quot;], &quot;PUMP&quot;: [&quot;&lt;pump_block&gt;&quot;], &quot;COMPR&quot;: [&quot;&lt;compressor_block&gt;&quot;], &quot;PIPE&quot;: [&quot;&lt;pipe_block&gt;&quot;], &quot;VALVE&quot;: [&quot;&lt;valve_block&gt;&quot;]},
    finalization_required_blocks=[&quot;&lt;block_id&gt;&quot;, &quot;&lt;heater_block&gt;&quot;, &quot;&lt;reactor_block&gt;&quot;, &quot;&lt;flash_block&gt;&quot;, &quot;&lt;split_block&gt;&quot;, &quot;&lt;column_block&gt;&quot;, &quot;&lt;pump_block&gt;&quot;, &quot;&lt;compressor_block&gt;&quot;, &quot;&lt;pipe_block&gt;&quot;, &quot;&lt;valve_block&gt;&quot;],
)
```

Replace every placeholder with the real block IDs you create. When one family needs multiple blocks, list every required block ID under that family key and include each ID in `finalization_required_blocks`.

## REQUIRED_BLOCKS wiring

Define one `REQUIRED_BLOCKS` list that includes every block ID on the final result path plus any gate-required native blocks. Pass the same list to `run_completion_engine_and_export(..., required_blocks=REQUIRED_BLOCKS)` and `finalize_task_summary(..., required_blocks=REQUIRED_BLOCKS)`.

```

### FILE: generated/initial_skill_selection.json
Reason: descriptor-based initial skill selection manifest
```text
{
  &quot;selection_basis&quot;: &quot;explicit skill descriptors and exact skill names; no keyword, regex, or free-text matching&quot;,
  &quot;input_skill_names&quot;: [
    &quot;aspen-task-execution-order&quot;,
    &quot;aspen-property-method-selection&quot;,
    &quot;aspen-material-stream-composition-must-be-specified&quot;,
    &quot;functional-role-semantics-validation&quot;,
    &quot;aspen-generic-readbacks&quot;,
    &quot;reactor-reaction-setup-high-level&quot;,
    &quot;sequential-reaction-topology&quot;,
    &quot;native-reactor-module-comparison&quot;,
    &quot;flash-control-chain&quot;,
    &quot;prefer-direct-component-splits&quot;,
    &quot;shared-material-port-topology&quot;,
    &quot;radfrac-absorber-like-configuration&quot;,
    &quot;radfrac-standard-column-pressure-basis&quot;,
    &quot;aspen-completion-error-hints&quot;,
    &quot;aspen-component-radfrac-evidence-repair&quot;,
    &quot;aspen-pump-outlet-specification&quot;,
    &quot;compr-analysis-variable-selection&quot;,
    &quot;aspen-custom-unit-set&quot;,
    &quot;solvent-recycle-closure-semantics&quot;,
    &quot;radfrac-extractive-distillation-solvent&quot;,
    &quot;optimization-constrained-feed-and-recycle-evidence&quot;,
    &quot;split-handoff-inheritance-boundary&quot;,
    &quot;rep-derived-metric-consistency&quot;,
    &quot;analysis-method-selection&quot;,
    &quot;analysis-object-output-repair&quot;
  ],
  &quot;selected_skill_names&quot;: [
    &quot;aspen-task-execution-order&quot;,
    &quot;aspen-property-method-selection&quot;,
    &quot;aspen-material-stream-composition-must-be-specified&quot;,
    &quot;functional-role-semantics-validation&quot;,
    &quot;aspen-generic-readbacks&quot;,
    &quot;reactor-reaction-setup-high-level&quot;,
    &quot;sequential-reaction-topology&quot;,
    &quot;native-reactor-module-comparison&quot;,
    &quot;flash-control-chain&quot;,
    &quot;prefer-direct-component-splits&quot;,
    &quot;shared-material-port-topology&quot;,
    &quot;radfrac-absorber-like-configuration&quot;,
    &quot;radfrac-standard-column-pressure-basis&quot;,
    &quot;aspen-completion-error-hints&quot;,
    &quot;aspen-component-radfrac-evidence-repair&quot;,
    &quot;aspen-pump-outlet-specification&quot;,
    &quot;compr-analysis-variable-selection&quot;,
    &quot;aspen-custom-unit-set&quot;,
    &quot;solvent-recycle-closure-semantics&quot;,
    &quot;radfrac-extractive-distillation-solvent&quot;,
    &quot;optimization-constrained-feed-and-recycle-evidence&quot;,
    &quot;split-handoff-inheritance-boundary&quot;,
    &quot;rep-derived-metric-consistency&quot;,
    &quot;analysis-method-selection&quot;,
    &quot;analysis-object-output-repair&quot;
  ],
  &quot;decisions&quot;: [
    {
      &quot;input_skill&quot;: &quot;aspen-task-execution-order&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;aspen-task-execution-order&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;aspen-property-method-selection&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;aspen-property-method-selection&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;aspen-property-method-selection&quot;,
        &quot;summary&quot;: &quot;Preserve methods; verify global/SRK free-water setup.&quot;,
        &quot;stage&quot;: &quot;init+repair&quot;,
        &quot;required_families&quot;: [],
        &quot;compatible_focus_ids&quot;: [],
        &quot;compatible_mini_focuses&quot;: [],
        &quot;init_replacement&quot;: &quot;&quot;,
        &quot;init_load&quot;: true
      }
    },
    {
      &quot;input_skill&quot;: &quot;aspen-material-stream-composition-must-be-specified&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;aspen-material-stream-composition-must-be-specified&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;aspen-material-stream-composition-must-be-specified&quot;,
        &quot;summary&quot;: &quot;Stream basis/state setup and independent-feed enthalpy preservation.&quot;,
        &quot;stage&quot;: &quot;init+repair&quot;,
        &quot;required_families&quot;: [],
        &quot;compatible_focus_ids&quot;: [],
        &quot;compatible_mini_focuses&quot;: [],
        &quot;init_replacement&quot;: &quot;&quot;,
        &quot;init_load&quot;: true
      }
    },
    {
      &quot;input_skill&quot;: &quot;functional-role-semantics-validation&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;functional-role-semantics-validation&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;aspen-generic-readbacks&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;aspen-generic-readbacks&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;aspen-generic-readbacks&quot;,
        &quot;summary&quot;: &quot;Generic Aspen/REP readbacks for streams, blocks, profiles, duties, and final evidence values.&quot;,
        &quot;stage&quot;: &quot;init+repair&quot;,
        &quot;required_families&quot;: [],
        &quot;compatible_focus_ids&quot;: [],
        &quot;compatible_mini_focuses&quot;: [],
        &quot;init_replacement&quot;: &quot;&quot;,
        &quot;init_load&quot;: true
      }
    },
    {
      &quot;input_skill&quot;: &quot;reactor-reaction-setup-high-level&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;reactor-reaction-setup-high-level&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;sequential-reaction-topology&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;sequential-reaction-topology&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;native-reactor-module-comparison&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;native-reactor-module-comparison&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;flash-control-chain&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;flash-control-chain&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;prefer-direct-component-splits&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;prefer-direct-component-splits&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;shared-material-port-topology&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;shared-material-port-topology&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;radfrac-absorber-like-configuration&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;radfrac-absorber-like-configuration&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;radfrac-standard-column-pressure-basis&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;radfrac-standard-column-pressure-basis&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;radfrac-standard-column-pressure-basis&quot;,
        &quot;summary&quot;: &quot;RadFrac pressure anchor and pressure-drop basis for standard distillation columns.&quot;,
        &quot;stage&quot;: &quot;init+repair&quot;,
        &quot;required_families&quot;: [
          &quot;RADFRAC&quot;
        ],
        &quot;compatible_focus_ids&quot;: [],
        &quot;compatible_mini_focuses&quot;: [],
        &quot;init_replacement&quot;: &quot;&quot;,
        &quot;init_load&quot;: true
      }
    },
    {
      &quot;input_skill&quot;: &quot;aspen-completion-error-hints&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;aspen-completion-error-hints&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;aspen-completion-error-hints&quot;,
        &quot;summary&quot;: &quot;Completion/PER_ERROR repairs; tear nonconvergence uses configure_recycle_convergence_options with readback; SRK uses configure_srk_free_water_steamnbs.&quot;,
        &quot;stage&quot;: &quot;init+repair&quot;,
        &quot;required_families&quot;: [],
        &quot;compatible_focus_ids&quot;: [],
        &quot;compatible_mini_focuses&quot;: [],
        &quot;init_replacement&quot;: &quot;&quot;,
        &quot;init_load&quot;: true
      }
    },
    {
      &quot;input_skill&quot;: &quot;aspen-component-radfrac-evidence-repair&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;aspen-component-radfrac-evidence-repair&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;aspen-pump-outlet-specification&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;aspen-pump-outlet-specification&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;compr-analysis-variable-selection&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;compr-analysis-variable-selection&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;compr-analysis-variable-selection&quot;,
        &quot;summary&quot;: &quot;Compressor selected-row pressure/power identity, units, and replay evidence.&quot;,
        &quot;stage&quot;: &quot;init+repair&quot;,
        &quot;required_families&quot;: [],
        &quot;compatible_focus_ids&quot;: [],
        &quot;compatible_mini_focuses&quot;: [],
        &quot;init_replacement&quot;: &quot;&quot;,
        &quot;init_load&quot;: true
      }
    },
    {
      &quot;input_skill&quot;: &quot;aspen-custom-unit-set&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;aspen-custom-unit-set&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;solvent-recycle-closure-semantics&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;solvent-recycle-closure-semantics&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;radfrac-extractive-distillation-solvent&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;radfrac-extractive-distillation-solvent&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;optimization-constrained-feed-and-recycle-evidence&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;optimization-constrained-feed-and-recycle-evidence&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;split-handoff-inheritance-boundary&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;split-handoff-inheritance-boundary&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;rep-derived-metric-consistency&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;rep-derived-metric-consistency&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;rep-derived-metric-consistency&quot;,
        &quot;summary&quot;: &quot;Derived metric consistency from trusted REP/readback raw values with explicit units and formulas.&quot;,
        &quot;stage&quot;: &quot;init+repair&quot;,
        &quot;required_families&quot;: [],
        &quot;compatible_focus_ids&quot;: [],
        &quot;compatible_mini_focuses&quot;: [],
        &quot;init_replacement&quot;: &quot;&quot;,
        &quot;init_load&quot;: true
      }
    },
    {
      &quot;input_skill&quot;: &quot;analysis-method-selection&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;analysis-method-selection&quot;,
      &quot;descriptor&quot;: {}
    },
    {
      &quot;input_skill&quot;: &quot;analysis-object-output-repair&quot;,
      &quot;decision&quot;: &quot;load_for_init&quot;,
      &quot;selected_skill&quot;: &quot;analysis-object-output-repair&quot;,
      &quot;descriptor&quot;: {}
    }
  ]
}
```

### FILE: generated/initial_helper_catalog_selection.json
Reason: descriptor-based helper catalog selection manifest
```text
{
  &quot;selection_basis&quot;: &quot;helper catalog descriptors plus exact task-profile families, surface docs, and skill names only; no keyword, regex, path-prefix, or free-text matching&quot;,
  &quot;profile_families&quot;: [
    &quot;COMPR&quot;,
    &quot;FLASH2&quot;,
    &quot;FSPLIT&quot;,
    &quot;HEATER&quot;,
    &quot;PIPE&quot;,
    &quot;PROPERTY_METHODS&quot;,
    &quot;PUMP&quot;,
    &quot;RADFRAC&quot;,
    &quot;RSTOIC&quot;,
    &quot;VALVE&quot;
  ],
  &quot;profile_surface_docs&quot;: [
    &quot;docs/hardcoded_script_plan/block_type_inject/compr.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/flash2.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/fsplit.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/heater.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/pipe.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/property_methods.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/pump.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/radfrac.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/rstoic.md&quot;,
    &quot;docs/hardcoded_script_plan/block_type_inject/valve.md&quot;
  ],
  &quot;profile_skill_names&quot;: [
    &quot;aspen-completion-error-hints&quot;,
    &quot;aspen-component-radfrac-evidence-repair&quot;,
    &quot;aspen-custom-unit-set&quot;,
    &quot;aspen-generic-readbacks&quot;,
    &quot;aspen-material-stream-composition-must-be-specified&quot;,
    &quot;aspen-property-method-selection&quot;,
    &quot;aspen-pump-outlet-specification&quot;,
    &quot;aspen-task-execution-order&quot;,
    &quot;compr-analysis-variable-selection&quot;,
    &quot;flash-control-chain&quot;,
    &quot;functional-role-semantics-validation&quot;,
    &quot;native-reactor-module-comparison&quot;,
    &quot;optimization-constrained-feed-and-recycle-evidence&quot;,
    &quot;prefer-direct-component-splits&quot;,
    &quot;radfrac-absorber-like-configuration&quot;,
    &quot;radfrac-extractive-distillation-solvent&quot;,
    &quot;radfrac-standard-column-pressure-basis&quot;,
    &quot;reactor-reaction-setup-high-level&quot;,
    &quot;rep-derived-metric-consistency&quot;,
    &quot;sequential-reaction-topology&quot;,
    &quot;shared-material-port-topology&quot;,
    &quot;solvent-recycle-closure-semantics&quot;,
    &quot;split-handoff-inheritance-boundary&quot;
  ],
  &quot;selected_helper_catalog_paths&quot;: [
    &quot;docs/hardcoded_script_plan/safe_aspen_calls_core_helpers.md&quot;,
    &quot;docs/hardcoded_script_plan/safe_aspen_calls_analysis_helpers.md&quot;,
    &quot;docs/hardcoded_script_plan/safe_aspen_calls_radfrac_helpers.md&quot;,
    &quot;docs/hardcoded_script_plan/safe_aspen_calls_heat_cascade_helpers.md&quot;
  ],
  &quot;decisions&quot;: [
    {
      &quot;helper_catalog&quot;: &quot;core&quot;,
      &quot;decision&quot;: &quot;load&quot;,
      &quot;reason&quot;: &quot;always_load&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;core&quot;,
        &quot;path&quot;: &quot;docs/hardcoded_script_plan/safe_aspen_calls_core_helpers.md&quot;,
        &quot;summary&quot;: &quot;Always-loaded session, component/property, stream state, run/export, and finalization helpers.&quot;,
        &quot;stage&quot;: &quot;init&quot;,
        &quot;required_families_any&quot;: [],
        &quot;required_surface_docs_any&quot;: [],
        &quot;required_skill_names_any&quot;: [],
        &quot;always_load&quot;: true
      }
    },
    {
      &quot;helper_catalog&quot;: &quot;analysis&quot;,
      &quot;decision&quot;: &quot;load&quot;,
      &quot;reason&quot;: &quot;matched_exact_skill_names:[&#x27;optimization-constrained-feed-and-recycle-evidence&#x27;]&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;analysis&quot;,
        &quot;path&quot;: &quot;docs/hardcoded_script_plan/safe_aspen_calls_analysis_helpers.md&quot;,
        &quot;summary&quot;: &quot;Native Design Spec, Sensitivity, and Optimization helper contracts.&quot;,
        &quot;stage&quot;: &quot;init&quot;,
        &quot;required_families_any&quot;: [
          &quot;CONSTRAINT&quot;,
          &quot;DESIGN_SPEC&quot;,
          &quot;OPTIMIZATION&quot;,
          &quot;SENSITIVITY&quot;
        ],
        &quot;required_surface_docs_any&quot;: [
          &quot;docs/hardcoded_script_plan/block_type_inject/constraint.md&quot;,
          &quot;docs/hardcoded_script_plan/block_type_inject/design_spec.md&quot;,
          &quot;docs/hardcoded_script_plan/block_type_inject/optimization.md&quot;,
          &quot;docs/hardcoded_script_plan/block_type_inject/sensitivity.md&quot;
        ],
        &quot;required_skill_names_any&quot;: [
          &quot;analysis-method-selection&quot;,
          &quot;analysis-object-output-repair&quot;,
          &quot;analysis-object-transaction-finalization&quot;,
          &quot;analysis-tools-single-pass-finalization&quot;,
          &quot;design-spec-manipulated-surface-selection&quot;,
          &quot;optimization-constrained-feed-and-recycle-evidence&quot;,
          &quot;optimization-manipulated-variable-selection&quot;,
          &quot;optimization-result-authenticity&quot;,
          &quot;sensitivity-uom-and-variable-setup&quot;,
          &quot;sensitivity-vary-patterns&quot;
        ],
        &quot;always_load&quot;: false
      }
    },
    {
      &quot;helper_catalog&quot;: &quot;radfrac&quot;,
      &quot;decision&quot;: &quot;load&quot;,
      &quot;reason&quot;: &quot;matched_explicit_profile_families:[&#x27;RADFRAC&#x27;]&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;radfrac&quot;,
        &quot;path&quot;: &quot;docs/hardcoded_script_plan/safe_aspen_calls_radfrac_helpers.md&quot;,
        &quot;summary&quot;: &quot;RadFrac setup, feed convention, profile, and product/readback helper contracts.&quot;,
        &quot;stage&quot;: &quot;init&quot;,
        &quot;required_families_any&quot;: [
          &quot;RADFRAC&quot;
        ],
        &quot;required_surface_docs_any&quot;: [
          &quot;docs/hardcoded_script_plan/block_type_inject/radfrac.md&quot;
        ],
        &quot;required_skill_names_any&quot;: [
          &quot;radfrac-absorber-like-configuration&quot;,
          &quot;radfrac-convergence-repair&quot;,
          &quot;radfrac-extractive-distillation-solvent&quot;,
          &quot;radfrac-no-condenser-reboiled-bottoms&quot;,
          &quot;radfrac-standard-column-pressure-basis&quot;,
          &quot;solvent-recycle-closure-semantics&quot;
        ],
        &quot;always_load&quot;: false
      }
    },
    {
      &quot;helper_catalog&quot;: &quot;heat_cascade&quot;,
      &quot;decision&quot;: &quot;load&quot;,
      &quot;reason&quot;: &quot;matched_explicit_profile_families:[&#x27;FLASH2&#x27;]&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;heat_cascade&quot;,
        &quot;path&quot;: &quot;docs/hardcoded_script_plan/safe_aspen_calls_heat_cascade_helpers.md&quot;,
        &quot;summary&quot;: &quot;Heat stream, HeatX, MHeatX, Flash2 evaporator, and multi-effect heat-cascade helpers.&quot;,
        &quot;stage&quot;: &quot;init&quot;,
        &quot;required_families_any&quot;: [
          &quot;FLASH2&quot;,
          &quot;HEATX&quot;,
          &quot;HEAT_STREAM&quot;,
          &quot;MHEATX&quot;
        ],
        &quot;required_surface_docs_any&quot;: [
          &quot;docs/hardcoded_script_plan/block_type_inject/flash2.md&quot;,
          &quot;docs/hardcoded_script_plan/block_type_inject/heat_stream.md&quot;,
          &quot;docs/hardcoded_script_plan/block_type_inject/heatx.md&quot;,
          &quot;docs/hardcoded_script_plan/block_type_inject/mheatx.md&quot;
        ],
        &quot;required_skill_names_any&quot;: [
          &quot;flash-control-chain&quot;,
          &quot;heatx-shortcut-target-and-area&quot;,
          &quot;multi-effect-evaporation-heatx&quot;,
          &quot;multi-effect-topology-init&quot;,
          &quot;phase-change-heat-cascade-integrity&quot;
        ],
        &quot;always_load&quot;: false
      }
    },
    {
      &quot;helper_catalog&quot;: &quot;probe&quot;,
      &quot;decision&quot;: &quot;skip&quot;,
      &quot;reason&quot;: &quot;no explicit descriptor condition matched for init&quot;,
      &quot;descriptor&quot;: {
        &quot;name&quot;: &quot;probe&quot;,
        &quot;path&quot;: &quot;docs/hardcoded_script_plan/safe_aspen_calls_probe_helpers.md&quot;,
        &quot;summary&quot;: &quot;Standard procedural probe matrix and selected-row replay helper contracts.&quot;,
        &quot;stage&quot;: &quot;repair&quot;,
        &quot;required_families_any&quot;: [],
        &quot;required_surface_docs_any&quot;: [],
        &quot;required_skill_names_any&quot;: [],
        &quot;always_load&quot;: false
      }
    }
  ]
}
```

### REACT-MCP NATIVE SKILL
React-MCP-native Aspen action contract:
1. Select exactly one JSON action: {&quot;action&quot;:&quot;mcp_tool&quot;,&quot;operation&quot;:&quot;...&quot;,&quot;parameters&quot;:{...}}.
2. Use only an operation in the visible catalog. Map process intent to the catalog operation,
   never emit Python, safe.call snippets, or invented HTTP operations.
3. After topology writes, read list_block_ports or node_info and verify the live connection.
   Use Aspen Tree paths with single backslashes (Data\\Blocks\\BLK); do not invent paths.
4. After specification writes, read the affected node/table and run the relevant block/stream
   completion check. Before engine_run, require the workflow Next-gate check.
5. Treat wrapper success as provisional. Continue when readback, completion, or evidence is
   missing; stop and repair when a readback contradicts the requested state.
6. Error routing: unknown operation -&gt; choose a catalog operation; missing parameter -&gt; supply
   it; node not found -&gt; normalize/re-read the canonical path and inspect parent elements;
   topology error -&gt; list ports before reconnecting; incomplete input -&gt; repair the named object
   then re-run the completion gate; runtime error -&gt; inspect same-run status before retrying.
7. For finalize_task_summary_with_llm_rep_readback, pass exactly the catalog schema fields:
   required `summary` and `final_bundle`; optional `rep_readback_targets` and evidence fields.
   Do not pass `case_id` as a standalone parameter. Do not call this finalizer until the
   current run has trusted engine evidence, raw PER_ERROR=0, and an exported REP/APW bundle.
8. When PER_ERROR is nonzero, do not finalize or normalize it away. Read the block/flowsheet
   error message, completion status, run status, and affected variable readbacks; repair the
   named physical input with a typed operation, rerun, and recheck raw PER_ERROR. Preserve
   the failed evidence and route the next action to the specific physical input, not merely
   to another finalize/readback call. `export_final_evidence` returns a bounded
   `diagnostic_summary`; inspect its `rep_problem_status.hints` and `repair_required` before
   changing a property method or any other physical input. A nonzero flag without a named
   diagnostic is not evidence for guessing a repair.

### SHARED SKILL REPRESENTATION ADAPTER
React action translation contract for shared script-agent skills:
- Shared SKILL.md files are authoritative process rules, Aspen semantics, safety constraints, and evidence requirements.
- Python/code blocks, safe.call snippets, generated-script examples, and helper implementation details are reference material only; do not emit Python or treat them as executable actions.
- Translate every required step into a registered MCP capability from the visible catalog, with JSON parameters only.
- When a skill names a helper, use the corresponding capability operation; after writes, perform the skill-required readback, topology evidence, completion/Next gate, and same-run evidence export.
- Never invent a tree path from an example. Use canonical Aspen paths with single backslashes (for example Data\Blocks\BLK), and use list_block_ports/node readback before wiring.
- A successful wrapper response is not sufficient evidence: inspect translated_operations, partial_failures, live ports, and readbacks before proceeding.
- Preserve the same skill rules and constraints as script-agent; this adapter changes only the action representation from script generation to MCP actions.

RUN_MEMORY_SUMMARY:
{
  &quot;case_id&quot;: &quot;chinese_5_1_radfrac&quot;,
  &quot;stateful_reducer&quot;: {
    &quot;enabled&quot;: false,
    &quot;contract&quot;: &quot;Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts.&quot;
  },
  &quot;task_requirements&quot;: {
    &quot;source&quot;: &quot;task text and gate contract in prompt&quot;,
    &quot;do_not_use_rejected_surrogates&quot;: []
  },
  &quot;current_model_state&quot;: {
    &quot;state_version&quot;: 25,
    &quot;domain_versions&quot;: {
      &quot;flowsheet&quot;: 25,
      &quot;properties&quot;: 2,
      &quot;stream:COLFD&quot;: 3,
      &quot;stream:BZIN2&quot;: 3,
      &quot;stream:H2RCY&quot;: 3,
      &quot;stream:RXIN&quot;: 3,
      &quot;stream:BZIN&quot;: 2,
      &quot;stream:VAP&quot;: 3,
      &quot;stream:PURGE&quot;: 3,
      &quot;stream:PURGE2&quot;: 2,
      &quot;stream:CHRCY&quot;: 3,
      &quot;stream:H2RCY2&quot;: 3,
      &quot;stream:H2IN&quot;: 2,
      &quot;stream:PRODUCT&quot;: 2,
      &quot;stream:CHRCY2&quot;: 3,
      &quot;stream:RXOUT&quot;: 3,
      &quot;stream:CHRCY3&quot;: 3,
      &quot;stream:LTENDS&quot;: 2,
      &quot;stream:LIQ&quot;: 3,
      &quot;block:FEEDPUMP&quot;: 2,
      &quot;block:FEED-MIX&quot;: 2,
      &quot;block:REACT&quot;: 2,
      &quot;block:HP-SEP&quot;: 2,
      &quot;block:VFLOW&quot;: 2,
      &quot;block:COMP&quot;: 2,
      &quot;block:VALVE&quot;: 2,
      &quot;block:LFLOW&quot;: 2,
      &quot;block:PUMP&quot;: 2,
      &quot;block:PIPE&quot;: 2,
      &quot;block:COLUMN&quot;: 2
    },
    &quot;components&quot;: [
      &quot;H2&quot;,
      &quot;N2&quot;,
      &quot;CH4&quot;,
      &quot;BENZENE&quot;,
      &quot;CYCLOHEX&quot;
    ],
    &quot;property_method&quot;: &quot;&quot;,
    &quot;blocks&quot;: [
      &quot;FEEDPUMP&quot;,
      &quot;FEED-MIX&quot;,
      &quot;REACT&quot;,
      &quot;HP-SEP&quot;,
      &quot;VFLOW&quot;,
      &quot;COMP&quot;,
      &quot;VALVE&quot;,
      &quot;LFLOW&quot;,
      &quot;PUMP&quot;,
      &quot;PIPE&quot;,
      &quot;COLUMN&quot;
    ],
    &quot;streams&quot;: [
      &quot;BZIN&quot;,
      &quot;H2IN&quot;,
      &quot;BZIN2&quot;,
      &quot;H2RCY2&quot;,
      &quot;RXIN&quot;,
      &quot;RXOUT&quot;,
      &quot;VAP&quot;,
      &quot;H2RCY&quot;,
      &quot;PURGE&quot;,
      &quot;PURGE2&quot;,
      &quot;LIQ&quot;,
      &quot;COLFD&quot;,
      &quot;CHRCY&quot;,
      &quot;CHRCY2&quot;,
      &quot;CHRCY3&quot;,
      &quot;LTENDS&quot;,
      &quot;PRODUCT&quot;
    ],
    &quot;connections&quot;: [],
    &quot;specs&quot;: [],
    &quot;engine_run&quot;: null,
    &quot;artifacts&quot;: {},
    &quot;readbacks&quot;: []
  },
  &quot;operation_ledger&quot;: {
    &quot;677ff79d23598058&quot;: {
      &quot;operation&quot;: &quot;add_components_by_cas&quot;,
      &quot;parameters&quot;: {
        &quot;components&quot;: [
          {
            &quot;component_id&quot;: &quot;H2&quot;,
            &quot;cas&quot;: &quot;1333-74-0&quot;
          },
          {
            &quot;component_id&quot;: &quot;N2&quot;,
            &quot;cas&quot;: &quot;7727-37-9&quot;
          },
          {
            &quot;component_id&quot;: &quot;CH4&quot;,
            &quot;cas&quot;: &quot;74-82-8&quot;
          },
          {
            &quot;component_id&quot;: &quot;BENZENE&quot;,
            &quot;cas&quot;: &quot;71-43-2&quot;
          },
          {
            &quot;component_id&quot;: &quot;CYCLOHEX&quot;,
            &quot;cas&quot;: &quot;110-82-7&quot;
          }
        ]
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;properties&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;properties&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;components_added&quot;: [
          {
            &quot;cas&quot;: &quot;1333740&quot;,
            &quot;component_id&quot;: &quot;H2&quot;,
            &quot;requested_component_id&quot;: &quot;H2&quot;,
            &quot;preferred_component_id&quot;: &quot;H2&quot;
          },
          {
            &quot;cas&quot;: &quot;7727379&quot;,
            &quot;component_id&quot;: &quot;N2&quot;,
            &quot;requested_component_id&quot;: &quot;N2&quot;,
            &quot;preferred_component_id&quot;: &quot;N2&quot;
          },
          {
            &quot;cas&quot;: &quot;74-82-8&quot;,
            &quot;component_id&quot;: &quot;CH4&quot;,
            &quot;requested_component_id&quot;: &quot;CH4&quot;,
            &quot;preferred_component_id&quot;: &quot;CH4&quot;
          },
          {
            &quot;cas&quot;: &quot;71-43-2&quot;,
            &quot;component_id&quot;: &quot;BENZENE&quot;,
            &quot;requested_component_id&quot;: &quot;BENZENE&quot;,
            &quot;preferred_component_id&quot;: &quot;BENZENE&quot;
          },
          {
            &quot;cas&quot;: &quot;110-82-7&quot;,
            &quot;component_id&quot;: &quot;CYCLOHEX&quot;,
            &quot;requested_component_id&quot;: &quot;CYCLOHEX&quot;,
            &quot;preferred_component_id&quot;: &quot;CYCLOHEX&quot;
          }
        ],
        &quot;count&quot;: 5,
        &quot;message&quot;: &quot;Added 5 component(s) successfully&quot;,
        &quot;verification&quot;: {
          &quot;success&quot;: true,
          &quot;expected_component_ids&quot;: [
            &quot;H2&quot;,
            &quot;N2&quot;,
            &quot;CH4&quot;,
            &quot;BENZENE&quot;,
            &quot;CYCLOHEX&quot;
          ],
          &quot;actual_component_ids&quot;: [
            &quot;H2&quot;,
            &quot;N2&quot;,
            &quot;CH4&quot;,
            &quot;BENZENE&quot;,
            &quot;CYCLOHEX&quot;
          ],
          &quot;missing_component_ids&quot;: []
        },
        &quot;contamination&quot;: {
          &quot;success&quot;: true,
          &quot;expected_component_ids&quot;: [
            &quot;H2&quot;,
            &quot;N2&quot;,
            &quot;CH4&quot;,
            &quot;BENZENE&quot;,
            &quot;CYCLOHEX&quot;
          ],
          &quot;actual_component_ids&quot;: [
            &quot;H2&quot;,
            &quot;N2&quot;,
            &quot;CH4&quot;,
            &quot;BENZENE&quot;,
            &quot;CYCLOHEX&quot;
          ],
          &quot;extra_component_ids&quot;: [],
          &quot;generic_extra_component_ids&quot;: []
        }
      }
    },
    &quot;d0f7c037faabb2bb&quot;: {
      &quot;operation&quot;: &quot;ensure_property_method&quot;,
      &quot;parameters&quot;: {
        &quot;method&quot;: &quot;RK-SOAVE&quot;
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;properties&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;properties&quot;: 2
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;virtual_tool&quot;: &quot;ensure_property_method&quot;,
        &quot;steps_completed&quot;: 5,
        &quot;steps_total&quot;: 5,
        &quot;last_result&quot;: null
      }
    },
    &quot;33ce8ec6c91a3f71&quot;: {
      &quot;operation&quot;: &quot;create_material_streams&quot;,
      &quot;parameters&quot;: {
        &quot;stream_names&quot;: [
          &quot;BZIN&quot;,
          &quot;H2IN&quot;,
          &quot;BZIN2&quot;,
          &quot;H2RCY2&quot;,
          &quot;RXIN&quot;,
          &quot;RXOUT&quot;,
          &quot;VAP&quot;,
          &quot;H2RCY&quot;,
          &quot;PURGE&quot;,
          &quot;PURGE2&quot;,
          &quot;LIQ&quot;,
          &quot;COLFD&quot;,
          &quot;CHRCY&quot;,
          &quot;CHRCY2&quot;,
          &quot;CHRCY3&quot;,
          &quot;LTENDS&quot;,
          &quot;PRODUCT&quot;
        ]
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;stream:BZIN&quot;,
        &quot;stream:H2IN&quot;,
        &quot;stream:BZIN2&quot;,
        &quot;stream:H2RCY2&quot;,
        &quot;stream:RXIN&quot;,
        &quot;stream:RXOUT&quot;,
        &quot;stream:VAP&quot;,
        &quot;stream:H2RCY&quot;,
        &quot;stream:PURGE&quot;,
        &quot;stream:PURGE2&quot;,
        &quot;stream:LIQ&quot;,
        &quot;stream:COLFD&quot;,
        &quot;stream:CHRCY&quot;,
        &quot;stream:CHRCY2&quot;,
        &quot;stream:CHRCY3&quot;,
        &quot;stream:LTENDS&quot;,
        &quot;stream:PRODUCT&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;stream:BZIN&quot;: 1,
        &quot;stream:H2IN&quot;: 1,
        &quot;stream:BZIN2&quot;: 1,
        &quot;stream:H2RCY2&quot;: 1,
        &quot;stream:RXIN&quot;: 1,
        &quot;stream:RXOUT&quot;: 1,
        &quot;stream:VAP&quot;: 1,
        &quot;stream:H2RCY&quot;: 1,
        &quot;stream:PURGE&quot;: 1,
        &quot;stream:PURGE2&quot;: 1,
        &quot;stream:LIQ&quot;: 1,
        &quot;stream:COLFD&quot;: 1,
        &quot;stream:CHRCY&quot;: 1,
        &quot;stream:CHRCY2&quot;: 1,
        &quot;stream:CHRCY3&quot;: 1,
        &quot;stream:LTENDS&quot;: 1,
        &quot;stream:PRODUCT&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;virtual_tool&quot;: &quot;create_material_streams&quot;,
        &quot;steps_completed&quot;: 17,
        &quot;steps_total&quot;: 17,
        &quot;last_result&quot;: null
      }
    },
    &quot;aeeab72bf4e897bd&quot;: {
      &quot;operation&quot;: &quot;create_pump&quot;,
      &quot;parameters&quot;: {
        &quot;block_name&quot;: &quot;FEEDPUMP&quot;
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;block:FEEDPUMP&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;block:FEEDPUMP&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;block_name&quot;: &quot;FEEDPUMP&quot;,
        &quot;block_type&quot;: &quot;PUMP&quot;,
        &quot;composite&quot;: &quot;FEEDPUMP!PUMP&quot;,
        &quot;message&quot;: &quot;Block FEEDPUMP (PUMP) created successfully&quot;,
        &quot;block_iteration_floor&quot;: {
          &quot;attempted&quot;: true,
          &quot;floor&quot;: 200,
          &quot;via&quot;: &quot;com_tree&quot;,
          &quot;reason&quot;: &quot;post-block-create&quot;,
          &quot;leaves&quot;: [
            &quot;MAXOL&quot;,
            &quot;MAXIT&quot;
          ],
          &quot;raised&quot;: [
            {
              &quot;block&quot;: &quot;FEEDPUMP&quot;,
              &quot;leaf&quot;: &quot;MAXIT&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\FEEDPUMP\\Input\\MAXIT&quot;,
              &quot;before&quot;: 30,
              &quot;after&quot;: 200
            }
          ],
          &quot;unchanged&quot;: [],
          &quot;failed&quot;: [],
          &quot;missing&quot;: [
            {
              &quot;block&quot;: &quot;FEEDPUMP&quot;,
              &quot;leaf&quot;: &quot;MAXOL&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\FEEDPUMP\\Input\\MAXOL&quot;,
              &quot;attempted_paths&quot;: [
                &quot;Data\\Blocks\\FEEDPUMP\\Input\\MAXOL&quot;
              ]
            }
          ],
          &quot;success&quot;: true
        }
      }
    },
    &quot;0909126309d406aa&quot;: {
      &quot;operation&quot;: &quot;create_heater&quot;,
      &quot;parameters&quot;: {
        &quot;block_name&quot;: &quot;FEED-MIX&quot;
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;block:FEED-MIX&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;block:FEED-MIX&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;block_name&quot;: &quot;FEED-MIX&quot;,
        &quot;block_type&quot;: &quot;HEATER&quot;,
        &quot;composite&quot;: &quot;FEED-MIX!HEATER&quot;,
        &quot;message&quot;: &quot;Block FEED-MIX (HEATER) created successfully&quot;,
        &quot;block_iteration_floor&quot;: {
          &quot;attempted&quot;: true,
          &quot;floor&quot;: 200,
          &quot;via&quot;: &quot;com_tree&quot;,
          &quot;reason&quot;: &quot;post-block-create&quot;,
          &quot;leaves&quot;: [
            &quot;MAXOL&quot;,
            &quot;MAXIT&quot;
          ],
          &quot;raised&quot;: [
            {
              &quot;block&quot;: &quot;FEED-MIX&quot;,
              &quot;leaf&quot;: &quot;MAXIT&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\FEED-MIX\\Input\\MAXIT&quot;,
              &quot;before&quot;: 30,
              &quot;after&quot;: 200
            }
          ],
          &quot;unchanged&quot;: [],
          &quot;failed&quot;: [],
          &quot;missing&quot;: [
            {
              &quot;block&quot;: &quot;FEED-MIX&quot;,
              &quot;leaf&quot;: &quot;MAXOL&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\FEED-MIX\\Input\\MAXOL&quot;,
              &quot;attempted_paths&quot;: [
                &quot;Data\\Blocks\\FEED-MIX\\Input\\MAXOL&quot;
              ]
            }
          ],
          &quot;success&quot;: true
        }
      }
    },
    &quot;a6c7e44d982c03d4&quot;: {
      &quot;operation&quot;: &quot;create_rstoic&quot;,
      &quot;parameters&quot;: {
        &quot;block_name&quot;: &quot;REACT&quot;
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;block:REACT&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;block:REACT&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;block_name&quot;: &quot;REACT&quot;,
        &quot;block_type&quot;: &quot;RSTOIC&quot;,
        &quot;composite&quot;: &quot;REACT!RSTOIC&quot;,
        &quot;message&quot;: &quot;Block REACT (RSTOIC) created successfully&quot;,
        &quot;block_iteration_floor&quot;: {
          &quot;attempted&quot;: true,
          &quot;floor&quot;: 200,
          &quot;via&quot;: &quot;com_tree&quot;,
          &quot;reason&quot;: &quot;post-block-create&quot;,
          &quot;leaves&quot;: [
            &quot;MAXOL&quot;,
            &quot;MAXIT&quot;
          ],
          &quot;raised&quot;: [
            {
              &quot;block&quot;: &quot;REACT&quot;,
              &quot;leaf&quot;: &quot;MAXIT&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\REACT\\Input\\MAXIT&quot;,
              &quot;before&quot;: 30,
              &quot;after&quot;: 200
            }
          ],
          &quot;unchanged&quot;: [],
          &quot;failed&quot;: [],
          &quot;missing&quot;: [
            {
              &quot;block&quot;: &quot;REACT&quot;,
              &quot;leaf&quot;: &quot;MAXOL&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\REACT\\Input\\MAXOL&quot;,
              &quot;attempted_paths&quot;: [
                &quot;Data\\Blocks\\REACT\\Input\\MAXOL&quot;
              ]
            }
          ],
          &quot;success&quot;: true
        }
      }
    },
    &quot;a2421e5bf09b3395&quot;: {
      &quot;operation&quot;: &quot;create_flash2&quot;,
      &quot;parameters&quot;: {
        &quot;block_name&quot;: &quot;HP-SEP&quot;
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;block:HP-SEP&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;block:HP-SEP&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;block_name&quot;: &quot;HP-SEP&quot;,
        &quot;block_type&quot;: &quot;FLASH2&quot;,
        &quot;composite&quot;: &quot;HP-SEP!FLASH2&quot;,
        &quot;message&quot;: &quot;Block HP-SEP (FLASH2) created successfully&quot;,
        &quot;block_iteration_floor&quot;: {
          &quot;attempted&quot;: true,
          &quot;floor&quot;: 200,
          &quot;via&quot;: &quot;com_tree&quot;,
          &quot;reason&quot;: &quot;post-block-create&quot;,
          &quot;leaves&quot;: [
            &quot;MAXOL&quot;,
            &quot;MAXIT&quot;
          ],
          &quot;raised&quot;: [
            {
              &quot;block&quot;: &quot;HP-SEP&quot;,
              &quot;leaf&quot;: &quot;MAXIT&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\HP-SEP\\Input\\MAXIT&quot;,
              &quot;before&quot;: 30,
              &quot;after&quot;: 200
            }
          ],
          &quot;unchanged&quot;: [],
          &quot;failed&quot;: [],
          &quot;missing&quot;: [
            {
              &quot;block&quot;: &quot;HP-SEP&quot;,
              &quot;leaf&quot;: &quot;MAXOL&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\HP-SEP\\Input\\MAXOL&quot;,
              &quot;attempted_paths&quot;: [
                &quot;Data\\Blocks\\HP-SEP\\Input\\MAXOL&quot;
              ]
            }
          ],
          &quot;success&quot;: true
        }
      }
    },
    &quot;9d6acd9818f63c1d&quot;: {
      &quot;operation&quot;: &quot;create_fsplit&quot;,
      &quot;parameters&quot;: {
        &quot;block_name&quot;: &quot;VFLOW&quot;
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;block:VFLOW&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;block:VFLOW&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;block_name&quot;: &quot;VFLOW&quot;,
        &quot;block_type&quot;: &quot;FSPLIT&quot;,
        &quot;composite&quot;: &quot;VFLOW!FSPLIT&quot;,
        &quot;message&quot;: &quot;Block VFLOW (FSPLIT) created successfully&quot;,
        &quot;block_iteration_floor&quot;: {
          &quot;attempted&quot;: true,
          &quot;floor&quot;: 200,
          &quot;via&quot;: &quot;com_tree&quot;,
          &quot;reason&quot;: &quot;post-block-create&quot;,
          &quot;leaves&quot;: [
            &quot;MAXOL&quot;,
            &quot;MAXIT&quot;
          ],
          &quot;raised&quot;: [],
          &quot;unchanged&quot;: [],
          &quot;failed&quot;: [],
          &quot;missing&quot;: [
            {
              &quot;block&quot;: &quot;VFLOW&quot;,
              &quot;leaf&quot;: &quot;MAXOL&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\VFLOW\\Input\\MAXOL&quot;,
              &quot;attempted_paths&quot;: [
                &quot;Data\\Blocks\\VFLOW\\Input\\MAXOL&quot;
              ]
            },
            {
              &quot;block&quot;: &quot;VFLOW&quot;,
              &quot;leaf&quot;: &quot;MAXIT&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\VFLOW\\Input\\MAXIT&quot;,
              &quot;attempted_paths&quot;: [
                &quot;Data\\Blocks\\VFLOW\\Input\\MAXIT&quot;
              ]
            }
          ],
          &quot;success&quot;: true
        }
      }
    },
    &quot;315f45151cc00f4e&quot;: {
      &quot;operation&quot;: &quot;create_compr&quot;,
      &quot;parameters&quot;: {
        &quot;block_name&quot;: &quot;COMP&quot;
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;block:COMP&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;block:COMP&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;block_name&quot;: &quot;COMP&quot;,
        &quot;block_type&quot;: &quot;COMPR&quot;,
        &quot;composite&quot;: &quot;COMP!COMPR&quot;,
        &quot;message&quot;: &quot;Block COMP (COMPR) created successfully&quot;,
        &quot;block_iteration_floor&quot;: {
          &quot;attempted&quot;: true,
          &quot;floor&quot;: 200,
          &quot;via&quot;: &quot;com_tree&quot;,
          &quot;reason&quot;: &quot;post-block-create&quot;,
          &quot;leaves&quot;: [
            &quot;MAXOL&quot;,
            &quot;MAXIT&quot;
          ],
          &quot;raised&quot;: [
            {
              &quot;block&quot;: &quot;COMP&quot;,
              &quot;leaf&quot;: &quot;MAXIT&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\COMP\\Input\\MAXIT&quot;,
              &quot;before&quot;: 30,
              &quot;after&quot;: 200
            }
          ],
          &quot;unchanged&quot;: [],
          &quot;failed&quot;: [],
          &quot;missing&quot;: [
            {
              &quot;block&quot;: &quot;COMP&quot;,
              &quot;leaf&quot;: &quot;MAXOL&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\COMP\\Input\\MAXOL&quot;,
              &quot;attempted_paths&quot;: [
                &quot;Data\\Blocks\\COMP\\Input\\MAXOL&quot;
              ]
            }
          ],
          &quot;success&quot;: true
        }
      }
    },
    &quot;608a52d659fb4d06&quot;: {
      &quot;operation&quot;: &quot;create_valve&quot;,
      &quot;parameters&quot;: {
        &quot;block_name&quot;: &quot;VALVE&quot;
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;block:VALVE&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;block:VALVE&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;block_name&quot;: &quot;VALVE&quot;,
        &quot;block_type&quot;: &quot;VALVE&quot;,
        &quot;composite&quot;: &quot;VALVE!VALVE&quot;,
        &quot;message&quot;: &quot;Block VALVE (VALVE) created successfully&quot;,
        &quot;block_iteration_floor&quot;: {
          &quot;attempted&quot;: true,
          &quot;floor&quot;: 200,
          &quot;via&quot;: &quot;com_tree&quot;,
          &quot;reason&quot;: &quot;post-block-create&quot;,
          &quot;leaves&quot;: [
            &quot;MAXOL&quot;,
            &quot;MAXIT&quot;
          ],
          &quot;raised&quot;: [
            {
              &quot;block&quot;: &quot;VALVE&quot;,
              &quot;leaf&quot;: &quot;MAXIT&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\VALVE\\Input\\MAXIT&quot;,
              &quot;before&quot;: 50,
              &quot;after&quot;: 200
            }
          ],
          &quot;unchanged&quot;: [],
          &quot;failed&quot;: [],
          &quot;missing&quot;: [
            {
              &quot;block&quot;: &quot;VALVE&quot;,
              &quot;leaf&quot;: &quot;MAXOL&quot;,
              &quot;path&quot;: &quot;Data\\Blocks\\VALVE\\Input\\MAXOL&quot;,
              &quot;attempted_paths&quot;: [
                &quot;Data\\Blocks\\VALVE\\Input\\MAXOL&quot;
              ]
            }
          ],
          &quot;success&quot;: true
        }
      }
    },
    &quot;46b80b341908af9d&quot;: {
      &quot;operation&quot;: &quot;create_fsplit&quot;,
      &quot;parameters&quot;: {
        &quot;block_name&quot;: &quot;LFLOW&quot;
      },
      &quot;attempts&quot;: 1,
      &quot;successes&quot;: 1,
      &quot;failures&quot;: 0,
      &quot;dependency_domains&quot;: [
        &quot;block:LFLOW&quot;
      ],
      &quot;dependency_versions&quot;: {
        &quot;block:LFLOW&quot;: 1
      },
      &quot;last_status&quot;: &quot;success&quot;,
      &quot;last_evidence&quot;: {
        &quot;success&quot;: true,
        &quot;block_name&quot;: &quot;LFLOW&quot;,
        &quot;block_type&quot;: &quot;FSPLIT&quot;,
        &quot;composite&quot;: &quot;LFLOW!FSPLIT&quot;,
        &quot;message&quot;: &quot;Block LFLOW (FSPLIT) created successfully&quot;,
        &quot;block_iteration_floor&quot;: {
          &quot;attempted&quot;: true,
          &quot;floor&quot;: 200,
          &quot;via&quot;: &quot;com_tree&quot;,
          &quot;reason&quot;: &quot;post-block-create&quot;,
          &quot;leaves&quot;: [
            &quot;MAXOL&quot;,
            &quot;MAXIT&quot;
          ],
          &quot;raised&quot;: [],
          &quot;unchanged&quot;: [],
          &quot;failed&quot;: [],
          &quot;missing&quot;: [
            {

...[context truncated for ReAct baseline prompt]...

ACTIVE_VALIDATOR_REPAIR_CONTEXT:
(none)

Aspen ReAct tool surface (registry-driven facade):
- Call one tool with action=mcp_tool, operation=&lt;name&gt;, parameters=&lt;JSON object&gt;.
- Virtual tools expand to documented Aspen HTTP operations internally through safe_aspen_calls.
- Shared core always includes streams, completion probes, engine_run, and export helpers.
- Shared core native tools: 32; virtual tools: 37.
- The runner starts an Aspen session before the first step.
- Allowed tools for this baseline run:
  - activate_custom_unit_set
  - add_components_by_cas
  - apply_reaction_row_heat_and_selectivity_reporting: Set RStoic HREF_CID/REF_CID/SEL_CID fields coherently for one reaction row.
    parameters: {&#x27;block_name&#x27;: &#x27;string&#x27;, &#x27;reaction_number&#x27;: &#x27;integer&#x27;, &#x27;href_cid&#x27;: &#x27;string (optional)&#x27;, &#x27;ref_cid&#x27;: &#x27;string (optional)&#x27;, &#x27;sel_cid&#x27;: &#x27;string (optional)&#x27;}
  - apply_valve_vendor_preset
  - assert_completion_ready
  - check_binary_interaction_parameters
  - check_block_completion
  - check_flowsheet_completion
  - check_stream_completion
  - collect_compr_power_readback
  - collect_radfrac_profile_markdown_evidence
  - configure_block_property_method
  - configure_calculator_stream_component_makeup_balance
  - configure_compr_pressure_rise
  - configure_condensate_stream: Set a liquid condensate material stream with vapor_fraction=0.
    parameters: {&#x27;stream_name&#x27;: &#x27;string&#x27;, &#x27;temperature&#x27;: &#x27;number (optional)&#x27;, &#x27;pressure&#x27;: &#x27;number (optional)&#x27;, &#x27;temperature_unit&#x27;: &#x27;string (optional)&#x27;, &#x27;pressure_unit&#x27;: &#x27;string (optional)&#x27;}
  - configure_custom_unit_set
  - configure_flash2_operating_specs: Alias for legal Flash2 SPEC_OPT plus typed TEMP/PRES/VFRAC/DUTY writes with mutual-exclusion cleanup.
    parameters: {&#x27;block_name&#x27;: &#x27;string&#x27;, &#x27;spec_opt&#x27;: &#x27;TP|TV|PV|PD|TD|TQ|PQ&#x27;, &#x27;pressure&#x27;: &#x27;number (optional)&#x27;, &#x27;pressure_unit&#x27;: &#x27;string (optional)&#x27;, &#x27;temperature&#x27;: &#x27;number (optional)&#x27;, &#x27;temperature_unit&#x27;: &#x27;string (optional)&#x27;, &#x27;vapor_fraction&#x27;: &#x27;number (optional)&#x27;, &#x27;duty&#x27;: &#x27;number (optional)&#x27;, &#x27;duty_unit&#x27;: &#x27;string (optional)&#x27;}
  - configure_fsplit_shared_outlets
  - configure_heat_stream_duty
  - configure_heat_stream_duty_map: Write DUTY on multiple heat streams, for example Q1..Q4 cascades.
    parameters: {&#x27;duties_by_stream&#x27;: &#x27;object mapping heat-stream names to duty values&#x27;, &#x27;unit&#x27;: &#x27;kJ/hr&#x27;, &#x27;verify_readback&#x27;: &#x27;bool (default true)&#x27;}
  - configure_inset_unit_system
  - configure_pipe_schedule_sizing
  - configure_radfrac_bottom_vapor_feed
  - configure_radfrac_extractive_distillation_pair
  - configure_radfrac_feed_convention
  - configure_radfrac_no_condenser_absorber
  - configure_radfrac_no_condenser_reboiled_bottoms
  - configure_radfrac_partial_vapor_condenser
  - configure_radfrac_total_condenser
  - configure_recycle_convergence_options
  - configure_rstoic_calculated_heat_reference
  - configure_rstoic_flash
  - configure_rstoic_fractional_conversions
  - configure_rstoic_stoichiometry
  - configure_srk_free_water_steamnbs
  - configure_valve_outlet_pressure_design
  - configure_valve_pressure_changer_outlet
  - configure_valve_pressure_changer_pressure_drop
  - connect_flash2_vapor_liquid_ports: Connect Flash2 vapor and liquid outlet ports in one safe helper call.
    parameters: {&#x27;block_name&#x27;: &#x27;string&#x27;, &#x27;feed_stream&#x27;: &#x27;string&#x27;, &#x27;vapor_stream&#x27;: &#x27;string&#x27;, &#x27;liquid_stream&#x27;: &#x27;string&#x27;}
  - connect_material_inlet_outlet: Connect a block material inlet and outlet in one helper call.
    parameters: {&#x27;block_name&#x27;: &#x27;string&#x27;, &#x27;inlet_stream&#x27;: &#x27;string&#x27;, &#x27;outlet_stream&#x27;: &#x27;string&#x27;}
  - connect_material_ports_by_order
  - connect_radfrac_feed_distillate_bottoms: Wire RadFrac feed(s), distillate, and bottoms by role-aware ports.
    parameters: {&#x27;block_name&#x27;: &#x27;string&#x27;, &#x27;inlet_streams&#x27;: [&#x27;F1&#x27;], &#x27;distillate_stream&#x27;: &#x27;D1&#x27;, &#x27;bottoms_stream&#x27;: &#x27;B1&#x27;}
  - connect_shared_material_port_block
  - connect_stream
  - create_block
  - create_compr
  - create_flash2
  - create_fsplit
  - create_heat_stream
  - create_heater
  - create_material_stream
  - create_material_streams
  - create_pipe
  - create_pump
  - create_radfrac
  - create_rstoic
  - create_unit_set_from_base
  - create_valve
  - engine_run
  - ensure_property_method: Ensure a global property method is active with idempotent readback.
    parameters: {&#x27;method&#x27;: &#x27;NRTL|SRK|...&#x27;}
  - export_apw
  - export_final_evidence: Run engine, read PER_ERROR, export REP/APW, and return a bounded diagnostic_summary with same-run REP problem status and repair hints when PER_ERROR is nonzero.
    parameters: {&#x27;run_engine&#x27;: &#x27;bool (optional; default true)&#x27;, &#x27;rep_filename&#x27;: &#x27;string (optional)&#x27;, &#x27;apw_filename&#x27;: &#x27;string (optional)&#x27;, &#x27;export_format&#x27;: &#x27;int (optional; default 2)&#x27;}
  - export_rep
  - export_standard_evidence: Trusted evidence export via safe.export_standard_evidence with REP/APW/BKP paths.
    parameters: {&#x27;script_stem&#x27;: &#x27;string&#x27;, &#x27;task_key&#x27;: &#x27;string&#x27;, &#x27;server_subdir&#x27;: &#x27;string (optional; default script_agent_experiment)&#x27;, &#x27;export_bkp&#x27;: &#x27;bool (optional)&#x27;, &#x27;export_rep&#x27;: &#x27;bool (optional; default true)&#x27;, &#x27;export_apw&#x27;: &#x27;bool (optional)&#x27;}
  - extract_block_ports
  - finalize_task_summary_with_llm_rep_readback: Merge the trusted final Aspen run bundle into summary and collect LLM REP readbacks. Call once only after a successful engine run with PER_ERROR=0 and exported REP/APW evidence.
    parameters: {&#x27;summary&#x27;: &#x27;object (required; current semantic summary)&#x27;, &#x27;final_bundle&#x27;: &#x27;object (required; trusted same-run evidence bundle)&#x27;, &#x27;rep_readback_targets&#x27;: &#x27;array of objects (optional; stream/block/derived/profile targets)&#x27;, &#x27;llm_rep_readback_artifact_dir&#x27;: &#x27;string (optional)&#x27;, &#x27;readbacks&#x27;: &#x27;object (optional; diagnostic readbacks)&#x27;, &#x27;validation_checks&#x27;: &#x27;array (optional)&#x27;, &#x27;required_streams&#x27;: &#x27;array of strings (optional)&#x27;, &#x27;required_blocks&#x27;: &#x27;array of strings (optional)&#x27;, &#x27;stages&#x27;: &#x27;array (optional)&#x27;, &#x27;name_mapping&#x27;: &#x27;object (optional)&#x27;, &#x27;rep_problem_status&#x27;: &#x27;object (optional)&#x27;, &#x27;soft_sanity_checks&#x27;: &#x27;object (optional)&#x27;}
  - get_block_per_error_message
  - get_latest_history
  - get_run_status
  - list_all_blocks
  - list_all_streams
  - list_block_ports
  - node_info
  - node_props
  - probe_model_state
  - read_active_unit_set
  - read_binary_interaction_parameters
  - read_block_heat_duty
  - read_dstwu_results_from_rep: Parse DSTWU results from REP text or a REP file path.
    parameters: {&#x27;block_name&#x27;: &#x27;string&#x27;, &#x27;rep_path&#x27;: &#x27;string (optional; provide rep_path or rep_text)&#x27;, &#x27;rep_text&#x27;: &#x27;string (optional; provide rep_text or rep_path)&#x27;, &#x27;feed_tray_convention&#x27;: &#x27;string (optional; default stages_above_feed)&#x27;}
  - read_dstwu_shortcut_basis
  - read_global_property_method
  - read_heater_duty
  - read_pressure_state
  - read_stream_mole_fractions
  - read_stream_output
  - read_stream_outputs: Batch read stream temperature, pressure, vapor fraction, and component flows.
    parameters: {&#x27;stream_name&#x27;: &#x27;string&#x27;, &#x27;components&#x27;: &#x27;array of component IDs (optional)&#x27;, &#x27;basis&#x27;: &#x27;mole_flow|mole_fraction|mass_flow (optional; default mole_flow)&#x27;}
  - run_completion_engine_and_export
  - run_standard_probe_matrix
  - scan_radfrac_bottoms_for_component_recovery
  - set_area
  - set_basis_br
  - set_basis_mixed
  - set_basis_rdv
  - set_basis_vn
  - set_block_reaction_stoichiometry
  - set_block_value
  - set_check_choke
  - set_conv_meth
  - set_d_f
  - set_deff
  - set_delp
  - set_dep_var
  - set_eff
  - set_energy_bal
  - set_flow_mixed
  - set_frac
  - set_fracs
  - set_heat_duty
  - set_heat_of_reac
  - set_heater_flash_spec
  - set_heater_pressure
  - set_heater_temperature
  - set_heatopt
  - set_href_cid
  - set_in_diam
  - set_indep_var
  - set_length
  - set_material
  - set_material_stream: Safe helper wrapper for mixed-spec, basis, state, and component flows on one material stream.
    parameters: {&#x27;stream_name&#x27;: &#x27;string&#x27;, &#x27;mixed_spec&#x27;: &#x27;TP|TV|PV (optional)&#x27;, &#x27;basis&#x27;: &#x27;MOLE-FLOW|MOLE-FRAC|MASS-FLOW (optional)&#x27;, &#x27;flows&#x27;: &#x27;object mapping component IDs to values (optional)&#x27;, &#x27;temperature&#x27;: &#x27;number (optional)&#x27;, &#x27;pressure&#x27;: &#x27;number (optional)&#x27;, &#x27;vapor_fraction&#x27;: &#x27;number (optional)&#x27;}
  - set_material_stream_composition: Set material stream basis and component flows or fractions.
    parameters: {&#x27;stream_name&#x27;: &#x27;string&#x27;, &#x27;basis&#x27;: &#x27;MOLE-FLOW|MOLE-FRAC|MASS-FLOW (optional; default MOLE-FLOW)&#x27;, &#x27;flows&#x27;: &#x27;object mapping component IDs to values (optional; aliases composition/components)&#x27;, &#x27;composition&#x27;: &#x27;alias for flows&#x27;, &#x27;components&#x27;: &#x27;alias for flows&#x27;, &#x27;flow_unit&#x27;: &#x27;string (optional; default kmol/hr)&#x27;, &#x27;total_flow&#x27;: &#x27;number (optional; required only when basis is MOLE-FRAC)&#x27;}
  - set_material_stream_conditions: Set material stream state spec (TP/TV/PV) plus optional basis/total flow.
    parameters: {&#x27;stream_name&#x27;: &#x27;string&#x27;, &#x27;temperature&#x27;: &#x27;number (optional)&#x27;, &#x27;temperature_unit&#x27;: &#x27;string (optional, e.g. C)&#x27;, &#x27;pressure&#x27;: &#x27;number (optional)&#x27;, &#x27;pressure_unit&#x27;: &#x27;string (optional, e.g. atm)&#x27;, &#x27;vapor_fraction&#x27;: &#x27;number (optional)&#x27;, &#x27;mixed_spec&#x27;: &#x27;TP|TV|PV (optional; inferred from provided fields)&#x27;}
  - set_maxol
  - set_meff
  - set_mixed_spec_mixed
  - set_mode
  - set_nominal_diam
  - set_npa
  - set_opt_cformat
  - set_opt_ctype
  - set_opt_design
  - set_opt_diam
  - set_p_drop
  - set_p_out
  - set_pdrp_fac
  - set_peff
  - set_petrofrac_operating_specs
  - set_petrofrac_pumparound_specs
  - set_petrofrac_side_stripper_specs
  - set_power
  - set_pratio
  - set_prec_fac
  - set_pres_mixed
  - set_prod_flow
  - set_prod_phase
  - set_prod_stage
  - set_property_method
  - set_pump_curve_table: Replace one Pump TABLE performance-curve slot with explicit flow/head rows.
    parameters: {&#x27;block_name&#x27;: &#x27;string&#x27;, &#x27;curve_points&#x27;: &#x27;array of {flow: number, head: number}&#x27;, &#x27;flow_unit&#x27;: &#x27;string (required)&#x27;, &#x27;head_unit&#x27;: &#x27;string (required)&#x27;, &#x27;curve_idx&#x27;: &#x27;integer (default 1)&#x27;}
  - set_pump_outlet_pressure
  - set_pump_outlet_spec
  - set_radfrac_condenser_type
  - set_radfrac_distillate_rate
  - set_radfrac_feed_stage
  - set_radfrac_reboiler_type
  - set_radfrac_reflux_ratio
  - set_radfrac_stage_count
  - set_radfrac_top_pressure
  - set_schedule
  - set_stream_flash_specs: Configure Flash2 operating spec route through typed setters, preserving Aspen mutual-exclusion cleanup.
    parameters: {&#x27;block_name&#x27;: &#x27;string&#x27;, &#x27;spec_opt&#x27;: &#x27;TP|TV|PV|PD|TD|TQ|PQ&#x27;, &#x27;pressure&#x27;: &#x27;number (optional)&#x27;, &#x27;pressure_unit&#x27;: &#x27;string (optional)&#x27;, &#x27;temperature&#x27;: &#x27;number (optional)&#x27;, &#x27;temperature_unit&#x27;: &#x27;string (optional)&#x27;, &#x27;vapor_fraction&#x27;: &#x27;number (optional)&#x27;, &#x27;duty&#x27;: &#x27;number (optional)&#x27;, &#x27;duty_unit&#x27;: &#x27;string (optional)&#x27;}
  - set_table_label
  - set_temp_mixed
  - set_totflow_mixed
  - set_type
  - set_unit_set_quantity
  - set_vfrac_mixed
  - ui_check_next_completion_status
  - ui_set_rstoic_flash_spec_pq
  - unitset_activate
  - unitset_create_from_base
  - unitset_read
  - unitset_set_quantity
  - validate_material_edge_plan
  - validate_required_native_blocks_plan
  - verify_custom_unit_set

DYNAMIC_OPERATION_EXPOSURE:
This step exposes schema/details for 173 operations. The facade retains 4979 executable profile capabilities, but undisclosed names are intentionally omitted from the action prompt to avoid repeated catalog-token overhead. Use the exposed operations; the selector refreshes the visible surface periodically and after tool or validation errors. Function-like names appearing only in prose, examples, annotations, or implementation notes are not callable tools.

STEP: 2 (budget-limited; no step cap)
OBSERVATION_CONTEXT:
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  &quot;observation_count&quot;: 0
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    &quot;event&quot;: &quot;preflight&quot;,
    &quot;health&quot;: {
      &quot;status&quot;: &quot;healthy&quot;
    },
    &quot;task_hash&quot;: &quot;&lt;REDACTED_TASK_ID&gt;&quot;
  },
  {
    &quot;event&quot;: &quot;session_started&quot;
  },
  {
    &quot;truncated&quot;: true,
    &quot;chars&quot;: 9822,
    &quot;preview&quot;: &quot;{\&quot;event\&quot;: \&quot;plan_result\&quot;, \&quot;actions_requested\&quot;: 25, \&quot;actions_executed\&quot;: 25, \&quot;stopped_on_error\&quot;: false, \&quot;first_error_index\&quot;: null, \&quot;pending_action_count\&quot;: 0, \&quot;action_outcomes\&quot;: [{\&quot;event\&quot;: \&quot;tool_result\&quot;, \&quot;operation\&quot;: \&quot;add_components_by_cas\&quot;, \&quot;parameters\&quot;: {\&quot;components\&quot;: [{\&quot;component_id\&quot;: \&quot;H2\&quot;, \&quot;cas\&quot;: \&quot;1333-74-0\&quot;}, {\&quot;component_id\&quot;: \&quot;N2\&quot;, \&quot;cas\&quot;: \&quot;7727-37-9\&quot;}, {\&quot;component_id\&quot;: \&quot;CH4\&quot;, \&quot;cas\&quot;: \&quot;74-82-8\&quot;}, {\&quot;component_id\&quot;: \&quot;BENZENE\&quot;, \&quot;cas\&quot;: \&quot;71-43-2\&quot;}, {\&quot;component_id\&quot;: \&quot;CYCLOHEX\&quot;, \&quot;cas\&quot;: \&quot;110-82-7\&quot;}]}, \&quot;facade\&quot;: true, \&quot;translated_operations\&quot;: [], \&quot;response_status\&quot;: \&quot;success\&quot;, \&quot;result\&quot;: {\&quot;success\&quot;: true, \&quot;message\&quot;: \&quot;Added 5 component(s) successfully\&quot;}}, {\&quot;truncated\&quot;: true, \&quot;chars\&quot;: 525, \&quot;preview\&quot;: \&quot;{\\\&quot;event\\\&quot;: \\\&quot;tool_result\\\&quot;, \\\&quot;operation\\\&quot;: \\\&quot;ensure_property_method\\\&quot;, \\\&quot;parameters\\\&quot;: {\\\&quot;method\\\&quot;: \\\&quot;RK-SOAVE\\\&quot;}, \\\&quot;facade\\\&quot;: true, \\\&quot;translated_operations\\\&quot;: [{\\\&quot;operation\\\&quot;: \\\&quot;set_property_method\\\&quot;, \\\&quot;success\\\&quot;: true, \\\&quot;error\\\&quot;: null}, {\\\&quot;operation\\\&quot;: \\\&quot;set_variable\\\&quot;, \\\&quot;success\\\&quot;: true, \\\&quot;error\\\&quot;: null}, {\\\&quot;operation\\\&quot;: \\\&quot;set_variable\\\&quot;, \\\&quot;success\\\&quot;: true, \\\&quot;error\\\&quot;: null}, {\\\&quot;operation\\\&quot;: \\\&quot;get_variable\\\&quot;, \\\&quot;success\\\&quot;: true, \\\&quot;error\\\&quot;: null}, {\\\&quot;operation\\\&quot;: \\\&quot;ge\\n...[truncated]\&quot;}, {\&quot;truncated\&quot;: true, \&quot;chars\&quot;: 1611, \&quot;preview\&quot;: \&quot;{\\\&quot;event\\\&quot;: \\\&quot;tool_result\\\&quot;, \\\&quot;operation\\\&quot;: \\\&quot;create_material_streams\\\&quot;, \\\&quot;parameters\\\&quot;: {\\\&quot;stream_names\\\&quot;: [\\\&quot;BZIN\\\&quot;, \\\&quot;H2IN\\\&quot;, \\\&quot;BZIN2\\\&quot;, \\\&quot;H2RCY2\\\&quot;, \\\&quot;RXIN\\\&quot;, \\\&quot;RXOUT\\\&quot;, \\\&quot;VAP\\\&quot;, \\\&quot;H2RCY\\\&quot;, \\\&quot;PURGE\\\&quot;, \\\&quot;PURGE2\\\&quot;, \\\&quot;LIQ\\\&quot;, \\\&quot;COLFD\\\&quot;, \\\&quot;CHRCY\\\&quot;, \\\&quot;CHRCY2\\\&quot;, \\\&quot;CHRCY3\\\&quot;, \\\&quot;LTENDS\\\&quot;, \\\&quot;PRODUCT\\\&quot;]}, \\\&quot;facade\\\&quot;: true, \\\&quot;translated_operations\\\&quot;: [{\\\&quot;operation\\\&quot;: \\\&quot;create_material_streams\\\&quot;, \\\&quot;success\\\&quot;: true, \\\&quot;error\\\&quot;: null}, {\\\&quot;operation\\\&quot;: \\\&quot;create_material_streams\\\&quot;, \\\&quot;success\\\&quot;: \\n...[truncated]\&quot;}, {\&quot;event\&quot;: \&quot;tool_result\&quot;, \&quot;operation\&quot;: \&quot;create_pump\&quot;, \&quot;parameters\&quot;: {\&quot;block_name\&quot;: \&quot;FEEDPUMP\&quot;}, \&quot;facade\&quot;: true, \&quot;translated_operations\&quot;: [], \&quot;response_status\&quot;: \&quot;success\&quot;, \&quot;result\&quot;: {\&quot;success\&quot;: true, \&quot;message\&quot;: \&quot;Block FEEDPUMP (PUMP) created successfully\&quot;, \&quot;block_name\&quot;: \&quot;FEEDPUMP\&quot;}}, {\&quot;event\&quot;: \&quot;tool_result\&quot;, \&quot;operation\&quot;: \&quot;create_heater\&quot;, \&quot;parameters\&quot;: {\&quot;block_name\&quot;: \&quot;FEED-MIX\&quot;}, \&quot;facade\&quot;: true, \&quot;translated_operations\&quot;: [], \&quot;response_status\&quot;: \&quot;success\&quot;, \&quot;result\&quot;: {\&quot;success\&quot;: true, \&quot;message\&quot;: \&quot;Block FEED-MIX (HEATER) created successfully\&quot;, \&quot;block_name\&quot;: \&quot;FEED-MIX\&quot;}}, {\&quot;event\&quot;: \&quot;tool_result\&quot;, \&quot;operation\&quot;: \&quot;create_rstoic\&quot;, \&quot;parameters\&quot;: {\&quot;block_name\&quot;: \&quot;REACT\&quot;}, \&quot;facade\&quot;: true, \n...[truncated]&quot;
  }
]

Choose the next JSON action.</code></pre>

</details>

## Raw model output

<details open><summary>Show output</summary>

<pre><code>{&quot;thought&quot;:&quot;Topology and core specs are created but not connected/configured; batch the figure-backed connections and task specs using typed helpers, leaving run/evidence for after completion repair.&quot;,&quot;action&quot;:&quot;mcp_plan&quot;,&quot;parameters&quot;:{&quot;actions&quot;:[{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;inlet_stream&quot;:&quot;BZIN&quot;,&quot;outlet_stream&quot;:&quot;BZIN2&quot;}},{&quot;operation&quot;:&quot;connect_shared_material_port_block&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEED-MIX&quot;,&quot;inlet_streams&quot;:[&quot;BZIN2&quot;,&quot;H2IN&quot;,&quot;H2RCY2&quot;,&quot;CHRCY3&quot;],&quot;outlet_streams&quot;:[&quot;RXIN&quot;]}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;REACT&quot;,&quot;inlet_stream&quot;:&quot;RXIN&quot;,&quot;outlet_stream&quot;:&quot;RXOUT&quot;}},{&quot;operation&quot;:&quot;connect_flash2_vapor_liquid_ports&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;HP-SEP&quot;,&quot;feed_stream&quot;:&quot;RXOUT&quot;,&quot;vapor_stream&quot;:&quot;VAP&quot;,&quot;liquid_stream&quot;:&quot;LIQ&quot;}},{&quot;operation&quot;:&quot;configure_fsplit_shared_outlets&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;VFLOW&quot;,&quot;inlet_stream&quot;:&quot;VAP&quot;,&quot;outlet_streams&quot;:[&quot;H2RCY&quot;,&quot;PURGE&quot;],&quot;split_fractions&quot;:{&quot;H2RCY&quot;:0.92}}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COMP&quot;,&quot;inlet_stream&quot;:&quot;H2RCY&quot;,&quot;outlet_stream&quot;:&quot;H2RCY2&quot;}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;VALVE&quot;,&quot;inlet_stream&quot;:&quot;PURGE&quot;,&quot;outlet_stream&quot;:&quot;PURGE2&quot;}},{&quot;operation&quot;:&quot;configure_fsplit_shared_outlets&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;LFLOW&quot;,&quot;inlet_stream&quot;:&quot;LIQ&quot;,&quot;outlet_streams&quot;:[&quot;CHRCY&quot;,&quot;COLFD&quot;],&quot;split_fractions&quot;:{&quot;CHRCY&quot;:0.30}}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PUMP&quot;,&quot;inlet_stream&quot;:&quot;CHRCY&quot;,&quot;outlet_stream&quot;:&quot;CHRCY2&quot;}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PIPE&quot;,&quot;inlet_stream&quot;:&quot;CHRCY2&quot;,&quot;outlet_stream&quot;:&quot;CHRCY3&quot;}},{&quot;operation&quot;:&quot;connect_stream&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;COLFD&quot;,&quot;port_name&quot;:&quot;F(IN)&quot;}},{&quot;operation&quot;:&quot;connect_stream&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;LTENDS&quot;,&quot;port_name&quot;:&quot;VD(OUT)&quot;}},{&quot;operation&quot;:&quot;connect_stream&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;PRODUCT&quot;,&quot;port_name&quot;:&quot;B(OUT)&quot;}},{&quot;operation&quot;:&quot;set_material_stream_conditions&quot;,&quot;parameters&quot;:{&quot;stream_name&quot;:&quot;H2IN&quot;,&quot;mixed_spec&quot;:&quot;TP&quot;,&quot;temperature&quot;:50.0,&quot;temperature_unit&quot;:&quot;C&quot;,&quot;pressure&quot;:2.5,&quot;pressure_unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;set_material_stream_composition&quot;,&quot;parameters&quot;:{&quot;stream_name&quot;:&quot;H2IN&quot;,&quot;basis&quot;:&quot;MOLE-FLOW&quot;,&quot;flows&quot;:{&quot;H2&quot;:321.75,&quot;N2&quot;:1.65,&quot;CH4&quot;:6.6},&quot;flow_unit&quot;:&quot;kmol/hr&quot;}},{&quot;operation&quot;:&quot;set_material_stream_conditions&quot;,&quot;parameters&quot;:{&quot;stream_name&quot;:&quot;BZIN&quot;,&quot;mixed_spec&quot;:&quot;TP&quot;,&quot;temperature&quot;:40.0,&quot;temperature_unit&quot;:&quot;C&quot;,&quot;pressure&quot;:0.1,&quot;pressure_unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;set_material_stream_composition&quot;,&quot;parameters&quot;:{&quot;stream_name&quot;:&quot;BZIN&quot;,&quot;basis&quot;:&quot;MOLE-FLOW&quot;,&quot;flows&quot;:{&quot;BENZENE&quot;:100.0},&quot;flow_unit&quot;:&quot;kmol/hr&quot;}},{&quot;operation&quot;:&quot;set_pump_outlet_spec&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;USE-CURVE&quot;}},{&quot;operation&quot;:&quot;set_opt_ctype&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;SINGLE-OPER&quot;}},{&quot;operation&quot;:&quot;set_opt_cformat&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;TABLE&quot;}},{&quot;operation&quot;:&quot;set_dep_var&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;HEAD&quot;}},{&quot;operation&quot;:&quot;set_indep_var&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;VOL-FLOW&quot;}},{&quot;operation&quot;:&quot;set_pump_curve_table&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;curve_idx&quot;:1,&quot;flow_unit&quot;:&quot;m3/hr&quot;,&quot;head_unit&quot;:&quot;m&quot;,&quot;curve_points&quot;:[{&quot;flow&quot;:20.0,&quot;head&quot;:40.0},{&quot;flow&quot;:10.0,&quot;head&quot;:250.0},{&quot;flow&quot;:5.0,&quot;head&quot;:300.0},{&quot;flow&quot;:3.0,&quot;head&quot;:400.0}]}},{&quot;operation&quot;:&quot;set_eff&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:0.6}},{&quot;operation&quot;:&quot;set_deff&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:0.9}},{&quot;operation&quot;:&quot;set_heater_flash_spec&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEED-MIX&quot;,&quot;value&quot;:&quot;TP&quot;}},{&quot;operation&quot;:&quot;set_heater_temperature&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEED-MIX&quot;,&quot;value&quot;:150.0,&quot;unit&quot;:&quot;C&quot;}},{&quot;operation&quot;:&quot;set_heater_pressure&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEED-MIX&quot;,&quot;value&quot;:2.3,&quot;unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;configure_rstoic_stoichiometry&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;REACT&quot;,&quot;reaction_number&quot;:1,&quot;reactants&quot;:{&quot;BENZENE&quot;:1.0,&quot;H2&quot;:3.0},&quot;products&quot;:{&quot;CYCLOHEX&quot;:1.0}}},{&quot;operation&quot;:&quot;configure_rstoic_fractional_conversions&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;REACT&quot;,&quot;conversions&quot;:[{&quot;reaction_number&quot;:1,&quot;component_id&quot;:&quot;BENZENE&quot;,&quot;conversion&quot;:0.998}]}},{&quot;operation&quot;:&quot;configure_rstoic_flash&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;REACT&quot;,&quot;spec_opt&quot;:&quot;TP&quot;,&quot;temperature&quot;:200.0,&quot;temperature_unit&quot;:&quot;C&quot;,&quot;pressure&quot;:-0.1,&quot;pressure_unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;configure_flash2_operating_specs&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;HP-SEP&quot;,&quot;spec_opt&quot;:&quot;TP&quot;,&quot;temperature&quot;:50.0,&quot;temperature_unit&quot;:&quot;C&quot;,&quot;pressure&quot;:-0.05,&quot;pressure_unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;set_pump_outlet_spec&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PUMP&quot;,&quot;value&quot;:&quot;PRES&quot;}},{&quot;operation&quot;:&quot;set_pump_outlet_pressure&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PUMP&quot;,&quot;value&quot;:2.6,&quot;unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;configure_compr_pressure_rise&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COMP&quot;,&quot;delta_pressure&quot;:0.4,&quot;pressure_unit&quot;:&quot;MPa&quot;,&quot;compressor_type&quot;:&quot;ISENTROPIC&quot;}},{&quot;operation&quot;:&quot;configure_valve_outlet_pressure_design&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;VALVE&quot;,&quot;outlet_pressure&quot;:2.0,&quot;pressure_unit&quot;:&quot;MPa&quot;,&quot;vendor_preset_id&quot;:&quot;neles_globe_v810_equal_pct_1p5in&quot;}},{&quot;operation&quot;:&quot;configure_pipe_schedule_sizing&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PIPE&quot;,&quot;material&quot;:&quot;CARBON-STEEL&quot;,&quot;schedule&quot;:40,&quot;nominal_diam&quot;:&quot;1-IN&quot;,&quot;length&quot;:25.0,&quot;length_unit&quot;:&quot;meter&quot;}},{&quot;operation&quot;:&quot;set_radfrac_condenser_type&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:&quot;PARTIAL-V&quot;}},{&quot;operation&quot;:&quot;set_radfrac_reboiler_type&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:&quot;KETTLE&quot;}},{&quot;operation&quot;:&quot;set_radfrac_stage_count&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:12}},{&quot;operation&quot;:&quot;set_radfrac_feed_stage&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;COLFD&quot;,&quot;value&quot;:8}},{&quot;operation&quot;:&quot;configure_radfrac_feed_convention&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;COLFD&quot;,&quot;convention&quot;:&quot;ON-STAGE-LIQ&quot;}},{&quot;operation&quot;:&quot;set_radfrac_top_pressure&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:1.5,&quot;unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;set_radfrac_reflux_ratio&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:1.2}},{&quot;operation&quot;:&quot;set_radfrac_distillate_rate&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:99.0,&quot;unit&quot;:&quot;kmol/hr&quot;}},{&quot;operation&quot;:&quot;configure_recycle_convergence_options&quot;,&quot;parameters&quot;:{&quot;tolerance&quot;:1e-5,&quot;tear_method&quot;:&quot;WEGSTEIN&quot;,&quot;wegstein_max_iterations&quot;:200}},{&quot;operation&quot;:&quot;probe_model_state&quot;,&quot;parameters&quot;:{&quot;stream_names&quot;:[&quot;BZIN&quot;,&quot;H2IN&quot;,&quot;PRODUCT&quot;],&quot;block_names&quot;:[&quot;FEEDPUMP&quot;,&quot;FEED-MIX&quot;,&quot;REACT&quot;,&quot;HP-SEP&quot;,&quot;VFLOW&quot;,&quot;LFLOW&quot;,&quot;COLUMN&quot;],&quot;include_flowsheet&quot;:true,&quot;include_ui_next&quot;:false}}]}}

{&quot;thought&quot;:&quot;Batch topology and all primary equipment/feed specifications now; defer run/evidence until completion status is known.&quot;,&quot;action&quot;:&quot;mcp_plan&quot;,&quot;parameters&quot;:{&quot;actions&quot;:[{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;inlet_stream&quot;:&quot;BZIN&quot;,&quot;outlet_stream&quot;:&quot;BZIN2&quot;}},{&quot;operation&quot;:&quot;connect_shared_material_port_block&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEED-MIX&quot;,&quot;inlet_streams&quot;:[&quot;BZIN2&quot;,&quot;H2IN&quot;,&quot;H2RCY2&quot;,&quot;CHRCY3&quot;],&quot;outlet_streams&quot;:[&quot;RXIN&quot;]}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;REACT&quot;,&quot;inlet_stream&quot;:&quot;RXIN&quot;,&quot;outlet_stream&quot;:&quot;RXOUT&quot;}},{&quot;operation&quot;:&quot;connect_flash2_vapor_liquid_ports&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;HP-SEP&quot;,&quot;feed_stream&quot;:&quot;RXOUT&quot;,&quot;vapor_stream&quot;:&quot;VAP&quot;,&quot;liquid_stream&quot;:&quot;LIQ&quot;}},{&quot;operation&quot;:&quot;configure_fsplit_shared_outlets&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;VFLOW&quot;,&quot;inlet_stream&quot;:&quot;VAP&quot;,&quot;outlet_streams&quot;:[&quot;H2RCY&quot;,&quot;PURGE&quot;],&quot;split_fractions&quot;:{&quot;H2RCY&quot;:0.92}}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COMP&quot;,&quot;inlet_stream&quot;:&quot;H2RCY&quot;,&quot;outlet_stream&quot;:&quot;H2RCY2&quot;}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;VALVE&quot;,&quot;inlet_stream&quot;:&quot;PURGE&quot;,&quot;outlet_stream&quot;:&quot;PURGE2&quot;}},{&quot;operation&quot;:&quot;configure_fsplit_shared_outlets&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;LFLOW&quot;,&quot;inlet_stream&quot;:&quot;LIQ&quot;,&quot;outlet_streams&quot;:[&quot;CHRCY&quot;,&quot;COLFD&quot;],&quot;split_fractions&quot;:{&quot;CHRCY&quot;:0.3}}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PUMP&quot;,&quot;inlet_stream&quot;:&quot;CHRCY&quot;,&quot;outlet_stream&quot;:&quot;CHRCY2&quot;}},{&quot;operation&quot;:&quot;connect_material_inlet_outlet&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PIPE&quot;,&quot;inlet_stream&quot;:&quot;CHRCY2&quot;,&quot;outlet_stream&quot;:&quot;CHRCY3&quot;}},{&quot;operation&quot;:&quot;connect_stream&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;COLFD&quot;,&quot;port_name&quot;:&quot;F(IN)&quot;}},{&quot;operation&quot;:&quot;connect_stream&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;LTENDS&quot;,&quot;port_name&quot;:&quot;VD(OUT)&quot;}},{&quot;operation&quot;:&quot;connect_stream&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;PRODUCT&quot;,&quot;port_name&quot;:&quot;B(OUT)&quot;}},{&quot;operation&quot;:&quot;set_material_stream_conditions&quot;,&quot;parameters&quot;:{&quot;stream_name&quot;:&quot;H2IN&quot;,&quot;mixed_spec&quot;:&quot;TP&quot;,&quot;temperature&quot;:50.0,&quot;temperature_unit&quot;:&quot;C&quot;,&quot;pressure&quot;:2.5,&quot;pressure_unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;set_material_stream_composition&quot;,&quot;parameters&quot;:{&quot;stream_name&quot;:&quot;H2IN&quot;,&quot;basis&quot;:&quot;MOLE-FLOW&quot;,&quot;flows&quot;:{&quot;H2&quot;:321.75,&quot;N2&quot;:1.65,&quot;CH4&quot;:6.6},&quot;flow_unit&quot;:&quot;kmol/hr&quot;}},{&quot;operation&quot;:&quot;set_material_stream_conditions&quot;,&quot;parameters&quot;:{&quot;stream_name&quot;:&quot;BZIN&quot;,&quot;mixed_spec&quot;:&quot;TP&quot;,&quot;temperature&quot;:40.0,&quot;temperature_unit&quot;:&quot;C&quot;,&quot;pressure&quot;:0.1,&quot;pressure_unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;set_material_stream_composition&quot;,&quot;parameters&quot;:{&quot;stream_name&quot;:&quot;BZIN&quot;,&quot;basis&quot;:&quot;MOLE-FLOW&quot;,&quot;flows&quot;:{&quot;BENZENE&quot;:100.0},&quot;flow_unit&quot;:&quot;kmol/hr&quot;}},{&quot;operation&quot;:&quot;set_pump_outlet_spec&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;USE-CURVE&quot;}},{&quot;operation&quot;:&quot;set_opt_ctype&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;SINGLE-OPER&quot;}},{&quot;operation&quot;:&quot;set_opt_cformat&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;TABLE&quot;}},{&quot;operation&quot;:&quot;set_dep_var&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;HEAD&quot;}},{&quot;operation&quot;:&quot;set_indep_var&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:&quot;VOL-FLOW&quot;}},{&quot;operation&quot;:&quot;set_pump_curve_table&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;curve_idx&quot;:1,&quot;flow_unit&quot;:&quot;m3/hr&quot;,&quot;head_unit&quot;:&quot;m&quot;,&quot;curve_points&quot;:[{&quot;flow&quot;:20.0,&quot;head&quot;:40.0},{&quot;flow&quot;:10.0,&quot;head&quot;:250.0},{&quot;flow&quot;:5.0,&quot;head&quot;:300.0},{&quot;flow&quot;:3.0,&quot;head&quot;:400.0}]}},{&quot;operation&quot;:&quot;set_eff&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:0.6}},{&quot;operation&quot;:&quot;set_deff&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEEDPUMP&quot;,&quot;value&quot;:0.9}},{&quot;operation&quot;:&quot;set_heater_flash_spec&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEED-MIX&quot;,&quot;value&quot;:&quot;TP&quot;}},{&quot;operation&quot;:&quot;set_heater_temperature&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEED-MIX&quot;,&quot;value&quot;:150.0,&quot;unit&quot;:&quot;C&quot;}},{&quot;operation&quot;:&quot;set_heater_pressure&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;FEED-MIX&quot;,&quot;value&quot;:2.3,&quot;unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;configure_rstoic_stoichiometry&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;REACT&quot;,&quot;reaction_number&quot;:1,&quot;reactants&quot;:{&quot;BENZENE&quot;:1.0,&quot;H2&quot;:3.0},&quot;products&quot;:{&quot;CYCLOHEX&quot;:1.0}}},{&quot;operation&quot;:&quot;configure_rstoic_fractional_conversions&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;REACT&quot;,&quot;conversions&quot;:[{&quot;reaction_number&quot;:1,&quot;component_id&quot;:&quot;BENZENE&quot;,&quot;conversion&quot;:0.998}]}},{&quot;operation&quot;:&quot;configure_rstoic_flash&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;REACT&quot;,&quot;spec_opt&quot;:&quot;TP&quot;,&quot;temperature&quot;:200.0,&quot;temperature_unit&quot;:&quot;C&quot;,&quot;pressure&quot;:-0.1,&quot;pressure_unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;configure_flash2_operating_specs&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;HP-SEP&quot;,&quot;spec_opt&quot;:&quot;TP&quot;,&quot;temperature&quot;:50.0,&quot;temperature_unit&quot;:&quot;C&quot;,&quot;pressure&quot;:-0.05,&quot;pressure_unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;set_pump_outlet_spec&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PUMP&quot;,&quot;value&quot;:&quot;PRES&quot;}},{&quot;operation&quot;:&quot;set_pump_outlet_pressure&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PUMP&quot;,&quot;value&quot;:2.6,&quot;unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;configure_compr_pressure_rise&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COMP&quot;,&quot;delta_pressure&quot;:0.4,&quot;pressure_unit&quot;:&quot;MPa&quot;,&quot;compressor_type&quot;:&quot;ISENTROPIC&quot;}},{&quot;operation&quot;:&quot;configure_valve_outlet_pressure_design&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;VALVE&quot;,&quot;outlet_pressure&quot;:2.0,&quot;pressure_unit&quot;:&quot;MPa&quot;,&quot;vendor_preset_id&quot;:&quot;neles_globe_v810_equal_pct_1p5in&quot;}},{&quot;operation&quot;:&quot;configure_pipe_schedule_sizing&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;PIPE&quot;,&quot;material&quot;:&quot;CARBON-STEEL&quot;,&quot;schedule&quot;:40,&quot;nominal_diam&quot;:&quot;1-IN&quot;,&quot;length&quot;:25.0,&quot;length_unit&quot;:&quot;meter&quot;}},{&quot;operation&quot;:&quot;set_radfrac_condenser_type&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:&quot;PARTIAL-V&quot;}},{&quot;operation&quot;:&quot;set_radfrac_reboiler_type&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:&quot;KETTLE&quot;}},{&quot;operation&quot;:&quot;set_radfrac_stage_count&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:12}},{&quot;operation&quot;:&quot;set_radfrac_feed_stage&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;COLFD&quot;,&quot;value&quot;:8}},{&quot;operation&quot;:&quot;configure_radfrac_feed_convention&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;stream_name&quot;:&quot;COLFD&quot;,&quot;convention&quot;:&quot;ON-STAGE-LIQ&quot;}},{&quot;operation&quot;:&quot;set_radfrac_top_pressure&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:1.5,&quot;unit&quot;:&quot;MPa&quot;}},{&quot;operation&quot;:&quot;set_radfrac_reflux_ratio&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:1.2}},{&quot;operation&quot;:&quot;set_radfrac_distillate_rate&quot;,&quot;parameters&quot;:{&quot;block_name&quot;:&quot;COLUMN&quot;,&quot;value&quot;:99.0,&quot;unit&quot;:&quot;kmol/hr&quot;}},{&quot;operation&quot;:&quot;configure_recycle_convergence_options&quot;,&quot;parameters&quot;:{&quot;tolerance&quot;:1e-5,&quot;tear_method&quot;:&quot;WEGSTEIN&quot;,&quot;wegstein_max_iterations&quot;:200}},{&quot;operation&quot;:&quot;probe_model_state&quot;,&quot;parameters&quot;:{&quot;stream_names&quot;:[&quot;BZIN&quot;,&quot;H2IN&quot;,&quot;PRODUCT&quot;],&quot;block_names&quot;:[&quot;FEEDPUMP&quot;,&quot;FEED-MIX&quot;,&quot;REACT&quot;,&quot;HP-SEP&quot;,&quot;VFLOW&quot;,&quot;LFLOW&quot;,&quot;COLUMN&quot;],&quot;include_flowsheet&quot;:true,&quot;include_ui_next&quot;:false}}]}}</code></pre>

</details>
