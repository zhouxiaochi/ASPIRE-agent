from __future__ import annotations
import json
from .llm import LLMAdapter, load_resource
from .models import ChemicalDiagnosis, ChemicalReasoningInput

class ChemicalReasoningAgent:
    ALLOWED = ("components", "feed-state", "topology", "mixer-pressure-energy", "heater-mode-spec", "stream-kind", "target-readback")
    def __init__(self, adapter: LLMAdapter | None = None): self.adapter = adapter
    @staticmethod
    def should_run(value: ChemicalReasoningInput) -> bool:
        return any(issue.physical for issue in value.audit.issues)
    def diagnose(self, value: ChemicalReasoningInput) -> ChemicalDiagnosis | None:
        if not self.should_run(value): return None
        if self.adapter:
            try:
                raw = json.loads(self.adapter.complete(load_resource("chemical_reasoning.md"), json.dumps(value.as_dict())))
                category = raw.get("category", "target-readback")
                if category in self.ALLOWED:
                    return ChemicalDiagnosis(category, str(raw["finding"]), str(raw["action"]), "model")
            except (ValueError, KeyError, TypeError): pass
        text = " ".join(issue.message.lower() for issue in value.audit.issues)
        choices = (("component", "components"), ("feed", "feed-state"), ("topolog", "topology"), ("pressure", "mixer-pressure-energy"), ("energy", "mixer-pressure-energy"), ("heater", "heater-mode-spec"), ("heat stream", "stream-kind"))
        category = next((result for token, result in choices if token in text), "target-readback")
        actions = {
            "components": "Verify every requested registry component is visibly landed.",
            "feed-state": "Verify feed temperature, pressure, basis, and component flows.",
            "topology": "Read live ports and verify material and heat stream roles.",
            "mixer-pressure-energy": "Verify MIXER pressure units and energy setting.",
            "heater-mode-spec": "Verify HEATER mode and its matching active values.",
            "stream-kind": "Verify material streams and heat streams use matching ports.",
            "target-readback": "Read the requested target from the trusted current run.",
        }
        return ChemicalDiagnosis(category, "Physical configuration evidence is incomplete.", actions[category])
