"""Slim own-agent Aspen script for chinese_5_1.

Builds the cyclohexane production flowsheet from the task figure using short
Aspen-safe IDs, with a name mapping back to the visible Chinese exercise labels.
The slim runtime owns session setup, CLI, final run/export, REP readback, and
summary finalization.
"""

from __future__ import annotations

import script_agent_exp.safe_aspen_calls as safe
from script_agent_exp.slim_task_runtime import (
    SlimTaskOutcome,
    SlimTaskSpec,
    block_rep_targets,
    run_slim_task,
    stream_rep_targets,
)

SCRIPT_STEM = "chinese_5_1_own_agent"
CASE_ID = "chinese_5_1"

# Aspen-safe short IDs. The task/figure labels are preserved in NAME_MAPPING.
BLOCKS = {
    "FEEDPUMP": "FP",
    "FEED-MIX": "FM",
    "REACT": "R1",
    "HP-SEP": "FL",
    "VFLOW": "VF",
    "VALVE": "VA",
    "COMP": "CP",
    "LFLOW": "LF",
    "PUMP": "RP",
    "PIPE": "PI",
    "COLUMN": "CO",
}

STREAMS = {
    "BZIN": "B1",
    "BZIN2": "B2",
    "H2IN": "H1",
    "H2RCY2": "H4",
    "RXIN": "R2",
    "RXOUT": "R3",
    "VAP": "V1",
    "H2RCY": "H3",
    "PURGE": "G1",
    "PURGE2": "G2",
    "LIQ": "L1",
    "COLFD": "C1",
    "CHRCY": "C2",
    "CHRCY2": "C3",
    "CHRCY3": "C4",
    "LTENDS": "T1",
    "PRODUCT": "P5",
}

COMPONENTS = {
    "hydrogen": "H2",
    "nitrogen": "N2",
    "methane": "METHANE",
    "benzene": "BENZENE",
    "cyclohexane": "CYCLOHEX",
}

REQUIRED_STREAMS = tuple(STREAMS.values())
REQUIRED_BLOCKS = (
    "FP",
    "FM",
    "R1",
    "FL",
    "VF",
    "VA",
    "CP",
    "LF",
    "RP",
    "PI",
    "CO",
)

MATERIAL_EDGES = [
    {"stream": "B1", "source": None, "destination": "FP"},
    {"stream": "B2", "source": "FP", "destination": "FM"},
    {"stream": "H1", "source": None, "destination": "FM"},
    {"stream": "H4", "source": "CP", "destination": "FM"},
    {"stream": "C4", "source": "PI", "destination": "FM"},
    {"stream": "R2", "source": "FM", "destination": "R1"},
    {"stream": "R3", "source": "R1", "destination": "FL"},
    {"stream": "V1", "source": "FL", "destination": "VF"},
    {"stream": "H3", "source": "VF", "destination": "CP"},
    {"stream": "G1", "source": "VF", "destination": "VA"},
    {"stream": "G2", "source": "VA", "destination": None},
    {"stream": "L1", "source": "FL", "destination": "LF"},
    {"stream": "C1", "source": "LF", "destination": "CO"},
    {"stream": "C2", "source": "LF", "destination": "RP"},
    {"stream": "C3", "source": "RP", "destination": "PI"},
    {"stream": "C4", "source": "PI", "destination": "FM"},
    {"stream": "T1", "source": "CO", "destination": None},
    {"stream": "P5", "source": "CO", "destination": None},
]

# Pump-curve table belongs to FEEDPUMP/FP only. The unlabelled head values are
# interpreted as metres of liquid head, matching the Chinese table heading head.
FEEDPUMP_CURVE_POINTS = [
    {"flow": 20.0, "head": 40.0},
    {"flow": 10.0, "head": 250.0},
    {"flow": 5.0, "head": 300.0},
    {"flow": 3.0, "head": 400.0},
]

NAME_MAPPING = {
    "blocks": BLOCKS,
    "streams": STREAMS,
    "components": {
        "H2": "H2",
        "N2": "N2",
        "CH4": "METHANE",
        "C6H6": "BENZENE",
        "C6H12": "CYCLOHEX",
    },
}

