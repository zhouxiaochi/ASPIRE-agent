from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
class BlockKind(str, Enum): MIXER="MIXER"; HEATER="HEATER"
class HeaterMode(str, Enum): TP="TP"; PV="PV"; PD="PD"
@dataclass(frozen=True)
class SessionRequest:
    task_hash: str; initial_bkp: str | None=None; show_gui: bool | None=None
@dataclass(frozen=True)
class OperationRequest:
    task_hash: str; operation: str; parameters: Mapping[str,Any]=field(default_factory=dict)
@dataclass(frozen=True)
class Port:
    name: str; direction: str; kind: str="MATERIAL"; connected_streams: tuple[str,...]=()
@dataclass(frozen=True)
class PreflightReport:
    complete: bool; completion: Mapping[str,Any]; next_status: Mapping[str,Any]
@dataclass(frozen=True)
class EvidenceBundle:
    run: Mapping[str,Any]; completion: Mapping[str,Any]; next_status: Mapping[str,Any]; export: Mapping[str,Any]
