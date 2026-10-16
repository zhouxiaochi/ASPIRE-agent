from __future__ import annotations
from typing import Any, Callable

class SetterError(ValueError): pass
UnitResolver = Callable[[str, str], str | None]

def _node(tree: Any, path: str) -> Any:
    node = tree.FindNode(path)
    if node is None: raise SetterError(f"Aspen tree path not found: {path}")
    return node

def _set(tree: Any, path: str, value: Any, unit: str | None = None, unit_resolver: UnitResolver | None = None) -> None:
    node = _node(tree, path)
    if unit is None: node.Value = value; return
    resolved = unit_resolver(path, unit) if unit_resolver else unit
    setter = getattr(node, "SetValueAndUnit", None)
    if not callable(setter): raise SetterError(f"Unit-aware write unavailable for {path}; cannot safely write {value} {unit}")
    setter(value, resolved)

def _clear(tree: Any, path: str) -> None:
    node = tree.FindNode(path)
    if node is not None:
        try: node.Value = None
        except Exception: pass

def set_mixer(tree: Any, block_name: str, *, energy_balance: str, pressure: float, pressure_unit: str, unit_resolver: UnitResolver | None = None) -> dict[str, Any]:
    energy = energy_balance.upper()
    if energy not in {"YES", "NO"}: raise SetterError("Mixer ENERGY_BAL must be YES or NO")
    root = f"Data\\Blocks\\{block_name}\\Input"
    _set(tree, root + "\\ENERGY_BAL", energy)
    _set(tree, root + "\\PRES", pressure, pressure_unit, unit_resolver)
    return {"ENERGY_BAL": energy, "PRES": pressure, "PRES_UOM": pressure_unit}

def set_heater(tree: Any, block_name: str, mode: str, *, temperature: float | None = None, temperature_unit: str | None = None, pressure: float | None = None, pressure_unit: str | None = None, vapor_fraction: float | None = None, duty: float | None = None, duty_unit: str | None = None, unit_resolver: UnitResolver | None = None) -> dict[str, Any]:
    mode = mode.upper(); required = {"TP": ("temperature", "pressure"), "PV": ("pressure", "vapor_fraction"), "PD": ("pressure", "duty")}
    values = {"temperature": temperature, "pressure": pressure, "vapor_fraction": vapor_fraction, "duty": duty}
    units = {"temperature": temperature_unit, "pressure": pressure_unit, "vapor_fraction": None, "duty": duty_unit}
    if mode not in required: raise SetterError("Heater mode must be TP, PV, or PD")
    missing = [name for name in required[mode] if values[name] is None or (name != "vapor_fraction" and units[name] is None)]
    if missing: raise SetterError(f"Heater {mode} requires values and units for: {', '.join(missing)}")
    root = f"Data\\Blocks\\{block_name}\\Input"; paths = {"temperature": "TEMP", "pressure": "PRES", "vapor_fraction": "VFRAC", "duty": "DUTY"}
    _set(tree, root + "\\SPEC_OPT", mode)
    active = set(required[mode])
    for key, leaf in paths.items():
        if key in active: _set(tree, root + "\\" + leaf, values[key], units[key], unit_resolver)
        else: _clear(tree, root + "\\" + leaf)
    return {"SPEC_OPT": mode, **{paths[key]: values[key] for key in active}}

def set_mixed_spec_mixed(tree: Any,stream_name: str,value: str):
    if value not in {"TP","TV","PV"}: raise SetterError("Material stream state must be TP, TV, or PV")
    _set(tree,f"Data\\Streams\\{stream_name}\\Input\\MIXED_SPEC\\MIXED",value); return {"success":True,"stream_name":stream_name,"value":value}
def set_temp_mixed(tree: Any,stream_name: str,value: float,unit: str):
    _set(tree,f"Data\\Streams\\{stream_name}\\Input\\TEMP\\MIXED",value,unit); return {"success":True,"stream_name":stream_name,"value":value,"unit":unit}
def set_pres_mixed(tree: Any,stream_name: str,value: float,unit: str):
    _set(tree,f"Data\\Streams\\{stream_name}\\Input\\PRES\\MIXED",value,unit); return {"success":True,"stream_name":stream_name,"value":value,"unit":unit}
def set_basis_mixed(tree: Any,stream_name: str,value: str):
    if value not in {"MOLE-FLOW","MASS-FLOW"}: raise SetterError("Local stream basis supports MOLE-FLOW or MASS-FLOW")
    _set(tree,f"Data\\Streams\\{stream_name}\\Input\\BASIS\\MIXED",value); return {"success":True,"stream_name":stream_name,"value":value}
def set_totflow_mixed(tree: Any,stream_name: str,value: float,unit: str):
    _set(tree,f"Data\\Streams\\{stream_name}\\Input\\TOTFLOW\\MIXED",value,unit); return {"success":True,"stream_name":stream_name,"value":value,"unit":unit}
def set_flow_mixed(tree: Any,stream_name: str,component_name: str,value: float,unit: str):
    _set(tree,f"Data\\Streams\\{stream_name}\\Input\\FLOW\\MIXED\\{component_name}",value,unit); return {"success":True,"stream_name":stream_name,"component_name":component_name,"value":value,"unit":unit}
