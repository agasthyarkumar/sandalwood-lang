from __future__ import annotations

from sandalwood.ast.nodes import (
    FunctionDefinition,
    Identifier,
    Literal,
    PrintStatement,
    Program,
    Statement,
    VariableDeclaration,
)
from sandalwood.errors.exceptions import RuntimeSandalwoodError
from sandalwood.runtime.environment import Environment


class Interpreter:
    """Minimal executable interpreter for Sandalwood foundations."""

    def __init__(self, environment: Environment | None = None) -> None:
        self.environment = environment or Environment()
        self.functions: dict[str, FunctionDefinition] = {}

    def interpret(self, program: Program) -> None:
        for statement in program.statements:
            if not isinstance(statement, FunctionDefinition):
                raise RuntimeSandalwoodError("Only function definitions are allowed at top level")
            self.functions[statement.name] = statement

        main_function = self.functions.get("main")
        if main_function is None:
            raise RuntimeSandalwoodError("Missing entry function: scene main()")
        self._execute_function(main_function)

    def _execute_function(self, function: FunctionDefinition) -> None:
        if function.parameters:
            raise RuntimeSandalwoodError("scene main() cannot declare parameters in this version")

        self.environment.push_scope()
        try:
            for statement in function.body:
                self._execute_statement(statement)
        finally:
            self.environment.pop_scope()

    def _execute_statement(self, statement: Statement) -> None:
        if isinstance(statement, VariableDeclaration):
            self.environment.define(statement.name, self._evaluate_expression(statement.value))
            return
        if isinstance(statement, PrintStatement):
            print(self._evaluate_expression(statement.value))
            return
        raise RuntimeSandalwoodError(f"Unsupported statement type: {type(statement).__name__}")

    def _evaluate_expression(self, expression: Identifier | Literal) -> object:
        if isinstance(expression, Literal):
            return expression.value
        if isinstance(expression, Identifier):
            try:
                return self.environment.resolve(expression.name)
            except NameError as exc:
                raise RuntimeSandalwoodError(str(exc)) from exc
        raise RuntimeSandalwoodError(f"Unsupported expression type: {type(expression).__name__}")
