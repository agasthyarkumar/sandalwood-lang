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
    UnaryExpression,
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

    def _parse_function_statement(self) -> VariableDeclaration | PrintStatement | IfStatement | ReturnStatement | ExpressionStatement:
        if self._is_keyword("idhu"):
            return self._parse_variable_declaration()
        if self._is_keyword("dialogue"):
            return self._parse_print_statement()
        if self._is_keyword("nodona"):
            return self._parse_if_statement()
        if self._is_keyword("packup"):
            return self._parse_return_statement()
        return ExpressionStatement(expression=self._parse_expression())

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

    def _parse_if_statement(self) -> IfStatement:
        self._consume_keyword("nodona")
        self._consume_delimiter("(", "Expected '(' after 'nodona'")
        condition = self._parse_expression()
        self._consume_delimiter(")", "Expected ')' after nodona condition")
        then_body = self._parse_block()

        elif_branches: list[tuple[Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression, list]] = []
        while self._is_keyword("illandre"):
            self._consume_keyword("illandre")
            self._consume_delimiter("(", "Expected '(' after 'illandre'")
            branch_condition = self._parse_expression()
            self._consume_delimiter(")", "Expected ')' after illandre condition")
            elif_branches.append((branch_condition, self._parse_block()))

        else_body = None
        if self._is_keyword("climax"):
            self._consume_keyword("climax")
            else_body = self._parse_block()

        return IfStatement(condition=condition, then_body=then_body, elif_branches=elif_branches, else_body=else_body)

    def _parse_return_statement(self) -> ReturnStatement:
        self._consume_keyword("packup")
        if self._check(TokenType.NEWLINE) or self._check_delimiter("}") or self._is_at_end():
            return ReturnStatement(value=None)
        return ReturnStatement(value=self._parse_expression())

    def _parse_block(self) -> list[VariableDeclaration | PrintStatement | IfStatement | ReturnStatement | ExpressionStatement]:
        self._consume_delimiter("{", "Expected '{' before block")
        self._consume_newlines()
        body = []
        while not self._check_delimiter("}"):
            if self._is_at_end():
                token = self._peek()
                raise ParserError("Unterminated block", token.line, token.column)
            body.append(self._parse_function_statement())
            self._consume_newlines()
        self._consume_delimiter("}", "Expected '}' after block")
        self._consume_newlines()
        return body

    def _parse_expression(self) -> Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression:
        return self._parse_logical_or()

    def _parse_logical_or(self) -> Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression:
        expression = self._parse_logical_and()
        while self._match_operator("||"):
            expression = BinaryExpression(left=expression, operator="||", right=self._parse_logical_and())
        return expression

    def _parse_logical_and(self) -> Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression:
        expression = self._parse_equality()
        while self._match_operator("&&"):
            expression = BinaryExpression(left=expression, operator="&&", right=self._parse_equality())
        return expression

    def _parse_equality(self) -> Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression:
        expression = self._parse_comparison()
        while True:
            if self._match_operator("=="):
                expression = BinaryExpression(left=expression, operator="==", right=self._parse_comparison())
                continue
            if self._match_operator("!="):
                expression = BinaryExpression(left=expression, operator="!=", right=self._parse_comparison())
                continue
            break
        return expression

    def _parse_comparison(self) -> Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression:
        expression = self._parse_term()
        while True:
            if self._match_operator(">="):
                expression = BinaryExpression(left=expression, operator=">=", right=self._parse_term())
                continue
            if self._match_operator("<="):
                expression = BinaryExpression(left=expression, operator="<=", right=self._parse_term())
                continue
            if self._match_operator(">"):
                expression = BinaryExpression(left=expression, operator=">", right=self._parse_term())
                continue
            if self._match_operator("<"):
                expression = BinaryExpression(left=expression, operator="<", right=self._parse_term())
                continue
            break
        return expression

    def _parse_term(self) -> Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression:
        expression = self._parse_factor()
        while True:
            if self._match_operator("+"):
                expression = BinaryExpression(left=expression, operator="+", right=self._parse_factor())
                continue
            if self._match_operator("-"):
                expression = BinaryExpression(left=expression, operator="-", right=self._parse_factor())
                continue
            break
        return expression

    def _parse_factor(self) -> Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression:
        expression = self._parse_unary()
        while True:
            if self._match_operator("*"):
                expression = BinaryExpression(left=expression, operator="*", right=self._parse_unary())
                continue
            if self._match_operator("//"):
                expression = BinaryExpression(left=expression, operator="//", right=self._parse_unary())
                continue
            if self._match_operator("/"):
                expression = BinaryExpression(left=expression, operator="/", right=self._parse_unary())
                continue
            if self._match_operator("%"):
                expression = BinaryExpression(left=expression, operator="%", right=self._parse_unary())
                continue
            break
        return expression

    def _parse_unary(self) -> Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression:
        if self._match_operator("!"):
            return UnaryExpression(operator="!", operand=self._parse_unary())
        if self._match_operator("-"):
            return UnaryExpression(operator="-", operand=self._parse_unary())
        return self._parse_call()

    def _parse_call(self) -> Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression:
        expression = self._parse_primary()
        while self._match_delimiter("("):
            arguments: list[Identifier | Literal | UnaryExpression | BinaryExpression | CallExpression] = []
            if not self._check_delimiter(")"):
                while True:
                    arguments.append(self._parse_expression())
                    if not self._match_delimiter(","):
                        break
            self._consume_delimiter(")", "Expected ')' after arguments")
            expression = CallExpression(callee=expression, arguments=arguments)
        return expression

    def _parse_primary(self) -> Identifier | Literal:
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
        if token.token_type == TokenType.DELIMITER and token.value == "(":
            self._advance()
            expression = self._parse_expression()
            self._consume_delimiter(")", "Expected ')' after expression")
            return expression
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

    def _match_operator(self, operator: str) -> bool:
        if self._is_at_end():
            return False
        token = self._peek()
        if token.token_type != TokenType.OPERATOR or token.value != operator:
            return False
        self._advance()
        return True

    def _check_delimiter(self, delimiter: str) -> bool:
        if self._is_at_end():
            return False
        token = self._peek()
        return token.token_type == TokenType.DELIMITER and token.value == delimiter

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().token_type == token_type

    def _consume_newlines(self) -> None:
        while self._match(TokenType.NEWLINE):
            continue

    def _is_keyword(self, keyword: str) -> bool:
        if self._is_at_end():
            return False
        token = self._peek()
        return token.token_type == TokenType.KEYWORD and token.value == keyword
