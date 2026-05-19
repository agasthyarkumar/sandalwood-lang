from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ASTNode:
    """Base AST node type."""


@dataclass(slots=True)
class Statement(ASTNode):
    """Base statement node."""


@dataclass(slots=True)
class Expression(ASTNode):
    """Base expression node."""


@dataclass(slots=True)
class Program(ASTNode):
    statements: list[Statement] = field(default_factory=list)


@dataclass(slots=True)
class FunctionDefinition(Statement):
    name: str
    parameters: list[str]
    body: list[Statement]


@dataclass(slots=True)
class VariableDeclaration(Statement):
    name: str
    value: "Expression"


@dataclass(slots=True)
class PrintStatement(Statement):
    value: "Expression"


@dataclass(slots=True)
class ReturnStatement(Statement):
    value: "Expression | None"


@dataclass(slots=True)
class IfStatement(Statement):
    condition: "Expression"
    then_body: list[Statement]
    elif_branches: list[tuple["Expression", list[Statement]]]
    else_body: list[Statement] | None


@dataclass(slots=True)
class ExpressionStatement(Statement):
    expression: "Expression"


@dataclass(slots=True)
class Identifier(Expression):
    name: str


@dataclass(slots=True)
class Literal(Expression):
    value: object


@dataclass(slots=True)
class UnaryExpression(Expression):
    operator: str
    operand: "Expression"


@dataclass(slots=True)
class BinaryExpression(Expression):
    left: "Expression"
    operator: str
    right: "Expression"


@dataclass(slots=True)
class CallExpression(Expression):
    callee: "Expression"
    arguments: list["Expression"]
