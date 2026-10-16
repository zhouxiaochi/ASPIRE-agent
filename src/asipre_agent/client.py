from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any, Mapping, Protocol
class HttpResponse(Protocol):
    status_code: int
    def json(self) -> Any: ...
class HttpTransport(Protocol):
    def request(self, method: str, url: str, *, json: Mapping[str, Any] | None = None, timeout: float | None = None) -> HttpResponse: ...
@dataclass
class HttpxTransport:
    def request(self, method: str, url: str, *, json: Mapping[str, Any] | None = None, timeout: float | None = None) -> HttpResponse:
        try: import httpx
        except ImportError as exc: raise RuntimeError("Install asipre-agent[http] to use the HTTP client") from exc
        return httpx.request(method, url, json=json, timeout=timeout)
class AspenError(RuntimeError): pass
_UNSET = object()

def is_explicitly_complete(payload: Mapping[str, Any]) -> bool:
    """Accept explicit completion evidence while failing closed on unknown payloads."""
    if payload.get("success") is False: return False
    for key in ("complete", "input_complete", "required_input_complete", "workflow_ready_by_fallback", "fallback_ready"):
        if key in payload: return payload[key] is True
    state = str(payload.get("input_state") or "").strip().casefold()
    if state in {"complete", "input_complete", "required_input_complete"}: return True
    diagnostic = str(payload.get("diagnostic_kind") or payload.get("feedback_window_kind") or "").strip().casefold()
    required = diagnostic == "required_input_complete"
    if payload.get("no_completion_issues") is True and required: return True
    engine = payload.get("engine_run")
    return bool(payload.get("guardrail_reason") == "non_gui_short_circuit_engine_run_success" and required and isinstance(engine,dict) and engine.get("success") is True)

