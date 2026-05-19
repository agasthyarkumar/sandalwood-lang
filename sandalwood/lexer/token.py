from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    OPERATOR = auto()
    DELIMITER = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass(slots=True)
class Token:
    token_type: TokenType
    value: str
    line: int
    column: int
