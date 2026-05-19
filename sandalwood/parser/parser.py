from __future__ import annotations

from sandalwood.ast.nodes import (
    FunctionDefinition,
    Identifier,
    Literal,
    PrintStatement,
    Program,
    VariableDeclaration,
)
from sandalwood.errors.exceptions import ParserError
from sandalwood.lexer.token import Token, TokenType


class Parser:
    """Builds a minimal executable AST from token streams."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = 0

    def parse(self) -> Program:
        program = Program()
        while not self._is_at_end():
            self._consume_newlines()
            if self._is_at_end():
                break
            program.statements.append(self._parse_top_level_statement())
        return program

    def _parse_top_level_statement(self) -> FunctionDefinition:
        if self._is_keyword("scene"):
            return self._parse_function_definition()
        raise ParserError(f"Unexpected top-level token: {self._peek().value}", self._peek().line, self._peek().column)

    def _parse_function_definition(self) -> FunctionDefinition:
        scene_token = self._consume_keyword("scene")
        name_token = self._consume(TokenType.IDENTIFIER, "Expected function name after 'scene'")
        self._consume_delimiter("(", "Expected '(' after function name")
        parameters = self._parse_parameters()
        self._consume_delimiter(")", "Expected ')' after parameter list")
        self._consume_delimiter("{", "Expected '{' before function body")
        self._consume_newlines()

        body = []
        while not self._check_delimiter("}"):
            if self._is_at_end():
                raise ParserError("Unterminated function body", scene_token.line, scene_token.column)
            body.append(self._parse_function_statement())
            self._consume_newlines()

        self._consume_delimiter("}", "Expected '}' after function body")
        self._consume_newlines()
        return FunctionDefinition(name=name_token.value, parameters=parameters, body=body)

    def _parse_parameters(self) -> list[str]:
        parameters: list[str] = []
        if self._check_delimiter(")"):
            return parameters

        while True:
            token = self._consume(TokenType.IDENTIFIER, "Expected parameter name")
            parameters.append(token.value)
            if not self._match_delimiter(","):
                break
        return parameters

    def _parse_function_statement(self) -> VariableDeclaration | PrintStatement:
        if self._is_keyword("idhu"):
            return self._parse_variable_declaration()
        if self._is_keyword("dialogue"):
            return self._parse_print_statement()
        raise ParserError(f"Unsupported statement: {self._peek().value}", self._peek().line, self._peek().column)

    def _parse_variable_declaration(self) -> VariableDeclaration:
        self._consume_keyword("idhu")
        name_token = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'idhu'")
        self._consume_operator("=", "Expected '=' after variable name")
        value = self._parse_expression()
        return VariableDeclaration(name=name_token.value, value=value)

    def _parse_print_statement(self) -> PrintStatement:
        self._consume_keyword("dialogue")
        self._consume_delimiter("(", "Expected '(' after 'dialogue'")
        value = self._parse_expression()
        self._consume_delimiter(")", "Expected ')' after dialogue argument")
        return PrintStatement(value=value)

    def _parse_expression(self) -> Identifier | Literal:
        token = self._peek()
        if token.token_type == TokenType.STRING:
            return Literal(value=self._advance().value)
        if token.token_type == TokenType.INTEGER:
            return Literal(value=int(self._advance().value))
        if token.token_type == TokenType.FLOAT:
            return Literal(value=float(self._advance().value))
        if token.token_type == TokenType.KEYWORD and token.value in {"blockbuster", "flop"}:
            self._advance()
            return Literal(value=token.value == "blockbuster")
        if token.token_type == TokenType.IDENTIFIER:
            return Identifier(name=self._advance().value)
        raise ParserError(f"Unsupported expression: {token.value}", token.line, token.column)

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

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._is_at_end() or self._peek().token_type != token_type:
            token = self._peek()
            raise ParserError(message, token.line, token.column)
        return self._advance()

    def _consume_keyword(self, keyword: str) -> Token:
        token = self._peek()
        if token.token_type != TokenType.KEYWORD or token.value != keyword:
            raise ParserError(f"Expected keyword '{keyword}'", token.line, token.column)
        return self._advance()

    def _consume_operator(self, operator: str, message: str) -> Token:
        token = self._peek()
        if token.token_type != TokenType.OPERATOR or token.value != operator:
            raise ParserError(message, token.line, token.column)
        return self._advance()

    def _consume_delimiter(self, delimiter: str, message: str) -> Token:
        token = self._peek()
        if token.token_type != TokenType.DELIMITER or token.value != delimiter:
            raise ParserError(message, token.line, token.column)
        return self._advance()

    def _match_delimiter(self, delimiter: str) -> bool:
        if self._is_at_end():
            return False
        token = self._peek()
        if token.token_type != TokenType.DELIMITER or token.value != delimiter:
            return False
        self._advance()
        return True

    def _check_delimiter(self, delimiter: str) -> bool:
        if self._is_at_end():
            return False
        token = self._peek()
        return token.token_type == TokenType.DELIMITER and token.value == delimiter

    def _consume_newlines(self) -> None:
        while self._match(TokenType.NEWLINE):
            continue

    def _is_keyword(self, keyword: str) -> bool:
        if self._is_at_end():
            return False
        token = self._peek()
        return token.token_type == TokenType.KEYWORD and token.value == keyword
