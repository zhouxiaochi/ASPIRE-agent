from __future__ import annotations
from importlib.resources import files

SKILL_NAMES = ("mixer", "heater", "common-components")

def list_skills() -> tuple[str, ...]:
    return SKILL_NAMES

def load_skill(name: str) -> str:
    if name not in SKILL_NAMES:
        raise KeyError(f"Unknown ASIPRE skill: {name}")
    return files("asipre_agent.resources.skills").joinpath(f"{name}.md").read_text(encoding="utf-8")
