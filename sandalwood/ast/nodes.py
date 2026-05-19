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
class PlaceholderStatement(Statement):
    tokens: list[str]


@dataclass(slots=True)
class Identifier(Expression):
    name: str


@dataclass(slots=True)
class Literal(Expression):
    value: str
