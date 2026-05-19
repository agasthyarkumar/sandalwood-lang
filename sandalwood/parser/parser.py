from __future__ import annotations

from sandalwood.ast.nodes import PlaceholderStatement, Program
from sandalwood.errors.exceptions import ParserError
from sandalwood.lexer.token import Token, TokenType


class Parser:
    """Builds placeholder AST nodes from token streams.

    This parser is intentionally minimal so new grammar rules can be added
    incrementally without large rewrites.
    """

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = 0

    def parse(self) -> Program:
        program = Program()
        while not self._is_at_end():
            if self._match(TokenType.NEWLINE):
                continue
            program.statements.append(self._parse_statement())
        return program

    def _parse_statement(self) -> PlaceholderStatement:
        values: list[str] = []
        while not self._is_at_end() and self._peek().token_type not in {
            TokenType.NEWLINE,
            TokenType.EOF,
        }:
            values.append(self._advance().value)
        self._match(TokenType.NEWLINE)
        if not values:
            raise ParserError("Empty statement")
        return PlaceholderStatement(tokens=values)

    def _match(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        if self._peek().token_type != token_type:
            return False
        self.position += 1
        return True

    def _peek(self) -> Token:
        return self.tokens[self.position]

    def _advance(self) -> Token:
        token = self.tokens[self.position]
        self.position += 1
        return token

    def _is_at_end(self) -> bool:
        return self._peek().token_type == TokenType.EOF