class AspenClient:
    def __init__(self, base_url: str = "http://127.0.0.1:5000", *, transport: HttpTransport | None = None, timeout: float = 60.0, ui_timeout: float | None = None): self.base_url,self.transport,self.timeout,self.ui_timeout=base_url.rstrip("/"),transport or HttpxTransport(),timeout,ui_timeout or timeout
    def _call(self, method: str, path: str, payload: Mapping[str, Any] | None=None) -> dict[str, Any]:
        call_timeout=self.ui_timeout if path=="/session/execute" and payload and payload.get("operation")=="ui_check_next_completion_status" else self.timeout
        response=self.transport.request(method,self.base_url+path,json=payload,timeout=call_timeout); body=response.json()
        if response.status_code>=400: raise AspenError(f"{method} {path} failed ({response.status_code}): {json.dumps(body,default=str)}")
        if not isinstance(body,dict): raise AspenError(f"{method} {path} returned a non-object response")
        return body
    def health(self): return self._call("GET","/health")
    def start(self,key: str,*,initial_bkp: str|None=None,show_gui: bool|object=_UNSET):
        payload={"task_hash":key};
        if initial_bkp is not None: payload["initial_bkp"]=initial_bkp
        if show_gui is not _UNSET: payload["show_gui"]=bool(show_gui)
        return self._call("POST","/session/start",payload)
    def load(self,key: str,bkp_path: str,*,show_gui: bool|object=_UNSET):
        payload={"task_hash":key,"bkp_path":bkp_path}
        if show_gui is not _UNSET: payload["show_gui"]=bool(show_gui)
        return self._call("POST","/session/load_bkp",payload)
    def checkpoint(self,key: str,filename: str|None=None): return self._call("POST","/session/checkpoint",{"task_hash":key,"filename":filename})
    def close(self,key: str): return self._call("POST","/session/close",{"task_hash":key})
    def execute(self,key: str,operation: str,**parameters: Any):
        envelope=self._call("POST","/session/execute",{"task_hash":key,"operation":operation,"parameters":parameters})
        result=envelope.get("result")
        return result if isinstance(result,dict) else envelope
    def create_material_stream(self,key: str,stream_name: str): return self.execute(key,"create_material_stream",stream_name=stream_name)
    def create_heat_stream(self,key: str,stream_name: str): return self.execute(key,"create_heat_stream",stream_name=stream_name)
    def create_mixer_block(self,key: str,block_name: str): return self.execute(key,"create_mixer",block_name=block_name)
    def create_heater_block(self,key: str,block_name: str): return self.execute(key,"create_heater",block_name=block_name)
    def list_block_ports(self,key: str,block_name: str): return self.execute(key,"list_block_ports",block_name=block_name)
    def connect_stream(self,key: str,block_name: str,stream_name: str,port_name: str):
        raw=self.list_block_ports(key,block_name).get("ports",{}); names=set(raw) if isinstance(raw,dict) else {p.get("name") for p in raw if isinstance(p,dict)}
        if port_name not in names: raise AspenError(f"Live port not found: {block_name}.{port_name}")
        return self.execute(key,"connect_stream",block_name=block_name,stream_name=stream_name,port_name=port_name)
    def inspect_component_table(self,key: str,component_ids: list[str]): return self.execute(key,"inspect_component_table",component_ids=component_ids)
    def add_components(self,key: str,names: list[str]):
        from .components import CompoundRegistry
        compounds=[CompoundRegistry().resolve(name) for name in names]; records=[{"component_id":x.aspen_id,"cas":x.cas} for x in compounds]
        added=self.execute(key,"add_components_by_cas",components=records)
        if added.get("success") is False: raise AspenError(f"Component addition failed: {added}")
        entries=added.get("components_added",[])
        visible_ids=[str(entry.get("component_id","")).strip().upper() for entry in entries if isinstance(entry,dict) and str(entry.get("component_id","")).strip()]
        if not visible_ids: raise AspenError(f"Component addition returned no visible component IDs: {added}")
        verification=added.get("verification")
        if isinstance(verification,dict) and (verification.get("success") is False or verification.get("missing_component_ids")):
            raise AspenError(f"Component addition verification failed: {verification}")
        inspected=self.inspect_component_table(key,visible_ids)
        missing=inspected.get("missing_requested_component_ids")
        if missing is None:
            rows=inspected.get("rows",[]); visible={str(row.get("component_id","")).upper() for row in rows if isinstance(row,dict)}; missing=[x.aspen_id for x in compounds if x.aspen_id.upper() not in visible]
        if missing: raise AspenError(f"Component table verification failed: {', '.join(map(str,missing))}")
        return {"components_added":added.get("components_added",added),"verification":added.get("verification"),"inspection":inspected}
    def configure_material_stream_tp(self,key: str,stream_name: str,*,temperature: float,temperature_unit: str,pressure: float,pressure_unit: str,basis: str,component_flows: Mapping[str,float],flow_unit: str):
        from .components import CompoundRegistry
        normalized_basis=basis.upper()
        if normalized_basis not in {"MOLE-FLOW","MASS-FLOW"}: raise ValueError("basis must be MOLE-FLOW or MASS-FLOW")
        if not component_flows: raise ValueError("component_flows must not be empty")
        resolved=[]
        for name,value in component_flows.items():
            numeric=float(value)
            if numeric<0: raise ValueError(f"Component flow must be nonnegative: {name}")
            resolved.append((CompoundRegistry().resolve(name).aspen_id,numeric))
        if not any(value>0 for _,value in resolved): raise ValueError("At least one component flow must be positive")
        calls=[self.execute(key,"set_mixed_spec_mixed",stream_name=stream_name,value="TP"),self.execute(key,"set_temp_mixed",stream_name=stream_name,value=temperature,unit=temperature_unit),self.execute(key,"set_pres_mixed",stream_name=stream_name,value=pressure,unit=pressure_unit),self.execute(key,"set_basis_mixed",stream_name=stream_name,value=normalized_basis)]
        for component_id,value in resolved: calls.append(self.execute(key,"set_flow_mixed",stream_name=stream_name,component_name=component_id,value=value,unit=flow_unit))
        return {"stream_name":stream_name,"basis":normalized_basis,"component_ids":[item[0] for item in resolved],"results":calls}
    def configure_mixer(self,key: str,block_name: str,*,energy_balance: bool,pressure: float,pressure_unit: str):
        energy=self.execute(key,"set_energy_bal",block_name=block_name,value="YES" if energy_balance else "NO"); pres=self.execute(key,"set_pres",block_name=block_name,value=pressure,unit=pressure_unit); return {"energy_balance":energy,"pressure":pres}
    def configure_heater(self,key: str,block_name: str,mode: str,**values: Any):
        mode=mode.upper(); required={"TP":(("temperature","set_temp"),("pressure","set_pres")),"PV":(("pressure","set_pres"),("vapor_fraction","set_vfrac")),"PD":(("pressure","set_pres"),("duty","set_duty"))}
        if mode not in required: raise ValueError("Heater mode must be TP, PV, or PD")
        results=[self.execute(key,"set_spec_opt",block_name=block_name,value=mode)]
        for name,operation in required[mode]:
            if name not in values: raise ValueError(f"Heater {mode} requires {name}")
            params={"block_name":block_name,"value":values[name]}; unit=values.get(name+"_unit")
            if unit is not None: params["unit"]=unit
            results.append(self.execute(key,operation,**params))
        return {"mode":mode,"results":results}
    def completion(self,key: str): return self.execute(key,"check_flowsheet_completion")
    def next_status(self,key: str): return self.execute(key,"ui_check_next_completion_status")
    def preflight(self,key: str):
        completion,next_status=self.completion(key),self.next_status(key)
        if not is_explicitly_complete(completion) or not is_explicitly_complete(next_status): raise AspenError(f"Preflight incomplete: completion={completion}, next={next_status}")
        return {"complete":True,"completion":completion,"next_status":next_status}
    def run(self,key: str):
        preflight=self.preflight(key); next_status=preflight["next_status"]; engine=next_status.get("engine_run")
        if next_status.get("guardrail_reason")=="non_gui_short_circuit_engine_run_success" and isinstance(engine,dict) and engine.get("success") is True:
            return {**engine,"source":"next_gate_short_circuit"}
        return self.execute(key,"engine_run")
    def export_rep(self,key: str,filename: str|None=None):
        params={"export_format":2}
        if filename is not None: params["filename"]=filename
        return self.execute(key,"export_rep",**params)
    def export_apw(self,key: str,filename: str|None=None):
        params={}
        if filename is not None: params["filename"]=filename
        return self.execute(key,"export_apw",**params)
    def export_evidence(self,key: str,name: str|None=None):
        if name is not None:
            from pathlib import PurePosixPath
            normalized=name.replace("\\","/"); path=PurePosixPath(normalized)
            if path.is_absolute() or ".." in path.parts or (path.parts and ":" in path.parts[0]): raise ValueError("Evidence name must be a safe server-relative path")
            stem=str(path.with_suffix("")) if path.suffix.lower() in {".rep",".apw"} else str(path)
            rep_name,apw_name=stem+".rep",stem+".apw"
        else: rep_name=apw_name=None
        rep=self.export_rep(key,rep_name); apw=self.export_apw(key,apw_name)
        return {"rep":rep,"apw":apw}
