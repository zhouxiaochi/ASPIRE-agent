# Architecture

Both public harnesses start with `PlannerAgent`, which creates serializable task and stage plans, selects only the packaged common-component, MIXER, and HEATER skills, and rejects obvious requests outside this domain. Thesis plans retain manifest stage order and dependencies.

Generation receives the plan plus the packaged text of exactly the selected allowlisted skills and, after failure, one bounded `RepairFocus`. `AuditAgent` parses generated Python before execution and applies deterministic process and evidence gates after execution. A nonzero process always fails. A successful process with no Aspen receipt is classified as process-only. A canonical runtime receipt must have `ok: true`, a complete preflight with explicit flowsheet and Next completion, a successful run whose source is `engine_run` or a proven `next_gate_short_circuit`, and successful REP and APW export responses. Explicitly normalized trusted-run receipts remain supported.

`ChemicalReasoningAgent` runs only when an audit issue is physical or configuration-related. Its structured diagnoses cover registry components, feed state, live topology, MIXER pressure and energy, HEATER mode and matching values, material versus heat stream roles, and target readback. Syntax and infrastructure failures bypass this role.

`RepairDirector` selects one focus for each bounded rerun. Plans, per-attempt audits, optional chemistry diagnoses, repair focuses, and fresh stage runtime receipts are persisted. Canonical Aspen `run-summary.json` evidence is never replaced by orchestration state; agent outcomes use `agent-summary.json`. Thesis execution stops after a failed prerequisite and protects accepted stage entry files from later generation.

The typed client targets canonical session operations. A runnable lifecycle lands and inspects registry components, configures material feeds, creates and connects MIXER or HEATER blocks through live ports, checks completion and Next status, checkpoints, runs, reads targets, and exports evidence. Harness execution supplies each stage a deterministic `--task-key`, a safe server-relative evidence prefix, and a stage-local checkpoint filename.
