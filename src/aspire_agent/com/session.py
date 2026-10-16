from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class Session:
    document: Any
    checkpoint: Callable[[str | None], dict[str, Any]] | None = None
    close: Callable[[bool], None] | None = None

class SessionStore:
    def __init__(self, factory: Callable[[str | None, bool], Any]):
        self.factory = factory
        self.sessions: dict[str, Session] = {}

    def start(self, key: str, initial_bkp: str | None, show_gui: bool) -> Session:
        if key not in self.sessions:
            self.sessions[key] = Session(self.factory(initial_bkp, show_gui))
        return self.sessions[key]

    def get(self, key: str) -> Session:
        if key not in self.sessions:
            raise KeyError(f"Unknown session: {key}")
        return self.sessions[key]

    def remove(self, key: str, save: bool) -> None:
        session = self.get(key)
        if session.close:
            session.close(save)
        del self.sessions[key]
