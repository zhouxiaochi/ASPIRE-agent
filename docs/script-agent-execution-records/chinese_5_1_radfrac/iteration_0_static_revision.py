"""Slim own-agent Aspen script for chinese_5_1.

Builds the cyclohexane production flowsheet from the task statement with short
Aspen-safe object IDs.  The slim runtime owns session setup, CLI, final run,
REP export, REP readback, summary finalization, and process exit status.
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

# Aspen-safe block IDs.  The visible task labels are preserved in NAME_MAPPING.
REQUIRED_BLOCKS = (
    "FP",  # FEEDPUMP, fresh benzene pump with pump curve
    "FM",  # FEED-MIX, modeled as the task-specified Heater node
    "R1",  # REACT, RStoic hydrogenation reactor
    "HS",  # HP-SEP, Flash2 high-pressure separator
    "VF",  # VFLOW, vapor splitter
    "VA",  # VALVE, purge pressure-changing valve
    "CP",  # COMP, vapor recycle compressor
    "LF",  # LFLOW, liquid splitter
    "P1",  # PUMP, liquid recycle pump
    "PI",  # PIPE, liquid recycle pipe
    "CO",  # COLUMN, RadFrac stabilizer
)

# Aspen-safe material stream IDs.  Every task-visible material stream has one
# physical edge row in MATERIAL_EDGES and one intended connection sequence.
REQUIRED_STREAMS = (
    "B1",  # BZIN
    "H1",  # H2IN
    "B2",  # BZIN2
    "H3",  # H2RCY2
    "R2",  # RXIN
    "R3",  # RXOUT
    "V1",  # VAP
    "H4",  # H2RCY
    "P2",  # PURGE
    "P3",  # PURGE2
    "L1",  # LIQ
    "C1",  # COLFD
    "C2",  # CHRCY
    "C3",  # CHRCY2
    "C4",  # CHRCY3
    "L2",  # LTENDS
    "P4",  # PRODUCT
)

NAME_MAPPING = {
    "blocks": {
        "FEEDPUMP": "FP",
        "FEED-MIX": "FM",
        "REACT": "R1",
        "HP-SEP": "HS",
        "VFLOW": "VF",
        "VALVE": "VA",
        "COMP": "CP",
        "LFLOW": "LF",
        "PUMP": "P1",
        "PIPE": "PI",
        "COLUMN": "CO",
    },
    "streams": {
        "BZIN": "B1",
        "H2IN": "H1",
        "BZIN2": "B2",
        "H2RCY2": "H3",
        "RXIN": "R2",
        "RXOUT": "R3",
        "VAP": "V1",
        "H2RCY": "H4",
        "PURGE": "P2",
        "PURGE2": "P3",
        "LIQ": "L1",
        "COLFD": "C1",
        "CHRCY": "C2",
        "CHRCY2": "C3",
        "CHRCY3": "C4",
        "LTENDS": "L2",
        "PRODUCT": "P4",
    },
    "components": {
        "H2": "H2",
        "N2": "N2",
        "CH4": "CH4",
        "C6H6/BENZENE": "BENZENE",
        "C6H12/CYCLOHEXANE": "CYCLO-01",
    },
}

COMPONENTS = (
    {"component_id": "H2", "cas": "1333-74-0"},
    {"component_id": "N2", "cas": "7727-37-9"},
    {"component_id": "CH4", "cas": "74-82-8"},
    {"component_id": "BENZENE", "cas": "71-43-2"},
    {"component_id": "CYCLO-01", "cas": "110-82-7"},
)

MATERIAL_EDGES = (
    {"stream": "B1", "source": None, "destination": "FP"},
    {"stream": "B2", "source": "FP", "destination": "FM"},
    {"stream": "H1", "source": None, "destination": "FM"},
    {"stream": "H3", "source": "CP", "destination": "FM"},
    {"stream": "C4", "source": "PI", "destination": "FM"},
    {"stream": "R2", "source": "FM", "destination": "R1"},
    {"stream": "R3", "source": "R1", "destination": "HS"},
    {"stream": "V1", "source": "HS", "destination": "VF"},
    {"stream": "H4", "source": "VF", "destination": "CP"},
    {"stream": "P2", "source": "VF", "destination": "VA"},
    {"stream": "P3", "source": "VA", "destination": None},
    {"stream": "L1", "source": "HS", "destination": "LF"},
    {"stream": "C1", "source": "LF", "destination": "CO"},
    {"stream": "C2", "source": "LF", "destination": "P1"},
    {"stream": "C3", "source": "P1", "destination": "PI"},
    {"stream": "L2", "source": "CO", "destination": None},
    {"stream": "P4", "source": "CO", "destination": None},
)

REQUIRED_BLOCKS_BY_FAMILY = {
    "HEATER": ["FM"],
    "RSTOIC": ["R1"],
    "FLASH2": ["HS"],
    "FSPLIT": ["VF", "LF"],
    "RADFRAC": ["CO"],
    "PUMP": ["FP", "P1"],
    "COMPR": ["CP"],
    "PIPE": ["PI"],
    "VALVE": ["VA"],
}

PUMP_CURVE_POINTS = (
    {"flow": 20.0, "head": 40.0},
    {"flow": 10.0, "head": 250.0},
    {"flow": 5.0, "head": 300.0},
    {"flow": 3.0, "head": 400.0},
)

REP_READBACK_TARGETS = (
    *stream_rep_targets(
        ("B1", "H1", "R2", "R3", "V1", "L1", "C1", "L2", "P4"),
        components=("H2", "N2", "CH4", "BENZENE", "CYCLO-01"),
        quantities=(
            "temperature",
            "pressure",
            "vapor_fraction",
            "total_flow",
            "component_flow",
        ),
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
        "object_name": "P4",
        "quantity": "mole_fraction",
        "component": "CYCLO-01",
        "basis_hint": "Raw full-material-stream mole fraction in PRODUCT/P4 after the converged Aspen run.",
    },
    {
        "request_id": "reactor_benzene_conversion",
        "kind": "derived",
        "object_name": "R1",
        "quantity": "conversion",
        "reactant_component": "BENZENE",
        "inlet_stream": "R2",
        "outlet_stream": "R3",
        "basis_hint": "Benzene conversion across the RStoic reactor from REP stream component flows.",
    },
    {
        "request_id": "column_product_identity",
        "kind": "block",
        "object_name": "CO",
        "quantity": "product_outlet_identity",
        "notes": "Verify CO/COLUMN has LTENDS mapped to L2 and PRODUCT mapped to P4; P4 is the final product stream.",
    },
    {
        "request_id": "feedpump_curve_mode",
        "kind": "block",
        "object_name": "FP",
        "quantity": "pump_curve_specification",
        "notes": "FEEDPUMP/FP must remain in USE-CURVE mode with the task table entered on FP, not on PUMP/P1.",
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
        "task_objective": "Report the mole fraction of cyclohexane in the final PRODUCT stream.",
        "property_method": "RK-SOAVE represented by Aspen SRK option set with SRK free-water repair.",
        "topology_source": "Task statement and figure-visible cyclohexane production flowsheet.",
        "component_id_basis": NAME_MAPPING["components"],
    },
)


def _validate_static_plans() -> None:
    """Validate static topology/native-block obligations before Aspen mutation."""
    safe.validate_material_edge_plan(
        list(MATERIAL_EDGES),
        block_names=list(REQUIRED_BLOCKS),
        stream_names=list(REQUIRED_STREAMS),
    )
    safe.validate_required_native_blocks_plan(
        REQUIRED_BLOCKS_BY_FAMILY,
        created_blocks_by_family=REQUIRED_BLOCKS_BY_FAMILY,
        finalization_required_blocks=list(REQUIRED_BLOCKS),
    )


def _setup_components_and_property(runtime, client) -> None:
    """Create the chemical slate and enforce the requested RK-SOAVE/SRK basis."""
    runtime.stage(
        "add_components_by_cas",
        lambda: client.invoke(
            "add_components_by_cas",
            components=[dict(item) for item in COMPONENTS],
        ),
        required=True,
    )
    runtime.stage(
        "list_component_ids",
        lambda: client.invoke("list_component_ids"),
        required=False,
    )
    runtime.stage(
        "ensure_property_method_srk",
        lambda: client.invoke("ensure_property_method", method="SRK"),
        required=True,
    )
    runtime.stage(
        "configure_srk_free_water_steamnbs",
        lambda: client.invoke("configure_srk_free_water_steamnbs"),
        required=True,
    )


def _create_streams_and_blocks(runtime, client) -> None:
    """Create every task-visible material stream and native Aspen block."""
    for stream_name in REQUIRED_STREAMS:
        runtime.stage(
            f"create_stream_{stream_name}",
            lambda stream_name=stream_name: client.invoke(
                "create_material_stream",
                stream_name=stream_name,
            ),
            required=True,
        )

    runtime.stage("create_pump_FP", lambda: client.invoke("create_pump", block_name="FP"), required=True)
    runtime.stage("create_heater_FM", lambda: client.invoke("create_heater", block_name="FM"), required=True)
    runtime.stage("create_rstoic_R1", lambda: client.invoke("create_rstoic", block_name="R1"), required=True)
    runtime.stage("create_flash2_HS", lambda: client.invoke("create_flash2", block_name="HS"), required=True)
    runtime.stage("create_fsplit_VF", lambda: client.invoke("create_fsplit", block_name="VF"), required=True)
    runtime.stage("create_valve_VA", lambda: client.invoke("create_valve", block_name="VA"), required=True)
    runtime.stage("create_compr_CP", lambda: client.invoke("create_compr", block_name="CP"), required=True)
    runtime.stage("create_fsplit_LF", lambda: client.invoke("create_fsplit", block_name="LF"), required=True)
    runtime.stage("create_pump_P1", lambda: client.invoke("create_pump", block_name="P1"), required=True)
    runtime.stage("create_pipe_PI", lambda: client.invoke("create_pipe", block_name="PI"), required=True)
    runtime.stage("create_radfrac_CO", lambda: client.invoke("create_radfrac", block_name="CO"), required=True)


def _record_port_diagnostics(runtime, client, suffix: str) -> None:
    """Persist opaque live port probes without inspecting them in generated code."""
    for block_name in REQUIRED_BLOCKS:
        runtime.stage(
            f"ports_{block_name}_{suffix}",
            lambda block_name=block_name: client.invoke(
                "list_block_ports",
                block_name=block_name,
            ),
            required=False,
        )


def _connect_topology(runtime, client) -> None:
    """Connect the complete task-visible material topology before writing specs."""
    _record_port_diagnostics(runtime, client, "before_connect")

    # Fresh benzene feed branch: BZIN -> FEEDPUMP -> BZIN2.
    runtime.stage("connect_B1_to_FP", lambda: client.invoke("connect_stream", block_name="FP", stream_name="B1", port_name="F(IN)"), required=True)
    runtime.stage("connect_B2_from_FP", lambda: client.invoke("connect_stream", block_name="FP", stream_name="B2", port_name="P(OUT)"), required=True)

    # FEED-MIX is the task-specified Heater node and the visible multi-feed merge point.
    runtime.stage("connect_B2_to_FM", lambda: client.invoke("connect_stream", block_name="FM", stream_name="B2", port_name="F(IN)"), required=True)
    runtime.stage("connect_H1_to_FM", lambda: client.invoke("connect_stream", block_name="FM", stream_name="H1", port_name="F(IN)"), required=True)
    runtime.stage("connect_H3_to_FM", lambda: client.invoke("connect_stream", block_name="FM", stream_name="H3", port_name="F(IN)"), required=True)
    runtime.stage("connect_C4_to_FM", lambda: client.invoke("connect_stream", block_name="FM", stream_name="C4", port_name="F(IN)"), required=True)
    runtime.stage("connect_R2_from_FM", lambda: client.invoke("connect_stream", block_name="FM", stream_name="R2", port_name="P(OUT)"), required=True)

    # Reactor and high-pressure separator path.
    runtime.stage("connect_R2_to_R1", lambda: client.invoke("connect_stream", block_name="R1", stream_name="R2", port_name="F(IN)"), required=True)
    runtime.stage("connect_R3_from_R1", lambda: client.invoke("connect_stream", block_name="R1", stream_name="R3", port_name="P(OUT)"), required=True)
    runtime.stage("connect_R3_to_HS", lambda: client.invoke("connect_stream", block_name="HS", stream_name="R3", port_name="F(IN)"), required=True)
    runtime.stage("connect_V1_from_HS", lambda: client.invoke("connect_stream", block_name="HS", stream_name="V1", port_name="V(OUT)"), required=True)
    runtime.stage("connect_L1_from_HS", lambda: client.invoke("connect_stream", block_name="HS", stream_name="L1", port_name="L(OUT)"), required=True)

    # Vapor split, recycle compressor, and purge valve.
    runtime.stage("connect_V1_to_VF", lambda: client.invoke("connect_stream", block_name="VF", stream_name="V1", port_name="F(IN)"), required=True)
    runtime.stage("connect_H4_from_VF", lambda: client.invoke("connect_stream", block_name="VF", stream_name="H4", port_name="P(OUT)"), required=True)
    runtime.stage("connect_P2_from_VF", lambda: client.invoke("connect_stream", block_name="VF", stream_name="P2", port_name="P(OUT)"), required=True)
    runtime.stage("connect_H4_to_CP", lambda: client.invoke("connect_stream", block_name="CP", stream_name="H4", port_name="F(IN)"), required=True)
    runtime.stage("connect_H3_from_CP", lambda: client.invoke("connect_stream", block_name="CP", stream_name="H3", port_name="P(OUT)"), required=True)
    runtime.stage("connect_P2_to_VA", lambda: client.invoke("connect_stream", block_name="VA", stream_name="P2", port_name="F(IN)"), required=True)
    runtime.stage("connect_P3_from_VA", lambda: client.invoke("connect_stream", block_name="VA", stream_name="P3", port_name="P(OUT)"), required=True)

    # Liquid split to column and liquid recycle through pump/pipe.
    runtime.stage("connect_L1_to_LF", lambda: client.invoke("connect_stream", block_name="LF", stream_name="L1", port_name="F(IN)"), required=True)
    runtime.stage("connect_C1_from_LF", lambda: client.invoke("connect_stream", block_name="LF", stream_name="C1", port_name="P(OUT)"), required=True)
    runtime.stage("connect_C2_from_LF", lambda: client.invoke("connect_stream", block_name="LF", stream_name="C2", port_name="P(OUT)"), required=True)
    runtime.stage("connect_C2_to_P1", lambda: client.invoke("connect_stream", block_name="P1", stream_name="C2", port_name="F(IN)"), required=True)
    runtime.stage("connect_C3_from_P1", lambda: client.invoke("connect_stream", block_name="P1", stream_name="C3", port_name="P(OUT)"), required=True)
    runtime.stage("connect_C3_to_PI", lambda: client.invoke("connect_stream", block_name="PI", stream_name="C3", port_name="F(IN)"), required=True)
    runtime.stage("connect_C4_from_PI", lambda: client.invoke("connect_stream", block_name="PI", stream_name="C4", port_name="P(OUT)"), required=True)

    # RadFrac stabilizer: COLFD feed, vapor light ends, and PRODUCT bottoms.
    runtime.stage("connect_C1_to_CO", lambda: client.invoke("connect_stream", block_name="CO", stream_name="C1", port_name="F(IN)"), required=True)
    runtime.stage("connect_L2_from_CO", lambda: client.invoke("connect_stream", block_name="CO", stream_name="L2", port_name="VD(OUT)"), required=True)
    runtime.stage("connect_P4_from_CO", lambda: client.invoke("connect_stream", block_name="CO", stream_name="P4", port_name="B(OUT)"), required=True)

    _record_port_diagnostics(runtime, client, "after_connect")


def _configure_feed_streams(runtime, client) -> None:
    """Enter the two fresh feed states and component molar flows."""
    runtime.stage("B1_mixed_spec", lambda: client.invoke("set_mixed_spec_mixed", stream_name="B1", value="TP"), required=True)
    runtime.stage("B1_basis", lambda: client.invoke("set_basis_mixed", stream_name="B1", value="MOLE-FLOW"), required=True)
    runtime.stage("B1_temperature", lambda: client.invoke("set_temp_mixed", stream_name="B1", value=40.0, unit="C"), required=True)
    runtime.stage("B1_pressure", lambda: client.invoke("set_pres_mixed", stream_name="B1", value=0.1, unit="MPa"), required=True)
    runtime.stage("B1_benzene_flow", lambda: client.invoke("set_flow_mixed", stream_name="B1", component_name="BENZENE", value=100.0, unit="kmol/hr"), required=True)

    runtime.stage("H1_mixed_spec", lambda: client.invoke("set_mixed_spec_mixed", stream_name="H1", value="TP"), required=True)
    runtime.stage("H1_basis", lambda: client.invoke("set_basis_mixed", stream_name="H1", value="MOLE-FLOW"), required=True)
    runtime.stage("H1_temperature", lambda: client.invoke("set_temp_mixed", stream_name="H1", value=50.0, unit="C"), required=True)
    runtime.stage("H1_pressure", lambda: client.invoke("set_pres_mixed", stream_name="H1", value=2.5, unit="MPa"), required=True)
    runtime.stage("H1_h2_flow", lambda: client.invoke("set_flow_mixed", stream_name="H1", component_name="H2", value=321.75, unit="kmol/hr"), required=True)
    runtime.stage("H1_n2_flow", lambda: client.invoke("set_flow_mixed", stream_name="H1", component_name="N2", value=1.65, unit="kmol/hr"), required=True)
    runtime.stage("H1_ch4_flow", lambda: client.invoke("set_flow_mixed", stream_name="H1", component_name="CH4", value=6.6, unit="kmol/hr"), required=True)

    runtime.stage("check_B1_completion", lambda: client.invoke("check_stream_completion", stream_name="B1"), required=False)
    runtime.stage("check_H1_completion", lambda: client.invoke("check_stream_completion", stream_name="H1"), required=False)


def _configure_pressure_changers(runtime, client) -> None:
    """Configure pumps, compressor, valve, and pipe per the pressure-unit table."""
    runtime.attach_artifact(
        "pump_curve_unit_assumption",
        {
            "block": "FP",
            "task_label": "FEEDPUMP",
            "flow_unit": "m3/hr",
            "head_unit_interpretation": "m",
            "curve_points": [dict(point) for point in PUMP_CURVE_POINTS],
            "note": "The table gives flow in m3/h and head without a printed unit; the native pump-curve write uses meters of head and records that assumption.",
        },
    )
    runtime.stage("FP_curve_mode", lambda: client.invoke("set_pump_outlet_spec", block_name="FP", value="USE-CURVE"), required=True)
    runtime.stage("FP_curve_control_type", lambda: client.invoke("set_opt_ctype", block_name="FP", value="SINGLE-OPER"), required=True)
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
            curve_points=[dict(point) for point in PUMP_CURVE_POINTS],
        ),
        required=True,
    )
    runtime.stage("FP_pump_efficiency", lambda: client.invoke("set_eff", block_name="FP", value=0.6), required=True)
    runtime.stage("FP_driver_efficiency", lambda: client.invoke("set_deff", block_name="FP", value=0.9), required=True)

    runtime.stage("P1_outlet_spec", lambda: client.invoke("set_pump_outlet_spec", block_name="P1", value="PRES"), required=True)
    runtime.stage("P1_outlet_pressure", lambda: client.invoke("set_pump_outlet_pressure", block_name="P1", value=2.6, unit="MPa"), required=True)

    runtime.stage(
        "CP_pressure_rise",
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


def _configure_process_blocks(runtime, client) -> None:
    """Configure reactor, flash, splitters, heater, and RadFrac column."""
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
            products={"CYCLO-01": 1.0},
        ),
        required=True,
    )
    runtime.stage(
        "R1_conversion",
        lambda: client.invoke(
            "configure_rstoic_fractional_conversions",
            block_name="R1",
            conversions=[
                {
                    "reaction_number": 1,
                    "component_id": "BENZENE",
                    "conversion": 0.998,
                }
            ],
        ),
        required=True,
    )
    runtime.stage(
        "R1_flash",
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

    runtime.stage("HS_flash_spec", lambda: client.invoke("set_flash2_flash_spec", block_name="HS", value="TP"), required=True)
    runtime.stage("HS_temperature", lambda: client.invoke("set_flash2_temperature", block_name="HS", value=50.0, unit="C"), required=True)
    runtime.stage("HS_pressure_drop", lambda: client.invoke("set_flash2_pressure", block_name="HS", value=-0.05, unit="MPa"), required=True)

    runtime.stage(
        "VF_split_fraction",
        lambda: client.invoke(
            "configure_fsplit_shared_outlets",
            block_name="VF",
            inlet_stream="V1",
            outlet_streams=["H4", "P2"],
            split_fractions={"H4": 0.92},
        ),
        required=True,
    )
    runtime.stage(
        "LF_split_fraction",
        lambda: client.invoke(
            "configure_fsplit_shared_outlets",
            block_name="LF",
            inlet_stream="L1",
            outlet_streams=["C2", "C1"],
            split_fractions={"C2": 0.30},
        ),
        required=True,
    )

    runtime.stage("CO_condenser", lambda: client.invoke("set_radfrac_condenser_type", block_name="CO", value="PARTIAL-V"), required=True)
    runtime.stage("CO_reboiler", lambda: client.invoke("set_radfrac_reboiler_type", block_name="CO", value="KETTLE"), required=True)
    runtime.stage("CO_stage_count", lambda: client.invoke("set_radfrac_stage_count", block_name="CO", value=12), required=True)
    runtime.stage("CO_feed_stage", lambda: client.invoke("set_radfrac_feed_stage", block_name="CO", stream_name="C1", value=8), required=True)
    runtime.stage("CO_feed_convention", lambda: client.invoke("configure_radfrac_feed_convention", block_name="CO", stream_name="C1", convention="ON-STAGE-LIQ"), required=True)
    runtime.stage("CO_top_pressure", lambda: client.invoke("set_radfrac_top_pressure", block_name="CO", value=1.5, unit="MPa"), required=True)
    runtime.stage("CO_reflux_ratio", lambda: client.invoke("set_radfrac_reflux_ratio", block_name="CO", value=1.2), required=True)
    runtime.stage("CO_distillate_rate", lambda: client.invoke("set_radfrac_distillate_rate", block_name="CO", value=99.0, unit="kmol/hr"), required=True)


def _configure_convergence_and_probes(runtime, client) -> None:
    """Add recycle convergence settings and bounded readiness diagnostics."""
    runtime.stage(
        "recycle_convergence_options",
        lambda: client.invoke(
            "configure_recycle_convergence_options",
            tolerance=1e-5,
            tear_method="WEGSTEIN",
            wegstein_max_iterations=100,
        ),
        required=False,
    )
    for block_name in REQUIRED_BLOCKS:
        runtime.stage(
            f"check_block_{block_name}",
            lambda block_name=block_name: client.invoke(
                "check_block_completion",
                block_name=block_name,
            ),
            required=False,
        )
    runtime.stage(
        "check_flowsheet_completion",
        lambda: client.invoke("check_flowsheet_completion"),
        required=False,
    )


def configure(runtime) -> SlimTaskOutcome:
    """Configure the complete Aspen model; slim runtime performs final evidence."""
    client = runtime.client
    _validate_static_plans()
    runtime.attach_artifact(
        "static_material_edge_plan",
        {
            "edges": [dict(edge) for edge in MATERIAL_EDGES],
            "policy": "Each physical material stream appears exactly once; C4/CHRCY3 is represented only by PI -> FM.",
        },
    )
    runtime.attach_artifact(
        "task_name_mapping",
        NAME_MAPPING,
    )

    _setup_components_and_property(runtime, client)
    _create_streams_and_blocks(runtime, client)
    _connect_topology(runtime, client)
    _configure_feed_streams(runtime, client)
    _configure_pressure_changers(runtime, client)
    _configure_process_blocks(runtime, client)
    _configure_convergence_and_probes(runtime, client)

    return SlimTaskOutcome(
        fields={
            "modeled_task": "Cyclohexane production with reactor, flash separator, vapor recycle/purge, liquid recycle, pressure-changing units, and RadFrac stabilizer.",
            "primary_result_request": {
                "stream": "P4",
                "task_stream_label": "PRODUCT",
                "component": "CYCLO-01",
                "quantity": "mole_fraction",
                "basis": "raw full material stream mole fraction from final REP readback",
            },
            "fixed_inputs": {
                "H2IN_H1": {
                    "temperature_C": 50.0,
                    "pressure_MPa": 2.5,
                    "total_kmol_hr": 330.0,
                    "mole_fractions": {"H2": 0.975, "N2": 0.005, "CH4": 0.02},
                },
                "BZIN_B1": {
                    "temperature_C": 40.0,
                    "pressure_MPa": 0.1,
                    "benzene_kmol_hr": 100.0,
                },
                "reaction": {
                    "stoichiometry": "BENZENE + 3 H2 -> CYCLO-01",
                    "benzene_conversion_fraction": 0.998,
                },
                "split_fractions": {"VFLOW_H2RCY": 0.92, "LFLOW_CHRCY": 0.30},
                "column": {
                    "nstage": 12,
                    "feed_stage": 8,
                    "reflux_ratio": 1.2,
                    "top_pressure_MPa": 1.5,
                    "distillate_rate_kmol_hr": 99.0,
                    "condenser": "PARTIAL-V vapor-only distillate semantics",
                },
            },
        },
        analysis_handoff={
            "native_analysis_required": False,
            "final_runtime_action": "Slim runtime should run completion/engine/export once after configuration and collect declared REP readbacks.",
            "required_blocks_by_family": REQUIRED_BLOCKS_BY_FAMILY,
            "required_streams": list(REQUIRED_STREAMS),
            "required_blocks": list(REQUIRED_BLOCKS),
        },
        analysis_objects={},
        validation_contract={
            "phase": "final_evidence_fact_production",
            "no_script_judgment_policy": True,
            "validator_decision_pending": True,
            "evidence_index": {
                "topology": "static_material_edge_plan artifact plus runtime stage port/connect receipts",
                "product_metric": "REP readback target product_cyclohexane_mole_fraction on stream P4 / PRODUCT",
                "reactor_contract": "R1_stoichiometry and R1_conversion stage receipts plus reactor_benzene_conversion REP derived target",
                "pressure_units": "pressure-changing unit stage receipts and pump_curve_unit_assumption artifact",
                "column_contract": "CO RadFrac specification stages plus CO block REP targets",
            },
            "result_path_requirements": [
                {
                    "result": "cyclohexane mole fraction in PRODUCT/P4",
                    "must_derive_from": "final converged Aspen REP stream evidence",
                    "forbid_sources": ["feed composition", "stoichiometric hand calculation", "another outlet stream"],
                }
            ],
        },
    )


if __name__ == "__main__":
    raise SystemExit(run_slim_task(spec=TASK_SPEC, configure=configure))
