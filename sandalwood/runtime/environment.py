from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Environment:
    """Runtime environment with scope stack support."""

    scopes: list[dict[str, Any]] = field(default_factory=lambda: [{}])

    def define(self, name: str, value: Any) -> None:
        self.scopes[-1][name] = value

    def assign(self, name: str, value: Any) -> bool:
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return True
        return False

    def resolve(self, name: str) -> Any:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Undefined name: {name}")

    def push_scope(self) -> None:
        self.scopes.append({})

    def pop_scope(self) -> None:
        if len(self.scopes) == 1:
            raise RuntimeError("Cannot pop global scope")
        self.scopes.pop()
