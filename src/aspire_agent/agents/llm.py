from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

class LLMAdapter(Protocol):
    def complete(self, system: str, user: str) -> str: ...

@dataclass
class OpenAIAdapter:
    model: str
    base_url: str | None = None

    def complete(self, system: str, user: str) -> str:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install aspire-agent[llm] to call a model") from exc
        client = OpenAI(base_url=self.base_url)
        response = client.chat.completions.create(model=self.model, messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        return response.choices[0].message.content or ""

@dataclass
class StaticAdapter:
    response: str
    def complete(self, system: str, user: str) -> str:
        return self.response

def load_resource(name: str) -> str:
    return (Path(__file__).parents[1] / "resources" / name).read_text(encoding="utf-8")
