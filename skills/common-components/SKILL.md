---
name: common-components
description: Resolve and verify the ten public ASPIRE Agent compounds.
---
# Common components

Use only this registry:

| English name | Aspen ID | CAS | Formula | English aliases |
|---|---|---|---|---|
| water | WATER | 7732-18-5 | H2O | steam |
| methanol | MEOH | 67-56-1 | CH4O | methyl alcohol; METHANOL |
| ethanol | ETHANOL | 64-17-5 | C2H6O | ethyl alcohol |
| methane | METHANE | 74-82-8 | CH4 | natural gas methane |
| carbon dioxide | CO2 | 124-38-9 | CO2 | carbonic gas |
| hydrogen | HYDROGEN | 1333-74-0 | H2 | molecular hydrogen |
| nitrogen | NITROGEN | 7727-37-9 | N2 | molecular nitrogen |
| ammonia | AMMONIA | 7664-41-7 | NH3 | azane |
| n-hexane | N-HEXANE | 110-54-3 | C6H14 | hexane; normal hexane |
| acetic acid | ACETIC-ACID | 64-19-7 | C2H4O2 | ethanoic acid |

## Stable landing route

1. Resolve each user-supplied English name, Aspen ID, CAS, formula, or English alias through `CompoundRegistry`.
2. Send explicit `{component_id, cas}` records to `add_components_by_cas`.
3. Call `inspect_component_table(component_ids=[...])` after addition.
4. Require an empty `missing_requested_component_ids` list or equivalent visible-row evidence for every requested Aspen ID.
5. Stop if the visible table contains a missing ID, suspicious duplicate, or placeholder-looking row.

Do not derive components from task context. Do not invent aliases, use placeholder IDs, or fall back to an unregistered compound.

## Feed configuration

After verified landing, configure every material feed before completion. Use configure_material_stream_tp with TP, explicit temperature and pressure units, MOLE-FLOW or MASS-FLOW, and nonnegative component flows with an explicit flow unit. Resolve each flow key through this registry; do not use fraction fallbacks.