REP_READBACK_TARGETS = (
    *stream_rep_targets(
        ("P5", "T1", "C1", "V1", "L1", "G2", "H4", "C4"),
        components=("H2", "N2", "METHANE", "BENZENE", "CYCLOHEX"),
        quantities=("temperature", "pressure", "vapor_fraction", "total_flow", "component_flow"),
    ),
    *block_rep_targets(
        {
            "CO": ("reflux_ratio", "distillate_flow"),
            "FM": ("block_heat_duty",),
            "R1": ("block_heat_duty",),
        }
    ),
    {
        "request_id": "product_cyclohexane_mole_fraction",
        "kind": "stream",
        "object_name": "P5",
        "quantity": "mole_fraction",
        "component": "CYCLOHEX",
        "notes": "Primary task result: raw full-material-stream mole fraction of cyclohexane in PRODUCT/P5.",
    },
    {
        "request_id": "reactor_benzene_conversion",
        "kind": "derived",
        "object_name": "R1",
        "quantity": "conversion",
        "reactant_component": "BENZENE",
        "inlet_stream": "R2",
        "outlet_stream": "R3",
        "notes": "Benzene conversion across REACT/R1 from final Aspen REP stream tables.",
    },
)

TASK_SPEC = SlimTaskSpec(
    script_stem=SCRIPT_STEM,
    required_streams=REQUIRED_STREAMS,
    required_blocks=REQUIRED_BLOCKS,
    case_id=CASE_ID,
    name_mapping=NAME_MAPPING,
    rep_readback_targets=REP_READBACK_TARGETS,
    phase="analysis",
    inset="SI",
    summary_seed={
        "task": "Cyclohexane production by benzene hydrogenation; report PRODUCT cyclohexane mole fraction.",
        "property_method": "RK-SOAVE represented by Aspen SRK/RK-Soave option set with SRK free-water advisory repaired.",
        "pump_curve_assignment": {
            "curve_owner": "FEEDPUMP/FP",
            "not_owner": "PUMP/RP",
            "flow_unit": "m3/hr",
            "head_unit_assumption": "m",
            "points": FEEDPUMP_CURVE_POINTS,
        },
    },
)


def _validate_static_plans() -> None:
    """Validate topology and required native-block declarations before Aspen mutation."""
    safe.validate_material_edge_plan(
        MATERIAL_EDGES,
        block_names=list(REQUIRED_BLOCKS),
        stream_names=list(REQUIRED_STREAMS),
    )
    safe.validate_required_native_blocks_plan(
        {
            "HEATER": ["FM"],
            "RSTOIC": ["R1"],
            "FLASH2": ["FL"],
            "FSPLIT": ["VF", "LF"],
            "RADFRAC": ["CO"],
            "PUMP": ["FP", "RP"],
            "COMPR": ["CP"],
            "PIPE": ["PI"],
            "VALVE": ["VA"],
        },
        created_blocks_by_family={
            "HEATER": ["FM"],
            "RSTOIC": ["R1"],
            "FLASH2": ["FL"],
            "FSPLIT": ["VF", "LF"],
            "RADFRAC": ["CO"],
            "PUMP": ["FP", "RP"],
            "COMPR": ["CP"],
            "PIPE": ["PI"],
            "VALVE": ["VA"],
        },
        finalization_required_blocks=list(REQUIRED_BLOCKS),
    )


def _setup_components_and_property(runtime) -> None:
    """Land the real components and RK-SOAVE/SRK thermodynamic method."""
    client = runtime.client
    runtime.stage(
        "add_components_by_cas",
        lambda: client.invoke(
            "add_components_by_cas",
            components=[
                {"component_id": "H2", "cas": "1333-74-0"},
                {"component_id": "N2", "cas": "7727-37-9"},
                {"component_id": "METHANE", "cas": "74-82-8"},
                {"component_id": "BENZENE", "cas": "71-43-2"},
                {"component_id": "CYCLOHEX", "cas": "110-82-7"},
            ],
        ),
        required=True,
    )
    runtime.stage(
        "list_component_ids_after_cas",
        lambda: client.invoke("list_component_ids"),
        required=False,
    )
    runtime.stage(
        "ensure_rk_soave_srk_property_method",
        lambda: client.invoke("ensure_property_method", method="SRK"),
        required=True,
    )
    runtime.stage(
        "configure_srk_free_water_steamnbs",
        lambda: client.invoke("configure_srk_free_water_steamnbs"),
        required=True,
    )


