import re
from importlib.resources import files
from pathlib import Path
from asipre_agent.skills import list_skills, load_skill
ROOT=Path(__file__).parents[1]
EXPECTED=("mixer","heater","common-components")
CJK=re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

def test_all_skills_discoverable_and_packaged():
    assert list_skills()==EXPECTED
    for name in EXPECTED:
        source=(ROOT/"skills"/name/"SKILL.md").read_text(encoding="utf-8")
        assert load_skill(name)==source
        packaged=files("asipre_agent.resources.skills").joinpath(f"{name}.md")
        assert packaged.is_file()

def test_skills_are_english_and_scoped():
    texts={name:load_skill(name) for name in EXPECTED}
    assert all(not CJK.search(text) for text in texts.values())
    mixer=texts["mixer"]
    assert "ENERGY_BAL" in mixer and "YES" in mixer and "NO" in mixer and "F(IN)" in mixer and "P(OUT)" in mixer
    assert "HEATER" not in mixer and "SPEC_OPT" not in mixer
    heater=texts["heater"]
    assert all(token in heater for token in ("HEATER","TP","PV","PD","set_spec_opt","set_temp","set_pres","set_vfrac","set_duty"))
    assert "MIXER" not in heater and "ENERGY_BAL" not in heater
    components=texts["common-components"]
    assert "add_components_by_cas" in components and "inspect_component_table" in components
    assert "MIXER" not in components and "HEATER" not in components

def test_component_skill_exact_registry_rows():
    text=load_skill("common-components")
    expected=(
        ("water","WATER","7732-18-5","H2O"),("methanol","MEOH","67-56-1","CH4O"),
        ("ethanol","ETHANOL","64-17-5","C2H6O"),("methane","METHANE","74-82-8","CH4"),
        ("carbon dioxide","CO2","124-38-9","CO2"),("hydrogen","HYDROGEN","1333-74-0","H2"),
        ("nitrogen","NITROGEN","7727-37-9","N2"),("ammonia","AMMONIA","7664-41-7","NH3"),
        ("n-hexane","N-HEXANE","110-54-3","C6H14"),("acetic acid","ACETIC-ACID","64-19-7","C2H4O2"),
    )
    for row in expected: assert all(value in text for value in row)
    assert text.count("|",text.index("| water |"))>0


def test_unrelated_skill_names_cannot_load():
    import pytest
    for name in ("other", "mixer/extra", "../mixer"):
        with pytest.raises(KeyError): load_skill(name)
