from __future__ import annotations

from sandalwood.ast.nodes import Program
from sandalwood.runtime.environment import Environment


class Interpreter:
    """Minimal interpreter skeleton for future AST execution."""

    def __init__(self, environment: Environment | None = None) -> None:
        self.environment = environment or Environment()

    def interpret(self, program: Program) -> None:
        for _statement in program.statements:
            # Placeholder: statement execution will be implemented in future phases.
            pass
