import pytest
from aspire_agent.com.setters import SetterError,set_heater,set_mixer
class Node:
    def __init__(self): self.Value="stale"; self.writes=[]
    def SetValueAndUnit(self,value,unit): self.Value=value; self.writes.append((value,unit))
class Tree:
    def __init__(self,block):
        root=f"Data\\Blocks\\{block}\\Input"; self.nodes={root+"\\"+x:Node() for x in ("ENERGY_BAL","PRES","SPEC_OPT","TEMP","VFRAC","DUTY")}
    def FindNode(self,path): return self.nodes.get(path)
def test_mixer_yes_no_numeric_pressure_with_unit():
    tree=Tree("M1"); result=set_mixer(tree,"M1",energy_balance="YES",pressure=2.5,pressure_unit="bar"); assert result["PRES"]==2.5; assert tree.FindNode("Data\\Blocks\\M1\\Input\\PRES").writes==[(2.5,"bar")]
    with pytest.raises(SetterError): set_mixer(tree,"M1",energy_balance="ADIABATIC",pressure=2,pressure_unit="bar")
def test_heater_unit_writes_and_stale_clear():
    tree=Tree("H1"); set_heater(tree,"H1","TP",temperature=350,temperature_unit="K",pressure=2,pressure_unit="bar"); assert tree.FindNode("Data\\Blocks\\H1\\Input\\TEMP").writes==[(350,"K")]; assert tree.FindNode("Data\\Blocks\\H1\\Input\\DUTY").Value is None
    set_heater(tree,"H1","PV",pressure=2,pressure_unit="bar",vapor_fraction=.5); set_heater(tree,"H1","PD",pressure=2,pressure_unit="bar",duty=0,duty_unit="kW")
    with pytest.raises(SetterError): set_heater(tree,"H1","TP",temperature=350,pressure=2,pressure_unit="bar")
from aspire_agent.com.setters import set_basis_mixed,set_flow_mixed,set_mixed_spec_mixed,set_pres_mixed,set_temp_mixed,set_totflow_mixed
class StreamNode:
    def __init__(self): self.Value=None; self.writes=[]
    def SetValueAndUnit(self,value,unit): self.Value=value; self.writes.append((value,unit))
class StreamTree:
    def __init__(self): self.nodes={}
    def FindNode(self,path): return self.nodes.setdefault(path,StreamNode())
def test_tree_material_stream_setters():
    tree=StreamTree();set_mixed_spec_mixed(tree,"F1","TP");set_temp_mixed(tree,"F1",300,"K");set_pres_mixed(tree,"F1",2,"bar");set_basis_mixed(tree,"F1","MASS-FLOW");set_flow_mixed(tree,"F1","WATER",10,"kg/hr");set_totflow_mixed(tree,"F1",10,"kg/hr")
    assert tree.FindNode("Data\\Streams\\F1\\Input\\MIXED_SPEC\\MIXED").Value=="TP"
    assert tree.FindNode("Data\\Streams\\F1\\Input\\FLOW\\MIXED\\WATER").writes==[(10,"kg/hr")]
