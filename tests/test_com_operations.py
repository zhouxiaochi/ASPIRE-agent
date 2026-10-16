import pytest
from aspire_agent.com.operations import *
class Elements:
    def __init__(self, items=None, add_factory=None): self.items=list(items or []); self.added=[]; self.add_factory=add_factory
    @property
    def Count(self): return len(self.items)
    def Item(self,key):
        if isinstance(key,str): return next(x for x in self.items if x.Name==key)
        return self.items[key]
    def Add(self,token): self.added.append(token); self.items.append(self.add_factory(token) if self.add_factory else Named(token)); return True
class Named:
    def __init__(self,name,elements=None): self.Name=name; self.Elements=elements or Elements(); self.Direction="IN"; self.Kind="MATERIAL"
class Tree:
    def __init__(self):
        self.streams=Named("Streams",Elements()); self.blocks=Named("Blocks",Elements()); connections=Elements(add_factory=lambda name: Named(name)); self.port=Named("F(IN)",connections); self.block=Named("M1"); self.block.Ports=Elements([self.port]); self.nodes={r"Data\Streams":self.streams,r"Data\Blocks":self.blocks,r"Data\Blocks\M1":self.block}
    def FindNode(self,path): return self.nodes.get(path)

def test_tree_creation_tokens():
    tree=Tree(); create_material_stream(tree,"F1"); create_heat_stream(tree,"Q1"); create_mixer_block(tree,"M1"); create_heater_block(tree,"H1")
    assert tree.streams.Elements.added == ["F1!MATERIAL","Q1!HEAT"]
    assert tree.blocks.Elements.added == ["M1!MIXER","H1!HEATER"]

def test_zero_based_ports_connect_and_readback():
    tree=Tree(); assert list_block_ports(tree,"M1")["ports"][0]["name"] == "F(IN)"
    result=connect_stream(tree,"M1","F1","F(IN)"); assert result["connected_streams"] == ["F1"]
    with pytest.raises(OperationError): connect_stream(tree,"M1","F1","BAD")
