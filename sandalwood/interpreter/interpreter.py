from __future__ import annotations

from sandalwood.ast.nodes import (
    BinaryExpression,
    CallExpression,
    ExpressionStatement,
    FunctionDefinition,
    IfStatement,
    Identifier,
    Literal,
    PrintStatement,
    Program,
    ReturnStatement,
    Statement,
    UnaryExpression,
    VariableDeclaration,
)
from sandalwood.errors.exceptions import RuntimeSandalwoodError
from sandalwood.runtime.environment import Environment


class _ReturnSignal(Exception):
    def __init__(self, value: object) -> None:
        self.value = value


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
        self._execute_function(main_function, [])

    def _execute_function(self, function: FunctionDefinition, arguments: list[object]) -> object:
        if len(function.parameters) != len(arguments):
            raise RuntimeSandalwoodError(
                f"Function '{function.name}' expects {len(function.parameters)} argument(s), got {len(arguments)}"
            )

        self.environment.push_scope()
        try:
            for name, value in zip(function.parameters, arguments):
                self.environment.define(name, value)
            for statement in function.body:
                self._execute_statement(statement)
        except _ReturnSignal as signal:
            return signal.value
        finally:
            self.environment.pop_scope()
        return None

    def _execute_statement(self, statement: Statement) -> None:
        if isinstance(statement, VariableDeclaration):
            self.environment.define(statement.name, self._evaluate_expression(statement.value))
            return
        if isinstance(statement, PrintStatement):
            print(self._evaluate_expression(statement.value))
            return
        if isinstance(statement, IfStatement):
            if self._is_truthy(self._evaluate_expression(statement.condition)):
                self._execute_block(statement.then_body)
                return
            for condition, body in statement.elif_branches:
                if self._is_truthy(self._evaluate_expression(condition)):
                    self._execute_block(body)
                    return
            if statement.else_body is not None:
                self._execute_block(statement.else_body)
            return
        if isinstance(statement, ReturnStatement):
            value = None if statement.value is None else self._evaluate_expression(statement.value)
            raise _ReturnSignal(value)
        if isinstance(statement, ExpressionStatement):
            self._evaluate_expression(statement.expression)
            return
        raise RuntimeSandalwoodError(f"Unsupported statement type: {type(statement).__name__}")

    def _execute_block(self, statements: list[Statement]) -> None:
        self.environment.push_scope()
        try:
            for statement in statements:
                self._execute_statement(statement)
        finally:
            self.environment.pop_scope()

    def _evaluate_expression(self, expression: Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression) -> object:
        if isinstance(expression, Literal):
            return expression.value
        if isinstance(expression, Identifier):
            try:
                return self.environment.resolve(expression.name)
            except NameError as exc:
                raise RuntimeSandalwoodError(str(exc)) from exc
        if isinstance(expression, UnaryExpression):
            operand = self._evaluate_expression(expression.operand)
            if expression.operator == "!":
                return not self._is_truthy(operand)
            if expression.operator == "-":
                return -operand
            raise RuntimeSandalwoodError(f"Unsupported unary operator: {expression.operator}")
        if isinstance(expression, BinaryExpression):
            if expression.operator == "&&":
                left = self._evaluate_expression(expression.left)
                if not self._is_truthy(left):
                    return False
                return self._is_truthy(self._evaluate_expression(expression.right))
            if expression.operator == "||":
                left = self._evaluate_expression(expression.left)
                if self._is_truthy(left):
                    return True
                return self._is_truthy(self._evaluate_expression(expression.right))

            left = self._evaluate_expression(expression.left)
            right = self._evaluate_expression(expression.right)
            if expression.operator == "+":
                return left + right
            if expression.operator == "-":
                return left - right
            if expression.operator == "*":
                return left * right
            if expression.operator == "/":
                return left / right
            if expression.operator == "//":
                return left // right
            if expression.operator == "%":
                return left % right
            if expression.operator == "==":
                return left == right
            if expression.operator == "!=":
                return left != right
            if expression.operator == ">":
                return left > right
            if expression.operator == "<":
                return left < right
            if expression.operator == ">=":
                return left >= right
            if expression.operator == "<=":
                return left <= right
            raise RuntimeSandalwoodError(f"Unsupported binary operator: {expression.operator}")
        if isinstance(expression, CallExpression):
            if not isinstance(expression.callee, Identifier):
                raise RuntimeSandalwoodError("Only named function calls are supported")
            callee_name = expression.callee.name
            arguments = [self._evaluate_expression(argument) for argument in expression.arguments]
            function = self.functions.get(callee_name)
            if function is not None:
                return self._execute_function(function, arguments)
            if callee_name == "size":
                if len(arguments) != 1:
                    raise RuntimeSandalwoodError("size() expects 1 argument")
                return len(arguments[0])
            raise RuntimeSandalwoodError(f"Undefined function: {callee_name}")
        raise RuntimeSandalwoodError(f"Unsupported expression type: {type(expression).__name__}")

    @staticmethod
    def _is_truthy(value: object) -> bool:
        return bool(value)