def _create_streams_and_blocks(runtime) -> None:
    """Create every figure-visible material stream and unit-operation block."""
    client = runtime.client
    for stream_name in REQUIRED_STREAMS:
        runtime.stage(
            f"create_stream_{stream_name}",
            lambda stream_name=stream_name: client.invoke(
                "create_material_stream",
                stream_name=stream_name,
            ),
            required=True,
        )

    runtime.stage("create_feedpump_FP", lambda: client.invoke("create_pump", block_name="FP"), required=True)
    runtime.stage("create_feedmix_heater_FM", lambda: client.invoke("create_heater", block_name="FM"), required=True)
    runtime.stage("create_reactor_R1", lambda: client.invoke("create_rstoic", block_name="R1"), required=True)
    runtime.stage("create_flash_FL", lambda: client.invoke("create_flash2", block_name="FL"), required=True)
    runtime.stage("create_vapor_split_VF", lambda: client.invoke("create_fsplit", block_name="VF"), required=True)
    runtime.stage("create_valve_VA", lambda: client.invoke("create_valve", block_name="VA"), required=True)
    runtime.stage("create_compressor_CP", lambda: client.invoke("create_compr", block_name="CP"), required=True)
    runtime.stage("create_liquid_split_LF", lambda: client.invoke("create_fsplit", block_name="LF"), required=True)
    runtime.stage("create_recycle_pump_RP", lambda: client.invoke("create_pump", block_name="RP"), required=True)
    runtime.stage("create_pipe_PI", lambda: client.invoke("create_pipe", block_name="PI"), required=True)
    runtime.stage("create_radfrac_CO", lambda: client.invoke("create_radfrac", block_name="CO"), required=True)


def _connect_topology(runtime) -> None:
    """Connect the complete figure topology before writing block specifications."""
    client = runtime.client

    for block_name in REQUIRED_BLOCKS:
        runtime.stage(
            f"ports_before_{block_name}",
            lambda block_name=block_name: client.invoke("list_block_ports", block_name=block_name),
            required=False,
        )

    runtime.stage(
        "connect_FEEDPUMP",
        lambda: client.invoke(
            "connect_material_inlet_outlet",
            block_name="FP",
            inlet_stream="B1",
            outlet_stream="B2",
        ),
        required=True,
    )
    runtime.stage(
        "connect_FEED_MIX_shared_feeds",
        lambda: client.invoke(
            "connect_material_ports_by_order",
            block_name="FM",
            inlet_streams=["B2", "H1", "H4", "C4"],
            outlet_streams=["R2"],
        ),
        required=True,
    )
    runtime.stage(
        "connect_REACT",
        lambda: client.invoke(
            "connect_material_inlet_outlet",
            block_name="R1",
            inlet_stream="R2",
            outlet_stream="R3",
        ),
        required=True,
    )
    runtime.stage(
        "connect_HP_SEP_flash_phase_ports",
        lambda: client.invoke(
            "connect_flash2_vapor_liquid_ports",
            block_name="FL",
            feed_stream="R3",
            vapor_stream="V1",
            liquid_stream="L1",
        ),
        required=True,
    )
    runtime.stage(
        "connect_VFLOW_split",
        lambda: client.invoke(
            "configure_fsplit_shared_outlets",
            block_name="VF",
            inlet_stream="V1",
            outlet_streams=["H3", "G1"],
            split_fractions={"H3": 0.92},
        ),
        required=True,
    )
    runtime.stage(
        "connect_COMP",
        lambda: client.invoke(
            "connect_material_inlet_outlet",
            block_name="CP",
            inlet_stream="H3",
            outlet_stream="H4",
        ),
        required=True,
    )
    runtime.stage(
        "connect_VALVE",
        lambda: client.invoke(
            "connect_material_inlet_outlet",
            block_name="VA",
            inlet_stream="G1",
            outlet_stream="G2",
        ),
        required=True,
    )
    runtime.stage(
        "connect_LFLOW_split",
        lambda: client.invoke(
            "configure_fsplit_shared_outlets",
            block_name="LF",
            inlet_stream="L1",
            outlet_streams=["C1", "C2"],
            split_fractions={"C2": 0.30},
        ),
        required=True,
    )
    runtime.stage(
        "connect_recycle_PUMP",
        lambda: client.invoke(
            "connect_material_inlet_outlet",
            block_name="RP",
            inlet_stream="C2",
            outlet_stream="C3",
        ),
        required=True,
    )
    runtime.stage(
        "connect_PIPE",
        lambda: client.invoke(
            "connect_material_inlet_outlet",
            block_name="PI",
            inlet_stream="C3",
            outlet_stream="C4",
        ),
        required=True,
    )
    runtime.stage(
        "connect_COLUMN_feed",
        lambda: client.invoke(
            "connect_stream",
            block_name="CO",
            stream_name="C1",
            port_name="F(IN)",
        ),
        required=True,
    )
    runtime.stage(
        "connect_COLUMN_vapor_light_ends",
        lambda: client.invoke(
            "connect_stream",
            block_name="CO",
            stream_name="T1",
            port_name="VD(OUT)",
        ),
        required=True,
    )
    runtime.stage(
        "connect_COLUMN_bottom_product",
        lambda: client.invoke(
            "connect_stream",
            block_name="CO",
            stream_name="P5",
            port_name="B(OUT)",
        ),
        required=True,
    )

    for block_name in REQUIRED_BLOCKS:
        runtime.stage(
            f"ports_after_{block_name}",
            lambda block_name=block_name: client.invoke("list_block_ports", block_name=block_name),
            required=False,
        )


