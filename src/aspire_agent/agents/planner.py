from __future__ import annotations
import re
from typing import Any
from .models import StagePlan, TaskPlan

_SKILLS = ("common-components", "mixer", "heater")
_BLOCKED = re.compile(r"\b(reactor|rstoic|rplug|rcstr|requil|rgibbs|rbatch|column|radfrac|dstwu|petrofrac|multifrac|separator|sep2?|flash|splitter|fsplit|compressor|compr|pump|turbine|valve|pipe|heatx|mheatx|cooler|absorber|stripper|distillation|kinetic|equilibrium)\w*\b|\b(heat[ -]?exchanger|design[ -]?spec|sensitivity|optimization|recycle|analysis)\b", re.I)

class PlannerAgent:
    """Build a deterministic, serializable plan inside the public domain."""
    def plan(self, request: str, manifest: dict[str, Any] | None = None, *, thesis: bool = False) -> TaskPlan:
        manifest = manifest or {"request": request}
        matches = tuple(sorted({m.group(0).lower() for m in _BLOCKED.finditer(request)}))
        skills = ["common-components"]
        lowered = request.lower()
        if "mixer" in lowered: skills.append("mixer")
        if "heater" in lowered: skills.append("heater")
        raw = manifest.get("stages") if thesis else None
        raw = raw or [{"name": "task" if not thesis else "workspace", "entry": "generated_task.py" if not thesis else "workflow.py"}]
        names = {str(item["name"]) for item in raw}
        stages = []
        previous: tuple[str, ...] = ()
        for item in raw:
            name = str(item["name"])
            supplied = item.get("dependencies", item.get("depends_on", previous))
            dependencies = (supplied,) if isinstance(supplied, str) else tuple(map(str, supplied or ()))
            unknown = [value for value in dependencies if value not in names]
            if unknown: matches += tuple(f"unknown dependency {value}" for value in unknown)
            stages.append(StagePlan(name, str(item.get("entry", "workflow.py")), dependencies, tuple(skills)))
            previous = (name,)
        return TaskPlan(request, tuple(stages), tuple(skills), not matches, matches)
