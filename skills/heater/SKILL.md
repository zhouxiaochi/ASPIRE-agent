---
name: heater
description: Build and audit Aspen HEATER topology and safe specifications.
---
# HEATER

Use this guidance only for an Aspen HEATER.

## Required sequence

1. Create the block with the canonical `create_heater` operation with `block_name`.
2. Create the required streams.
3. Call `list_block_ports(block_name=...)` and connect only through live Aspen ports.
4. Read ports again and verify the intended connections before configuration.

A heat stream is optional. Use one only when the intended energy topology requires it and Aspen exposes a compatible live heat port. Do not invent a heat connection.

## Legal specification subset

Set `SPEC_OPT` first with `set_spec_opt`, then set exactly the matching active variables:

- `TP`: `set_temp`, then `set_pres`; provide temperature and pressure values with units.
- `PV`: `set_pres`, then `set_vfrac`; provide pressure with a unit and a numeric vapor fraction.
- `PD`: `set_pres`, then `set_duty`; provide pressure and duty values with units.

Inactive `TEMP`, `PRES`, `VFRAC`, or `DUTY` values may be stale after changing modes. Clear inactive scalar values where the active Aspen surface permits it, and verify the selected mode and active values by readback.

## Run gate

Check flowsheet completion and Next completion status through `ui_check_next_completion_status` after topology and configuration. Run only when both checks explicitly confirm completion. Save a checkpoint before the engine run.
