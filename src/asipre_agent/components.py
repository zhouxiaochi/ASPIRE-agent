from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Compound:
    name: str
    aspen_id: str
    cas: str
    formula: str
    aliases: tuple[str, ...] = ()

_COMPOUNDS = (
    Compound("water", "WATER", "7732-18-5", "H2O", ("steam",)),
    Compound("methanol", "MEOH", "67-56-1", "CH4O", ("methyl alcohol", "METHANOL")),
    Compound("ethanol", "ETHANOL", "64-17-5", "C2H6O", ("ethyl alcohol",)),
    Compound("methane", "METHANE", "74-82-8", "CH4", ("natural gas methane",)),
    Compound("carbon dioxide", "CO2", "124-38-9", "CO2", ("carbonic gas",)),
    Compound("hydrogen", "HYDROGEN", "1333-74-0", "H2", ("molecular hydrogen",)),
    Compound("nitrogen", "NITROGEN", "7727-37-9", "N2", ("molecular nitrogen",)),
    Compound("ammonia", "AMMONIA", "7664-41-7", "NH3", ("azane",)),
    Compound("n-hexane", "N-HEXANE", "110-54-3", "C6H14", ("hexane", "normal hexane")),
    Compound("acetic acid", "ACETIC-ACID", "64-19-7", "C2H4O2", ("ethanoic acid",)),
)
COMMON_COMPOUNDS = _COMPOUNDS

class CompoundRegistry:
    def __init__(self, compounds: tuple[Compound, ...] = _COMPOUNDS):
        self.compounds = compounds
        self._keys: dict[str, Compound] = {}
        for item in compounds:
            for key in (item.name, item.aspen_id, item.cas, item.formula, *item.aliases):
                self._keys[key.casefold()] = item

    def resolve(self, value: str) -> Compound:
        try:
            return self._keys[value.strip().casefold()]
        except KeyError as exc:
            raise KeyError(f"Unknown public compound: {value}") from exc

    def cas_numbers(self, names: list[str]) -> list[str]:
        return [self.resolve(name).cas for name in names]
