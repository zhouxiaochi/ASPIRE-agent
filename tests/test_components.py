import pytest
from aspire_agent.components import COMMON_COMPOUNDS, CompoundRegistry

def test_registry_has_exact_public_compounds():
    assert len(COMMON_COMPOUNDS) == 10
    assert {c.name for c in COMMON_COMPOUNDS} == {"water", "methanol", "ethanol", "methane", "carbon dioxide", "hydrogen", "nitrogen", "ammonia", "n-hexane", "acetic acid"}
    registry = CompoundRegistry()
    assert registry.resolve("ethyl alcohol").cas == "64-17-5"
    assert registry.resolve("CO2").name == "carbon dioxide"
    assert registry.resolve("methanol").aspen_id == "MEOH"
    assert registry.resolve("METHANOL").aspen_id == "MEOH"
    with pytest.raises(KeyError): registry.resolve("unknown")