def _set_feed_streams(runtime) -> None:
    """Set the two fresh feeds exactly from the problem statement."""
    client = runtime.client
    runtime.stage("H1_mixed_spec", lambda: client.invoke("set_mixed_spec_mixed", stream_name="H1", value="TP"), required=True)
    runtime.stage("H1_basis", lambda: client.invoke("set_basis_mixed", stream_name="H1", value="MOLE-FLOW"), required=True)
    runtime.stage("H1_temperature", lambda: client.invoke("set_temp_mixed", stream_name="H1", value=50.0, unit="C"), required=True)
    runtime.stage("H1_pressure", lambda: client.invoke("set_pres_mixed", stream_name="H1", value=2.5, unit="MPa"), required=True)
    runtime.stage("H1_H2_flow", lambda: client.invoke("set_flow_mixed", stream_name="H1", component_name="H2", value=321.75, unit="kmol/hr"), required=True)
    runtime.stage("H1_N2_flow", lambda: client.invoke("set_flow_mixed", stream_name="H1", component_name="N2", value=1.65, unit="kmol/hr"), required=True)
    runtime.stage("H1_CH4_flow", lambda: client.invoke("set_flow_mixed", stream_name="H1", component_name="METHANE", value=6.6, unit="kmol/hr"), required=True)

    runtime.stage("B1_mixed_spec", lambda: client.invoke("set_mixed_spec_mixed", stream_name="B1", value="TP"), required=True)
    runtime.stage("B1_basis", lambda: client.invoke("set_basis_mixed", stream_name="B1", value="MOLE-FLOW"), required=True)
    runtime.stage("B1_temperature", lambda: client.invoke("set_temp_mixed", stream_name="B1", value=40.0, unit="C"), required=True)
    runtime.stage("B1_pressure", lambda: client.invoke("set_pres_mixed", stream_name="B1", value=0.1, unit="MPa"), required=True)
    runtime.stage("B1_benzene_flow", lambda: client.invoke("set_flow_mixed", stream_name="B1", component_name="BENZENE", value=100.0, unit="kmol/hr"), required=True)


def _set_pressure_changing_units(runtime) -> None:
    """Configure FEEDPUMP curve, recycle pump, compressor, pipe, and valve."""
    client = runtime.client

    runtime.stage("FP_outlet_curve_mode", lambda: client.invoke("set_pump_outlet_spec", block_name="FP", value="USE-CURVE"), required=True)
    runtime.stage("FP_curve_type", lambda: client.invoke("set_opt_ctype", block_name="FP", value="SINGLE-OPER"), required=True)
    runtime.stage("FP_curve_format", lambda: client.invoke("set_opt_cformat", block_name="FP", value="TABLE"), required=True)
    runtime.stage("FP_curve_dep_var", lambda: client.invoke("set_dep_var", block_name="FP", value="HEAD"), required=True)
    runtime.stage("FP_curve_indep_var", lambda: client.invoke("set_indep_var", block_name="FP", value="VOL-FLOW"), required=True)
    runtime.stage(
        "FP_curve_table",
        lambda: client.invoke(
            "set_pump_curve_table",
            block_name="FP",
            curve_idx=1,
            flow_unit="m3/hr",
            head_unit="m",
            curve_points=FEEDPUMP_CURVE_POINTS,
        ),
        required=True,
    )
    runtime.stage("FP_pump_efficiency", lambda: client.invoke("set_eff", block_name="FP", value=0.6), required=True)
    runtime.stage("FP_driver_efficiency", lambda: client.invoke("set_deff", block_name="FP", value=0.9), required=True)

    runtime.stage("RP_outlet_pressure_mode", lambda: client.invoke("set_pump_outlet_spec", block_name="RP", value="PRES"), required=True)
    runtime.stage("RP_outlet_pressure", lambda: client.invoke("set_pump_outlet_pressure", block_name="RP", value=2.6, unit="MPa"), required=True)

    runtime.stage(
        "CP_isentropic_pressure_rise",
        lambda: client.invoke(
            "configure_compr_pressure_rise",
            block_name="CP",
            delta_pressure=0.4,
            pressure_unit="MPa",
            compressor_type="ISENTROPIC",
        ),
        required=True,
    )
    runtime.stage(
        "PI_schedule_sizing",
        lambda: client.invoke(
            "configure_pipe_schedule_sizing",
            block_name="PI",
            material="CARBON-STEEL",
            schedule=40,
            nominal_diam="1-IN",
            length=25.0,
            length_unit="meter",
        ),
        required=True,
    )
    runtime.stage(
        "VA_outlet_pressure_and_vendor",
        lambda: client.invoke(
            "configure_valve_outlet_pressure_design",
            block_name="VA",
            outlet_pressure=2.0,
            pressure_unit="MPa",
            vendor_preset_id="neles_globe_v810_equal_pct_1p5in",
        ),
        required=True,
    )


