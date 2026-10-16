from __future__ import annotations
from typing import Any, Callable
from .operations import connect_stream, create_heat_stream, create_heater_block, create_material_stream, create_mixer_block, list_block_ports
from .setters import _set, set_basis_mixed, set_flow_mixed, set_heater, set_mixed_spec_mixed, set_mixer, set_pres_mixed, set_temp_mixed, set_totflow_mixed
Operation = Callable[..., Any]
TYPE_PATH=r"Data\Components\Specifications\Input\TYPE"; ROW_COMP_ID=0; ROW_CAS=4

def _children(node: Any) -> list[Any]:
    elements=getattr(node,"Elements",None); count=int(getattr(elements,"Count",0)); out=[]
    for index in list(range(count))+list(range(1,count+1)):
        try: item=elements.Item(index)
        except Exception: continue
        if item is not None and item not in out: out.append(item)
    return out

def _label(table: Any,row: int,col: int) -> str:
    getter=getattr(table,"GetLabel",None)
    if callable(getter):
        try: return str(getter(row,col,False) or "").strip()
        except Exception: return ""
    return ""

def _visible_components(tree: Any) -> list[dict[str,str]]:
    table=tree.FindNode(TYPE_PATH)
    if table is None: return []
    if callable(getattr(table,"GetLabel",None)):
        rows=[]; empty=0
        for col in range(200):
            cid,cas=_label(table,ROW_COMP_ID,col).upper(),_label(table,ROW_CAS,col)
            if not cid and not cas:
                empty+=1
                if rows and empty>=3: break
                continue
            empty=0; rows.append({"component_id":cid,"cas":cas})
        return rows
    return [{"component_id":str(getattr(item,"Name","" )).upper(),"cas":str(getattr(item,"CAS",getattr(item,"cas","")))} for item in _children(table)]

def inspect_component_table(tree: Any,component_ids: list[str]|None=None,max_cols: int=200) -> dict[str,Any]:
    requested=[str(value).strip().upper() for value in (component_ids or []) if str(value).strip()]; rows=_visible_components(tree); selected=[row for row in rows if not requested or row["component_id"] in requested]; matched=[row["component_id"] for row in selected]
    return {"success":True,"table_path":TYPE_PATH,"row_count":len(rows),"component_ids":[row["component_id"] for row in rows],"rows":selected,"requested_component_ids":requested,"matched_component_ids":matched,"missing_requested_component_ids":[value for value in requested if value not in matched]}

def add_components_by_cas(tree: Any,components: list[dict[str,str]]) -> dict[str,Any]:
    table=tree.FindNode(TYPE_PATH)
    if table is None: raise RuntimeError("Component TYPE table not found")
    setter=getattr(table,"SetLabel",None)
    if callable(setter):
        existing=len(_visible_components(tree))
        for offset,record in enumerate(components):
            col=existing+offset; setter(ROW_CAS,col,False,str(record["cas"])); setter(ROW_COMP_ID,col,False,str(record["component_id"]))
    else:
        add_record=getattr(table,"AddComponentRecord",None)
        if not callable(add_record): raise RuntimeError("TYPE table lacks SetLabel and explicit AddComponentRecord fallback")
        for record in components: add_record(str(record["cas"]),str(record["component_id"]))
    inspection=inspect_component_table(tree,[record["component_id"] for record in components])
    if inspection["missing_requested_component_ids"]: raise RuntimeError(f"Visible TYPE-table verification failed: {inspection['missing_requested_component_ids']}")
    return {"success":True,"components_added":[record["component_id"] for record in components],"verification":inspection}

def _scalar(tree: Any,block_name: str,leaf: str,value: Any,unit: str|None=None):
    _set(tree,f"Data\\Blocks\\{block_name}\\Input\\{leaf}",value,unit); return {"success":True,"block_name":block_name,"value":value,"unit":unit}
def set_energy_bal(tree: Any,block_name: str,value: Any,unit: str|None=None): return _scalar(tree,block_name,"ENERGY_BAL",value,unit)
def set_pres(tree: Any,block_name: str,value: Any,unit: str|None=None): return _scalar(tree,block_name,"PRES",value,unit)
def set_spec_opt(tree: Any,block_name: str,value: Any,unit: str|None=None): return _scalar(tree,block_name,"SPEC_OPT",value,unit)
def set_temp(tree: Any,block_name: str,value: Any,unit: str|None=None): return _scalar(tree,block_name,"TEMP",value,unit)
def set_vfrac(tree: Any,block_name: str,value: Any,unit: str|None=None): return _scalar(tree,block_name,"VFRAC",value,unit)
def set_duty(tree: Any,block_name: str,value: Any,unit: str|None=None): return _scalar(tree,block_name,"DUTY",value,unit)
def check_flowsheet_completion(document: Any): return dict(document.CheckFlowsheetCompletion())
def check_next_completion_status(document: Any): return dict(document.CheckNextCompletionStatus())
def engine_run(document: Any): return dict(document.EngineRun())
def export_rep(document: Any,filename: str|None=None,export_format: int=2): return dict(document.ExportRep(filename,export_format))
def export_apw(document: Any,filename: str|None=None): return dict(document.ExportApw(filename))
def export_evidence(document: Any,output_dir: str): return {"rep":export_rep(document,output_dir+".rep"),"apw":export_apw(document,output_dir+".apw")}

def operation_registry() -> dict[str,tuple[Operation,str]]:
    tree={"create_material_stream":create_material_stream,"create_heat_stream":create_heat_stream,"create_mixer":create_mixer_block,"create_heater":create_heater_block,"create_mixer_block":create_mixer_block,"create_heater_block":create_heater_block,"list_block_ports":list_block_ports,"connect_stream":connect_stream,"add_components_by_cas":add_components_by_cas,"inspect_component_table":inspect_component_table,"configure_mixer":set_mixer,"configure_heater":set_heater,"set_energy_bal":set_energy_bal,"set_pres":set_pres,"set_spec_opt":set_spec_opt,"set_temp":set_temp,"set_vfrac":set_vfrac,"set_duty":set_duty,"set_mixed_spec_mixed":set_mixed_spec_mixed,"set_temp_mixed":set_temp_mixed,"set_pres_mixed":set_pres_mixed,"set_basis_mixed":set_basis_mixed,"set_totflow_mixed":set_totflow_mixed,"set_flow_mixed":set_flow_mixed}
    doc={"check_flowsheet_completion":check_flowsheet_completion,"ui_check_next_completion_status":check_next_completion_status,"check_next_completion_status":check_next_completion_status,"engine_run":engine_run,"export_rep":export_rep,"export_apw":export_apw,"export_evidence":export_evidence}
    return {**{name:(func,"tree") for name,func in tree.items()},**{name:(func,"doc") for name,func in doc.items()}}
def execute(document: Any,operation: str,parameters: dict[str,Any]):
    try: function,target=operation_registry()[operation]
    except KeyError as exc: raise ValueError(f"Unsupported public operation: {operation}") from exc
    return function(document.Tree if target=="tree" else document,**parameters)
