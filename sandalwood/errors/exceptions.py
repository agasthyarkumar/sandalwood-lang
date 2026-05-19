from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SandalwoodError(Exception):
    message: str
    line: int | None = None
    column: int | None = None

    def __str__(self) -> str:
        if self.line is None or self.column is None:
            return self.message
        return f"{self.message} (line={self.line}, column={self.column})"


class LexerError(SandalwoodError):
    """Raised when lexing fails."""


class ParserError(SandalwoodError):
    """Raised when parsing fails."""


class RuntimeSandalwoodError(SandalwoodError):
    """Raised when runtime execution fails."""