def _set_reactor_separator_column(runtime) -> None:
    """Configure heater, reactor chemistry, flash separator, splitters, and RadFrac."""
    client = runtime.client

    runtime.stage("FM_flash_spec", lambda: client.invoke("set_heater_flash_spec", block_name="FM", value="TP"), required=True)
    runtime.stage("FM_temperature", lambda: client.invoke("set_heater_temperature", block_name="FM", value=150.0, unit="C"), required=True)
    runtime.stage("FM_pressure", lambda: client.invoke("set_heater_pressure", block_name="FM", value=2.3, unit="MPa"), required=True)

    runtime.stage(
        "R1_stoichiometry",
        lambda: client.invoke(
            "configure_rstoic_stoichiometry",
            block_name="R1",
            reaction_number=1,
            reactants={"BENZENE": 1.0, "H2": 3.0},
            products={"CYCLOHEX": 1.0},
        ),
        required=True,
    )
    runtime.stage(
        "R1_fractional_conversion",
        lambda: client.invoke(
            "configure_rstoic_fractional_conversions",
            block_name="R1",
            conversions=[{"reaction_number": 1, "component_id": "BENZENE", "conversion": 0.998}],
        ),
        required=True,
    )
    runtime.stage(
        "R1_calculated_heat_reference",
        lambda: client.invoke(
            "configure_rstoic_calculated_heat_reference",
            block_name="R1",
            rows=[{"reaction_number": 1, "reference_component_id": "BENZENE", "reference_phase": "V"}],
            reference_temperature=298.15,
            reference_temperature_unit="K",
            reference_pressure=1.0,
            reference_pressure_unit="atm",
        ),
        required=True,
    )
    runtime.stage(
        "R1_flash_conditions",
        lambda: client.invoke(
            "configure_rstoic_flash",
            block_name="R1",
            spec_opt="TP",
            temperature=200.0,
            temperature_unit="C",
            pressure=-0.1,
            pressure_unit="MPa",
        ),
        required=True,
    )

    runtime.stage("FL_flash_spec", lambda: client.invoke("set_flash2_flash_spec", block_name="FL", value="TP"), required=True)
    runtime.stage("FL_temperature", lambda: client.invoke("set_flash2_temperature", block_name="FL", value=50.0, unit="C"), required=True)
    runtime.stage("FL_pressure_drop", lambda: client.invoke("set_flash2_pressure", block_name="FL", value=-0.05, unit="MPa"), required=True)

    runtime.stage("CO_condenser_partial_vapor", lambda: client.invoke("set_radfrac_condenser_type", block_name="CO", value="PARTIAL-V"), required=True)
    runtime.stage("CO_reboiler_kettle", lambda: client.invoke("set_radfrac_reboiler_type", block_name="CO", value="KETTLE"), required=True)
    runtime.stage("CO_stage_count", lambda: client.invoke("set_radfrac_stage_count", block_name="CO", value=12), required=True)
    runtime.stage("CO_feed_stage", lambda: client.invoke("set_radfrac_feed_stage", block_name="CO", stream_name="C1", value=8), required=True)
    runtime.stage("CO_feed_convention", lambda: client.invoke("configure_radfrac_feed_convention", block_name="CO", stream_name="C1", convention="ON-STAGE-LIQ"), required=True)
    runtime.stage("CO_top_pressure", lambda: client.invoke("set_radfrac_top_pressure", block_name="CO", value=1.5, unit="MPa"), required=True)
    runtime.stage("CO_reflux_ratio", lambda: client.invoke("set_radfrac_reflux_ratio", block_name="CO", value=1.2), required=True)
    runtime.stage("CO_distillate_rate", lambda: client.invoke("set_radfrac_distillate_rate", block_name="CO", value=99.0, unit="kmol/hr"), required=True)

    runtime.stage(
        "recycle_convergence_options",
        lambda: client.invoke(
            "configure_recycle_convergence_options",
            tolerance=1e-5,
            tear_method="WEGSTEIN",
            wegstein_max_iterations=100,
        ),
        required=True,
    )


