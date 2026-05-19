from __future__ import annotations

from dataclasses import dataclass

from sandalwood.errors.exceptions import LexerError
from sandalwood.lexer.token import Token, TokenType
from sandalwood.utils.config_loader import load_config


@dataclass(slots=True)
class LexerConfig:
    keywords: set[str]
    operators: list[str]
    delimiters: set[str]

    @classmethod
    def from_files(cls) -> "LexerConfig":
        keyword_data = load_config("keywords.json")
        operator_data = load_config("operators.json")
        operators = sorted(operator_data["operators"], key=len, reverse=True)
        return cls(
            keywords=set(keyword_data["keywords"]),
            operators=operators,
            delimiters=set(operator_data["delimiters"]),
        )


class Lexer:
    """Converts Sandalwood source code into a token stream."""

    def __init__(self, source: str, config: LexerConfig | None = None) -> None:
        self.source = source
        self.config = config or LexerConfig.from_files()
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while not self._is_at_end():
            current = self._peek()
            if current in {" ", "\t", "\r"}:
                self._advance()
                continue
            if current == "\n":
                tokens.append(Token(TokenType.NEWLINE, "\\n", self.line, self.column))
                self._advance_line()
                continue
            if current.isalpha() or current == "_":
                tokens.append(self._identifier_or_keyword())
                continue
            if current.isdigit():
                tokens.append(self._number_literal())
                continue
            if current in {'"', "'"}:
                tokens.append(self._string_literal())
                continue
            operator = self._match_operator()
            if operator is not None:
                tokens.append(operator)
                continue
            if current in self.config.delimiters:
                tokens.append(Token(TokenType.DELIMITER, current, self.line, self.column))
                self._advance()
                continue
            raise LexerError(f"Unexpected character: {current}", self.line, self.column)
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    def _identifier_or_keyword(self) -> Token:
        start_line, start_column = self.line, self.column
        buffer: list[str] = []
        while not self._is_at_end() and (self._peek().isalnum() or self._peek() == "_"):
            buffer.append(self._advance())
        value = "".join(buffer)
        token_type = TokenType.KEYWORD if value in self.config.keywords else TokenType.IDENTIFIER
        return Token(token_type, value, start_line, start_column)

    def _number_literal(self) -> Token:
        start_line, start_column = self.line, self.column
        buffer: list[str] = []
        has_decimal = False
        while not self._is_at_end():
            char = self._peek()
            if char.isdigit():
                buffer.append(self._advance())
                continue
            if char == "." and not has_decimal:
                has_decimal = True
                buffer.append(self._advance())
                continue
            break
        token_type = TokenType.FLOAT if has_decimal else TokenType.INTEGER
        return Token(token_type, "".join(buffer), start_line, start_column)

    def _string_literal(self) -> Token:
        start_line, start_column = self.line, self.column
        quote = self._advance()
        buffer: list[str] = []
        while not self._is_at_end() and self._peek() != quote:
            if self._peek() == "\n":
                raise LexerError("Unterminated string literal", start_line, start_column)
            buffer.append(self._advance())
        if self._is_at_end():
            raise LexerError("Unterminated string literal", start_line, start_column)
        self._advance()
        return Token(TokenType.STRING, "".join(buffer), start_line, start_column)

    def _match_operator(self) -> Token | None:
        for operator in self.config.operators:
            if self.source.startswith(operator, self.position):
                token = Token(TokenType.OPERATOR, operator, self.line, self.column)
                for _ in operator:
                    self._advance()
                return token
        return None

    def _peek(self) -> str:
        return self.source[self.position]

    def _is_at_end(self) -> bool:
        return self.position >= len(self.source)

    def _advance(self) -> str:
        char = self.source[self.position]
        self.position += 1
        self.column += 1
        return char

    def _advance_line(self) -> None:
        self.position += 1
        self.line += 1
        self.column = 1
