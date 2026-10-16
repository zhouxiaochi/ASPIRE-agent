---
name: mixer
description: Build and audit Aspen MIXER topology and specifications.
---
# MIXER

Use this guidance only for an Aspen MIXER.

## Required sequence

1. Create the block with the canonical `create_mixer` operation with `block_name`.
2. Create the required material streams.
3. Call `list_block_ports(block_name=...)` and use the live port names returned by Aspen.
4. Connect feeds through the shared `F(IN)` collection and products through the shared `P(OUT)` collection with `connect_stream`.
5. Verify every intended connection from a fresh live port readback.
6. Configure specifications only after topology is complete.

## Specifications

- Set `ENERGY_BAL` to exactly `YES` or `NO` with `set_energy_bal`.
- Set `PRES` to a numeric pressure with an explicit unit using `set_pres`.
- Apply energy balance first, then pressure.
- Never encode a pressure mode token as the pressure value.
- A unit-bearing pressure write must remain a value-plus-unit operation.

## Run gate

Check flowsheet completion and Next completion status through `ui_check_next_completion_status` after topology and specifications are landed. Run only when both checks provide explicit affirmative completion. Save a checkpoint before the engine run and retain live topology evidence.