def _record_completion_probes(runtime) -> None:
    """Record concise completion diagnostics without treating probes as fatal."""
    client = runtime.client
    runtime.stage(
        "model_state_probe_before_final_runtime_run",
        lambda: client.invoke(
            "probe_model_state",
            stream_names=list(REQUIRED_STREAMS),
            block_names=list(REQUIRED_BLOCKS),
            include_flowsheet=True,
            include_ui_next=False,
        ),
        required=False,
    )
    for stream_name in ("H1", "B1"):
        runtime.stage(
            f"stream_completion_{stream_name}",
            lambda stream_name=stream_name: client.invoke("check_stream_completion", stream_name=stream_name),
            required=False,
        )
    for block_name in REQUIRED_BLOCKS:
        runtime.stage(
            f"block_completion_{block_name}",
            lambda block_name=block_name: client.invoke("check_block_completion", block_name=block_name),
            required=False,
        )


def configure(runtime) -> SlimTaskOutcome:
    """Slim runtime entry point: configure the model and return semantic handoff fields."""
    client = runtime.client
    _ = client
    _validate_static_plans()
    runtime.attach_artifact(
        "static_topology_contract",
        {
            "material_edges": MATERIAL_EDGES,
            "name_mapping": NAME_MAPPING,
            "required_streams": REQUIRED_STREAMS,
            "required_blocks": REQUIRED_BLOCKS,
        },
    )

    _setup_components_and_property(runtime)
    _create_streams_and_blocks(runtime)
    _connect_topology(runtime)
    _set_feed_streams(runtime)
    _set_pressure_changing_units(runtime)
    _set_reactor_separator_column(runtime)
    _record_completion_probes(runtime)

    return SlimTaskOutcome(
        fields={
            "model_basis": {
                "objective": "Report CYCLOHEX mole fraction in PRODUCT/P5 from final Aspen REP evidence.",
                "property_method": "RK-SOAVE task method implemented as Aspen SRK option set.",
                "feed_basis": {
                    "H1": "H2IN: 330 kmol/hr at 50 C and 2.5 MPa; H2/N2/CH4 = 0.975/0.005/0.02.",
                    "B1": "BZIN: 100 kmol/hr pure benzene at 40 C and 0.1 MPa.",
                },
                "reaction": "BENZENE + 3 H2 -> CYCLOHEX with 0.998 benzene conversion in R1.",
            },
            "pump_curve_unit_interpretation": {
                "assigned_block": "FP",
                "assigned_visible_block": "FEEDPUMP",
                "flow_unit": "m3/hr",
                "head_unit": "m",
                "curve_points": FEEDPUMP_CURVE_POINTS,
                "recycle_pump_RP_curve_assigned": False,
            },
        },
        analysis_handoff={
            "native_analysis_required": False,
            "final_result_source": "Slim runtime final engine/export plus REP readback target product_cyclohexane_mole_fraction.",
            "phase_role_evidence_needed": ["FL outlet V1/L1 phase readbacks", "CO vapor light ends T1 and bottoms product P5 readbacks"],
        },
        analysis_objects={},
        validation_contract={
            "phase": "final_evidence_fact_collection",
            "validator_decision_pending": True,
            "no_script_judgment_policy": True,
            "primary_measurement": {
                "request_id": "product_cyclohexane_mole_fraction",
                "stream": "P5",
                "visible_stream": "PRODUCT",
                "component": "CYCLOHEX",
                "basis": "raw full-material-stream mole fraction from final Aspen REP",
            },
            "topology_evidence_index": {
                "required_blocks": REQUIRED_BLOCKS,
                "required_streams": REQUIRED_STREAMS,
                "material_edges_artifact": "static_topology_contract",
            },
        },
    )


if __name__ == "__main__":
    raise SystemExit(run_slim_task(spec=TASK_SPEC, configure=configure))
