# ReAct main-control LLM calls
> **At a glance:** 10 sequential `select_action` calls · 1,309,384 input tokens · 10,602 output tokens · 1,319,986 total tokens · $6.864980.
> Provider token telemetry and raw model outputs are exact persisted records. Literal input message bodies were not persisted by the original runner; the inputs below are deterministic reconstructions from the persisted task/context artifacts, memory rules, and prior observations. Each call retains the exact recorded provider token counts. Local paths and run/session identifiers are redacted.
## Shared input repeated on every ReAct call

### System message

```text
You are a ReAct baseline agent for Aspen Plus through an MCP-like HTTP tool surface.

You are not writing a Python script. You must solve the task by repeatedly choosing one JSON action.
Use the provided skills/context as operational policy. Prefer high-level documented operations when available.

Return exactly one JSON object, no markdown fences:
{
  "thought": "brief private working note",
  "action": "mcp_tool" | "mcp_plan" | "finalize",
  "operation": "Aspen operation name when action=mcp_tool",
  "parameters": {"name": "value"},
  "final_summary": {"case_id": "...", "ok": true, "evidence": {}, "results": {}, "self_validation": {}}
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

```

### Task and context block

```text
### FILE: tasks/test/chn/chapter_05/exercise_5_1.md
Reason: target task statement
` ` `text
# 习题 5.1

![习题 5.1 流程图](./images/exercise_5_1_flow.png)

附图为环己烷生产流程图，采用 `Aspen Plus` 创建该流程，熟悉其中的压力变换单元，并求产品物流中环己烷的摩尔分数。物性方法为 `RK-SOAVE`。

环己烷可以用苯加氢反应得到，反应如下：

`C6H6(苯) + 3H2(氢气) -> C6H12(环己烷)`
在进入固定床接触反应器之前，苯和氢气进料与循环氢气和环己烷混合。假设苯的转化率为 `99.8%`，反应器出料被冷却，轻气体从两相闪蒸器中分离出去。部分轻气体作为循环氢气返回反应器。从分离器出来的部分液相物流进入精馏塔进一步脱除溶解的轻气体，使最终产品稳定，其余液相物流进入反应器，辅助控制温度。

## 已知条件

- 物流 `H2IN`：温度 `50℃`，压力 `2.5 MPa`，总流量 `330 kmol/h`，其中 `H2`、`N2`、`CH4` 的摩尔分数分别为 `0.975`、`0.005` 和 `0.02`
- 物流 `BZIN`：温度 `40℃`，压力 `0.1 MPa`，组分为纯苯，流量 `100 kmol/h`
- 模块 `FEED-MIX`（`Heater` 模块）：温度 `150℃`，压力 `2.3 MPa`
- 模块 `REACT`（`Rstoic` 模块）：温度 `200℃`，压降 `0.1 MPa`，苯的转化率 `0.998`
- 模块 `VFLOW`（`FSplit` 模块）：物流 `H2RCY` 的分数 `92%`
- 模块 `LFLOW`（`FSplit` 模块）：物流 `CHRCY` 的分数为 `30%`
- 模块 `HP-SEP`（`Flash2` 模块）：温度 `50℃`，压降 `0.05 MPa`
- 模块 `COLUMN`（`RadFrac` 模块）：理论板数 `12`，回流比 `1.2`，进料位置第 `8` 块理论板，塔压 `1.5 MPa`，塔馏出物采出率 `99 kmol/h`，冷凝器为只有气相采出的部分冷凝器
- 模块 `FEEDPUMP`（`Pump` 模块）：泵的效率 `0.6`，驱动机效率 `0.9`
- 模块 `PIPE`（`Pipe` 模块）：材质为碳钢，系列号 `40`，直径 `1 in`，长度 `25 m`
- 模块 `PUMP`（`Pump HI`）：出口压力 `2.6 MPa`
- 模块 `COMP`（`Compr` 模块）：采用等熵压缩机，压力增量 `0.4 MPa`
- 模块 `VALVE`（`Valve` 模块）：出口压力 `2 MPa`，阀门规格 `V810 equal percent flow` 截止阀，公称直径 `1.5 in`

## 泵特性曲线

以下特性曲线属于新鲜苯进料支路的 `FEEDPUMP`，即 `BZIN → FEEDPUMP → BZIN2`，不属于循环液相支路的 `PUMP`。

- `FEEDPUMP` 必须采用泵特性曲线模式；写入曲线后保持该模式，不得再切换为固定出口压力模式而使曲线失效。
- `FEEDPUMP` 的泵效率为 `0.6`，驱动机效率为 `0.9`；其出口状态由有效曲线及实际流量计算，不能用下游 `FEED-MIX` 的 `2.3 MPa` 直接替代泵曲线规格。
- 循环液相支路的 `PUMP` 使用独立的固定出口压力规格 `2.6 MPa`，不得将下表曲线写到该泵。
- 曲线流量按表中的 `m3/h` 使用。扬程原文未标明单位；写入 Aspen 前须明确记录所采用的单位解释，并按原生曲线表的实际单位进行转换，不能直接在 SI 表中填入原数字。
- 必须读回两台泵的实际规格模式、曲线单元格及各自连接支路，证明曲线在 `FEEDPUMP` 上有效参与计算。模块 ID 可以使用别名，但支路与规格归属不得改变。

| 项目 | 数值 1 | 数值 2 | 数值 3 | 数值 4 |
| --- | --- | --- | --- | --- |
| 流量 / (m3/h) | 20 | 10 | 5 | 3 |
| 扬程 | 40 | 250 | 300 | 400 |

## 目标

求产品物流中环己烷的摩尔分数。

` ` `

### FILE: generated/react_v2_task_figure_grounding.md
Reason: reviewed V2 figure grounding reused for React
` ` `text
# V2 Figure Grounding

This is the reviewed cached figure grounding for the current case.

## subfigure_scope_and_authority
这张题图不包含多个子图/流程；只显示一个完整的流程图。可见子图/流程为：1 个环己烷生产流程图。图内未看到独立的子图标题或图注；任务上下文中的图注/标题为“习题 5.1 流程图”，并描述为“环己烷生产流程图”。当前任务最可能对应这个唯一的流程图。

Visual evidence:
- 图中只有一套连续连接的流程网络，没有分栏、(a)/(b)、part_a/part_b、并列流程或多个独立图框。
- 可见设备/模块标签包括：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。
- 可见物流标签包括：BZIN、H2IN、BZIN2、H2RCY2、RXIN、RXOUT、VAP、H2RCY、PURGE、PURGE2、LIQ、COLFD、CHRCY、CHRCY2、CHRCY3、LTENDS、PRODUCT。
- 流程连接显示为同一套环己烷生产流程：进料 BZIN/H2IN 与循环物流进入 FEED-MIX，经 REACT、HP-SEP 后，气相经 VFLOW 分流为 H2RCY 和 PURGE，液相经 LFLOW 分流进入 COLUMN 或循环回 FEED-MIX。

## labels_and_topology
{'visible_modules_or_equipment': [{'visible_label': 'FEEDPUMP', 'type_from_context': 'Pump'}, {'visible_label': 'FEED-MIX', 'type_from_context': 'Heater'}, {'visible_label': 'REACT', 'type_from_context': 'Rstoic'}, {'visible_label': 'HP-SEP', 'type_from_context': 'Flash2'}, {'visible_label': 'VFLOW', 'type_from_context': 'FSplit'}, {'visible_label': 'VALVE', 'type_from_context': 'Valve'}, {'visible_label': 'COMP', 'type_from_context': 'Compr'}, {'visible_label': 'LFLOW', 'type_from_context': 'FSplit'}, {'visible_label': 'PUMP', 'type_from_context': 'Pump HI'}, {'visible_label': 'PIPE', 'type_from_context': 'Pipe'}, {'visible_label': 'COLUMN', 'type_from_context': 'RadFrac'}], 'visible_stream_labels': ['BZIN', 'H2IN', 'BZIN2', 'H2RCY2', 'RXIN', 'RXOUT', 'VAP', 'H2RCY', 'PURGE', 'PURGE2', 'LIQ', 'COLFD', 'CHRCY', 'CHRCY2', 'CHRCY3', 'LTENDS', 'PRODUCT'], 'directly_visible_connections_as_edges': [{'stream_label': 'BZIN', 'connection': 'external left feed -> into FEEDPUMP'}, {'stream_label': 'BZIN2', 'connection': 'FEEDPUMP -> into FEED-MIX'}, {'stream_label': 'H2IN', 'connection': 'external left feed -> into FEED-MIX'}, {'stream_label': 'H2RCY2', 'connection': 'COMP -> into FEED-MIX'}, {'stream_label': 'CHRCY3', 'connection': 'PIPE -> into FEED-MIX'}, {'stream_label': 'RXIN', 'connection': 'FEED-MIX -> into REACT'}, {'stream_label': 'RXOUT', 'connection': 'REACT -> into HP-SEP'}, {'stream_label': 'VAP', 'connection': 'HP-SEP -> into VFLOW'}, {'stream_label': 'H2RCY', 'connection': 'VFLOW -> into COMP'}, {'stream_label': 'PURGE', 'connection': 'VFLOW -> into VALVE'}, {'stream_label': 'PURGE2', 'connection': 'VALVE -> external right outlet'}, {'stream_label': 'LIQ', 'connection': 'HP-SEP -> into LFLOW'}, {'stream_label': 'COLFD', 'connection': 'LFLOW -> into COLUMN'}, {'stream_label': 'CHRCY', 'connection': 'LFLOW -> into PUMP'}, {'stream_label': 'CHRCY2', 'connection': 'PUMP -> into PIPE'}, {'stream_label': 'LTENDS', 'connection': 'COLUMN -> external right outlet'}, {'stream_label': 'PRODUCT', 'connection': 'COLUMN -> external right outlet'}], 'visible_node_fan_in_fan_out_summary': [{'node': 'FEEDPUMP', 'fan_in': ['BZIN'], 'fan_out': ['BZIN2']}, {'node': 'FEED-MIX', 'fan_in': ['BZIN2', 'H2IN', 'H2RCY2', 'CHRCY3'], 'fan_out': ['RXIN']}, {'node': 'REACT', 'fan_in': ['RXIN'], 'fan_out': ['RXOUT']}, {'node': 'HP-SEP', 'fan_in': ['RXOUT'], 'fan_out': ['VAP', 'LIQ']}, {'node': 'VFLOW', 'fan_in': ['VAP'], 'fan_out': ['H2RCY', 'PURGE']}, {'node': 'COMP', 'fan_in': ['H2RCY'], 'fan_out': ['H2RCY2']}, {'node': 'VALVE', 'fan_in': ['PURGE'], 'fan_out': ['PURGE2']}, {'node': 'LFLOW', 'fan_in': ['LIQ'], 'fan_out': ['COLFD', 'CHRCY']}, {'node': 'PUMP', 'fan_in': ['CHRCY'], 'fan_out': ['CHRCY2']}, {'node': 'PIPE', 'fan_in': ['CHRCY2'], 'fan_out': ['CHRCY3']}, {'node': 'COLUMN', 'fan_in': ['COLFD'], 'fan_out': ['LTENDS', 'PRODUCT']}]}

Visual evidence:
- 图中可见设备/模块文字标签包括："FEEDPUMP", "FEED-MIX", "REACT", "HP-SEP", "VFLOW", "VALVE", "COMP", "LFLOW", "PUMP", "PIPE", "COLUMN"。
- 左侧有 "BZIN" 进入 "FEEDPUMP"，其后物流标为 "BZIN2" 并接入 "FEED-MIX"。
- "FEED-MIX" 左侧/下侧同时可见 "H2IN", "BZIN2", "H2RCY2", "CHRCY3" 接入；右侧输出 "RXIN" 至 "REACT"。
- "REACT" 右侧输出 "RXOUT" 至 "HP-SEP"。
- "HP-SEP" 上方输出 "VAP" 至 "VFLOW"，下方输出 "LIQ" 至 "LFLOW"。
- "VFLOW" 左侧物流标为 "H2RCY"，通向 "COMP"；右侧物流 "PURGE" 经过 "VALVE" 后成为 "PURGE2"。
- "LFLOW" 右侧物流 "COLFD" 通向 "COLUMN"；左侧物流 "CHRCY" 通向 "PUMP"，再经 "CHRCY2" 到 "PIPE"，再以 "CHRCY3" 回到 "FEED-MIX"。
- "COLUMN" 右侧可见两条外出物流：上部 "LTENDS"，下部 "PRODUCT"。

Uncertainties:
- 部分小箭头较淡或模糊；上述方向主要按可见箭头、物流布局以及标签相邻关系记录。
- 图中 COLUMN 顶部附近有小图标/连接点，但没有清晰独立设备标签；按要求未将其新增为节点，只把 "COLUMN" 作为一个可见节点。
- "type_from_context" 来自题干上下文，不是图中可见文字；可见节点仍仅按图中设备标签记录。

## numbers_and_constraints
{'清晰可见的数值': [], '清晰可见的单位': [], '清晰可见的阶段号': [], '清晰可见的图注': [], '清晰可见的操作条件': [], '清晰可见的设备或模块标签': ['FEEDPUMP', 'FEED-MIX', 'REACT', 'HP-SEP', 'VFLOW', 'VALVE', 'COMP', 'LFLOW', 'PUMP', 'PIPE', 'COLUMN'], '清晰可见的物流标签': ['BZIN', 'H2IN', 'BZIN2', 'H2RCY2', 'RXIN', 'RXOUT', 'VAP', 'H2RCY', 'PURGE', 'PURGE2', 'LIQ', 'COLFD', 'CHRCY', 'CHRCY2', 'CHRCY3', 'LTENDS', 'PRODUCT'], '产品_回流_循环_排放说明': {'PRODUCT': 'COLUMN 底部/下部右侧外出产品物流', 'LTENDS': 'COLUMN 上部右侧外出轻端物流', 'H2RCY': 'VFLOW 分出的循环气物流，进入 COMP', 'H2RCY2': 'COMP 出口物流，回到 FEED-MIX', 'CHRCY': 'LFLOW 分出的液相循环物流，进入 PUMP', 'CHRCY2': 'PUMP 出口物流，进入 PIPE', 'CHRCY3': 'PIPE 出口物流，回到 FEED-MIX', 'PURGE': 'VFLOW 分出的排放物流，进入 VALVE', 'PURGE2': 'VALVE 出口外排物流'}, '对_Aspen_建模重要的可见约束': ['BZIN 是外部进料，进入 FEEDPUMP；FEEDPUMP 出口为 BZIN2。', 'H2IN 是外部进料，直接进入 FEED-MIX。', 'FEED-MIX 有 4 条可见入口：BZIN2、H2IN、H2RCY2、CHRCY3；出口为 RXIN。', 'RXIN 进入 REACT；REACT 出口为 RXOUT。', 'RXOUT 进入 HP-SEP；HP-SEP 有两个出口：上部 VAP、下部 LIQ。', 'VAP 进入 VFLOW；VFLOW 将气相分为 H2RCY 和 PURGE 两股。', 'H2RCY 经 COMP 后成为 H2RCY2，并回到 FEED-MIX，形成气相循环回路。', 'PURGE 经 VALVE 后成为 PURGE2，并作为外出物流离开流程。', 'LIQ 进入 LFLOW；LFLOW 将液相分为 COLFD 和 CHRCY 两股。', 'COLFD 进入 COLUMN。', 'CHRCY 依次经过 PUMP、PIPE，物流名依次为 CHRCY、CHRCY2、CHRCY3，最终回到 FEED-MIX，形成液相循环回路。', 'COLUMN 有一个可见进料 COLFD，两个可见外出物流：LTENDS 和 PRODUCT。', '图中没有可见的温度、压力、流量、组成、转化率、分流比、回流比、塔板数、进料板位置或泵/压缩机/阀门参数。']}

Visual evidence:
- 图中模块文字框或设备旁标注清楚可见："FEEDPUMP", "FEED-MIX", "REACT", "HP-SEP", "VFLOW", "VALVE", "COMP", "LFLOW", "PUMP", "PIPE", "COLUMN"。
- 左侧可见物流 "BZIN" 进入 "FEEDPUMP"，之后物流标注为 "BZIN2"。
- "H2IN", "BZIN2", "H2RCY2", "CHRCY3" 均以箭头接入 "FEED-MIX"，"FEED-MIX" 出口标注为 "RXIN"。
- "RXIN" 进入 "REACT"，"REACT" 出口为 "RXOUT"，进入 "HP-SEP"。
- "HP-SEP" 上部出口标注 "VAP"，下部出口标注 "LIQ"。
- "VAP" 进入 "VFLOW"；"VFLOW" 左侧出口为 "H2RCY"，右侧出口为 "PURGE"。
- "H2RCY" 进入 "COMP"，出口为 "H2RCY2" 并回到 "FEED-MIX"。
- "PURGE" 经过 "VALVE" 后成为 "PURGE2"，并向右离开流程。
- "LIQ" 进入 "LFLOW"；"LFLOW" 右侧出口为 "COLFD"，进入 "COLUMN"；左侧出口为 "CHRCY"。
- "CHRCY" 进入 "PUMP"，之后为 "CHRCY2"，再进入 "PIPE"，之后为 "CHRCY3" 并回到 "FEED-MIX"。
- "COLUMN" 右侧有两股外出物流：上部 "LTENDS"，下部 "PRODUCT"。

Uncertainties:
- 题图本身未显示任何数值、单位、阶段号、温度、压力、流量、组成、分率或设备规格；这些若存在只能来自正文条件，不能从图中读取。
- 图中没有独立可见图题或图注文字；只能看到流程图及设备/物流标签。
- COLUMN 内部塔板数、进料板位置、冷凝器/再沸器设置等没有在图中以文字或数字标出。

## stream_types_and_coupling
{'stream_type_classification': {'material_streams_solid_line': ['BZIN', 'H2IN', 'BZIN2', 'H2RCY2', 'RXIN', 'RXOUT', 'VAP', 'H2RCY', 'PURGE', 'PURGE2', 'LIQ', 'COLFD', 'CHRCY', 'CHRCY2', 'CHRCY3', 'LTENDS', 'PRODUCT'], 'heat_streams_dashed_line_with_C': [], 'work_streams_dashed_line_with_W': [], 'power_streams_dashed_line_with_I': []}, 'block_unit_symbols_separate_from_stream_labels': ['FEEDPUMP', 'FEED-MIX', 'REACT', 'HP-SEP', 'VFLOW', 'VALVE', 'COMP', 'LFLOW', 'PUMP', 'PIPE', 'COLUMN'], 'summary': 'All visible labeled streams in the task figure are drawn as solid material-flow lines. No dashed heat/work/power coupling lines with C, W, or I symbols are visible.'}

Uncertainties:
- The figure is low-resolution, but the visible stream lines appear consistently solid; no dashed heat/work/power stream symbols are discernible.
- Block/unit symbols are listed as visible block labels only; the provided reference legend is for stream types, not for detailed equipment-icon classification.

## multi_effect_evaporation_port_contract
{'is_active_figure_multi_effect_evaporation_flowsheet': False, 'reason': 'The active figure is a cyclohexane production/reaction-separation flowsheet, not a multi-effect evaporation flowsheet. No evaporator effects, condensers, Q1/Q2/Q3/Q4 heat labels, or heat-cascade lines are visible.', 'aspen_topology_contract_from_active_subfigure_only': {'liquid_or_concentrate_material_path': {'status': 'not a multi-effect evaporation liquid/concentrate path', 'visible_material_edges': ['BZIN -> FEEDPUMP -> BZIN2 -> FEED-MIX', 'FEED-MIX -> RXIN -> REACT', 'REACT -> RXOUT -> HP-SEP', 'HP-SEP -> LIQ -> LFLOW', 'LFLOW -> COLFD -> COLUMN', 'COLUMN -> PRODUCT', 'LFLOW -> CHRCY -> PUMP -> CHRCY2 -> PIPE -> CHRCY3 -> FEED-MIX']}, 'secondary_vapor_or_heating_material_path': {'status': 'no multi-effect secondary-vapor/heating-material cascade is visible', 'visible_vapor_or_gas_material_edges': ['HP-SEP -> VAP -> VFLOW', 'VFLOW -> H2RCY -> COMP -> H2RCY2 -> FEED-MIX', 'VFLOW -> PURGE -> VALVE -> PURGE2', 'H2IN -> FEED-MIX'], 'material_vapor_streams_feeding_heater_or_exchanger_symbols_separate_from_Q': [{'stream': 'H2IN', 'visible_connection': 'external feed -> FEED-MIX', 'note': 'This is a material stream, not a Q heat stream.'}, {'stream': 'H2RCY2', 'visible_connection': 'COMP -> FEED-MIX', 'note': 'This is a material recycle stream, not a Q heat stream.'}]}, 'condensate_or_water_path': {'status': 'none visible', 'visible_edges': []}, 'heat_or_energy_coupling_path': {'status': 'none visible', 'visible_Q_heat_stream_rows': [], 'unresolved_Q_heat_stream_rows': [], 'note': 'No visible heat labels such as Q1, Q2, Q3, or Q4 appear in the active figure, so no Aspen heat-port contract of the form source.HS(OUT) -> Q* -> sink.HS(IN) can be completed or even proposed from this figure.'}}}

Visual evidence:
- Visible equipment/module labels are: FEEDPUMP, FEED-MIX, REACT, HP-SEP, VFLOW, VALVE, COMP, LFLOW, PUMP, PIPE, COLUMN.
- Visible stream labels include: BZIN, H2IN, BZIN2, H2RCY2, RXIN, RXOUT, VAP, H2RCY, PURGE, PURGE2, LIQ, COLFD, CHRCY, CHRCY2, CHRCY3, LTENDS, PRODUCT.
- The only visibly labeled flash-like unit is HP-SEP, with RXOUT entering and VAP/LIQ leaving.
- The vapor/gas path shown is HP-SEP -> VAP -> VFLOW, then split to H2RCY through COMP back to FEED-MIX and PURGE through VALVE to PURGE2.
- No labels Q1, Q2, Q3, Q4, no dashed heat streams, and no evaporator-effect labels are visible in the active figure.

Uncertainties:
- The figure does not show any heat-stream labels or explicit Aspen energy ports; therefore heat coupling endpoints cannot be resolved.
- FEED-MIX is identified in the task context as a Heater module, but the visible figure does not show a separate Q heat stream into or out of it.
- The active figure is not a multi-effect evaporation flowsheet, so evaporation-specific path classes are not directly applicable.

## label_semantics_and_mapping
题图可见的是一套以名称标签为主的流程图，没有可见的阶段号、罗马数字、塔板号、效号或表格段号。图中可见设备/模块名称为：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。图中可见物流名称为：BZIN、H2IN、BZIN2、H2RCY2、RXIN、RXOUT、VAP、H2RCY、PURGE、PURGE2、LIQ、COLFD、CHRCY、CHRCY2、CHRCY3、LTENDS、PRODUCT。

图中带数字后缀的物流名称包括：BZIN2、H2RCY2、PURGE2、CHRCY2、CHRCY3；另有 H2IN、H2RCY、H2RCY2 中的“H2”表示氢气符号的一部分，不应解释为“第2级/第2段”。这些数字后缀只能从图中确认是物流名称的一部分，不能直接解释为语义上的第二段、第二效、第二级或第二股主物流。

与任务上下文的对应关系：模块名 FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、LFLOW、COLUMN、PIPE、PUMP、COMP、VALVE 在图中均以相同名称出现，因此这些名称与上下文中的模块名称可以直接对应。物流名 H2IN、BZIN、H2RCY、CHRCY、PRODUCT 等也在图中出现，可与上下文中同名物流对应。但图中没有显示温度、压力、流量、组成、分流比、转化率、塔板数、进料板位置、回流比、泵曲线编号等语义编号或数值条件；这些必须依赖正文或表格补足。

不能从图中直接得出的映射包括：COLUMN 的“12 块理论板”和“第 8 块理论板进料”在图中没有板号或进料板号标注，不能由图中 COLFD 接入位置直接推出；泵特性曲线中的“数值 1、数值 2、数值 3、数值 4”没有出现在图中，不能映射到图中 FEEDPUMP 或 PUMP 的某一序号；BZIN2、H2RCY2、PURGE2、CHRCY2、CHRCY3 的数字后缀不能直接映射为正文中的第一段/第二段/第几级，只能按图中连接关系理解为相应单元前后的不同物流名。也不能仅凭图中“PUMP”和“FEEDPUMP”判断哪个是语义上的第一台泵或第二台泵；其类型和参数需依赖正文给出的模块说明。

Visual evidence:
- 设备/模块标签清晰可见："FEEDPUMP", "FEED-MIX", "REACT", "HP-SEP", "VFLOW", "VALVE", "COMP", "LFLOW", "PUMP", "PIPE", "COLUMN"。
- 物流标签清晰可见："BZIN", "H2IN", "BZIN2", "H2RCY2", "RXIN", "RXOUT", "VAP", "H2RCY", "PURGE", "PURGE2", "LIQ", "COLFD", "CHRCY", "CHRCY2", "CHRCY3", "LTENDS", "PRODUCT"。
- "BZIN" 进入 "FEEDPUMP"，其出口物流标为 "BZIN2"，说明 BZIN2 是图中一条具体物流名称，而不是可见阶段号。
- "H2RCY" 经 "COMP" 后成为 "H2RCY2" 并返回 "FEED-MIX"；图中只能确认这是压缩机前后两条物流的名称。
- "PURGE" 经 "VALVE" 后成为 "PURGE2"；图中只能确认这是阀前后物流名称。
- "CHRCY" 经 "PUMP" 后为 "CHRCY2"，再经 "PIPE" 后为 "CHRCY3"，随后返回 "FEED-MIX"；图中数字后缀体现物流命名变化，不显示任何级数或效数含义。
- "COLUMN" 只有一个可见进料 "COLFD" 和两个可见出口 "LTENDS"、"PRODUCT"；图中未显示塔板 1–12、进料第 8 板或任何板号标注。

Uncertainties:
- 图中没有可见的阶段号、效号、罗马数字、塔板号或表格编号，因此无法从图像本身建立这些语义编号的映射。
- 带数字后缀的物流名，如 BZIN2、PURGE2、CHRCY2、CHRCY3，可能是 Aspen 中为区分单元前后物流而命名，但图中未说明数字后缀的命名规则。
- COLUMN 的理论板数、进料位置、回流比和采出率均不在图中显示，必须依赖任务正文。
- 泵曲线表中的“数值 1–4”没有在图中出现，不能判断这些编号对应图中哪一个点、哪一段或哪一个单元。
- FEEDPUMP 和 PUMP 都是图中可见名称，但图中本身未标注它们的 Aspen 模块类型；类型对应关系需依赖上下文正文。

## icon_unit_family
[{'symbol_id': 'S1', 'symbol_location_without_using_text': 'far left on the lower incoming material line', 'icon_candidates': ['Pump'], 'preferred_candidate_from_task_context': 'Pump', 'visual_reason_from_shape_only': 'The symbol is a small circular rotating-equipment icon with a short connected line and base-like shading, matching the supplied Pump icon more closely than vessel, valve, or column icons.', 'semantic_reason_from_task_context': 'The task context describes this left-side pressure-raising unit as a pump.', 'confidence': 'high', 'uncertainty': 'Low-resolution shading makes fine details indistinct, but the round pump-like shape is distinctive.'}, {'symbol_id': 'S2', 'symbol_location_without_using_text': 'left-center where several incoming lines join before the reactor-like vessel', 'icon_candidates': ['Heater'], 'preferred_candidate_from_task_context': 'Heater', 'visual_reason_from_shape_only': 'The remaining non-text symbol is a small round icon with internal diagonal/zigzag-like markings. This is closest to the supplied Heater icon, not to the triangular Mixer or FSplit icons.', 'semantic_reason_from_task_context': 'The task context states that this feed conditioning/mixing point is modeled with a heater-type module.', 'confidence': 'medium', 'uncertainty': 'The internal markings are small and blurred; the symbol also functions topologically as a mixing point, but its shape does not match the supplied triangular Mixer icon.'}, {'symbol_id': 'S3', 'symbol_location_without_using_text': 'center-left, immediately downstream of the round multi-inlet symbol', 'icon_candidates': ['RStoic'], 'preferred_candidate_from_task_context': 'RStoic', 'visual_reason_from_shape_only': 'The symbol is a horizontal cylindrical vessel with internal crosshatched/packed-looking shading, closely matching the supplied RStoic reactor icon.', 'semantic_reason_from_task_context': 'The task context describes this step as the stoichiometric reaction section.', 'confidence': 'high', 'uncertainty': 'The hatch pattern is somewhat low-resolution, but the horizontal crosshatched reactor vessel is visually distinctive.'}, {'symbol_id': 'S4', 'symbol_location_without_using_text': 'center-right vertical vessel receiving material from the reactor-like symbol and sending one line upward and one downward', 'icon_candidates': ['Flash2'], 'preferred_candidate_from_task_context': 'Flash2', 'visual_reason_from_shape_only': 'The symbol is a simple vertical rounded vessel without column trays or external condenser/reboiler attachments, matching the supplied Flash2 icon.', 'semantic_reason_from_task_context': 'The task context describes this vessel as a two-phase flash separator.', 'confidence': 'high', 'uncertainty': 'It could be generically interpreted as a vertical separator from shape alone, but among the supplied icons Flash2 is the closest match.'}, {'symbol_id': 'S5', 'symbol_location_without_using_text': 'upper middle, small filled square on the upward vapor/gas path where the line divides left and right', 'icon_candidates': ['FSplit', 'Dupl', 'Mult'], 'preferred_candidate_from_task_context': 'FSplit', 'visual_reason_from_shape_only': 'The visible symbol is only a small filled square junction with one incoming line and two outgoing lines. It does not closely match the supplied wedge-shaped FSplit icon or the boxed Mult/Dupl icons, so the match is a simplified splitter-marker ambiguity rather than a distinctive icon match.', 'semantic_reason_from_task_context': 'The task context identifies this upper gas-path divider as a fractional splitter.', 'confidence': 'medium-low', 'uncertainty': 'Shape alone is not a close match to any supplied splitter icon; the candidate ranking depends strongly on the non-text split topology and task context.'}, {'symbol_id': 'S6', 'symbol_location_without_using_text': 'upper left of the vapor/gas recycle loop, on the line returning toward the central feed-conditioning area', 'icon_candidates': ['Compr'], 'preferred_candidate_from_task_context': 'Compr', 'visual_reason_from_shape_only': 'The symbol is a tapered wedge/trapezoid rotating-equipment icon, visually matching the supplied compressor icon.', 'semantic_reason_from_task_context': 'The task context describes this recycle-gas pressure-changing unit as a compressor.', 'confidence': 'high', 'uncertainty': 'No significant ambiguity from the remaining shape.'}, {'symbol_id': 'S7', 'symbol_location_without_using_text': 'upper right on the outlet branch after the upper splitter marker', 'icon_candidates': ['Valve'], 'preferred_candidate_from_task_context': 'Valve', 'visual_reason_from_shape_only': 'The symbol is an inline valve/bowtie-like mark with a small stem-like feature, matching the supplied Valve icon.', 'semantic_reason_from_task_context': 'The task context describes this outlet pressure-changing unit as a valve.', 'confidence': 'high', 'uncertainty': 'The icon is small, but its inline valve geometry is recognizable.'}, {'symbol_id': 'S8', 'symbol_location_without_using_text': 'lower middle, small filled square below the vertical flash-like vessel where the liquid path divides', 'icon_candidates': ['FSplit', 'Dupl', 'Mult'], 'preferred_candidate_from_task_context': 'FSplit', 'visual_reason_from_shape_only': 'The visible symbol is a small filled square junction with one incoming line and two outgoing lines. It is not a distinctive match to the supplied wedge-shaped FSplit icon, so the geometry-only identification remains ambiguous among simplified splitter-type blocks.', 'semantic_reason_from_task_context': 'The task context identifies this lower liquid-path divider as a fractional splitter.', 'confidence': 'medium-low', 'uncertainty': 'The square marker shape is not a close geometry match to the supplied Aspen splitter icons; context is needed to prefer FSplit.'}, {'symbol_id': 'S9', 'symbol_location_without_using_text': 'lower center-left on the recycle line leaving the lower splitter marker', 'icon_candidates': ['Pump'], 'preferred_candidate_from_task_context': 'Pump', 'visual_reason_from_shape_only': 'The symbol is a circular rotating-equipment icon with connected inlet/outlet lines, matching the supplied Pump icon.', 'semantic_reason_from_task_context': 'The task context describes this lower recycle pressure-raising unit as a pump.', 'confidence': 'high', 'uncertainty': 'Low-resolution shading limits fine-detail comparison, but the pump-like circle is clear.'}, {'symbol_id': 'S10', 'symbol_location_without_using_text': 'lower left-of-center, horizontal tubular element downstream of the lower pump-like symbol', 'icon_candidates': ['Pipe', 'Pipeline'], 'preferred_candidate_from_task_context': 'Pipe', 'visual_reason_from_shape_only': 'The symbol is a short horizontal cylindrical tube. This geometry is closest to the supplied Pipe and Pipeline icons, which are visually similar in the legend.', 'semantic_reason_from_task_context': 'The task context describes this recycle-line element as a pipe section.', 'confidence': 'medium-high', 'uncertainty': 'The supplied Pipe and Pipeline icons are very similar; the figure’s simplified tube shape does not distinguish them by geometry alone.'}, {'symbol_id': 'S11', 'symbol_location_without_using_text': 'right side, tall vertical tower with side connection from the lower splitter path and two product-side exits', 'icon_candidates': ['DSTWU', 'Distl', 'RadFrac'], 'preferred_candidate_from_task_context': 'RadFrac', 'visual_reason_from_shape_only': 'The symbol is a vertical distillation-column-like vessel with small top and bottom auxiliary round features. The supplied DSTWU, Distl, and RadFrac column icons are visually very similar, so the simplified shape alone does not uniquely distinguish among them.', 'semantic_reason_from_task_context': 'The task context describes this tower as a rigorous distillation column modeled with a RadFrac-type block.', 'confidence': 'medium', 'uncertainty': 'The icon geometry alone is ambiguous among several distillation-column icons in the reference legend.'}]

Visual evidence:
- All rectangular callout boxes and text were mentally masked before matching.
- The remaining process symbols include two round pump-like icons, one round heater-like multi-inlet icon, one horizontal crosshatched reactor-like vessel, one simple vertical flash-like vessel, two small filled square splitter markers, one tapered compressor-like wedge, one inline valve symbol, one short horizontal tube, and one tall column-like tower.
- The two small filled square splitter markers are not close geometric matches to the supplied wedge or boxed splitter icons, so they are reported as simplified ambiguous splitter symbols rather than distinctive icon matches.

Uncertainties:
- The figure is low-resolution, so small internal markings are blurry.
- The splitter symbols appear as filled squares, whereas the provided reference splitter icons use other geometries; context is needed to prefer a specific splitter block type.
- The distillation-column icon is simplified and visually compatible with multiple supplied column-type icons.
- The short horizontal tube cannot be distinguished geometrically between Pipe and Pipeline from the supplied icons alone.

` ` `

### FILE: generated/react_v2_target_priority_judgment.md
Reason: reviewed V2 target-priority context reused for React
` ` `text
# Target Priority Judgment

Use this as a priority guide when planning repairs and interpreting target-related validation.
Primary semantic targets and topology hard gates are blocking. Secondary fidelity targets should be evidenced and reported, but they should not override primary targets or topology when conflicts are documented.

Source artifact: `<REPOSITORY_ROOT>\experiments\script_agent_experiment\iter0_context_packs\v2\cases\chinese_5_1_radfrac\target_priority_judgment.json`

## Primary Semantic Targets
- P1_product_cyclohexane_mole_fraction: Report the mole fraction of cyclohexane/C6H12 in the final PRODUCT material stream.
  Evidence policy: The stated objective is to求产品物流中环己烷的摩尔分数. This is the main deliverable of the task.
- P2_aspen_flowsheet_result_path: The reported PRODUCT C6H12 mole fraction must come from a solved Aspen Plus flowsheet, not from a hand calculation or an input-only restatement.
  Evidence policy: The task asks to use Aspen Plus to create the cyclohexane production process and determine the product composition. A result not derived from the Aspen flowsheet would not satisfy the central request.
- P3_core_process_semantics: Model the intended cyclohexane production chemistry and separations: benzene hydrogenation C6H6 + 3 H2 -> C6H12 with 99.8% benzene conversion, cooling/flash light-gas separation, vapor purge/recycle, liquid recycle/column feed split, and RadFrac stabilization column producing PRODUCT.
  Evidence policy: These features define the process whose product composition is requested. Omitting or replacing them changes the semantic meaning of the requested PRODUCT composition.
- P4_fixed_feed_and_major_operating_specs: Use the task-stated feed compositions/flow rates and major reactor, flash, split, and column operating specifications as the basis for the Aspen calculation.
  Evidence policy: The requested mole fraction is meaningful only for the given problem conditions, including H2IN, BZIN, reactor conversion/conditions, flash conditions, split fractions, and RadFrac conditions.

## Topology Hard Gates
- T1_visible_nodes_and_block_identities: The flowsheet must contain the figure-visible named process nodes FEEDPUMP, FEED-MIX, REACT, HP-SEP, VFLOW, VALVE, COMP, LFLOW, PUMP, PIPE, and COLUMN, with the text-specified Aspen block families where applicable.
  Evidence policy: The task asks to create the Aspen Plus flowsheet shown in the figure, and the text names the module families for these blocks. Removing, renaming, splitting, or substituting visible nodes changes the required flowsheet identity.
- T2_feed_mixing_and_reactor_path: The feed/recycle path must preserve the visible topology: BZIN -> FEEDPUMP -> BZIN2 -> FEED-MIX; H2IN -> FEED-MIX; H2RCY2 -> FEED-MIX; CHRCY3 -> FEED-MIX; FEED-MIX -> RXIN -> REACT -> RXOUT -> HP-SEP.
  Evidence policy: This is the figure-backed inlet and reactor topology leading to the process whose product is requested.
- T3_separator_vapor_recycle_and_purge_topology: HP-SEP vapor outlet must feed VFLOW; VFLOW must split to H2RCY -> COMP -> H2RCY2 -> FEED-MIX and PURGE -> VALVE -> PURGE2.
  Evidence policy: The vapor recycle/purge loop is visible in the figure and described in the text as part of the cyclohexane production process.
- T4_separator_liquid_column_and_liquid_recycle_topology: HP-SEP liquid outlet must feed LFLOW; LFLOW must split to COLFD -> COLUMN and CHRCY -> PUMP -> CHRCY2 -> PIPE -> CHRCY3 -> FEED-MIX.
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

` ` `

### FILE: generated/react_v2_planner_initial_context.md
Reason: reviewed V2 planner context reused for React
` ` `text
# Planner Initial Context

This context was selected for the React run from the shared task planner.
Treat explicit task facts as hard requirements.

## Explicit Blocks
- name=FEEDPUMP; block_type=PUMP; specs=泵的效率 `0.6`，驱动机效率 `0.9` Numeric table `泵特性曲线` assigned to this block:
| 项目 | 数值 1 | 数值 2 | 数值 3 | 数值 4 |
| --- | --- | --- | --- | --- |
| 流量 / (m3/h) | 20 | 10 | 5 | 3 |
| 扬程 | 40 | 250 | 300 | 400 |
- name=FEED-MIX; block_type=HEATER; specs=Temperature 150℃, pressure 2.3 MPa.
- name=REACT; block_type=RSTOIC; specs=Temperature 200℃, pressure drop 0.1 MPa; reaction C6H6 + 3H2 -> C6H12; benzene conversion 0.998.
- name=VFLOW; block_type=FSPLIT; specs=Fraction of stream H2RCY is 92%.
- name=LFLOW; block_type=FSPLIT; specs=Fraction of stream CHRCY is 30%.
- name=HP-SEP; block_type=FLASH2; specs=Temperature 50℃, pressure drop 0.05 MPa.
- name=COLUMN; block_type=RADFRAC; specs=12 theoretical stages; reflux ratio 1.2; feed on stage 8; column pressure 1.5 MPa; distillate rate 99 kmol/h; partial condenser with vapor distillate only.
- name=PIPE; block_type=PIPE; specs=Carbon steel; schedule 40; diameter 1 in; length 25 m.
- name=PUMP; block_type=PUMP; specs=出口压力 `2.6 MPa`
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
- Create base Aspen session, components, property method, blocks, and figure topology; phase=workflow_build; blocks=['FP', 'FM', 'R1', 'HS', 'VF', 'VALVE', 'CP', 'LF', 'PUMP', 'PIPE', 'CO']; streams=['B1', 'H1', 'B2', 'H3', 'R2', 'R3', 'V1', 'H4', 'P1', 'P2', 'L1', 'C3', 'C4', 'C5', 'C6', 'L3', 'P5']
- Configure fresh feed material streams; phase=stream_variable_config; blocks=[]; streams=['H1', 'B1']
- Configure Pump blocks FEEDPUMP and PUMP; phase=block_variable_config; blocks=['FP', 'PUMP']; streams=[]
- Configure FEED-MIX Heater block; phase=block_variable_config; blocks=['FM']; streams=[]
- Configure RStoic core operating specs; phase=block_variable_config; blocks=['R1']; streams=[]
- Write RStoic stoichiometry rows; phase=block_variable_config; blocks=['R1']; streams=[]
- Apply RStoic conversion and selectivity metadata; phase=block_variable_config; blocks=['R1']; streams=[]
- Configure HP-SEP Flash2 block; phase=block_variable_config; blocks=['HS']; streams=[]
- Configure VFLOW and LFLOW FSplit blocks; phase=block_variable_config; blocks=['VF', 'LF']; streams=[]
- Configure COMP compressor block; phase=block_variable_config; blocks=['CP']; streams=[]
- Configure VALVE block; phase=block_variable_config; blocks=['VALVE']; streams=[]
- Configure PIPE block; phase=block_variable_config; blocks=['PIPE']; streams=[]
- Configure COLUMN RadFrac block; phase=block_variable_config; blocks=['CO']; streams=[]
- Complete missing required variables and verify readiness; phase=completion_repair; blocks=['FP', 'FM', 'R1', 'HS', 'VF', 'VALVE', 'CP', 'LF', 'PUMP', 'PIPE', 'CO']; streams=['B1', 'H1', 'B2', 'H3', 'R2', 'R3', 'V1', 'H4', 'P1', 'P2', 'L1', 'C3', 'C4', 'C5', 'C6', 'L3', 'P5']
- Solve flowsheet and report PRODUCT cyclohexane mole fraction; phase=analysis_tuning; blocks=[]; streams=['P5']

` ` `

### FILE: experiments/script_agent_experiment/iter0_context_packs/v2/cases/chinese_5_1_radfrac/task_profile.json
Reason: LLM-selected task profile from task text
` ` `text
{
  "case_id": "chinese_5_1_radfrac",
  "task_profile_path": "",
  "task_markdown": "tasks/test/chn/chapter_05/exercise_5_1.md",
  "script_stem": "chinese_5_1",
  "baseline_script": "tool_side_generation/healthcheck/full_evaluation/chinese_5_1.py",
  "notes": "Cyclohexane production flowsheet (Chi-5.1 BKP); chapter 5 skill applies.",
  "gate_contract_path": "experiments/script_agent_experiment/generated_context/chinese_5_1_radfrac_gate_contract.json",
  "forbidden_paths": [
    "tool_side_generation/healthcheck/full_evaluation/chinese_5_1.py",
    "tool_side_generation/healthcheck/full_evaluation/",
    "tool_side_generation/healthcheck/full_example/homework/",
    "chinese_5_1_agent_generated.py",
    "chinese_5_1_fresh_gpt54.py",
    "chinese_5_1_own_agent.py"
  ],
  "block_families": [
    "PROPERTY_METHODS",
    "HEATER",
    "RSTOIC",
    "FLASH2",
    "FSPLIT",
    "RADFRAC",
    "PUMP",
    "COMPR",
    "PIPE",
    "VALVE"
  ],
  "planning_validator_families": [
    "PROPERTY_METHODS",
    "HEATER",
    "RSTOIC",
    "FLASH2",
    "FSPLIT",
    "RADFRAC",
    "PUMP",
    "COMPR",
    "PIPE",
    "VALVE"
  ],
  "surface_docs": [
    "docs/hardcoded_script_plan/block_type_inject/property_methods.md",
    "docs/hardcoded_script_plan/block_type_inject/heater.md",
    "docs/hardcoded_script_plan/block_type_inject/rstoic.md",
    "docs/hardcoded_script_plan/block_type_inject/flash2.md",
    "docs/hardcoded_script_plan/block_type_inject/fsplit.md",
    "docs/hardcoded_script_plan/block_type_inject/radfrac.md",
    "docs/hardcoded_script_plan/block_type_inject/pump.md",
    "docs/hardcoded_script_plan/block_type_inject/compr.md",
    "docs/hardcoded_script_plan/block_type_inject/pipe.md",
    "docs/hardcoded_script_plan/block_type_inject/valve.md"
  ],
  "skill_names": [
    "aspen-task-execution-order",
    "aspen-property-method-selection",
    "aspen-material-stream-composition-must-be-specified",
    "functional-role-semantics-validation",
    "aspen-generic-readbacks",
    "reactor-reaction-setup-high-level",
    "sequential-reaction-topology",
    "native-reactor-module-comparison",
    "flash-control-chain",
    "prefer-direct-component-splits",
    "shared-material-port-topology",
    "radfrac-absorber-like-configuration",
    "radfrac-standard-column-pressure-basis",
    "aspen-completion-error-hints",
    "aspen-component-radfrac-evidence-repair",
    "aspen-pump-outlet-specification",
    "compr-analysis-variable-selection",
    "aspen-custom-unit-set",
    "solvent-recycle-closure-semantics",
    "radfrac-extractive-distillation-solvent",
    "optimization-constrained-feed-and-recycle-evidence",
    "split-handoff-inheritance-boundary",
    "rep-derived-metric-consistency"
  ],
  "requires_design_spec_chain": false,
  "validator_gates": [
    "hard_metrics_contract",
    "recycle_topology"
  ],
  "task_semantics": {
    "source": "LLM task profile",
    "validator_policy": {
      "allow_equivalent_model": false,
      "allow_equivalent_column_model": false,
      "stagewise_column_required": true,
      "external_blackbox_optimization_ok": false,
      "native_analysis_required_kinds": [],
      "native_analysis_optional_kinds": [],
      "design_spec_target_kind": "none",
      "workflow_gates": [],
      "family_validators": [],
      "reactor_module_families": []
    },
    "uncertainties": [
      "The figure shows FEED-MIX as the single visible convergence/feed-conditioning node, while the written task specifies it as a Heater module; the topology should preserve one visible FEED-MIX node rather than silently splitting it into a separate mixer and heater.",
      "The figure itself does not show the COLUMN condenser/reboiler details; the partial condenser with vapor distillate and the stated RadFrac operating specifications come from the written task.",
      "The pump characteristic curve table heading does not name a specific module even though two pump-class modules are present; dataset attachment follows the supplied table-attachment rule rather than relying on proximity, subtype wording, or the block label PUMP.",
      "The visible figure contains only solid material streams and no dashed heat, work, or power streams."
    ],
    "dataset_attachments": [
      {
        "heading": "泵特性曲线",
        "block": "FEEDPUMP",
        "excluded_blocks": [
          "PUMP"
        ]
      }
    ],
    "figure_context_used": true,
    "figure_image_references": [
      "./images/exercise_5_1_flow.png"
    ],
    "figure_resolved_image_paths": [
      "tasks/test/chn/chapter_05/images/exercise_5_1_flow.png"
    ]
  }
}
` ` `

### FILE: experiments/script_agent_experiment/generated_context/chinese_5_1_radfrac_gate_contract.json
Reason: LLM-selected validation gate contract from task text
` ` `text
{
  "case_id": "chinese_5_1_radfrac",
  "required_gates": [
    {
      "kind": "property_method_contract",
      "required": false,
      "allowed_surrogate": false,
      "why": "任务明确规定物性方法为 RK-SOAVE；产品物流中环己烷摩尔分数必须由使用该物性方法的 Aspen Plus 模型计算得到。",
      "deterministic_evidence": [
        "Aspen Properties/Setup readback shows global property method RK-SOAVE.",
        "Final reported PRODUCT composition is from a run using RK-SOAVE, not from a different method or hand calculation."
      ],
      "scoring_only": true
    },
    {
      "kind": "recycle_topology",
      "required": true,
      "allowed_surrogate": false,
      "why": "The task requires physical material recycle return paths; accounting-only declarations cannot replace those connections.",
      "deterministic_evidence": [
        "Final live material-port/stream readbacks prove every task-stated recycle return path reaches its upstream process unit, including task/figure intermediate equipment and branch splits.",
        "Final same-run Aspen results prove the physically connected recycle loops converged and participated in the reported product result; a declared recovery or makeup balance alone is insufficient.",
        "Recycle identities, destinations, and split specifications follow the authoritative task and figure, not recycled gate prose or inherited solution values."
      ],
      "closure_semantics": {
        "closure_type": "numerical_recycle_tear",
        "accepted_topology": "task-stated physical material return paths into upstream process units",
        "physical_recycle_required": true
      }
    },
    {
      "kind": "reaction_separator_splitter_contract",
      "required": true,
      "allowed_surrogate": false,
      "why": "任务明确给出苯加氢反应、Rstoic 反应器转化率、Flash2 闪蒸器条件以及两个 FSplit 分流比例；这些是产品组成计算的核心过程定义。",
      "deterministic_evidence": [
        "REACT is implemented as an Rstoic block or Aspen-equivalent stoichiometric reactor for C6H6 + 3 H2 -> C6H12.",
        "REACT has temperature 200 °C, pressure drop 0.1 MPa, and benzene conversion 0.998.",
        "HP-SEP is implemented as Flash2 with temperature 50 °C and pressure drop 0.05 MPa.",
        "VFLOW is an FSplit or equivalent vapor splitter with H2RCY split fraction 0.92 of VAP.",
        "LFLOW is an FSplit or equivalent liquid splitter with CHRCY split fraction 0.30 of LIQ.",
        "Final stream readbacks confirm VAP and LIQ originate from HP-SEP and feed the specified splitters."
      ]
    },
    {
      "kind": "stagewise_column",
      "required": true,
      "allowed_surrogate": false,
      "why": "最终产品来自 COLUMN；任务明确要求 COLUMN 为 RadFrac，给出理论板数、回流比、进料板、塔压、馏出物采出率和部分冷凝器气相采出要求。",
      "deterministic_evidence": [
        "COLUMN is a RadFrac block or Aspen native rigorous column block with 12 theoretical stages.",
        "COLFD feeds stage 8.",
        "Column pressure is 1.5 MPa.",
        "Reflux ratio is 1.2.",
        "Distillate withdrawal rate is 99 kmol/h.",
        "Condenser is a partial condenser with vapor-only distillate/light-end withdrawal, consistent with LTENDS as light-end outlet and PRODUCT as product outlet.",
        "Final Aspen stream readbacks identify which column outlet is PRODUCT and provide its composition."
      ]
    },
    {
      "kind": "pressure_transform_unit_fidelity",
      "required": true,
      "allowed_surrogate": false,
      "why": "任务目标包括熟悉压力变换单元，并逐项规定 FEEDPUMP、PUMP、COMP、VALVE、PIPE 的规格；这些规格会影响 recycle 和最终产品组成，不能被省略或互换。",
      "deterministic_evidence": [
        "FEEDPUMP is located only on the fresh benzene branch BZIN -> FEEDPUMP -> BZIN2.",
        "Recycle liquid PUMP is located only on CHRCY -> PUMP -> CHRCY2 and uses fixed outlet pressure 2.6 MPa.",
        "COMP is located on H2RCY -> COMP -> H2RCY2 and uses isentropic compressor semantics with pressure increase 0.4 MPa.",
        "VALVE is located on PURGE -> VALVE -> PURGE2 and has outlet pressure 2 MPa with V810 equal-percent globe valve, nominal diameter 1.5 in.",
        "PIPE is located on CHRCY2 -> PIPE -> CHRCY3 and has carbon steel, schedule 40, diameter 1 in, length 25 m.",
        "Final Aspen block and stream readbacks confirm pressure changes on each pressure-transform unit from calculated outlet streams, not merely configured helper values."
      ]
    },
    {
      "kind": "pump_curve_fidelity",
      "required": true,
      "allowed_surrogate": false,
      "why": "任务单独强调泵特性曲线属于新鲜苯 FEEDPUMP，必须保持曲线模式，不能切换为固定出口压力，且不得把曲线写到循环液相 PUMP。",
      "deterministic_evidence": [
        "FEEDPUMP actual specification mode/readback shows pump-curve mode active after all inputs are written.",
        "FEEDPUMP pump efficiency is 0.6 and driver efficiency is 0.9.",
        "FEEDPUMP curve table contains flow entries 20, 10, 5, 3 m3/h.",
        "FEEDPUMP curve table contains corresponding head entries 40, 250, 300, 400 after explicitly documented unit interpretation and conversion into Aspen-native curve units.",
        "FEEDPUMP outlet state is Aspen-calculated from the curve and actual flow; evidence does not replace it with downstream FEED-MIX pressure 2.3 MPa or a fixed pump outlet pressure.",
        "PUMP on the CHRCY recycle branch has no copied FEEDPUMP curve and instead uses fixed outlet pressure 2.6 MPa.",
        "Readbacks show FEEDPUMP connects BZIN -> BZIN2 and PUMP connects CHRCY -> CHRCY2."
      ]
    },
    {
      "kind": "result_path_no_surrogate",
      "required": true,
      "allowed_surrogate": false,
      "why": "目标是求产品物流中环己烷的摩尔分数；该数值必须来自收敛 Aspen Plus 模型的 PRODUCT 物流组成输出，而不能由进料、化学计量、指定转化率或手算近似代替。",
      "deterministic_evidence": [
        "Final run status is converged with recycle closure.",
        "Reported value is read from Aspen results for stream PRODUCT, component C6H12/cyclohexane, mole-fraction basis.",
        "Evidence includes Aspen result path or tabular readback identifying stream PRODUCT and component cyclohexane.",
        "No direct input specification fixes PRODUCT cyclohexane mole fraction to the reported value.",
        "No hand stoichiometric calculation, feed composition, reactor conversion alone, or column input specification is used as the final answer."
      ]
    },
    {
      "kind": "convergence_and_rep_evidence",
      "required": false,
      "allowed_surrogate": false,
      "why": "流程含气相与液相回收支路、反应、闪蒸和精馏；产品组成只有在 Aspen 计算收敛后才可接受。",
      "deterministic_evidence": [
        "Aspen run status indicates successful completion/convergence.",
        "Recycle tear streams, if any, are converged within Aspen tolerances.",
        "No required block reports fatal errors or unexecuted status.",
        "PRODUCT stream flow and composition are available in final results."
      ],
      "scoring_only": true
    }
  ],
  "optional_fidelity_gates": [
    {
      "kind": "component_material_balance",
      "required": false,
      "scoring_only": true,
      "why": "完整组分物料衡算有助于审查反应、闪蒸、分流、循环和精馏是否一致，但任务的核心交付是 PRODUCT 中环己烷摩尔分数。",
      "deterministic_evidence": [
        "Report component molar flow table for BZIN, H2IN, RXIN, RXOUT, VAP, LIQ, COLFD, LTENDS, PRODUCT, H2RCY2, and CHRCY3.",
        "Show benzene consumption and cyclohexane formation are consistent with Rstoic conversion within simulation tolerance."
      ]
    },
    {
      "kind": "pressure_profile_report",
      "required": false,
      "scoring_only": true,
      "why": "题目强调压力变换单元；除必须的规格与结果读回外，完整压力剖面报告可提高可审查性。",
      "deterministic_evidence": [
        "Report inlet/outlet pressures for FEEDPUMP, FEED-MIX, REACT, HP-SEP, COMP, VALVE, PUMP, PIPE, COLUMN, and associated streams.",
        "Highlight pressure changes caused by pump curve, fixed-pressure pump, compressor pressure increment, valve outlet pressure, pipe pressure behavior, and separator/reactor pressure drops."
      ]
    },
    {
      "kind": "composition_basis_writeup",
      "required": false,
      "scoring_only": true,
      "why": "产品摩尔分数通常应为 PRODUCT 全物流摩尔分数；明确组成基准和 Aspen 坐标可避免把归一化烃类组成或质量分数误报为摩尔分数。",
      "deterministic_evidence": [
        "State that the reported cyclohexane value is the raw full-stream mole fraction in PRODUCT unless an explicitly separate normalized diagnostic is also shown.",
        "Identify Aspen stream-result table, component ID, and mole-fraction basis used."
      ]
    },
    {
      "kind": "property_method_contract",
      "required": false,
      "allowed_surrogate": false,
      "why": "任务明确规定物性方法为 RK-SOAVE；产品物流中环己烷摩尔分数必须由使用该物性方法的 Aspen Plus 模型计算得到。",
      "deterministic_evidence": [
        "Aspen Properties/Setup readback shows global property method RK-SOAVE.",
        "Final reported PRODUCT composition is from a run using RK-SOAVE, not from a different method or hand calculation."
      ],
      "scoring_only": true
    },
    {
      "kind": "convergence_and_rep_evidence",
      "required": false,
      "allowed_surrogate": false,
      "why": "流程含气相与液相回收支路、反应、闪蒸和精馏；产品组成只有在 Aspen 计算收敛后才可接受。",
      "deterministic_evidence": [
        "Aspen run status indicates successful completion/convergence.",
        "Recycle tear streams, if any, are converged within Aspen tolerances.",
        "No required block reports fatal errors or unexecuted status.",
        "PRODUCT stream flow and composition are available in final results."
      ],
      "scoring_only": true
    }
  ],
  "required_analysis_objects": [],
  "optional_analysis_objects": [],
  "analysis_object_adjudication": {
    "mode": "llm_soft_judgment",
    "native_required_kinds": [],
    "optional_bonus_kinds": [],
    "not_required_kinds": [
      {
        "kind": "design_spec",
        "why_not_required": "任务给出固定流程与固定操作规格，并要求计算 PRODUCT 中环己烷摩尔分数；没有要求用 Aspen Design Spec 调节变量以达到产品指标。",
        "confidence": "high"
      },
      {
        "kind": "sensitivity",
        "why_not_required": "任务没有要求灵敏度分析、参数扫描、变量变化曲线或响应表；泵曲线本身是设备规格，不是 Aspen Sensitivity 研究。",
        "confidence": "high"
      },
      {
        "kind": "optimization",
        "why_not_required": "任务没有要求最大化、最小化、选择最优条件或使用 Aspen Optimization；所有主要操作条件均已给定。",
        "confidence": "high"
      }
    ],
    "review_needed": false,
    "review_reason": "分析对象需求不含明显歧义；任务是固定流程建模与结果读取，而非设计规格、灵敏度或优化研究。"
  },
  "result_path_requirements": [
    {
      "result": "PRODUCT stream cyclohexane mole fraction",
      "must_derive_from": [
        "Converged Aspen Plus results",
        "Stream PRODUCT composition table",
        "Component cyclohexane/C6H12 mole fraction",
        "Full flowsheet containing FEEDPUMP, FEED-MIX, REACT, HP-SEP, VFLOW, COMP, VALVE, LFLOW, PUMP, PIPE, and COLUMN",
        "Closed gas recycle H2RCY/H2RCY2 and liquid recycle CHRCY/CHRCY2/CHRCY3",
        "RK-SOAVE property method"
      ],
      "forbid_sources": [
        "Feed composition alone",
        "Stoichiometric hand calculation from 99.8% benzene conversion",
        "Assumed pure cyclohexane product",
        "Column distillate rate or reflux ratio used as a proxy for product composition",
        "Any direct PRODUCT composition input specification",
        "Unconverged or open-loop flowsheet results"
      ],
      "why": "目标量是最终产品物流的 Aspen 输出摩尔分数，受反应、闪蒸、循环、压力单元和 RadFrac 分离共同影响。"
    },
    {
      "result": "FEEDPUMP outlet state and pressure contribution to BZIN2",
      "must_derive_from": [
        "FEEDPUMP active pump-curve mode",
        "Actual BZIN flow through FEEDPUMP",
        "Pump curve flow/head table with documented head-unit interpretation and conversion",
        "FEEDPUMP efficiency and driver efficiency readbacks",
        "Final BZIN2 stream readback"
      ],
      "forbid_sources": [
        "Directly setting FEEDPUMP fixed outlet pressure",
        "Using FEED-MIX pressure 2.3 MPa as FEEDPUMP outlet pressure",
        "Copying the curve to recycle PUMP instead of FEEDPUMP",
        "Using the raw head numbers in an SI curve table without unit conversion documentation"
      ],
      "why": "任务明确要求曲线在 FEEDPUMP 上有效参与计算，且出口状态不得由下游压力替代。"
    },
    {
      "result": "Recycle-closed PRODUCT composition",
      "must_derive_from": [
        "Aspen converged recycle solution",
        "H2 recycle from VFLOW through COMP back to FEED-MIX",
        "Liquid recycle from LFLOW through PUMP and PIPE back to FEED-MIX"
      ],
      "forbid_sources": [
        "Single-pass reactor/separator calculation without recycles",
        "Disconnected recycle streams with guessed makeup values",
        "Manual iteration not reflected in final Aspen results"
      ],
      "why": "任务文字和图示均要求循环氢气和液相物流回到反应器入口，产品组成必须来自闭合流程。"
    }
  ],
  "numeric_acceptance_metrics": [
    {
      "metric": "H2IN temperature",
      "operator": "=",
      "value": 50,
      "unit": "degC",
      "evidence": "物流 H2IN：温度 50℃。"
    },
    {
      "metric": "H2IN pressure",
      "operator": "=",
      "value": 2.5,
      "unit": "MPa",
      "evidence": "物流 H2IN：压力 2.5 MPa。"
    },
    {
      "metric": "H2IN total molar flow",
      "operator": "=",
      "value": 330,
      "unit": "kmol/h",
      "evidence": "物流 H2IN：总流量 330 kmol/h。"
    },
    {
      "metric": "H2IN mole fractions",
      "operator": "=",
      "value": "H2 0.975, N2 0.005, CH4 0.02",
      "unit": "mole fraction",
      "evidence": "H2、N2、CH4 的摩尔分数分别为 0.975、0.005 和 0.02。"
    },
    {
      "metric": "BZIN temperature",
      "operator": "=",
      "value": 40,
      "unit": "degC",
      "evidence": "物流 BZIN：温度 40℃。"
    },
    {
      "metric": "BZIN pressure",
      "operator": "=",
      "value": 0.1,
      "unit": "MPa",
      "evidence": "物流 BZIN：压力 0.1 MPa。"
    },
    {
      "metric": "BZIN molar flow",
      "operator": "=",
      "value": 100,
      "unit": "kmol/h",
      "evidence": "物流 BZIN：纯苯，流量 100 kmol/h。"
    },
    {
      "metric": "BZIN composition",
      "operator": "=",
      "value": "pure benzene",
      "unit": "component basis",
      "evidence": "物流 BZIN：组分为纯苯。"
    },
    {
      "metric": "FEED-MIX temperature",
      "operator": "=",
      "value": 150,
      "unit": "degC",
      "evidence": "模块 FEED-MIX（Heater 模块）：温度 150℃。"
    },
    {
      "metric": "FEED-MIX pressure",
      "operator": "=",
      "value": 2.3,
      "unit": "MPa",
      "evidence": "模块 FEED-MIX（Heater 模块）：压力 2.3 MPa。"
    },
    {
      "metric": "REACT temperature",
      "operator": "=",
      "value": 200,
      "unit": "degC",
      "evidence": "模块 REACT（Rstoic 模块）：温度 200℃。"
    },
    {
      "metric": "REACT pressure drop",
      "operator": "=",
      "value": 0.1,
      "unit": "MPa",
      "evidence": "模块 REACT（Rstoic 模块）：压降 0.1 MPa。"
    },
    {
      "metric": "Benzene conversion in REACT",
      "operator": "=",
      "value": 0.998,
      "unit": "fraction",
      "evidence": "苯的转化率为 99.8%；REACT 中苯的转化率 0.998。"
    },
    {
      "metric": "VFLOW H2RCY split fraction",
      "operator": "=",
      "value": 0.92,
      "unit": "fraction of VAP",
      "evidence": "模块 VFLOW（FSplit 模块）：物流 H2RCY 的分数 92%。"
    },
    {
      "metric": "LFLOW CHRCY split fraction",
      "operator": "=",
      "value": 0.3,
      "unit": "fraction of LIQ",
      "evidence": "模块 LFLOW（FSplit 模块）：物流 CHRCY 的分数为 30%。"
    },
    {
      "metric": "HP-SEP temperature",
      "operator": "=",
      "value": 50,
      "unit": "degC",
      "evidence": "模块 HP-SEP（Flash2 模块）：温度 50℃。"
    },
    {
      "metric": "HP-SEP pressure drop",
      "operator": "=",
      "value": 0.05,
      "unit": "MPa",
      "evidence": "模块 HP-SEP（Flash2 模块）：压降 0.05 MPa。"
    },
    {
      "metric": "COLUMN theoretical stages",
      "operator": "=",
      "value": 12,
      "unit": "stages",
      "evidence": "模块 COLUMN（RadFrac 模块）：理论板数 12。"
    },
    {
      "metric": "COLUMN reflux ratio",
      "operator": "=",
      "value": 1.2,
      "unit": "dimensionless",
      "evidence": "模块 COLUMN（RadFrac 模块）：回流比 1.2。"
    },
    {
      "metric": "COLUMN feed stage",
      "operator": "=",
      "value": 8,
      "unit": "stage number",
      "evidence": "模块 COLUMN（RadFrac 模块）：进料位置第 8 块理论板。"
    },
    {
      "metric": "COLUMN pressure",
      "operator": "=",
      "value": 1.5,
      "unit": "MPa",
      "evidence": "模块 COLUMN（RadFrac 模块）：塔压 1.5 MPa。"
    },
    {
      "metric": "COLUMN distillate withdrawal rate",
      "operator": "=",
      "value": 99,
      "unit": "kmol/h",
      "evidence": "模块 COLUMN（RadFrac 模块）：塔馏出物采出率 99 kmol/h。"
    },
    {
      "metric": "COLUMN condenser type",
      "operator": "=",
      "value": "partial condenser with vapor-only distillate withdrawal",
      "unit": "configuration",
      "evidence": "冷凝器为只有气相采出的部分冷凝器。"
    },
    {
      "metric": "FEEDPUMP pump efficiency",
      "operator": "=",
      "value": 0.6,
      "unit": "fraction",
      "evidence": "模块 FEEDPUMP：泵的效率 0.6；泵特性曲线说明重复要求 FEEDPUMP 的泵效率为 0.6。"
    },
    {
      "metric": "FEEDPUMP driver efficiency",
      "operator": "=",
      "value": 0.9,
      "unit": "fraction",
      "evidence": "模块 FEEDPUMP：驱动机效率 0.9。"
    },
    {
      "metric": "FEEDPUMP curve flow points",
      "operator": "=",
      "value": "20, 10, 5, 3",
      "unit": "m3/h",
      "evidence": "泵特性曲线：流量 / (m3/h) 为 20、10、5、3。"
    },
    {
      "metric": "FEEDPUMP curve head points",
      "operator": "=",
      "value": "40, 250, 300, 400 with documented unit interpretation and Aspen-native conversion",
      "unit": "head units unspecified in source",
      "evidence": "泵特性曲线：扬程 40、250、300、400；原文未标明单位，写入 Aspen 前须明确记录所采用的单位解释并转换。"
    },
    {
      "metric": "Recycle liquid PUMP outlet pressure",
      "operator": "=",
      "value": 2.6,
      "unit": "MPa",
      "evidence": "模块 PUMP（Pump HI）：出口压力 2.6 MPa。"
    },
    {
      "metric": "COMP pressure increase",
      "operator": "=",
      "value": 0.4,
      "unit": "MPa",
      "evidence": "模块 COMP（Compr 模块）：采用等熵压缩机，压力增量 0.4 MPa。"
    },
    {
      "metric": "VALVE outlet pressure",
      "operator": "=",
      "value": 2,
      "unit": "MPa",
      "evidence": "模块 VALVE（Valve 模块）：出口压力 2 MPa。"
    },
    {
      "metric": "VALVE specification",
      "operator": "=",
      "value": "V810 equal percent flow globe valve, nominal diameter 1.5 in",
      "unit": "valve configuration",
      "evidence": "阀门规格 V810 equal percent flow 截止阀，公称直径 1.5 in。"
    },
    {
      "metric": "PIPE material",
      "operator": "=",
      "value": "carbon steel",
      "unit": "material",
      "evidence": "模块 PIPE（Pipe 模块）：材质为碳钢。"
    },
    {
      "metric": "PIPE schedule",
      "operator": "=",
      "value": 40,
      "unit": "schedule number",
      "evidence": "模块 PIPE（Pipe 模块）：系列号 40。"
    },
    {
      "metric": "PIPE diameter",
      "operator": "=",
      "value": 1,
      "unit": "in",
      "evidence": "模块 PIPE（Pipe 模块）：直径 1 in。"
    },
    {
      "metric": "PIPE length",
      "operator": "=",
      "value": 25,
      "unit": "m",
      "evidence": "模块 PIPE（Pipe 模块）：长度 25 m。"
    },
    {
      "metric": "PRODUCT cyclohexane mole fraction",
      "operator": "report",
      "value": "Aspen-calculated value",
      "unit": "mole fraction",
      "evidence": "目标：求产品物流中环己烷的摩尔分数。"
    }
  ],
  "component_role_contract": {
    "feed_components": [
      {
        "name": "benzene / C6H6",
        "role": "fresh reactant feed in BZIN; hydrogenation reactant converted in REACT",
        "source_text": "物流 BZIN：组分为纯苯，流量 100 kmol/h；反应 C6H6 + 3H2 -> C6H12。"
      },
      {
        "name": "hydrogen / H2",
        "role": "fresh reactant feed in H2IN and main gas recycle component",
        "source_text": "物流 H2IN：H2 摩尔分数 0.975；苯加氢反应需要 H2；部分轻气体作为循环氢气返回反应器。"
      },
      {
        "name": "nitrogen / N2",
        "role": "inert/light-gas component in H2IN",
        "source_text": "物流 H2IN：N2 摩尔分数 0.005。"
      },
      {
        "name": "methane / CH4",
        "role": "inert/light-gas component in H2IN",
        "source_text": "物流 H2IN：CH4 摩尔分数 0.02。"
      }
    ],
    "product_components": [
      {
        "name": "cyclohexane / C6H12",
        "role": "desired product component whose mole fraction in PRODUCT is the requested result",
        "source_text": "环己烷可以用苯加氢反应得到；目标：求产品物流中环己烷的摩尔分数。"
      }
    ],
    "solvents_or_auxiliaries": [],
    "recycle_components": [
      {
        "name": "hydrogen / H2",
        "role": "gas recycle component in H2RCY/H2RCY2 returned to FEED-MIX/reactor feed",
        "source_text": "部分轻气体作为循环氢气返回反应器；VFLOW 中 H2RCY 的分数 92%。"
      },
      {
        "name": "cyclohexane / C6H12",
        "role": "liquid recycle component in CHRCY/CHRCY2/CHRCY3 used to help control reactor temperature",
        "source_text": "苯和氢气进料与循环氢气和环己烷混合；其余液相物流进入反应器，辅助控制温度；LFLOW 中 CHRCY 分数 30%。"
      },
      {
        "name": "light gases",
        "role": "may be present in vapor recycle/purge and are separated in HP-SEP/COLUMN",
        "source_text": "轻气体从两相闪蒸器中分离出去；部分轻气体作为循环氢气返回反应器；精馏塔进一步脱除溶解的轻气体。"
      }
    ],
    "semantic_conflicts": []
  },
  "immutability_classification": {
    "immutable_task_specs": [
      "Component set includes benzene/C6H6, hydrogen/H2, nitrogen/N2, methane/CH4, and cyclohexane/C6H12.",
      "Reaction is C6H6 + 3H2 -> C6H12.",
      "Property method is RK-SOAVE.",
      "H2IN conditions: 50 °C, 2.5 MPa, 330 kmol/h, mole fractions H2 0.975, N2 0.005, CH4 0.02.",
      "BZIN conditions: 40 °C, 0.1 MPa, pure benzene, 100 kmol/h.",
      "FEED-MIX is specified as Heater module with 150 °C and 2.3 MPa.",
      "REACT is specified as Rstoic with 200 °C, 0.1 MPa pressure drop, benzene conversion 0.998.",
      "HP-SEP is specified as Flash2 with 50 °C and 0.05 MPa pressure drop.",
      "VFLOW is specified as FSplit with H2RCY fraction 92%.",
      "LFLOW is specified as FSplit with CHRCY fraction 30%.",
      "COLUMN is specified as RadFrac with 12 theoretical stages, reflux ratio 1.2, feed stage 8, pressure 1.5 MPa, distillate withdrawal rate 99 kmol/h, and partial condenser with vapor-only distillate withdrawal.",
      "FEEDPUMP belongs to BZIN -> FEEDPUMP -> BZIN2 fresh benzene branch and must use pump-curve mode.",
      "FEEDPUMP pump efficiency is 0.6 and driver efficiency is 0.9.",
      "FEEDPUMP curve flow points are 20, 10, 5, 3 m3/h and head entries are 40, 250, 300, 400 with explicit unit interpretation before Aspen entry.",
      "Recycle liquid PUMP belongs to CHRCY branch and uses fixed outlet pressure 2.6 MPa; the FEEDPUMP curve must not be assigned to it.",
      "COMP is an isentropic compressor with pressure increase 0.4 MPa.",
      "VALVE outlet pressure is 2 MPa with V810 equal percent flow globe valve, nominal diameter 1.5 in.",
      "PIPE is carbon steel, schedule 40, diameter 1 in, length 25 m.",
      "Visible topology and stream labels from the figure: FEEDPUMP, FEED-MIX, REACT, HP-SEP, VFLOW, VALVE, COMP, LFLOW, PUMP, PIPE, COLUMN; streams BZIN, BZIN2, H2IN, H2RCY, H2RCY2, RXIN, RXOUT, VAP, PURGE, PURGE2, LIQ, COLFD, PRODUCT, LTENDS, CHRCY, CHRCY2, CHRCY3.",
      "Requested result is PRODUCT stream cyclohexane mole fraction."
    ],
    "provisional_model_assumptions": [
      "Interpretation of the pump-curve head unit is not specified by the source text and must be explicitly documented before conversion to Aspen-native curve units.",
      "Aspen component databank IDs and aliases for benzene, hydrogen, nitrogen, methane, and cyclohexane may be chosen by the modeler if chemically unambiguous.",
      "Numerical convergence settings, tear-stream initial guesses, and recycle initialization values are modeler choices.",
      "If Aspen requires additional RadFrac condenser/reboiler options not specified beyond the given condenser, reflux ratio, stages, pressure, feed stage, and distillate rate, those detailed settings are modeler assumptions consistent with the task.",
      "If block aliases are used, they must preserve branch ownership and topology even if IDs differ from the task labels."
    ],
    "exploration_dimensions": [
      "Recycle tear stream selection and initial estimates may be varied to obtain convergence.",
      "Numerical solver methods and tolerances may be adjusted without changing task specifications.",
      "Documented pump-head unit interpretation can be checked for consistency, but raw curve ownership and flow/head data cannot be reassigned.",
      "Aspen implementation details for pressure-drop calculations in PIPE may be adjusted only within the specified material, schedule, diameter, and length constraints.",
      "RadFrac numerical initialization may be varied while preserving all specified column conditions."
    ],
    "classification_notes": [
      "The pump curve is immutable in branch assignment and data values, but its unspecified head unit creates a required documented interpretation rather than a free numerical target.",
      "The task does not provide an expected numeric cyclohexane mole fraction; the accepted result is a reported Aspen output value with proper evidence path.",
      "Figure-derived topology is authoritative for visible stream connections and confirms that FEEDPUMP and PUMP are distinct devices on different branches."
    ]
  },
  "uncertainties": [
    "The pump-curve head unit is not stated; validation must require an explicit unit interpretation and conversion before Aspen entry.",
    "The task states COLUMN distillate withdrawal rate 99 kmol/h and a partial condenser with vapor-only distillate withdrawal; the final model must clearly map LTENDS and PRODUCT to RadFrac outlets and show PRODUCT is the requested product stream.",
    "The figure contains no numeric conditions; numeric specifications come from the written task text.",
    "The PRODUCT cyclohexane mole fraction has no target numeric value in the task and must be reported from final Aspen results rather than compared to a preset acceptance number."
  ],
  "figure_context_used": true,
  "figure_image_references": [
    "./images/exercise_5_1_flow.png"
  ],
  "figure_resolved_image_paths": [
    "tasks/test/chn/chapter_05/images/exercise_5_1_flow.png"
  ],
  "figure_grounding_summary": "## Figure-Derived Supplement\n\nFor topology, visible stream labels, stream types, and figure-shown coupling, the figure evidence below is the highest-priority task source.\nTreat the `labels_and_topology` answer as the visible topology contract. Icon-family candidates are only block-type hints and must not split, remove, rename, or invent visible nodes.\nUse written text/tables for numeric conditions or semantics that are not visible in the figure, but do not silently overwrite a visible figure fact.\nIf any figure note conflicts with the written markdown or a generated split-task description, keep the conflict visible as a blocker until resolved.\n\n### Image: `tasks/test/chn/chapter_05/images/exercise_5_1_flow.png`\n\n- Question `subfigure_scope_and_authority`: 请只根据题图和任务上下文，判断这张图是否包含多个子图/流程。列出每个可见子图的标题或图注，并说明当前任务最可能对应哪个子图。如果正文派生描述与图中可见连接或标签冲突，必须把冲突列为 blocking uncertainty，不要自动用正文覆盖题图。选择子图时优先使用明确的流程安排词，例如 并流、错流、parallel、co-current、cross-flow；不要把 part_a、part_b 或生成的 split id 当作权威依据。如果 split id 与流程安排词冲突，必须报告冲突并以流程安排词为准。\n  - Direct answer: 这张题图不包含多个子图/流程；可见的是一个完整的 Aspen Plus 环己烷生产流程图。图中没有可见的子图编号、子图标题或单独图注。任务最可能对应该唯一流程图，即“习题 5.1 流程图”所示的环己烷生产流程。\n  - Visual evidence: 整张图是一个连续连接的流程网络，没有分隔框、(a)/(b)、part_a/part_b、并列面板或多个独立流程。\n  - Visual evidence: 可见设备/模块包括：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。\n  - Visual evidence: 可见物流标签包括：BZIN、BZIN2、H2IN、H2RCY、H2RCY2、RXIN、RXOUT、VAP、PURGE、PURGE2、LIQ、COLFD、PRODUCT、LTENDS、CHRCY、CHRCY2、CHRCY3。\n  - Visual evidence: 流程连接显示为单一工艺：BZIN 经 FEEDPUMP 到 FEED-MIX；H2IN 和回收气 H2RCY2 也进入 FEED-MIX；REACT 出料 RXOUT 进入 HP-SEP；气相 VAP 经 VFLOW 分成 H2RCY 回收和 PURGE 排放；液相 LIQ 经 LFLOW 分成进入 COLUMN 的 COLFD 和回流反应器的 CHRCY 支路。\n  - Visual evidence: 图中未见“并流”、“错流”、“parallel”、“co-current”、“cross-flow”等多个流程安排词，也未见多个可选流程布局。\n  - Uncertainty: 图中没有内嵌标题或图注；“习题 5.1 流程图”来自任务上下文而不是图内可见文字。\n  - Uncertainty: 未发现任务正文与图中可见连接或标签之间的 blocking conflict。\n- Question `labels_and_topology`: 请只根据这张题图，列出图中清晰可见的模块/设备标签、物流标签，以及这些物流与模块之间直接可见的连接关系。把这部分当作拓扑合同：可见模块/设备标签是节点，物流标签是边；对每条边尽量写清 from -> through/into -> to。如果一个可见设备标签处同时汇合多股物流或分出多股物流，只记录为一个可见节点及其 fan-in/fan-out，不要因为过程语义、多条反应方程式或图标候选把它拆成多个未在图中标出的节点。一个可见反应器就是一个节点；同一设备中的主反应和副反应仍属于这一个节点。若正文给出 Aspen block type，而图中只显示设备标签，请把 visible_label 与 type_from_context 分开记录；图标类型候选不能覆盖、删除、拆分或新增这里的可见标签节点。不要补充图中看不清或未出现的名称。\n  - Direct answer: {'visible_modules_or_equipment_nodes': [{'visible_label': 'FEEDPUMP', 'type_from_context': 'Pump'}, {'visible_label': 'FEED-MIX', 'type_from_context': 'Heater'}, {'visible_label': 'REACT', 'type_from_context': 'Rstoic'}, {'visible_label': 'HP-SEP', 'type_from_context': 'Flash2'}, {'visible_label': 'VFLOW', 'type_from_context': 'FSplit'}, {'visible_label': 'VALVE', 'type_from_context': 'Valve'}, {'visible_label': 'COMP', 'type_from_context': 'Compr'}, {'visible_label': 'LFLOW', 'type_from_context': 'FSplit'}, {'visible_label': 'PUMP', 'type_from_context': 'Pump HI'}, {'visible_label': 'PIPE', 'type_from_context': 'Pipe'}, {'visible_label': 'COLUMN', 'type_from_context': 'RadFrac'}], 'visible_stream_edges_and_connections': [{'stream_label': 'BZIN', 'connection': 'external source -> FEEDPUMP'}, {'stream_label': 'BZIN2', 'connection': 'FEEDPUMP -> FEED-MIX'}, {'stream_label': 'H2IN', 'connection': 'external source -> FEED-MIX'}, {'stream_label': 'H2RCY2', 'connection': 'COMP -> FEED-MIX'}, {'stream_label': 'CHRCY3', 'connection': 'PIPE -> FEED-MIX'}, {'stream_label': 'RXIN', 'connection': 'FEED-MIX -> REACT'}, {'stream_label': 'RXOUT', 'connection': 'REACT -> HP-SEP'}, {'stream_label': 'VAP', 'connection': 'HP-SEP -> VFLOW'}, {'stream_label': 'H2RCY', 'connection': 'VFLOW -> COMP'}, {'stream_label': 'PURGE', 'connection': 'VFLOW -> VALVE'}, {'stream_label': 'PURGE2', 'connection': 'VALVE -> external sink'}, {'stream_label': 'LIQ', 'connection': 'HP-SEP -> LFLOW'}, {'stream_label': 'CHRCY', 'connection': 'LFLOW -> PUMP'}, {'stream_label': 'CHRCY2', 'connection': 'PUMP -> PIPE'}, {'stream_label': 'COLFD', 'connection': 'LFLOW -> COLUMN'}, {'stream_label': 'LTENDS', 'connection': 'COLUMN -> external sink'}, {'stream_label': 'PRODUCT', 'connection': 'COLUMN -> external sink'}], 'visible_node_fan_in_fan_out': [{'node': 'FEEDPUMP', 'fan_in': ['BZIN'], 'fan_out': ['BZIN2']}, {'node': 'FEED-MIX', 'fan_in': ['BZIN2', 'H2IN', 'H2RCY2', 'CHRCY3'], 'fan_out': ['RXIN']}, {'node': 'REACT', 'fan_in': ['RXIN'], 'fan_out': ['RXOUT']}, {'node': 'HP-SEP', 'fan_in': ['RXOUT'], 'fan_out': ['VAP', 'LIQ']}, {'node': 'VFLOW', 'fan_in': ['VAP'], 'fan_out': ['H2RCY', 'PURGE']}, {'node': 'COMP', 'fan_in': ['H2RCY'], 'fan_out': ['H2RCY2']}, {'node': 'VALVE', 'fan_in': ['PURGE'], 'fan_out': ['PURGE2']}, {'node': 'LFLOW', 'fan_in': ['LIQ'], 'fan_out': ['CHRCY', 'COLFD']}, {'node': 'PUMP', 'fan_in': ['CHRCY'], 'fan_out': ['CHRCY2']}, {'node': 'PIPE', 'fan_in': ['CHRCY2'], 'fan_out': ['CHRCY3']}, {'node': 'COLUMN', 'fan_in': ['COLFD'], 'fan_out': ['LTENDS', 'PRODUCT']}]}\n  - Visual evidence: 图中可清晰读到设备/模块标签：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。\n  - Visual evidence: 图中可清晰读到物流标签：BZIN、BZIN2、H2IN、H2RCY、H2RCY2、RXIN、RXOUT、VAP、PURGE、PURGE2、LIQ、COLFD、PRODUCT、LTENDS、CHRCY、CHRCY2、CHRCY3。\n  - Visual evidence: FEED-MIX 处可见多股物流汇合：BZIN2、H2IN、H2RCY2、CHRCY3，并输出 RXIN。\n  - Visual evidence: HP-SEP 顶部可见 VAP 至 VFLOW，底部可见 LIQ 至 LFLOW。\n  - Visual evidence: VFLOW 可见分出 H2RCY 至 COMP，以及 PURGE 至 VALVE；VALVE 后为 PURGE2。\n  - Visual evidence: LFLOW 可见分出 COLFD 至 COLUMN，以及 CHRCY 至 PUMP；PUMP、PIPE 后回到 FEED-MIX 的 CHRCY3。\n  - Visual evidence: COLUMN 可见 COLFD 进入，LTENDS 与 PRODUCT 输出。\n  - Uncertainty: 个别物流箭头方向较小，但整体连线和箭头显示支持上述 from -> to 方向。\n  - Uncertainty: type_from_context 来自题干上下文，不是图中直接显示；图中直接可见的是 visible_label。\n  - Uncertainty: 图中没有显示外部源/汇的名称，因此用 external source 和 external sink 表示边界连接。\n- Question `numbers_and_constraints`: 请只根据这张题图，列出图中清晰可见的数值、单位、阶段号、图注、操作条件、产品/回流/循环说明，以及任何对 Aspen 建模重要但正文可能没有写出的可见约束。不要猜测。\n  - Direct answer: {'清晰可见的数值': '未见任何清晰的工艺数值参数。图中可见的“2”“3”等只出现在物流名如 H2IN、H2RCY2、BZIN2、CHRCY2、CHRCY3、PURGE2 中，不能解读为数值条件。', '清晰可见的单位': '未见单位。', '清晰可见的阶段号': '未见塔板号、阶段号或进料板号。', '清晰可见的图注': '未见独立图题、图注或说明文字；只有设备/模块名与物流名。', '清晰可见的操作条件': '未见温度、压力、流量、转化率、压降、回流比、采出率、效率、管径、长度等操作条件。', '清晰可见的产品/回流/循环说明': {'产品物流': 'COLUMN 输出物流标为 PRODUCT；另有顶部/轻端输出 LTENDS。', '放空气/排放': 'HP-SEP 顶部 VAP 进入 VFLOW；VFLOW 分出 PURGE，经 VALVE 后为 PURGE2，排出系统。', '气相循环': 'VFLOW 分出的 H2RCY 进入 COMP，压缩后物流为 H2RCY2，并返回 FEED-MIX。', '液相循环': 'HP-SEP 底部 LIQ 进入 LFLOW；LFLOW 分出 CHRCY，经 PUMP 为 CHRCY2，再经 PIPE 为 CHRCY3，返回 FEED-MIX。', '进入精馏塔的物流': 'LFLOW 另一出口 COLFD 进入 COLUMN。'}, '对_Aspen_建模重要的可见约束': ['FEEDPUMP 只位于新鲜 BZIN 支路：BZIN -> FEEDPUMP -> BZIN2。', 'FEED-MIX 有四股入口物流：BZIN2、H2IN、H2RCY2、CHRCY3；出口为 RXIN。', '反应器连接为：FEED-MIX -> RXIN -> REACT -> RXOUT -> HP-SEP。', 'HP-SEP 显示为两相分离节点：顶部/气相出口 VAP，底部/液相出口 LIQ。', 'VFLOW 是气相分流节点：入口 VAP，出口 H2RCY 与 PURGE。', 'H2RCY 支路经过 COMP 后以 H2RCY2 返回 FEED-MIX。', 'PURGE 支路经过 VALVE 后以 PURGE2 离开流程。', 'LFLOW 是液相分流节点：入口 LIQ，出口 COLFD 与 CHRCY。', 'CHRCY 支路经过 PUMP 和 PIPE 后以 CHRCY3 返回 FEED-MIX。', 'COLFD 进入 COLUMN；COLUMN 输出 LTENDS 和 PRODUCT。', '图中没有显示任何回流物流从 COLUMN 返回塔内或其他设备；不能从图中确认回流比或冷凝器类型。', '图中没有显示 FEEDPUMP 与 PUMP 共用曲线或规格；两台泵是不同可见设备节点，分别位于 BZIN 支路和 CHRCY 循环支路。']}\n  - Visual evidence: 可见设备/模块标签：FEEDPUMP、FEED-MIX、REACT、HP-SEP、VFLOW、VALVE、COMP、LFLOW、PUMP、PIPE、COLUMN。\n  - Visual evidence: 可见物流标签：BZIN、BZIN2、H2IN、H2RCY、H2RCY2、RXIN、RXOUT、VAP、PURGE、PURGE2、LIQ、COLFD、PRODUCT、LTENDS、CHRCY、CHRCY2、CHRCY3。\n  - Visual evidence: BZIN 从左侧进入 FEEDPUMP，FEEDPUMP 后的物流标为 BZIN2。\n  - Visual evidence: BZIN2、H2IN、H2RCY2、CHRCY3 四股物流汇入 FEED-MIX，FEED-MIX 出口为 RXIN。\n  - Visual evidence: RXIN 进入 REACT，REACT 出口 RXOUT 进入 HP-SEP。\n  - Visual evidence: HP-SEP 顶部物流 VAP 向上进入 VFLOW；底部物流 LIQ 向下进入 LFLOW。\n  - Visual evidence: VFLOW 右侧出口为 PURGE，经过 VALVE 后为 PURGE2；左侧出口为 H2RCY，进入 COMP 后变为 H2RCY2 返回 FEED-MIX。\n  - Visual evidence: LFLOW 右侧出口 COLFD 进入 COLUMN；左侧出口 CHRCY 经 PUMP、CHRCY2、PIPE、CHRCY3 返回 FEED-MIX。\n  - Uncertainty: 图中没有可读的数值、单位或操作条件，因此不能仅凭图确认温度、压力、流量、转化率、分流比、泵效率、塔板数、进料板、回流比等。\n  - Uncertainty: COLUMN 的 LTENDS 与 PRODUCT 位置暗示轻端/产品出口，但图中没有文字说明其相态、组成或具体采出位置。\n  - Uncertainty: 图中没有显示 COLUMN 内部回流线、冷凝器/再沸器规格或塔板编号。\n  - Uncertai",
  "source": "LLM gate contract",
  "model": "gpt-5.5",
  "analysis_policy_version": "analysis_optional_bonus_v2",
  "input_scope": "task text only; no cases.yaml block_family or baseline script",
  "_usage": {
    "model": "gpt-5.5",
    "prompt_tokens": 15266,
    "completion_tokens": 9275,
    "total_tokens": 24541
  },
  "recycle_closure_contract": {
    "closure_type": "numerical_recycle_tear",
    "accepted_topology": "task-stated physical material return paths into upstream process units",
    "physical_recycle_required": true
  },
  "requirement_registration": {
    "status": "task_specific_dynamic",
    "task_specific_kinds": [
      "pressure_transform_unit_fidelity",
      "pump_curve_fidelity",
      "reaction_separator_splitter_contract"
    ],
    "permission_granted": false,
    "validation_route": "generic_gate_adjudication"
  }
}
` ` `

### FILE: docs/hardcoded_script_plan/guide-for-hardcoded-script.md
Reason: core hardcoded script/runtime contract
` ` `text
# Hardcoded Script 编写指南

## 目标

本指南用于统一 `hardcoded script` 的编写、改造、验证与交付方式。目标不是“能跑一次”，而是形成可复用、可核验、可批量迁移的正式脚本资产。

每个正式脚本都应尽量满足以下目标：

- 从空白 session 或明确 checkpoint 起点稳定重建流程。
- 运行后输出有序证据：`REP`、`APW`、`BKP`。
- 结果可回填到 `hardcoded-script-跟踪文档.md`。
- 尽量消除 `PER_ERROR`，并记录 completion / warning / 剩余风险。

## 总原则

### 1. 先改造现有资产，不要优先从零新写

默认复用顺序：

1. `tool_side_generation/healthcheck/full_evaluation/*.py`
2. `tool_side_generation/healthcheck/full_example/*.py`
3. `tool_side_generation/healthcheck/full_example/homework/*.py`
4. `scripts/*.py`
5. 仅在现有资产明显不适配时，再新建脚本

改造前必须先回答三个问题：

- 现有脚本里已经覆盖了哪些流程拓扑、组件、模块、物性方法？
- 当前脚本失败的首个真实阻塞点是什么：命名、单位、拓扑、模块规格、工具能力，还是结果偏差？
- 是“修脚本”更快，还是“补公共底座”更快？如果是工具问题，优先修工具，再回到题脚本验证。

### 2. 以题面和题图为准，不以旧脚本为准

旧脚本只是资产，不是权威。题面、题图、表格、给定条件才是最终真值来源。

尤其要重点核对：

- 流程拓扑是否和题图一致。
- 流股/块名是否需要转换为 Aspen-safe 运行时名称。
- 单位系统是否与 setter / readback / REP 口径一致。
- 题目要求的是“建模求解”还是“分析比较”还是“参数扫描/优化”。

### 3. 先让模型表达正确，再追求结果漂亮

优先级建议：

1. 能稳定建模
2. completion 正常
3. `PER_ERROR` 归零
4. 导出证据完整
5. 结果与题意一致
6. 再做收敛质量、分析图表、可读性优化

## 正式脚本结构

正式 hardcoded script 尽量沿用 `healthcheck/full_evaluation` 现有骨架，避免平行体系。

建议结构：

1. 常量区：`TASK_SET`、`TASK_ID`、`SCRIPT_STEM`
2. 单位换算与输入数据常量
3. 小型工具函数
4. `_build_*` / `_configure_*` / `_run_*` 主流程函数
5. `main_async()`
6. 证据导出与 `summary.json`

建议复用：

- `default_task_output_dir_for_script`
- `default_task_bkp_subdir_for_script`
- `export_evidence_bundle`
- `read_per_error_best_effort`
- `resolve_server_url`
- `check_server_health_or_exit`

## 输出与证据规范

正式脚本必须按以下目录落盘：

` ` `text
data/file/output/hardcoded/tasks/<task_set>/<task_id>/<script_stem>/
` ` `

必须导出：

- `REP`
- `APW`
- `BKP`
- `summary.json`

`summary.json` 建议至少包含：

- 输入条件
- 关键建模选择
- completion 状态
- `PER_ERROR`
- 最终关键数值
- 证据文件路径
- 已知假设和剩余风险

## 注释规范

### 1. 函数入口要有结构化块注释

对外暴露的主函数、关键 builder、复杂 readback 函数，必须写结构化说明。若脚本语言支持 JSDoc，优先使用 JSDoc 风格；Python 脚本则使用等价的多行 docstring，至少说明：

- 这个函数负责什么
- 关键输入是什么
- 为什么这样建模 / 读取
- 返回值里最重要的字段是什么

### 2. 操作逻辑和变量功能必须写 inline comment

这是新增硬性要求。不是所有行都要注释，而是以下情况必须注释：

- 某段操作代表题面中的哪一个流程动作
- 为什么选这个 Aspen 规格路径，而不是另一条路径
- 某个变量的物理意义、控制作用或换算口径
- 某个读数为什么从这个节点拿，而不是别的节点
- 某个 workaround 是为了绕过什么 Aspen/MCP 限制

不合格的注释：

- “设置温度”
- “创建流股”
- “运行 Aspen”

合格的注释应解释“为什么”和“对应题意的哪一部分”，例如：

- “题面给的是泵出口压力，因此这里选 `PRES` 规格而不是 `DELT`。”
- “该变量代表题图中的液相循环支路分流比，必须在 `FSplit` 上显式固化，避免默认值漂移。”
- “这里优先从 REP 读取最终结果，保证人工核验口径与导出报告一致。”

## Aspen 原生分析工具优先级

### 1. 优先使用 Aspen 内建工具，不要默认手写 sweep

只要题意允许，优先顺序如下：

1. `Sensitivity Analysis`
2. `Design Spec`
3. `Optimization`
4. 直接求解 + 读回
5. 手写 Python 循环 sweep

原因：

- 更符合 Aspen 原生建模思路
- 结果更容易人工复核
- 更利于后续迁移到 UI / MCP / 教学示例
- 可以减少脚本里“外部控制 Aspen”的脆弱逻辑

### 2. 把分析工具当成“达成题目目标”的主路径，而不是附属展示

后续 hardcoded script 默认应主动评估这三类工具能否直接服务题目目标：

- `Sensitivity Analysis`：适合做趋势、扫描、响应面、参数影响分析
- `Design Spec`：适合做“反推某个设定值以满足目标结果”
- `Optimization`：适合做“在约束下寻找最佳操作点”

重要的是，不要把它们理解成“模型跑完以后顺手补一个图表”的附属功能。很多题目的真正目标，本来就是：

- 通过扫描找到规律
- 通过反求达到某个目标指标
- 通过优化寻找最佳条件

这类题如果只靠手写 Python 循环、外部二分、人工反复试参数来完成，通常会出现以下问题：

- 脚本表达的是“外部控制逻辑”，而不是 Aspen 原生求解意图
- 结果难以在 GUI / REP 中直接人工复核
- 后续迁移到 MCP、教学案例或 UI 自动化时，复用价值下降
- 代码里容易积累大量脆弱的试探式控制分支

因此，正式 hardcoded script 应优先问自己：

1. 这道题本质上是扫描问题吗？如果是，优先考虑 `Sensitivity Analysis`
2. 这道题本质上是反求目标值吗？如果是，优先考虑 `Design Spec`
3. 这道题本质上是寻找最优操作点吗？如果是，优先考虑 `Optimization`
4. 如果题目同时包含扫描、反求、最优条件比较，能否组合使用这三类工具，而不是退回手写控制逻辑

### 3.5 `Design Spec` 先验证“变量是否真的在块里被指定”

这是一个高频、且代价很高的坑。Design Spec helper 返回“操纵变量写入成功”，**不等于** Aspen 后续求解时认定该变量已经是 block 内有效输入。

出现下面这类报错时，默认优先怀疑“操纵变量没有在 block 中 materialize”，而不是先怀疑 Aspen 求解器失灵：

` ` `text
ERROR WHILE CHECKING INPUT SPECIFICATIONS FOR VARIED VARIABLE IN DESIGN-SPEC
THIS VARIABLE IS NOT SPECIFIED IN THE BLOCK.
YOU CAN PROVIDE AN INITIAL VALUE IN THE BLOCK OR USE ANOTHER VARIABLE.
` ` `

正式脚本里应遵守以下顺序：

1. 先确认这是不是题目真正允许变化的自由度。
2. 再确认该自由度已经通过 block setter 或树节点**真实写进 block 输入**，而不是只停留在 flowsheet 流股层或初始化猜值层。
3. 最后才把它接到 `Design Spec` 的 `helper-managed manipulated-variable field`。

尤其对 `RadFrac` 要注意：

- `Design Spec` 的块变量名，很多时候是 **Aspen 内部产品槽位名**，不是 flowsheet 流股名。
- 例如 flowsheet 上看到的是 `V1`，但 `helper-managed manipulated-variable field` 里真正对应的可能是 `MOLE-L1`、`MOLE-VN`、`MOLE-D` 之类内部 token。
- 如果 block 输入树里真正落地的是 `Data\Blocks\<BLK>\Input\PROD_FLOW\<stream>`，就不能想当然把 `V1` 当成 `helper-managed manipulated-variable field` 语义本体；要先确认 Aspen 对外暴露的那个 **原生块变量 token** 是什么。

推荐的核验动作：

- 读 helper readback、`probe_model_state` 或 block 专用 collector，确认对应 block 输入已落地，且不是 `null` / 未指定。
- 如果有专用语义 capability（如 `set_prod_flow`、`set_radfrac_distillate_rate`），先单独调用并读回。
- 再看 `Design Spec` 的 `helper-managed manipulated-variable field` 动态下拉里，是否存在与该已指定输入一一对应的原生 token。
- 若 `helper-managed manipulated-variable field` 需要 `helper-managed manipulated-variable field`，优先按 `HAP_PROMPT` 或已知块类型经验填写；不要直接把 flowsheet 流股名当作当然正确的 `ID1`。

如果以上任一步不能自证，请先停在“变量落地验证”，不要急着继续调 `LOWER/UPPER`、`ASKED` 或外层 sweep。否则很容易把“变量没指定”误判成“Design Spec 没激活”。

### 3. 原生分析工具应视为正式求解能力

当任务语义与扫描、反求或优化匹配时，hardcoded script 应把 Aspen 原生分析工具接入任务主流程，并保留配置、参与和结果证据。

这条经验的意义不在于“每道题都必须同时使用三种工具”，而在于：

- `Sensitivity Analysis` / `Design Spec` / `Optimization` 已经不应再被视为遥远或特殊能力
- 它们应当成为后续 hardcoded script 的默认武器库
- 当题目目标与扫描、反求、优化天然匹配时，应优先尝试把这三类工具纳入正式求解路径
- 即使最终只使用其中一种，也应先做过工具层面的思考，而不是默认退回手写 sweep 或人工调参

建议采用以下默认心智：

- 不是“这题能不能不用分析工具先硬写出来”
- 而是“这题最适合由哪一个 Aspen 原生分析工具来完成”

### 4. 组合使用三类工具是被鼓励的

后续脚本如果题意合适，明确鼓励组合使用：

1. 先用 `Sensitivity Analysis` 找到变量影响方向、敏感区间或候选操作区间
2. 再用 `Design Spec` 反推满足目标约束的设定值
3. 最后用 `Optimization` 在可行域内寻找更优操作点

并且要把这种组合视为“更成熟的正式脚本设计”，而不是“过度复杂化”。只要它更贴近题意、更容易复核、更有证据链，就优于外部手写控制。

### 5. 什么时候可以手写 sweep

只有在以下情况才允许手写 sweep：

- 当前 MCP / HTTP 能力暂时无法完整配置 Aspen 原生分析工具
- 原生分析工具配置后无法稳定读回目标结果
- 题目只是要求画趋势图，且手写 sweep 更稳定、更透明

如果用了手写 sweep，必须在代码注释和 `summary.json` 里写明：

- 为什么没有使用 `Sensitivity Analysis` / `Design Spec` / `Optimization`
- 手写 sweep 的变量、范围、步数、重置策略
- 与 Aspen 原生分析工具相比的局限

## Headless 运行规范

### 1. 默认目标是无 GUI 运行

正式 hardcoded script 的默认运行目标应是“不显示 Aspen GUI”。这样更适合批处理、回归验证和后台执行。

### 2. 当前机制

当前服务端 `session/start` 已支持 `show_gui` 参数，不需要额外发明新的服务端 CLI 参数。

已确认的行为：

- `show_gui=true`：显示 Aspen GUI
- `show_gui=false`：以隐藏主窗口方式运行 session
- 若脚本未显式传值，则由服务端默认策略决定

公共底座 `AspenHttpClient.ensure_session()` 现已支持：

- 显式向服务端传递 `show_gui=false`
- 通过环境变量 `ASPEN_HARDCODED_SHOW_GUI=0/1` 统一覆盖 hardcoded 脚本的 session 可见性

### 3. 何时允许打开 GUI

以下场景允许显式打开 GUI：

- 需要调用 `ui_check_next_completion_status`
- 某些 `Sensitivity Analysis / Design Spec / Optimization` 步骤当前仍依赖 GUI 辅助收尾
- 需要人工观察 Aspen 弹窗、定位 completion 页面或诊断 UI 相关问题

建议脚本统一提供：

` ` `text
--show-gui
` ` `

并按如下思路调用：

` ` `python
client.ensure_session(show_gui=bool(args.show_gui) or None)
` ` `

如果某题确认必须 headless 才是正式交付口径，则应改为显式传 `False`，并只在调试模式下开放 GUI。

## 迁移步骤建议

每道题建议按以下顺序处理：

1. 读取题面、题图、表格，明确任务目标。
2. 搜索现有资产，确定“从哪个脚本改起”。
3. 先跑基线，抓首个真实阻塞点。
4. 优先修公共能力问题，再修题脚本。
5. 修正 Aspen-safe 命名、单位、拓扑和关键规格。
6. 跑通建模与求解。
7. 补齐 `completion`、`PER_ERROR`、`REP/APW/BKP`。
8. 若题目要求分析，优先接入 `Sensitivity Analysis` / `Design Spec` / `Optimization`。
9. 若题目目标天然对应扫描 / 反求 / 优化，优先让 Aspen 原生分析工具承担主要求解职责，而不是只做展示。
9. 更新 `summary.json`。
10. 回填 `hardcoded-script-跟踪文档.md`。

## 常见坑

- 旧脚本里的长流股名/块名不符合 Aspen 命名规则。
- 题图拓扑和旧脚本不一致，尤其是 recycle、purge、pressure-change 支路。
- 单位口径混乱：题面单位、setter 单位、全局 `INSET=SI`、REP 读数口径不一致。
- 结果读回路径选错，导致“看起来有值，但不是题目要的值”。
- 误把手写 sweep 当默认方案，绕开了 Aspen 原生分析工具。
- GUI 辅助功能与 headless 目标冲突，却没有在脚本里显式声明。

## 交付检查清单

提交前至少确认：

- 已优先检查并复用现有脚本资产
- 题图/题面与脚本拓扑一致
- 关键逻辑和关键变量有 inline comment
- 优先尝试 Aspen 原生分析工具，而不是默认手写 sweep
- 已明确评估 `Sensitivity Analysis` / `Design Spec` / `Optimization` 是否能更直接达成题目目标
- 输出目录符合规范
- `REP/APW/BKP` 已落盘
- `completion` 已记录
- `PER_ERROR` 已记录
- 最终关键结果已写入 `summary.json`
- 跟踪文档已回填

## 结论

正式 hardcoded script 的核心不是“会调 Aspen”，而是把“已有资产复用、题意对齐、工具优先级、证据留存、可批处理运行”统一到一套稳定方法里。后续新题一律按本指南收敛，避免再次出现从零散脚本重新摸索的情况。

` ` `

### FILE: docs/hardcoded_script_plan/script_agent_http_api_contract.md
Reason: core hardcoded script/runtime contract
` ` `text
# Script Agent Aspen HTTP API Contract

This file is compact context for the local script-authoring agent. It is not a
task solution. It lists stable operation names and parameter shapes that
generated hardcoded scripts should use through `AspenHttpClient.invoke(...)`.
The name of this document describes the native transport, not a requirement for
generated code to choose between HTTP and local Python helpers.

## Default Unified Invocation Contract

`client.invoke("capability", **params)` is the default for registered capabilities
and returns a `status`/`result` envelope. Registered local helpers and native HTTP
operations share one registry; generated code need not classify them by transport.
`safe.call(client, "capability", **params)` strictly checks the routed outcome and
unwraps its result payload. `safe.probe_call(client, "capability", **params)` uses
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

` ` `python
import script_agent_exp.safe_aspen_calls as safe
` ` `

Or use the existing typed imports:

` ` `python
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
` ` `

Use the helpers when possible. They enforce the exact parameter names below and
raise useful diagnostics when Aspen or HTTP rejects a call. Prefer block-family
helpers (`configure_heatx_shortcut_target`, `configure_heatx_detailed_shell_tube_rating`,
`configure_radfrac_total_condenser`, ...) over ad hoc sequences of raw `set_*`
calls when a helper covers the task.

**Important:** `create_block` is a local typed Python helper, not a registered
HTTP capability. Generated slim source must never call `client.invoke("create_block", ...)`;
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

` ` `text
--section-out-dir <path>
--bkp-subdir <server-relative-subdir>
--task-key <stable-task-key>
--server-url <url>       # optional
--port <int>             # optional
--show-gui              # optional flag
` ` `

Every generated script must accept all of them. Write `summary.json` at:

` ` `python
Path(args.section_out_dir) / SCRIPT_STEM / "summary.json"
` ` `

Use `args.bkp_subdir` for evidence exports when present, and use
`args.task_key` for the Aspen HTTP task hash/name seed when present.

## Staged Script Shape

The harness currently runs one generated Python script per case. To make complex
work easier, write that script as small stages instead of one large `main` body:

` ` `python
def setup_components(client): ...
def build_topology(client): ...
def set_specs(client): ...
def run_and_export(client, args): ...
` ` `

Record stage diagnostics in `summary.json` under a top-level `stages` key. Rerun
the deterministic script from scratch on every repair iteration. Do not depend
on BKP/checkpoint handoff as normal state transfer; it is cheap to rebuild from
the script.

## Probe As You Build

Generated scripts should not be open-loop. After each major stage, probe Aspen
state and log it into `summary.json`:

` ` `python
topology_probe = probe_model_state(
    client,
    stream_names=["F1", "P1"],
    block_names=["M1", "R1"],
    include_flowsheet=True,
    include_ui_next=False,
)
` ` `

Use focused probes when repairing:

` ` `python
check_stream_completion(client, "F1")
check_block_completion(client, "R1")
check_flowsheet_completion(client)
` ` `

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

` ` `python
ready_probe = probe_model_state(
    client,
    stream_names=["F1"],
    block_names=["C1"],
    include_flowsheet=True,
)
assert_completion_ready(ready_probe, require_streams=["F1"], require_blocks=["C1"])
` ` `

If a feed stream says `input_incomplete`, call `ui_next_completion(...)` once and
fix the missing stream state before running. A common error is setting
`mixed_spec="TP"` while only setting pressure and vapor fraction; Aspen then
reports `SUBSTREAM not complete: SSID = MIXED` and `Two of Temperature,
Pressure, and Vapor Fraction must be specified`.

## Aspen-Safe Names

This project server enforces short Aspen object names:

` ` `text
^[A-Za-z][A-Za-z0-9:-]{0,15}$
` ` `

Use names such as `F1`, `P2`, `V1`, `L1`, `H1`, `R1`, `D1`, `S1`, `C-1`,
`FL`, or `HX`. Do not use long semantic stream names like `FEED`, `PROD`,
`VAPOR`, `LIQUID`, `PRODUCT`, `PUMPED`, or names with underscores/spaces.
Explain the mapping in `summary.json`, for example `F1 = feed`, `P2 = product`.

## Canonical Operations

Component setup:

` ` `python
client.invoke(
    "add_components_by_cas",
    components=[
        {"component_id": "ETOH", "cas": "64-17-5"},
        {"component_id": "H2O", "cas": "7732-18-5"},
    ],
)
client.invoke("list_component_ids")
` ` `

Recycle Calculator and convergence operations:

` ` `python
client.invoke("create_calculator", calculator_name="C-1")

client.invoke(
    "calculator_define_stream_component_flow",
    calculator_name="C-1",
    variable_name="A",
    stream_name="M1",
    component="COMP-01",
    unit="kmol/hr",
    substream="MIXED",
    vartype="MOLE-FLOW",
)

client.invoke(
    "calculator_set_fortran_exec",
    calculator_name="C-1",
    statements="A = 120 - B",
    method="FORTRAN",
)

client.invoke(
    "calculator_set_execute_before_block",
    calculator_name="C-1",
    block_name="MX",
    block_type="BLOCK",
)

client.invoke(
    "set_convergence_options",
    tolerance=1e-4,
    tear_method="WEGSTEIN",
)

client.invoke(
    "set_wegstein_options",
    max_iterations=100,      # WEG_MAXIT
    wait=1,                  # WEG_WAIT
    direct_steps=0,          # ACCELERATE
    acceleration_steps=1,    # NACCELERATE
    lower_bound=-5.0,        # WEG_QMIN
    upper_bound=0.0,         # WEG_QMAX
)
client.invoke("read_recycle_convergence_setup", calculator_name="C-1")
` ` `

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

` ` `python
ensure_property_method(client, method="NRTL")
` ` `

`ensure_property_method(...)` is idempotent. If Aspen reports
`OPTION-SETS (...) already exists`, the helper still sets and reads back the
global `GBASEOPSET` / `GOPSETNAME` fields before returning success.

Block-wise property method / local option set:

` ` `python
configure_block_property_method(client, block_name="A1", method="UNIQUAC")
configure_block_property_method(client, block_name="A2", method="NRTL")
configure_block_property_method(client, block_name="A3", method="WILSON")
` ` `

This writes and reads back `\Data\Blocks\<BLOCK>\Input\OPSETNAME`. Do not call
nonexistent operations such as `set_block_property_method`.

Streams and blocks:

` ` `python
client.invoke("create_material_stream", stream_name="F1")
client.invoke("create_material_stream", stream_name="P2")
client.invoke("create_heater", block_name="H1")
client.invoke("create_flash2", block_name="FL")
client.invoke("create_pump", block_name="P1")
` ` `

Topology:

The unwrapped `list_block_ports` payload is
`{"success": true, "block_name": "H1", "ports": {"F(IN)": [], "P(OUT)": []}}`.
Direct routed client calls return that payload in a `status`/`result` envelope.
Port names are dictionary keys; an empty connected-stream list means a port
exists but is currently unwired. Normalize either form with the existing pure
`safe.extract_block_ports` helper, not a local response-shape parser.

` ` `python
block_name = "H1"
ports = safe.extract_block_ports(client.invoke("list_block_ports", block_name=block_name))
for name in ("F(IN)", "P(OUT)"):
    if name not in ports:
        raise RuntimeError(f"Required port {name} missing on {block_name}")
client.invoke("connect_stream", block_name=block_name, stream_name="F1", port_name="F(IN)")
client.invoke("connect_stream", block_name=block_name, stream_name="P2", port_name="P(OUT)")
wired = safe.extract_block_ports(client.invoke("list_block_ports", block_name=block_name))
if "F1" not in wired.get("F(IN)", []) or "P2" not in wired.get("P(OUT)", []):
    raise RuntimeError("Intended stream wiring was not confirmed by live readback")
` ` `

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

` ` `python
connect_material_inlet_outlet(client, block_name="P1", inlet_stream="F1", outlet_stream="P2")
` ` `

It calls `list_block_ports` and uses live material ports such as `F(IN)` and
`P(OUT)`.

For multi-feed/multi-product material blocks, never invent ports such as `IN1`,
`F2(IN)`, or heat ports such as `HS(IN)`. Prefer:

` ` `python
connect_material_ports_by_order(
    client,
    block_name="M1",
    inlet_streams=["F1", "F2"],
    outlet_streams=["S1"],
)
` ` `

It calls `list_block_ports`, filters out heat/work ports, connects by live
material-port order, and returns the port evidence for `summary.json`.

Material stream state and composition:

` ` `python
client.invoke("set_mixed_spec_mixed", stream_name="F1", value="TP")
client.invoke("set_basis_mixed", stream_name="F1", value="MOLE-FLOW")
client.invoke("set_temp_mixed", stream_name="F1", value=25.0, unit="C")
client.invoke("set_pres_mixed", stream_name="F1", value=1.0, unit="atm")
client.invoke("set_flow_mixed", stream_name="F1", component_name="ETOH", value=50.0, unit="kmol/hr")
` ` `

Use `component_name` and `value` for `set_flow_mixed`. Do not use
`component_id`, `flow_rate`, or total-only flow when component flow/fraction is
required.

The selected `mixed_spec` must match exactly two state variables:

` ` `python
# Normal T/P feed:
set_material_stream(..., mixed_spec="TP", temperature=25.0, temperature_unit="C", pressure=1.0, pressure_unit="atm")

# Saturated liquid/vapor at pressure:
set_material_stream(..., mixed_spec="PV", pressure=1.0, pressure_unit="atm", vapor_fraction=0.0)
` ` `

Do not use `mixed_spec="TP"` with only pressure + vapor fraction. That leaves
temperature unset and makes the stream incomplete.

Component-specific probe readback:

` ` `python
purity = call(
    client,
    "read_stream_output",
    stream_name="P2",
    variable="mole_fraction",
    component_name="ETOH",
)
` ` `

`read_stream_output` is a registered local helper, not an HTTP wire route. A
state snapshot with no explicit component fraction cannot supply purity evidence.
Preserve units/basis and trusted-run evidence; final scored metrics still use the
final REP readback contract.

Common block specs:

` ` `python
# HEATER / FLASH2
client.invoke("set_spec_opt", block_name="H1", value="TP")
client.invoke("set_temp", block_name="H1", value=80.0, unit="C")
client.invoke("set_pres", block_name="H1", value=1.0, unit="atm")
client.invoke("set_duty", block_name="H1", value=0.0, unit="kW")

# PUMP
client.invoke("set_opt_spec", block_name="P1", value="DELP")
client.invoke("set_delp", block_name="P1", value=2.0, unit="bar")
client.invoke("set_pres", block_name="P1", value=5.0, unit="bar")
` ` `

For `FLASH2`, legal `set_spec_opt` values include `TP`, `TV`, `PV`, `TD`, and
`PD`. If `TP` is selected, set both `set_temp` and `set_pres`.

Completion and run:

` ` `python
completion = client.invoke("ui_check_next_completion_status", close_window=True, status_timeout_s=8.0)
final = run_completion_engine_and_export(
    client,
    server_subdir=args.bkp_subdir,
    script_stem=SCRIPT_STEM,
    task_key=args.task_key,
    export_bkp=False,
)
per_error = final.get("per_error")
run = final.get("engine_run")
` ` `

Before `engine_run`, call `ui_check_next_completion_status` at least once and
store the payload in `summary.json`.

For generated scripts, prefer the final-stage helper:

` ` `python
final = run_completion_engine_and_export(
    client,
    server_subdir=args.bkp_subdir,
    script_stem=SCRIPT_STEM,
    task_key=args.task_key,
    export_bkp=False,
)
` ` `

It returns `completion`, `engine_run`, `per_error`, and REP/APW `evidence`.

Common RStoic helpers:

` ` `python
configure_rstoic_stoichiometry(
    client,
    block_name="R1",
    reaction_number=1,
    reactants={"BENZ": 1.0, "H2": 3.0},
    products={"CH": 1.0},
)
configure_rstoic_fractional_conversions(
    client,
    block_name="R1",
    conversions=[{"reaction_number": 1, "component_id": "BENZ", "conversion": 0.75}],
)
configure_rstoic_calculated_heat_reference(
    client,
    block_name="R1",
    rows=[
        {
            "reaction_number": 1,
            "reference_component_id": "BENZ",
            "reference_phase": "V",
        },
    ],
    reference_temperature=298.15,
    reference_temperature_unit="K",
    reference_pressure=1.0,
    reference_pressure_unit="atm",
)
configure_rstoic_flash(
    client,
    block_name="R1",
    spec_opt="TP",
    temperature=200.0,
    temperature_unit="C",
    pressure=20.0,
    pressure_unit="bar",
)
` ` `

Pass positive magnitudes to `reactants`; the helper sends negative Aspen
stoichiometric coefficients for reactants and positive coefficients for
products.

Common REquil helper:

` ` `python
configure_requil_equilibrium_reactions(
    client,
    block_name="R1",
    nphase=2,
    spec_opt="TP",
    temperature=450.0,
    temperature_unit="F",
    pressure=1.0,
    pressure_unit="atm",
    reactions=[
        {
            "reaction_number": 1,
            "reactants": {"MEOH": 1.0},
            "products": {"CO": 1.0, "H2": 2.0},
            "delta": 0.0,
        },
        {
            "reaction_number": 2,
            "reactants": {"CO": 1.0, "H2O": 1.0},
            "products": {"CO2": 1.0, "H2": 1.0},
            "delta": 0.0,
        },
    ],
)
` ` `

For REquil, never set only `set_opt_ext_delt` / `set_delt`. The reaction
stoichiometry table must be written with `set_block_reaction_stoichiometry`
first, otherwise the block stays input-incomplete and will block the flowsheet.
Prefer `SPEC_OPT="TP"` when the task states reactor temperature and pressure.
Using `PD` with arbitrary zero duty can pass input completion but fail at runtime
with `UNABLE TO FIND OUTLET TEMPERATURE`.
After REquil reaction setup, probe `check_block_completion(client, "R1")` and do
not bypass an incomplete REquil by exporting only a separate RGibbs block.

Evidence export:

` ` `python
client.invoke("export_rep", filename="output/subdir/run.rep", export_format=2)
client.invoke("export_apw", filename="output/subdir/run.apw")
# Optional debug evidence only; not required for script-agent success:
# client.checkpoint(filename="output/subdir/run.bkp")
` ` `

`summary.json` should include a top-level `evidence` dict with non-empty
`rep_path` and `apw_path` after successful export. `bkp_path` may be null.

` ` `

### FILE: docs/hardcoded_script_plan/evidence_finalization_tools.md
Reason: core hardcoded script/runtime contract
` ` `text
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

` ` `python
from script_agent_exp.safe_aspen_calls import run_completion_engine_and_export

final = run_completion_engine_and_export(
    client,
    server_subdir=f"script_agent_experiment/{SCRIPT_STEM}/{case_key}",
    script_stem=f"{SCRIPT_STEM}_{case_key}",
    task_key=f"{task_key}_{case_key}",
    required_streams=["F1"],
    required_blocks=["H1", "PF", "H2", "AD", "H3", "V1", "V2"],
)
` ` `

Record the returned object directly in the case summary:

- `case["engine_run"] = final["engine_run"]`
- `case["per_error"] = final["per_error"]`
- `case["run_status"] = final["run_status"]`
- `case["evidence"] = final["evidence"]`
- `case["completion"] = final["completion"]`

Then derive gates from the returned fields:

- `PER_ERROR=0`: `final["per_error"]["value"] == 0`
- REP exists: `final["evidence"]["rep_path"]`
- APW exists: `final["evidence"]["apw_path"]`
- REP convergence: parse `final["evidence"]["rep_path"]` with `rep_parser.parse_problem_status`.

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

` ` `json
{
  "cases": [
    {
      "case_key": "araby",
      "crude": "Araby",
      "engine_run": {},
      "per_error": {"value": 0},
      "run_status": {},
      "evidence": {
        "rep_path": "...",
        "apw_path": "..."
      },
      "rep_converged": true,
      "product_streams_m3_d": {},
      "column_readbacks": {}
    }
  ],
  "evidence_gate": {
    "all_cases_have_rep_apw": true,
    "all_cases_per_error_zero": true,
    "all_cases_rep_converged": true
  }
}
` ` `

The top-level `summary["evidence"]` may point to the final case or contain
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

` ` `

### FILE: docs/hardcoded_script_plan/rep_parser_helper_contract.md
Reason: core hardcoded script/runtime contract
` ` `text
# REP Parser Helper Contract

Generated scripts should not copy or reimplement REP parsers. Import the stable
helpers from `script_agent_exp.safe_aspen_calls`, which re-exports the parser
implementation from `healthcheck.full_example.rep_parser`.

` ` `python
from script_agent_exp.safe_aspen_calls import (
    build_agent_visible_rep_text,
    load_rep,
    parse_block_heat_duty_watt,
    parse_block_theoretical_stages,
    parse_problem_status,
    parse_radfrac_liquid_x_profile,
    parse_stream_section,
)
` ` `

## Core Calls

### `load_rep(path: str) -> str`

Read a textual Aspen `.rep` file. Use this for the `evidence.rep_path` produced
by `run_completion_engine_and_export(...)` or `finalize_task_summary(...)`.

### `parse_problem_status(rep_text: str) -> dict`

Return a convergence summary:

` ` `python
status = parse_problem_status(rep_text)
converged = bool(status.get("converged"))
hints = status.get("hints") or []
` ` `

Use this to support final `rep_converged` / problem-status evidence.

### `parse_stream_section(rep_text: str) -> dict[str, RepStreamRow]`

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

` ` `python
rep_text = load_rep(final["evidence"]["rep_path"])
streams = parse_stream_section(rep_text)
outlet = streams.get("P1")
water_kmol_s = (outlet.components_kmol_s or {}).get("WATER") if outlet else None
` ` `

## Task-Specific Helpers

### `parse_block_heat_duty_watt(rep_text: str) -> dict[str, float | None]`

Best-effort block heat-duty extraction from the U-O-S block section. Use for
HeatX, Heater, condenser/reboiler, and similar duty readbacks when direct Aspen
tree readbacks are unavailable or need REP corroboration.

### `parse_block_theoretical_stages(rep_text: str, *, block_name: str) -> float | None`

Best-effort stage/tray count extraction for shortcut or column blocks. Use for
DSTWU/RadFrac comparison evidence when the task asks for theoretical stages.

### `parse_radfrac_liquid_x_profile(rep_text: str, *, block_name: str, component_ids: list[str]) -> dict`

Best-effort RadFrac liquid mole-fraction profile extraction. Use when the task
asks for composition profiles or stagewise liquid composition evidence.

### `build_agent_visible_rep_text(rep_text: str, *, max_chars: int = 18000) -> str`

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

` ` `

### FILE: docs/hardcoded_script_plan/safe_aspen_calls_core_helpers.md
Reason: descriptor-selected safe Aspen helper catalog
` ` `text
# Safe Aspen Calls Core Helper Catalog

This catalog is always safe to include in own-agent init prompts. It contains
generic helper contracts used by most generated scripts. Specialized RadFrac,
analysis, probe, and heat-cascade helpers live in separate complete catalogs.

## Unified Capability Invocation

Default to `client.invoke("capability", **params)` for registered capabilities.
It returns a `status`/`result` envelope. Local Python helpers and native HTTP
operations use the same capability registry; generated code need not decide
which transport implements a registered capability.

Use `safe.call(client, "capability", **params)` for strict execution: it checks
the routed outcome and unwraps the result payload. Use
`safe.probe_call(client, "capability", **params)` for diagnostics through the
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

Call `client.ensure_session(...)` before model mutation. Use `inset="SI"` or
another legal built-in unit set through `ensure_session`; do not write INSET
through raw tree access.

## Components And Properties

Use CAS-based component landing helpers when real chemicals are known. After
adding components, verify the visible component table before writing stream
composition, reactions, or downstream specs.

Use documented property-method helpers. Do not invent raw tree writes for global
or block-local property methods.

After `ensure_property_method(..., method="SRK")`, call registered
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

` ` `python
purity = client.invoke(
    "read_stream_output",
    stream_name="P1",
    variable="mole_fraction",
    component_name="ETOH",
)
` ` `

A default stream-state snapshot (temperature, pressure, vapor fraction, total
flow) is not component-purity evidence. Preserve the readback unit/basis and
trusted-run provenance; final scored evidence still follows the final REP
readback contract below.

## Run And Export

For final evidence, prefer:

` ` `python
final = client.invoke("run_completion_engine_and_export",
    required_streams=REQUIRED_STREAMS,
    required_blocks=REQUIRED_BLOCKS,
    server_subdir=args.bkp_subdir,
    script_stem=SCRIPT_STEM,
    task_key=args.task_key,
    export_bkp=False,
)
` ` `

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

` ` `

### FILE: docs/hardcoded_script_plan/safe_aspen_calls_analysis_helpers.md
Reason: descriptor-selected safe Aspen helper catalog
` ` `text
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

` ` `python
suite = client.invoke("configure_sensitivity_exploration_suite",  suite_name=suite_name, sweeps=sweeps, summary=summary,
    collect=True, decision_basis=decision_basis,
)
# The suite owns collection and records per-Sensitivity evidence in summary.
# Inspect configuration_status separately if whole-request success is false.
` ` `

Use stream-variable sweeps for material stream feed, solvent, makeup, or utility
flow handles. Use block-variable sweeps only when the manipulated surface is
actually block-owned.

The suite returns `schema_version="sensitivity_configuration_transaction.v1"`.
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

` ` `

### FILE: docs/hardcoded_script_plan/safe_aspen_calls_radfrac_helpers.md
Reason: descriptor-selected safe Aspen helper catalog
` ` `text
# Safe Aspen Calls RadFrac Helper Catalog

Use this complete catalog when the task profile explicitly includes `RADFRAC`.

## Standard Column Setup

For ordinary total-condenser/kettle columns, prefer:

` ` `python
client.invoke("configure_radfrac_total_condenser",
    block_name="D1",
    feed_stream="F1",
    nstage=20,
    feed_stage=10,
    reflux_ratio=1.5,
    distillate_flow=1.0,
    distillate_flow_unit="kmol/hr",
    top_pressure=1.0,
    pressure_unit="atm",
)
` ` `

Use the declared keyword names `nstage`, `distillate_flow`, and `top_pressure`;
`feed_stream` is required. The flow unit belongs in `distillate_flow_unit`, and
column pressure uses `pressure_unit`. These illustrative values are not task
answers. Do not invent aliases or raw tree paths when a helper owns the setup.
The runtime parent supplies canonical imports; do not generate a `sys.path`
bootstrap or use legacy experiments-package fallbacks.

If a task, reference BKP, or live readback shows explicit `PRES1` / `PRES2`
pressure rows, use `bottom_pressure_mode="pres2"` with
`configure_radfrac_total_condenser(...)`, or call `client.execute("set_pres2",
...)` directly after `set_pres1`. The default helper behavior keeps historical
`DP-COL` semantics for `bottom_pressure`; it is not a substitute for probing
`PRES2` when the Aspen file's pressure surface is TOP-BOTTOM / P-SPEC2.

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

` ` `python
client.invoke("configure_radfrac_feed_convention",
    block_name="D1",
    stream_name="F1",
    convention="ON-STAGE",
)
` ` `

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

` ` `

### FILE: docs/hardcoded_script_plan/safe_aspen_calls_heat_cascade_helpers.md
Reason: descriptor-selected safe Aspen helper catalog
` ` `text
# Safe Aspen Calls Heat-Cascade Helper Catalog

Use this complete catalog when explicit task-profile families or descriptors
select heat-stream, HeatX, MHeatX, Flash2 evaporator, or multi-effect heat-duty
work.

## Heat Stream Duty

Heat streams created by `create_heat_stream` live under `Data\Streams\<Q>` with
heat-stream semantics. Use helper calls for duty writes:

` ` `python
client.invoke("configure_heat_stream_duty",
    stream_name="Q1",
    duty=1.5e7,
    unit="Watt",
)
` ` `

For cascades:

` ` `python
client.invoke("configure_heat_stream_duty_map",
    duties_by_stream={"Q1": 2.0e7, "Q2": 1.5e7},
    unit="Watt",
)
` ` `

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

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/streams_globals.md
Reason: generic stream/global Aspen surface
` ` `text
# Block-Type 注入：Streams & Globals（流股 / 全局 / 引擎）

- **块类型**：跨块（非单元块）
- **Aspen 语义**：物料流、全局物性、引擎运行与 completion 检查。热流股详见 `docs/hardcoded_script_plan/block_type_inject/heat_stream.md`。

---

## 0. Helper

| Helper | 何时用 |
|--------|--------|
| `configure_block_property_method(...)` | 块级物性方法（block-wise property） |
| `ensure_property_method(...)` / `read_global_property_method(...)` | 全局物性包 ensure + readback |
| `configure_inset_unit_system(...)` | 全局单位制 INSET（**唯一正确路径**；**Python-only**，勿 `client.execute(...)`） |
| 物料流 helper | `set_mixed_spec_mixed` + `set_basis_mixed` + 组成/TP 等（见 material stream MCP） |

**`configure_inset_unit_system` 示例**：

` ` `python
# 方式 A：session 启动后由 ensure_session 自动设置（推荐）
client.ensure_session(show_gui=False, inset="SI")   # 或 inset="ENG"

# 方式 B：显式 helper
client.invoke("configure_inset_unit_system",  value="SI")
# path: Data\Setup\Global\Input\INSET
# 合法值：SI | ENG | ENGUS | MET | SI-CHEM | MET-CHEM
# 错误路径 Data\Setup\System-Options\Input\INSET 不存在，勿用
` ` `

---

## 1. 写入顺序门控（CRITICAL）

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| `set_property_method` / 组分 | 流股组成 | 全局物性包 + 组分表 |
| 物料流 TP/组成 | 块 Input | 进料流 completion 后再连块 |
| `check_next_completion_status` | `engine_run` | 至少一次 workflow 级检查 |

---

## 2. Core MCP / HTTP Operations

### 2.1 组分与物性

| MCP operation | 参数 | 说明 |
|---------------|------|------|
| `add_components_by_cas` | `components: [{cas, component_id}]` | **优选** 组分添加（各 benchmark 入口） |
| `set_property_method` | `method: str` | 全局物性方法 |

### 2.2 物料流

| MCP operation | Aspen 变量 | 允许值 / 参数 | 说明 |
|---------------|------------|---------------|------|
| `create_material_stream` | — | `stream_name` | 建物料流 |
| `set_mixed_spec_mixed` | 混合规格 | `TP`/`TV`/`PV`/… | 须先于 T/P/组成 |
| `set_basis_mixed` | 基准 | `MOLE-FLOW`/`MASS-FLOW`/… | 流量基准 |
| `set_temp_mixed` | TEMP | float + unit | 温度 |
| `set_pres_mixed` | PRES | float + unit | 压力 |
| `set_flow_mixed` | 组分流量 | component + value + unit | 组成/流量 |
| `set_vfrac_mixed` | VFRAC | float | 汽相分率（TV/PV 等） |

### 2.3 热流股

热流股已拆分到独立注入文档：`docs/hardcoded_script_plan/block_type_inject/heat_stream.md`。当任务需要 heat stream / heat duty / utility heat topology / 热级联时必须加载该文档。

### 2.4 全局与引擎

| MCP operation | 说明 |
|---------------|------|
| `set_property_method` | 全局物性方法（亦见 §2.1） |
| `engine_reinit` / `engine_run` | 重算 / 运行 |
| `ui_check_next_completion_status` | Next/completion 工作流 |
| `export_rep` / `export_bkp` | 证据导出 |
| `table_dump` / `table_insert_label` | 组分/计量表 |

---

## 3. 拓扑与其它 MCP

见各单元块 inject；所有块共用 `list_block_ports`、`connect_stream`。

---

## 4. 结果读回

| 目标 | 方式 |
|------|------|
| 流股 T/P/流量/组成 | `Data\Streams\<S>\Output\...` 或 REP |
| 全局物性 | `ensure_property_method` / `read_global_property_method` readback payload |
| INSET | `safe.configure_inset_unit_system(client, value=...)` readback；或 `client.ensure_session(..., inset="SI")` |


---

## 9. 汇总

| 项 | 内容 |
|----|------|
| 用途 | 与单元块 inject 分桶；勿把 stream setter 算进块 core |

` ` `

### FILE: docs/hardcoded_script_plan/aspen_component_id_hints.md
Reason: generic stream/global Aspen surface
` ` `text
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
  abbreviations from task text (`Water` -> `H2O`, not `WA`; `Methanol` -> `MEOH`,
  not `ME`).
- Prefer task-visible component names and CAS lookup helpers over guessing.
- If the generated script uses local short IDs such as `BZ` or `TOL`, record the
  mapping in `summary.json`.
- Do not silently substitute a different component just to satisfy completion.
- If a task needs pseudo-components or missing metadata repair, record the
  formula/molecular-weight assumption and prove the final Aspen evidence still
  matches the task intent.

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/property_methods.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：Property Methods（物性方法）

- **块类型**：`PROPERTY_METHODS`（跨块能力）
- **Aspen 语义**：全局或块级热力学/物性方法选择与对比。

---

## 0. Helper

| Helper | 何时用 |
|--------|--------|
| `ensure_property_method(...)` | 全局物性 ensure + readback |
| `read_global_property_method(...)` | 只读全局 GBASEOPSET/GOPSETNAME |
| `configure_block_property_method(...)` | 指定块使用 UNIQUAC/NRTL/WILSON 等与全局不同方法；**Python-only**，勿 `client.execute(...)` |

---

## 1. 写入顺序门控（CRITICAL）

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| 全局 `set_property_method` | 首次 run | 默认物性包 |
| 组分添加 | 流股/反应 | cas-lookup → add_components |
| 块级 OPSETNAME | 该块 Input | block-wise 对比任务 |

---

## 2. Core MCP / HTTP Operations

| MCP operation | Aspen 变量 | 允许值 / 参数 | 说明 |
|---------------|------------|---------------|------|
| `set_property_method` | 全局方法 | NRTL/UNIQUAC/WILSON/… | Setup 级物性 |
| `set_opsetname` | `OPSETNAME` | 方法名 | 块级 Property Specification |

块级 ensure/readback 优先 `safe.configure_block_property_method(client, block_name=..., method=...)`，见 §0。

---

## 3. 拓扑与其它 MCP

物性方法不改变端口拓扑；对比任务须 **distinct configured cases** + 可信 REP。

---

## 4. 结果读回

| 目标 | 方式 |
|------|------|
| 方法落地 | block/global readback |
| 对比证据 | 分 case REP，禁止混用同一 bkp 冒充两方法 |


---

## 9. 汇总

| 项 | 内容 |
|----|------|
| 推荐 helper | `configure_block_property_method` |
| 相关 skill | block-wise-property-methods |

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/heater.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：HEATER（加热器/冷却器）

- **块类型**：`HEATER`
- **Aspen 语义**：单股物料加热/冷却；出口 TP / PV 等规格。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper

无专用 helper；使用 §2 MCP operation。

---

## 1. 写入顺序门控

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| `set_heater_flash_spec` | `TEMP` / `PRES` / `VFRAC` | 先模式后数值 |
| 拓扑 | Input | 进/出口连接后再写规格 |

---

## 2. Core MCP / HTTP Operations

| MCP operation | 变量 | 允许值 / 参数 | 说明 |
|---------------|------|---------------|------|
| `set_heater_flash_spec` | `SPEC_OPT` | 见 §2.1 | 出口规格模式 gate |
| `set_heater_temperature` | `TEMP` | float + unit | 出口温度 |
| `set_heater_pressure` | `PRES` | float + unit | 出口压力（>0 绝压；≤0 压降） |
| `set_heater_vapor_fraction` | `VFRAC` | float | **`SPEC_OPT=PV`** 时汽相分率 |
| `set_heater_duty` | `DUTY` | float + unit | `TQ`/`PQ`/`TD`/`PD` 等 duty/heat 类模式 |

### 2.1 `SPEC_OPT` / Operating Specification

**必须先 `set_heater_flash_spec`，再写与模式匹配的变量**；selector 与后续 setter 必须成对。

| `SPEC_OPT` | 配对规格（语义） | 典型后续变量 |
|------------|-----------------|-------------|
| `TP` | Temperature + pressure | `TEMP` + `PRES` |
| `TV` | Temperature + vapor fraction | `TEMP` + `VFRAC` |
| `TD` | Temperature + heat duty | `TEMP` + `DUTY` |
| `TDPPARM` | Temperature + duty parameter | `TEMP` + duty-parameter 表/leaf |
| `PV` | Pressure + vapor fraction | `PRES` + `VFRAC` |
| `PD` | Pressure + heat duty | `PRES` + `DUTY` |
| `PDT` | Pressure + temperature change | `PRES` + 温变 leaf |
| `PDEGSUP` | Pressure + degrees superheat | `PRES` + 过热度 |
| `PDEGSUB` | Pressure + degrees subcooling | `PRES` + 过冷度 |
| `VDPPARM` | Vapor fraction + duty parameter | `VFRAC` + duty-parameter |
| `DDPPARM` | Duty parameter（双参数 duty 规格） | duty-parameter 相关 leaf |
| `DTV` | Temperature change + vapor fraction | 温变 + `VFRAC` |
| `DTD` | Temperature change + heat duty | 温变 + `DUTY` |
| `DTDPPARM` | Temperature change + duty parameter | 温变 + duty-parameter |
| `DEGSUPDPPARM` | Degrees superheat + duty parameter | 过热度 + duty-parameter |
| `DEGSUBDPPARM` | Degrees subcooling + duty parameter | 过冷度 + duty-parameter |
| `PQ` | Pressure + heat/duty | `PRES` + heat stream / `DUTY` |
| `TQ` | Temperature + heat/duty | `TEMP` + heat stream / `DUTY` |
| `DTQ` | Temperature change + heat/duty | 温变 + heat stream / `DUTY` |
| `DPPARMQ` | Duty parameter + heat/duty | duty-parameter + heat/duty path |

**选择规则**：

- 固定出口 T、P → `TP`；级间冷却常见。
- 冷凝 → `PV` + `set_vfrac=0` + `set_heater_pressure`。
- 题目给过热度/过冷度 → `PDEGSUP` / `PDEGSUB` 或 `DEGSUP*` / `DEGSUB*` 变体，不要混用普通 `TP`。
- 题目给 duty/热负荷 → `TD`/`PD`/`TQ`/`PQ`/`DTQ` 等 **Q 或 D 类**模式；不要选 P* 却写 `TEMP`，也不要选 T* 却写 `PRES`。
- `*PPARM` / `DPPARMQ` 仅当任务明确使用 parameterized duty 表时使用。

**级间冷却**：`set_spec_opt=TP` 或仅 `set_heater_temperature` 固定出口温度（两级压缩中间 Heater）。

**冷凝**：`set_spec_opt=PV` + `set_vfrac=0` + `set_heater_pressure`。

---

## 3. 拓扑 MCP

| 操作 | 参数 |
|------|------|
| `create_heater` | `block_name` |
| `connect_stream` | 物料 `F(IN)` / `P(OUT)`；可选 `HS(IN)`/`HS(OUT)` 连热流股 |
| `engine_run` | — |

Live `list_block_ports` 常见返回：

` ` `text
F(IN), HS(IN), P(OUT), WD(OUT), HS(OUT)
` ` `

- `HS(IN): []` / `HS(OUT): []` 表示 heat port 存在但未连接；可以按该端口名连接 heat stream。
- 如果题目只是固定 Heater 出口温度、压力、汽相分率或 block duty，用 block-owned setter（`set_heater_flash_spec` + `set_heater_temperature`/`set_heater_pressure`/`set_heater_vapor_fraction`/`set_heater_duty`）即可，不要创建孤立 Q stream。
- 如果题目要求两个单元之间存在真实能量流股，必须 `create_heat_stream` 并连接到 live `HS(IN)`/`HS(OUT)`，再用 heat stream readback 与两侧 block duty/enthalpy change 证明能量参与。
- 物料侧进/出连接只证明物料经过 Heater；如果题目要求 energy topology，还必须证明 heat stream 或 native duty path 参与同一个最终 run，不能只用 outlet temperature narrative。

---

## 5. 关联块

- 成对 Heater 通过 heat stream 表达能量交换时，须证明两侧 duty / enthalpy change 能量闭合。
- 级间冷却在 **Compr** 链中（`compr.md`）。

---

## 9. 汇总

| 项 | 内容 |
|----|------|
| Core setter | 4 |
| 推荐 helper | — |

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/rstoic.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：RSTOIC（化学计量反应器）

- **块类型**：`RSTOIC`
- **Aspen 语义**：化学计量反应 + 转化率/闪蒸操作条件。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

| Helper | 主要参数 | 作用 |
|--------|----------|------|
| `configure_rstoic_stoichiometry(...)` | `block_name`, 反应行 | 写 inline 计量 |
| `configure_rstoic_fractional_conversions(...)` | `block_name`, conversion rows | 转化率行 |
| `configure_rstoic_calculated_heat_reference(...)` | `block_name`, reaction rows, reference state | 反应热 reference-condition bundle |
| `configure_rstoic_flash(...)` | `block_name`, 合法 `SPEC_OPT` 对 | TP/TD/TV/PD/PV/DV |

---

## 1. 写入顺序门控

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| `configure_rstoic_stoichiometry(...)` | 转化率 | 计量先落地 |
| `SPEC_OPT` | 仅 TP/TD/TV/PD/PV/DV | 禁止 PQ/TQ/VQ |

---

## 2. Core MCP / HTTP Operations

| MCP operation | 变量 | 允许值 / 参数 |
|---------------|------|---------------|
| `set_rstoic_flash_spec` | `SPEC_OPT` | 见 §2.1（**仅六对合法**） |
| `set_rstoic_temperature` | `TEMP` | float + unit |
| `set_rstoic_pressure` | `PRES` | float + **unit required**. Legal tokens include **`bar`**, `bara`, `barg`, `MPa`, `kPa`, `psia`, `mmHg`, … |
| `set_rstoic_duty` | `DUTY` | float + unit（`PD`/`DV` 等） |
| `set_heatopt` | `HEATOPT` | 见 §2.2 |
| `set_heat_of_reac` | `HEAT_OF_REAC` | 见 §2.3 |
| `set_opt_ext_conv` | `OPT_EXT_CONV` | **`CONVERSION`** \| `EXTENT` |
| `set_key_cid` | `KEY_CID` | 关键反应物组分 ID（转化基准） |
| `set_conv` | `CONV` | float (0–1) |

### 2.1 `SPEC_OPT` / Flash Operating Specification

**合法仅六对**（Aspen RStoic Setup → Specifications）；**禁止** `PQ` / `TQ` / `VQ` 等 Flash2 风格 token：

| token | 含义 | 必填后续变量 |
|-------|------|-------------|
| `TP` | Temperature + pressure | `TEMP` + `PRES` |
| `TD` | Temperature + duty | `TEMP` + `DUTY` |
| `TV` | Temperature + vapor fraction | `TEMP` + `VFRAC` |
| `PD` | Pressure + duty | `PRES` + `DUTY` |
| `PV` | Pressure + vapor fraction | `PRES` + `VFRAC` |
| `DV` | Duty + vapor fraction | `DUTY` + `VFRAC` |

Pressure + duty 题（如「0.3 MPa + 0 kW duty」）用 **`PD`**，不是 `PQ`。若 COM 写入与 GUI 不一致，用 HTTP `ui_set_rstoic_flash_spec_pq`（legacy 名）驱动 GUI 到合法对如 `PD`。

**Bar-scale `PRES`（与 INSET 无关）**：`set_pres(..., unit="bar")` 合法。Meta 常见 `PRES = -0.1` 配合 **`unit="bar"`**（absolute bar 负值 = 压降）。勿把 bar 量级改写成 MPa。见 `aspen-custom-unit-set` 与 `bar_pressure_write_probe.py`。

### 2.2 `HEATOPT` / Heat Transfer Option

| token | 含义 |
|-------|------|
| `CONST-DUTY` | Constant duty |
| `CONST-TEMP` | Constant temperature |
| `LMTD` | Log mean temperature difference |
| `CONDENSING` | Condensing service |
| `EVAPORATING` | Evaporating service |
| `DYNAMIC` | Dynamic heat transfer |

### 2.3 `HEAT_OF_REAC` / Heat of Reaction

| token | 含义 |
|-------|------|
| `CALCULATE` | Aspen 计算反应热 |
| `SPECIFY` | 用户指定反应热 |
| `NO-CALC-SPEC` | 不计算/不指定 |

When calculated heat is needed, do not call low-level reference-condition
setters directly. Use `configure_rstoic_calculated_heat_reference(...)` after
stoichiometry and conversion helper calls, then verify Next/completion clears
the Heat of Reaction page.

---

## 3. 拓扑 MCP

| 操作 | 参数 |
|------|------|
| `create_rstoic` | `block_name` |
| `connect_stream` | F(IN), P(OUT) |
| `engine_run` | — |

---

## 9. 汇总

| 项 | 内容 |
|----|------|
| Core setter | §2 |
| 推荐 helper | §0 四条 |

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/flash2.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：FLASH2（两相闪蒸）

- **块类型**：`FLASH2`
- **Aspen 语义**：两相闪蒸；`SPEC_OPT` 决定 TP/TV/PV/TD/PD/TQ 等规格配对。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper

无专用 helper；使用 §2 MCP operation。

---

## 1. 写入顺序门控

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| `set_flash2_flash_spec` | T/P/Duty | 须先定模式 |
| 拓扑 | Input | F(IN), V(OUT), L(OUT)；heat stream 只接 live `HS(IN)`/`HS(OUT)` |

---

## 2. Core MCP / HTTP Operations

| MCP operation | 变量 | 允许值 / 参数 |
|---------------|------|---------------|
| `set_flash2_flash_spec` | `SPEC_OPT` | 见 §2.1 |
| `set_flash2_temperature` | `TEMP` | float + unit（`TP`/`TD`/`TQ`） |
| `set_flash2_pressure` | `PRES` | float + **unit required**. Legal tokens include **`bar`**, `bara`, `barg`, `MPa`, `kPa`, `psia`, `mmHg`, `atm`, … (`TP`/`PD`) |
| `set_flash2_duty` | `DUTY` | float + unit（`TD`/`PD`/`TQ` 等 duty/heat 类模式） |
| `set_flash2_vapor_fraction` | `VFRAC` | float（`TV`/`PV`） |
| `set_energy_bal` | `ENERGY_BAL` | `YES` \| `NO` |

### 2.1 `SPEC_OPT` option 语义

| token | 含义 | 必填后续变量 |
|-------|------|-------------|
| `TP` | Temperature + pressure | `TEMP` + `PRES` |
| `TV` | Temperature + vapor fraction | `TEMP` + `VFRAC` |
| `PV` | Pressure + vapor fraction | `PRES` + `VFRAC` |
| `TD` | Temperature + duty | `TEMP` + `DUTY` |
| `PD` | Pressure + duty | `PRES` + `DUTY` |
| `TQ` | Temperature + heat/duty | `TEMP` + connected heat stream / duty path |

**配对规则**：题面给 T+P 保持 `TP` 并写 `TEMP`+`PRES`；给 P+duty 用 `PD` 写 `PRES`+`DUTY`；**不要**把 `PRES+DUTY` 误写成 `PQ`（Flash2 无 `PQ` token）。

### 2.2 Bar-scale / near-atmospheric `PRES`

- **`unit="bar"` 可用**（与全局 INSET 无关）；`set_flash2_pressure` 的 Literal 里包含 `bar` / `bara` / `barg`。
- 常压/略低于常压闪蒸：meta 常见 **`PRES = -0.05`** 配合 **`unit="bar"`**（absolute bar 下负值 = 压降）。
- **禁止**把 bar 量级数字改写成 **`MPa`**（如 `-0.05 bar` → `2.15 MPa` 是数量级错误）。
- 写完后用 readback 核对数值；readback 的 display unit 可能是 `psia` 等，不以 display label 代替写入时的 `unit=`。

` ` `python
client.invoke("set_flash2_pressure", block_name="F", value=-0.05, unit="bar")
` ` `

多级普通闪蒸链：每级 Flash2 可写独立 `set_flash2_temperature` + `set_flash2_pressure`。选择 `SPEC_OPT` 时要区分操作条件和结果目标：题面给定的温度、压力、duty、vapor fraction 可以作为规格；产品组成、回收率、蒸发量、utility requirement 等结果目标不能只靠直接设置等价结果变量来证明。

### 2.1 Heat Stream / Duty 口径

Flash2 的 live `list_block_ports` 可返回 `HS(IN)` / `HS(OUT)`，例如：

` ` `text
F(IN), HS(IN), V(OUT), L(OUT), WD(OUT), HS(OUT)
` ` `

- `HS(IN): []` 或 `HS(OUT): []` 表示端口存在但尚未连接；不要把空数组解读为没有 heat port。
- 需要显式热流股拓扑时，先 `create_heat_stream(<heat_stream>)`，再用 `connect_stream(block_name=<flash>, stream_name=<heat_stream>, port_name="HS(IN)")` 或 live 返回的对应 heat port。连接后必须用 port readback、heat stream duty/readback、REP/APW 证明它参与了最终 run。
- 只给固定 duty / fixed heat balance 的普通 Flash2，不需要创建孤立 heat stream；用 block-owned `set_flash2_flash_spec` + `set_flash2_duty` / `set_flash2_temperature` / `set_flash2_pressure`。
- `TQ` 是 Flash2 可用的温度 + heat/duty 规格口径，适合任务给出温度并把相变程度交给 heat stream / duty path 决定的场景。配置顺序通常是连接物料/heat stream 拓扑后，`set_spec_opt(..., "TQ")` + `set_temp(...)`，再由连接的 heat stream / block duty path 在最终 run 中闭合。
- `set_flash2_vapor_fraction` 是 Flash2 的操作规格之一；只有当汽相分率本身是题目给定的操作条件时才可作为最终规格。若题目要求由 heat/duty path 产生结果，不能只用 `set_flash2_vapor_fraction` 作为结果达标证据，必须证明 heat stream 或 native duty path 参与同一个最终 run。
- 注意：这里的 `TQ` 是 **Flash2** 规格。不要把它泛化到 RStoic 等其它 block family；例如 RStoic 的合法 `SPEC_OPT` 集合不包含 `TQ`。

---

## 3. 拓扑 MCP

| 操作 | 参数 |
|------|------|
| `create_flash2` | `block_name` |
| `connect_stream` | 物料：`F(IN)`, `V(OUT)`, `L(OUT)`；热流股：live `HS(IN)`/`HS(OUT)` |
| `engine_run` | — |

---

## 9. 汇总

| 项 | 内容 |
|----|------|
| Core setter | 5 |

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/fsplit.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：FSPLIT（分流器）

- **块类型**：`FSPLIT`
- **Aspen 语义**：按分流比将一股分成多股。

---

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

| Helper | 主要参数 | 作用 |
|--------|----------|------|
| `configure_fsplit_shared_outlets(...)` | `block_name`, `inlet_stream`, `outlet_streams`, `split_fractions` | **Python-only** helper；把所有产品接到共享 `P(OUT)`，再写 `set_frac` |

`configure_fsplit_shared_outlets(...)` 不是 Aspen HTTP operation。生成脚本必须通过
`safe.configure_fsplit_shared_outlets(client, ...)` 或
`call_helper("configure_fsplit_shared_outlets", client, ...)` 调用；**禁止**
`client.execute("configure_fsplit_shared_outlets", ...)` 或
`do_op(client, "configure_fsplit_shared_outlets", ...)`.

` ` `python
client.invoke("configure_fsplit_shared_outlets",
    block_name="VF",
    inlet_stream="V2",
    outlet_streams=["V4", "V3"],
    split_fractions={"V4": 0.92},
)
` ` `

规则：

- 参数名是 **`inlet_stream`**，不是 `feed_stream`。
- 参数名是 **`outlet_streams`**（列表）和 **`split_fractions`**（dict），不是 `outlet_fractions`。
- `outlet_streams` 至少 2 股；`split_fractions` 只写 **除 1 个 closure stream 外** 的所有出口分流比。Aspen 用未写的那一股闭合。
- 底层 HTTP 操作只有 `connect_stream` + `set_frac`；不要把 helper 名字当成 HTTP op。

---

## 1. 写入顺序门控（CRITICAL）

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| 拓扑 | Input | 先 `list_block_ports` + helper 连接，再写 `set_frac` |

---

## 2. Core MCP / HTTP Operations

| MCP operation | Aspen 变量 | 允许值 / 参数 | 说明 |
|---------------|------------|---------------|------|
| `set_frac` | `FRAC` | float 0..1 | 指定 outlet stream 的分流比；closure stream 不要写 |

---

## 3. 拓扑与其它 MCP

| 操作 | 参数 | 说明 |
|------|------|------|
| `create_fsplit` | `block_name` | 创建 FSPLIT 块 |
| `create_material_stream` | `stream_name` | 按需建流股 |
| `list_block_ports` | `block_name` | 查端口名 |
| `connect_stream` | `block_name`, `stream_name`, `port_name` | 通常由 helper 完成 |
| `check_block_completion` | `block_name` | 块 completion |
| `check_next_completion_status` | — | run 前至少一次 |
| `engine_run` | — | 仿真 |

---

## 4. 结果读回

| 目标 | 方式 |
|------|------|
| 块/分析输出 | REP、helper readback payload |
| 输入验收 | 关键 Input 变量非 null |

---

## 9. 汇总

| 项 | 内容 |
|----|------|
| Core operations | `set_frac` |
| 推荐 helper | `configure_fsplit_shared_outlets(...)` via `safe_aspen_calls` |

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/radfrac.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：RADFRAC（严格精馏塔）

- **块类型**：`RADFRAC`
- **Aspen 语义**：严格 MESH 精馏 / 吸收 / 汽提；与 DSTWU 简捷块分离。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

| Helper | 主要参数 | 作用 |
|--------|----------|------|
| `configure_radfrac_total_condenser(...)` | `block_name`, `feed_stream`, `nstage`, `feed_stage`, `reflux_ratio`, `distillate_flow`, `distillate_flow_unit`, `top_pressure`, `bottom_pressure`, `pressure_unit` | 全凝器 + 釜式再沸；写 `BASIS_RR` + `BASIS_D` |
| `configure_radfrac_bottom_vapor_feed(...)` | `feed_stream`, `nstage`, `feed_stage`, `top_pressure`, `pressure_unit`, `column_dp`, `reflux_ratio`, `distillate_flow`, `d_over_f` | 塔底/末级 **气相进料**；写 `PRES1` + `FEED_CONVEN=ON-STAGE-VAP` |
| `configure_radfrac_no_condenser_absorber(...)` | `nstage`, `feed_stages: dict`, `feed_conventions: dict`, `top_pressure`, `pressure_unit`, `bottom_pressure`, `column_dp` | 无冷凝/无再沸；写 `PRES1`，可选 `PRES2` 或 `DP_COL`，并写多进料约定 |
| `configure_radfrac_no_condenser_reboiled_bottoms(...)` | `reboiler_type`, `feed_stages`, `top_pressure`, `pressure_unit`, … | 无冷凝器 + 再沸器；压力语义同 `PRES1` / `PRES2` / `DP_COL` |
| `configure_radfrac_feed_convention(...)` | `block_name`, `stream_name`, `convention` | **Python-only** helper；写 `FEED_CONVEN` + `FEED_CONVE2` 同值；**不要** `client.execute("configure_radfrac_feed_convention", ...)` |
| `configure_radfrac_extractive_distillation_pair(...)` | 双塔名 + 六股流角色 + 各级数/进料级/回流比 | 萃取精馏主塔 + 溶剂回收塔 |
| `connect_radfrac_feed_distillate_bottoms(...)` | `block_name`, `inlet_streams`, `distillate_stream`, `bottoms_stream` | 按角色连接普通 RadFrac：进料走 `F(IN)`，液相馏出优先 `LD(OUT)`，塔釜走 `B(OUT)`；返回端口读回 evidence |
| `scan_radfrac_bottoms_for_component_recovery(...)` | `column_block`, `feed_stream`, `bottoms_stream`, `component_name`, `flow_values`, `flow_unit`, `target_recovery` | 扫描 RadFrac `BASIS_B` 塔釜产品流量，用进料/塔釜组分流量读回证明回收率；只用于“调节/寻找塔釜流量以满足回收率”的任务 |
| `collect_radfrac_profile_markdown_evidence(...)` | keyword-only: `rep_text`, `block_name`, `component_ids`, `output_dir`, optional `profile_name`, `source_rep_path` | 从当前 REP 文本生成 canonical Markdown 塔板组成 profile 证据；不要把 `client` 作为位置参数传入 |

Use `inlet_streams=[feed]`, not `feed_stream=`, for `connect_radfrac_feed_distillate_bottoms`. WRONG: `feed_stream=F1`; CORRECT: `inlet_streams=[F1]`.

### 0.1 场景选择（先定塔型，再选 helper）

| 场景 | 推荐方式 | 必要输入 / 证据 |
|------|----------|-----------------|
| 常规精馏：全凝器 + 再沸器，给回流比和馏出流量 | `configure_radfrac_total_condenser(...)` | `set_condenser(TOTAL)`、`set_reboiler(KETTLE)`、`BASIS_RR`、`BASIS_D`、`PRES1` |
| 吸收塔：无冷凝器、无再沸器，气体自塔底进、溶剂自塔顶进 | `configure_radfrac_no_condenser_absorber(...)` | 必须传 `feed_stages` **和** `feed_conventions`；塔顶气相产品走 `VD(OUT)`，塔底液相产品走 `B(OUT)` |
| 无冷凝器但有再沸/热底部规格 | `configure_radfrac_no_condenser_reboiled_bottoms(...)` | 不要套用 absorber 的 `REBOILER=NONE`；记录再沸器类型、底部温度/热负荷/产品规格 |
| 填料塔高度变化 / packing-height perturbation | 优先写 packed-section/HETP/height 字段；若只能用 stage surrogate，必须显式标注 | 百分比高度变化需要 base 和 modified 两组 Aspen 证据；stage surrogate 只能作为近似模型说明 |
| 题目给 textbook base target 后要求扰动结果 | 先校准 base，再做扰动 | base outlet 应接近题面 target；若未校准，只能报告为收敛 surrogate 或诊断结果 |

**吸收塔硬约束**：

- `configure_radfrac_no_condenser_absorber(...)` 的签名中 `feed_conventions` 是必填，不是可选。遗漏时会停在 Bottom Stage / Reboiler=None 的 Next gate。
- 气体进末级时，`feed_conventions[gas_stream]` 用 `ON-STAGE-VAP`；液体进塔顶时，`feed_conventions[solvent_stream]` 用 `ON-STAGE-LIQ`。helper 会同时写 `FEED_CONVEN` 和 `FEED_CONVE2`。
- `REBOILER=NONE` 时，Bottom Stage 必须有合规进料：末级 `ON-STAGE-VAP`，或 Aspen 允许的 `NSTAGE+1` above-stage vapor/liquid 约定。不要只写 feed stage 而不写 convention。
- 先 `list_block_ports`。无冷凝吸收塔顶端通常是 `VD(OUT)`，不是标准精馏的 `D(OUT)`。
- 如果 Aspen / UI Next 报：
  - `FEEDS not complete: SID = <stream>`
  - `Stage must be specified.`
  - `A feed or pumparound stream to the top stage must be specified when Condenser=None or condenser duty is zero.`
  - `A feed or pumparound stream to the bottom stage must be specified when Reboiler=None or reboiler duty is zero.`
  修复动作不是猜 `FEEDS\<stream>\STAGE` 表路径，而是：`set_feed_stage(...)` + `FEED_CONVEN` + `FEED_CONVE2` + `set_pres1(...)`，优先直接调用 `configure_radfrac_no_condenser_absorber(...)`。

---

## 1. 写入顺序门控

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| `set_radfrac_condenser_type` / `set_radfrac_reboiler_type` | `set_radfrac_stage_count` | 塔型先定 |
| `set_radfrac_stage_count` | `set_radfrac_feed_stage` | 级数含冷凝/再沸级 |
| `set_radfrac_feed_stage` | 进料约定 | 每股进料写 `FEED_CONVEN` + `FEED_CONVE2` |
| 压力 profile | 进料流 `set_pres_mixed` | 进料压 ≥ feed 级板压 |
| 拓扑 | Input | `list_block_ports` → `D(OUT)` / `VD(OUT)` / `B(OUT)` |

### 1.1 压力 profile（先写 `PRES1`，再选第二压力路径）

| 模式 | MCP | 适用场景 |
|------|-----|----------|
| 单一塔压 / 无压降近似 | `set_radfrac_top_pressure` | 吸收塔、常压塔、题面只给一个塔压，或先让 RadFrac 输入完整；`PRES1` 是 Stage 1 / Condenser / top reference pressure |
| TOP-BOTTOM | `set_radfrac_top_pressure` + `set_radfrac_bottom_pressure` | 题面明确给 top/bottom pressure，或需要直接固定第二压力锚点；`PRES2` 是第二 pressure anchor / bottom-side pressure，必须与 `PRES1` 使用同一单位基准 |
| DP-COL | `set_opt_pres(DP-COL)` + `set_radfrac_top_pressure` + `set_radfrac_column_pressure_drop` | 题面给总塔压降；`DP_COL = bottom_pressure - top_pressure` |

如果参考 BKP / APW 的 RadFrac 输入显式出现 `P-SPEC2: PRES1=... PRES2=...`，
不要只写 `PRES1` 后把失败归因于 recycle、feed stage 或 solver。`PRES2`
必须进入初始配置或下一轮 probe 轴；`configure_radfrac_total_condenser(...)`
可用 `bottom_pressure_mode="pres2"` 保留这种 TOP-BOTTOM/P-SPEC2 语义。

`PRES1` 必须优先落地。若 Next / completion 返回
`Top Stage Pressure must be specified when Top/Bottom or Section Pressure Drop is selected.`
或 GUI 落在 `Stage 1 / Condenser pressure`，修复动作是写/读回
`set_pres1(block_name=<BLK>, value=<top pressure>, unit=<unit>)`。

选择第二压力路径时：

- 若题面给 **bottom pressure**，可用 `set_radfrac_bottom_pressure`，或换算成 `DP_COL`
  走 DP-COL；不要两条路径混写后不读回。
- 若题面给 **column pressure drop**，优先用 `OPT_PRES=DP-COL` + `set_radfrac_column_pressure_drop`。
- 若没有明确压降，先只写 `PRES1`；不要为了“补 bottom”虚构压降或底压。
- `bottom_pressure >= top_pressure` 应在同一单位、同一绝压/表压基准下判断。`psig/barg/kPag`
  与 `psia/bar/kPa` 不可直接比较；必要时统一到绝压 `kPa`。
- 常用安全单位：`kPa`, `bar`, `atm`, `mmHg`, `MPa`, `psi`, `psia`, `psig`。
  传给 `set_radfrac_top_pressure` / `set_radfrac_bottom_pressure` 的数值必须匹配单位字面值；`set_radfrac_column_pressure_drop`
  传的是压差，通常用 `kPa`, `bar`, `psi`, `mmHg`, `MPa` 等压差单位。
- 固定塔压的已策展操作是 `set_radfrac_top_pressure` / `set_radfrac_bottom_pressure` / `set_radfrac_column_pressure_drop`。其它 RadFrac 输入先查本文件、helper 签名、或 live option/readback 后再写。

排障顺序：

1. `read_pressure_state(block_name, unit=<same_unit>)` 或直接读
   `Data\Blocks\<BLK>\Input\PRES1`, `PRES2`, `OPT_PRES`, `DP_COL`。
2. 如果 `PRES1` 为空或单位不可信，先重写 `set_radfrac_top_pressure`。
3. 如果 `OPT_PRES=DP-COL`，确认 `DP_COL` 是压降而不是 bottom absolute pressure。
4. 如果使用 `set_radfrac_bottom_pressure`，确认 `PRES2` 与 `PRES1` 同单位且第二压力不低于顶压。
5. 写完压力后再对齐进料流压力；feed stream pressure 应不低于其 feed stage 压力，避免后续 REP/PER_ERROR 报 feed pressure too low。

### 1.2 进料约定（Python helper，不是 HTTP operation）

`configure_radfrac_feed_convention(...)` 是 `script_agent_exp.safe_aspen_calls`
里的 **Python helper**，不是 Aspen HTTP `/execute` operation。生成脚本必须通过
`safe.configure_radfrac_feed_convention(client, ...)` 或
`call_helper("configure_radfrac_feed_convention", client, ...)` 调用；**禁止**
`client.execute("configure_radfrac_feed_convention", ...)` 或
`do_op(client, "configure_radfrac_feed_convention", ...)`。

| helper | token 示例 |
|--------|-------------|
| `configure_radfrac_feed_convention(client, block_name=..., stream_name=..., convention=...)` | `ON-STAGE`, `ABOVE-STAGE`, `VAPOR`, `LIQUID`, `ON-STAGE-VAP`, `ON-STAGE-LIQ`（以 live legal values 为准；UI 可能显示 Vapor/Liquid，生成工具可能接受 `ON-STAGE-VAP`/`ON-STAGE-LIQ`） |
| 内部写 `FEED_CONVEN` + `FEED_CONVE2` **同值** | 失败返回 `legal_values` |

` ` `python
client.invoke("configure_radfrac_feed_convention",
    block_name="CO",
    stream_name="CF",
    convention="ON-STAGE-LIQ",
)
` ` `

禁止把 RadFrac feed stage 当作 `Data\Blocks\<BLK>\Input\FEEDS\<stream>\STAGE` 或 `...\FEEDS\<stream>\FEED_STAGE` 这类猜测路径来写；这些路径在许多模型中不存在或不是可写 surface。进料 **stage** 用 HTTP `set_feed_stage(...)`；进料 **convention** 用上面的 Python helper。

当 RadFrac probe 全部 `PER_ERROR=1` 或塔内交通/进料级附近异常时，不要只扫
`feed_stage` 的数字。`ABOVE-STAGE` / `ON-STAGE` / `VAPOR` / `LIQUID`
（或 `ON-STAGE-VAP` / `ON-STAGE-LIQ` 等工具 token）可能改变 Aspen 对进料落点、
相态和物料衡算的解释，应作为 L1 轴与 stage 数字成束测试。优先用少量 bundle，
例如 `(stage=40, convention=ON-STAGE)`、`(stage=40, convention=ABOVE-STAGE)`、
`(stage=40, convention=VAPOR)`、`(stage=40, convention=LIQUID)`，再扩展到相邻 stage。

### 1.2.1 Bottom-vapor-feed operating specs

`BASIS_D` (molar distillate flow) and `D:F` (distillate/feed ratio) are alternative
operating-spec selections. Numeric writes can change active `COL-SPECS` membership;
do not append `set_d_f` after a successful `set_radfrac_reflux_ratio` + `set_radfrac_distillate_rate` bundle.
For `reboiler != "NONE"`, a call with `reflux_ratio` must also pass exactly one draw specification: `distillate_flow` plus explicit `distillate_flow_unit`, or `d_over_f`. RR alone is structurally under-specified and must be rejected before Aspen execution.

`configure_radfrac_bottom_vapor_feed` keeps explicit `distillate_flow` when both
arguments are supplied and records `d_over_f` as inactive evidence. Ratio-only
calls retain `set_d_f`. The order remains end effects -> stage/pressure -> feed
stage/convention -> reflux -> one draw spec. This is not a mechanism for clearing
old specs on inherited columns: inspect active UI/COL-SPECS rows before a basis
switch; do not guess selector paths or suppress a selected setter failure.
A saturated-vapor bottom feed does not imply `CONDENSER=NONE`: preserve a stated
total condenser and its `LD(OUT)` product role.

### 1.3 端口

| 角色 | 常见端口 | 说明 |
|------|----------|------|
| 进料 | `F(IN)` | 多股进料通常共享这一 material feed collection；不要为第二股进料发明 `F2(IN)` |
| 标准液相馏出 | `LD(OUT)` / `D(OUT)` | 常规全凝器精馏优先 `LD(OUT)`；若 live ports 只有 `D(OUT)` 再用 `D(OUT)` |
| 顶部气相产品 | `VD(OUT)` / `V(OUT)` | 无冷凝吸收/汽提或 vapor overhead 服务使用；不要把气相顶产品接到 `LD(OUT)` |
| 塔釜产品 | `B(OUT)` | 常规 bottoms material outlet |
| 冷凝/再沸热流 | `CHS(OUT)`, `CWS(IN/OUT)`, `HS(IN/OUT)` 等 | 热/公用工程/特殊端口，不是普通 material stream |

Generated slim source treats `list_block_ports` as opaque cross-iteration evidence: record it directly in `runtime.stage(..., required=False)` and do not assign, normalize, parse, or branch on the payload. Use a registered role-aware RadFrac topology capability for connection work; framework internals own any port normalization. Complete topology before product-rate, pressure, condenser, or reboiler specifications.

---

## 2. Core MCP / HTTP Operations

### 2.1 塔型、级数、压力

| MCP operation | 变量 | 允许值 / 参数 |
|---------------|------|---------------|
| `set_radfrac_condenser_type` | `CONDENSER` | `NONE` \| `TOTAL` \| `PARTIAL-V` \| `PARTIAL-V-L` |
| `set_radfrac_reboiler_type` | `REBOILER` | `NONE` \| `KETTLE` \| `THERMOSYPHON` |
| `set_radfrac_stage_count` | `NSTAGE` | int |
| `set_radfrac_top_pressure` | `PRES1` | Stage 1 / Condenser / top reference pressure；float + pressure unit |
| `set_radfrac_bottom_pressure` | `PRES2` | 第二 pressure anchor / bottom-side pressure；float + pressure unit；不要当压降写 |
| `set_radfrac_pressure_mode` | `OPT_PRES` | `DP-STAGE` \| `DP-COL`；总塔压降优先用 `DP-COL` |
| `set_radfrac_column_pressure_drop` | `DP_COL` | 总塔压降；**float + unit 必填**（如 `atm`, `kPa`, `bar`）；值 = bottom pressure − top pressure；缺 `unit` 时 HTTP 直接失败 |
| `read_pressure_state` | `OPT_PRES/PRES1/PRES2/DP_COL/...` | 修压力报错前读回当前 pressure mode 和单位 |

### 2.2 进料与产品规格

Generated code must use the family-specific semantic names below. Native names `set_basis_d` and `set_basis_b` are framework-internal because they collide with PetroFrac/MultiFrac signatures.

| MCP operation | 变量 | 允许值 / 参数 |
|---------------|------|---------------|
| `set_radfrac_feed_stage` | `FEED_STAGE` | exact kwargs: `block_name`, `stream_name`, `value`; `value` is the Aspen stage int (including condenser/reboiler stages). **Do not use `stage=`, `stage_number=`, or `feed_stage=`.** |
| `set_radfrac_reflux_ratio` | `BASIS_RR` | float |
| `set_radfrac_distillate_rate` | `BASIS_D` | float + unit（**摩尔**：`kmol/hr`, `mol/hr`） |
| `set_radfrac_bottoms_rate` | `BASIS_B` | float + unit |
| `set_basis_br` | `BASIS_BR` | float（再沸比） |
| `set_d_f` | `D:F` | float |
| `set_prod_phase` | **`(block_name, value, stream_name)`** | 侧线相；或 `set_reactor_prod_phase` |
| `set_prod_stage` / `set_prod_flow` | 侧线 | 级 / **流量** |

Exact direct-call form for an additional or special RadFrac feed:

` ` `python
client.invoke(
    "set_radfrac_feed_stage",
    block_name="D1",
    stream_name="S1",
    value=5,
)
` ` `

The public capability retains the native setter's generic numeric keyword `value`. The semantic name does **not** imply a `stage` keyword. Prefer `configure_radfrac_total_condenser(..., feed_stage=...)` for the standard single-feed bundle; use the direct capability above only for per-feed additions.

### 2.2.0 Partial-Vapor + Distillate rate 的真实写面

当 GUI/题面组合为 `Condenser = Partial-Vapor`、`Reboiler = Kettle`，并且
Operating specifications 显示 `Reflux ratio` + `Distillate rate` 时，第二行
`Distillate rate` 必须写 RadFrac 原生产品流量变量：

` ` `python
Application.Tree.FindNode(r"\Data\Blocks\D1\Input\BASIS_D")
` ` `

在 MCP/helper 层对应 `client.invoke("set_radfrac_distillate_rate", block_name="D1", value=<rate>, unit=<molar-flow-unit>)`。
不要把这个组合写到 `BASIS_RDV` / `set_basis_rdv`，也不要改写成 `D:F` 分率，除非
live UI 或题面明确把操作规格行改成了 vapor distillate fraction / D:F 一类规格。
完成后必须读回 `BASIS_RR` 与 `BASIS_D`；`BASIS_D` 为空时，塔的 operating specs
仍未完整。

### 2.2.1 固定产品流量 vs 回收率调节

- 如果题目明确给定产品流量（例如 `50 mol/hr bottoms is required`），这是
  RadFrac 原生产品规格：write `BASIS_B` or `BASIS_D` through `set_radfrac_bottoms_rate` / `set_radfrac_distillate_rate`，最终以 converged REP /
  stream readback 证明产品流量、组成和回收率。不要为了“report recovery”再
  人为构造 Design Spec。
- 如果题目要求在一个流量窗口内**调节/寻找**塔釜产品流量以满足某组分回收率，
  使用 `scan_radfrac_bottoms_for_component_recovery(...)` 或 active native
  Design Spec。scan 后必须把选中的 converged 行作为决策依据；若任务要求固定
  产品流量，scan 只能作为诊断，最终仍要重置并运行题面固定规格。
- 不要把固定的 `BASIS_B` seed 加上事后 proof-only recovery 说明当作“调节
  workflow”。调节任务需要 scan/DS 参与同一次 post-adjustment run；固定规格
  任务只需要 final run 的 native spec readback 和产品/组分流量 evidence。

### 2.2.2 RadFrac profile Markdown evidence

`collect_radfrac_profile_markdown_evidence(...)` 是纯文本 helper，不接收
Aspen client。调用时先从当前 trusted REP 读取文本，再用 keyword-only 参数：

` ` `python
rep_text = Path(rep_path).read_text(encoding="utf-8", errors="replace")
profile = safe.collect_radfrac_profile_markdown_evidence(
    rep_text=rep_text,
    block_name="D1",
    component_ids=["MEOH", "ETOH", "H2O"],
    output_dir=artifact_dir,
    profile_name="MOLE-X-PROFILE",
    source_rep_path=rep_path,
)
` ` `

选择 `profile_name` 要跟题目一致：液相组成用 `MOLE-X-PROFILE`，气相组成用
`MOLE-Y-PROFILE`。这只生成数值表。题目要求绘制曲线时，还要调用 §2.4 的
`export_radfrac_composition_profile_plot`，`basis` 与该 profile 一致
（气相摩尔为 `mole_y`，液相摩尔为 `mole_x`）。如果 helper 返回 `row_count=0`，
先修复当前 trusted REP 的 profile，再出图。

吸收塔示例（最小可跑骨架）：

` ` `python
configure_radfrac_no_condenser_absorber(
    client,
    block_name="D1",
    nstage=12,
    feed_stages={"W1": 1, "G1": 12},
    feed_conventions={"W1": "ON-STAGE-LIQ", "G1": "ON-STAGE-VAP"},
    top_pressure=101.325,
    pressure_unit="kPa",
)
` ` `

若 helper 不可用，等价底层写入顺序是：

1. `set_condenser(D1, NONE)` + `set_reboiler(D1, NONE)` + `set_nstage(D1, 12)`。
2. `set_pres1(D1, 101.325, "kPa")`，必要时再选择 `set_radfrac_bottom_pressure` 或 `OPT_PRES=DP-COL` + `set_radfrac_column_pressure_drop`。
3. `set_feed_stage(D1, W1, 1)`、`set_feed_stage(D1, G1, 12)`。
4. `safe.configure_radfrac_feed_convention(client, block_name="D1", stream_name=..., convention=...)`；气体 `ON-STAGE-VAP`，液体 `ON-STAGE-LIQ`。

### 2.3 收敛与其它

| MCP operation | 变量 | 允许值 |
|---------------|------|--------|
| `set_conv_meth` | `CONV_METH` | `STANDARD` \| … \| `AZEOTROPIC` |
| `set_maxol` | `MAXOL` | float |
| 共沸初值 | helper 内部 | `INIT_OPTION`/`RESTART` 由专用 helper 处理，agent 勿 raw tree 写 |
| `read_pressure_state` | — | `block_name`, `unit` → 各级压力读回 |

### 2.4 组成分布曲线

任务要求绘制塔内组成曲线时，调用
`export_radfrac_composition_profile_plot(client, block_name=..., components=[...], basis=...)`。
`basis` 取 `mole_y`（气相摩尔，含「气相组成」）、`mole_x`（液相摩尔）、`mass_y`、`mass_x`。
该调用读取当前结果树并写出英文 PNG，把返回路径写入 `summary["plots"]`。
`MOLE-Y-PROFILE` / `MOLE-X-PROFILE` 或 Markdown 表只作为同基准的数值来源。

| MCP operation | 说明 |
|---------------|------|
| `export_radfrac_composition_profile_plot` | 从当前结果树绘制英文组成分布 PNG |
| `ui_export_radfrac_profile_plot` | 仅 Aspen 窗口截图，不作为曲线成品 |

---

## 3. 拓扑 MCP

| 操作 | 参数 |
|------|------|
| `create_radfrac` | `block_name` |
| `list_block_ports` | `block_name` |
| `connect_stream` | `block_name`, `stream_name`, `port_name` |
| `engine_run` | — |

---

## 4. 读回

| 目标 | 方式 |
|------|------|
| 产品纯度/流量 | REP / stream Output |
| 塔板组成曲线 | `export_radfrac_composition_profile_plot` 的英文 PNG；数值来源为同基准的 `MOLE-X-PROFILE` / `MOLE-Y-PROFILE` |

---

## 5. 关联块

- 简捷初值 → **DSTWU**（`dstwu.md`）
- DS/SA/OPT 操纵 token → `design_spec.md` / `sensitivity.md` / `optimization.md`

---

## 9. 汇总

| 项 | 内容 |
|----|------|
| Core setter | §2 所列 |
| 推荐 helper | §0 六条 |

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/pump.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：PUMP（泵）

- **块类型**：`PUMP`（Aspen 仅有此泵族；题面 “Pump HI” 不是独立块型）
- **Aspen 语义**：液体加压；出口规格 `OPT_SPEC` 必设。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper

无专用 helper；直接使用 §2 MCP operation。

---

## 1. 写入顺序门控（CRITICAL）

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| `set_pump_outlet_spec` | 出口规格 / 曲线 | **缺则 completion 报 Outlet Specification must be specified** |
| 曲线 bundle | `USE-CURVE` 选定后 | `OPT_CTYPE` → `OPT_CFORMAT` → `DEP_VAR` / `INDEP_VAR` → `set_pump_curve_table` |
| 拓扑 | Input | F(IN)/P(OUT) 连接 |

---

## 2. Core MCP / HTTP Operations

| MCP operation | Aspen 变量 | 允许值 / 参数 | 说明 |
|---------------|------------|---------------|------|
| `set_pump_outlet_spec` | `OPT_SPEC` | 见 §2.1 | **缺则 completion 报 Outlet Specification must be specified** |
| `set_pump_outlet_pressure` | `PRES` | float + unit | `OPT_SPEC=PRES` 时出口压力 |
| `set_delp` | `DELP` | float + unit | `OPT_SPEC=DELP` 时压升 |
| `set_pratio` | `PRATIO` | float | `OPT_SPEC=PRATIO` 时压比 |
| `set_power` | `POWER` | float + unit | `OPT_SPEC=POWER` 时功率 |
| `set_eff` | `EFF` | float | 泵效率 |
| `set_deff` | `DEFF` | float | 驱动效率，默认 1 |
| `set_opt_ctype` | `OPT_CTYPE` | `SINGLE-OPER` \| `SINGLE-REFE` \| `MULTIP` | 曲线控制类型 |
| `set_opt_cformat` | `OPT_CFORMAT` | `TABLE` \| `POLY` \| `USER-CURVES` | 曲线数据格式 |
| `set_dep_var` | `DEP_VAR` | `HEAD` \| `HEAD-COEF` \| `POWER` \| `PRES` \| `PRAT` \| `DELP` | 性能曲线纵轴 |
| `set_indep_var` | `INDEP_VAR` | `VOL-FLOW` \| `MASS-FLOW` | 性能曲线横轴流量类型 |
| `set_pump_curve_table` | （曲线表） | 见说明 | HEAD_DATA + H_FLOW 表写入 |

### 2.1 `OPT_SPEC` / Outlet Specification

| token | 含义 | 后续写入 |
|-------|------|----------|
| `PRES` | Discharge pressure | `set_pres(..., unit=...)` |
| `DELP` | Pressure increase | `set_delp` |
| `PRATIO` | Pressure ratio | `set_pratio` |
| `POWER` | Power required | `set_power` |
| `USE-CURVE` | Performance curve | 曲线 bundle（§2.2） |

**配置特性曲线必须先选 `USE-CURVE`。**

### 2.2 曲线模式推荐顺序（`OPT_SPEC=USE-CURVE`）

1. `set_opt_spec(USE-CURVE)`
2. `set_opt_ctype(SINGLE-OPER)`（或题面指定）
3. `set_opt_cformat(TABLE)`
4. `set_dep_var(HEAD)` + `set_indep_var(VOL-FLOW)`
5. `set_pump_curve_table(curve_points=[{flow, head}, ...])`
6. 可选 `set_eff` / `set_deff`

---

## 3. 拓扑与其它 MCP

| 操作 | 参数 | 说明 |
|------|------|------|
| `create_pump` | `block_name` | 创建 PUMP 块 |
| `create_material_stream` | `stream_name` | 按需建流股 |
| `list_block_ports` | `block_name` | 查端口名 |
| `connect_stream` | `block_name`, `stream_name`, `port_name` | 拓扑完成后再写 Input |
| `check_block_completion` | `block_name` | 块 completion |
| `check_next_completion_status` | — | run 前至少一次 |
| `engine_run` | — | 仿真 |

---

## 4. 结果读回

| 目标 | 方式 |
|------|------|
| 块/分析输出 | REP、helper readback payload |
| 输入验收 | REP 中 `OPT_SPEC`、曲线点、效率 |

---

## 9. 汇总

| 项 | 内容 |
|----|------|
| Core operations | 12+ |
| 推荐 skill | `aspen-pump-outlet-specification` |

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/compr.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：COMPR（压缩机）

- **块类型**：`COMPR`
- **Aspen 语义**：压缩机；出口 **PRES**、**DELP**、压比或功率规格。

---

Generated public capability names in this document are family-specific. The underlying Aspen variable tokens remain unchanged; do not replace these names with generic native setters from another block family.

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

` ` `text
configure_compr_pressure_rise(
    client, *, block_name, delta_pressure, pressure_unit=None,
    compressor_type="ISENTROPIC",
)
` ` `

---

## 1. 写入顺序门控

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| `set_type` | `set_compr_outlet_spec` | 压缩机类型 |
| `set_compr_outlet_spec` | `set_compr_outlet_pressure` / `set_delp` / `set_pratio` | 规格模式 |
| 效率 | 数值规格 | `set_peff`, `set_meff`（多变/ASME 型） |

---

## 2. Core MCP / HTTP Operations

| MCP operation | 变量 | 允许值 / 参数 | 说明 |
|---------------|------|---------------|------|
| `set_type` | `TYPE` | 见 §2.1 | 压缩模型；须先于 `OPT_SPEC` |
| `set_compr_outlet_spec` | `OPT_SPEC` | 见 §2.2 | 出口规格类型 |
| `set_compr_outlet_pressure` | `PRES` | float + unit | **`OPT_SPEC=PRES`** 时出口压力 |
| `set_delp` | `DELP` | float + unit | **`OPT_SPEC=DELP`** 时压升 |
| `set_pratio` | `PRATIO` | float | **`OPT_SPEC=PRATIO`** 时压比 |
| `set_power` | `POWER` | float + unit | **`OPT_SPEC=POWER`** 时功率 |
| `set_peff` | `PEFF` | float (0–1) | 多变效率 |
| `set_meff` | `MEFF` | float (0–1) | 机械效率，默认 1.0 |

### 2.1 `TYPE` / Compressor Model

| token | 含义 | 何时使用 |
|-------|------|----------|
| `ISENTROPIC` | Isentropic | 等熵效率题 |
| `ASME-POLYTROP` | Polytropic (ASME) | 两级压缩链常见（tya 题） |
| `GPSA-POLYTROP` | Polytropic (GPSA) | GPSA 多变法 |
| `ASME-ISENTROP` | Isentropic (ASME) | ASME 等熵 |
| `GPSA-ISENTROP` | Isentropic (GPSA) | GPSA 等熵 |
| `INT-POLYTROP` | Polytropic, piecewise integration | 分段积分多变 |
| `POS-DISP` | Positive displacement | 容积式 |
| `INT-POS-DISP` | Positive displacement, piecewise | 分段容积式 |

### 2.2 `OPT_SPEC` / Outlet Specification

| token | 含义 | 后续写入 |
|-------|------|----------|
| `PRES` | Discharge pressure | `set_compr_outlet_pressure` |
| `DELP` | Pressure increase | `set_delp` |
| `PRATIO` | Pressure ratio | `set_pratio` |
| `POWER` | Power required | `set_power` |
| `USE-CURVE` | Performance curve | 曲线表数据 |

**必须先 `set_compr_outlet_spec`，再写对应数值**；与 Pump 的 `OPT_SPEC` 同 token 集合。

### 2.1 两级压缩链（典型拓扑）

| 块 | 写入 |
|----|------|
| C1 | `ASME-POLYTROP`, `OPT_SPEC=PRES`, `set_peff`, `set_meff`, `set_compr_outlet_pressure` |
| IC (Heater) | `set_compr_temperature` 级间冷却 |
| C2 | 同上，终压 `set_compr_outlet_pressure` |

Sensitivity 常扫 **C1 `PRES`**，响应 **C1/C2 轴功率**（`WNET`/`BRAKEHP` 等 BLOCK-VAR）。

---

## 3. 拓扑 MCP

| 操作 | 参数 |
|------|------|
| `create_compr` | `block_name` |
| `connect_stream` | INLET / OUTLET |
| `engine_run` | — |

---

## 5. 关联块

级间冷却 → **Heater**（`heater.md`），不是 Compr 变量。

---

## 9. 汇总

| 项 | 内容 |
|----|------|
| Core setter | 6 |
| 推荐 helper | `configure_compr_pressure_rise` |

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/pipe.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：PIPE（管道）

- **块类型**：`PIPE`
- **Aspen 语义**：管道压降/长度/管系表（schedule）定径。

---

## 0. Helper

管系定径仅用 **`safe.configure_pipe_schedule_sizing(...)`**。Agent 脚本不要直接调用底层 pipe sizing HTTP operation。

---

## 1. 写入顺序门控（CRITICAL）

| 步骤 | 说明 |
|------|------|
| 拓扑 | 先 `list_block_ports` + `connect_stream` |
| 管系规格 | 再 `configure_pipe_schedule_sizing(...)`（helper 内部保证顺序） |

---

## 2. Agent 可用配置面

### `configure_pipe_schedule_sizing` — 目的

Aspen **PIPE + OSCHED（管系表定径）** 路径对 Input 变量有**严格先后依赖**：必须先切到 schedule 模式，再写材质 → 系列号 → 公称直径 → 管长。Agent 若逐步调用底层 setter，常见结果是顺序错乱、静默丢写或 completion 卡住（chn-9-1 等题已复现）。

该 helper 的目的：

1. **把 OSCHED 整包写入收成一次调用**，在 agent 侧固定顺序，避免 planner/codegen 拆成多个 HTTP op。
2. **写后读回** `OPT_DIAM` / `MATERIAL` / `SCHEDULE` / `NOMINAL_DIAM` / `LENGTH`，产出 `check_ok`、`readbacks`、`summary`，可直接进 `summary.json` 作 validator/score 证据。
3. **与 skill 对齐**：skill 只暴露 helper，不再引导 agent 记底层 setter 名称。

### 覆盖范围

| 维度 | 覆盖 | 不覆盖 |
|------|------|--------|
| 块类型 | `PIPE` | `Pipeline`、其它块 |
| 定径模式 | `OPT_DIAM=OSCHED`（管系表） | `OINNER` 内径直给、`USER-SUBR` |
| 写入变量 | `OPT_DIAM`、`MATERIAL`、`SCHEDULE`、`NOMINAL_DIAM`、`LENGTH` | 摩擦关联式、保温、管件、其它 Input 页 |
| 参数面 | `material`（`CARBON-STEEL` / `STAINLESS`）；`schedule`（10/20/40/80/120/160）；`nominal_diam`（如 `1-IN`）；`length` + `length_unit` | 非上述枚举的材质/管系/公称直径 token |
| 拓扑 / 生命周期 | 无（假定块已 `create_pipe` 且进出口已连接） | `create_pipe`、`connect_stream`、删除/替换块 |
| 典型任务 | chn-9-1：`PIPE` 碳钢 Sch-40、1 in、25 m | 只给内径、无 schedule 的 PIPE 题 |

### 入口一览

| 入口 | 说明 |
|------|------|
| `configure_pipe_schedule_sizing` | OSCHED 管系定径整包（agent 侧 safe helper） |

### 参数 option list

helper 签名：

` ` `python
safe.configure_pipe_schedule_sizing(
    client,
    *,
    block_name: str,
    material: str = "CARBON-STEEL",
    schedule: int = <number>,
    nominal_diam: str = "1-IN",
    length: float =<float number>,
    length_unit: str = "meter",
)
` ` `

| 参数 | Aspen 变量 | 允许值 / 说明 |
|------|------------|---------------|
| `block_name` | — | 已创建且已连线的 `PIPE` 块名 |
| `material` | `MATERIAL` | `CARBON-STEEL` \| `STAINLESS` |
| `schedule` | `SCHEDULE` | `10` \| `20` \| `40` \| `80` \| `120` \| `160` |
| `nominal_diam` | `NOMINAL_DIAM` | 见下表（公称直径 token，必须带 `-IN` 后缀） |
| `length` | `LENGTH` | 正浮点数 |
| `length_unit` | `LENGTH` 单位 | 常用 `meter`；与 Aspen 量纲一致即可 |

### 2.1 必填几何输入与 `OPT_DIAM` 分支

`PIPE` 的管长是几何输入，不应由拓扑或 schedule token 代替。直接树路径是
`Data\Blocks\<BLK>\Input\LENGTH`；例如本类流程中的 `PI` 块为
`Data\Blocks\PI\Input\LENGTH`。

内径输入取决于 `OPT_DIAM`：

| `OPT_DIAM` 路径 | 必填几何/定径输入 | 说明 |
|-----------------|-------------------|------|
| `OSCHED` schedule 模式 | `MATERIAL`、`SCHEDULE`、`NOMINAL_DIAM`、`LENGTH` | 通过 `configure_pipe_schedule_sizing(...)` 整包写入；不要额外要求 `IN_DIAM` |
| direct inner-diameter / `OINNER` 模式 | `IN_DIAM`、`LENGTH` | `IN_DIAM` 直接路径为 `Data\Blocks\<BLK>\Input\IN_DIAM`，如 `Data\Blocks\PI\Input\IN_DIAM` |

如果 completion 或 UI Next 指向 pipe length，先补 `LENGTH`；只有确认
`OPT_DIAM` 是 direct inner-diameter 模式时，才把 `IN_DIAM` 当作缺失必填项。

**`nominal_diam` 完整 option list：**

`0.25-IN`, `0.375-IN`, `0.5-IN`, `0.75-IN`, `1-IN`, `1.5-IN`, `2-IN`, `3-IN`, `4-IN`, `5-IN`, `6-IN`, `8-IN`, `10-IN`, `12-IN`, `14-IN`, `16-IN`, `18-IN`, `20-IN`, `24-IN`, `30-IN`, `36-IN`, `42-IN`, `48-IN`, `54-IN`, `60-IN`, `66-IN`, `72-IN`, `78-IN`, `84-IN`, `90-IN`, `96-IN`


helper 内部固定写入顺序（只读、勿在脚本中复现）：`OPT_DIAM=OSCHED` → `MATERIAL` → `SCHEDULE` → `NOMINAL_DIAM` → `LENGTH`。

更多示例见 skill `aspen-pipe-material-and-schedule`。

---

## 3. 拓扑与其它 MCP

| 操作 | 参数 | 说明 |
|------|------|------|
| `create_pipe` | `block_name` | 创建 PIPE 块 |
| `create_material_stream` | `stream_name` | 按需建流股 |
| `list_block_ports` | `block_name` | 查端口名 |
| `connect_stream` | `block_name`, `stream_name`, `port_name` | 拓扑完成后再写 Input |
| `check_block_completion` | `block_name` | 块 completion |
| `check_next_completion_status` | — | run 前至少一次 |
| `engine_run` | — | 仿真 |

---

## 4. 结果读回

| 目标 | 方式 |
|------|------|
| 块输入 | REP 中 `OPT-DIAM`、`MATERIAL`、`SCHEDULE`、`NOMINAL-DIAM`、`LENGTH`；或 helper 返回的 `readbacks` / `check_ok` |
| 块输出 | REP 压降/出口状态 |

---

## 9. 汇总

| 项 | 内容 |
|----|------|
| Agent 配置入口 | `configure_pipe_schedule_sizing` |
| 推荐 skill | `aspen-pipe-material-and-schedule` |

` ` `

### FILE: docs/hardcoded_script_plan/block_type_inject/valve.md
Reason: block-family Aspen surface selected from task profile
` ` `text
# Block-Type 注入：VALVE（阀门）

- **块类型**：`VALVE`
- **Aspen 语义**：压力降/出口压力规格；任务若给出厂商/系列/口径，须用 vendor preset 一次写入四字段。

---

## 0. Helper（`script_agent_exp.safe_aspen_calls`）

| Helper | 主要参数 | 作用 |
|--------|----------|------|
| `configure_valve_pressure_changer_outlet(...)` | `block_name`, `outlet_pressure`, `pressure_unit` | **效间降压 / pressure changer**：`MODE=ADIAB-FLASH` → `OPT_DESIGN=P-OUT` → `P_OUT+unit` |
| `configure_valve_pressure_changer_pressure_drop(...)` | `block_name`, `pressure_drop`, `pressure_unit` | **pressure changer + 压降规格**：`MODE=ADIAB-FLASH` → `OPT_DESIGN=P-DROP` → `P_DROP+unit` |
| `configure_valve_outlet_pressure_design(...)` | `block_name`, `outlet_pressure`, `pressure_unit`, 可选 `vendor_preset_id` | **阀门系数设计**：`MODE=SET-PRESSURE` → `OPT_DESIGN=P-OUT` → `P_OUT+unit`；任务有 vendor 规格时传 `vendor_preset_id` |
| `list_valve_vendor_presets(client)` | — | 只读：返回稳定 `(VAL_TYPE, MFGR, SERIES, SIZE)` 组合表 |
| `apply_valve_vendor_preset(client, block_name=..., preset_id=...)` | `preset_id` | **唯一** agent 写入 commercial geometry 的路径；内部按序写四字段并读回 |

**生成脚本优先用 helper，不要裸调 `set_mode` / `set_opt_design` 后漏写 `P_OUT` 或 `unit`。**

**Pressure changer**（GUI Calculation type = *Adiabatic flash for specified outlet pressure*）：`MODE=ADIAB-FLASH` 选定后，**Pressure specification** 二选一，且必须写对应数值+单位：

| GUI 选项 | `OPT_DESIGN` | 必填 leaf | Helper |
|----------|--------------|-----------|--------|
| Outlet pressure | `P-OUT` | `P_OUT + unit` | `configure_valve_pressure_changer_outlet` |
| Pressure drop | `P-DROP` | `P_DROP + unit` | `configure_valve_pressure_changer_pressure_drop` |

效间降压 — 题目给**绝对出口压力**（多效蒸发 VA1–VA4 常见）：

` ` `python
outlet_pressure_value = ...  # effect pressure basis from task/table
client.invoke("configure_valve_pressure_changer_outlet",
    block_name="VA1",
    outlet_pressure=outlet_pressure_value,
    pressure_unit="kPa",
)
` ` `

效间降压 — 题目给**阀压降 / ΔP**：

` ` `python
delta_p_value = ...  # pressure drop from task
client.invoke("configure_valve_pressure_changer_pressure_drop",
    block_name="VA1",
    pressure_drop=delta_p_value,
    pressure_unit="kPa",
)
` ` `

**禁止**在生成脚本中调用 `set_val_type` / `set_mfgr` / `set_series` / `set_size`：它们不在 script-agent **core MCP 面**（`main_core.py`），仅作为 `apply_valve_vendor_preset` 的内部实现。

阀门系数 **design**（任务只给出口压力、无 vendor 文字，`MODE=SET-PRESSURE`）：

` ` `python
outlet_pressure_value = ...  # numeric value from the task
client.invoke("configure_valve_outlet_pressure_design",
    block_name="VA",
    outlet_pressure=outlet_pressure_value,
    pressure_unit="MPa",
)
` ` `

任务同时给出 vendor / series / characteristic / nominal size 时，**必须**从 §2.4 catalog 选择匹配的 `preset_id`，不要只写出口压力：

` ` `python
outlet_pressure_value = ...  # numeric value from the task
selected_preset_id = "..."  # from list_valve_vendor_presets / §2.4 catalog
client.invoke("configure_valve_outlet_pressure_design",
    block_name="VA",
    outlet_pressure=outlet_pressure_value,
    pressure_unit="MPa",
    vendor_preset_id=selected_preset_id,
)
` ` `

或先 design 再单独 preset：

` ` `python
client.invoke("apply_valve_vendor_preset",
    block_name="VA",
    preset_id=selected_preset_id,
)
` ` `

压力-only 案例可以不写 vendor preset；只要任务出现厂商、系列、流量特性、口径、nominal size 等 commercial geometry 语义，就必须补 `vendor_preset_id` 或单独调用 `safe.apply_valve_vendor_preset(...)`。

---

## 1. 写入顺序门控（CRITICAL）

| 步骤 | 必须先于 | 说明 |
|------|----------|------|
| 拓扑 | Input | 先 `list_block_ports` + `connect_stream`，再写块变量 |
| `MODE` | 压力/系数规格 | `MODE` 是 Valve 的 calculation type gate，必须先决定计算类型 |
| `OPT_DESIGN` | `P_OUT` / `P_DROP` | **`P-OUT`** → `set_p_out(..., unit=...)`；**`P-DROP`** → `set_p_drop(..., unit=...)` |
| 压力数值 + unit | Fill / run | 与 `OPT_DESIGN` 匹配的 leaf 必须带 **unit**；漏 unit 会 TypeError |
| commercial geometry | completion 要求 Manufacturer/Series/Size | **仅** `list_valve_vendor_presets` → `apply_valve_vendor_preset`；禁止散写四字段 |

**Commercial valve geometry 是强门控。** Aspen 会根据前一个下拉框刷新后续 option list；`apply_valve_vendor_preset` 已封装 `VAL_TYPE → MFGR → SERIES → SIZE` 顺序。

---

## 2. Core MCP / HTTP Operations

| MCP operation | Aspen 变量 | 允许值 / 参数 | 说明 |
|---------------|------------|---------------|------|
| `set_mode` | `MODE` | ADIAB-FLASH / SET-PRESSURE / CALC-PRESSURE | **Calculation type gate**。见 §2.1；必须早于 pressure/design/rating/vendor 规格。 |
| `set_opt_design` | `OPT_DESIGN` | `P-OUT` / `P-DROP` | GUI **Pressure specification**；见 §2.2 |
| `set_p_out` | `P_OUT` | **`value` + `unit`** | **`OPT_DESIGN=P-OUT`** → `\Data\Blocks\<ID>\Input\P_OUT` |
| `set_p_drop` | `P_DROP` | **`value` + `unit`** | **`OPT_DESIGN=P-DROP`** → `\Data\Blocks\<ID>\Input\P_DROP` |
| `set_check_choke` | `CHECK_CHOKE` | NO / YES | 任务未讨论 choking 时通常 `NO`。 |
| `set_pdrp_fac` | `PDRP_FAC` | float | 可选 rating factor；只有任务或既有基准明确给出时写。 |
| `set_prec_fac` | `PREC_FAC` | float | 可选 rating factor；只有任务或既有基准明确给出时写。 |
| `list_valve_vendor_presets` | — | read-only | 返回稳定 preset 表；生成脚本优先 `safe.list_valve_vendor_presets`。 |
| `apply_valve_vendor_preset` | `VAL_TYPE/MFGR/SERIES/SIZE` | `preset_id` | **唯一** commercial geometry 写入面；生成脚本优先 `safe.apply_valve_vendor_preset`。 |

`vendor_preset_id` 与 `PDRP_FAC` / `PREC_FAC` 互斥：Aspen 把 commercial
Library Valve 几何和 pressure/recovery factors 当作二选一输入。通过
`configure_valve_outlet_pressure_design(..., vendor_preset_id=...)` 时不要再写
`set_pdrp_fac` / `set_prec_fac`；helper 会跳过默认 rating factors 并记录
`rating_factors_skipped_due_to_vendor_preset`。

### 2.1 `MODE` / Calculation Type

`Data\Blocks\<B>\Input\MODE` 对应 GUI 的 **Calculation type**，是 Valve 最重要的 function gate：

| `MODE` 值 | GUI 文案 | 何时使用 | 后续规格 |
| --- | --- | --- | --- |
| `ADIAB-FLASH` | Adiabatic flash for specified outlet pressure (pressure changer) | 只需要按给定出口压力做绝热闪蒸/压力改变，不需要计算 valve coefficient | 通常配合 `OPT_DESIGN=P-OUT` + `P_OUT` |
| `SET-PRESSURE` | Calculate valve flow coefficient for specified outlet pressure (design) | 已知出口压力，希望 Aspen 计算阀门流量系数/设计参数 | `OPT_DESIGN=P-OUT` + `set_p_out(..., unit=...)` + 任务有 vendor 时 `apply_valve_vendor_preset` |
| `CALC-PRESSURE` | Calculate outlet pressure for specified valve (rating) | 已知阀门/开度/flow coefficient，让 Aspen 反算出口压力 | 通常进入 rating 路线，配合 vendor geometry、`OPT_RATING`、`VAL_POSN` 或 `FLO_COEF` |

`MODE` 写错会改变后续必填项：例如把 design 任务误设成 rating，Aspen 会开始要求 valve vendor/size/position；把 rating 任务误设成 pressure changer，则不会使用真实阀门规格。

### 2.2 `OPT_DESIGN` / Pressure Specification（option + value）

GUI 面板 **Pressure specification** 是 **二选一 radio + 数值** 结构：先选 option，再写对应 leaf。

| `OPT_DESIGN` | GUI 选项 | 必填 tree leaf | MCP 写法 |
|--------------|---------|---------------|----------|
| `P-OUT` | Outlet pressure | `\Data\Blocks\<ID>\Input\P_OUT` | `set_opt_design(..., value="P-OUT")` 然后 `set_p_out(..., value=..., unit=...)` |
| `P-DROP` | Pressure drop | `\Data\Blocks\<ID>\Input\P_DROP` | `set_opt_design(..., value="P-DROP")` 然后 `set_p_drop(..., value=..., unit=...)` |

**规则**：

- 题目给 **出口压力** → `P-OUT` + `P_OUT`（`configure_valve_outlet_pressure_design` 默认此路径）。
- 题目给 **阀压降**（inlet − outlet）→ `P-DROP` + `P_DROP`；**不要**在 `P-DROP` 模式下写 `P_OUT`。
- 两种模式都必须带 **unit**（如 `bar`、`MPa`）；只传 float 会 TypeError。

### 2.3 Rating 路线 enum（`MODE=CALC-PRESSURE` 时）

| MCP / 变量 | 合法 token | 含义 |
|------------|-----------|------|
| `set_opt_rating` / `OPT_RATING` | `VAL-POSN` \| `FLOW-COEF` | Rating 操作规格：按开度或流量系数 |
| `set_char_eq` / `CHAR_EQ` | `LINEAR` \| `PARABOLIC` \| `HYPERBOLIC` \| `SQUARE-ROOT` \| `QUICK-OPENING` \| `EQUAL-PERCENTAGE` | 阀门特性曲线 |
| `set_opt_min_pres` / `OPT_MIN_PRES` | `GLOBAL` \| `SPECIFY` \| `CHOKING` | Rating 时出口最小压力规格 |

### 2.4 Commercial Geometry Presets（只读对照表）

四字段 **不能** 由 agent 逐个 MCP 写入；下表仅用于从任务文字映射 `preset_id`：

| 字段 | Tree path 示例 | 设置方式 |
| --- | --- | --- |
| `VAL_TYPE` | `Data\Blocks\B1\Input\VAL_TYPE` | 仅经 `apply_valve_vendor_preset` |
| `MFGR` | `Data\Blocks\B1\Input\MFGR` | 仅经 `apply_valve_vendor_preset` |
| `SERIES` | `Data\Blocks\B1\Input\SERIES` | 仅经 `apply_valve_vendor_preset` |
| `SIZE` | `Data\Blocks\B1\Input\SIZE` | 仅经 `apply_valve_vendor_preset` |

已知稳定组合（`data/code/set_valve_variables/set_valve_variables.py` → `_VALVE_VENDOR_PRESETS`）：

| `preset_id` | `VAL_TYPE` | `MFGR` | `SERIES` | `SIZE` |
| --- | --- | --- | --- | --- |
| `neles_ball_v810_equal_pct_2in` | `BALL` | `NELES-JAMESBURY` | `V810_EQUAL_PERCENT_FLOW` | `2-IN` |
| `neles_butterfly_v810_equal_pct_3in` | `BUTTERFLY` | `NELES-JAMESBURY` | `V810_EQUAL_PERCENT_FLOW` | `3-IN` |
| `neles_globe_v500_equal_pct_1p5in` | `GLOBE` | `NELES-JAMESBURY` | `V500_EQUAL_PERCENT_FLOW` | `1.5-IN` |
| `neles_globe_v500_linear_1p5in` | `GLOBE` | `NELES-JAMESBURY` | `V500_LINEAR_FLOW` | `1.5-IN` |
| `neles_globe_v810_equal_pct_1p5in` | `GLOBE` | `NELES-JAMESBURY` | `V810_EQUAL_PERCENT_FLOW` | `1.5-IN` |
| `neles_globe_v810_linear_1p5in` | `GLOBE` | `NELES-JAMESBURY` | `V810_LINEAR_FLOW` | `1.5-IN` |

任务文字 → preset 映射示例：

| 任务关键词 | `preset_id` |
| --- | --- |
| V810 equal percent flow globe 1.5 in | `neles_globe_v810_equal_pct_1p5in` |
| V810 linear flow globe 1.5 in | `neles_globe_v810_linear_1p5in` |
| V500 equal percent globe 1.5 in | `neles_globe_v500_equal_pct_1p5in` |

Agent 必须：

- **Design 出口压力**：`configure_valve_outlet_pressure_design(...)`；不要漏 `unit`。
- **任务含 vendor/系列/口径**：同一 helper 传 `vendor_preset_id`，或 `apply_valve_vendor_preset`；**不要**裸调 `set_val_type` / `set_mfgr` / `set_series` / `set_size`。
- completion 仍缺 Manufacturer/Series/Size 时：先确认已 `apply_valve_vendor_preset`，再查 `MODE` 是否误入 `CALC-PRESSURE`。

---

## 3. 拓扑与其它 MCP

| 操作 | 参数 | 说明 |
|------|------|------|
| `create_valve` | `block_name` | 创建 VALVE 块 |
| `create_material_stream` | `stream_name` | 按需建流股 |
| `list_block_ports` | `block_name` | 查端口名 |
| `connect_stream` | `block_name`, `stream_name`, `port_name` | 拓扑完成后再写 Input |
| `check_block_completion` | `block_name` | 块 completion |
| `check_next_completion_status` | — | run 前至少一次 |
| `engine_run` | — | 仿真 |

---

## 4. 结果读回

| 目标 | 方式 |
|------|------|
| 块/分析输出 | REP、helper readback payload |
| 输入验收 | 关键 Input 变量非 null；`P_OUT` 读回应与 `unit` 一致 |
| vendor 四字段 | `apply_valve_vendor_preset` 返回的 `readback` 或 helper readback on `VAL_TYPE/MFGR/SERIES/SIZE` |

---

## 5. 常见失败

| 症状 | 根因 | 修复 |
|------|------|------|
| completion 落在 Valve Operation，Outlet pressure 为空 | `MODE=ADIAB-FLASH` + `P-OUT` 但未写 `P_OUT` | `configure_valve_pressure_changer_outlet(...)` |
| completion 落在 Valve Operation，Pressure drop 为空 | `MODE=ADIAB-FLASH` + `P-DROP` 但未写 `P_DROP` | `configure_valve_pressure_changer_pressure_drop(...)` |
| `set_p_out() missing 1 required positional argument: 'unit'` | 裸调 `set_p_out` 只传 value | 改用 `configure_valve_pressure_changer_outlet` / `configure_valve_outlet_pressure_design` 或补 `unit="MPa"` |
| completion 要求 Manufacturer/Series/Size | 任务有 vendor 但未 preset | 按 §2.4 选择 `preset_id`，传 `vendor_preset_id` 或调用 `apply_valve_vendor_preset` |
| completion 要求 Manufacturer/Series/Size | `MODE=CALC-PRESSURE` 误入 rating | 改回 `SET-PRESSURE` + `P-OUT`，并补 vendor preset |
| vendor 字段写不进去 | 散写四字段或顺序错 | **仅** `apply_valve_vendor_preset(preset_id=...)` |

---

## 9. 汇总

| 项 | 内容 |
|----|------|
| Core operations | 6 pressure/design setters + 2 vendor preset helpers |
| 推荐 helper | `configure_valve_pressure_changer_outlet` / `configure_valve_pressure_changer_pressure_drop`（效间降压）；`configure_valve_outlet_pressure_design`（design）；vendor **仅** `apply_valve_vendor_preset` |
| 关键陷阱 | `ADIAB-FLASH` 只改 calculation type 不够；`P-OUT` 需 `P_OUT+unit`，`P-DROP` 需 `P_DROP+unit` |

` ` `

### FILE: aspen_agent_skills/guides/aspen-task-execution-order/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: aspen-task-execution-order
description: Core execution order for generated Aspen scripts. Use for every Aspen task to sequence setup, topology, analysis objects, engine runs, and final evidence without hiding failures behind later steps.
---

# Aspen Task Execution Order

## Unified Capability Call Contract

- Generated Aspen model operations use exactly `client.invoke("capability", **keyword_parameters)`.
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

` ` `python
client.invoke("ensure_property_method",  method="UNIQUAC")
` ` `

This must set and read back the active global option-set fields. If Aspen reports `OPTION-SETS (...) already exists`, treat that as non-fatal only when the global method readback still matches the requested method.

For block-local methods, use:

` ` `python
client.invoke("configure_block_property_method",  block_name="A1", method="UNIQUAC")
` ` `

Then read back `\Data\Blocks\<BLOCK>\Input\OPSETNAME` for each block.

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
- Legacy `ensure_session(initial_bkp=None, show_gui=None, inset=None)` returns `None` on success and raises on failure; never classify `None` as a failed envelope. `task_name`/`task_key` are not session-method arguments: invalid signatures fail clearly, never silently drop identity. Slim runtime uses its canonical `ensure_runtime_session(*, show_gui=False, inset="SI")` receipt without changing regular consumers.
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

` ` `

### FILE: aspen_agent_skills/guides/aspen-property-method-selection/SKILL.md
Reason: selected skill for task block family
` ` `text
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

A liquid activity-coefficient method and a vapor EOS are separate requirements. Selecting UNIFAC alone does not establish ideal-gas vapor: Aspen's default UNIFAC option set can retain REDLICH-KWONG vapor. When the task explicitly requests UNIFAC liquid plus ideal-gas vapor (IG), call the existing `safe.configure_unifac_ideal_vapor(client)` rather than only `ensure_property_method(..., method="UNIFAC")`. Require helper success and its readbacks `GMODIFY=YES`, `GVAPOREOS=ESIG`, and retained `GLIQGAMMA=GMUFAC`. Do not replace the whole method with IDEAL or silently preserve RK to obtain convergence.

After the trusted run, request the effective liquid and vapor models from the current native REP property-method/block sections and verify UNIFAC / IDEAL GAS for the task-relevant blocks. Include method and phase-model REP targets in the normal final readback transaction; the global option-set name, setter success, or separation targets alone do not prove the vapor overlay participated. Preserve conflicting REP evidence as a blocker (including local option-set overrides), export the checkpoint, and verify the overlay survives reload. If the helper or effective-model evidence is unavailable, report a capability boundary; do not invent an operation or declare task completion from a method label.

## Candidate Exploration

When the task does not name a fixed property method and the target results are
phase-equilibrium-sensitive, do not treat the first plausible method as settled.
Record a small candidate set and compare it with the same topology and operating
handles before final selection.

Use this as a generic pattern:

- Pick candidates from the component class and task wording, not from a previous
  case's numeric optimum.
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

` ` `python
pm = client.invoke("ensure_property_method",  method="NRTL")
if not pm.get("success"):
    raise RuntimeError(pm)
` ` `

or, when using raw operations:

` ` `python
pm = client.invoke("set_property_method", method="NRTL")
if not (pm.get("result") or {}).get("success"):
    raise RuntimeError(pm)
` ` `

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
`client.invoke("configure_srk_free_water_steamnbs")` for its registered local
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

` ` `text
\Data\Properties\Specifications\Input\GBASEOPSET
\Data\Properties\Specifications\Input\GOPSETNAME
` ` `

Report the method in final evidence when phase equilibrium, vapor/liquid split, column separation, flash composition, or reaction equilibrium results depend on it.

## Binary Interaction Parameters

When a task explicitly asks to check binary interaction parameters, call the
compact helper after components and the global property method are in place:

` ` `python
client.invoke("add_components_by_cas",  components=[...])
client.invoke("ensure_property_method",  method="NRTL")
bip = client.invoke("check_binary_interaction_parameters")
` ` `

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
- Either use the task's constant-alpha calculation as a separate analytic reference, or use a trusted Aspen base/standard model property method and state that the Aspen result is a property-package approximation.
- If scoring or validation is tied to a standard BKP/APW, prefer matching the standard model's property method over inventing a method from the case id.

## Block-Local Methods

This skill covers the global property method. If different blocks or cases must use different methods, also use `block-wise-property-methods` and verify each block's `OPSETNAME` independently.

` ` `

### FILE: aspen_agent_skills/guides/aspen-material-stream-composition-must-be-specified/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: aspen-material-stream-composition-must-be-specified
description: >-
  Choose MATERIAL stream state specs (TP/TV/PV) from task variables, set
  MASS-FLOW basis before kg/h component flows, and map Component Flow,
  Fraction, or Concentration must be specified to incomplete stream
  composition on Data\Streams\<StreamName>.
---

# Stream State Spec Selection

Use this skill when a task describes stream state with different variable combinations.

- When using the high-level helper, the signature is
  `safe.set_material_stream(client, *, stream_name, mixed_spec, basis,
  component_flows, flow_unit, temperature/pressure/vapor_fraction...)`. The
  `basis` keyword is mandatory. For molar component flows use
  `basis="MOLE-FLOW"` with `flow_unit="kmol/hr"`; for mass component flows use
  `basis="MASS-FLOW"` with an explicit mass unit such as `kg/hr`.
- **Task feed in kg/h (mass flow):** After components exist, set the MATERIAL stream mixed spec and state (`TP` / `TV` / `PV` as required), then call `set_basis_mixed(MASS-FLOW)` **before** component flow writes. Use `set_flow_mixed` with the task's numeric mass-flow rates, **canonical component IDs**, and an explicit mass-flow unit such as `unit="kg/hr"` (the tool normalizes exact `kg/h` input to `kg/hr`). Do **not** rely on `MASS-FLOW` basis alone and do **not** omit `unit` for component-flow values; the tool should reject flow-basis writes without a unit. Do **not** convert kg/h to kmol/h unless the only live tool path is truly molar-flow and you document the molecular-weight conversion.
- **Unit continuity:** Prefer the units stated in the task for stream flow setters and probe axes whenever the live tool accepts them. If the task gives `kg/hr`, keep `unit="kg/hr"` rather than switching to `kg/sec`, `lb/hr`, or `kmol/hr` unless there is a documented conversion reason and a `unit_reconciliation` entry. Always pass the `unit` keyword explicitly on component-flow setters.
- Choose the spec mode from the variables explicitly provided for each stream.
- Default mapping when the task wording is clear: `T + P -> TP`, `T + vapor fraction -> TV`, `P + vapor fraction or a defensible saturated-pressure statement -> PV`.
- Handle each stream independently if the task mixes different state-spec styles.
- Preserve independent feed partitions, component amounts and phase/state even at equal T/P: equal T/P does not imply thermodynamic equivalence. A summed-composition TP stream can flash differently and change total inlet enthalpy. Use verified shared material inlets or a real adiabatic Mixer carrying its computed outlet state, not a fresh TP reset. Any permitted feed aggregation requires current-run phase/enthalpy readbacks, explicit units/property scope, total enthalpy-flow and energy-balance evidence; otherwise retain the separate feeds.
- For MATERIAL stream object-level completion, set the chosen mixed spec first, then the minimum state fields for that mode, then the first accepted component flow.
- In the validated minimal probes, `TP` completion needed basis plus `TEMP` and `PRES`, while `TV` and `PV` completion both succeeded with basis plus one named state variable and one component flow; `set_vfrac_mixed` was not required in those probes.
- Treat `set_vfrac_mixed` as a good follow-up candidate for `TV` or `PV`, not as an automatic first-pass requirement, unless the task or Aspen evidence clearly promotes it.

## Completion diagnostics (Material streams)

If **Material Stream Config** / stream input completion or Next shows **`Component Flow, Fraction, or Concentration must be specified.`**, the **stream's composition/amount specification is incomplete** on **`Data\Streams\<StreamName>\Input\...`** (at least one of component flow, fraction, or concentration, consistent with the chosen basis). This is a **hard workflow gate**: the flowsheet will not advance until that stream is finished—fix the landed stream's basis + state + component-side specs before downstream blocks.

## Material stream completion messages

| Aspen message (typical) | Meaning | First fix |
| --- | --- | --- |
| `Component Flow, Fraction, or Concentration must be specified.` | Composition/flow side not closed for this MATERIAL stream. | On **`Data\Streams\<StreamName>`**, complete basis + (as required) total flow and component flow / fraction / concentration per the active spec; re-run `check_stream_completion` / workflow Next. |

## Task mass flow (kg/h) and `material_stream_variables`

When the problem statement gives **per-component flow rates in kg/h** (or otherwise clearly as **mass flow**):

1. Complete stream spec order for MATERIAL streams still applies: mixed spec mode first (`set_mixed_spec_mixed`), then basis, then intensive state for that mode, then flows.
2. Set **`set_basis_mixed(MASS-FLOW)`** so Aspen treats subsequent flow entries in a **mass-flow** sense for that stream.
3. Call **`set_flow_mixed`** once per component with the **numeric values from the task**, **canonical `component_name` IDs** from the live component table, and an explicit mass-flow unit such as `unit="kg/hr"` (or `unit="kg/h"`, normalized by the tool).

**Schema vs chemistry:** Inspecting `set_flow_mixed` should show `kg/hr` (and may show `kg/h`) in the `unit` enum. If a stale schema lists only molar or standard-volumetric units, refresh the tool surface or call the HTTP operation with explicit `unit="kg/hr"` if available; do **not** omit `unit` and rely on basis semantics. If the only safe path is truly molar flow, then document a **defensible kg/h → kmol/h** conversion using molecular weights and set **`MOLE-FLOW`** basis instead—do not guess.

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
  - `set_basis_mixed(MOLE-FLOW)` **or** `set_basis_mixed(MASS-FLOW)` when the task specifies mass flows (e.g. kg/h); match basis to the task's stated quantity type.
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

For common normal paraffins, use the established canonical IDs when the task names these compounds: propane `C3` (CAS 74-98-6), n-butane `NC4` (CAS 106-97-8), n-pentane `NC5` (CAS 109-66-0), and n-hexane `NC6` (CAS 110-54-3). In particular, after adding n-pentane as `NC5`, write stream composition with `component_name="NC5"`, not `N-PENTANE`. If the live table does not contain the intended ID, stop before composition writes and repair component landing; do not rely on runtime alias guessing.

` ` `

### FILE: aspen_agent_skills/guides/functional-role-semantics-validation/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: functional-role-semantics-validation
description: >-
  Validates process-functional roles before or during Aspen repair work. Covers
  hot/cold sides, feed/product intent, absorber/stripper direction, extract/raffinate
  meaning, and similar role semantics that topology or completion alone cannot prove.
  Use when a block or flowsheet can be wired and even run but still behaves against
  the intended process role, or when REP / PER_ERROR mentions energy-direction,
  wrong side, wrong product role, or other semantic conflicts.
---

# Functional Role Semantics Validation

## When this skill applies

Use this skill when Aspen work has moved beyond "does the node exist" and into
"does this object play the intended process role".

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

Stream IDs and local VAPOR/LIQUID constants are arbitrary, not role evidence. Bind quantities to `block -> native port -> connected stream -> same-run phase/vapor_fraction`; reconcile native BKP topology/stored phase results with trusted REP outlet declarations. Flash2 uses `F(IN)`, `V(OUT)` and `L(OUT)`; verify actual landing, never ordered outlet assignment. Discover Flash3/REquil family-native ports instead of inventing tokens. Names-only mismatches require consistent answer/target/formula remapping; task-bound or downstream physical mismatches require reconnection and rerun. Renaming is not physical repair. Missing/conflicting phase evidence remains unresolved. See `vapor-liquid-outlet-role-validation` for the dedicated readback contract.

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
   - absorber-like service should not be wired/spec'd like a stripper
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
- `WRONG SPEC OF HOT & COLD SIDES`
- top/bottom product or phase-role inconsistencies
- absorber / stripper configuration contradictions
- extraction products behaving opposite to the task wording
- repeated probe rows where the "target product" stream is consistently lean in
  the target component while another product stream is rich

The exact text is less important than the pattern: **the model can execute, but the configured role contradicts the intended process function**.

## Cross-family examples

- **MHeatX / HEATX**: hot/cold faces, branch ownership, heat-direction consistency
- **Paired Heater heat transfer**: separate hot-side and cold-side Heater blocks connected by one heat stream must prove both sides of the duty, not just one outlet state
- **RadFrac / absorber-like columns**: condenser/reboiler mode, top/bottom service, product-phase role
- **Extractors / separators**: which outlet is the actual target product versus the reject / secondary stream
- **Recycle or purge sections**: which stream is meant to return versus leave the system

### Paired Heater duty-balance consistency

For tasks that ask for "two Heater blocks with a heat stream transferring heat between the blocks", treat the heat stream as the shared contract between the blocks:

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
- If a warning sounds semantic, widen the search from "what variable is missing" to "what function is this object meant to serve".
- Use family-specific skills afterward for the concrete fix; this skill is the generic decision layer that tells the agent **where to look first**.

` ` `

### FILE: aspen_agent_skills/guides/aspen-generic-readbacks/SKILL.md
Reason: selected skill for task block family
` ` `text
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

` ` `python
summary = safe.finalize_task_summary_with_llm_rep_readback(
    summary,
    final_bundle=final,
    rep_readback_targets=targets,
    llm_rep_readback_artifact_dir=out / "artifacts",
)
` ` `

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

Store the list on `summary["rep_readback_targets"]` before collection.

## Quantity map (REP-readable)

| kind | quantity examples | notes |
|------|-------------------|-------|
| stream | `temperature`, `pressure`, `vapor_fraction`, `total_flow`, `component_flow` | component for flows/fractions |
| block | `heatx_area`, `heatx_duty`, `block_heat_duty`, `dstwu_theoretical_stages`, `dstwu_minimum_reflux`, `reflux_ratio`, `distillate_flow`, `reflux_flow`, `condenser_condensation` | block U-O-S / rating tables |
| profile | `profile_composition`, `radfrac_flow_profile`, `internal_liquid_vapor_ratio` | RadFrac MOLE-Y / MOLE-X and liquid/vapor flow profiles |
| derived | `conversion`, `reflux_plus_distillate`, `dstwu_reboiler_vaporization`, `internal_liquid_vapor_ratio`, DSTWU top-down feed plate | script records formula and raw REP inputs. DSTWU `NUMBER OF ACTUAL STAGES ABOVE FEED` is the rectifying-stage count. With the condenser as stage 1, the top-down feed plate is `1 + that number`. Do not subtract it from total stages and call the remainder the top-down plate. |

## DSTWU reboiler vaporization

DSTWU REP prints `REBOILER HEAT DUTY` and `ACTUAL REFLUX RATIO`. It does not print a line named boilup or 塔釜蒸发量. When the task asks for reboiler vaporization, boilup amount, or 塔釜蒸发量:

1. Read the distillate stream molar `TOTAL FLOW` and `ACTUAL REFLUX RATIO` from the same REP.
2. For a total condenser (`DISTILLATE VAPOR FRACTION` is 0), the constant-molal-overflow vaporization is `distillate_molar_flow * (1 + actual_reflux_ratio)`.
3. Store that as derived quantity `dstwu_reboiler_vaporization`, with the formula and the two raw request ids. Report the molar flow. Do not substitute reboiler duty for the vaporization amount.

## Example: HeatX + streams

` ` `python
targets = [
    {"request_id": "hx_area", "kind": "block", "object_name": "HX", "quantity": "heatx_area"},
    {"request_id": "hx_duty", "kind": "block", "object_name": "HX", "quantity": "heatx_duty"},
    {"request_id": "h2_out_temp", "kind": "stream", "object_name": "H2", "quantity": "temperature"},
]
safe.finalize_task_summary_with_llm_rep_readback(
    summary,
    final_bundle=final,
    rep_readback_targets=targets,
    llm_rep_readback_artifact_dir=out / "artifacts",
)
` ` `

## Example: conversion

` ` `python
{
    "request_id": "r1_bz_conv",
    "kind": "derived",
    "object_name": "R1",
    "quantity": "conversion",
    "reactant_component": "BZ",
    "inlet_stream": "F2",
    "outlet_stream": "P1",
}
` ` `

## Unit sets (setup only)

Custom unit sets use COM helpers during **setup** (`configure_custom_unit_set`, `read_active_unit_set`, `verify_custom_unit_set`). **INSET routing, METCBAR template default, bar-scale `set_pres`, and INSET-switch hazards** are in **`aspen-custom-unit-set`** (default-injected).

Common setup mistakes: `configure_inset_unit_system("METCBAR")` (use `activate_custom_unit_set`); task **bar** written as **MPa** (use `unit="bar"` — legal under any INSET). Re-read critical `PRES` after any INSET change.

Final displayed stream/block numbers for scoring use LLM REP readback after the trusted run. Derived metrics use those raw readbacks as inputs and must store the formula and source `request_id`s.

## RadFrac Operating Metrics

For final RadFrac/distillation scoring metrics, use LLM REP readback after the
selected replay run. Do not rely on stale probe-row direct reads or parse COM
diagnostics as final answers.

Recommended targets:

` ` `python
targets = [
    {"request_id": "c1_reflux_ratio", "kind": "block", "object_name": "C1", "quantity": "reflux_ratio"},
    {"request_id": "c1_reflux_flow", "kind": "block", "object_name": "C1", "quantity": "reflux_flow"},
    {"request_id": "c1_distillate_flow", "kind": "block", "object_name": "C1", "quantity": "distillate_flow"},
    {
        "request_id": "c1_internal_lv_basis",
        "kind": "profile",
        "object_name": "C1",
        "quantity": "internal_liquid_vapor_ratio",
        "basis_hint": "Use an internal stage/profile basis away from a total-condenser stage where vapor flow is zero.",
    },
    {
        "request_id": "c1_condenser_condensed_vapor",
        "kind": "derived",
        "object_name": "C1",
        "quantity": "reflux_plus_distillate",
        "basis_hint": "For a total condenser, total vapor condensed is reflux plus distillate/top liquid product on a common molar-flow unit basis.",
    },
]
` ` `

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

` ` `

### FILE: aspen_agent_skills/guides/reactor-reaction-setup-high-level/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: reactor-reaction-setup-high-level
description: >-
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
and `source_kind='external_given'` or `'native_component_property'`.
`verify_ryield_molecular_weights(...)` accepts explicit external reference MW
only after native identity is independently verified. Native property records
also need matching annotated `native_readback`. Use registered MW units
(`kg/kmol`, `g/mol`, `kg/mol`), not handwritten component constants. This
validates provenance and unit conversion, not an external source's accuracy.
An independent non-reacting property-only native run may supply
`source_kind='native_nonreactive_flow_ratio'` with annotated `mass_flow`,
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

` ` `python
from script_agent_exp import safe_aspen_calls as safe

rstoic_stoich = client.invoke("configure_rstoic_stoichiometry",
    block_name="R1",
    reaction_number=1,
    reactants={"TOLUENE": 1.0, "H2": 1.0},
    products={"BENZENE": 1.0, "METHANE": 1.0},
)
rstoic_conversion = client.invoke("configure_rstoic_fractional_conversions",
    block_name="R1",
    conversions=[
        {"reaction_number": 1, "component_id": "TOLUENE", "conversion": 0.75},
    ],
)
summary.setdefault("results", {})["rstoic_reaction_setup"] = {
    "stoichiometry": rstoic_stoich,
    "conversion": rstoic_conversion,
}
` ` `

Pass positive magnitudes in `reactants` and `products`; the helper handles Aspen's
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

` ` `python
rstoic_heat_ref = client.invoke("configure_rstoic_calculated_heat_reference",
    block_name="R1",
    rows=[
        {
            "reaction_number": 1,
            "reference_component_id": "TOLUENE",
            "reference_phase": "V",
        },
        {
            "reaction_number": 2,
            "reference_component_id": "BENZENE",
            "reference_phase": "V",
        },
    ],
    reference_temperature=298.15,
    reference_temperature_unit="K",
    reference_pressure=1.0,
    reference_pressure_unit="atm",
)
summary.setdefault("results", {})["rstoic_reaction_setup"]["heat_reference"] = rstoic_heat_ref
` ` `

For any reaction-mode switch that creates follow-through rows or table cells
(conversion component, stoichiometric coefficients, heat reference component,
rate basis, or phase basis), treat the write as complete only after the visible
table-facing path can read back both the component identity and the numeric/mode
cell. Hash-only component leaves or a successful wrapper response are not enough
when Next/completion still names the reaction sheet.

## REquil Pattern

` ` `python
from script_agent_exp import safe_aspen_calls as safe

requil_reactions = client.invoke("configure_requil_equilibrium_reactions",
    block_name="R1",
    nphase=2,
    spec_opt="TP",
    temperature=450.0,
    temperature_unit="F",
    pressure=1.0,
    pressure_unit="atm",
    reactions=[
        {
            "reaction_number": 1,
            "reactants": {"MEOH": 1.0},
            "products": {"CO": 1.0, "H2": 2.0},
            "delta": 0.0,
        },
        {
            "reaction_number": 2,
            "reactants": {"CO": 1.0, "H2O": 1.0},
            "products": {"CO2": 1.0, "H2": 1.0},
            "delta": 0.0,
        },
    ],
)
summary.setdefault("results", {})["requil_reaction_setup"] = requil_reactions
` ` `

After REquil reaction setup, keep the existing REquil skill's round-trip and
product-readback gates: completion must be trusted after BKP/reload evidence, and
product values must come from Aspen outlet/REP readbacks.

## RYield Complete Component-Yield Configuration Bundle

A `RYield` block needs an actual numeric component-yield table, not just operating
conditions. Configure and verify the following dependency bundle before running
or declaring input completeness. Iteration scheduling belongs to the runtime:
verified components and topology -> legal flash selector and its complete input
pair -> `set_user_yield=NO` -> one high-level yield helper call for every intended
non-inert product component -> per-row readback -> block completion and Next.
`NO` selects built-in Component yields; `YES/NO2/NO3` selects a user-subroutine
route and is not an "enable yield table" flag.

Use `client.invoke("configure_ryield_component_yield", block_name=..., component_id=...,
substream='MIXED', basis='MASS', mass_yield=..., mass_yield_unit='1')` for an
explicit mass ratio. Explicit task mass percentages are divided by 100 exactly
once. MASS yield is product mass/non-inert feed mass, not outlet mole fraction.
For MOLE supply `mole_yield`, `mole_yield_unit`, verified
`aspen_mole_yield_unit`, and `native_yield_unit_source`: its native basis is
product amount/non-inert feed mass, not product amount/total product amount.
Do not pass `kmol/hr` or `kg/hr` to either yield branch or normalize an outlet
molar ratio directly into native yield cells.

The helper owns materialization of the visible component row in **both**
`Data\Blocks\<block>\Input\BASIS` and
`Data\Blocks\<block>\Input\MOLE_YIELD`. The latter is the native table name
also when the row basis is MASS; do not invent a `MASS_YIELD` tree leaf.
Do not replace the helper with `COMP_LIST` labels, guessed `#component` leaves,
or `set_yield` (that sets the user subroutine name).

For each intended row require helper `success=True`, then verify
`basis_result.after` matches the requested basis and
`mole_yield_result.after` matches the helper's reconciled `yield_value_written`, with
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

` ` `

### FILE: aspen_agent_skills/guides/sequential-reaction-topology/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: sequential-reaction-topology
description: >-
  Counts Aspen reactor blocks from physical vessels in the task and figure, not
  from the number of reaction equations. Use when a task has a main reaction and
  a side reaction, series reactions inside one reactor, or more than one reactor
  vessel.
---

# Sequential Reaction Topology

## Core Rule

Count physical vessels, not reaction equations.

A vessel is a reactor the task names or the figure draws: "the reactor", "the first reactor", "the second reactor", or one reactor icon. Every equation the task places in that vessel is a `reaction_number` row on that one block. RStoic applies those rows in order. "The side reaction consumes a product of the main reaction" and "after the first reaction", when both belong to the same vessel, are the next row on that block. They are not a new block.

Create another reactor block only when the task or the figure shows another vessel. That is a second named reactor, a stream that leaves one reactor and enters the next, or a temperature and pressure the task assigns to a different reactor. Do not create one block per equation.

Do not add a heat stream because a reactor has a duty, a heat of reaction, or a quench temperature. Add a heat stream only when the figure shows a heat line or the task names a heat stream. A quench the task describes as a material stream stays a material stream.

## RStoic Pattern

Same vessel:

1. Create one RStoic for that vessel.
2. Write each reaction with `configure_rstoic_stoichiometry(..., reaction_number=N)` and the matching conversion row on that same block.
3. Set that block's temperature and pressure once.

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

` ` `

### FILE: aspen_agent_skills/guides/native-reactor-module-comparison/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: native-reactor-module-comparison
description: >-
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

` ` `python
from pathlib import Path

from script_agent_exp.script_runtime.rep_parser import load_rep
from script_agent_exp import safe_aspen_calls as safe


def sum_component_kmol_hr_from_rep(rep_path: Path, stream_ids: list[str], component_id: str) -> dict[str, object]:
    rep_text = load_rep(str(rep_path))
    tables = safe.extract_all_stream_tables_from_rep_text(rep_text)
    component = component_id.strip().upper()
    total_kmol_s = 0.0
    contributing: dict[str, float] = {}
    for stream_id in stream_ids:
        row = tables.get(stream_id.strip().upper())
        if not row:
            continue
        value = (row.get("components_kmol_s") or {}).get(component)
        if value is None:
            continue
        contributing[stream_id.strip().upper()] = float(value)
        total_kmol_s += float(value)
    return {
        "success": bool(contributing),
        "component_id": component,
        "stream_ids": [stream_id.strip().upper() for stream_id in stream_ids],
        "components_kmol_s": contributing,
        "total_kmol_s": total_kmol_s if contributing else None,
        "total_kmol_hr": total_kmol_s * 3600.0 if contributing else None,
        "source": "current-run REP stream table component flow",
    }


requil_h2 = sum_component_kmol_hr_from_rep(rep_path, ["V1", "L1"], "H2")
rgibbs_h2 = sum_component_kmol_hr_from_rep(rep_path, ["V2"], "H2")

summary["results"]["product_h2_kmol_hr"] = requil_h2["total_kmol_hr"]
summary["results"]["product_hydrogen_kmol_hr"] = requil_h2["total_kmol_hr"]
summary["results"]["requil_product_h2_readback"] = requil_h2
summary["results"]["rgibbs_product_h2_readback"] = rgibbs_h2
summary["results"]["result_source"] = (
    "H2 product flow is summed from current-run Aspen REP outlet stream tables; "
    "REquil uses both material outlets V1 and L1, RGibbs uses V2."
)
` ` `

Use the exact keys `product_h2_kmol_hr` or `product_hydrogen_kmol_hr` for the primary product-component result. Human-friendly variants such as `hydrogen_product_kmol_hr` or generic `product_component_kmol_hr` are useful supporting evidence, but they may not satisfy generic product-component validation by themselves.

## Module-Specific Inputs

- RStoic conversion values must match the task.
- For RStoic, put conversion evidence in a structured summary key, not only in prose. A good shape is:
  `results.rstoic_conversion_evidence = [{"block_name": "R1", "reaction_number": 1, "key_component": "TOLUENE", "conversion_fraction": 0.75, "source": "configure_rstoic_fractional_conversions/readback"}]`.
- When using `configure_rstoic_fractional_conversions(...)`, preserve its returned `rows[*].conversion`, `rows[*].component_id`, and `rows[*].readback` in the final summary so validator/scorer can identify the native conversion setting.
- RPlug geometry such as length and diameter must be configured and evidenced.
- RCSTR volume must be configured and evidenced.
- If a property-method warning is accepted as a narrow PER_ERROR exception,
  record raw and effective status; otherwise do not change the task's property
  method merely to make the scalar status clean.

` ` `

### FILE: aspen_agent_skills/guides/flash-control-chain/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: flash-control-chain
description: Handle flash tasks by choosing topology from real phase structure, locking SPEC_OPT first, using compatible mode pairs, and using heat-coupled modes such as TQ when heat duty should participate in vaporization or product composition.
---

# Flash Control Chain

- Choose topology from the real phase structure: `Flash2`, `Flash3`, `Mixer`, and `Dupl` have different jobs.
- **Independent-feed energy boundary:** Preserve each task-specified feed's composition, amount, T/P, and phase/state independently. Equal feed temperature and pressure do **not** make a summed-composition `TP` stream thermodynamically equivalent: phase equilibrium and nonideal mixing enthalpy depend on composition. A fresh combined `TP` stream can change total inlet enthalpy and therefore an adiabatic flash result.
- Inspect `list_block_ports` before wiring multiple feeds; a single material inlet can be a shared collection, not a one-stream limit. Use verified collection connections or an upstream adiabatic `Mixer`, preserving all independent inlet states; never invent numbered ports or replace the mixer outlet with a specified total-flow `TP` feed.
- For property-method comparisons, keep feed partition/state identical across branches and verify each branch's property scope; if upstream mixers are used, verify their method basis too. Before trusting outputs, record live feed ownership plus current-run inlet phase/enthalpy evidence and energy-balance closure. Convergence and summed component balances alone do not prove feed-state fidelity.
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
- With an inlet heat stream, temperature-family routes such as `TQ`, `TV`, and `TD` mean "write `TEMP` only". Do **not** write `PRES`, `DUTY`, or `VFRAC` after selecting one of these routes; Aspen may accept the setter call but export/read back an inconsistent `SPEC-OPT=TQ` plus residual pressure state.
- With an inlet heat stream, pressure-family routes such as `PQ` and `PV` mean "write `PRES` only". Do **not** write `TEMP`, `DUTY`, or `VFRAC` after selecting one of these routes; temperature/vapor fraction become responses.
- The same rule applies even if a wrapper says `set_pres(...)` succeeded. For heat-stream-fed `Flash2`, successful dependent setters are not enough; the script must preserve the one-variable route semantics before run/export.
- If a task fixes effect temperatures in an evaporator cascade, use `TQ`, write only `TEMP`, and let pressure/composition be response variables. If the task fixes pressure instead, use a pressure-family route and write only `PRES`.
- If a heat-driven evaporator fails in one fixed-variable route, probe the other block variable, especially a small temperature or pressure bracket, before declaring the heat cascade infeasible.
- **Idle manipulated variable diagnostic:** If changing heat duty, steam flow, or heat-stream inputs does not move product composition while affected Flash2 blocks still read back as `TP`, treat this as a model-fidelity / route mistake first. Re-read `SPEC_OPT` and replan onto a heat-coupled flash route before concluding the task has no solution.
- If material split readbacks look physically right but run status or `PER_ERROR` is still bad, keep the run-status/setup-state problem visible. Do not "repair" by changing the reported split until you have checked completion, `SPEC_OPT`, unit basis, and current REP/export trust.
- Use REP stream evidence to confirm outlet phases, interstage connections, and property-method comparisons.

## Vapor/liquid ownership proof

Stream IDs are arbitrary. After connecting, verify `F(IN)` and actual `V(OUT)`/`L(OUT)` connected streams, then match same-run REP outlet declarations and stream PHASE/vapor_fraction before reporting compositions. A successful helper or inherited BKP stream order is not role proof. Names-only mismatches need consistent answer/target/formula mapping; task-bound or downstream physical mismatches require reconnection and rerun, not renaming. For Flash3/REquil discover family-native phase ports; do not assume Flash2 tokens. See `vapor-liquid-outlet-role-validation`.

## Compatible pairs

- Plain `TP` => `TEMP` + `PRES` only when no inlet heat-stream limitation is active; with inlet heat stream, `TP` is invalid and must be rejected.
- `PV` => `PRES` + `VFRAC` only when no inlet heat-stream limitation is active; with inlet heat stream, `PV` is a pressure route and only `PRES` should be written.
- `PD` => `PRES` + `DUTY`
- `TQ` => `TEMP` + heat-stream participation; write only `TEMP` on heat-stream-fed `Flash2`.
- `PQ` => `PRES` + heat-stream participation; write only `PRES` on heat-stream-fed `Flash2`.

## Aspen HTTP setter order for TQ

` ` `python
client.invoke("set_spec_opt", block_name="A1", value="TQ")
client.invoke("set_temp", block_name="A1", value=50.0, unit="C")
# verify readback on SPEC_OPT and TEMP before run/export
` ` `

Connecting a heat stream is topology only; it does not replace block-side `SPEC_OPT=TQ` or prove duty participation.

## Bar-scale pressure on `set_pres` (Flash2 / near-atmospheric flash)

When task text or standard meta gives **bar-scale** flash pressure (e.g. `PRES = -0.05 bar`), write it with an explicit **`unit="bar"`** on `set_pres`. This is **legal under any INSET** (SI/ENG/MET/METCBAR).

` ` `python
client.invoke("set_spec_opt", block_name="F", value="TP")
client.invoke("set_temp", block_name="F", value=50.0, unit="C")
client.invoke("set_pres", block_name="F", value=-0.05, unit="bar")
` ` `

Rules:

- **`bar` / `bara` / `barg`** are accepted setter units — see block-type inject `flash2.md` / `rstoic.md` and `aspen-custom-unit-set`.
- Do **not** convert bar-scale numbers to **`MPa`** unless the task truly specifies MPa.
- With **absolute** bar units, a **negative** `PRES` means **pressure drop** (Aspen Flash help), not “set MPa outlet pressure”.
- After `set_pres`, verify `SPEC_OPT` + numeric readback; display unit on readback may differ from the write token.
- If the flowsheet also uses **SI-only equipment tables** (pump curves, etc.), prefer **`INSET=SI` + `unit="bar"`** on flash pressure — do not write bar under METCBAR then switch INSET mid-build (rescales stored `PRES`). See `aspen-custom-unit-set`.

Live probe: `python tool_side_generation/healthcheck/bar_pressure_write_probe.py`


` ` `

### FILE: aspen_agent_skills/guides/prefer-direct-component-splits/SKILL.md
Reason: selected skill for task block family
` ` `text
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

- component `H2` -> outlet A
- component `NC7` -> outlet B
- component `TOLUENE` -> outlet B

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

` ` `

### FILE: aspen_agent_skills/guides/shared-material-port-topology/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: shared-material-port-topology
description: Handles Aspen blocks that expose shared material collection ports. Use when a Mixer, FSplit, reactor, or other block seems to have too few material ports, when agents are tempted to invent numbered ports, or when recycle/product branches are being kept only as aliases instead of physical connections.
---

# Shared Material Port Topology

## Core Rule
Some Aspen blocks expose one collection port for many material streams. A single live port can accept multiple streams through `Elements.Add(...)`.

Do not assume "one process branch = one visible port".

## Common Cases
- Mixer-like blocks may expose one shared `F(IN)` and one `P(OUT)`. Connect every material feed to `F(IN)`, then connect the mixed product to `P(OUT)`.
- A connected Mixer may still need a minimal input paragraph before export/run.
  If history says `BLOCK: "M1" APPEARS IN THE FLOWSHEET, BUT NO BLOCK
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

` ` `python
runtime.stage(
    "C1_ports_before_connect",
    lambda: client.invoke(
        "list_block_ports",
        block_name="C1",
    ),
    required=False,
)

runtime.stage(
    "connect_C1",
    lambda: client.invoke(
        "connect_material_inlet_outlet",
        block_name="C1",
        inlet_stream="F1",
        outlet_stream="P1",
    ),
    required=True,
)

runtime.stage(
    "C1_ports_after_connect",
    lambda: client.invoke(
        "list_block_ports",
        block_name="C1",
    ),
    required=False,
)
` ` `

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
- Marking a required stream as "logical only" or "retained in name mapping" after failing to connect it physically.

` ` `

### FILE: aspen_agent_skills/guides/radfrac-absorber-like-configuration/SKILL.md
Reason: selected skill for task block family
` ` `text
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
   (`Data\Blocks\<BLK>\Input\BASIS_D`) with the task molar-flow unit. Use
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
| `TOTAL` | only top vapor product on `VD(OUT)` | `BASIS_RR` + `BASIS_D` | Fails: `"RDV" IS LESS THAN 1. A LIQUID DISTILLATE STREAM IS NEEDED BUT NOT SPECIFIED.` |
| `PARTIAL-V` | top vapor product on `VD(OUT)`, bottoms on `B(OUT)` | `BASIS_RR` + `BASIS_D` when the visible row is ordinary `Distillate rate`; also valid with `BASIS_RDV` + `BASIS_RR` + `BASIS_B` when vapor-distillate fraction is explicitly intended | `PER_ERROR=0` |
| `PARTIAL-V` | only top liquid product on `LD(OUT)` | any ordinary distillate-rate setup | Fails: `"RDV" IS GREATER THAN 0. A VAPOR DISTILLATE STREAM IS NEEDED BUT NOT SPECIFIED.` |
| `PARTIAL-V-L` | both `VD(OUT)` and `LD(OUT)` connected | `BASIS_RDV` + `BASIS_RR` + `BASIS_B` | `PER_ERROR=0` |
| `PARTIAL-V-L` | only `LD(OUT)` with `RDV=0` | `BASIS_RDV=0` + `BASIS_RR` + `BASIS_D` | `PER_ERROR=0`, but prefer `TOTAL` for true liquid-only service |
| `PARTIAL-V-L` | only `VD(OUT)` with `RDV=1` | `BASIS_RDV=1` + `BASIS_RR` + `BASIS_B` | `PER_ERROR=0`, but prefer `PARTIAL-V`/`NONE` for true vapor-only service |
| `PARTIAL-V-L` | any top-port arrangement without `BASIS_RDV` | `BASIS_RR` + `BASIS_D`, or stream `PROD_FLOW` alone | Fails: `"T1" OR "RDV" NEEDS TO BE SPECIFIED.` |
| `NONE` with reboiler | top vapor product on `VD(OUT)`, bottoms on `B(OUT)`, feed or pumparound enters stage 1 | Bottoms/boilup-style handles such as `BASIS_B`; no condenser reflux/distillate semantics | `PER_ERROR=0` in the probe with top-stage feed |
| `NONE` with reboiler | only top liquid product on `LD(OUT)` | bottoms/boilup-style handles | Fails: `"RDV" IS GREATER THAN 0. A VAPOR DISTILLATE STREAM IS NEEDED BUT NOT SPECIFIED.` |
| `NONE` with reboiler | `VD(OUT)` but no feed/pumparound to top stage when `Q1=0` | bottoms/boilup-style handles | Fails: `WHEN "Q1=0"... THERE MUST BE A FEED/PUMPAROUND ENTERING THE TOP STAGE.` |

Do not collapse this map to "`Condenser=None` or `PARTIAL-V` means `VD(OUT)`".
`PARTIAL-V-L` is governed by `RDV`; `RDV=0` and `RDV=1` are legal boundary
cases, while mixed vapor-liquid service needs both top ports and an explicit
`BASIS_RDV`. `NONE` also has an independent top-stage feed/pumparound
requirement when condenser duty is zero.

## Bottom Vapor Feed Pattern
For tasks that say a saturated vapor feed enters at or near the bottom of a RadFrac column:

1. Put the feed on the intended bottom-side stage, often `NSTAGE`.
2. Set feed convention explicitly with `FEED_CONVEN/<stream>` and `FEED_CONVE2/<stream>` as `ON-STAGE-VAP`.
3. Align feed pressure with the column pressure profile. If using pressure drop, set `OPT_PRES=DP-COL` and `DP_COL`, then choose feed pressure consistent with the feed stage.
4. Choose one distillate operating spec: material-balance molar flow (`BASIS_D`) **or** distillate/feed ratio (`D:F`), never both. Writing these numeric leaves can change the active `COL-SPECS` selection; `D:F` is not a harmless annotation after `BASIS_RR + BASIS_D`. In `configure_radfrac_bottom_vapor_feed`, explicit `distillate_flow` takes precedence when both arguments are present; `d_over_f` is recorded as inactive evidence, not sent to Aspen. Use only `d_over_f` to request the ratio route. The helper preserves the existing end-effect -> stage/pressure -> feed convention -> reflux -> selected draw write order; it does not clear old specs on an inherited column. Verify active UI/COL-SPECS rows before switching an inherited basis, and do not invent selector paths.
5. If the REP says `COLUMN DRIES UP OR COLUMN FLOWS VIOLATE BUILT-IN LIMITS`, re-check feed convention, pressure profile, product draw basis, stage count, and product outlet roles before changing solver tolerances.

In generated hardcoded scripts, prefer `configure_radfrac_bottom_vapor_feed(...)`
from `runtime/script_agent_experiment/script_agent_exp/safe_aspen_calls/`
when this pattern applies. The runtime parent owns canonical import roots;
generated scripts must not modify `sys.path` or scan legacy experiments paths.

## End-Mode-Aware Operating Specification Budget

`TOTAL/NONE` is not an ordinary two-numerical-spec distillation column. Aspen counts `Reboiler=None` as an operating specification, so only one additional numerical operating spec remains. `BASIS_RR + BASIS_D` can therefore be overspecified even when no `D:F` setter exists. Keep the requested `NONE`; do not introduce a kettle reboiler to make the pair fit. With reflux ratio as the chosen handle, a material-balance distillate estimate belongs in diagnostic/target evidence, not another setter.

Use `configure_radfrac_operating_spec_bundle(..., condenser="TOTAL", reboiler="NONE", reflux_ratio=...)` after end effects and feed conventions are landed. The bottom-vapor-feed helper delegates to this bundle; explicit flow still precedes ratio for the ordinary `TOTAL/KETTLE` case. In `TOTAL/NONE`, reflux takes precedence over supplied draw estimates; the unused values and reason are recorded explicitly. The total-condenser helper accepts `reboiler="NONE"` rather than forcing its default kettle representation. No helper clears inherited specs or writes a guessed selector. Setter rejection remains fatal. Inspect the actual `COL-SPECS` table, end-mode readback, completion and current-run evidence: populated numeric leaves alone do not prove active specification membership. `BASIS_RDV=0` in a total-condenser backup is a product-phase condition, not proof of an extra independent operating spec. For inherited or utility-exchanger configurations, live active rows remain authoritative. `COL-SPECS` is a serialized BKP/UI section and is not necessarily an Aspen tree node: a failed tree-table lookup must remain visible rather than trigger guessed selector paths. `collect_radfrac_operating_spec_state` records native numerical-leaf values and `node_props` prompts, end modes and completion. In verified `TOTAL/NONE` readback, the draw-leaf prompt explicitly states that only one Operating Specification is allowed; RR is populated while the unselected draw leaves remain unset. Combine this with same-session exported BKP `COL-SPECS`, setter rejection and run evidence; do not label it as a successful GUI active-row table readback.

## No-Condenser / No-Reboiler Absorbers

When the task explicitly says `Condenser=None` and `Reboiler=None`, preserve that process intent. Do not silently change the model to `PARTIAL-V` plus `KETTLE` just to make completion easier; that turns an absorber into a distillation surrogate and can converge to the wrong product semantics. A generated script that records `PARTIAL-V`/`KETTLE` as a "runnable representation" for this kind of task should remain failing until the no-condenser/no-reboiler configuration has been repaired.

Do not infer `Reboiler=None` from "no condenser" alone. If only the condenser is absent and the task gives a bottom-product temperature target, keep `Condenser=None` but allow a real reboiler or bottom operating specification. A cold-feed column with both `Condenser=None` and `Reboiler=None` may be physically unable to reach a warm bottoms-temperature target by varying solvent flow, vapor draw, or a bottom vapor stub.

For no-condenser absorber-like tasks with cold feeds, a warm bottoms-temperature target, and a requested top vapor product flow/composition, use `radfrac-no-condenser-reboiled-bottoms` instead of this no-reboiler repair pattern unless the task explicitly says no reboiler. The required settings are `Condenser=None`, `Reboiler=KETTLE`, `ABSORBER=NO`, a true overhead vapor outlet stream, a bottoms stream, and a bottom energy/spec handle such as boilup ratio or reboiler duty for the Design Spec. Do not set `ABSORBER=YES`, do not use a near-top side draw as the only vapor outlet, and do not vary the top vapor stream flow to satisfy a bottoms-temperature target.

For no-reboiler RadFrac absorbers, Aspen may require a bottom-side vapor/on-stage feed convention even when the physical bulk feed belongs on an upper stage. Use this repair order before changing condenser/reboiler mode:

1. Keep the absorbent as an on-stage liquid feed at its stated upper stage.
2. Keep the main gas feed at the stated stage, and explicitly set `FEED_CONVEN/<stream>` and `FEED_CONVE2/<stream>` to vapor/on-stage tokens such as `ON-STAGE-VAP`.
3. If Aspen still needs bottom-stage vapor traffic for `Reboiler=None`, split a small documented fraction of the gas feed to a separate Aspen-safe stream on stage `NSTAGE`; preserve total feed composition and flow across the main and bottom-stub streams.
4. Set the bottom-stub feed convention with `FEED_CONVEN` / `FEED_CONVE2` as `ON-STAGE-VAP`.
5. For top gas products, use the true top vapor outlet where possible. If Aspen forbids writing product flow on a top/bottom outlet, use a documented near-top vapor side draw only for the initial product-flow guess, and report the actual top-gas evidence from REP/readbacks.

In generated scripts, prefer `configure_radfrac_no_condenser_absorber(...)` from `script_agent_exp.safe_aspen_calls` for the end effects, feed-stage rows, and feed-convention writes. It keeps `Condenser=None` and `Reboiler=None` instead of drifting to `PARTIAL-V`/`KETTLE`.

If a repeated helper call reports `Variable CONDENSER not found` or `Variable REBOILER not found` after an earlier successful `NONE` write in the same session, treat this as a possible Aspen option-tree/idempotency collapse, not as permission to skip condenser/reboiler setup. Keep using `configure_radfrac_no_condenser_absorber(...)`; the helper should record structured idempotent evidence only when a prior accepted write or readback proves the target no-condenser/no-reboiler mode. A first-attempt missing node without prior evidence remains a blocker.

### `set_dp_col` requires a pressure unit

The HTTP/MCP `set_dp_col` operation **always** requires `unit` (e.g. `atm`, `kPa`,
`bar`, `mmHg`). Calling `set_dp_col(block_name="C1", value=0.0)` without `unit`
fails at the server with `missing 1 required positional argument: 'unit'`.

- Prefer `configure_radfrac_no_condenser_absorber(..., column_dp=0.0, pressure_unit="atm")` — the helper passes `unit=pressure_unit` (or `column_dp_unit`) automatically.
- If writing `set_dp_col` directly: `set_dp_col(block_name="C1", value=0.0, unit="atm")`.
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

` ` `

### FILE: aspen_agent_skills/guides/radfrac-standard-column-pressure-basis/SKILL.md
Reason: selected skill for task block family
` ` `text
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

Examples for "1 atm column, 1 psi pressure drop":

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

- Write `Data\Blocks\<BLK>\Input\BASIS_D`, e.g.
  `Application.Tree.FindNode("\Data\Blocks\D1\Input\BASIS_D")`.
- Use the task's molar-flow unit for the visible `Distillate rate` row; for
  kmol/h tasks the value belongs on `BASIS_D` with a compatible kmol/time unit.
- Do not route this GUI combination to `BASIS_RDV` / `set_basis_rdv` or to a
  fractional `D:F` surface unless the task or live UI explicitly changes the
  operating-spec row away from `Distillate rate`.

Read back `BASIS_RR` and `BASIS_D` before trusting the column setup; a blank
`BASIS_D` under this spec pair means the column operating specs are incomplete.

## Partial-Condenser Temperature

For RadFrac partial condensers, Aspen's required condenser-temperature input is
the `T1` node, not PetroFrac-style `T_COND`. If history says `"T1" OR "RDV"
NEEDS TO BE SPECIFIED`, use the RadFrac `set_t1` operation, or the compatibility
alias `set_t_cond` which writes `Data\Blocks\<BLK>\Input\T1`.

Do not spend repair time searching for `OPT_COND` / `T_COND` under RadFrac unless
live UI evidence proves that this specific case exposes those nodes. A
`PARTIAL-V-L` RadFrac can satisfy the translator with `T1=<temperature>` plus the
normal operating specs, or with `BASIS_RDV` when a vapor-fraction spec is intended.

## Native RadFrac Pressure Modes

Do not flatten every RadFrac pressure-drop task into explicit top/bottom endpoint
pressures. Some validated Aspen files use RadFrac's native pressure-option modes,
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

- `Data\Blocks\<BLK>\Input\OPT_PRES_TOP` selects the top-of-column pressure
  option. `STAGE-2` pairs with `Data\Blocks\<BLK>\Input\PRES2`; `DP-COND`
  pairs with `Data\Blocks\<BLK>\Input\DP_COND`.
- `Data\Blocks\<BLK>\Input\OPT_PRES` selects the pressure-drop option for the
  rest of the column. `DP-STAGE` pairs with
  `Data\Blocks\<BLK>\Input\DP_STAGE`; `DP-COL` pairs with
  `Data\Blocks\<BLK>\Input\DP_COL`.
- Unit-bearing pressure leaves must be written through unit-aware setters or
  COM unit APIs. A raw `typed helper write surface` write is suitable for enum leaves such as
  `OPT_PRES_TOP`, but not sufficient when the value's unit must be selected on
  the same Aspen node.
- For a per-stage pressure-drop task, the usual direct expression is
  `OPT_PRES_TOP=STAGE-2`, `PRES2=PRES1 + deltaP_per_stage`,
  `OPT_PRES=DP-STAGE`, and `DP_STAGE=deltaP_per_stage`, followed by REP
  pressure-profile verification.

Treat reference BKP pressure settings as evidence for the current task only, not
as reusable global rules. If a reference file uses a native RadFrac pressure mode,
mirror the mode and verify the resulting pressure profile; do not record the
case name, task number, or benchmark-specific numeric pattern in this skill.

For ordinary new tasks that only say "column at `P` with pressure drop `deltaP`"
and give no reference BKP or native mode, keep the default top-anchored basis:
`P_bottom = P_top + deltaP`.

Required final evidence:

- Read back or REP evidence for top and bottom pressures in one unit basis.
- When using generated scripts, `set_pres2` is the curated operation for direct
  `Data\Blocks\<BLK>\Input\PRES2` writes. The safe helper
  `configure_radfrac_total_condenser(..., bottom_pressure=...,
  bottom_pressure_mode="pres2")` preserves explicit `PRES2`; its default
  `bottom_pressure_mode="dp_col"` keeps legacy pressure-drop behavior.
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
with that stage's pressure.

## Total-condenser helper signature

`configure_radfrac_total_condenser` uses `pressure_unit=` for pressures and `distillate_flow_unit=` for the product-rate specification. Do not pass a generic `unit=` keyword. The helper owns family-specific `set_pres1`/`set_pres2`/`set_dp_col` and `set_basis_d` routing.

## Exact direct feed-stage signature

For a RadFrac feed that is not already owned by a standard high-level column bundle, use exactly:

` ` `python
client.invoke("set_radfrac_feed_stage", block_name="D1", stream_name="F1", value=20)
` ` `

`set_radfrac_feed_stage` accepts `block_name`, `stream_name`, and `value`. Never pass `stage=`, `stage_number=`, or `feed_stage=` to this capability. `feed_stage=` belongs to high-level helpers such as `configure_radfrac_total_condenser`, which translate it internally to `value`.

` ` `

### FILE: aspen_agent_skills/guides/aspen-completion-error-hints/SKILL.md
Reason: selected skill for task block family
` ` `text
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

Global `PER_ERROR` is a run-health signal, not proof that the task's manipulated
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
Prefer `client.invoke("configure_srk_free_water_steamnbs")`; compatible execute
shares the registry, and typed safe helpers remain client-first direct-payload
calls. Invoke supplies the client and returns a status/result envelope. Never
retry missing helpers or local errors through native transport.
Call it proactively after successful `ensure_property_method(..., method="SRK")`.
Require setter success plus
`\Data\Properties\Specifications\Input\GFREE_WATER=STEAMNBS` readback.
`FREE_WATER` is not the writable global surface; direct writes return
`AE_UNDERSPEC`. Preserve exact setter failure and actual returned live options;
never invent missing fields/tokens or waive failure because an old value matches.

Raw nonzero SRK `PER_ERROR` remains blocking even with a historical service's
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
| `Invalid symbol value` for a property method | Use one exact token from the setter's `suggested_methods` / `available_methods`; do not write `GBASEOPSET` directly with the rejected alias. |
| repeated 300s timeouts after a token rejection | Stop the loop and repair the token first; do not interpret the timeout series as physical property infeasibility. |

Evidence after repair: setter response `success: true`, readback of
`\Data\Properties\Specifications\Input\GBASEOPSET` or `...\GOPSETNAME`, and the
chosen token recorded in `summary.json`.

## Pressure / unit basis: semantic setter error (Class B)

These patterns often trace to **wrong `unit=` on a pressure setter**, not to â€œAspen cannot use barâ€ or a missing custom INSET:

| Symptom | Likely mistake | Repair |
|---|---|---|
| Flash/RStoic runs but V/L split wrong; column feed composition off | Task/meta **bar** written as **`MPa`** (e.g. `-0.05 bar` â†’ `2.15 MPa`) | `set_pres(..., unit="bar")` with task numeric value |
| Tree `PRES` readback orders of magnitude wrong after INSET change | Wrote bar under METCBAR, then switched global **`INSET` to SI** mid-build | Re-write bar pressures after SI switch, or use **SI + `unit="bar"`** throughout â€” see `aspen-custom-unit-set` |
| Pump `DELTA P` / outlet pressure ~1e18; downstream **ZERO FEED** | Pump curve / table validated under **SI** while session stayed on another INSET | Force coherent INSET for equipment tables; re-read upstream `PRES` |

**`set_pres(..., unit="bar")` is legal under SI/ENG/MET/METCBAR.** Do not â€œfixâ€ bar tasks by forcing METCBAR unless the task is about display INSET.

Load **`aspen-custom-unit-set`** for INSET routing, template default, and live probes.

## Mixer: `input_incomplete`

If a `MIXER` block remains `input_incomplete` while topology and feeds look connected, suspect missing mixer pressure before rebuilding streams.

Repair hint:

- Write `set_pres(block_name=<MIXER>, value=<pressure>, unit=<unit>)` using the intended outlet/downstream pressure basis.
- Then rerun `check_block_completion(<MIXER>)`.
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

` ` `text
INLET/OUTLET PHASES ARE NOT IN EQUILIBRIUM
COMPONENT '<id>' IN STREAM '<stream>' IS NOT IN PHASE EQUILIBRIUM
RELATIVE ERROR IN VL FUGACITY ...
` ` `

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
2. Verify the named stream's live owner and physical port role. For a column,
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
`0.0 < LBC < 0.5*TUBE-LENGTH`, or inlet/outlet baffle-spacing bounds are detailed
HeatX geometry input errors, not convergence failures.

Repair hint:

- Prefer `configure_heatx_detailed_shell_tube_rating(...)` so geometry is written
  as a coherent bundle.
- Enforce tube length greater than baffled flow length; mid spacing strictly below
  half the tube length; inlet and outlet spacing each within Aspen's reported
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
- `"COLD" stream is hotter than "HOT" stream`
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

` ` `python
client.invoke(
    "configure_recycle_convergence_options",
    tolerance=1e-5,
    tear_method="WEGSTEIN",
    wegstein_max_iterations=300,
)
` ` `

The helper writes Aspen global `Data\Convergence\Conv-Options` fields, including `TEAR_METHOD` and `WEG_MAXIT`, then calls `read_recycle_convergence_setup`. Treat the repair as applied only when setter operations succeed and readback shows the requested values. `wegstein_max_iterations` is the legal keyword; `max_iterations` is not. Do not confuse automatic block `Input\MAXIT` raising with tear-solver convergence settings.

Preserve the process topology and task-fixed operating specifications while changing only convergence controls. After readback, rerun once and require current-run `PER_ERROR=0`, convergence-block normal completion, and disappearance of any downstream mass-balance symptom before trusting results. If method/readback evidence says the active solver is not WEGSTEIN, stop or use an explicitly supported method; do not write WEGSTEIN-only fields blindly.

## RadFrac: No Condenser / No Reboiler Feed Completion

For absorber-like `RadFrac` with `CONDENSER=NONE` and `REBOILER=NONE`, these Aspen messages map to feed-stage and feed-convention repair:

- `FEEDS not complete: SID = <stream>`
- `Stage must be specified.`
- `A feed or pumparound stream to the top stage must be specified when Condenser=None or condenser duty is zero.`
- `A feed or pumparound stream to the bottom stage must be specified when Reboiler=None or reboiler duty is zero.`
- Next-gate text such as `Feed to the Bottom Stage must be specified when Reboiler=None`.

Repair hint:

- Prefer `configure_radfrac_no_condenser_absorber(...)`.
- Provide both `feed_stages` and `feed_conventions`.
- Use `set_pres1(...)` for the top/stage-1 pressure before final completion.
- Gas feeds near the bottom usually need `ON-STAGE-VAP`; liquid absorbent feeds near the top usually need `ON-STAGE-LIQ`.
- Write both `Data\Blocks\<BLK>\Input\FEED_CONVEN\<stream>` and `Data\Blocks\<BLK>\Input\FEED_CONVE2\<stream>` when not using the helper.
- Do not guess table paths like `Data\Blocks\<BLK>\Input\FEEDS\<stream>\STAGE`; use `set_feed_stage(...)` or verified live paths.
- Also load `aspen_agent_skills/guides/radfrac-absorber-like-configuration/SKILL.md` for bottom-stub and product-outlet semantics.

Only tune reflux, boilup, product flows, or convergence methods after the no-condenser/no-reboiler feed completion messages are gone.

## PetroFrac: Pseudo Streams Page (`PSEUDO-STR`)

When Next or flowsheet completion reports:

- `PSEUDO-STR not complete: STREAM = <name> Stage must be specified.`
- Multiple streams in one message, e.g. `STREAM = PA1 ... STREAM = PA2 ...`

Repair hint:

- The stream `<name>` is a **pseudo-side stream** on PetroFrac block `<blk>`, not an ordinary product stream.
- Extract **all** `STREAM = <name>` entries from the same Next message and repair every one; completion is not cleared until every listed pseudo stream has its token-specific required fields.
- Classify pseudo ownership first. For `PA`, call `set_petrofrac_pumparound_specs`; for `STRIPPER`, call `set_petrofrac_side_stripper_specs`; for true `MAINCOL`, call `set_petrofrac_pseudo_stream(block_name=<blk>, stream_name=<name>, pseudo_kind='MAINCOL', stage=<tray>, phase='L'|'V'|'TV'|'TL', app=app)`.
- Compatible fields are branch-specific: `MAINCOL` writes `PS2_STAGE` + `PS2_PHASE`; `PA` writes `PS2_PANO` + `PS2_STATE`; `STRIPPER` writes `PS2_STRNO` + `PS2_SOURCE` + `PS2_S_STAGE` + `PS2_S_PHASE` + `PS2_S_STATE`.
- Option lists: `OPT_PSEUDO` â†’ `MAINCOL` | `PA` | `STRIPPER`; `PS2_PHASE` â†’ `L` | `V` | `TV` | `TL`.
- **`Pumparound ID must be specified`** on a PA pseudo stream â†’ the pumparound subobject is missing or `PS2_PANO` is empty. Repair with **`set_petrofrac_pumparound_specs`**, not pseudo page alone.
- **Side-stripper product streams** â†’ use `set_petrofrac_side_stripper_specs` / `configure_petrofrac_side_stripper_bundle` with a native `Subobjects\Strippers\S-n` row, product flow, reboiler duty, and two independent Liquid Return specs such as `return_flow` + `return_duty`.
- Real PetroFrac AD probe result: after full native stripper setup, `OPT_PSEUDO\<stream>` and `PS2_*\<stream>` may be absent/null because Aspen stores the complete stripper through `Subobjects\Strippers\S-n` plus `PSTRS_*` linkage. If the stripper subobject exists, indexed leaves are written, Liquid Return specs are complete, and block/global completion is input-complete, do not treat missing `OPT_PSEUDO\<stream>` as a remaining `PSEUDO-STR` failure.
- Do not set pumparound pseudo streams to `MAINCOL`, and do not write `PS2_STAGE`/`PS2_PHASE` after selecting `PA`; those fields belong to the `MAINCOL` radio branch.
- Vacuum/main product columns with `NPA=0` and no `OPT_PSEUDO` labeled children (typical V1/V2) do **not** need this page.
- Also load `aspen_agent_skills/guides/petrofrac-native-internals/SKILL.md`.

## RadFrac / Column: Dry-Up Or Built-In Flow Limits

Messages such as these indicate a physically inconsistent column specification or feed/traffic setup, not a solver-tolerance problem:

- `COLUMN DRIES UP OR COLUMN FLOWS VIOLATE BUILT-IN LIMITS`
- `stage <n> dries up`
- `dry column`
- severe final relative errors tied to a dry stage, missing liquid traffic, or missing vapor traffic

Repair direction:

- Verify live topology first: feed streams land on the intended stages, product streams use roles consistent with their physical phase, and abandoned/replacement streams are not still connected.
- Verify feed traffic before changing column specs: feed flows are nonzero, stream state specs are complete, feed phase/convention matches the intended tray service, and **upstream flash/reactor/heater pressure-temperature-unit basis** is physically consistent with the column pressure profile (**check Class B bar vs MPa** â€” see pressure section above).
- Check end effects and degrees of freedom as a bundle. `CONDENSER`, `REBOILER`, product phases, reflux/boilup, and product-flow or split specs must describe one coherent column, not a mixed partial setup.
- For `PARTIAL-V` vapor-overhead columns, do not stop at
  `set_condenser(PARTIAL-V)`: provide a coherent product-flow/reflux spec pair.
  If the visible operating-spec row is `Distillate rate`, write
  **`BASIS_D`** (`Data\Blocks\<BLK>\Input\BASIS_D`) with the task molar-flow
  unit. Use **`BASIS_RDV`** (`set_basis_rdv`) only when the task or live UI
  explicitly exposes a vapor-distillate fraction/rate spec; its readback path is
  `Data\Blocks\<BLK>\Input\BASIS_RDV`.
- For no-condenser/no-reboiler or absorber-like service, repair feed-stage/feed-convention/product-outlet semantics before adding reflux, boilup, or distillate-flow specs.
- If dry-up persists after topology and specs are coherent, reassess whether the requested separation, pressure profile, stage count, or product draw basis is physically feasible. Report infeasibility with REP/history evidence instead of masking it with solver settings.

Evidence to require after repair:

- `list_block_ports` or connection readback for feeds/products.
- Readback of feed stage/convention, pressure profile, condenser/reboiler mode, and active column specs.
- Upstream Flash/RStoic **`PRES`** vs task/meta pressure basis.
- A trusted `engine_run` plus REP/history evidence showing the dry-up message is gone.
## RadFrac: Negative Reflux Ratio / `BASIS_RR` Range Error

When Aspen rejects a RadFrac reflux specification with a message such as:

` ` `text
Value is out of range; it must be between 1e-15 and 1e+10
` ` `

and the rejected `BASIS_RR`/reflux value is negative or zero, treat this as an upstream operating-spec calculation error, not as an Aspen convergence failure or a generic input-incomplete message. A reflux ratio is positive; do not clamp the value to a small positive number or replace it with an arbitrary feasible value.

Repair direction:

- Preserve the exact rejected operation, block, value, and Aspen range in the failure payload.
- Trace the value back to the minimum-reflux/q-line/equilibrium calculation. For constant-relative-volatility initialization, evaluate both q-line/equilibrium roots and select the physical root: finite, `0 < x < 1`, compatible with the target distillate composition and pinch direction, and yielding `Rmin > 0`.
- Before calling `set_radfrac_reflux_ratio` or writing `Data\\Blocks\\<BLK>\\Input\\BASIS_RR`, require a finite positive value and record the calculation inputs (`q`, equilibrium basis, target composition, selected root, `Rmin`, and multiplier).
- Write the repaired positive value through the high-level RadFrac helper, then read `BASIS_RR` back and require `0 < RR < 1e10` before checking block completion or running Aspen.
- Keep feed, product, topology, condenser/reboiler, and task-fixed separation targets unchanged while repairing the root-selection calculation.

A negative `BASIS_RR` proves that the proposed configuration transaction is invalid; it does not prove that the column is physically infeasible. Stop at this boundary and expose the exact intermediate calculation instead of continuing with unrelated repairs.

` ` `

### FILE: aspen_agent_skills/guides/aspen-component-radfrac-evidence-repair/SKILL.md
Reason: selected skill for task block family
` ` `text
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

- `client.invoke("set_radfrac_distillate_rate", block_name="C1", value=99.0, unit="kmol/hr")`
- `client.invoke("set_radfrac_bottoms_rate", block_name="C1", value=40.0, unit="kmol/hr")`
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
- In headless Aspen sessions, `PER_ERROR` may be unavailable even after a successful engine run. Treat "PER_ERROR node not found" as missing evidence, not as convergence. Export and parse the current REP; accept the run only if REP Problem Status says the calculations completed normally and no real nonzero PER_ERROR is reported.
- If APW export destabilizes a headless rerun, preserve REP plus BKP/DEF evidence and make APW export opt-in rather than blocking summary generation.
- Avoid broad REP-export retry loops after Aspen cannot produce a REP. Use the bounded evidence helper once, preserve diagnostics, and fail clearly if evidence remains untrusted.

` ` `

### FILE: aspen_agent_skills/guides/aspen-pump-outlet-specification/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: aspen-pump-outlet-specification
description: >-
  Configure Aspen PUMP blocks (pressure, curve, or power mode), set Compr type
  early, preserve efficiency semantics, and map Pump completion text such as
  Outlet Specification must be specified to unset OPT_SPEC.
---

# Rotating Equipment Setup

Use this skill for **Aspen `PUMP` blocks** and `Compr` tasks where the answer depends on block mode, outlet specification, curve data, or efficiency semantics.

## Block family note (important)

Aspen exposes **one pump block family: `PUMP`**. Textbook labels such as “Pump HI” in problem statements refer to **operating/spec context**, not a separate Aspen block type. Always use `create_pump` and configure through `Data\Blocks\<BlockName>\Input\OPT_SPEC` and the dependent inputs below.

## `OPT_SPEC` option list (`Data\Blocks\<BlockName>\Input\OPT_SPEC`)

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

1. `set_opt_spec(block_name, "USE-CURVE")`
2. `set_opt_ctype(block_name, "SINGLE-OPER")` — or `SINGLE-REFE` / `MULTIP` per task
3. `set_opt_cformat(block_name, "TABLE")` — for tabulated head vs flow
4. `set_dep_var(block_name, "HEAD")` — dependent axis for TABLE curves
5. `set_indep_var(block_name, "VOL-FLOW")` — or `MASS-FLOW` if task uses mass flow
6. `set_pump_curve_table(block_name, curve_points=[{"flow": …, "head": …}, …], flow_unit="m3/hr", head_unit="m", curve_idx=1)`. This call sets `OPT_SPEC=USE-CURVE` itself. A previous `PRES`, `DELP`, `PRATIO`, or `POWER` does not remain the outlet specification.
7. Optional fidelity: `set_eff`, `set_deff`

`set_pump_curve_table` requires explicit `flow_unit` and `head_unit`. Pass the units printed with the curve. Accepted `flow_unit` values include `m3/hr`, `cum/hr`, `l/min`, `gpm`, and `cuft/min`. Accepted `head_unit` values include `m`, `ft`, `cm`, and `in`. Point values use those API units. Aspen's block-level `HEAD_UNITS` enum is `METER` or `FT`; the helper writes that token. Do not write `HEAD_UNITS` directly. The worked example below is the verified call.

A missing or illegal unit returns `success: false` with `error_code` `PUMP_CURVE_UNIT` and a message that starts `ERROR_CODE=PUMP_CURVE_UNIT`. That is the runtime ruff repair. Add or replace only `flow_unit` and `head_unit` on the existing call. Keep `curve_points`, `curve_idx`, and the pump mode.

The curve-table operation replaces the target `curve_idx` rows. Repeating the same call does not append a second copy of the points.

### Generic worked example (not tied to any scored case)

Cooling-water circulation pump `CW-P` on `FEED → CW-P → TO-TWR`:

` ` `python
client.invoke("set_opt_spec", block_name="CW-P", value="USE-CURVE")
client.invoke("set_opt_ctype", block_name="CW-P", value="SINGLE-OPER")
client.invoke("set_opt_cformat", block_name="CW-P", value="TABLE")
client.invoke("set_dep_var", block_name="CW-P", value="HEAD")
client.invoke("set_indep_var", block_name="CW-P", value="VOL-FLOW")
client.invoke(
    "set_pump_curve_table",
    block_name="CW-P",
    curve_idx=1,
    flow_unit="m3/hr",
    head_unit="m",
    curve_points=[
        {"flow": 18.0, "head": 22.0},
        {"flow": 12.0, "head": 28.0},
        {"flow": 8.0, "head": 31.0},
        {"flow": 5.0, "head": 34.0},
    ],
)
client.invoke("set_eff", block_name="CW-P", value=0.72)
client.invoke("set_deff", block_name="CW-P", value=0.95)
` ` `

Verify with REP/U-O-S readback that curve rows and `OPT_SPEC=USE-CURVE` appear under the pump input section.

## Pressure-target pump workflow (`OPT_SPEC=PRES`)

1. Connect `F(IN)` / `P(OUT)`.
2. `set_opt_spec(block_name, "PRES")`
3. `set_pres(block_name, value=..., unit=...)` — match task unit set
4. Add `set_eff` / `set_deff` only when task or REP requires them.

### Generic example

Booster pump `B-P` with 450 kPa discharge:

` ` `python
client.invoke("set_opt_spec", block_name="B-P", value="PRES")
client.invoke("set_pres", block_name="B-P", value=450.0, unit="kPa")
` ` `

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

` ` `

### FILE: aspen_agent_skills/guides/compr-analysis-variable-selection/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: compr-analysis-variable-selection
description: >-
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

Bind every selected numeric cell to its source row, object, variable token, actual exported/readback unit and physical role. A pressure axis (absolute/gauge pressure or pressure ratio) is not a compressor work column; indicated, brake and net power are distinct quantities. Never identify these roles by column position, field suffix, magnitude, or configured `helper-managed manipulated-variable field`/`helper-managed sampled-variable field` alone. Convert actual `AnnotatedQuantity` readbacks through `UNIT_REGISTRY`, keep unknown units unresolved, and replay the accepted manipulated pressure on its owning block with input verification. The final REP/BKP must agree with that selected row's pressure and same-role work terms; summed power requires converted, compatible terms, not a mislabeled pressure value.

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

` ` `python
compressor_terms = [
    {"label": f"W{i}", "block_name": block_name, "variable": "IND-POWER", "uom": work_unit}
    for i, block_name in enumerate(serial_compressor_blocks, start=1)
]
optimization_config = safe.configure_optimization_multi_block_var_objective(
    client,
    optimization_name="OPT-COMP",
    objective_terms=compressor_terms,
    expression="+".join(term["label"] for term in compressor_terms),
    vary_block=<compressor_or_upstream_block_that_owns_the_decision>,
    vary_variable=<live_pressure_or_ratio_token>,
    vary_uom=<task_pressure_unit>,
    lower=<physically_valid_lower_bound>,
    upper=<physically_valid_upper_bound>,
    constraints=[
        {
            "constraint_name": f"C{i}",
            "type": "block_var_bound",
            "block_name": term["block_name"],
            "variable": term["variable"],
            "operator": "GE",
            "target": minimum_work_value,
            "unit": work_unit,
            "label": f"C{i}",
        }
        for i, term in enumerate(compressor_terms, start=1)
    ] if minimum_work_value is not None else None,
    direction="MINIMIZE",
)
if not optimization_config.get("success"):
    summary.setdefault("analysis_objects", {}).setdefault("optimization", {})["OPT-COMP"] = optimization_config
    raise RuntimeError("compressor Optimization configuration failed; see repair_feedback")
final = safe.run_completion_engine_and_export(client, ...)
targets = [
    {
        "request_id": "opt_objective_total",
        "kind": "derived",
        "object_name": "OPT-COMP",
        "quantity": "optimization_objective",
        "notes": "FINAL OBJECTIVE FUNCTION VALUE from the native Optimization object",
    },
    {
        "request_id": "opt_manipulated_pres",
        "kind": "block",
        "object_name": vary_block,
        "quantity": "outlet_pressure",
        "notes": "FINAL VALUE for manipulated pressure in MANIPULATED VARIABLES",
    },
]
for term in compressor_terms:
    targets.append(
        {
            "request_id": f"w_{term['block_name']}",
            "kind": "block",
            "object_name": term["block_name"],
            "quantity": "indicated_power",
            "notes": f"{term['label']} / IND-POWER from OPTIMIZATION sampled variables or COMPR block section",
        }
    )
    targets.extend(
        [
            {
                "request_id": f"{term['block_name']}_polytropic_method",
                "kind": "block",
                "object_name": term["block_name"],
                "quantity": "polytropic_method",
                "notes": "POLYTROPIC COMPRESSOR USING ... METHOD from COMPR INPUT DATA (e.g. ASME)",
            },
            {
                "request_id": f"{term['block_name']}_polytropic_efficiency",
                "kind": "block",
                "object_name": term["block_name"],
                "quantity": "polytropic_efficiency",
                "notes": "POLYTROPIC EFFICIENCY from COMPR INPUT DATA",
            },
            {
                "request_id": f"{term['block_name']}_mechanical_efficiency",
                "kind": "block",
                "object_name": term["block_name"],
                "quantity": "mechanical_efficiency",
                "notes": "MECHANICAL EFFICIENCY from COMPR INPUT DATA",
            },
        ]
    )
safe.finalize_task_summary_with_llm_rep_readback(
    summary,
    final_bundle=final,
    rep_readback_targets=targets,
    llm_rep_readback_artifact_dir=artifact_dir,
    readbacks={"optimization_config": optimization_config},
)
` ` `

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
`safe.collect_compr_power_readback(client, block_name="CP", output_unit="W")`.
This helper tries native output leaves such as `IND_POWER`, `BRAKE_POWER`, and
`WNET`, then returns both `value` and `numeric_value`. Do not build custom
attempt rows that copy the successful Aspen payload under `payload.result.value`
while leaving the evidence row's own `numeric_value` as `None`; validators treat
that as no numeric compressor power evidence.

` ` `python
power = client.invoke("collect_compr_power_readback",  block_name="CP", output_unit="W")
summary.setdefault("results", {})["compressor_power"] = power
checks.append({
    "name": "compressor_power_read_from_compr_output",
    "passed": bool(power.get("success")),
    "evidence": power,
})
` ` `

## Pressure Coupling

When the Optimization varies the first compressor outlet pressure, any
intercooler/heater between compressor stages must preserve that pressure by
using zero pressure drop or a pressure-following setup. Do not fix the
intercooler outlet pressure to an analytic seed such as the equal-pressure-ratio
estimate; that decouples the second compressor from the manipulated variable.

If an intermediate pressure estimate is useful, use it only as a seed or bounds
hint. The reported optimum must come from native analysis output or final Aspen
readback after the analysis object has run.

` ` `

### FILE: aspen_agent_skills/guides/aspen-custom-unit-set/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: aspen-custom-unit-set
description: Creates and activates Aspen Plus custom or preset unit sets; routes INSET vs setter unit= correctly. Use when tasks need mixed display units, preset names like METCBAR, bar-scale block pressures, or any INSET outside the six built-in global tokens.
---

# Aspen Custom Unit Set

## Two failure classes (do not confuse them)

| Class | Symptom | Root cause | Fix |
|---|---|---|---|
| **A. INSET / unit-set routing** | `invalid_inset_value`, preset name missing, REP display units wrong | Wrong helper (`configure_inset_unit_system("METCBAR")`), set not created/activated | Paths below + `read_active_unit_set` |
| **B. Setter semantic unit** | Flash/RStoic runs but V/L wrong; RadFrac dry-up; absurd pump ΔP | Task/meta says **bar** but script writes **MPa** or omits `unit=` | **`unit="bar"`** (or task token) on `set_pres` / `set_pres_mixed` — legal under **any** INSET |

Class B is **not** “Aspen blocks bar”. Live probes confirm `set_pres(..., unit="bar")` under SI/ENG/MET/METCBAR.

When history/REP shows **stage dry-up**, **zero upstream feed**, or **pump/compressor pressure ~1e18**, check Class B and INSET-switch hazards below — not only solver settings. See `aspen-completion-error-hints`.

## Three INSET paths

| Path | When | Helper |
|---|---|---|
| **Built-in globals** | Task accepts SI/ENG/MET only | `configure_inset_unit_system` or `ensure_session(..., inset=...)` |
| **Preset / saved names** | Unit set already under `Data\Setup\Units-Sets` (BKP or HTTP template) | `activate_custom_unit_set` |
| **New mixed sets** | Derive from ENG/SI and override Unit-Types | `configure_custom_unit_set` |

Built-in tokens for `configure_inset_unit_system`:

`ENG`, `ENGUS`, `MET`, `MET-CHEM`, `SI`, `SI-CHEM`

Any other INSET (`MX`, `METCBAR`, …) → **`activate_custom_unit_set`** or **`configure_custom_unit_set`** — not `configure_inset_unit_system("MX")` (`invalid_inset_value`).

Do **not** edit BKP files to inject unit sets.

## Default blank session (HTTP template)

Aspen HTTP loads `tasks/standards/template_with_metcbar.apt` by default (`ASPEN_DEFAULT_SESSION_TEMPLATE`; `=off` disables). Fresh sessions expose `Units-Sets\METCBAR` and **`INSET=METCBAR`**.

- **`ensure_session()`** without `inset=` → preserves template INSET.
- **`ensure_session(..., inset="SI")`** → intentional override.
- Match task/reference INSET; do not force METCBAR on every flowsheet.

## Choosing an INSET strategy

| Task shape | Recommended approach |
|---|---|
| Display/reporting only (METCBAR or custom MX) | Preserve template or activate/configure custom set; verify `unit_types` |
| **Bar-scale** Flash/RStoic specs **and** SI-validated equipment (pump curves, some legacy tables) | Prefer **`INSET=SI`** + explicit **`unit="bar"`** on pressure setters — avoid METCBAR for the whole build then a late SI switch |
| Custom °C + mmHg on ENG base | `configure_custom_unit_set` → `MX` (works on template or built-in sessions) |
| Reference BKP at `INSET=METCBAR` | Load BKP; avoid global INSET rewrite unless task requires it |

## INSET switching hazard (mid-session)

**Verified:** Flash/RStoic `PRES` written with `unit="bar"` under **METCBAR**, then global **`INSET` switched to SI** later (e.g. pump performance table), can **rescale stored block pressures** (e.g. `-0.05` → `-5000` in tree readback) and break downstream traffic.

Rules:

- Choose strategy from the table **before** bulk writes.
- If SI-only tables are required, use **SI throughout** with explicit `unit="bar"` on pressures, **or** re-write bar pressures **after** the SI switch with `unit="bar"`.
- After any INSET change, re-read Flash/RStoic/feed **`PRES`** before `engine_run`.

## Mixed unit set (typical: ENG base, °C + mmHg display)

` ` `python
import script_agent_exp.safe_aspen_calls as safe

result = client.invoke("configure_custom_unit_set",
    unit_set_name="MX",
    base_set="ENG",
    quantity_units={"TEMPERATURE": "C", "PRESSURE": "mmHg"},
    set_active=True,
)
safe.require_success(result, label="configure_custom_unit_set")

verified = client.invoke("verify_custom_unit_set",
    unit_set_name="MX",
    expected_temperature="C",
    expected_pressure="mmHg",
    require_active_inset=True,
)
` ` `

Step-by-step equivalent:

` ` `python
client.invoke("create_unit_set_from_base",  unit_set_name="MX", base_set="ENG")
client.invoke("set_unit_set_quantity",  unit_set_name="MX", quantity="TEMPERATURE", unit="C")
client.invoke("set_unit_set_quantity",  unit_set_name="MX", quantity="PRESSURE", unit="mmHg")
client.invoke("activate_custom_unit_set",  unit_set_name="MX")
bundle = client.invoke("read_active_unit_set",  unit_set_name="MX")
` ` `

## Preset names (e.g. METCBAR)

Reference BKPs and the default HTTP template ship **`METCBAR`** (`Data\Setup\Units-Sets\METCBAR`, often `INSET=METCBAR`). It is **not** a built-in token for `configure_inset_unit_system`.

When the set exists in the live session:

` ` `python
client.invoke("activate_custom_unit_set",  unit_set_name="METCBAR")
bundle = client.invoke("read_active_unit_set",  unit_set_name="METCBAR")
` ` `

If `METCBAR` is absent (template disabled, old server): load a BKP that defines it, or use **`INSET=SI/MET`** with explicit **`unit="bar"`** on pressure setters — process specs stay correct even when display defaults differ.

Other named sets use the same **activate** path when listed under `Units-Sets`.

## Writing pressure with `unit="bar"` (INSET-independent)

**Verified:** `set_pres(..., unit="bar")` on Flash2 and RStoic under `INSET=SI`, `ENG`, `MET`, and template **METCBAR**.

| Fact | Detail |
|---|---|
| Legal setter tokens | `bar`, `bara`, `barg`, `MPa`, `kPa`, `psia`, `mmHg`, … on `set_pres` / `set_pres_mixed` |
| INSET independence | Pass **`unit="bar"` explicitly**; INSET does not auto-pick setter units |
| Common mistake | Rewriting bar-scale targets as **`MPa`** (e.g. `-0.05 bar` → `2.15 MPa`) — ~40× error |
| Negative absolute bar | On Flash2/RStoic with **absolute** bar units, **negative value = pressure drop** (near-atmospheric specs) |

` ` `python
# Near-atmospheric flash (meta often PRES = -0.05 bar)
client.invoke("set_spec_opt", block_name="F", value="TP")
client.invoke("set_temp", block_name="F", value=50.0, unit="C")
client.invoke("set_pres", block_name="F", value=-0.05, unit="bar")

# Reactor flash (meta often PRES = -0.1 bar)
client.invoke("set_spec_opt", block_name="R", value="TP")
client.invoke("set_temp", block_name="R", value=200.0, unit="C")
client.invoke("set_pres", block_name="R", value=-0.1, unit="bar")
` ` `

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

` ` `bash
# Full reform suite (quick: skip heavy ch91 build)
python tool_side_generation/healthcheck/unit_set_reform_experiment.py
python tool_side_generation/healthcheck/unit_set_reform_experiment.py --skip-heavy

python tool_side_generation/healthcheck/bar_pressure_write_probe.py
python tool_side_generation/healthcheck/metcbar_fresh_session_probe.py
python tool_side_generation/healthcheck/full_evaluation/custom_unit_set_probe.py --fresh --unit-set-name MX

# Mixed flowsheet: SI inset + bar PRES + partial-V RDV (regression)
python tool_side_generation/healthcheck/ch91_unit_set_reform_probe.py --si-inset
` ` `

` ` `

### FILE: aspen_agent_skills/guides/solvent-recycle-closure-semantics/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: solvent-recycle-closure-semantics
description: >-
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
- Do **not** build a physical `recovery bottoms -> mixer -> upstream column feed` tear loop on the first pass merely because the task says "connect", "recycle", or "return". In this skill, those words are process-intent words until a reference model or explicit task requirement proves a numerical tear is required.
- A physical tear loop that destabilizes a previously converged open-loop design is a topology-semantics failure, not a reason to keep tuning RadFrac specs blindly.

First distinguish:

| Closure type | Meaning | Typical Aspen pattern |
|--------------|---------|----------------------|
| **Process accounting closure** | Material balance is closed by a declared feed target plus makeup/recovery accounting | Fixed solvent feed (`S=120`), calculator for makeup, mixer outlet **not** wired back to upstream column |
| **Numerical recycle-tear closure** | A physical recycle loop is torn and solved by Wegstein/Broyden | Mixer outlet → upstream unit feed, explicit tear stream, circulation solved iteratively |

Both can be chemically valid. Pick the one the **task wording** and any **verified reference model** actually require.

Use a strict machine-readable enum in generated evidence:

- `closure_semantics.closure_type = "process_accounting"`
- `closure_semantics.closure_type = "numerical_recycle_tear"`

Do not invent hybrid closure types such as "accounting-first physical recycle". If a mixer outlet feeds an upstream unit, classify it as `numerical_recycle_tear` and prove the physical-tear prerequisites. If recovered material and makeup are only reported against a protected upstream target, classify it as `process_accounting`.

## Makeup Feed Semantics

A **makeup feed** is an external compensating feed that replaces material lost from the process through products, purge, vents, or waste streams. It is not, by itself, evidence that Aspen must solve a numerical recycle tear.

When a task says "provide a makeup feed", "make up losses", or "account for losses":

- Treat the makeup stream as a **loss-accounting handle** unless the task explicitly says the recovered stream replaces the protected upstream feed.
- Preserve any upstream fixed solvent/auxiliary circulation target as the primary feed contract; compute or report makeup as the difference between that protected target and recovered solvent plus outlet losses.
- Do not use the makeup stream as a reason to convert a previously fixed solvent feed into a mixer outlet that must be torn back to the upstream unit.
- If the task asks for losses "from each column" or "from each outlet", report per-column/per-outlet loss evidence and the makeup formula. This is stronger evidence for process accounting than for physical tear topology.
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

Plain words such as "connect bottoms", "return recycle", or "provide makeup" are not enough by themselves to prefer physical recycle when a fixed upstream solvent target already exists.

## Wiring Checklist

Before first `engine_run`:

1. Write the material edge plan and name each stream's **functional role** (fresh feed, fixed solvent, recovery bottoms, makeup, tear, product).
2. Confirm which edges are **physical** vs **accounting-only**.
3. If using accounting closure:
   - keep the fixed upstream feed stream on the upstream unit
   - route recovery to mixer/product/makeup as required
   - do **not** add `mixer outlet → upstream feed` just because a recycle concept exists in the task text
   - record a top-level `closure_semantics` object in `summary.json`:
     - `closure_type: "process_accounting"`
     - protected upstream solvent/feed target and unit
     - recovered solvent stream flow/composition
     - fresh makeup amount and formula
     - statement that physical tear closure was not required or was deferred
   - include APW/REP evidence from the converged accounting-closure run
4. If using physical recycle:
   - set `closure_semantics.closure_type: "numerical_recycle_tear"`; never use a hybrid closure type
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

` ` `

### FILE: aspen_agent_skills/guides/radfrac-extractive-distillation-solvent/SKILL.md
Reason: selected skill for task block family
` ` `text
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

Unit trap: Aspen's native Sensitivity CSV/REP may export stream flow rows in a
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
  recovery bottoms and makeup stream are mixed downstream, and Aspen's
  convergence system closes the loop. A standard solved case may leave the
  explicit Tear Streams table empty, relying on automatic sequencing plus
  convergence options instead of a manually listed tear stream.
- Some valid Aspen examples model solvent recycle as an accounting closure
  rather than a physically wired material loop. In that pattern, the extractive
  column receives a circulation/tear feed stream, while the recovered solvent
  and fresh makeup enter a downstream mixer whose outlet is used for balance
  evidence but is not necessarily wired back to the extractive-column inlet.
  Do not "repair" this by forcing the mixer outlet into the column if the
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

` ` `

### FILE: aspen_agent_skills/guides/optimization-constrained-feed-and-recycle-evidence/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: optimization-constrained-feed-and-recycle-evidence
description: >-
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

` ` `
1. Components + property method
2. Build **closed** material topology (including recycle + makeup **before** first real run)
3. Seed all feeds to input-complete (manipulated streams inside O1/DS bounds)
4. Configure Design Spec / Optimization (complete pairs + constraints)
5. engine_run on the **same** flowsheet topology
6. Export REP/APW from that final run
7. Populate results ONLY from step 5–6 readbacks / analysis output
` ` `

**Never** export base-case REP, then append recycle edges, then claim the recycle loop converged.

---

## O1 formulation: minimum feed with specs

When the task asks for *optimum / minimum / best amount* of an **auxiliary, solvent, or makeup feed**:

| Layer | Rule |
|-------|------|
| Manipulated | STREAM-VAR on the owning feed stream (`F2`, `SF1`, `MU1`, …) — see optimization-manipulated-variable-selection |
| Objective | Minimize that stream's mole-flow or mass-flow through the constrained stream-feed Optimization helper |
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

` ` `
MINIMIZE F2 MOLE-FLOW, vary F2, bounds 20–250, no CON/DS  →  FINAL_VAL ≈ lower bound
answer.md: "optimum phenol = 100 kmol/hr (design input)"     →  G2 FAIL
` ` `

### Required readbacks after O1

- helper readback identifies the intended feed stream
- helper readback identifies stream-flow minimization with the task direction
- Manipulated final value inside `[LOWER, UPPER]` **and** consistent with `summary.results.selected_*` or `rep_readback_evidence`
- `rep_readback_evidence` contains optimized feed flow and purity gates with `found: yes`

Use `configure_optimization_stream_var_minimize_flow` / `configure_optimization_stream_var` for HTTP landing; omit nonexistent active leaves from strict helper success checks.

- For constrained O1 on feed minimization with product/recycle purities:

` ` `python
configure_optimization_constrained_stream_var_minimize_flow(
    client,
    optimization_name="O1",
    objective_stream="<auxiliary_or_solvent_feed>",
    purity_constraints=[
        {
            "constraint_name": "C1",
            "stream_name": "<product_or_recycle_stream>",
            "component_name": "<key_component>",
            "lower_bound": 0.95,
        },
    ],
    lower=<lower_bound>,
    upper=<upper_bound>,
    step_size=<step_size>,
    max_step_size=<max_step_size>,
    vary_uom="kmol/hr",
    fvn_uom="kmol/hr",
)
final = run_completion_engine_and_export(...)
targets = [
    {
        "request_id": "opt_feed_flow",
        "kind": "stream",
        "object_name": "<auxiliary_or_solvent_feed>",
        "quantity": "total_flow",
        "notes": "Optimized manipulated feed flow from MANIPULATED VARIABLES or stream table",
    },
    {"request_id": "gate_1_purity", "kind": "stream", "object_name": "<stream>", "quantity": "component_flow", "component": "<cid>"},
]
safe.finalize_task_summary_with_llm_rep_readback(
    summary,
    final_bundle=final,
    rep_readback_targets=targets,
    llm_rep_readback_artifact_dir=artifact_dir,
)
` ` `

Before any constraint configuration, call **`list_constraint_recipes(block_types=[...], task_keywords=["purity"])`** and use recipe **`stream_mole_fraction_ge`** through the helper route; do not hand-code purity rows.

---

## Recycle / makeup: integrated topology

When the task requires *connect bottoms/recycle back to the column*, *makeup for losses*, or *execute until convergence*:

### Build in-loop (generic pattern)

` ` `
column-2 bottoms (recycle stream RC*) ──┐
makeup stream (MU*) ────────────────────┼──► mixer (MX*) ──► solvent/aux feed (SF*) ──► column-1
fresh process feed (F*) ───────────────────────────────────► column-1 (separate port)
` ` `

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

` ` `
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
- [ ] No "post-run proof only" language in final answer without a converged rerun
- [ ] analysis_objects.optimization.success reflects readbacks + usable output, not object creation alone
` ` `

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

**Task fragments:** "optimum auxiliary/solvent feed", "≥95% product purity",
"≥99.5% recycle purity", "connect recovery bottoms back with makeup".

| Step | Action |
|------|--------|
| Topology | Recovery-column bottoms → recycle stream; makeup + recycle → mixer → solvent feed → first column; process feed → first column |
| Seed | Solvent/auxiliary feed inside O1 `[LOWER, UPPER]` |
| Specs | Native Constraint rows and/or Design Spec on product/recycle purities |
| O1 | MINIMIZE solvent/auxiliary stream MOLE-FLOW via STREAM-VAR + linked CONID rows |
| Final | One post-optimization REP; report optimum from REP readback/manipulated stream, not seed inputs |

Use the task's actual stream and block names. This table is a **pattern**, not a mandate to hardcode any particular flow rate or label set.

` ` `

### FILE: aspen_agent_skills/guides/split-handoff-inheritance-boundary/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: split-handoff-inheritance-boundary
description: >-
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

` ` `json
{
  "handoff_inheritance": {
    "semantic_roles_inherited": [],
    "topology_intent_inherited": [],
    "component_property_basis_inherited": [],
    "numeric_values_used_as_seeds": [],
    "numeric_values_protected": [],
    "paper_locked_facts_preserved": [],
    "values_changed_for_downstream_reason": [],
    "change_triggers": [],
    "handoff_requalified_after_change": false
  }
}
` ` `

For every changed upstream handoff spec, the summary must also record:

- what was inherited unchanged
- what was protected as paper-locked
- which inherited numbers were used only as seeds
- which upstream closure/spec values were changed
- which downstream evidence trigger forced the change
- whether the repaired handoff stream/block re-qualified against the active gate after the change

## Generic Rule

Do not equate "continue from upstream" with "freeze all upstream numbers". Continue the process meaning first; protect numeric parameters only when they are explicitly part of the downstream contract. When downstream evidence shows the inherited numeric closure is wrong, repair the handoff boundary before widening optional downstream features.

For downstream analysis/optimization tasks, also do not equate "fresh Aspen
session" with "rediscover the train from a minimum prefix". Reuse the upstream
qualified topology and scaffold evidence; requalify once, then analyze.

Cross-scenario setup descriptions must cover the immediate dependency's full
proven scope (for example T02 → T03 hands off PF+CDU+VDU). Prefer
`producer_setup_description.md` from the upstream handoff bundle; do not treat a
nested earlier-hop PF-only note as the T02→T03 authority.

` ` `

### FILE: aspen_agent_skills/guides/rep-derived-metric-consistency/SKILL.md
Reason: selected skill for task block family
` ` `text
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

` ` `

### FILE: aspen_agent_skills/guides/analysis-method-selection/SKILL.md
Reason: selected skill for task block family
` ` `text
---
name: analysis-method-selection
description: Selects between Aspen Design Spec, Optimization, Sensitivity, and Aspen-backed candidate tables from task semantics. Use when a task asks to hit a target, choose an optimum, build a response curve, or repair an analysis route that overuses SA/OPT/DS.
---

# Analysis Method Selection

Use the smallest native analysis method that matches the task's decision
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

` ` `

### FILE: aspen_agent_skills/guides/analysis-object-output-repair/SKILL.md
Reason: selected skill for task block family
` ` `text
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

Persist under `analysis_objects.<family>`:

- object name and helper used;
- readbacks for manipulated and sampled/objective/constraint sides;
- post-run REP/APW/history identity;
- native output values and units;
- decision source row/value;
- unresolved blocker when output remains unavailable.

` ` `

### FILE: generated/task_profile_planning_validators.md
Reason: task-profile helper signatures for planning validators
` ` `text
# Task Profile: Planning Validator Helper Signatures

This section is generated from the LLM-selected task profile.
Use your actual Aspen block/stream IDs from the task statement; the placeholders below are generic.

- case_id: `chinese_5_1_radfrac`
- planning_validator_families: PROPERTY_METHODS, HEATER, RSTOIC, FLASH2, FSPLIT, RADFRAC, PUMP, COMPR, PIPE, VALVE

## validate_material_edge_plan

Validate a static material topology before mutating Aspen.

Signature:

` ` `python
validate_material_edge_plan(
    edges,
    *,
    block_names=None,
    stream_names=None,
)
` ` `

Rules:

- Pass the edge list as the **first positional** argument named `edges`.
- Do **not** pass `edge_plan=`, `topology=`, or other invented keyword aliases.
- Edge tuples `(stream, source, destination)` are case-insensitively unique: write each physical edge once, never silently deduplicate, and keep connection calls in one-to-one correspondence with the plan.
- **PRE-SUBMIT MATERIAL EDGE CHECKLIST (mechanical, before outputting Python):** inspect the complete static `MATERIAL_EDGES`/`edges` list and count rows by case-insensitive stream ID.
- Every physical material stream must have exactly one edge row, including feeds/products whose `source` or `destination` is `None`; a recycle is still one `source -> destination` edge.
- Never duplicate a connection merely to show it in multiple process groups. Do not use a `set` or `dict` to silently deduplicate; if any stream count exceeds one, rewrite the list.
- Verify one-to-one correspondence in both directions: each connection call has exactly one edge row, and each edge row has exactly one connection call.
- Each edge item uses `{"stream": "<stream_id>", "source": <block_id | None>, "destination": <block_id | None>}`.
- Feeds have `source=None`; products have `destination=None`.
- Aspen stream IDs must match `^[A-Za-z]{1,2}[0-9]{0,2}$` (examples: `F1`, `D1`, `S3`). Long semantic names such as `NAP`/`KERO`/`HNAP` are invalid; map them with `allocate_aspen_short_stream_names(...)` and `rewrite_material_edge_plan_streams(...)` before validation.
- Optional `block_names` / `stream_names` declare IDs you expect in the plan; missing declared streams raise.

Placeholder edge-plan shape:

` ` `python
validate_material_edge_plan(
    [
        {"stream": "<feed_stream>", "source": None, "destination": "<first_block>"},
        {"stream": "<intermediate_stream>", "source": "<upstream_block>", "destination": "<downstream_block>"},
        {"stream": "<product_stream>", "source": "<last_block>", "destination": None},
    ],
    block_names=["<first_block>", "<upstream_block>", "<downstream_block>", "<last_block>"],
    stream_names=["<feed_stream>", "<intermediate_stream>", "<product_stream>"],
)
` ` `

If the helper raises, fix the stream/block mapping before creating or connecting Aspen objects.

## Recycle convergence helper

Hard signature rule:

` ` `python
client.invoke("configure_recycle_convergence_options", tolerance=1e-5, tear_method="WEGSTEIN", wegstein_max_iterations=100)
` ` `

Never pass `max_iterations`; it is an incorrect alias, not a supported parameter.

Design Spec block-var rule: `BASIS_*` input leaves are forbidden in both `vary_variable` and `vary_patterns`. Resolve the exact token from live options; when unknown omit `vary_variable` and pass only semantic `vary_patterns`. `max_step_size` is a dimensionless 0..1 fraction.

## validate_required_native_blocks_plan

Validate that required native process blocks stay on the evidence-bearing path.

Signature:

` ` `python
validate_required_native_blocks_plan(
    required_blocks_by_family,
    *,
    created_blocks_by_family,
    finalization_required_blocks,
)
` ` `

Rules:

- Pass `required_blocks_by_family` as the **only positional** argument.
- Pass `created_blocks_by_family` and `finalization_required_blocks` as **keyword-only** arguments.
- Family keys are uppercase tokens such as `PUMP`, `RSTOIC`, `RADFRAC`. Values are lists of your block IDs.
- Do **not** pass a second positional argument.
- Rejected keyword aliases include `planned_native_blocks`, `planned_blocks`, `block_plan`, `required_blocks`, and `native_blocks`.
- `TypeError: ... takes 1 positional argument but 2 were given` usually means a block list was passed positionally instead of inside `required_blocks_by_family`.
- Model Analysis objects (Design Spec, Sensitivity, Optimization) are **not** block families for this helper.

### Block families for this case

- `PROPERTY_METHODS` → map to your script's block ID (placeholder `<block_id>`)
- `HEATER` → map to your script's block ID (placeholder `<heater_block>`)
- `RSTOIC` → map to your script's block ID (placeholder `<reactor_block>`)
- `FLASH2` → map to your script's block ID (placeholder `<flash_block>`)
- `FSPLIT` → map to your script's block ID (placeholder `<split_block>`)
- `RADFRAC` → map to your script's block ID (placeholder `<column_block>`)
- `PUMP` → map to your script's block ID (placeholder `<pump_block>`)
- `COMPR` → map to your script's block ID (placeholder `<compressor_block>`)
- `PIPE` → map to your script's block ID (placeholder `<pipe_block>`)
- `VALVE` → map to your script's block ID (placeholder `<valve_block>`)

Placeholder call shape for this case's block families:

` ` `python
validate_required_native_blocks_plan(
    {"PROPERTY_METHODS": ["<block_id>"], "HEATER": ["<heater_block>"], "RSTOIC": ["<reactor_block>"], "FLASH2": ["<flash_block>"], "FSPLIT": ["<split_block>"], "RADFRAC": ["<column_block>"], "PUMP": ["<pump_block>"], "COMPR": ["<compressor_block>"], "PIPE": ["<pipe_block>"], "VALVE": ["<valve_block>"]},
    created_blocks_by_family={"PROPERTY_METHODS": ["<block_id>"], "HEATER": ["<heater_block>"], "RSTOIC": ["<reactor_block>"], "FLASH2": ["<flash_block>"], "FSPLIT": ["<split_block>"], "RADFRAC": ["<column_block>"], "PUMP": ["<pump_block>"], "COMPR": ["<compressor_block>"], "PIPE": ["<pipe_block>"], "VALVE": ["<valve_block>"]},
    finalization_required_blocks=["<block_id>", "<heater_block>", "<reactor_block>", "<flash_block>", "<split_block>", "<column_block>", "<pump_block>", "<compressor_block>", "<pipe_block>", "<valve_block>"],
)
` ` `

Replace every placeholder with the real block IDs you create. When one family needs multiple blocks, list every required block ID under that family key and include each ID in `finalization_required_blocks`.

## REQUIRED_BLOCKS wiring

Define one `REQUIRED_BLOCKS` list that includes every block ID on the final result path plus any gate-required native blocks. Pass the same list to `run_completion_engine_and_export(..., required_blocks=REQUIRED_BLOCKS)` and `finalize_task_summary(..., required_blocks=REQUIRED_BLOCKS)`.

` ` `

### FILE: generated/initial_skill_selection.json
Reason: descriptor-based initial skill selection manifest
` ` `text
{
  "selection_basis": "explicit skill descriptors and exact skill names; no keyword, regex, or free-text matching",
  "input_skill_names": [
    "aspen-task-execution-order",
    "aspen-property-method-selection",
    "aspen-material-stream-composition-must-be-specified",
    "functional-role-semantics-validation",
    "aspen-generic-readbacks",
    "reactor-reaction-setup-high-level",
    "sequential-reaction-topology",
    "native-reactor-module-comparison",
    "flash-control-chain",
    "prefer-direct-component-splits",
    "shared-material-port-topology",
    "radfrac-absorber-like-configuration",
    "radfrac-standard-column-pressure-basis",
    "aspen-completion-error-hints",
    "aspen-component-radfrac-evidence-repair",
    "aspen-pump-outlet-specification",
    "compr-analysis-variable-selection",
    "aspen-custom-unit-set",
    "solvent-recycle-closure-semantics",
    "radfrac-extractive-distillation-solvent",
    "optimization-constrained-feed-and-recycle-evidence",
    "split-handoff-inheritance-boundary",
    "rep-derived-metric-consistency",
    "analysis-method-selection",
    "analysis-object-output-repair"
  ],
  "selected_skill_names": [
    "aspen-task-execution-order",
    "aspen-property-method-selection",
    "aspen-material-stream-composition-must-be-specified",
    "functional-role-semantics-validation",
    "aspen-generic-readbacks",
    "reactor-reaction-setup-high-level",
    "sequential-reaction-topology",
    "native-reactor-module-comparison",
    "flash-control-chain",
    "prefer-direct-component-splits",
    "shared-material-port-topology",
    "radfrac-absorber-like-configuration",
    "radfrac-standard-column-pressure-basis",
    "aspen-completion-error-hints",
    "aspen-component-radfrac-evidence-repair",
    "aspen-pump-outlet-specification",
    "compr-analysis-variable-selection",
    "aspen-custom-unit-set",
    "solvent-recycle-closure-semantics",
    "radfrac-extractive-distillation-solvent",
    "optimization-constrained-feed-and-recycle-evidence",
    "split-handoff-inheritance-boundary",
    "rep-derived-metric-consistency",
    "analysis-method-selection",
    "analysis-object-output-repair"
  ],
  "decisions": [
    {
      "input_skill": "aspen-task-execution-order",
      "decision": "load_for_init",
      "selected_skill": "aspen-task-execution-order",
      "descriptor": {}
    },
    {
      "input_skill": "aspen-property-method-selection",
      "decision": "load_for_init",
      "selected_skill": "aspen-property-method-selection",
      "descriptor": {
        "name": "aspen-property-method-selection",
        "summary": "Preserve methods; verify global/SRK free-water setup.",
        "stage": "init+repair",
        "required_families": [],
        "compatible_focus_ids": [],
        "compatible_mini_focuses": [],
        "init_replacement": "",
        "init_load": true
      }
    },
    {
      "input_skill": "aspen-material-stream-composition-must-be-specified",
      "decision": "load_for_init",
      "selected_skill": "aspen-material-stream-composition-must-be-specified",
      "descriptor": {
        "name": "aspen-material-stream-composition-must-be-specified",
        "summary": "Stream basis/state setup and independent-feed enthalpy preservation.",
        "stage": "init+repair",
        "required_families": [],
        "compatible_focus_ids": [],
        "compatible_mini_focuses": [],
        "init_replacement": "",
        "init_load": true
      }
    },
    {
      "input_skill": "functional-role-semantics-validation",
      "decision": "load_for_init",
      "selected_skill": "functional-role-semantics-validation",
      "descriptor": {}
    },
    {
      "input_skill": "aspen-generic-readbacks",
      "decision": "load_for_init",
      "selected_skill": "aspen-generic-readbacks",
      "descriptor": {
        "name": "aspen-generic-readbacks",
        "summary": "Generic Aspen/REP readbacks for streams, blocks, profiles, duties, and final evidence values.",
        "stage": "init+repair",
        "required_families": [],
        "compatible_focus_ids": [],
        "compatible_mini_focuses": [],
        "init_replacement": "",
        "init_load": true
      }
    },
    {
      "input_skill": "reactor-reaction-setup-high-level",
      "decision": "load_for_init",
      "selected_skill": "reactor-reaction-setup-high-level",
      "descriptor": {}
    },
    {
      "input_skill": "sequential-reaction-topology",
      "decision": "load_for_init",
      "selected_skill": "sequential-reaction-topology",
      "descriptor": {}
    },
    {
      "input_skill": "native-reactor-module-comparison",
      "decision": "load_for_init",
      "selected_skill": "native-reactor-module-comparison",
      "descriptor": {}
    },
    {
      "input_skill": "flash-control-chain",
      "decision": "load_for_init",
      "selected_skill": "flash-control-chain",
      "descriptor": {}
    },
    {
      "input_skill": "prefer-direct-component-splits",
      "decision": "load_for_init",
      "selected_skill": "prefer-direct-component-splits",
      "descriptor": {}
    },
    {
      "input_skill": "shared-material-port-topology",
      "decision": "load_for_init",
      "selected_skill": "shared-material-port-topology",
      "descriptor": {}
    },
    {
      "input_skill": "radfrac-absorber-like-configuration",
      "decision": "load_for_init",
      "selected_skill": "radfrac-absorber-like-configuration",
      "descriptor": {}
    },
    {
      "input_skill": "radfrac-standard-column-pressure-basis",
      "decision": "load_for_init",
      "selected_skill": "radfrac-standard-column-pressure-basis",
      "descriptor": {
        "name": "radfrac-standard-column-pressure-basis",
        "summary": "RadFrac pressure anchor and pressure-drop basis for standard distillation columns.",
        "stage": "init+repair",
        "required_families": [
          "RADFRAC"
        ],
        "compatible_focus_ids": [],
        "compatible_mini_focuses": [],
        "init_replacement": "",
        "init_load": true
      }
    },
    {
      "input_skill": "aspen-completion-error-hints",
      "decision": "load_for_init",
      "selected_skill": "aspen-completion-error-hints",
      "descriptor": {
        "name": "aspen-completion-error-hints",
        "summary": "Completion/PER_ERROR repairs; tear nonconvergence uses configure_recycle_convergence_options with readback; SRK uses configure_srk_free_water_steamnbs.",
        "stage": "init+repair",
        "required_families": [],
        "compatible_focus_ids": [],
        "compatible_mini_focuses": [],
        "init_replacement": "",
        "init_load": true
      }
    },
    {
      "input_skill": "aspen-component-radfrac-evidence-repair",
      "decision": "load_for_init",
      "selected_skill": "aspen-component-radfrac-evidence-repair",
      "descriptor": {}
    },
    {
      "input_skill": "aspen-pump-outlet-specification",
      "decision": "load_for_init",
      "selected_skill": "aspen-pump-outlet-specification",
      "descriptor": {}
    },
    {
      "input_skill": "compr-analysis-variable-selection",
      "decision": "load_for_init",
      "selected_skill": "compr-analysis-variable-selection",
      "descriptor": {
        "name": "compr-analysis-variable-selection",
        "summary": "Compressor selected-row pressure/power identity, units, and replay evidence.",
        "stage": "init+repair",
        "required_families": [],
        "compatible_focus_ids": [],
        "compatible_mini_focuses": [],
        "init_replacement": "",
        "init_load": true
      }
    },
    {
      "input_skill": "aspen-custom-unit-set",
      "decision": "load_for_init",
      "selected_skill": "aspen-custom-unit-set",
      "descriptor": {}
    },
    {
      "input_skill": "solvent-recycle-closure-semantics",
      "decision": "load_for_init",
      "selected_skill": "solvent-recycle-closure-semantics",
      "descriptor": {}
    },
    {
      "input_skill": "radfrac-extractive-distillation-solvent",
      "decision": "load_for_init",
      "selected_skill": "radfrac-extractive-distillation-solvent",
      "descriptor": {}
    },
    {
      "input_skill": "optimization-constrained-feed-and-recycle-evidence",
      "decision": "load_for_init",
      "selected_skill": "optimization-constrained-feed-and-recycle-evidence",
      "descriptor": {}
    },
    {
      "input_skill": "split-handoff-inheritance-boundary",
      "decision": "load_for_init",
      "selected_skill": "split-handoff-inheritance-boundary",
      "descriptor": {}
    },
    {
      "input_skill": "rep-derived-metric-consistency",
      "decision": "load_for_init",
      "selected_skill": "rep-derived-metric-consistency",
      "descriptor": {
        "name": "rep-derived-metric-consistency",
        "summary": "Derived metric consistency from trusted REP/readback raw values with explicit units and formulas.",
        "stage": "init+repair",
        "required_families": [],
        "compatible_focus_ids": [],
        "compatible_mini_focuses": [],
        "init_replacement": "",
        "init_load": true
      }
    },
    {
      "input_skill": "analysis-method-selection",
      "decision": "load_for_init",
      "selected_skill": "analysis-method-selection",
      "descriptor": {}
    },
    {
      "input_skill": "analysis-object-output-repair",
      "decision": "load_for_init",
      "selected_skill": "analysis-object-output-repair",
      "descriptor": {}
    }
  ]
}
` ` `

### FILE: generated/initial_helper_catalog_selection.json
Reason: descriptor-based helper catalog selection manifest
` ` `text
{
  "selection_basis": "helper catalog descriptors plus exact task-profile families, surface docs, and skill names only; no keyword, regex, path-prefix, or free-text matching",
  "profile_families": [
    "COMPR",
    "FLASH2",
    "FSPLIT",
    "HEATER",
    "PIPE",
    "PROPERTY_METHODS",
    "PUMP",
    "RADFRAC",
    "RSTOIC",
    "VALVE"
  ],
  "profile_surface_docs": [
    "docs/hardcoded_script_plan/block_type_inject/compr.md",
    "docs/hardcoded_script_plan/block_type_inject/flash2.md",
    "docs/hardcoded_script_plan/block_type_inject/fsplit.md",
    "docs/hardcoded_script_plan/block_type_inject/heater.md",
    "docs/hardcoded_script_plan/block_type_inject/pipe.md",
    "docs/hardcoded_script_plan/block_type_inject/property_methods.md",
    "docs/hardcoded_script_plan/block_type_inject/pump.md",
    "docs/hardcoded_script_plan/block_type_inject/radfrac.md",
    "docs/hardcoded_script_plan/block_type_inject/rstoic.md",
    "docs/hardcoded_script_plan/block_type_inject/valve.md"
  ],
  "profile_skill_names": [
    "aspen-completion-error-hints",
    "aspen-component-radfrac-evidence-repair",
    "aspen-custom-unit-set",
    "aspen-generic-readbacks",
    "aspen-material-stream-composition-must-be-specified",
    "aspen-property-method-selection",
    "aspen-pump-outlet-specification",
    "aspen-task-execution-order",
    "compr-analysis-variable-selection",
    "flash-control-chain",
    "functional-role-semantics-validation",
    "native-reactor-module-comparison",
    "optimization-constrained-feed-and-recycle-evidence",
    "prefer-direct-component-splits",
    "radfrac-absorber-like-configuration",
    "radfrac-extractive-distillation-solvent",
    "radfrac-standard-column-pressure-basis",
    "reactor-reaction-setup-high-level",
    "rep-derived-metric-consistency",
    "sequential-reaction-topology",
    "shared-material-port-topology",
    "solvent-recycle-closure-semantics",
    "split-handoff-inheritance-boundary"
  ],
  "selected_helper_catalog_paths": [
    "docs/hardcoded_script_plan/safe_aspen_calls_core_helpers.md",
    "docs/hardcoded_script_plan/safe_aspen_calls_analysis_helpers.md",
    "docs/hardcoded_script_plan/safe_aspen_calls_radfrac_helpers.md",
    "docs/hardcoded_script_plan/safe_aspen_calls_heat_cascade_helpers.md"
  ],
  "decisions": [
    {
      "helper_catalog": "core",
      "decision": "load",
      "reason": "always_load",
      "descriptor": {
        "name": "core",
        "path": "docs/hardcoded_script_plan/safe_aspen_calls_core_helpers.md",
        "summary": "Always-loaded session, component/property, stream state, run/export, and finalization helpers.",
        "stage": "init",
        "required_families_any": [],
        "required_surface_docs_any": [],
        "required_skill_names_any": [],
        "always_load": true
      }
    },
    {
      "helper_catalog": "analysis",
      "decision": "load",
      "reason": "matched_exact_skill_names:['optimization-constrained-feed-and-recycle-evidence']",
      "descriptor": {
        "name": "analysis",
        "path": "docs/hardcoded_script_plan/safe_aspen_calls_analysis_helpers.md",
        "summary": "Native Design Spec, Sensitivity, and Optimization helper contracts.",
        "stage": "init",
        "required_families_any": [
          "CONSTRAINT",
          "DESIGN_SPEC",
          "OPTIMIZATION",
          "SENSITIVITY"
        ],
        "required_surface_docs_any": [
          "docs/hardcoded_script_plan/block_type_inject/constraint.md",
          "docs/hardcoded_script_plan/block_type_inject/design_spec.md",
          "docs/hardcoded_script_plan/block_type_inject/optimization.md",
          "docs/hardcoded_script_plan/block_type_inject/sensitivity.md"
        ],
        "required_skill_names_any": [
          "analysis-method-selection",
          "analysis-object-output-repair",
          "analysis-object-transaction-finalization",
          "analysis-tools-single-pass-finalization",
          "design-spec-manipulated-surface-selection",
          "optimization-constrained-feed-and-recycle-evidence",
          "optimization-manipulated-variable-selection",
          "optimization-result-authenticity",
          "sensitivity-uom-and-variable-setup",
          "sensitivity-vary-patterns"
        ],
        "always_load": false
      }
    },
    {
      "helper_catalog": "radfrac",
      "decision": "load",
      "reason": "matched_explicit_profile_families:['RADFRAC']",
      "descriptor": {
        "name": "radfrac",
        "path": "docs/hardcoded_script_plan/safe_aspen_calls_radfrac_helpers.md",
        "summary": "RadFrac setup, feed convention, profile, and product/readback helper contracts.",
        "stage": "init",
        "required_families_any": [
          "RADFRAC"
        ],
        "required_surface_docs_any": [
          "docs/hardcoded_script_plan/block_type_inject/radfrac.md"
        ],
        "required_skill_names_any": [
          "radfrac-absorber-like-configuration",
          "radfrac-convergence-repair",
          "radfrac-extractive-distillation-solvent",
          "radfrac-no-condenser-reboiled-bottoms",
          "radfrac-standard-column-pressure-basis",
          "solvent-recycle-closure-semantics"
        ],
        "always_load": false
      }
    },
    {
      "helper_catalog": "heat_cascade",
      "decision": "load",
      "reason": "matched_explicit_profile_families:['FLASH2']",
      "descriptor": {
        "name": "heat_cascade",
        "path": "docs/hardcoded_script_plan/safe_aspen_calls_heat_cascade_helpers.md",
        "summary": "Heat stream, HeatX, MHeatX, Flash2 evaporator, and multi-effect heat-cascade helpers.",
        "stage": "init",
        "required_families_any": [
          "FLASH2",
          "HEATX",
          "HEAT_STREAM",
          "MHEATX"
        ],
        "required_surface_docs_any": [
          "docs/hardcoded_script_plan/block_type_inject/flash2.md",
          "docs/hardcoded_script_plan/block_type_inject/heat_stream.md",
          "docs/hardcoded_script_plan/block_type_inject/heatx.md",
          "docs/hardcoded_script_plan/block_type_inject/mheatx.md"
        ],
        "required_skill_names_any": [
          "flash-control-chain",
          "heatx-shortcut-target-and-area",
          "multi-effect-evaporation-heatx",
          "multi-effect-topology-init",
          "phase-change-heat-cascade-integrity"
        ],
        "always_load": false
      }
    },
    {
      "helper_catalog": "probe",
      "decision": "skip",
      "reason": "no explicit descriptor condition matched for init",
      "descriptor": {
        "name": "probe",
        "path": "docs/hardcoded_script_plan/safe_aspen_calls_probe_helpers.md",
        "summary": "Standard procedural probe matrix and selected-row replay helper contracts.",
        "stage": "repair",
        "required_families_any": [],
        "required_surface_docs_any": [],
        "required_skill_names_any": [],
        "always_load": false
      }
    }
  ]
}
` ` `

### REACT-MCP NATIVE SKILL
React-MCP-native Aspen action contract:
1. Select exactly one JSON action: {"action":"mcp_tool","operation":"...","parameters":{...}}.
2. Use only an operation in the visible catalog. Map process intent to the catalog operation,
   never emit Python, safe.call snippets, or invented HTTP operations.
3. After topology writes, read list_block_ports or node_info and verify the live connection.
   Use Aspen Tree paths with single backslashes (Data\\Blocks\\BLK); do not invent paths.
4. After specification writes, read the affected node/table and run the relevant block/stream
   completion check. Before engine_run, require the workflow Next-gate check.
5. Treat wrapper success as provisional. Continue when readback, completion, or evidence is
   missing; stop and repair when a readback contradicts the requested state.
6. Error routing: unknown operation -> choose a catalog operation; missing parameter -> supply
   it; node not found -> normalize/re-read the canonical path and inspect parent elements;
   topology error -> list ports before reconnecting; incomplete input -> repair the named object
   then re-run the completion gate; runtime error -> inspect same-run status before retrying.
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
```

### Tool catalog

```text
Aspen ReAct tool surface (registry-driven facade):
- Call one tool with action=mcp_tool, operation=<name>, parameters=<JSON object>.
- Virtual tools expand to documented Aspen HTTP operations internally through safe_aspen_calls.
- Shared core always includes streams, completion probes, engine_run, and export helpers.
- Shared core native tools: 32; virtual tools: 37.
- The runner starts an Aspen session before the first step.
- Allowed tools for this baseline run:
  - activate_custom_unit_set
  - add_components_by_cas
  - apply_reaction_row_heat_and_selectivity_reporting: Set RStoic HREF_CID/REF_CID/SEL_CID fields coherently for one reaction row.
    parameters: {'block_name': 'string', 'reaction_number': 'integer', 'href_cid': 'string (optional)', 'ref_cid': 'string (optional)', 'sel_cid': 'string (optional)'}
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
    parameters: {'stream_name': 'string', 'temperature': 'number (optional)', 'pressure': 'number (optional)', 'temperature_unit': 'string (optional)', 'pressure_unit': 'string (optional)'}
  - configure_custom_unit_set
  - configure_flash2_operating_specs: Alias for legal Flash2 SPEC_OPT plus typed TEMP/PRES/VFRAC/DUTY writes with mutual-exclusion cleanup.
    parameters: {'block_name': 'string', 'spec_opt': 'TP|TV|PV|PD|TD|TQ|PQ', 'pressure': 'number (optional)', 'pressure_unit': 'string (optional)', 'temperature': 'number (optional)', 'temperature_unit': 'string (optional)', 'vapor_fraction': 'number (optional)', 'duty': 'number (optional)', 'duty_unit': 'string (optional)'}
  - configure_fsplit_shared_outlets
  - configure_heat_stream_duty
  - configure_heat_stream_duty_map: Write DUTY on multiple heat streams, for example Q1..Q4 cascades.
    parameters: {'duties_by_stream': 'object mapping heat-stream names to duty values', 'unit': 'kJ/hr', 'verify_readback': 'bool (default true)'}
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
    parameters: {'block_name': 'string', 'feed_stream': 'string', 'vapor_stream': 'string', 'liquid_stream': 'string'}
  - connect_material_inlet_outlet: Connect a block material inlet and outlet in one helper call.
    parameters: {'block_name': 'string', 'inlet_stream': 'string', 'outlet_stream': 'string'}
  - connect_material_ports_by_order
  - connect_radfrac_feed_distillate_bottoms: Wire RadFrac feed(s), distillate, and bottoms by role-aware ports.
    parameters: {'block_name': 'string', 'inlet_streams': ['F1'], 'distillate_stream': 'D1', 'bottoms_stream': 'B1'}
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
    parameters: {'method': 'NRTL|SRK|...'}
  - export_apw
  - export_final_evidence: Run engine, read PER_ERROR, export REP/APW, and return a bounded diagnostic_summary with same-run REP problem status and repair hints when PER_ERROR is nonzero.
    parameters: {'run_engine': 'bool (optional; default true)', 'rep_filename': 'string (optional)', 'apw_filename': 'string (optional)', 'export_format': 'int (optional; default 2)'}
  - export_rep
  - export_standard_evidence: Trusted evidence export via safe.export_standard_evidence with REP/APW/BKP paths.
    parameters: {'script_stem': 'string', 'task_key': 'string', 'server_subdir': 'string (optional; default script_agent_experiment)', 'export_bkp': 'bool (optional)', 'export_rep': 'bool (optional; default true)', 'export_apw': 'bool (optional)'}
  - extract_block_ports
  - finalize_task_summary_with_llm_rep_readback: Merge the trusted final Aspen run bundle into summary and collect LLM REP readbacks. Call once only after a successful engine run with PER_ERROR=0 and exported REP/APW evidence.
    parameters: {'summary': 'object (required; current semantic summary)', 'final_bundle': 'object (required; trusted same-run evidence bundle)', 'rep_readback_targets': 'array of objects (optional; stream/block/derived/profile targets)', 'llm_rep_readback_artifact_dir': 'string (optional)', 'readbacks': 'object (optional; diagnostic readbacks)', 'validation_checks': 'array (optional)', 'required_streams': 'array of strings (optional)', 'required_blocks': 'array of strings (optional)', 'stages': 'array (optional)', 'name_mapping': 'object (optional)', 'rep_problem_status': 'object (optional)', 'soft_sanity_checks': 'object (optional)'}
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
    parameters: {'block_name': 'string', 'rep_path': 'string (optional; provide rep_path or rep_text)', 'rep_text': 'string (optional; provide rep_text or rep_path)', 'feed_tray_convention': 'string (optional; default stages_above_feed)'}
  - read_dstwu_shortcut_basis
  - read_global_property_method
  - read_heater_duty
  - read_pressure_state
  - read_stream_mole_fractions
  - read_stream_output
  - read_stream_outputs: Batch read stream temperature, pressure, vapor fraction, and component flows.
    parameters: {'stream_name': 'string', 'components': 'array of component IDs (optional)', 'basis': 'mole_flow|mole_fraction|mass_flow (optional; default mole_flow)'}
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
    parameters: {'stream_name': 'string', 'mixed_spec': 'TP|TV|PV (optional)', 'basis': 'MOLE-FLOW|MOLE-FRAC|MASS-FLOW (optional)', 'flows': 'object mapping component IDs to values (optional)', 'temperature': 'number (optional)', 'pressure': 'number (optional)', 'vapor_fraction': 'number (optional)'}
  - set_material_stream_composition: Set material stream basis and component flows or fractions.
    parameters: {'stream_name': 'string', 'basis': 'MOLE-FLOW|MOLE-FRAC|MASS-FLOW (optional; default MOLE-FLOW)', 'flows': 'object mapping component IDs to values (optional; aliases composition/components)', 'composition': 'alias for flows', 'components': 'alias for flows', 'flow_unit': 'string (optional; default kmol/hr)', 'total_flow': 'number (optional; required only when basis is MOLE-FRAC)'}
  - set_material_stream_conditions: Set material stream state spec (TP/TV/PV) plus optional basis/total flow.
    parameters: {'stream_name': 'string', 'temperature': 'number (optional)', 'temperature_unit': 'string (optional, e.g. C)', 'pressure': 'number (optional)', 'pressure_unit': 'string (optional, e.g. atm)', 'vapor_fraction': 'number (optional)', 'mixed_spec': 'TP|TV|PV (optional; inferred from provided fields)'}
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
    parameters: {'block_name': 'string', 'curve_points': 'array of {flow: number, head: number}', 'flow_unit': 'string (required)', 'head_unit': 'string (required)', 'curve_idx': 'integer (default 1)'}
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
    parameters: {'block_name': 'string', 'spec_opt': 'TP|TV|PV|PD|TD|TQ|PQ', 'pressure': 'number (optional)', 'pressure_unit': 'string (optional)', 'temperature': 'number (optional)', 'temperature_unit': 'string (optional)', 'vapor_fraction': 'number (optional)', 'duty': 'number (optional)', 'duty_unit': 'string (optional)'}
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
```

## Call 1: `select_action`

- Input tokens: **124,796**
- Output tokens: **1,483**
- Total tokens: **126,279**
- Provider cost: **$0.668470**
- Recorded at: `2026-10-18T20:58:21.073`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 0,
    "domain_versions": {},
    "components": [],
    "property_method": "",
    "blocks": [],
    "streams": [],
    "connections": [],
    "specs": [],
    "engine_run": null,
    "artifacts": {},
    "readbacks": []
  },
  "operation_ledger": {},
  "failed_attempts": [],
  "validator_rejections": []
}
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 0
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "event": "preflight",
    "health": {
      "status": "healthy"
    },
    "task_hash": "<REDACTED_TASK_ID>"
  },
  {
    "event": "session_started"
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Build the exact named flowsheet in a batched prefix: components, RK-SOAVE, streams/blocks, and physical topology before specs.","action":"mcp_plan","parameters":{"actions":[{"operation":"add_components_by_cas","parameters":{"components":[{"component_id":"H2","cas":"1333-74-0"},{"component_id":"N2","cas":"7727-37-9"},{"component_id":"CH4","cas":"74-82-8"},{"component_id":"BENZENE","cas":"71-43-2"},{"component_id":"CYCLOHEX","cas":"110-82-7"}]}},{"operation":"ensure_property_method","parameters":{"method":"RK-SOAVE"}},{"operation":"create_material_streams","parameters":{"stream_names":["BZIN","H2IN","BZIN2","H2RCY2","RXIN","RXOUT","VAP","H2RCY","PURGE","PURGE2","LIQ","COLFD","CHRCY","CHRCY2","CHRCY3","LTENDS","PRODUCT"]}},{"operation":"create_pump","parameters":{"block_name":"FEEDPUMP"}},{"operation":"create_heater","parameters":{"block_name":"FEED-MIX"}},{"operation":"create_rstoic","parameters":{"block_name":"REACT"}},{"operation":"create_flash2","parameters":{"block_name":"HP-SEP"}},{"operation":"create_fsplit","parameters":{"block_name":"VFLOW"}},{"operation":"create_compr","parameters":{"block_name":"COMP"}},{"operation":"create_valve","parameters":{"block_name":"VALVE"}},{"operation":"create_fsplit","parameters":{"block_name":"LFLOW"}},{"operation":"create_pump","parameters":{"block_name":"PUMP"}},{"operation":"create_pipe","parameters":{"block_name":"PIPE"}},{"operation":"create_radfrac","parameters":{"block_name":"COLUMN"}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"FEEDPUMP","inlet_stream":"BZIN","outlet_stream":"BZIN2"}},{"operation":"connect_shared_material_port_block","parameters":{"block_name":"FEED-MIX","inlet_streams":["BZIN2","H2IN","H2RCY2","CHRCY3"],"outlet_streams":["RXIN"]}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"REACT","inlet_stream":"RXIN","outlet_stream":"RXOUT"}},{"operation":"connect_flash2_vapor_liquid_ports","parameters":{"block_name":"HP-SEP","feed_stream":"RXOUT","vapor_stream":"VAP","liquid_stream":"LIQ"}},{"operation":"configure_fsplit_shared_outlets","parameters":{"block_name":"VFLOW","inlet_stream":"VAP","outlet_streams":["H2RCY","PURGE"],"split_fractions":{"H2RCY":0.92}}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"COMP","inlet_stream":"H2RCY","outlet_stream":"H2RCY2"}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"VALVE","inlet_stream":"PURGE","outlet_stream":"PURGE2"}},{"operation":"configure_fsplit_shared_outlets","parameters":{"block_name":"LFLOW","inlet_stream":"LIQ","outlet_streams":["CHRCY","COLFD"],"split_fractions":{"CHRCY":0.30}}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"PUMP","inlet_stream":"CHRCY","outlet_stream":"CHRCY2"}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"PIPE","inlet_stream":"CHRCY2","outlet_stream":"CHRCY3"}},{"operation":"connect_radfrac_feed_distillate_bottoms","parameters":{"block_name":"COLUMN","inlet_streams":["COLFD"],"distillate_stream":"LTENDS","bottoms_stream":"PRODUCT"}}]}} 


{"thought":"Topology build started; waiting for MCP plan observations to continue with any repair and then specifications.","action":"finalize","final_summary":{"case_id":"chinese_5_1_radfrac","ok":false,"evidence":{},"results":{},"self_validation":{"status":"blocked_before_observation","reason":"No tool observation was provided after the batched MCP plan, so I cannot honestly claim the Aspen flowsheet was created or solved."}}}
```

</details>

## Call 2: `select_action`

- Input tokens: **130,421**
- Output tokens: **5,208**
- Total tokens: **135,629**
- Provider cost: **$0.808345**
- Recorded at: `2026-10-18T20:59:10.439`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 25,
    "domain_versions": {
      "properties": 2,
      "flowsheet": 25,
      "stream:H2RCY2": 3,
      "stream:CHRCY2": 3,
      "stream:LIQ": 3,
      "stream:RXOUT": 3,
      "stream:PURGE": 3,
      "stream:BZIN": 2,
      "stream:PRODUCT": 2,
      "stream:H2IN": 2,
      "stream:CHRCY3": 3,
      "stream:LTENDS": 2,
      "stream:BZIN2": 3,
      "stream:VAP": 3,
      "stream:H2RCY": 3,
      "stream:PURGE2": 2,
      "stream:CHRCY": 3,
      "stream:RXIN": 3,
      "stream:COLFD": 3,
      "block:FEEDPUMP": 2,
      "block:FEED-MIX": 2,
      "block:REACT": 2,
      "block:HP-SEP": 2,
      "block:VFLOW": 2,
      "block:COMP": 2,
      "block:VALVE": 2,
      "block:LFLOW": 2,
      "block:PUMP": 2,
      "block:PIPE": 2,
      "block:COLUMN": 2
    },
    "components": [
      "H2",
      "N2",
      "CH4",
      "BENZENE",
      "CYCLOHEX"
    ],
    "property_method": "",
    "blocks": [
      "FEEDPUMP",
      "FEED-MIX",
      "REACT",
      "HP-SEP",
      "VFLOW",
      "COMP",
      "VALVE",
      "LFLOW",
      "PUMP",
      "PIPE",
      "COLUMN"
    ],
    "streams": [
      "BZIN",
      "H2IN",
      "BZIN2",
      "H2RCY2",
      "RXIN",
      "RXOUT",
      "VAP",
      "H2RCY",
      "PURGE",
      "PURGE2",
      "LIQ",
      "COLFD",
      "CHRCY",
      "CHRCY2",
      "CHRCY3",
      "LTENDS",
      "PRODUCT"
    ],
    "connections": [],
    "specs": [],
    "engine_run": null,
    "artifacts": {},
    "readbacks": []
  },
  "operation_ledger": {
    "677ff79d23598058": {
      "operation": "add_components_by_cas",
      "parameters": {
        "components": [
          {
            "component_id": "H2",
            "cas": "1333-74-0"
          },
          {
            "component_id": "N2",
            "cas": "7727-37-9"
          },
          {
            "component_id": "CH4",
            "cas": "74-82-8"
          },
          {
            "component_id": "BENZENE",
            "cas": "71-43-2"
          },
          {
            "component_id": "CYCLOHEX",
            "cas": "110-82-7"
          }
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "components_added": [
          {
            "cas": "1333740",
            "component_id": "H2",
            "requested_component_id": "H2",
            "preferred_component_id": "H2"
          },
          {
            "cas": "7727379",
            "component_id": "N2",
            "requested_component_id": "N2",
            "preferred_component_id": "N2"
          },
          {
            "cas": "74-82-8",
            "component_id": "CH4",
            "requested_component_id": "CH4",
            "preferred_component_id": "CH4"
          },
          {
            "cas": "71-43-2",
            "component_id": "BENZENE",
            "requested_component_id": "BENZENE",
            "preferred_component_id": "BENZENE"
          },
          {
            "cas": "110-82-7",
            "component_id": "CYCLOHEX",
            "requested_component_id": "CYCLOHEX",
            "preferred_component_id": "CYCLOHEX"
          }
        ],
        "count": 5,
        "message": "Added 5 component(s) successfully",
        "verification": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "missing_component_ids": []
        },
        "contamination": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "extra_component_ids": [],
          "generic_extra_component_ids": []
        }
      }
    },
    "d0f7c037faabb2bb": {
      "operation": "ensure_property_method",
      "parameters": {
        "method": "RK-SOAVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 2
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "ensure_property_method",
        "steps_completed": 5,
        "steps_total": 5,
        "last_result": null
      }
    },
    "33ce8ec6c91a3f71": {
      "operation": "create_material_streams",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "stream:BZIN",
        "stream:H2IN",
        "stream:BZIN2",
        "stream:H2RCY2",
        "stream:RXIN",
        "stream:RXOUT",
        "stream:VAP",
        "stream:H2RCY",
        "stream:PURGE",
        "stream:PURGE2",
        "stream:LIQ",
        "stream:COLFD",
        "stream:CHRCY",
        "stream:CHRCY2",
        "stream:CHRCY3",
        "stream:LTENDS",
        "stream:PRODUCT"
      ],
      "dependency_versions": {
        "stream:BZIN": 1,
        "stream:H2IN": 1,
        "stream:BZIN2": 1,
        "stream:H2RCY2": 1,
        "stream:RXIN": 1,
        "stream:RXOUT": 1,
        "stream:VAP": 1,
        "stream:H2RCY": 1,
        "stream:PURGE": 1,
        "stream:PURGE2": 1,
        "stream:LIQ": 1,
        "stream:COLFD": 1,
        "stream:CHRCY": 1,
        "stream:CHRCY2": 1,
        "stream:CHRCY3": 1,
        "stream:LTENDS": 1,
        "stream:PRODUCT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "create_material_streams",
        "steps_completed": 17,
        "steps_total": 17,
        "last_result": null
      }
    },
    "aeeab72bf4e897bd": {
      "operation": "create_pump",
      "parameters": {
        "block_name": "FEEDPUMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEEDPUMP"
      ],
      "dependency_versions": {
        "block:FEEDPUMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEEDPUMP",
        "block_type": "PUMP",
        "composite": "FEEDPUMP!PUMP",
        "message": "Block FEEDPUMP (PUMP) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "0909126309d406aa": {
      "operation": "create_heater",
      "parameters": {
        "block_name": "FEED-MIX"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEED-MIX"
      ],
      "dependency_versions": {
        "block:FEED-MIX": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEED-MIX",
        "block_type": "HEATER",
        "composite": "FEED-MIX!HEATER",
        "message": "Block FEED-MIX (HEATER) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEED-MIX\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a6c7e44d982c03d4": {
      "operation": "create_rstoic",
      "parameters": {
        "block_name": "REACT"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:REACT"
      ],
      "dependency_versions": {
        "block:REACT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "REACT",
        "block_type": "RSTOIC",
        "composite": "REACT!RSTOIC",
        "message": "Block REACT (RSTOIC) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "REACT",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\REACT\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "REACT",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\REACT\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\REACT\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a2421e5bf09b3395": {
      "operation": "create_flash2",
      "parameters": {
        "block_name": "HP-SEP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:HP-SEP"
      ],
      "dependency_versions": {
        "block:HP-SEP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "HP-SEP",
        "block_type": "FLASH2",
        "composite": "HP-SEP!FLASH2",
        "message": "Block HP-SEP (FLASH2) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "HP-SEP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "HP-SEP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\HP-SEP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "9d6acd9818f63c1d": {
      "operation": "create_fsplit",
      "parameters": {
        "block_name": "VFLOW"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VFLOW"
      ],
      "dependency_versions": {
        "block:VFLOW": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VFLOW",
        "block_type": "FSPLIT",
        "composite": "VFLOW!FSPLIT",
        "message": "Block VFLOW (FSPLIT) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VFLOW",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXOL"
              ]
            },
            {
              "block": "VFLOW",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXIT",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXIT"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "315f45151cc00f4e": {
      "operation": "create_compr",
      "parameters": {
        "block_name": "COMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:COMP"
      ],
      "dependency_versions": {
        "block:COMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "COMP",
        "block_type": "COMPR",
        "composite": "COMP!COMPR",
        "message": "Block COMP (COMPR) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "COMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\COMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "COMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\COMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\COMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "608a52d659fb4d06": {
      "operation": "create_valve",
      "parameters": {
        "block_name": "VALVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VALVE"
      ],
      "dependency_versions": {
        "block:VALVE": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VALVE",
        "block_type": "VALVE",
        "composite": "VALVE!VALVE",
        "message": "Block VALVE (VALVE) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "VALVE",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXIT",
              "before": 50,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VALVE",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\VALVE\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "46b80b341908af9d": {
      "operation": "create_fsplit",
      "parameters": {
        "block_name": "LFLOW"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:LFLOW"
      ],
      "dependency_versions": {
        "block:LFLOW": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "LFLOW",
        "block_type": "FSPLIT",
        "composite": "LFLOW!FSPLIT",
        "message": "Block LFLOW (FSPLIT) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [],
          "unchanged": [],
          "failed": [],
          "missing": [
            {

...[context truncated for ReAct baseline prompt]...
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 0
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "event": "preflight",
    "health": {
      "status": "healthy"
    },
    "task_hash": "<REDACTED_TASK_ID>"
  },
  {
    "event": "session_started"
  },
  {
    "truncated": true,
    "chars": 9822,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 25, \"actions_executed\": 25, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"add_components_by_cas\", \"parameters\": {\"components\": [{\"component_id\": \"H2\", \"cas\": \"1333-74-0\"}, {\"component_id\": \"N2\", \"cas\": \"7727-37-9\"}, {\"component_id\": \"CH4\", \"cas\": \"74-82-8\"}, {\"component_id\": \"BENZENE\", \"cas\": \"71-43-2\"}, {\"component_id\": \"CYCLOHEX\", \"cas\": \"110-82-7\"}]}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Added 5 component(s) successfully\"}}, {\"truncated\": true, \"chars\": 525, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"ensure_property_method\\\", \\\"parameters\\\": {\\\"method\\\": \\\"RK-SOAVE\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"set_property_method\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"set_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"set_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"get_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"ge\\n...[truncated]\"}, {\"truncated\": true, \"chars\": 1611, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"create_material_streams\\\", \\\"parameters\\\": {\\\"stream_names\\\": [\\\"BZIN\\\", \\\"H2IN\\\", \\\"BZIN2\\\", \\\"H2RCY2\\\", \\\"RXIN\\\", \\\"RXOUT\\\", \\\"VAP\\\", \\\"H2RCY\\\", \\\"PURGE\\\", \\\"PURGE2\\\", \\\"LIQ\\\", \\\"COLFD\\\", \\\"CHRCY\\\", \\\"CHRCY2\\\", \\\"CHRCY3\\\", \\\"LTENDS\\\", \\\"PRODUCT\\\"]}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"create_material_streams\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"create_material_streams\\\", \\\"success\\\": \\n...[truncated]\"}, {\"event\": \"tool_result\", \"operation\": \"create_pump\", \"parameters\": {\"block_name\": \"FEEDPUMP\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Block FEEDPUMP (PUMP) created successfully\", \"block_name\": \"FEEDPUMP\"}}, {\"event\": \"tool_result\", \"operation\": \"create_heater\", \"parameters\": {\"block_name\": \"FEED-MIX\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Block FEED-MIX (HEATER) created successfully\", \"block_name\": \"FEED-MIX\"}}, {\"event\": \"tool_result\", \"operation\": \"create_rstoic\", \"parameters\": {\"block_name\": \"REACT\"}, \"facade\": true, \n...[truncated]"
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Topology and core specs are created but not connected/configured; batch the figure-backed connections and task specs using typed helpers, leaving run/evidence for after completion repair.","action":"mcp_plan","parameters":{"actions":[{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"FEEDPUMP","inlet_stream":"BZIN","outlet_stream":"BZIN2"}},{"operation":"connect_shared_material_port_block","parameters":{"block_name":"FEED-MIX","inlet_streams":["BZIN2","H2IN","H2RCY2","CHRCY3"],"outlet_streams":["RXIN"]}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"REACT","inlet_stream":"RXIN","outlet_stream":"RXOUT"}},{"operation":"connect_flash2_vapor_liquid_ports","parameters":{"block_name":"HP-SEP","feed_stream":"RXOUT","vapor_stream":"VAP","liquid_stream":"LIQ"}},{"operation":"configure_fsplit_shared_outlets","parameters":{"block_name":"VFLOW","inlet_stream":"VAP","outlet_streams":["H2RCY","PURGE"],"split_fractions":{"H2RCY":0.92}}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"COMP","inlet_stream":"H2RCY","outlet_stream":"H2RCY2"}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"VALVE","inlet_stream":"PURGE","outlet_stream":"PURGE2"}},{"operation":"configure_fsplit_shared_outlets","parameters":{"block_name":"LFLOW","inlet_stream":"LIQ","outlet_streams":["CHRCY","COLFD"],"split_fractions":{"CHRCY":0.30}}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"PUMP","inlet_stream":"CHRCY","outlet_stream":"CHRCY2"}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"PIPE","inlet_stream":"CHRCY2","outlet_stream":"CHRCY3"}},{"operation":"connect_stream","parameters":{"block_name":"COLUMN","stream_name":"COLFD","port_name":"F(IN)"}},{"operation":"connect_stream","parameters":{"block_name":"COLUMN","stream_name":"LTENDS","port_name":"VD(OUT)"}},{"operation":"connect_stream","parameters":{"block_name":"COLUMN","stream_name":"PRODUCT","port_name":"B(OUT)"}},{"operation":"set_material_stream_conditions","parameters":{"stream_name":"H2IN","mixed_spec":"TP","temperature":50.0,"temperature_unit":"C","pressure":2.5,"pressure_unit":"MPa"}},{"operation":"set_material_stream_composition","parameters":{"stream_name":"H2IN","basis":"MOLE-FLOW","flows":{"H2":321.75,"N2":1.65,"CH4":6.6},"flow_unit":"kmol/hr"}},{"operation":"set_material_stream_conditions","parameters":{"stream_name":"BZIN","mixed_spec":"TP","temperature":40.0,"temperature_unit":"C","pressure":0.1,"pressure_unit":"MPa"}},{"operation":"set_material_stream_composition","parameters":{"stream_name":"BZIN","basis":"MOLE-FLOW","flows":{"BENZENE":100.0},"flow_unit":"kmol/hr"}},{"operation":"set_pump_outlet_spec","parameters":{"block_name":"FEEDPUMP","value":"USE-CURVE"}},{"operation":"set_opt_ctype","parameters":{"block_name":"FEEDPUMP","value":"SINGLE-OPER"}},{"operation":"set_opt_cformat","parameters":{"block_name":"FEEDPUMP","value":"TABLE"}},{"operation":"set_dep_var","parameters":{"block_name":"FEEDPUMP","value":"HEAD"}},{"operation":"set_indep_var","parameters":{"block_name":"FEEDPUMP","value":"VOL-FLOW"}},{"operation":"set_pump_curve_table","parameters":{"block_name":"FEEDPUMP","curve_idx":1,"flow_unit":"m3/hr","head_unit":"m","curve_points":[{"flow":20.0,"head":40.0},{"flow":10.0,"head":250.0},{"flow":5.0,"head":300.0},{"flow":3.0,"head":400.0}]}},{"operation":"set_eff","parameters":{"block_name":"FEEDPUMP","value":0.6}},{"operation":"set_deff","parameters":{"block_name":"FEEDPUMP","value":0.9}},{"operation":"set_heater_flash_spec","parameters":{"block_name":"FEED-MIX","value":"TP"}},{"operation":"set_heater_temperature","parameters":{"block_name":"FEED-MIX","value":150.0,"unit":"C"}},{"operation":"set_heater_pressure","parameters":{"block_name":"FEED-MIX","value":2.3,"unit":"MPa"}},{"operation":"configure_rstoic_stoichiometry","parameters":{"block_name":"REACT","reaction_number":1,"reactants":{"BENZENE":1.0,"H2":3.0},"products":{"CYCLOHEX":1.0}}},{"operation":"configure_rstoic_fractional_conversions","parameters":{"block_name":"REACT","conversions":[{"reaction_number":1,"component_id":"BENZENE","conversion":0.998}]}},{"operation":"configure_rstoic_flash","parameters":{"block_name":"REACT","spec_opt":"TP","temperature":200.0,"temperature_unit":"C","pressure":-0.1,"pressure_unit":"MPa"}},{"operation":"configure_flash2_operating_specs","parameters":{"block_name":"HP-SEP","spec_opt":"TP","temperature":50.0,"temperature_unit":"C","pressure":-0.05,"pressure_unit":"MPa"}},{"operation":"set_pump_outlet_spec","parameters":{"block_name":"PUMP","value":"PRES"}},{"operation":"set_pump_outlet_pressure","parameters":{"block_name":"PUMP","value":2.6,"unit":"MPa"}},{"operation":"configure_compr_pressure_rise","parameters":{"block_name":"COMP","delta_pressure":0.4,"pressure_unit":"MPa","compressor_type":"ISENTROPIC"}},{"operation":"configure_valve_outlet_pressure_design","parameters":{"block_name":"VALVE","outlet_pressure":2.0,"pressure_unit":"MPa","vendor_preset_id":"neles_globe_v810_equal_pct_1p5in"}},{"operation":"configure_pipe_schedule_sizing","parameters":{"block_name":"PIPE","material":"CARBON-STEEL","schedule":40,"nominal_diam":"1-IN","length":25.0,"length_unit":"meter"}},{"operation":"set_radfrac_condenser_type","parameters":{"block_name":"COLUMN","value":"PARTIAL-V"}},{"operation":"set_radfrac_reboiler_type","parameters":{"block_name":"COLUMN","value":"KETTLE"}},{"operation":"set_radfrac_stage_count","parameters":{"block_name":"COLUMN","value":12}},{"operation":"set_radfrac_feed_stage","parameters":{"block_name":"COLUMN","stream_name":"COLFD","value":8}},{"operation":"configure_radfrac_feed_convention","parameters":{"block_name":"COLUMN","stream_name":"COLFD","convention":"ON-STAGE-LIQ"}},{"operation":"set_radfrac_top_pressure","parameters":{"block_name":"COLUMN","value":1.5,"unit":"MPa"}},{"operation":"set_radfrac_reflux_ratio","parameters":{"block_name":"COLUMN","value":1.2}},{"operation":"set_radfrac_distillate_rate","parameters":{"block_name":"COLUMN","value":99.0,"unit":"kmol/hr"}},{"operation":"configure_recycle_convergence_options","parameters":{"tolerance":1e-5,"tear_method":"WEGSTEIN","wegstein_max_iterations":200}},{"operation":"probe_model_state","parameters":{"stream_names":["BZIN","H2IN","PRODUCT"],"block_names":["FEEDPUMP","FEED-MIX","REACT","HP-SEP","VFLOW","LFLOW","COLUMN"],"include_flowsheet":true,"include_ui_next":false}}]}}

{"thought":"Batch topology and all primary equipment/feed specifications now; defer run/evidence until completion status is known.","action":"mcp_plan","parameters":{"actions":[{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"FEEDPUMP","inlet_stream":"BZIN","outlet_stream":"BZIN2"}},{"operation":"connect_shared_material_port_block","parameters":{"block_name":"FEED-MIX","inlet_streams":["BZIN2","H2IN","H2RCY2","CHRCY3"],"outlet_streams":["RXIN"]}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"REACT","inlet_stream":"RXIN","outlet_stream":"RXOUT"}},{"operation":"connect_flash2_vapor_liquid_ports","parameters":{"block_name":"HP-SEP","feed_stream":"RXOUT","vapor_stream":"VAP","liquid_stream":"LIQ"}},{"operation":"configure_fsplit_shared_outlets","parameters":{"block_name":"VFLOW","inlet_stream":"VAP","outlet_streams":["H2RCY","PURGE"],"split_fractions":{"H2RCY":0.92}}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"COMP","inlet_stream":"H2RCY","outlet_stream":"H2RCY2"}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"VALVE","inlet_stream":"PURGE","outlet_stream":"PURGE2"}},{"operation":"configure_fsplit_shared_outlets","parameters":{"block_name":"LFLOW","inlet_stream":"LIQ","outlet_streams":["CHRCY","COLFD"],"split_fractions":{"CHRCY":0.3}}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"PUMP","inlet_stream":"CHRCY","outlet_stream":"CHRCY2"}},{"operation":"connect_material_inlet_outlet","parameters":{"block_name":"PIPE","inlet_stream":"CHRCY2","outlet_stream":"CHRCY3"}},{"operation":"connect_stream","parameters":{"block_name":"COLUMN","stream_name":"COLFD","port_name":"F(IN)"}},{"operation":"connect_stream","parameters":{"block_name":"COLUMN","stream_name":"LTENDS","port_name":"VD(OUT)"}},{"operation":"connect_stream","parameters":{"block_name":"COLUMN","stream_name":"PRODUCT","port_name":"B(OUT)"}},{"operation":"set_material_stream_conditions","parameters":{"stream_name":"H2IN","mixed_spec":"TP","temperature":50.0,"temperature_unit":"C","pressure":2.5,"pressure_unit":"MPa"}},{"operation":"set_material_stream_composition","parameters":{"stream_name":"H2IN","basis":"MOLE-FLOW","flows":{"H2":321.75,"N2":1.65,"CH4":6.6},"flow_unit":"kmol/hr"}},{"operation":"set_material_stream_conditions","parameters":{"stream_name":"BZIN","mixed_spec":"TP","temperature":40.0,"temperature_unit":"C","pressure":0.1,"pressure_unit":"MPa"}},{"operation":"set_material_stream_composition","parameters":{"stream_name":"BZIN","basis":"MOLE-FLOW","flows":{"BENZENE":100.0},"flow_unit":"kmol/hr"}},{"operation":"set_pump_outlet_spec","parameters":{"block_name":"FEEDPUMP","value":"USE-CURVE"}},{"operation":"set_opt_ctype","parameters":{"block_name":"FEEDPUMP","value":"SINGLE-OPER"}},{"operation":"set_opt_cformat","parameters":{"block_name":"FEEDPUMP","value":"TABLE"}},{"operation":"set_dep_var","parameters":{"block_name":"FEEDPUMP","value":"HEAD"}},{"operation":"set_indep_var","parameters":{"block_name":"FEEDPUMP","value":"VOL-FLOW"}},{"operation":"set_pump_curve_table","parameters":{"block_name":"FEEDPUMP","curve_idx":1,"flow_unit":"m3/hr","head_unit":"m","curve_points":[{"flow":20.0,"head":40.0},{"flow":10.0,"head":250.0},{"flow":5.0,"head":300.0},{"flow":3.0,"head":400.0}]}},{"operation":"set_eff","parameters":{"block_name":"FEEDPUMP","value":0.6}},{"operation":"set_deff","parameters":{"block_name":"FEEDPUMP","value":0.9}},{"operation":"set_heater_flash_spec","parameters":{"block_name":"FEED-MIX","value":"TP"}},{"operation":"set_heater_temperature","parameters":{"block_name":"FEED-MIX","value":150.0,"unit":"C"}},{"operation":"set_heater_pressure","parameters":{"block_name":"FEED-MIX","value":2.3,"unit":"MPa"}},{"operation":"configure_rstoic_stoichiometry","parameters":{"block_name":"REACT","reaction_number":1,"reactants":{"BENZENE":1.0,"H2":3.0},"products":{"CYCLOHEX":1.0}}},{"operation":"configure_rstoic_fractional_conversions","parameters":{"block_name":"REACT","conversions":[{"reaction_number":1,"component_id":"BENZENE","conversion":0.998}]}},{"operation":"configure_rstoic_flash","parameters":{"block_name":"REACT","spec_opt":"TP","temperature":200.0,"temperature_unit":"C","pressure":-0.1,"pressure_unit":"MPa"}},{"operation":"configure_flash2_operating_specs","parameters":{"block_name":"HP-SEP","spec_opt":"TP","temperature":50.0,"temperature_unit":"C","pressure":-0.05,"pressure_unit":"MPa"}},{"operation":"set_pump_outlet_spec","parameters":{"block_name":"PUMP","value":"PRES"}},{"operation":"set_pump_outlet_pressure","parameters":{"block_name":"PUMP","value":2.6,"unit":"MPa"}},{"operation":"configure_compr_pressure_rise","parameters":{"block_name":"COMP","delta_pressure":0.4,"pressure_unit":"MPa","compressor_type":"ISENTROPIC"}},{"operation":"configure_valve_outlet_pressure_design","parameters":{"block_name":"VALVE","outlet_pressure":2.0,"pressure_unit":"MPa","vendor_preset_id":"neles_globe_v810_equal_pct_1p5in"}},{"operation":"configure_pipe_schedule_sizing","parameters":{"block_name":"PIPE","material":"CARBON-STEEL","schedule":40,"nominal_diam":"1-IN","length":25.0,"length_unit":"meter"}},{"operation":"set_radfrac_condenser_type","parameters":{"block_name":"COLUMN","value":"PARTIAL-V"}},{"operation":"set_radfrac_reboiler_type","parameters":{"block_name":"COLUMN","value":"KETTLE"}},{"operation":"set_radfrac_stage_count","parameters":{"block_name":"COLUMN","value":12}},{"operation":"set_radfrac_feed_stage","parameters":{"block_name":"COLUMN","stream_name":"COLFD","value":8}},{"operation":"configure_radfrac_feed_convention","parameters":{"block_name":"COLUMN","stream_name":"COLFD","convention":"ON-STAGE-LIQ"}},{"operation":"set_radfrac_top_pressure","parameters":{"block_name":"COLUMN","value":1.5,"unit":"MPa"}},{"operation":"set_radfrac_reflux_ratio","parameters":{"block_name":"COLUMN","value":1.2}},{"operation":"set_radfrac_distillate_rate","parameters":{"block_name":"COLUMN","value":99.0,"unit":"kmol/hr"}},{"operation":"configure_recycle_convergence_options","parameters":{"tolerance":1e-5,"tear_method":"WEGSTEIN","wegstein_max_iterations":200}},{"operation":"probe_model_state","parameters":{"stream_names":["BZIN","H2IN","PRODUCT"],"block_names":["FEEDPUMP","FEED-MIX","REACT","HP-SEP","VFLOW","LFLOW","COLUMN"],"include_flowsheet":true,"include_ui_next":false}}]}}
```

</details>

## Call 3: `select_action`

- Input tokens: **131,210**
- Output tokens: **401**
- Total tokens: **131,611**
- Provider cost: **$0.668080**
- Recorded at: `2026-10-18T20:59:30.641`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 71,
    "domain_versions": {
      "properties": 2,
      "flowsheet": 71,
      "stream:H2RCY2": 5,
      "stream:CHRCY2": 5,
      "stream:LIQ": 5,
      "stream:RXOUT": 5,
      "stream:PURGE": 5,
      "stream:BZIN": 5,
      "stream:PRODUCT": 3,
      "stream:H2IN": 5,
      "stream:CHRCY3": 5,
      "stream:LTENDS": 3,
      "stream:BZIN2": 5,
      "stream:VAP": 5,
      "stream:H2RCY": 5,
      "stream:PURGE2": 3,
      "stream:CHRCY": 5,
      "stream:RXIN": 5,
      "stream:COLFD": 7,
      "block:FEEDPUMP": 11,
      "block:FEED-MIX": 6,
      "block:REACT": 6,
      "block:HP-SEP": 4,
      "block:VFLOW": 3,
      "block:COMP": 4,
      "block:VALVE": 4,
      "block:LFLOW": 3,
      "block:PUMP": 5,
      "block:PIPE": 4,
      "block:COLUMN": 13
    },
    "components": [
      "H2",
      "N2",
      "CH4",
      "BENZENE",
      "CYCLOHEX"
    ],
    "property_method": "",
    "blocks": [
      "FEEDPUMP",
      "FEED-MIX",
      "REACT",
      "HP-SEP",
      "VFLOW",
      "COMP",
      "VALVE",
      "LFLOW",
      "PUMP",
      "PIPE",
      "COLUMN"
    ],
    "streams": [
      "BZIN",
      "H2IN",
      "BZIN2",
      "H2RCY2",
      "RXIN",
      "RXOUT",
      "VAP",
      "H2RCY",
      "PURGE",
      "PURGE2",
      "LIQ",
      "COLFD",
      "CHRCY",
      "CHRCY2",
      "CHRCY3",
      "LTENDS",
      "PRODUCT"
    ],
    "connections": [
      {
        "block_name": "COLUMN",
        "stream_name": "COLFD",
        "port_name": "F(IN)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "LTENDS",
        "port_name": "VD(OUT)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "PRODUCT",
        "port_name": "B(OUT)",
        "source_operation": "connect_stream"
      }
    ],
    "specs": [
      {
        "stream_name": "H2IN",
        "temperature": 50.0,
        "pressure": 2.5,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      },
      {
        "stream_name": "BZIN",
        "temperature": 40.0,
        "pressure": 0.1,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      }
    ],
    "engine_run": null,
    "artifacts": {},
    "readbacks": []
  },
  "operation_ledger": {
    "677ff79d23598058": {
      "operation": "add_components_by_cas",
      "parameters": {
        "components": [
          {
            "component_id": "H2",
            "cas": "1333-74-0"
          },
          {
            "component_id": "N2",
            "cas": "7727-37-9"
          },
          {
            "component_id": "CH4",
            "cas": "74-82-8"
          },
          {
            "component_id": "BENZENE",
            "cas": "71-43-2"
          },
          {
            "component_id": "CYCLOHEX",
            "cas": "110-82-7"
          }
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "components_added": [
          {
            "cas": "1333740",
            "component_id": "H2",
            "requested_component_id": "H2",
            "preferred_component_id": "H2"
          },
          {
            "cas": "7727379",
            "component_id": "N2",
            "requested_component_id": "N2",
            "preferred_component_id": "N2"
          },
          {
            "cas": "74-82-8",
            "component_id": "CH4",
            "requested_component_id": "CH4",
            "preferred_component_id": "CH4"
          },
          {
            "cas": "71-43-2",
            "component_id": "BENZENE",
            "requested_component_id": "BENZENE",
            "preferred_component_id": "BENZENE"
          },
          {
            "cas": "110-82-7",
            "component_id": "CYCLOHEX",
            "requested_component_id": "CYCLOHEX",
            "preferred_component_id": "CYCLOHEX"
          }
        ],
        "count": 5,
        "message": "Added 5 component(s) successfully",
        "verification": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "missing_component_ids": []
        },
        "contamination": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "extra_component_ids": [],
          "generic_extra_component_ids": []
        }
      }
    },
    "d0f7c037faabb2bb": {
      "operation": "ensure_property_method",
      "parameters": {
        "method": "RK-SOAVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 2
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "ensure_property_method",
        "steps_completed": 5,
        "steps_total": 5,
        "last_result": null
      }
    },
    "33ce8ec6c91a3f71": {
      "operation": "create_material_streams",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "stream:BZIN",
        "stream:H2IN",
        "stream:BZIN2",
        "stream:H2RCY2",
        "stream:RXIN",
        "stream:RXOUT",
        "stream:VAP",
        "stream:H2RCY",
        "stream:PURGE",
        "stream:PURGE2",
        "stream:LIQ",
        "stream:COLFD",
        "stream:CHRCY",
        "stream:CHRCY2",
        "stream:CHRCY3",
        "stream:LTENDS",
        "stream:PRODUCT"
      ],
      "dependency_versions": {
        "stream:BZIN": 1,
        "stream:H2IN": 1,
        "stream:BZIN2": 1,
        "stream:H2RCY2": 1,
        "stream:RXIN": 1,
        "stream:RXOUT": 1,
        "stream:VAP": 1,
        "stream:H2RCY": 1,
        "stream:PURGE": 1,
        "stream:PURGE2": 1,
        "stream:LIQ": 1,
        "stream:COLFD": 1,
        "stream:CHRCY": 1,
        "stream:CHRCY2": 1,
        "stream:CHRCY3": 1,
        "stream:LTENDS": 1,
        "stream:PRODUCT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "create_material_streams",
        "steps_completed": 17,
        "steps_total": 17,
        "last_result": null
      }
    },
    "aeeab72bf4e897bd": {
      "operation": "create_pump",
      "parameters": {
        "block_name": "FEEDPUMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEEDPUMP"
      ],
      "dependency_versions": {
        "block:FEEDPUMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEEDPUMP",
        "block_type": "PUMP",
        "composite": "FEEDPUMP!PUMP",
        "message": "Block FEEDPUMP (PUMP) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "0909126309d406aa": {
      "operation": "create_heater",
      "parameters": {
        "block_name": "FEED-MIX"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEED-MIX"
      ],
      "dependency_versions": {
        "block:FEED-MIX": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEED-MIX",
        "block_type": "HEATER",
        "composite": "FEED-MIX!HEATER",
        "message": "Block FEED-MIX (HEATER) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEED-MIX\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a6c7e44d982c03d4": {
      "operation": "create_rstoic",
      "parameters": {
        "block_name": "REACT"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:REACT"
      ],
      "dependency_versions": {
        "block:REACT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "REACT",
        "block_type": "RSTOIC",
        "composite": "REACT!RSTOIC",
        "message": "Block REACT (RSTOIC) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "REACT",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\REACT\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "REACT",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\REACT\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\REACT\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a2421e5bf09b3395": {
      "operation": "create_flash2",
      "parameters": {
        "block_name": "HP-SEP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:HP-SEP"
      ],
      "dependency_versions": {
        "block:HP-SEP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "HP-SEP",
        "block_type": "FLASH2",
        "composite": "HP-SEP!FLASH2",
        "message": "Block HP-SEP (FLASH2) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "HP-SEP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "HP-SEP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\HP-SEP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "9d6acd9818f63c1d": {
      "operation": "create_fsplit",
      "parameters": {
        "block_name": "VFLOW"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VFLOW"
      ],
      "dependency_versions": {
        "block:VFLOW": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VFLOW",
        "block_type": "FSPLIT",
        "composite": "VFLOW!FSPLIT",
        "message": "Block VFLOW (FSPLIT) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VFLOW",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXOL"
              ]
            },
            {
              "block": "VFLOW",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXIT",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXIT"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "315f45151cc00f4e": {
      "operation": "create_compr",
      "parameters": {
        "block_name": "COMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:COMP"
      ],
      "dependency_versions": {
        "block:COMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "COMP",
        "block_type": "COMPR",
        "composite": "COMP!COMPR",
        "message": "Block COMP (COMPR) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "COMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\COMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "COMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\COMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\COMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "608a52d659fb4d06": {
      "operation": "create_valve",
      "parameters": {
        "block_name": "VALVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VALVE"
      ],
      "dependency_versions": {
        "block:VALVE": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VALVE",
        "block_type": "VALVE",
        "composite": "VALVE!VALVE",
        "message": "Block VALVE (VALVE) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "VALVE",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXIT",
              "before": 50,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VALVE",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXOL",
              "attempted_paths": [

...[context truncated for ReAct baseline prompt]...
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 0
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "event": "preflight",
    "health": {
      "status": "healthy"
    },
    "task_hash": "<REDACTED_TASK_ID>"
  },
  {
    "event": "session_started"
  },
  {
    "truncated": true,
    "chars": 9822,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 25, \"actions_executed\": 25, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"add_components_by_cas\", \"parameters\": {\"components\": [{\"component_id\": \"H2\", \"cas\": \"1333-74-0\"}, {\"component_id\": \"N2\", \"cas\": \"7727-37-9\"}, {\"component_id\": \"CH4\", \"cas\": \"74-82-8\"}, {\"component_id\": \"BENZENE\", \"cas\": \"71-43-2\"}, {\"component_id\": \"CYCLOHEX\", \"cas\": \"110-82-7\"}]}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Added 5 component(s) successfully\"}}, {\"truncated\": true, \"chars\": 525, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"ensure_property_method\\\", \\\"parameters\\\": {\\\"method\\\": \\\"RK-SOAVE\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"set_property_method\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"set_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"set_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"get_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"ge\\n...[truncated]\"}, {\"truncated\": true, \"chars\": 1611, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"create_material_streams\\\", \\\"parameters\\\": {\\\"stream_names\\\": [\\\"BZIN\\\", \\\"H2IN\\\", \\\"BZIN2\\\", \\\"H2RCY2\\\", \\\"RXIN\\\", \\\"RXOUT\\\", \\\"VAP\\\", \\\"H2RCY\\\", \\\"PURGE\\\", \\\"PURGE2\\\", \\\"LIQ\\\", \\\"COLFD\\\", \\\"CHRCY\\\", \\\"CHRCY2\\\", \\\"CHRCY3\\\", \\\"LTENDS\\\", \\\"PRODUCT\\\"]}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"create_material_streams\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"create_material_streams\\\", \\\"success\\\": \\n...[truncated]\"}, {\"event\": \"tool_result\", \"operation\": \"create_pump\", \"parameters\": {\"block_name\": \"FEEDPUMP\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Block FEEDPUMP (PUMP) created successfully\", \"block_name\": \"FEEDPUMP\"}}, {\"event\": \"tool_result\", \"operation\": \"create_heater\", \"parameters\": {\"block_name\": \"FEED-MIX\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Block FEED-MIX (HEATER) created successfully\", \"block_name\": \"FEED-MIX\"}}, {\"event\": \"tool_result\", \"operation\": \"create_rstoic\", \"parameters\": {\"block_name\": \"REACT\"}, \"facade\": true, \n...[truncated]"
  },
  {
    "truncated": true,
    "chars": 19494,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 47, \"actions_executed\": 47, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"connect_material_inlet_outlet\", \"parameters\": {\"block_name\": \"FEEDPUMP\", \"inlet_stream\": \"BZIN\", \"outlet_stream\": \"BZIN2\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"list_block_ports\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"connect_shared_material_port_block\", \"parameters\": {\"block_name\": \"FEED-MIX\", \"inlet_streams\": [\"BZIN2\", \"H2IN\", \"H2RCY2\", \"CHRCY3\"], \"outlet_streams\": [\"RXIN\"]}, \"facade\": true, \"translated_operations\": [{\"operation\": \"connect_shared_material_port_block\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"connect_material_inlet_outlet\", \"parameters\": {\"block_name\": \"REACT\", \"inlet_stream\": \"RXIN\", \"outlet_stream\": \"RXOUT\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"list_block_ports\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"truncated\": true, \"chars\": 549, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"connect_flash2_vapor_liquid_ports\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"HP-SEP\\\", \\\"feed_stream\\\": \\\"RXOUT\\\", \\\"vapor_stream\\\": \\\"VAP\\\", \\\"liquid_stream\\\": \\\"LIQ\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"list_block_ports\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"connect_stream\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"connect_stream\\\", \\\"success\\\": true, \\\"error\\\": nu\\n...[truncated]\"}, {\"event\": \"tool_result\", \"operation\": \"configure_fsplit_shared_outlets\", \"parameters\": {\"block_name\": \"VFLOW\", \"inlet_stream\": \"VAP\", \"outlet_streams\": [\"H2RCY\", \"PURGE\"], \"split_fractions\": {\"H2RCY\": 0.92}}, \"facade\": true, \"translated_operations\": [{\"operation\": \"configure_fsplit_shared_outlets\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}\n...[truncated]"
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Check live model completion/readbacks before attempting run; need identify missing specs or topology contradictions from current Aspen state.","action":"mcp_tool","operation":"probe_model_state","parameters":{"stream_names":["BZIN","H2IN","BZIN2","H2RCY2","RXIN","RXOUT","VAP","H2RCY","PURGE","PURGE2","LIQ","COLFD","CHRCY","CHRCY2","CHRCY3","LTENDS","PRODUCT"],"block_names":["FEEDPUMP","FEED-MIX","REACT","HP-SEP","VFLOW","COMP","VALVE","LFLOW","PUMP","PIPE","COLUMN"],"include_flowsheet":true,"include_ui_next":true}}
```

</details>

## Call 4: `select_action`

- Input tokens: **131,411**
- Output tokens: **189**
- Total tokens: **131,600**
- Provider cost: **$0.662725**
- Recorded at: `2026-10-18T21:00:10.730`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 71,
    "domain_versions": {
      "properties": 2,
      "flowsheet": 71,
      "stream:H2RCY2": 5,
      "stream:CHRCY2": 5,
      "stream:LIQ": 5,
      "stream:RXOUT": 5,
      "stream:PURGE": 5,
      "stream:BZIN": 5,
      "stream:PRODUCT": 3,
      "stream:H2IN": 5,
      "stream:CHRCY3": 5,
      "stream:LTENDS": 3,
      "stream:BZIN2": 5,
      "stream:VAP": 5,
      "stream:H2RCY": 5,
      "stream:PURGE2": 3,
      "stream:CHRCY": 5,
      "stream:RXIN": 5,
      "stream:COLFD": 7,
      "block:FEEDPUMP": 11,
      "block:FEED-MIX": 6,
      "block:REACT": 6,
      "block:HP-SEP": 4,
      "block:VFLOW": 3,
      "block:COMP": 4,
      "block:VALVE": 4,
      "block:LFLOW": 3,
      "block:PUMP": 5,
      "block:PIPE": 4,
      "block:COLUMN": 13
    },
    "components": [
      "H2",
      "N2",
      "CH4",
      "BENZENE",
      "CYCLOHEX"
    ],
    "property_method": "",
    "blocks": [
      "FEEDPUMP",
      "FEED-MIX",
      "REACT",
      "HP-SEP",
      "VFLOW",
      "COMP",
      "VALVE",
      "LFLOW",
      "PUMP",
      "PIPE",
      "COLUMN"
    ],
    "streams": [
      "BZIN",
      "H2IN",
      "BZIN2",
      "H2RCY2",
      "RXIN",
      "RXOUT",
      "VAP",
      "H2RCY",
      "PURGE",
      "PURGE2",
      "LIQ",
      "COLFD",
      "CHRCY",
      "CHRCY2",
      "CHRCY3",
      "LTENDS",
      "PRODUCT"
    ],
    "connections": [
      {
        "block_name": "COLUMN",
        "stream_name": "COLFD",
        "port_name": "F(IN)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "LTENDS",
        "port_name": "VD(OUT)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "PRODUCT",
        "port_name": "B(OUT)",
        "source_operation": "connect_stream"
      }
    ],
    "specs": [
      {
        "stream_name": "H2IN",
        "temperature": 50.0,
        "pressure": 2.5,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      },
      {
        "stream_name": "BZIN",
        "temperature": 40.0,
        "pressure": 0.1,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      }
    ],
    "engine_run": null,
    "artifacts": {},
    "readbacks": []
  },
  "operation_ledger": {
    "677ff79d23598058": {
      "operation": "add_components_by_cas",
      "parameters": {
        "components": [
          {
            "component_id": "H2",
            "cas": "1333-74-0"
          },
          {
            "component_id": "N2",
            "cas": "7727-37-9"
          },
          {
            "component_id": "CH4",
            "cas": "74-82-8"
          },
          {
            "component_id": "BENZENE",
            "cas": "71-43-2"
          },
          {
            "component_id": "CYCLOHEX",
            "cas": "110-82-7"
          }
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "components_added": [
          {
            "cas": "1333740",
            "component_id": "H2",
            "requested_component_id": "H2",
            "preferred_component_id": "H2"
          },
          {
            "cas": "7727379",
            "component_id": "N2",
            "requested_component_id": "N2",
            "preferred_component_id": "N2"
          },
          {
            "cas": "74-82-8",
            "component_id": "CH4",
            "requested_component_id": "CH4",
            "preferred_component_id": "CH4"
          },
          {
            "cas": "71-43-2",
            "component_id": "BENZENE",
            "requested_component_id": "BENZENE",
            "preferred_component_id": "BENZENE"
          },
          {
            "cas": "110-82-7",
            "component_id": "CYCLOHEX",
            "requested_component_id": "CYCLOHEX",
            "preferred_component_id": "CYCLOHEX"
          }
        ],
        "count": 5,
        "message": "Added 5 component(s) successfully",
        "verification": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "missing_component_ids": []
        },
        "contamination": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "extra_component_ids": [],
          "generic_extra_component_ids": []
        }
      }
    },
    "d0f7c037faabb2bb": {
      "operation": "ensure_property_method",
      "parameters": {
        "method": "RK-SOAVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 2
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "ensure_property_method",
        "steps_completed": 5,
        "steps_total": 5,
        "last_result": null
      }
    },
    "33ce8ec6c91a3f71": {
      "operation": "create_material_streams",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "stream:BZIN",
        "stream:H2IN",
        "stream:BZIN2",
        "stream:H2RCY2",
        "stream:RXIN",
        "stream:RXOUT",
        "stream:VAP",
        "stream:H2RCY",
        "stream:PURGE",
        "stream:PURGE2",
        "stream:LIQ",
        "stream:COLFD",
        "stream:CHRCY",
        "stream:CHRCY2",
        "stream:CHRCY3",
        "stream:LTENDS",
        "stream:PRODUCT"
      ],
      "dependency_versions": {
        "stream:BZIN": 1,
        "stream:H2IN": 1,
        "stream:BZIN2": 1,
        "stream:H2RCY2": 1,
        "stream:RXIN": 1,
        "stream:RXOUT": 1,
        "stream:VAP": 1,
        "stream:H2RCY": 1,
        "stream:PURGE": 1,
        "stream:PURGE2": 1,
        "stream:LIQ": 1,
        "stream:COLFD": 1,
        "stream:CHRCY": 1,
        "stream:CHRCY2": 1,
        "stream:CHRCY3": 1,
        "stream:LTENDS": 1,
        "stream:PRODUCT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "create_material_streams",
        "steps_completed": 17,
        "steps_total": 17,
        "last_result": null
      }
    },
    "aeeab72bf4e897bd": {
      "operation": "create_pump",
      "parameters": {
        "block_name": "FEEDPUMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEEDPUMP"
      ],
      "dependency_versions": {
        "block:FEEDPUMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEEDPUMP",
        "block_type": "PUMP",
        "composite": "FEEDPUMP!PUMP",
        "message": "Block FEEDPUMP (PUMP) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "0909126309d406aa": {
      "operation": "create_heater",
      "parameters": {
        "block_name": "FEED-MIX"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEED-MIX"
      ],
      "dependency_versions": {
        "block:FEED-MIX": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEED-MIX",
        "block_type": "HEATER",
        "composite": "FEED-MIX!HEATER",
        "message": "Block FEED-MIX (HEATER) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEED-MIX\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a6c7e44d982c03d4": {
      "operation": "create_rstoic",
      "parameters": {
        "block_name": "REACT"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:REACT"
      ],
      "dependency_versions": {
        "block:REACT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "REACT",
        "block_type": "RSTOIC",
        "composite": "REACT!RSTOIC",
        "message": "Block REACT (RSTOIC) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "REACT",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\REACT\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "REACT",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\REACT\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\REACT\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a2421e5bf09b3395": {
      "operation": "create_flash2",
      "parameters": {
        "block_name": "HP-SEP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:HP-SEP"
      ],
      "dependency_versions": {
        "block:HP-SEP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "HP-SEP",
        "block_type": "FLASH2",
        "composite": "HP-SEP!FLASH2",
        "message": "Block HP-SEP (FLASH2) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "HP-SEP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "HP-SEP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\HP-SEP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "9d6acd9818f63c1d": {
      "operation": "create_fsplit",
      "parameters": {
        "block_name": "VFLOW"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VFLOW"
      ],
      "dependency_versions": {
        "block:VFLOW": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VFLOW",
        "block_type": "FSPLIT",
        "composite": "VFLOW!FSPLIT",
        "message": "Block VFLOW (FSPLIT) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VFLOW",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXOL"
              ]
            },
            {
              "block": "VFLOW",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXIT",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXIT"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "315f45151cc00f4e": {
      "operation": "create_compr",
      "parameters": {
        "block_name": "COMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:COMP"
      ],
      "dependency_versions": {
        "block:COMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "COMP",
        "block_type": "COMPR",
        "composite": "COMP!COMPR",
        "message": "Block COMP (COMPR) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "COMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\COMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "COMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\COMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\COMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "608a52d659fb4d06": {
      "operation": "create_valve",
      "parameters": {
        "block_name": "VALVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VALVE"
      ],
      "dependency_versions": {
        "block:VALVE": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VALVE",
        "block_type": "VALVE",
        "composite": "VALVE!VALVE",
        "message": "Block VALVE (VALVE) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "VALVE",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXIT",
              "before": 50,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VALVE",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXOL",
              "attempted_paths": [

...[context truncated for ReAct baseline prompt]...
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 1,
  "event_counts": {
    "preflight": 1
  },
  "operation_counts_top": {},
  "successful_operations_tail": [],
  "failures_tail": [],
  "artifacts_tail": [],
  "validator_feedback_tail": []
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "event": "session_started"
  },
  {
    "truncated": true,
    "chars": 9822,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 25, \"actions_executed\": 25, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"add_components_by_cas\", \"parameters\": {\"components\": [{\"component_id\": \"H2\", \"cas\": \"1333-74-0\"}, {\"component_id\": \"N2\", \"cas\": \"7727-37-9\"}, {\"component_id\": \"CH4\", \"cas\": \"74-82-8\"}, {\"component_id\": \"BENZENE\", \"cas\": \"71-43-2\"}, {\"component_id\": \"CYCLOHEX\", \"cas\": \"110-82-7\"}]}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Added 5 component(s) successfully\"}}, {\"truncated\": true, \"chars\": 525, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"ensure_property_method\\\", \\\"parameters\\\": {\\\"method\\\": \\\"RK-SOAVE\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"set_property_method\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"set_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"set_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"get_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"ge\\n...[truncated]\"}, {\"truncated\": true, \"chars\": 1611, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"create_material_streams\\\", \\\"parameters\\\": {\\\"stream_names\\\": [\\\"BZIN\\\", \\\"H2IN\\\", \\\"BZIN2\\\", \\\"H2RCY2\\\", \\\"RXIN\\\", \\\"RXOUT\\\", \\\"VAP\\\", \\\"H2RCY\\\", \\\"PURGE\\\", \\\"PURGE2\\\", \\\"LIQ\\\", \\\"COLFD\\\", \\\"CHRCY\\\", \\\"CHRCY2\\\", \\\"CHRCY3\\\", \\\"LTENDS\\\", \\\"PRODUCT\\\"]}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"create_material_streams\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"create_material_streams\\\", \\\"success\\\": \\n...[truncated]\"}, {\"event\": \"tool_result\", \"operation\": \"create_pump\", \"parameters\": {\"block_name\": \"FEEDPUMP\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Block FEEDPUMP (PUMP) created successfully\", \"block_name\": \"FEEDPUMP\"}}, {\"event\": \"tool_result\", \"operation\": \"create_heater\", \"parameters\": {\"block_name\": \"FEED-MIX\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Block FEED-MIX (HEATER) created successfully\", \"block_name\": \"FEED-MIX\"}}, {\"event\": \"tool_result\", \"operation\": \"create_rstoic\", \"parameters\": {\"block_name\": \"REACT\"}, \"facade\": true, \n...[truncated]"
  },
  {
    "truncated": true,
    "chars": 19494,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 47, \"actions_executed\": 47, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"connect_material_inlet_outlet\", \"parameters\": {\"block_name\": \"FEEDPUMP\", \"inlet_stream\": \"BZIN\", \"outlet_stream\": \"BZIN2\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"list_block_ports\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"connect_shared_material_port_block\", \"parameters\": {\"block_name\": \"FEED-MIX\", \"inlet_streams\": [\"BZIN2\", \"H2IN\", \"H2RCY2\", \"CHRCY3\"], \"outlet_streams\": [\"RXIN\"]}, \"facade\": true, \"translated_operations\": [{\"operation\": \"connect_shared_material_port_block\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"connect_material_inlet_outlet\", \"parameters\": {\"block_name\": \"REACT\", \"inlet_stream\": \"RXIN\", \"outlet_stream\": \"RXOUT\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"list_block_ports\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"truncated\": true, \"chars\": 549, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"connect_flash2_vapor_liquid_ports\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"HP-SEP\\\", \\\"feed_stream\\\": \\\"RXOUT\\\", \\\"vapor_stream\\\": \\\"VAP\\\", \\\"liquid_stream\\\": \\\"LIQ\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"list_block_ports\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"connect_stream\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"connect_stream\\\", \\\"success\\\": true, \\\"error\\\": nu\\n...[truncated]\"}, {\"event\": \"tool_result\", \"operation\": \"configure_fsplit_shared_outlets\", \"parameters\": {\"block_name\": \"VFLOW\", \"inlet_stream\": \"VAP\", \"outlet_streams\": [\"H2RCY\", \"PURGE\"], \"split_fractions\": {\"H2RCY\": 0.92}}, \"facade\": true, \"translated_operations\": [{\"operation\": \"configure_fsplit_shared_outlets\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}\n...[truncated]"
  },
  {
    "event": "tool_result",
    "operation": "probe_model_state",
    "parameters": {
      "stream_names": [
        "BZIN",
        "H2IN",
        "BZIN2",
        "H2RCY2",
        "RXIN",
        "RXOUT",
        "VAP",
        "H2RCY",
        "PURGE",
        "PURGE2",
        "LIQ",
        "COLFD",
        "CHRCY",
        "CHRCY2",
        "CHRCY3",
        "LTENDS",
        "PRODUCT"
      ],
      "block_names": [
        "FEEDPUMP",
        "FEED-MIX",
        "REACT",
        "HP-SEP",
        "VFLOW",
        "COMP",
        "VALVE",
        "LFLOW",
        "PUMP",
        "PIPE",
        "COLUMN"
      ],
      "include_flowsheet": true,
      "include_ui_next": true
    },
    "facade": true,
    "translated_operations": [],
    "response_status": null,
    "result": {}
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Need current live completion/readback after the bulk build because compact observation omitted probe payload.","action":"mcp_tool","operation":"probe_model_state","parameters":{"stream_names":["BZIN","H2IN","PRODUCT"],"block_names":["FEEDPUMP","FEED-MIX","REACT","HP-SEP","VFLOW","COMP","VALVE","LFLOW","PUMP","PIPE","COLUMN"],"include_flowsheet":true,"include_ui_next":false}}
```

</details>

## Call 5: `select_action`

- Input tokens: **131,591**
- Output tokens: **517**
- Total tokens: **132,108**
- Provider cost: **$0.673465**
- Recorded at: `2026-10-18T21:00:20.696`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 71,
    "domain_versions": {
      "properties": 2,
      "flowsheet": 71,
      "stream:H2RCY2": 5,
      "stream:CHRCY2": 5,
      "stream:LIQ": 5,
      "stream:RXOUT": 5,
      "stream:PURGE": 5,
      "stream:BZIN": 5,
      "stream:PRODUCT": 3,
      "stream:H2IN": 5,
      "stream:CHRCY3": 5,
      "stream:LTENDS": 3,
      "stream:BZIN2": 5,
      "stream:VAP": 5,
      "stream:H2RCY": 5,
      "stream:PURGE2": 3,
      "stream:CHRCY": 5,
      "stream:RXIN": 5,
      "stream:COLFD": 7,
      "block:FEEDPUMP": 11,
      "block:FEED-MIX": 6,
      "block:REACT": 6,
      "block:HP-SEP": 4,
      "block:VFLOW": 3,
      "block:COMP": 4,
      "block:VALVE": 4,
      "block:LFLOW": 3,
      "block:PUMP": 5,
      "block:PIPE": 4,
      "block:COLUMN": 13
    },
    "components": [
      "H2",
      "N2",
      "CH4",
      "BENZENE",
      "CYCLOHEX"
    ],
    "property_method": "",
    "blocks": [
      "FEEDPUMP",
      "FEED-MIX",
      "REACT",
      "HP-SEP",
      "VFLOW",
      "COMP",
      "VALVE",
      "LFLOW",
      "PUMP",
      "PIPE",
      "COLUMN"
    ],
    "streams": [
      "BZIN",
      "H2IN",
      "BZIN2",
      "H2RCY2",
      "RXIN",
      "RXOUT",
      "VAP",
      "H2RCY",
      "PURGE",
      "PURGE2",
      "LIQ",
      "COLFD",
      "CHRCY",
      "CHRCY2",
      "CHRCY3",
      "LTENDS",
      "PRODUCT"
    ],
    "connections": [
      {
        "block_name": "COLUMN",
        "stream_name": "COLFD",
        "port_name": "F(IN)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "LTENDS",
        "port_name": "VD(OUT)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "PRODUCT",
        "port_name": "B(OUT)",
        "source_operation": "connect_stream"
      }
    ],
    "specs": [
      {
        "stream_name": "H2IN",
        "temperature": 50.0,
        "pressure": 2.5,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      },
      {
        "stream_name": "BZIN",
        "temperature": 40.0,
        "pressure": 0.1,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      }
    ],
    "engine_run": null,
    "artifacts": {},
    "readbacks": []
  },
  "operation_ledger": {
    "677ff79d23598058": {
      "operation": "add_components_by_cas",
      "parameters": {
        "components": [
          {
            "component_id": "H2",
            "cas": "1333-74-0"
          },
          {
            "component_id": "N2",
            "cas": "7727-37-9"
          },
          {
            "component_id": "CH4",
            "cas": "74-82-8"
          },
          {
            "component_id": "BENZENE",
            "cas": "71-43-2"
          },
          {
            "component_id": "CYCLOHEX",
            "cas": "110-82-7"
          }
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "components_added": [
          {
            "cas": "1333740",
            "component_id": "H2",
            "requested_component_id": "H2",
            "preferred_component_id": "H2"
          },
          {
            "cas": "7727379",
            "component_id": "N2",
            "requested_component_id": "N2",
            "preferred_component_id": "N2"
          },
          {
            "cas": "74-82-8",
            "component_id": "CH4",
            "requested_component_id": "CH4",
            "preferred_component_id": "CH4"
          },
          {
            "cas": "71-43-2",
            "component_id": "BENZENE",
            "requested_component_id": "BENZENE",
            "preferred_component_id": "BENZENE"
          },
          {
            "cas": "110-82-7",
            "component_id": "CYCLOHEX",
            "requested_component_id": "CYCLOHEX",
            "preferred_component_id": "CYCLOHEX"
          }
        ],
        "count": 5,
        "message": "Added 5 component(s) successfully",
        "verification": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "missing_component_ids": []
        },
        "contamination": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "extra_component_ids": [],
          "generic_extra_component_ids": []
        }
      }
    },
    "d0f7c037faabb2bb": {
      "operation": "ensure_property_method",
      "parameters": {
        "method": "RK-SOAVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 2
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "ensure_property_method",
        "steps_completed": 5,
        "steps_total": 5,
        "last_result": null
      }
    },
    "33ce8ec6c91a3f71": {
      "operation": "create_material_streams",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "stream:BZIN",
        "stream:H2IN",
        "stream:BZIN2",
        "stream:H2RCY2",
        "stream:RXIN",
        "stream:RXOUT",
        "stream:VAP",
        "stream:H2RCY",
        "stream:PURGE",
        "stream:PURGE2",
        "stream:LIQ",
        "stream:COLFD",
        "stream:CHRCY",
        "stream:CHRCY2",
        "stream:CHRCY3",
        "stream:LTENDS",
        "stream:PRODUCT"
      ],
      "dependency_versions": {
        "stream:BZIN": 1,
        "stream:H2IN": 1,
        "stream:BZIN2": 1,
        "stream:H2RCY2": 1,
        "stream:RXIN": 1,
        "stream:RXOUT": 1,
        "stream:VAP": 1,
        "stream:H2RCY": 1,
        "stream:PURGE": 1,
        "stream:PURGE2": 1,
        "stream:LIQ": 1,
        "stream:COLFD": 1,
        "stream:CHRCY": 1,
        "stream:CHRCY2": 1,
        "stream:CHRCY3": 1,
        "stream:LTENDS": 1,
        "stream:PRODUCT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "create_material_streams",
        "steps_completed": 17,
        "steps_total": 17,
        "last_result": null
      }
    },
    "aeeab72bf4e897bd": {
      "operation": "create_pump",
      "parameters": {
        "block_name": "FEEDPUMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEEDPUMP"
      ],
      "dependency_versions": {
        "block:FEEDPUMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEEDPUMP",
        "block_type": "PUMP",
        "composite": "FEEDPUMP!PUMP",
        "message": "Block FEEDPUMP (PUMP) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "0909126309d406aa": {
      "operation": "create_heater",
      "parameters": {
        "block_name": "FEED-MIX"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEED-MIX"
      ],
      "dependency_versions": {
        "block:FEED-MIX": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEED-MIX",
        "block_type": "HEATER",
        "composite": "FEED-MIX!HEATER",
        "message": "Block FEED-MIX (HEATER) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEED-MIX\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a6c7e44d982c03d4": {
      "operation": "create_rstoic",
      "parameters": {
        "block_name": "REACT"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:REACT"
      ],
      "dependency_versions": {
        "block:REACT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "REACT",
        "block_type": "RSTOIC",
        "composite": "REACT!RSTOIC",
        "message": "Block REACT (RSTOIC) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "REACT",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\REACT\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "REACT",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\REACT\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\REACT\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a2421e5bf09b3395": {
      "operation": "create_flash2",
      "parameters": {
        "block_name": "HP-SEP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:HP-SEP"
      ],
      "dependency_versions": {
        "block:HP-SEP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "HP-SEP",
        "block_type": "FLASH2",
        "composite": "HP-SEP!FLASH2",
        "message": "Block HP-SEP (FLASH2) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "HP-SEP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "HP-SEP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\HP-SEP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "9d6acd9818f63c1d": {
      "operation": "create_fsplit",
      "parameters": {
        "block_name": "VFLOW"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VFLOW"
      ],
      "dependency_versions": {
        "block:VFLOW": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VFLOW",
        "block_type": "FSPLIT",
        "composite": "VFLOW!FSPLIT",
        "message": "Block VFLOW (FSPLIT) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VFLOW",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXOL"
              ]
            },
            {
              "block": "VFLOW",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXIT",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXIT"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "315f45151cc00f4e": {
      "operation": "create_compr",
      "parameters": {
        "block_name": "COMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:COMP"
      ],
      "dependency_versions": {
        "block:COMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "COMP",
        "block_type": "COMPR",
        "composite": "COMP!COMPR",
        "message": "Block COMP (COMPR) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "COMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\COMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "COMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\COMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\COMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "608a52d659fb4d06": {
      "operation": "create_valve",
      "parameters": {
        "block_name": "VALVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VALVE"
      ],
      "dependency_versions": {
        "block:VALVE": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VALVE",
        "block_type": "VALVE",
        "composite": "VALVE!VALVE",
        "message": "Block VALVE (VALVE) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "VALVE",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXIT",
              "before": 50,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VALVE",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXOL",
              "attempted_paths": [

...[context truncated for ReAct baseline prompt]...
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 2,
  "event_counts": {
    "preflight": 1,
    "session_started": 1
  },
  "operation_counts_top": {},
  "successful_operations_tail": [],
  "failures_tail": [],
  "artifacts_tail": [],
  "validator_feedback_tail": []
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "truncated": true,
    "chars": 9822,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 25, \"actions_executed\": 25, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"add_components_by_cas\", \"parameters\": {\"components\": [{\"component_id\": \"H2\", \"cas\": \"1333-74-0\"}, {\"component_id\": \"N2\", \"cas\": \"7727-37-9\"}, {\"component_id\": \"CH4\", \"cas\": \"74-82-8\"}, {\"component_id\": \"BENZENE\", \"cas\": \"71-43-2\"}, {\"component_id\": \"CYCLOHEX\", \"cas\": \"110-82-7\"}]}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Added 5 component(s) successfully\"}}, {\"truncated\": true, \"chars\": 525, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"ensure_property_method\\\", \\\"parameters\\\": {\\\"method\\\": \\\"RK-SOAVE\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"set_property_method\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"set_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"set_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"get_variable\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"ge\\n...[truncated]\"}, {\"truncated\": true, \"chars\": 1611, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"create_material_streams\\\", \\\"parameters\\\": {\\\"stream_names\\\": [\\\"BZIN\\\", \\\"H2IN\\\", \\\"BZIN2\\\", \\\"H2RCY2\\\", \\\"RXIN\\\", \\\"RXOUT\\\", \\\"VAP\\\", \\\"H2RCY\\\", \\\"PURGE\\\", \\\"PURGE2\\\", \\\"LIQ\\\", \\\"COLFD\\\", \\\"CHRCY\\\", \\\"CHRCY2\\\", \\\"CHRCY3\\\", \\\"LTENDS\\\", \\\"PRODUCT\\\"]}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"create_material_streams\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"create_material_streams\\\", \\\"success\\\": \\n...[truncated]\"}, {\"event\": \"tool_result\", \"operation\": \"create_pump\", \"parameters\": {\"block_name\": \"FEEDPUMP\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Block FEEDPUMP (PUMP) created successfully\", \"block_name\": \"FEEDPUMP\"}}, {\"event\": \"tool_result\", \"operation\": \"create_heater\", \"parameters\": {\"block_name\": \"FEED-MIX\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"message\": \"Block FEED-MIX (HEATER) created successfully\", \"block_name\": \"FEED-MIX\"}}, {\"event\": \"tool_result\", \"operation\": \"create_rstoic\", \"parameters\": {\"block_name\": \"REACT\"}, \"facade\": true, \n...[truncated]"
  },
  {
    "truncated": true,
    "chars": 19494,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 47, \"actions_executed\": 47, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"connect_material_inlet_outlet\", \"parameters\": {\"block_name\": \"FEEDPUMP\", \"inlet_stream\": \"BZIN\", \"outlet_stream\": \"BZIN2\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"list_block_ports\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"connect_shared_material_port_block\", \"parameters\": {\"block_name\": \"FEED-MIX\", \"inlet_streams\": [\"BZIN2\", \"H2IN\", \"H2RCY2\", \"CHRCY3\"], \"outlet_streams\": [\"RXIN\"]}, \"facade\": true, \"translated_operations\": [{\"operation\": \"connect_shared_material_port_block\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"connect_material_inlet_outlet\", \"parameters\": {\"block_name\": \"REACT\", \"inlet_stream\": \"RXIN\", \"outlet_stream\": \"RXOUT\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"list_block_ports\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"truncated\": true, \"chars\": 549, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"connect_flash2_vapor_liquid_ports\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"HP-SEP\\\", \\\"feed_stream\\\": \\\"RXOUT\\\", \\\"vapor_stream\\\": \\\"VAP\\\", \\\"liquid_stream\\\": \\\"LIQ\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"list_block_ports\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"connect_stream\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"connect_stream\\\", \\\"success\\\": true, \\\"error\\\": nu\\n...[truncated]\"}, {\"event\": \"tool_result\", \"operation\": \"configure_fsplit_shared_outlets\", \"parameters\": {\"block_name\": \"VFLOW\", \"inlet_stream\": \"VAP\", \"outlet_streams\": [\"H2RCY\", \"PURGE\"], \"split_fractions\": {\"H2RCY\": 0.92}}, \"facade\": true, \"translated_operations\": [{\"operation\": \"configure_fsplit_shared_outlets\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}\n...[truncated]"
  },
  {
    "event": "tool_result",
    "operation": "probe_model_state",
    "parameters": {
      "stream_names": [
        "BZIN",
        "H2IN",
        "BZIN2",
        "H2RCY2",
        "RXIN",
        "RXOUT",
        "VAP",
        "H2RCY",
        "PURGE",
        "PURGE2",
        "LIQ",
        "COLFD",
        "CHRCY",
        "CHRCY2",
        "CHRCY3",
        "LTENDS",
        "PRODUCT"
      ],
      "block_names": [
        "FEEDPUMP",
        "FEED-MIX",
        "REACT",
        "HP-SEP",
        "VFLOW",
        "COMP",
        "VALVE",
        "LFLOW",
        "PUMP",
        "PIPE",
        "COLUMN"
      ],
      "include_flowsheet": true,
      "include_ui_next": true
    },
    "facade": true,
    "translated_operations": [],
    "response_status": null,
    "result": {}
  },
  {
    "event": "tool_result",
    "operation": "probe_model_state",
    "parameters": {
      "stream_names": [
        "BZIN",
        "H2IN",
        "PRODUCT"
      ],
      "block_names": [
        "FEEDPUMP",
        "FEED-MIX",
        "REACT",
        "HP-SEP",
        "VFLOW",
        "COMP",
        "VALVE",
        "LFLOW",
        "PUMP",
        "PIPE",
        "COLUMN"
      ],
      "include_flowsheet": true,
      "include_ui_next": false
    },
    "facade": true,
    "translated_operations": [
      {
        "operation": "probe_model_state",
        "success": true,
        "error": null
      }
    ],
    "response_status": null,
    "result": {}
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Run workflow completion/readback diagnostics before attempting engine run; prior probes returned compact empty summaries, so use explicit completion tools.","action":"mcp_plan","operation":"diagnose_completion","parameters":{"actions":[{"operation":"read_global_property_method","parameters":{}},{"operation":"ui_check_next_completion_status","parameters":{"close_window":true,"status_timeout_s":8.0}},{"operation":"check_flowsheet_completion","parameters":{}},{"operation":"check_block_completion","parameters":{"block_name":"FEEDPUMP"}},{"operation":"check_block_completion","parameters":{"block_name":"FEED-MIX"}},{"operation":"check_block_completion","parameters":{"block_name":"REACT"}},{"operation":"check_block_completion","parameters":{"block_name":"HP-SEP"}},{"operation":"check_block_completion","parameters":{"block_name":"VFLOW"}},{"operation":"check_block_completion","parameters":{"block_name":"COMP"}},{"operation":"check_block_completion","parameters":{"block_name":"VALVE"}},{"operation":"check_block_completion","parameters":{"block_name":"LFLOW"}},{"operation":"check_block_completion","parameters":{"block_name":"PUMP"}},{"operation":"check_block_completion","parameters":{"block_name":"PIPE"}},{"operation":"check_block_completion","parameters":{"block_name":"COLUMN"}},{"operation":"check_stream_completion","parameters":{"stream_name":"BZIN"}},{"operation":"check_stream_completion","parameters":{"stream_name":"H2IN"}}]}}
```

</details>

## Call 6: `select_action`

- Input tokens: **131,547**
- Output tokens: **258**
- Total tokens: **131,805**
- Provider cost: **$0.665475**
- Recorded at: `2026-10-18T21:00:38.714`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 72,
    "domain_versions": {
      "properties": 2,
      "flowsheet": 72,
      "stream:H2RCY2": 5,
      "stream:CHRCY2": 5,
      "stream:LIQ": 5,
      "stream:RXOUT": 5,
      "stream:PURGE": 5,
      "stream:BZIN": 5,
      "stream:PRODUCT": 3,
      "stream:H2IN": 5,
      "stream:CHRCY3": 5,
      "stream:LTENDS": 3,
      "stream:BZIN2": 5,
      "stream:VAP": 5,
      "stream:H2RCY": 5,
      "stream:PURGE2": 3,
      "stream:CHRCY": 5,
      "stream:RXIN": 5,
      "stream:COLFD": 7,
      "block:FEEDPUMP": 11,
      "block:FEED-MIX": 6,
      "block:REACT": 6,
      "block:HP-SEP": 4,
      "block:VFLOW": 3,
      "block:COMP": 4,
      "block:VALVE": 4,
      "block:LFLOW": 3,
      "block:PUMP": 5,
      "block:PIPE": 4,
      "block:COLUMN": 13
    },
    "components": [
      "H2",
      "N2",
      "CH4",
      "BENZENE",
      "CYCLOHEX"
    ],
    "property_method": "",
    "blocks": [
      "FEEDPUMP",
      "FEED-MIX",
      "REACT",
      "HP-SEP",
      "VFLOW",
      "COMP",
      "VALVE",
      "LFLOW",
      "PUMP",
      "PIPE",
      "COLUMN"
    ],
    "streams": [
      "BZIN",
      "H2IN",
      "BZIN2",
      "H2RCY2",
      "RXIN",
      "RXOUT",
      "VAP",
      "H2RCY",
      "PURGE",
      "PURGE2",
      "LIQ",
      "COLFD",
      "CHRCY",
      "CHRCY2",
      "CHRCY3",
      "LTENDS",
      "PRODUCT"
    ],
    "connections": [
      {
        "block_name": "COLUMN",
        "stream_name": "COLFD",
        "port_name": "F(IN)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "LTENDS",
        "port_name": "VD(OUT)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "PRODUCT",
        "port_name": "B(OUT)",
        "source_operation": "connect_stream"
      }
    ],
    "specs": [
      {
        "stream_name": "H2IN",
        "temperature": 50.0,
        "pressure": 2.5,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      },
      {
        "stream_name": "BZIN",
        "temperature": 40.0,
        "pressure": 0.1,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      }
    ],
    "engine_run": null,
    "artifacts": {},
    "readbacks": []
  },
  "operation_ledger": {
    "677ff79d23598058": {
      "operation": "add_components_by_cas",
      "parameters": {
        "components": [
          {
            "component_id": "H2",
            "cas": "1333-74-0"
          },
          {
            "component_id": "N2",
            "cas": "7727-37-9"
          },
          {
            "component_id": "CH4",
            "cas": "74-82-8"
          },
          {
            "component_id": "BENZENE",
            "cas": "71-43-2"
          },
          {
            "component_id": "CYCLOHEX",
            "cas": "110-82-7"
          }
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "components_added": [
          {
            "cas": "1333740",
            "component_id": "H2",
            "requested_component_id": "H2",
            "preferred_component_id": "H2"
          },
          {
            "cas": "7727379",
            "component_id": "N2",
            "requested_component_id": "N2",
            "preferred_component_id": "N2"
          },
          {
            "cas": "74-82-8",
            "component_id": "CH4",
            "requested_component_id": "CH4",
            "preferred_component_id": "CH4"
          },
          {
            "cas": "71-43-2",
            "component_id": "BENZENE",
            "requested_component_id": "BENZENE",
            "preferred_component_id": "BENZENE"
          },
          {
            "cas": "110-82-7",
            "component_id": "CYCLOHEX",
            "requested_component_id": "CYCLOHEX",
            "preferred_component_id": "CYCLOHEX"
          }
        ],
        "count": 5,
        "message": "Added 5 component(s) successfully",
        "verification": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "missing_component_ids": []
        },
        "contamination": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "extra_component_ids": [],
          "generic_extra_component_ids": []
        }
      }
    },
    "d0f7c037faabb2bb": {
      "operation": "ensure_property_method",
      "parameters": {
        "method": "RK-SOAVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 2
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "ensure_property_method",
        "steps_completed": 5,
        "steps_total": 5,
        "last_result": null
      }
    },
    "33ce8ec6c91a3f71": {
      "operation": "create_material_streams",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "stream:BZIN",
        "stream:H2IN",
        "stream:BZIN2",
        "stream:H2RCY2",
        "stream:RXIN",
        "stream:RXOUT",
        "stream:VAP",
        "stream:H2RCY",
        "stream:PURGE",
        "stream:PURGE2",
        "stream:LIQ",
        "stream:COLFD",
        "stream:CHRCY",
        "stream:CHRCY2",
        "stream:CHRCY3",
        "stream:LTENDS",
        "stream:PRODUCT"
      ],
      "dependency_versions": {
        "stream:BZIN": 1,
        "stream:H2IN": 1,
        "stream:BZIN2": 1,
        "stream:H2RCY2": 1,
        "stream:RXIN": 1,
        "stream:RXOUT": 1,
        "stream:VAP": 1,
        "stream:H2RCY": 1,
        "stream:PURGE": 1,
        "stream:PURGE2": 1,
        "stream:LIQ": 1,
        "stream:COLFD": 1,
        "stream:CHRCY": 1,
        "stream:CHRCY2": 1,
        "stream:CHRCY3": 1,
        "stream:LTENDS": 1,
        "stream:PRODUCT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "create_material_streams",
        "steps_completed": 17,
        "steps_total": 17,
        "last_result": null
      }
    },
    "aeeab72bf4e897bd": {
      "operation": "create_pump",
      "parameters": {
        "block_name": "FEEDPUMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEEDPUMP"
      ],
      "dependency_versions": {
        "block:FEEDPUMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEEDPUMP",
        "block_type": "PUMP",
        "composite": "FEEDPUMP!PUMP",
        "message": "Block FEEDPUMP (PUMP) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "0909126309d406aa": {
      "operation": "create_heater",
      "parameters": {
        "block_name": "FEED-MIX"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEED-MIX"
      ],
      "dependency_versions": {
        "block:FEED-MIX": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEED-MIX",
        "block_type": "HEATER",
        "composite": "FEED-MIX!HEATER",
        "message": "Block FEED-MIX (HEATER) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEED-MIX\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a6c7e44d982c03d4": {
      "operation": "create_rstoic",
      "parameters": {
        "block_name": "REACT"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:REACT"
      ],
      "dependency_versions": {
        "block:REACT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "REACT",
        "block_type": "RSTOIC",
        "composite": "REACT!RSTOIC",
        "message": "Block REACT (RSTOIC) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "REACT",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\REACT\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "REACT",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\REACT\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\REACT\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a2421e5bf09b3395": {
      "operation": "create_flash2",
      "parameters": {
        "block_name": "HP-SEP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:HP-SEP"
      ],
      "dependency_versions": {
        "block:HP-SEP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "HP-SEP",
        "block_type": "FLASH2",
        "composite": "HP-SEP!FLASH2",
        "message": "Block HP-SEP (FLASH2) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "HP-SEP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "HP-SEP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\HP-SEP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "9d6acd9818f63c1d": {
      "operation": "create_fsplit",
      "parameters": {
        "block_name": "VFLOW"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VFLOW"
      ],
      "dependency_versions": {
        "block:VFLOW": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VFLOW",
        "block_type": "FSPLIT",
        "composite": "VFLOW!FSPLIT",
        "message": "Block VFLOW (FSPLIT) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VFLOW",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXOL"
              ]
            },
            {
              "block": "VFLOW",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXIT",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXIT"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "315f45151cc00f4e": {
      "operation": "create_compr",
      "parameters": {
        "block_name": "COMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:COMP"
      ],
      "dependency_versions": {
        "block:COMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "COMP",
        "block_type": "COMPR",
        "composite": "COMP!COMPR",
        "message": "Block COMP (COMPR) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "COMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\COMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "COMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\COMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\COMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "608a52d659fb4d06": {
      "operation": "create_valve",
      "parameters": {
        "block_name": "VALVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VALVE"
      ],
      "dependency_versions": {
        "block:VALVE": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VALVE",
        "block_type": "VALVE",
        "composite": "VALVE!VALVE",
        "message": "Block VALVE (VALVE) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "VALVE",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXIT",
              "before": 50,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VALVE",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXOL",
              "attempted_paths": [

...[context truncated for ReAct baseline prompt]...
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 3,
  "event_counts": {
    "preflight": 1,
    "session_started": 1,
    "plan_result": 1
  },
  "operation_counts_top": {},
  "successful_operations_tail": [],
  "failures_tail": [],
  "artifacts_tail": [],
  "validator_feedback_tail": []
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "truncated": true,
    "chars": 19494,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 47, \"actions_executed\": 47, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"connect_material_inlet_outlet\", \"parameters\": {\"block_name\": \"FEEDPUMP\", \"inlet_stream\": \"BZIN\", \"outlet_stream\": \"BZIN2\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"list_block_ports\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"connect_shared_material_port_block\", \"parameters\": {\"block_name\": \"FEED-MIX\", \"inlet_streams\": [\"BZIN2\", \"H2IN\", \"H2RCY2\", \"CHRCY3\"], \"outlet_streams\": [\"RXIN\"]}, \"facade\": true, \"translated_operations\": [{\"operation\": \"connect_shared_material_port_block\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"connect_material_inlet_outlet\", \"parameters\": {\"block_name\": \"REACT\", \"inlet_stream\": \"RXIN\", \"outlet_stream\": \"RXOUT\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"list_block_ports\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}, {\"operation\": \"connect_stream\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"truncated\": true, \"chars\": 549, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"connect_flash2_vapor_liquid_ports\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"HP-SEP\\\", \\\"feed_stream\\\": \\\"RXOUT\\\", \\\"vapor_stream\\\": \\\"VAP\\\", \\\"liquid_stream\\\": \\\"LIQ\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [{\\\"operation\\\": \\\"list_block_ports\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"connect_stream\\\", \\\"success\\\": true, \\\"error\\\": null}, {\\\"operation\\\": \\\"connect_stream\\\", \\\"success\\\": true, \\\"error\\\": nu\\n...[truncated]\"}, {\"event\": \"tool_result\", \"operation\": \"configure_fsplit_shared_outlets\", \"parameters\": {\"block_name\": \"VFLOW\", \"inlet_stream\": \"VAP\", \"outlet_streams\": [\"H2RCY\", \"PURGE\"], \"split_fractions\": {\"H2RCY\": 0.92}}, \"facade\": true, \"translated_operations\": [{\"operation\": \"configure_fsplit_shared_outlets\", \"success\": true, \"error\": null}], \"response_status\": \"success\", \"result\": {\"success\": true}}\n...[truncated]"
  },
  {
    "event": "tool_result",
    "operation": "probe_model_state",
    "parameters": {
      "stream_names": [
        "BZIN",
        "H2IN",
        "BZIN2",
        "H2RCY2",
        "RXIN",
        "RXOUT",
        "VAP",
        "H2RCY",
        "PURGE",
        "PURGE2",
        "LIQ",
        "COLFD",
        "CHRCY",
        "CHRCY2",
        "CHRCY3",
        "LTENDS",
        "PRODUCT"
      ],
      "block_names": [
        "FEEDPUMP",
        "FEED-MIX",
        "REACT",
        "HP-SEP",
        "VFLOW",
        "COMP",
        "VALVE",
        "LFLOW",
        "PUMP",
        "PIPE",
        "COLUMN"
      ],
      "include_flowsheet": true,
      "include_ui_next": true
    },
    "facade": true,
    "translated_operations": [],
    "response_status": null,
    "result": {}
  },
  {
    "event": "tool_result",
    "operation": "probe_model_state",
    "parameters": {
      "stream_names": [
        "BZIN",
        "H2IN",
        "PRODUCT"
      ],
      "block_names": [
        "FEEDPUMP",
        "FEED-MIX",
        "REACT",
        "HP-SEP",
        "VFLOW",
        "COMP",
        "VALVE",
        "LFLOW",
        "PUMP",
        "PIPE",
        "COLUMN"
      ],
      "include_flowsheet": true,
      "include_ui_next": false
    },
    "facade": true,
    "translated_operations": [
      {
        "operation": "probe_model_state",
        "success": true,
        "error": null
      }
    ],
    "response_status": null,
    "result": {}
  },
  {
    "truncated": true,
    "chars": 8167,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 16, \"actions_executed\": 16, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"read_global_property_method\", \"parameters\": {}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"ui_check_next_completion_status\", \"parameters\": {\"close_window\": true, \"status_timeout_s\": 8.0}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"per_error\": null}}, {\"truncated\": true, \"chars\": 556, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_flowsheet_completion\\\", \\\"parameters\\\": {}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"node_path_used\\\": \\\"Data\\\\\\\\Flowsheet\\\\\\\\Section\\\\\\\\GLOBAL\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\\"input_incomplete\\\": false, \\\"input_co\\n...[truncated]\"}, {\"truncated\": true, \"chars\": 602, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"FEEDPUMP\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"block_name\\\": \\\"FEEDPUMP\\\", \\\"node_path_used\\\": \\\"Data\\\\\\\\Blocks\\\\\\\\FEEDPUMP\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\n...[truncated]\"}, {\"truncated\": true, \"chars\": 602, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"FEED-MIX\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"block_name\\\": \\\"FEED-MIX\\\", \\\"node_path_used\\\": \\\"Data\\\\\\\\Blocks\\\\\\\\FEED-MIX\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\n...[truncated]\"}, {\"truncated\": true, \"chars\": 593, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"REACT\\\"}, \\\"facade\\\": true, \\\n...[truncated]"
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Model appears built and completion checked; run/export current flowsheet to see trusted status and diagnostics before readbacks/finalization.","action":"mcp_tool","operation":"export_final_evidence","parameters":{"run_engine":true,"rep_filename":"chinese_5_1_radfrac.rep","apw_filename":"chinese_5_1_radfrac.apw","export_format":2}}
```

</details>

## Call 7: `select_action`

- Input tokens: **131,074**
- Output tokens: **515**
- Total tokens: **131,589**
- Provider cost: **$0.670820**
- Recorded at: `2026-10-18T21:00:53.171`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 73,
    "domain_versions": {
      "properties": 2,
      "flowsheet": 73,
      "stream:H2RCY2": 5,
      "stream:CHRCY2": 5,
      "stream:LIQ": 5,
      "stream:RXOUT": 5,
      "stream:PURGE": 5,
      "stream:BZIN": 5,
      "stream:PRODUCT": 3,
      "stream:H2IN": 5,
      "stream:CHRCY3": 5,
      "stream:LTENDS": 3,
      "stream:BZIN2": 5,
      "stream:VAP": 5,
      "stream:H2RCY": 5,
      "stream:PURGE2": 3,
      "stream:CHRCY": 5,
      "stream:RXIN": 5,
      "stream:COLFD": 7,
      "block:FEEDPUMP": 11,
      "block:FEED-MIX": 6,
      "block:REACT": 6,
      "block:HP-SEP": 4,
      "block:VFLOW": 3,
      "block:COMP": 4,
      "block:VALVE": 4,
      "block:LFLOW": 3,
      "block:PUMP": 5,
      "block:PIPE": 4,
      "block:COLUMN": 13
    },
    "components": [
      "H2",
      "N2",
      "CH4",
      "BENZENE",
      "CYCLOHEX"
    ],
    "property_method": "",
    "blocks": [
      "FEEDPUMP",
      "FEED-MIX",
      "REACT",
      "HP-SEP",
      "VFLOW",
      "COMP",
      "VALVE",
      "LFLOW",
      "PUMP",
      "PIPE",
      "COLUMN"
    ],
    "streams": [
      "BZIN",
      "H2IN",
      "BZIN2",
      "H2RCY2",
      "RXIN",
      "RXOUT",
      "VAP",
      "H2RCY",
      "PURGE",
      "PURGE2",
      "LIQ",
      "COLFD",
      "CHRCY",
      "CHRCY2",
      "CHRCY3",
      "LTENDS",
      "PRODUCT"
    ],
    "connections": [
      {
        "block_name": "COLUMN",
        "stream_name": "COLFD",
        "port_name": "F(IN)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "LTENDS",
        "port_name": "VD(OUT)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "PRODUCT",
        "port_name": "B(OUT)",
        "source_operation": "connect_stream"
      }
    ],
    "specs": [
      {
        "stream_name": "H2IN",
        "temperature": 50.0,
        "pressure": 2.5,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      },
      {
        "stream_name": "BZIN",
        "temperature": 40.0,
        "pressure": 0.1,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      }
    ],
    "engine_run": null,
    "artifacts": {},
    "readbacks": []
  },
  "operation_ledger": {
    "677ff79d23598058": {
      "operation": "add_components_by_cas",
      "parameters": {
        "components": [
          {
            "component_id": "H2",
            "cas": "1333-74-0"
          },
          {
            "component_id": "N2",
            "cas": "7727-37-9"
          },
          {
            "component_id": "CH4",
            "cas": "74-82-8"
          },
          {
            "component_id": "BENZENE",
            "cas": "71-43-2"
          },
          {
            "component_id": "CYCLOHEX",
            "cas": "110-82-7"
          }
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "components_added": [
          {
            "cas": "1333740",
            "component_id": "H2",
            "requested_component_id": "H2",
            "preferred_component_id": "H2"
          },
          {
            "cas": "7727379",
            "component_id": "N2",
            "requested_component_id": "N2",
            "preferred_component_id": "N2"
          },
          {
            "cas": "74-82-8",
            "component_id": "CH4",
            "requested_component_id": "CH4",
            "preferred_component_id": "CH4"
          },
          {
            "cas": "71-43-2",
            "component_id": "BENZENE",
            "requested_component_id": "BENZENE",
            "preferred_component_id": "BENZENE"
          },
          {
            "cas": "110-82-7",
            "component_id": "CYCLOHEX",
            "requested_component_id": "CYCLOHEX",
            "preferred_component_id": "CYCLOHEX"
          }
        ],
        "count": 5,
        "message": "Added 5 component(s) successfully",
        "verification": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "missing_component_ids": []
        },
        "contamination": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "extra_component_ids": [],
          "generic_extra_component_ids": []
        }
      }
    },
    "d0f7c037faabb2bb": {
      "operation": "ensure_property_method",
      "parameters": {
        "method": "RK-SOAVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 2
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "ensure_property_method",
        "steps_completed": 5,
        "steps_total": 5,
        "last_result": null
      }
    },
    "33ce8ec6c91a3f71": {
      "operation": "create_material_streams",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "stream:BZIN",
        "stream:H2IN",
        "stream:BZIN2",
        "stream:H2RCY2",
        "stream:RXIN",
        "stream:RXOUT",
        "stream:VAP",
        "stream:H2RCY",
        "stream:PURGE",
        "stream:PURGE2",
        "stream:LIQ",
        "stream:COLFD",
        "stream:CHRCY",
        "stream:CHRCY2",
        "stream:CHRCY3",
        "stream:LTENDS",
        "stream:PRODUCT"
      ],
      "dependency_versions": {
        "stream:BZIN": 1,
        "stream:H2IN": 1,
        "stream:BZIN2": 1,
        "stream:H2RCY2": 1,
        "stream:RXIN": 1,
        "stream:RXOUT": 1,
        "stream:VAP": 1,
        "stream:H2RCY": 1,
        "stream:PURGE": 1,
        "stream:PURGE2": 1,
        "stream:LIQ": 1,
        "stream:COLFD": 1,
        "stream:CHRCY": 1,
        "stream:CHRCY2": 1,
        "stream:CHRCY3": 1,
        "stream:LTENDS": 1,
        "stream:PRODUCT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "create_material_streams",
        "steps_completed": 17,
        "steps_total": 17,
        "last_result": null
      }
    },
    "aeeab72bf4e897bd": {
      "operation": "create_pump",
      "parameters": {
        "block_name": "FEEDPUMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEEDPUMP"
      ],
      "dependency_versions": {
        "block:FEEDPUMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEEDPUMP",
        "block_type": "PUMP",
        "composite": "FEEDPUMP!PUMP",
        "message": "Block FEEDPUMP (PUMP) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "0909126309d406aa": {
      "operation": "create_heater",
      "parameters": {
        "block_name": "FEED-MIX"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEED-MIX"
      ],
      "dependency_versions": {
        "block:FEED-MIX": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEED-MIX",
        "block_type": "HEATER",
        "composite": "FEED-MIX!HEATER",
        "message": "Block FEED-MIX (HEATER) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEED-MIX\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a6c7e44d982c03d4": {
      "operation": "create_rstoic",
      "parameters": {
        "block_name": "REACT"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:REACT"
      ],
      "dependency_versions": {
        "block:REACT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "REACT",
        "block_type": "RSTOIC",
        "composite": "REACT!RSTOIC",
        "message": "Block REACT (RSTOIC) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "REACT",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\REACT\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "REACT",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\REACT\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\REACT\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a2421e5bf09b3395": {
      "operation": "create_flash2",
      "parameters": {
        "block_name": "HP-SEP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:HP-SEP"
      ],
      "dependency_versions": {
        "block:HP-SEP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "HP-SEP",
        "block_type": "FLASH2",
        "composite": "HP-SEP!FLASH2",
        "message": "Block HP-SEP (FLASH2) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "HP-SEP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "HP-SEP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\HP-SEP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "9d6acd9818f63c1d": {
      "operation": "create_fsplit",
      "parameters": {
        "block_name": "VFLOW"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VFLOW"
      ],
      "dependency_versions": {
        "block:VFLOW": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VFLOW",
        "block_type": "FSPLIT",
        "composite": "VFLOW!FSPLIT",
        "message": "Block VFLOW (FSPLIT) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VFLOW",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXOL"
              ]
            },
            {
              "block": "VFLOW",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXIT",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXIT"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "315f45151cc00f4e": {
      "operation": "create_compr",
      "parameters": {
        "block_name": "COMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:COMP"
      ],
      "dependency_versions": {
        "block:COMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "COMP",
        "block_type": "COMPR",
        "composite": "COMP!COMPR",
        "message": "Block COMP (COMPR) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "COMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\COMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "COMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\COMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\COMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "608a52d659fb4d06": {
      "operation": "create_valve",
      "parameters": {
        "block_name": "VALVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VALVE"
      ],
      "dependency_versions": {
        "block:VALVE": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VALVE",
        "block_type": "VALVE",
        "composite": "VALVE!VALVE",
        "message": "Block VALVE (VALVE) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "VALVE",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXIT",
              "before": 50,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VALVE",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXOL",
              "attempted_paths": [

...[context truncated for ReAct baseline prompt]...
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 4,
  "event_counts": {
    "plan_result": 2,
    "preflight": 1,
    "session_started": 1
  },
  "operation_counts_top": {},
  "successful_operations_tail": [],
  "failures_tail": [],
  "artifacts_tail": [],
  "validator_feedback_tail": []
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "event": "tool_result",
    "operation": "probe_model_state",
    "parameters": {
      "stream_names": [
        "BZIN",
        "H2IN",
        "BZIN2",
        "H2RCY2",
        "RXIN",
        "RXOUT",
        "VAP",
        "H2RCY",
        "PURGE",
        "PURGE2",
        "LIQ",
        "COLFD",
        "CHRCY",
        "CHRCY2",
        "CHRCY3",
        "LTENDS",
        "PRODUCT"
      ],
      "block_names": [
        "FEEDPUMP",
        "FEED-MIX",
        "REACT",
        "HP-SEP",
        "VFLOW",
        "COMP",
        "VALVE",
        "LFLOW",
        "PUMP",
        "PIPE",
        "COLUMN"
      ],
      "include_flowsheet": true,
      "include_ui_next": true
    },
    "facade": true,
    "translated_operations": [],
    "response_status": null,
    "result": {}
  },
  {
    "event": "tool_result",
    "operation": "probe_model_state",
    "parameters": {
      "stream_names": [
        "BZIN",
        "H2IN",
        "PRODUCT"
      ],
      "block_names": [
        "FEEDPUMP",
        "FEED-MIX",
        "REACT",
        "HP-SEP",
        "VFLOW",
        "COMP",
        "VALVE",
        "LFLOW",
        "PUMP",
        "PIPE",
        "COLUMN"
      ],
      "include_flowsheet": true,
      "include_ui_next": false
    },
    "facade": true,
    "translated_operations": [
      {
        "operation": "probe_model_state",
        "success": true,
        "error": null
      }
    ],
    "response_status": null,
    "result": {}
  },
  {
    "truncated": true,
    "chars": 8167,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 16, \"actions_executed\": 16, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"read_global_property_method\", \"parameters\": {}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"ui_check_next_completion_status\", \"parameters\": {\"close_window\": true, \"status_timeout_s\": 8.0}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"per_error\": null}}, {\"truncated\": true, \"chars\": 556, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_flowsheet_completion\\\", \\\"parameters\\\": {}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"node_path_used\\\": \\\"Data\\\\\\\\Flowsheet\\\\\\\\Section\\\\\\\\GLOBAL\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\\"input_incomplete\\\": false, \\\"input_co\\n...[truncated]\"}, {\"truncated\": true, \"chars\": 602, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"FEEDPUMP\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"block_name\\\": \\\"FEEDPUMP\\\", \\\"node_path_used\\\": \\\"Data\\\\\\\\Blocks\\\\\\\\FEEDPUMP\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\n...[truncated]\"}, {\"truncated\": true, \"chars\": 602, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"FEED-MIX\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"block_name\\\": \\\"FEED-MIX\\\", \\\"node_path_used\\\": \\\"Data\\\\\\\\Blocks\\\\\\\\FEED-MIX\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\n...[truncated]\"}, {\"truncated\": true, \"chars\": 593, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"REACT\\\"}, \\\"facade\\\": true, \\\n...[truncated]"
  },
  {
    "event": "tool_result",
    "operation": "export_final_evidence",
    "parameters": {
      "run_engine": true,
      "rep_filename": "chinese_5_1_radfrac.rep",
      "apw_filename": "chinese_5_1_radfrac.apw",
      "export_format": 2
    },
    "facade": true,
    "translated_operations": [],
    "response_status": "success",
    "result": {
      "success": true,
      "diagnostic_summary": {
        "per_error": 0,
        "converged": true,
        "rep_path": "<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210043_react_mc.rep",
        "apw_path": "<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210044_react_mc.apw",
        "messages": [],
        "value": 0,
        "path": "Data\\Results Summary\\Run-Status\\Output\\PER_ERROR",
        "rep_problem_status": {
          "converged": true,
          "hints": [
            "ID        ID               ERR/TOL      RELATIVE     ERROR       STAT  BLOCK",
            "****   MAXIMUM FINAL RELATIVE ERRORS   ****"
          ]
        },
        "repair_required": false
      }
    }
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Converged evidence exists; now read final PRODUCT composition and key validation readbacks.","action":"mcp_plan","parameters":{"actions":[{"operation":"read_stream_mole_fractions","parameters":{"stream_name":"PRODUCT"}},{"operation":"read_stream_outputs","parameters":{"stream_name":"PRODUCT","components":["H2","N2","CH4","BENZENE","CYCLOHEX"],"basis":"mole_fraction"}},{"operation":"read_global_property_method","parameters":{}},{"operation":"list_block_ports","parameters":{"block_name":"FEEDPUMP"}},{"operation":"list_block_ports","parameters":{"block_name":"PUMP"}},{"operation":"list_block_ports","parameters":{"block_name":"COLUMN"}}]}}
```

</details>

## Call 8: `select_action`

- Input tokens: **131,962**
- Output tokens: **564**
- Total tokens: **132,526**
- Provider cost: **$0.676730**
- Recorded at: `2026-10-18T21:01:02.306`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 73,
    "domain_versions": {
      "properties": 2,
      "flowsheet": 73,
      "stream:H2RCY2": 5,
      "stream:CHRCY2": 5,
      "stream:LIQ": 5,
      "stream:RXOUT": 5,
      "stream:PURGE": 5,
      "stream:BZIN": 5,
      "stream:PRODUCT": 3,
      "stream:H2IN": 5,
      "stream:CHRCY3": 5,
      "stream:LTENDS": 3,
      "stream:BZIN2": 5,
      "stream:VAP": 5,
      "stream:H2RCY": 5,
      "stream:PURGE2": 3,
      "stream:CHRCY": 5,
      "stream:RXIN": 5,
      "stream:COLFD": 7,
      "block:FEEDPUMP": 11,
      "block:FEED-MIX": 6,
      "block:REACT": 6,
      "block:HP-SEP": 4,
      "block:VFLOW": 3,
      "block:COMP": 4,
      "block:VALVE": 4,
      "block:LFLOW": 3,
      "block:PUMP": 5,
      "block:PIPE": 4,
      "block:COLUMN": 13
    },
    "components": [
      "H2",
      "N2",
      "CH4",
      "BENZENE",
      "CYCLOHEX"
    ],
    "property_method": "",
    "blocks": [
      "FEEDPUMP",
      "FEED-MIX",
      "REACT",
      "HP-SEP",
      "VFLOW",
      "COMP",
      "VALVE",
      "LFLOW",
      "PUMP",
      "PIPE",
      "COLUMN"
    ],
    "streams": [
      "BZIN",
      "H2IN",
      "BZIN2",
      "H2RCY2",
      "RXIN",
      "RXOUT",
      "VAP",
      "H2RCY",
      "PURGE",
      "PURGE2",
      "LIQ",
      "COLFD",
      "CHRCY",
      "CHRCY2",
      "CHRCY3",
      "LTENDS",
      "PRODUCT"
    ],
    "connections": [
      {
        "block_name": "COLUMN",
        "stream_name": "COLFD",
        "port_name": "F(IN)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "LTENDS",
        "port_name": "VD(OUT)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "PRODUCT",
        "port_name": "B(OUT)",
        "source_operation": "connect_stream"
      }
    ],
    "specs": [
      {
        "stream_name": "H2IN",
        "temperature": 50.0,
        "pressure": 2.5,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      },
      {
        "stream_name": "BZIN",
        "temperature": 40.0,
        "pressure": 0.1,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      }
    ],
    "engine_run": null,
    "artifacts": {},
    "readbacks": []
  },
  "operation_ledger": {
    "677ff79d23598058": {
      "operation": "add_components_by_cas",
      "parameters": {
        "components": [
          {
            "component_id": "H2",
            "cas": "1333-74-0"
          },
          {
            "component_id": "N2",
            "cas": "7727-37-9"
          },
          {
            "component_id": "CH4",
            "cas": "74-82-8"
          },
          {
            "component_id": "BENZENE",
            "cas": "71-43-2"
          },
          {
            "component_id": "CYCLOHEX",
            "cas": "110-82-7"
          }
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "components_added": [
          {
            "cas": "1333740",
            "component_id": "H2",
            "requested_component_id": "H2",
            "preferred_component_id": "H2"
          },
          {
            "cas": "7727379",
            "component_id": "N2",
            "requested_component_id": "N2",
            "preferred_component_id": "N2"
          },
          {
            "cas": "74-82-8",
            "component_id": "CH4",
            "requested_component_id": "CH4",
            "preferred_component_id": "CH4"
          },
          {
            "cas": "71-43-2",
            "component_id": "BENZENE",
            "requested_component_id": "BENZENE",
            "preferred_component_id": "BENZENE"
          },
          {
            "cas": "110-82-7",
            "component_id": "CYCLOHEX",
            "requested_component_id": "CYCLOHEX",
            "preferred_component_id": "CYCLOHEX"
          }
        ],
        "count": 5,
        "message": "Added 5 component(s) successfully",
        "verification": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "missing_component_ids": []
        },
        "contamination": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "extra_component_ids": [],
          "generic_extra_component_ids": []
        }
      }
    },
    "d0f7c037faabb2bb": {
      "operation": "ensure_property_method",
      "parameters": {
        "method": "RK-SOAVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 2
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "ensure_property_method",
        "steps_completed": 5,
        "steps_total": 5,
        "last_result": null
      }
    },
    "33ce8ec6c91a3f71": {
      "operation": "create_material_streams",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "stream:BZIN",
        "stream:H2IN",
        "stream:BZIN2",
        "stream:H2RCY2",
        "stream:RXIN",
        "stream:RXOUT",
        "stream:VAP",
        "stream:H2RCY",
        "stream:PURGE",
        "stream:PURGE2",
        "stream:LIQ",
        "stream:COLFD",
        "stream:CHRCY",
        "stream:CHRCY2",
        "stream:CHRCY3",
        "stream:LTENDS",
        "stream:PRODUCT"
      ],
      "dependency_versions": {
        "stream:BZIN": 1,
        "stream:H2IN": 1,
        "stream:BZIN2": 1,
        "stream:H2RCY2": 1,
        "stream:RXIN": 1,
        "stream:RXOUT": 1,
        "stream:VAP": 1,
        "stream:H2RCY": 1,
        "stream:PURGE": 1,
        "stream:PURGE2": 1,
        "stream:LIQ": 1,
        "stream:COLFD": 1,
        "stream:CHRCY": 1,
        "stream:CHRCY2": 1,
        "stream:CHRCY3": 1,
        "stream:LTENDS": 1,
        "stream:PRODUCT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "create_material_streams",
        "steps_completed": 17,
        "steps_total": 17,
        "last_result": null
      }
    },
    "aeeab72bf4e897bd": {
      "operation": "create_pump",
      "parameters": {
        "block_name": "FEEDPUMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEEDPUMP"
      ],
      "dependency_versions": {
        "block:FEEDPUMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEEDPUMP",
        "block_type": "PUMP",
        "composite": "FEEDPUMP!PUMP",
        "message": "Block FEEDPUMP (PUMP) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "0909126309d406aa": {
      "operation": "create_heater",
      "parameters": {
        "block_name": "FEED-MIX"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEED-MIX"
      ],
      "dependency_versions": {
        "block:FEED-MIX": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEED-MIX",
        "block_type": "HEATER",
        "composite": "FEED-MIX!HEATER",
        "message": "Block FEED-MIX (HEATER) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEED-MIX\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a6c7e44d982c03d4": {
      "operation": "create_rstoic",
      "parameters": {
        "block_name": "REACT"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:REACT"
      ],
      "dependency_versions": {
        "block:REACT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "REACT",
        "block_type": "RSTOIC",
        "composite": "REACT!RSTOIC",
        "message": "Block REACT (RSTOIC) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "REACT",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\REACT\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "REACT",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\REACT\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\REACT\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a2421e5bf09b3395": {
      "operation": "create_flash2",
      "parameters": {
        "block_name": "HP-SEP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:HP-SEP"
      ],
      "dependency_versions": {
        "block:HP-SEP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "HP-SEP",
        "block_type": "FLASH2",
        "composite": "HP-SEP!FLASH2",
        "message": "Block HP-SEP (FLASH2) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "HP-SEP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "HP-SEP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\HP-SEP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "9d6acd9818f63c1d": {
      "operation": "create_fsplit",
      "parameters": {
        "block_name": "VFLOW"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VFLOW"
      ],
      "dependency_versions": {
        "block:VFLOW": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VFLOW",
        "block_type": "FSPLIT",
        "composite": "VFLOW!FSPLIT",
        "message": "Block VFLOW (FSPLIT) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VFLOW",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXOL"
              ]
            },
            {
              "block": "VFLOW",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXIT",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXIT"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "315f45151cc00f4e": {
      "operation": "create_compr",
      "parameters": {
        "block_name": "COMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:COMP"
      ],
      "dependency_versions": {
        "block:COMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "COMP",
        "block_type": "COMPR",
        "composite": "COMP!COMPR",
        "message": "Block COMP (COMPR) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "COMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\COMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "COMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\COMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\COMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "608a52d659fb4d06": {
      "operation": "create_valve",
      "parameters": {
        "block_name": "VALVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VALVE"
      ],
      "dependency_versions": {
        "block:VALVE": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VALVE",
        "block_type": "VALVE",
        "composite": "VALVE!VALVE",
        "message": "Block VALVE (VALVE) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "VALVE",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXIT",
              "before": 50,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VALVE",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXOL",
              "attempted_paths": [

...[context truncated for ReAct baseline prompt]...
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 5,
  "event_counts": {
    "plan_result": 2,
    "preflight": 1,
    "session_started": 1,
    "tool_result": 1
  },
  "operation_counts_top": {
    "probe_model_state": 1
  },
  "successful_operations_tail": [
    {
      "index": 4,
      "operation": "probe_model_state",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ],
        "block_names": [
          "FEEDPUMP",
          "FEED-MIX",
          "REACT",
          "HP-SEP",
          "VFLOW",
          "COMP",
          "VALVE",
          "LFLOW",
          "PUMP",
          "PIPE",
          "COLUMN"
        ],
        "include_flowsheet": true,
        "include_ui_next": true
      }
    }
  ],
  "failures_tail": [],
  "artifacts_tail": [],
  "validator_feedback_tail": []
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "event": "tool_result",
    "operation": "probe_model_state",
    "parameters": {
      "stream_names": [
        "BZIN",
        "H2IN",
        "PRODUCT"
      ],
      "block_names": [
        "FEEDPUMP",
        "FEED-MIX",
        "REACT",
        "HP-SEP",
        "VFLOW",
        "COMP",
        "VALVE",
        "LFLOW",
        "PUMP",
        "PIPE",
        "COLUMN"
      ],
      "include_flowsheet": true,
      "include_ui_next": false
    },
    "facade": true,
    "translated_operations": [
      {
        "operation": "probe_model_state",
        "success": true,
        "error": null
      }
    ],
    "response_status": null,
    "result": {}
  },
  {
    "truncated": true,
    "chars": 8167,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 16, \"actions_executed\": 16, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"read_global_property_method\", \"parameters\": {}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"ui_check_next_completion_status\", \"parameters\": {\"close_window\": true, \"status_timeout_s\": 8.0}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"per_error\": null}}, {\"truncated\": true, \"chars\": 556, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_flowsheet_completion\\\", \\\"parameters\\\": {}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"node_path_used\\\": \\\"Data\\\\\\\\Flowsheet\\\\\\\\Section\\\\\\\\GLOBAL\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\\"input_incomplete\\\": false, \\\"input_co\\n...[truncated]\"}, {\"truncated\": true, \"chars\": 602, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"FEEDPUMP\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"block_name\\\": \\\"FEEDPUMP\\\", \\\"node_path_used\\\": \\\"Data\\\\\\\\Blocks\\\\\\\\FEEDPUMP\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\n...[truncated]\"}, {\"truncated\": true, \"chars\": 602, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"FEED-MIX\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"block_name\\\": \\\"FEED-MIX\\\", \\\"node_path_used\\\": \\\"Data\\\\\\\\Blocks\\\\\\\\FEED-MIX\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\n...[truncated]\"}, {\"truncated\": true, \"chars\": 593, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"REACT\\\"}, \\\"facade\\\": true, \\\n...[truncated]"
  },
  {
    "event": "tool_result",
    "operation": "export_final_evidence",
    "parameters": {
      "run_engine": true,
      "rep_filename": "chinese_5_1_radfrac.rep",
      "apw_filename": "chinese_5_1_radfrac.apw",
      "export_format": 2
    },
    "facade": true,
    "translated_operations": [],
    "response_status": "success",
    "result": {
      "success": true,
      "diagnostic_summary": {
        "per_error": 0,
        "converged": true,
        "rep_path": "<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210043_react_mc.rep",
        "apw_path": "<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210044_react_mc.apw",
        "messages": [],
        "value": 0,
        "path": "Data\\Results Summary\\Run-Status\\Output\\PER_ERROR",
        "rep_problem_status": {
          "converged": true,
          "hints": [
            "ID        ID               ERR/TOL      RELATIVE     ERROR       STAT  BLOCK",
            "****   MAXIMUM FINAL RELATIVE ERRORS   ****"
          ]
        },
        "repair_required": false
      }
    }
  },
  {
    "event": "plan_result",
    "actions_requested": 6,
    "actions_executed": 6,
    "stopped_on_error": false,
    "first_error_index": null,
    "pending_action_count": 0,
    "action_outcomes": [
      {
        "event": "tool_result",
        "operation": "read_stream_mole_fractions",
        "parameters": {
          "stream_name": "PRODUCT"
        },
        "facade": true,
        "translated_operations": [
          {
            "operation": "read_stream_mole_fractions",
            "success": true,
            "error": null
          }
        ],
        "response_status": "success",
        "result": {
          "success": true
        }
      },
      {
        "truncated": true,
        "chars": 840,
        "preview": "{\"event\": \"tool_result\", \"operation\": \"read_stream_outputs\", \"parameters\": {\"stream_name\": \"PRODUCT\", \"components\": [\"H2\", \"N2\", \"CH4\", \"BENZENE\", \"CYCLOHEX\"], \"basis\": \"mole_fraction\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \n...[truncated]"
      },
      {
        "event": "tool_result",
        "operation": "read_global_property_method",
        "parameters": {},
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true
        }
      },
      {
        "event": "tool_result",
        "operation": "list_block_ports",
        "parameters": {
          "block_name": "FEEDPUMP"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "message": "Found 5 port(s) for block FEEDPUMP",
          "block_name": "FEEDPUMP",
          "ports": {
            "F(IN)": [
              "BZIN"
            ],
            "WS(IN)": [],
            "P(OUT)": [
              "BZIN2"
            ],
            "WD(OUT)": [],
            "WS(OUT)": []
          }
        }
      },
      {
        "event": "tool_result",
        "operation": "list_block_ports",
        "parameters": {
          "block_name": "PUMP"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "message": "Found 5 port(s) for block PUMP",
          "block_name": "PUMP",
          "ports": {
            "F(IN)": [
              "CHRCY"
            ],
            "WS(IN)": [],
            "P(OUT)": [
              "CHRCY2"
            ],
            "WD(OUT)": [],
            "WS(OUT)": []
          }
        }
      },
      {
        "event": "tool_result",
        "operation": "list_block_ports",
        "parameters": {
          "block_name": "COLUMN"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "message": "Found 11 port(s) for block COLUMN",
          "block_name": "COLUMN",
          "ports": {
            "F(IN)": [
              "COLFD"
            ],
            "HS(IN)": [],
            "VD(OUT)": [
              "LTENDS"
            ],
            "LD(OUT)": [],
            "B(OUT)": [
              "PRODUCT"
            ],
            "SP(OUT)": [],
            "WD(OUT)": [],
            "CHS(OUT)": [],
            "RHS(OUT)": [],
            "PS(OUT)": [],
            "HS(OUT)": []
          }
        }
      }
    ]
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Need exact PRODUCT cyclohexane mole fraction from converged run plus concise supporting readbacks before finalizing.","action":"mcp_plan","operation":"readbacks_for_final_result","parameters":{"actions":[{"operation":"read_stream_output","parameters":{"stream_name":"PRODUCT","variable":"mole_fraction","component_name":"CYCLOHEX"}},{"operation":"read_stream_output","parameters":{"stream_name":"PRODUCT","variable":"total_flow"}},{"operation":"read_stream_outputs","parameters":{"stream_name":"PRODUCT","components":["H2","N2","CH4","BENZENE","CYCLOHEX"],"basis":"mole_fraction"}},{"operation":"read_global_property_method","parameters":{}},{"operation":"node_info","parameters":{"path":"Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC"}},{"operation":"node_info","parameters":{"path":"Data\\Blocks\\PUMP\\Input\\OPT_SPEC"}}]}}
```

</details>

## Call 9: `select_action`

- Input tokens: **132,645**
- Output tokens: **731**
- Total tokens: **133,376**
- Provider cost: **$0.685155**
- Recorded at: `2026-10-18T21:01:12.979`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 75,
    "domain_versions": {
      "properties": 2,
      "flowsheet": 75,
      "stream:H2RCY2": 5,
      "stream:CHRCY2": 5,
      "stream:LIQ": 5,
      "stream:RXOUT": 5,
      "stream:PURGE": 5,
      "stream:BZIN": 5,
      "stream:PRODUCT": 3,
      "stream:H2IN": 5,
      "stream:CHRCY3": 5,
      "stream:LTENDS": 3,
      "stream:BZIN2": 5,
      "stream:VAP": 5,
      "stream:H2RCY": 5,
      "stream:PURGE2": 3,
      "stream:CHRCY": 5,
      "stream:RXIN": 5,
      "stream:COLFD": 7,
      "block:FEEDPUMP": 12,
      "block:FEED-MIX": 6,
      "block:REACT": 6,
      "block:HP-SEP": 4,
      "block:VFLOW": 3,
      "block:COMP": 4,
      "block:VALVE": 4,
      "block:LFLOW": 3,
      "block:PUMP": 6,
      "block:PIPE": 4,
      "block:COLUMN": 13
    },
    "components": [
      "H2",
      "N2",
      "CH4",
      "BENZENE",
      "CYCLOHEX"
    ],
    "property_method": "",
    "blocks": [
      "FEEDPUMP",
      "FEED-MIX",
      "REACT",
      "HP-SEP",
      "VFLOW",
      "COMP",
      "VALVE",
      "LFLOW",
      "PUMP",
      "PIPE",
      "COLUMN"
    ],
    "streams": [
      "BZIN",
      "H2IN",
      "BZIN2",
      "H2RCY2",
      "RXIN",
      "RXOUT",
      "VAP",
      "H2RCY",
      "PURGE",
      "PURGE2",
      "LIQ",
      "COLFD",
      "CHRCY",
      "CHRCY2",
      "CHRCY3",
      "LTENDS",
      "PRODUCT"
    ],
    "connections": [
      {
        "block_name": "COLUMN",
        "stream_name": "COLFD",
        "port_name": "F(IN)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "LTENDS",
        "port_name": "VD(OUT)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "PRODUCT",
        "port_name": "B(OUT)",
        "source_operation": "connect_stream"
      }
    ],
    "specs": [
      {
        "stream_name": "H2IN",
        "temperature": 50.0,
        "pressure": 2.5,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      },
      {
        "stream_name": "BZIN",
        "temperature": 40.0,
        "pressure": 0.1,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      }
    ],
    "engine_run": null,
    "artifacts": {},
    "readbacks": []
  },
  "operation_ledger": {
    "677ff79d23598058": {
      "operation": "add_components_by_cas",
      "parameters": {
        "components": [
          {
            "component_id": "H2",
            "cas": "1333-74-0"
          },
          {
            "component_id": "N2",
            "cas": "7727-37-9"
          },
          {
            "component_id": "CH4",
            "cas": "74-82-8"
          },
          {
            "component_id": "BENZENE",
            "cas": "71-43-2"
          },
          {
            "component_id": "CYCLOHEX",
            "cas": "110-82-7"
          }
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "components_added": [
          {
            "cas": "1333740",
            "component_id": "H2",
            "requested_component_id": "H2",
            "preferred_component_id": "H2"
          },
          {
            "cas": "7727379",
            "component_id": "N2",
            "requested_component_id": "N2",
            "preferred_component_id": "N2"
          },
          {
            "cas": "74-82-8",
            "component_id": "CH4",
            "requested_component_id": "CH4",
            "preferred_component_id": "CH4"
          },
          {
            "cas": "71-43-2",
            "component_id": "BENZENE",
            "requested_component_id": "BENZENE",
            "preferred_component_id": "BENZENE"
          },
          {
            "cas": "110-82-7",
            "component_id": "CYCLOHEX",
            "requested_component_id": "CYCLOHEX",
            "preferred_component_id": "CYCLOHEX"
          }
        ],
        "count": 5,
        "message": "Added 5 component(s) successfully",
        "verification": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "missing_component_ids": []
        },
        "contamination": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "extra_component_ids": [],
          "generic_extra_component_ids": []
        }
      }
    },
    "d0f7c037faabb2bb": {
      "operation": "ensure_property_method",
      "parameters": {
        "method": "RK-SOAVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 2
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "ensure_property_method",
        "steps_completed": 5,
        "steps_total": 5,
        "last_result": null
      }
    },
    "33ce8ec6c91a3f71": {
      "operation": "create_material_streams",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "stream:BZIN",
        "stream:H2IN",
        "stream:BZIN2",
        "stream:H2RCY2",
        "stream:RXIN",
        "stream:RXOUT",
        "stream:VAP",
        "stream:H2RCY",
        "stream:PURGE",
        "stream:PURGE2",
        "stream:LIQ",
        "stream:COLFD",
        "stream:CHRCY",
        "stream:CHRCY2",
        "stream:CHRCY3",
        "stream:LTENDS",
        "stream:PRODUCT"
      ],
      "dependency_versions": {
        "stream:BZIN": 1,
        "stream:H2IN": 1,
        "stream:BZIN2": 1,
        "stream:H2RCY2": 1,
        "stream:RXIN": 1,
        "stream:RXOUT": 1,
        "stream:VAP": 1,
        "stream:H2RCY": 1,
        "stream:PURGE": 1,
        "stream:PURGE2": 1,
        "stream:LIQ": 1,
        "stream:COLFD": 1,
        "stream:CHRCY": 1,
        "stream:CHRCY2": 1,
        "stream:CHRCY3": 1,
        "stream:LTENDS": 1,
        "stream:PRODUCT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "create_material_streams",
        "steps_completed": 17,
        "steps_total": 17,
        "last_result": null
      }
    },
    "aeeab72bf4e897bd": {
      "operation": "create_pump",
      "parameters": {
        "block_name": "FEEDPUMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEEDPUMP"
      ],
      "dependency_versions": {
        "block:FEEDPUMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEEDPUMP",
        "block_type": "PUMP",
        "composite": "FEEDPUMP!PUMP",
        "message": "Block FEEDPUMP (PUMP) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "0909126309d406aa": {
      "operation": "create_heater",
      "parameters": {
        "block_name": "FEED-MIX"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEED-MIX"
      ],
      "dependency_versions": {
        "block:FEED-MIX": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEED-MIX",
        "block_type": "HEATER",
        "composite": "FEED-MIX!HEATER",
        "message": "Block FEED-MIX (HEATER) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEED-MIX",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEED-MIX\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEED-MIX\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a6c7e44d982c03d4": {
      "operation": "create_rstoic",
      "parameters": {
        "block_name": "REACT"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:REACT"
      ],
      "dependency_versions": {
        "block:REACT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "REACT",
        "block_type": "RSTOIC",
        "composite": "REACT!RSTOIC",
        "message": "Block REACT (RSTOIC) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "REACT",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\REACT\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "REACT",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\REACT\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\REACT\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "a2421e5bf09b3395": {
      "operation": "create_flash2",
      "parameters": {
        "block_name": "HP-SEP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:HP-SEP"
      ],
      "dependency_versions": {
        "block:HP-SEP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "HP-SEP",
        "block_type": "FLASH2",
        "composite": "HP-SEP!FLASH2",
        "message": "Block HP-SEP (FLASH2) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "HP-SEP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "HP-SEP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\HP-SEP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\HP-SEP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "9d6acd9818f63c1d": {
      "operation": "create_fsplit",
      "parameters": {
        "block_name": "VFLOW"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VFLOW"
      ],
      "dependency_versions": {
        "block:VFLOW": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VFLOW",
        "block_type": "FSPLIT",
        "composite": "VFLOW!FSPLIT",
        "message": "Block VFLOW (FSPLIT) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VFLOW",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXOL"
              ]
            },
            {
              "block": "VFLOW",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VFLOW\\Input\\MAXIT",
              "attempted_paths": [
                "Data\\Blocks\\VFLOW\\Input\\MAXIT"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "315f45151cc00f4e": {
      "operation": "create_compr",
      "parameters": {
        "block_name": "COMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:COMP"
      ],
      "dependency_versions": {
        "block:COMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "COMP",
        "block_type": "COMPR",
        "composite": "COMP!COMPR",
        "message": "Block COMP (COMPR) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "COMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\COMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "COMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\COMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\COMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "608a52d659fb4d06": {
      "operation": "create_valve",
      "parameters": {
        "block_name": "VALVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:VALVE"
      ],
      "dependency_versions": {
        "block:VALVE": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "VALVE",
        "block_type": "VALVE",
        "composite": "VALVE!VALVE",
        "message": "Block VALVE (VALVE) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "VALVE",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXIT",
              "before": 50,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "VALVE",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\VALVE\\Input\\MAXOL",
              "attempted_paths": [

...[context truncated for ReAct baseline prompt]...
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 6,
  "event_counts": {
    "plan_result": 2,
    "tool_result": 2,
    "preflight": 1,
    "session_started": 1
  },
  "operation_counts_top": {
    "probe_model_state": 2
  },
  "successful_operations_tail": [
    {
      "index": 4,
      "operation": "probe_model_state",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ],
        "block_names": [
          "FEEDPUMP",
          "FEED-MIX",
          "REACT",
          "HP-SEP",
          "VFLOW",
          "COMP",
          "VALVE",
          "LFLOW",
          "PUMP",
          "PIPE",
          "COLUMN"
        ],
        "include_flowsheet": true,
        "include_ui_next": true
      }
    },
    {
      "index": 5,
      "operation": "probe_model_state",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "PRODUCT"
        ],
        "block_names": [
          "FEEDPUMP",
          "FEED-MIX",
          "REACT",
          "HP-SEP",
          "VFLOW",
          "COMP",
          "VALVE",
          "LFLOW",
          "PUMP",
          "PIPE",
          "COLUMN"
        ],
        "include_flowsheet": true,
        "include_ui_next": false
      }
    }
  ],
  "failures_tail": [],
  "artifacts_tail": [],
  "validator_feedback_tail": []
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "truncated": true,
    "chars": 8167,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 16, \"actions_executed\": 16, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"read_global_property_method\", \"parameters\": {}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true}}, {\"event\": \"tool_result\", \"operation\": \"ui_check_next_completion_status\", \"parameters\": {\"close_window\": true, \"status_timeout_s\": 8.0}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"per_error\": null}}, {\"truncated\": true, \"chars\": 556, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_flowsheet_completion\\\", \\\"parameters\\\": {}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"node_path_used\\\": \\\"Data\\\\\\\\Flowsheet\\\\\\\\Section\\\\\\\\GLOBAL\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\\"input_incomplete\\\": false, \\\"input_co\\n...[truncated]\"}, {\"truncated\": true, \"chars\": 602, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"FEEDPUMP\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"block_name\\\": \\\"FEEDPUMP\\\", \\\"node_path_used\\\": \\\"Data\\\\\\\\Blocks\\\\\\\\FEEDPUMP\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\n...[truncated]\"}, {\"truncated\": true, \"chars\": 602, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"FEED-MIX\\\"}, \\\"facade\\\": true, \\\"translated_operations\\\": [], \\\"response_status\\\": \\\"success\\\", \\\"result\\\": {\\\"success\\\": true, \\\"block_name\\\": \\\"FEED-MIX\\\", \\\"node_path_used\\\": \\\"Data\\\\\\\\Blocks\\\\\\\\FEED-MIX\\\", \\\"input_state\\\": \\\"complete\\\", \\\"input_complete\\\": true, \\\"status_flags\\\": {\\\"results_success\\\": false, \\\"no_results\\\": true, \\\"results_warnings\\\": false, \\n...[truncated]\"}, {\"truncated\": true, \"chars\": 593, \"preview\": \"{\\\"event\\\": \\\"tool_result\\\", \\\"operation\\\": \\\"check_block_completion\\\", \\\"parameters\\\": {\\\"block_name\\\": \\\"REACT\\\"}, \\\"facade\\\": true, \\\n...[truncated]"
  },
  {
    "event": "tool_result",
    "operation": "export_final_evidence",
    "parameters": {
      "run_engine": true,
      "rep_filename": "chinese_5_1_radfrac.rep",
      "apw_filename": "chinese_5_1_radfrac.apw",
      "export_format": 2
    },
    "facade": true,
    "translated_operations": [],
    "response_status": "success",
    "result": {
      "success": true,
      "diagnostic_summary": {
        "per_error": 0,
        "converged": true,
        "rep_path": "<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210043_react_mc.rep",
        "apw_path": "<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210044_react_mc.apw",
        "messages": [],
        "value": 0,
        "path": "Data\\Results Summary\\Run-Status\\Output\\PER_ERROR",
        "rep_problem_status": {
          "converged": true,
          "hints": [
            "ID        ID               ERR/TOL      RELATIVE     ERROR       STAT  BLOCK",
            "****   MAXIMUM FINAL RELATIVE ERRORS   ****"
          ]
        },
        "repair_required": false
      }
    }
  },
  {
    "event": "plan_result",
    "actions_requested": 6,
    "actions_executed": 6,
    "stopped_on_error": false,
    "first_error_index": null,
    "pending_action_count": 0,
    "action_outcomes": [
      {
        "event": "tool_result",
        "operation": "read_stream_mole_fractions",
        "parameters": {
          "stream_name": "PRODUCT"
        },
        "facade": true,
        "translated_operations": [
          {
            "operation": "read_stream_mole_fractions",
            "success": true,
            "error": null
          }
        ],
        "response_status": "success",
        "result": {
          "success": true
        }
      },
      {
        "truncated": true,
        "chars": 840,
        "preview": "{\"event\": \"tool_result\", \"operation\": \"read_stream_outputs\", \"parameters\": {\"stream_name\": \"PRODUCT\", \"components\": [\"H2\", \"N2\", \"CH4\", \"BENZENE\", \"CYCLOHEX\"], \"basis\": \"mole_fraction\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \n...[truncated]"
      },
      {
        "event": "tool_result",
        "operation": "read_global_property_method",
        "parameters": {},
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true
        }
      },
      {
        "event": "tool_result",
        "operation": "list_block_ports",
        "parameters": {
          "block_name": "FEEDPUMP"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "message": "Found 5 port(s) for block FEEDPUMP",
          "block_name": "FEEDPUMP",
          "ports": {
            "F(IN)": [
              "BZIN"
            ],
            "WS(IN)": [],
            "P(OUT)": [
              "BZIN2"
            ],
            "WD(OUT)": [],
            "WS(OUT)": []
          }
        }
      },
      {
        "event": "tool_result",
        "operation": "list_block_ports",
        "parameters": {
          "block_name": "PUMP"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "message": "Found 5 port(s) for block PUMP",
          "block_name": "PUMP",
          "ports": {
            "F(IN)": [
              "CHRCY"
            ],
            "WS(IN)": [],
            "P(OUT)": [
              "CHRCY2"
            ],
            "WD(OUT)": [],
            "WS(OUT)": []
          }
        }
      },
      {
        "event": "tool_result",
        "operation": "list_block_ports",
        "parameters": {
          "block_name": "COLUMN"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "message": "Found 11 port(s) for block COLUMN",
          "block_name": "COLUMN",
          "ports": {
            "F(IN)": [
              "COLFD"
            ],
            "HS(IN)": [],
            "VD(OUT)": [
              "LTENDS"
            ],
            "LD(OUT)": [],
            "B(OUT)": [
              "PRODUCT"
            ],
            "SP(OUT)": [],
            "WD(OUT)": [],
            "CHS(OUT)": [],
            "RHS(OUT)": [],
            "PS(OUT)": [],
            "HS(OUT)": []
          }
        }
      }
    ]
  },
  {
    "event": "plan_result",
    "actions_requested": 6,
    "actions_executed": 6,
    "stopped_on_error": false,
    "first_error_index": null,
    "pending_action_count": 0,
    "action_outcomes": [
      {
        "event": "tool_result",
        "operation": "read_stream_output",
        "parameters": {
          "stream_name": "PRODUCT",
          "variable": "mole_fraction",
          "component_name": "CYCLOHEX"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "stream_name": "PRODUCT",
          "value": 0.999122737,
          "unit": null,
          "path": "\\Data\\Streams\\PRODUCT\\Output\\MOLEFRAC\\MIXED\\CYCLOHEX"
        }
      },
      {
        "event": "tool_result",
        "operation": "read_stream_output",
        "parameters": {
          "stream_name": "PRODUCT",
          "variable": "total_flow"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "stream_name": "PRODUCT",
          "value": 2.45448313,
          "unit": null,
          "path": "\\Data\\Streams\\PRODUCT\\Output\\TOT_FLOW"
        }
      },
      {
        "truncated": true,
        "chars": 840,
        "preview": "{\"event\": \"tool_result\", \"operation\": \"read_stream_outputs\", \"parameters\": {\"stream_name\": \"PRODUCT\", \"components\": [\"H2\", \"N2\", \"CH4\", \"BENZENE\", \"CYCLOHEX\"], \"basis\": \"mole_fraction\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \n...[truncated]"
      },
      {
        "event": "tool_result",
        "operation": "read_global_property_method",
        "parameters": {},
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true
        }
      },
      {
        "event": "tool_result",
        "operation": "node_info",
        "parameters": {
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC"
        }
      },
      {
        "event": "tool_result",
        "operation": "node_info",
        "parameters": {
          "path": "Data\\Blocks\\PUMP\\Input\\OPT_SPEC"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "path": "Data\\Blocks\\PUMP\\Input\\OPT_SPEC"
        }
      }
    ]
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Need concrete readback evidence for pump modes/curve and broader topology before finalizing.","action":"mcp_plan","operation":"batch","parameters":{"actions":[{"operation":"node_props","parameters":{"path":"Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC"}},{"operation":"node_props","parameters":{"path":"Data\\Blocks\\FEEDPUMP\\Input\\OPT_CTYPE"}},{"operation":"node_props","parameters":{"path":"Data\\Blocks\\FEEDPUMP\\Input\\OPT_CFORMAT"}},{"operation":"node_props","parameters":{"path":"Data\\Blocks\\FEEDPUMP\\Input\\DEP_VAR"}},{"operation":"node_props","parameters":{"path":"Data\\Blocks\\FEEDPUMP\\Input\\INDEP_VAR"}},{"operation":"node_props","parameters":{"path":"Data\\Blocks\\FEEDPUMP\\Input\\EFF"}},{"operation":"node_props","parameters":{"path":"Data\\Blocks\\FEEDPUMP\\Input\\DEFF"}},{"operation":"node_props","parameters":{"path":"Data\\Blocks\\PUMP\\Input\\OPT_SPEC"}},{"operation":"node_props","parameters":{"path":"Data\\Blocks\\PUMP\\Input\\PRES"}},{"operation":"list_block_ports","parameters":{"block_name":"FEED-MIX"}},{"operation":"list_block_ports","parameters":{"block_name":"REACT"}},{"operation":"list_block_ports","parameters":{"block_name":"HP-SEP"}},{"operation":"list_block_ports","parameters":{"block_name":"VFLOW"}},{"operation":"list_block_ports","parameters":{"block_name":"COMP"}},{"operation":"list_block_ports","parameters":{"block_name":"VALVE"}},{"operation":"list_block_ports","parameters":{"block_name":"LFLOW"}},{"operation":"list_block_ports","parameters":{"block_name":"PIPE"}}]}} 

```

</details>

## Call 10: `select_action`

- Input tokens: **132,727**
- Output tokens: **736**
- Total tokens: **133,463**
- Provider cost: **$0.685715**
- Recorded at: `2026-10-18T21:01:25.175`
- Input provenance: `reconstructed_from_persisted_state`

<details><summary>Dynamic input: memory and observation context</summary>

#### Memory summary

```text
{
  "case_id": "chinese_5_1_radfrac",
  "stateful_reducer": {
    "enabled": false,
    "contract": "Preserve the complete normalized action ledger and current Aspen state; never trim already-operated state facts."
  },
  "task_requirements": {
    "source": "task text and gate contract in prompt",
    "do_not_use_rejected_surrogates": []
  },
  "current_model_state": {
    "state_version": 75,
    "domain_versions": {
      "properties": 2,
      "flowsheet": 75,
      "stream:H2RCY2": 5,
      "stream:CHRCY2": 5,
      "stream:LIQ": 5,
      "stream:RXOUT": 5,
      "stream:PURGE": 5,
      "stream:BZIN": 5,
      "stream:PRODUCT": 3,
      "stream:H2IN": 5,
      "stream:CHRCY3": 5,
      "stream:LTENDS": 3,
      "stream:BZIN2": 5,
      "stream:VAP": 5,
      "stream:H2RCY": 5,
      "stream:PURGE2": 3,
      "stream:CHRCY": 5,
      "stream:RXIN": 5,
      "stream:COLFD": 7,
      "block:FEEDPUMP": 12,
      "block:FEED-MIX": 6,
      "block:REACT": 6,
      "block:HP-SEP": 4,
      "block:VFLOW": 3,
      "block:COMP": 4,
      "block:VALVE": 4,
      "block:LFLOW": 3,
      "block:PUMP": 6,
      "block:PIPE": 4,
      "block:COLUMN": 13
    },
    "components": [
      "H2",
      "N2",
      "CH4",
      "BENZENE",
      "CYCLOHEX"
    ],
    "property_method": "",
    "blocks": [
      "FEEDPUMP",
      "FEED-MIX",
      "REACT",
      "HP-SEP",
      "VFLOW",
      "COMP",
      "VALVE",
      "LFLOW",
      "PUMP",
      "PIPE",
      "COLUMN"
    ],
    "streams": [
      "BZIN",
      "H2IN",
      "BZIN2",
      "H2RCY2",
      "RXIN",
      "RXOUT",
      "VAP",
      "H2RCY",
      "PURGE",
      "PURGE2",
      "LIQ",
      "COLFD",
      "CHRCY",
      "CHRCY2",
      "CHRCY3",
      "LTENDS",
      "PRODUCT"
    ],
    "connections": [
      {
        "block_name": "COLUMN",
        "stream_name": "COLFD",
        "port_name": "F(IN)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "LTENDS",
        "port_name": "VD(OUT)",
        "source_operation": "connect_stream"
      },
      {
        "block_name": "COLUMN",
        "stream_name": "PRODUCT",
        "port_name": "B(OUT)",
        "source_operation": "connect_stream"
      }
    ],
    "specs": [
      {
        "stream_name": "H2IN",
        "temperature": 50.0,
        "pressure": 2.5,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      },
      {
        "stream_name": "BZIN",
        "temperature": 40.0,
        "pressure": 0.1,
        "vapor_fraction": null,
        "mixed_spec": "TP",
        "temperature_unit": "C",
        "pressure_unit": "MPa",
        "source_operation": "set_material_stream_conditions"
      }
    ],
    "engine_run": null,
    "artifacts": {},
    "readbacks": [
      {
        "operation": "node_props",
        "parameters": {
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC"
        },
        "result": {
          "success": true,
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC",
          "normalized_path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC",
          "attempted_paths": [
            "Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC"
          ],
          "exists": true,
          "has_elements": false,
          "props": {
            "HAP_PROMPT": "",
            "HAP_OPTIONLIST": "PRES\nDELP\nPRATIO\nPOWER\nUSE-CURVE",
            "HAP_UNITROW": 0,
            "HAP_UNITCOL": 0,
            "HAP_HASCHILDREN": 0,
            "ValueType": 3,
            "Name": "OPT_SPEC",
            "Value": "USE-CURVE"
          }
        }
      },
      {
        "operation": "node_props",
        "parameters": {
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_CTYPE"
        },
        "result": {
          "success": true,
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_CTYPE",
          "normalized_path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_CTYPE",
          "attempted_paths": [
            "Data\\Blocks\\FEEDPUMP\\Input\\OPT_CTYPE"
          ],
          "exists": true,
          "has_elements": false,
          "props": {
            "HAP_PROMPT": "",
            "HAP_OPTIONLIST": "SINGLE-OPER\nSINGLE-REFE\nMULTIP",
            "HAP_UNITROW": 0,
            "HAP_UNITCOL": 0,
            "HAP_HASCHILDREN": 0,
            "ValueType": 3,
            "Name": "OPT_CTYPE",
            "Value": "SINGLE-OPER"
          }
        }
      },
      {
        "operation": "node_props",
        "parameters": {
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_CFORMAT"
        },
        "result": {
          "success": true,
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_CFORMAT",
          "normalized_path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_CFORMAT",
          "attempted_paths": [
            "Data\\Blocks\\FEEDPUMP\\Input\\OPT_CFORMAT"
          ],
          "exists": true,
          "has_elements": false,
          "props": {
            "HAP_PROMPT": "",
            "HAP_OPTIONLIST": "TABLE\nPOLY\nUSER-CURVES",
            "HAP_UNITROW": 0,
            "HAP_UNITCOL": 0,
            "HAP_HASCHILDREN": 0,
            "ValueType": 3,
            "Name": "OPT_CFORMAT",
            "Value": "TABLE"
          }
        }
      },
      {
        "operation": "node_props",
        "parameters": {
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\DEP_VAR"
        },
        "result": {
          "success": true,
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\DEP_VAR",
          "normalized_path": "Data\\Blocks\\FEEDPUMP\\Input\\DEP_VAR",
          "attempted_paths": [
            "Data\\Blocks\\FEEDPUMP\\Input\\DEP_VAR"
          ],
          "exists": true,
          "has_elements": false,
          "props": {
            "HAP_PROMPT": "Type of performance curve(s). Specify the curve data in Curve Data sheet.",
            "HAP_OPTIONLIST": "HEAD\nHEAD-COEF\nPOWER\nPRES\nPRAT\nDELP",
            "HAP_UNITROW": 0,
            "HAP_UNITCOL": 0,
            "HAP_HASCHILDREN": 0,
            "ValueType": 3,
            "Name": "DEP_VAR",
            "Value": "HEAD"
          }
        }
      },
      {
        "operation": "node_props",
        "parameters": {
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\INDEP_VAR"
        },
        "result": {
          "success": true,
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\INDEP_VAR",
          "normalized_path": "Data\\Blocks\\FEEDPUMP\\Input\\INDEP_VAR",
          "attempted_paths": [
            "Data\\Blocks\\FEEDPUMP\\Input\\INDEP_VAR"
          ],
          "exists": true,
          "has_elements": false,
          "props": {
            "HAP_PROMPT": "Type of flow variable used for performance curve(s).",
            "HAP_OPTIONLIST": "VOL-FLOW\nMASS-FLOW",
            "HAP_UNITROW": 0,
            "HAP_UNITCOL": 0,
            "HAP_HASCHILDREN": 0,
            "ValueType": 3,
            "Name": "INDEP_VAR",
            "Value": "VOL-FLOW"
          }
        }
      },
      {
        "operation": "node_props",
        "parameters": {
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\EFF"
        },
        "result": {
          "success": true,
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\EFF",
          "normalized_path": "Data\\Blocks\\FEEDPUMP\\Input\\EFF",
          "attempted_paths": [
            "Data\\Blocks\\FEEDPUMP\\Input\\EFF"
          ],
          "exists": true,
          "has_elements": false,
          "props": {
            "HAP_PROMPT": "Efficiency. Pump: fluid HP/brake HP. Turbine: brake HP/fluid HP. Use Help for information on default value.",
            "HAP_VALUEDEFAULT": 1e+35,
            "HAP_UPPERLIMIT": 1.0,
            "HAP_LOWERLIMIT": 1e-15,
            "HAP_UNITROW": 0,
            "HAP_UNITCOL": 0,
            "HAP_HASCHILDREN": 0,
            "ValueType": 2,
            "Name": "EFF",
            "Value": 0.6
          }
        }
      },
      {
        "operation": "node_props",
        "parameters": {
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\DEFF"
        },
        "result": {
          "success": true,
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\DEFF",
          "normalized_path": "Data\\Blocks\\FEEDPUMP\\Input\\DEFF",
          "attempted_paths": [
            "Data\\Blocks\\FEEDPUMP\\Input\\DEFF"
          ],
          "exists": true,
          "has_elements": false,
          "props": {
            "HAP_PROMPT": "Driver efficiency. Pump: brake HP/electrical HP. Turbine: electrical HP/ brake HP. Default=1.",
            "HAP_VALUEDEFAULT": 1.0,
            "HAP_UPPERLIMIT": 1.0,
            "HAP_LOWERLIMIT": 1e-15,
            "HAP_UNITROW": 0,
            "HAP_UNITCOL": 0,
            "HAP_HASCHILDREN": 0,
            "ValueType": 2,
            "Name": "DEFF",
            "Value": 0.9
          }
        }
      },
      {
        "operation": "node_props",
        "parameters": {
          "path": "Data\\Blocks\\PUMP\\Input\\OPT_SPEC"
        },
        "result": {
          "success": true,
          "path": "Data\\Blocks\\PUMP\\Input\\OPT_SPEC",
          "normalized_path": "Data\\Blocks\\PUMP\\Input\\OPT_SPEC",
          "attempted_paths": [
            "Data\\Blocks\\PUMP\\Input\\OPT_SPEC"
          ],
          "exists": true,
          "has_elements": false,
          "props": {
            "HAP_PROMPT": "",
            "HAP_OPTIONLIST": "PRES\nDELP\nPRATIO\nPOWER\nUSE-CURVE",
            "HAP_UNITROW": 0,
            "HAP_UNITCOL": 0,
            "HAP_HASCHILDREN": 0,
            "ValueType": 3,
            "Name": "OPT_SPEC",
            "Value": "PRES"
          }
        }
      },
      {
        "operation": "node_props",
        "parameters": {
          "path": "Data\\Blocks\\PUMP\\Input\\PRES"
        },
        "result": {
          "success": true,
          "path": "Data\\Blocks\\PUMP\\Input\\PRES",
          "normalized_path": "Data\\Blocks\\PUMP\\Input\\PRES",
          "attempted_paths": [
            "Data\\Blocks\\PUMP\\Input\\PRES"
          ],
          "exists": true,
          "has_elements": false,
          "props": {
            "HAP_PROMPT": "Outlet pressure.",
            "HAP_VALUEDEFAULT": 1e+35,
            "HAP_UPPERLIMIT": 10000000000.0,
            "HAP_LOWERLIMIT": 1e-15,
            "HAP_UNITROW": 20,
            "HAP_UNITCOL": 20,
            "HAP_HASCHILDREN": 0,
            "ValueType": 2,
            "Name": "PRES",
            "Value": 2.6
          }
        }
      }
    ]
  },
  "operation_ledger": {
    "677ff79d23598058": {
      "operation": "add_components_by_cas",
      "parameters": {
        "components": [
          {
            "component_id": "H2",
            "cas": "1333-74-0"
          },
          {
            "component_id": "N2",
            "cas": "7727-37-9"
          },
          {
            "component_id": "CH4",
            "cas": "74-82-8"
          },
          {
            "component_id": "BENZENE",
            "cas": "71-43-2"
          },
          {
            "component_id": "CYCLOHEX",
            "cas": "110-82-7"
          }
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "components_added": [
          {
            "cas": "1333740",
            "component_id": "H2",
            "requested_component_id": "H2",
            "preferred_component_id": "H2"
          },
          {
            "cas": "7727379",
            "component_id": "N2",
            "requested_component_id": "N2",
            "preferred_component_id": "N2"
          },
          {
            "cas": "74-82-8",
            "component_id": "CH4",
            "requested_component_id": "CH4",
            "preferred_component_id": "CH4"
          },
          {
            "cas": "71-43-2",
            "component_id": "BENZENE",
            "requested_component_id": "BENZENE",
            "preferred_component_id": "BENZENE"
          },
          {
            "cas": "110-82-7",
            "component_id": "CYCLOHEX",
            "requested_component_id": "CYCLOHEX",
            "preferred_component_id": "CYCLOHEX"
          }
        ],
        "count": 5,
        "message": "Added 5 component(s) successfully",
        "verification": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "missing_component_ids": []
        },
        "contamination": {
          "success": true,
          "expected_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "actual_component_ids": [
            "H2",
            "N2",
            "CH4",
            "BENZENE",
            "CYCLOHEX"
          ],
          "extra_component_ids": [],
          "generic_extra_component_ids": []
        }
      }
    },
    "d0f7c037faabb2bb": {
      "operation": "ensure_property_method",
      "parameters": {
        "method": "RK-SOAVE"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "properties"
      ],
      "dependency_versions": {
        "properties": 2
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "ensure_property_method",
        "steps_completed": 5,
        "steps_total": 5,
        "last_result": null
      }
    },
    "33ce8ec6c91a3f71": {
      "operation": "create_material_streams",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ]
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "stream:BZIN",
        "stream:H2IN",
        "stream:BZIN2",
        "stream:H2RCY2",
        "stream:RXIN",
        "stream:RXOUT",
        "stream:VAP",
        "stream:H2RCY",
        "stream:PURGE",
        "stream:PURGE2",
        "stream:LIQ",
        "stream:COLFD",
        "stream:CHRCY",
        "stream:CHRCY2",
        "stream:CHRCY3",
        "stream:LTENDS",
        "stream:PRODUCT"
      ],
      "dependency_versions": {
        "stream:BZIN": 1,
        "stream:H2IN": 1,
        "stream:BZIN2": 1,
        "stream:H2RCY2": 1,
        "stream:RXIN": 1,
        "stream:RXOUT": 1,
        "stream:VAP": 1,
        "stream:H2RCY": 1,
        "stream:PURGE": 1,
        "stream:PURGE2": 1,
        "stream:LIQ": 1,
        "stream:COLFD": 1,
        "stream:CHRCY": 1,
        "stream:CHRCY2": 1,
        "stream:CHRCY3": 1,
        "stream:LTENDS": 1,
        "stream:PRODUCT": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "virtual_tool": "create_material_streams",
        "steps_completed": 17,
        "steps_total": 17,
        "last_result": null
      }
    },
    "aeeab72bf4e897bd": {
      "operation": "create_pump",
      "parameters": {
        "block_name": "FEEDPUMP"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEEDPUMP"
      ],
      "dependency_versions": {
        "block:FEEDPUMP": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEEDPUMP",
        "block_type": "PUMP",
        "composite": "FEEDPUMP!PUMP",
        "message": "Block FEEDPUMP (PUMP) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"
          ],
          "raised": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXIT",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXIT",
              "before": 30,
              "after": 200
            }
          ],
          "unchanged": [],
          "failed": [],
          "missing": [
            {
              "block": "FEEDPUMP",
              "leaf": "MAXOL",
              "path": "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL",
              "attempted_paths": [
                "Data\\Blocks\\FEEDPUMP\\Input\\MAXOL"
              ]
            }
          ],
          "success": true
        }
      }
    },
    "0909126309d406aa": {
      "operation": "create_heater",
      "parameters": {
        "block_name": "FEED-MIX"
      },
      "attempts": 1,
      "successes": 1,
      "failures": 0,
      "dependency_domains": [
        "block:FEED-MIX"
      ],
      "dependency_versions": {
        "block:FEED-MIX": 1
      },
      "last_status": "success",
      "last_evidence": {
        "success": true,
        "block_name": "FEED-MIX",
        "block_type": "HEATER",
        "composite": "FEED-MIX!HEATER",
        "message": "Block FEED-MIX (HEATER) created successfully",
        "block_iteration_floor": {
          "attempted": true,
          "floor": 200,
          "via": "com_tree",
          "reason": "post-block-create",
          "leaves": [
            "MAXOL",
            "MAXIT"

...[context truncated for ReAct baseline prompt]...
```

#### Observation context

```text
PROMPT_REDUCER: enabled; full uncompressed trajectory remains in react_mcp_trajectory.jsonl.
OLDER_OBSERVATION_DIGEST:
{
  "observation_count": 7,
  "event_counts": {
    "plan_result": 3,
    "tool_result": 2,
    "preflight": 1,
    "session_started": 1
  },
  "operation_counts_top": {
    "probe_model_state": 2
  },
  "successful_operations_tail": [
    {
      "index": 4,
      "operation": "probe_model_state",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "BZIN2",
          "H2RCY2",
          "RXIN",
          "RXOUT",
          "VAP",
          "H2RCY",
          "PURGE",
          "PURGE2",
          "LIQ",
          "COLFD",
          "CHRCY",
          "CHRCY2",
          "CHRCY3",
          "LTENDS",
          "PRODUCT"
        ],
        "block_names": [
          "FEEDPUMP",
          "FEED-MIX",
          "REACT",
          "HP-SEP",
          "VFLOW",
          "COMP",
          "VALVE",
          "LFLOW",
          "PUMP",
          "PIPE",
          "COLUMN"
        ],
        "include_flowsheet": true,
        "include_ui_next": true
      }
    },
    {
      "index": 5,
      "operation": "probe_model_state",
      "parameters": {
        "stream_names": [
          "BZIN",
          "H2IN",
          "PRODUCT"
        ],
        "block_names": [
          "FEEDPUMP",
          "FEED-MIX",
          "REACT",
          "HP-SEP",
          "VFLOW",
          "COMP",
          "VALVE",
          "LFLOW",
          "PUMP",
          "PIPE",
          "COLUMN"
        ],
        "include_flowsheet": true,
        "include_ui_next": false
      }
    }
  ],
  "failures_tail": [],
  "artifacts_tail": [],
  "validator_feedback_tail": []
}

RECENT_OBSERVATIONS_COMPACT:
[
  {
    "event": "tool_result",
    "operation": "export_final_evidence",
    "parameters": {
      "run_engine": true,
      "rep_filename": "chinese_5_1_radfrac.rep",
      "apw_filename": "chinese_5_1_radfrac.apw",
      "export_format": 2
    },
    "facade": true,
    "translated_operations": [],
    "response_status": "success",
    "result": {
      "success": true,
      "diagnostic_summary": {
        "per_error": 0,
        "converged": true,
        "rep_path": "<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210043_react_mc.rep",
        "apw_path": "<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210044_react_mc.apw",
        "messages": [],
        "value": 0,
        "path": "Data\\Results Summary\\Run-Status\\Output\\PER_ERROR",
        "rep_problem_status": {
          "converged": true,
          "hints": [
            "ID        ID               ERR/TOL      RELATIVE     ERROR       STAT  BLOCK",
            "****   MAXIMUM FINAL RELATIVE ERRORS   ****"
          ]
        },
        "repair_required": false
      }
    }
  },
  {
    "event": "plan_result",
    "actions_requested": 6,
    "actions_executed": 6,
    "stopped_on_error": false,
    "first_error_index": null,
    "pending_action_count": 0,
    "action_outcomes": [
      {
        "event": "tool_result",
        "operation": "read_stream_mole_fractions",
        "parameters": {
          "stream_name": "PRODUCT"
        },
        "facade": true,
        "translated_operations": [
          {
            "operation": "read_stream_mole_fractions",
            "success": true,
            "error": null
          }
        ],
        "response_status": "success",
        "result": {
          "success": true
        }
      },
      {
        "truncated": true,
        "chars": 840,
        "preview": "{\"event\": \"tool_result\", \"operation\": \"read_stream_outputs\", \"parameters\": {\"stream_name\": \"PRODUCT\", \"components\": [\"H2\", \"N2\", \"CH4\", \"BENZENE\", \"CYCLOHEX\"], \"basis\": \"mole_fraction\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \n...[truncated]"
      },
      {
        "event": "tool_result",
        "operation": "read_global_property_method",
        "parameters": {},
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true
        }
      },
      {
        "event": "tool_result",
        "operation": "list_block_ports",
        "parameters": {
          "block_name": "FEEDPUMP"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "message": "Found 5 port(s) for block FEEDPUMP",
          "block_name": "FEEDPUMP",
          "ports": {
            "F(IN)": [
              "BZIN"
            ],
            "WS(IN)": [],
            "P(OUT)": [
              "BZIN2"
            ],
            "WD(OUT)": [],
            "WS(OUT)": []
          }
        }
      },
      {
        "event": "tool_result",
        "operation": "list_block_ports",
        "parameters": {
          "block_name": "PUMP"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "message": "Found 5 port(s) for block PUMP",
          "block_name": "PUMP",
          "ports": {
            "F(IN)": [
              "CHRCY"
            ],
            "WS(IN)": [],
            "P(OUT)": [
              "CHRCY2"
            ],
            "WD(OUT)": [],
            "WS(OUT)": []
          }
        }
      },
      {
        "event": "tool_result",
        "operation": "list_block_ports",
        "parameters": {
          "block_name": "COLUMN"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "message": "Found 11 port(s) for block COLUMN",
          "block_name": "COLUMN",
          "ports": {
            "F(IN)": [
              "COLFD"
            ],
            "HS(IN)": [],
            "VD(OUT)": [
              "LTENDS"
            ],
            "LD(OUT)": [],
            "B(OUT)": [
              "PRODUCT"
            ],
            "SP(OUT)": [],
            "WD(OUT)": [],
            "CHS(OUT)": [],
            "RHS(OUT)": [],
            "PS(OUT)": [],
            "HS(OUT)": []
          }
        }
      }
    ]
  },
  {
    "event": "plan_result",
    "actions_requested": 6,
    "actions_executed": 6,
    "stopped_on_error": false,
    "first_error_index": null,
    "pending_action_count": 0,
    "action_outcomes": [
      {
        "event": "tool_result",
        "operation": "read_stream_output",
        "parameters": {
          "stream_name": "PRODUCT",
          "variable": "mole_fraction",
          "component_name": "CYCLOHEX"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "stream_name": "PRODUCT",
          "value": 0.999122737,
          "unit": null,
          "path": "\\Data\\Streams\\PRODUCT\\Output\\MOLEFRAC\\MIXED\\CYCLOHEX"
        }
      },
      {
        "event": "tool_result",
        "operation": "read_stream_output",
        "parameters": {
          "stream_name": "PRODUCT",
          "variable": "total_flow"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "stream_name": "PRODUCT",
          "value": 2.45448313,
          "unit": null,
          "path": "\\Data\\Streams\\PRODUCT\\Output\\TOT_FLOW"
        }
      },
      {
        "truncated": true,
        "chars": 840,
        "preview": "{\"event\": \"tool_result\", \"operation\": \"read_stream_outputs\", \"parameters\": {\"stream_name\": \"PRODUCT\", \"components\": [\"H2\", \"N2\", \"CH4\", \"BENZENE\", \"CYCLOHEX\"], \"basis\": \"mole_fraction\"}, \"facade\": true, \"translated_operations\": [{\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \"error\": null}, {\"operation\": \"read_stream_output\", \"success\": true, \n...[truncated]"
      },
      {
        "event": "tool_result",
        "operation": "read_global_property_method",
        "parameters": {},
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true
        }
      },
      {
        "event": "tool_result",
        "operation": "node_info",
        "parameters": {
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "path": "Data\\Blocks\\FEEDPUMP\\Input\\OPT_SPEC"
        }
      },
      {
        "event": "tool_result",
        "operation": "node_info",
        "parameters": {
          "path": "Data\\Blocks\\PUMP\\Input\\OPT_SPEC"
        },
        "facade": true,
        "translated_operations": [],
        "response_status": "success",
        "result": {
          "success": true,
          "path": "Data\\Blocks\\PUMP\\Input\\OPT_SPEC"
        }
      }
    ]
  },
  {
    "truncated": true,
    "chars": 5602,
    "preview": "{\"event\": \"plan_result\", \"actions_requested\": 17, \"actions_executed\": 17, \"stopped_on_error\": false, \"first_error_index\": null, \"pending_action_count\": 0, \"action_outcomes\": [{\"event\": \"tool_result\", \"operation\": \"node_props\", \"parameters\": {\"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\OPT_SPEC\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\OPT_SPEC\"}}, {\"event\": \"tool_result\", \"operation\": \"node_props\", \"parameters\": {\"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\OPT_CTYPE\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\OPT_CTYPE\"}}, {\"event\": \"tool_result\", \"operation\": \"node_props\", \"parameters\": {\"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\OPT_CFORMAT\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\OPT_CFORMAT\"}}, {\"event\": \"tool_result\", \"operation\": \"node_props\", \"parameters\": {\"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\DEP_VAR\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\DEP_VAR\"}}, {\"event\": \"tool_result\", \"operation\": \"node_props\", \"parameters\": {\"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\INDEP_VAR\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\INDEP_VAR\"}}, {\"event\": \"tool_result\", \"operation\": \"node_props\", \"parameters\": {\"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\EFF\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\EFF\"}}, {\"event\": \"tool_result\", \"operation\": \"node_props\", \"parameters\": {\"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\DEFF\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"path\": \"Data\\\\Blocks\\\\FEEDPUMP\\\\Input\\\\DEFF\"}}, {\"event\": \"tool_result\", \"operation\": \"node_props\", \"parameters\": {\"path\": \"Data\\\\Blocks\\\\PUMP\\\\Input\\\\OPT_SPEC\"}, \"facade\": true, \"translated_operations\": [], \"response_status\": \"success\", \"result\": {\"success\": true, \"path\": \"Data\\\\Blocks\\\\PUMP\\\\Input\\\\OPT_SPEC\"}}, {\"event\": \"tool_result\", \"operation\": \"node_props\", \"parameters\n...[truncated]"
  }
]
```

</details>

<details><summary>Raw model output</summary>

```text
{"thought":"Converged Aspen evidence and PRODUCT CYCLOHEX mole fraction readback are available; finalize with documented evidence and limitations.","action":"finalize","final_summary":{"case_id":"chinese_5_1_radfrac","ok":true,"evidence":{"aspen_run":{"per_error":0,"converged":true,"rep_path":"<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210043_react_mc.rep","apw_path":"<REPOSITORY_ROOT>\\data\\file\\chinese_5_1_radfrac_20261018_210044_react_mc.apw","rep_problem_status":{"converged":true}},"product_readback":{"stream":"PRODUCT","component":"CYCLOHEX","variable":"mole_fraction","value":0.999122737,"path":"\\Data\\Streams\\PRODUCT\\Output\\MOLEFRAC\\MIXED\\CYCLOHEX"},"product_identity":{"column_ports":{"F(IN)":["COLFD"],"VD(OUT)":["LTENDS"],"B(OUT)":["PRODUCT"]},"meaning":"PRODUCT is the COLUMN bottoms outlet; LTENDS is vapor distillate/light ends."},"topology_evidence":{"FEEDPUMP_ports":{"F(IN)":["BZIN"],"P(OUT)":["BZIN2"]},"PUMP_ports":{"F(IN)":["CHRCY"],"P(OUT)":["CHRCY2"]}},"pump_spec_readbacks":{"FEEDPUMP":{"OPT_SPEC":"USE-CURVE","OPT_CTYPE":"SINGLE-OPER","OPT_CFORMAT":"TABLE","DEP_VAR":"HEAD","INDEP_VAR":"VOL-FLOW","EFF":0.6,"DEFF":0.9,"curve_assignment_note":"Pump curve is assigned to FEEDPUMP branch BZIN -> FEEDPUMP -> BZIN2; flow unit m3/hr and head interpreted as meters for Aspen curve entry."},"PUMP":{"OPT_SPEC":"PRES","PRES":2.6,"branch":"CHRCY -> PUMP -> CHRCY2"}}},"results":{"product_cyclohexane_mole_fraction":0.999122737,"product_total_flow_readback":2.45448313,"product_component":"CYCLOHEX/cyclohexane","basis":"raw full material-stream mole fraction in PRODUCT including H2, N2, CH4, BENZENE, and CYCLOHEX where present","property_method_requested":"RK-SOAVE"},"self_validation":{"primary_target_satisfied":true,"result_from_solved_aspen_flowsheet":true,"per_error_zero":true,"product_stream_is_column_product":true,"pressure_unit_and_pump_curve_caveat":"FEEDPUMP mode/curve-axis/efficiency readbacks and branch readbacks were obtained; detailed curve table cell values were probed during setup but only summarized here from available evidence.","not_claimed":"No manual hand-calculation result is used; no unobserved tolerance-level match for every individual stream pressure is claimed."}}}
```

</details>
