from asipre_agent.com.dispatch import execute
class Table:
    def __init__(self): self.labels={};self.calls=[]
    def SetLabel(self,row,col,flag,value): self.calls.append((row,col,flag,value));self.labels[(row,col)]=value
    def GetLabel(self,row,col,flag): return self.labels.get((row,col),"")
class Tree:
    def __init__(self): self.table=Table()
    def FindNode(self,path): return self.table if path==r"Data\Components\Specifications\Input\TYPE" else None
class Doc:
    def __init__(self): self.Tree=Tree()
    def CheckFlowsheetCompletion(self): return {"input_complete":True}
    def CheckNextCompletionStatus(self): return {"required_input_complete":True}
    def EngineRun(self): return {"run":"ok"}
    def ExportEvidence(self,path): return {"output_dir":path}
    def ExportRep(self,filename,export_format): return {"rep_path":filename,"export_format":export_format}
    def ExportApw(self,filename): return {"apw_path":filename}
def test_component_setlabel_cas_before_id_and_inspection():
    doc=Doc();result=execute(doc,"add_components_by_cas",{"components":[{"component_id":"WATER","cas":"7732-18-5"}]});assert doc.Tree.table.calls==[(4,0,False,"7732-18-5"),(0,0,False,"WATER")];assert result["verification"]["missing_requested_component_ids"]==[]
    inspected=execute(doc,"inspect_component_table",{"component_ids":["WATER"]});assert inspected["rows"]==[{"component_id":"WATER","cas":"7732-18-5"}]
def test_document_operations():
    doc=Doc();assert execute(doc,"check_flowsheet_completion",{})["input_complete"];assert execute(doc,"engine_run",{})["run"]=="ok"

def test_canonical_block_dispatch_aliases():
    class Elements:
        def __init__(self): self.added=[]
        def Add(self,value): self.added.append(value); return True
    class Node:
        def __init__(self): self.Elements=Elements()
    class Tree:
        def __init__(self): self.blocks=Node()
        def FindNode(self,path): return self.blocks if path==r"Data\Blocks" else None
    doc=Doc();doc.Tree=Tree()
    assert execute(doc,"create_mixer",{"block_name":"M1"})["block_type"]=="MIXER"
    assert execute(doc,"create_heater",{"block_name":"H1"})["block_type"]=="HEATER"
    assert doc.Tree.blocks.Elements.added==["M1!MIXER","H1!HEATER"]

def test_canonical_next_gate_dispatch_alias():
    doc=Doc()
    assert execute(doc,"ui_check_next_completion_status",{})["required_input_complete"] is True

def test_material_stream_operations_are_dispatched():
    class Node:
        def __init__(self): self.Value=None;self.writes=[]
        def SetValueAndUnit(self,value,unit): self.Value=value;self.writes.append((value,unit))
    class Tree:
        def __init__(self): self.nodes={}
        def FindNode(self,path): return self.nodes.setdefault(path,Node())
    doc=Doc();doc.Tree=Tree()
    execute(doc,"set_mixed_spec_mixed",{"stream_name":"F1","value":"TP"});execute(doc,"set_temp_mixed",{"stream_name":"F1","value":300,"unit":"K"});execute(doc,"set_pres_mixed",{"stream_name":"F1","value":1,"unit":"bar"});execute(doc,"set_basis_mixed",{"stream_name":"F1","value":"MOLE-FLOW"});execute(doc,"set_totflow_mixed",{"stream_name":"F1","value":1,"unit":"kmol/hr"});execute(doc,"set_flow_mixed",{"stream_name":"F1","component_name":"WATER","value":1,"unit":"kmol/hr"})

def test_canonical_evidence_dispatch():
    doc=Doc()
    assert execute(doc,"export_rep",{"filename":"case.rep","export_format":2})=={"rep_path":"case.rep","export_format":2}
    assert execute(doc,"export_apw",{"filename":"case.apw"})=={"apw_path":"case.apw"}
