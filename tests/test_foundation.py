from __future__ import annotations

import io
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
import tomllib
import unittest

from sandalwood.ast.nodes import BinaryExpression, IfStatement, ReturnStatement, VariableDeclaration
from sandalwood.cli.main import run_file
from sandalwood.errors.exceptions import LexerError, ParserError, RuntimeSandalwoodError
from sandalwood.interpreter.interpreter import Interpreter
from sandalwood.lexer.lexer import Lexer
from sandalwood.lexer.token import TokenType
from sandalwood.parser.parser import Parser


def _parse_program(source: str):
    return Parser(Lexer(source).tokenize()).parse()


class LexerFoundationTests(unittest.TestCase):
    def test_tokenizes_keyword_identifier_literal_operator_delimiter(self) -> None:
        source = 'idhu number = 42\ndialogue(number)\n'
        tokens = Lexer(source).tokenize()
        token_types = [token.token_type for token in tokens]
        self.assertIn(TokenType.KEYWORD, token_types)
        self.assertIn(TokenType.IDENTIFIER, token_types)
        self.assertIn(TokenType.INTEGER, token_types)
        self.assertIn(TokenType.OPERATOR, token_types)
        self.assertIn(TokenType.DELIMITER, token_types)

    def test_tokenizes_multi_character_operators(self) -> None:
        source = "idhu ok = a >= b && c <= d || e == f != g // 2\n"
        tokens = Lexer(source).tokenize()
        operators = [token.value for token in tokens if token.token_type == TokenType.OPERATOR]
        self.assertIn(">=", operators)
        self.assertIn("<=", operators)
        self.assertIn("&&", operators)
        self.assertIn("||", operators)
        self.assertIn("==", operators)
        self.assertIn("!=", operators)
        self.assertIn("//", operators)

    def test_raises_for_unterminated_string(self) -> None:
        with self.assertRaises(LexerError):
            Lexer('dialogue("hello)\n').tokenize()

    def test_raises_for_unexpected_character(self) -> None:
        with self.assertRaises(LexerError):
            Lexer("idhu a = 1 @ 2").tokenize()


class ParserFoundationTests(unittest.TestCase):
    def test_parses_if_return_and_call_syntax(self) -> None:
        program = _parse_program(
            """
scene fib(n) {
  nodona (n <= 1) {
    packup n
  }
  packup fib(n - 1) + fib(n - 2)
}
scene main() {
  idhu result = fib(6)
  dialogue(result)
}
"""
        )
        self.assertEqual(len(program.statements), 2)
        fib_function = program.statements[0]
        self.assertIsInstance(fib_function.body[0], IfStatement)
        self.assertIsInstance(fib_function.body[1], ReturnStatement)
        self.assertIsInstance(fib_function.body[1].value, BinaryExpression)

    def test_respects_operator_precedence(self) -> None:
        program = _parse_program(
            """
scene main() {
  idhu value = 1 + 2 * 3
}
"""
        )
        declaration = program.statements[0].body[0]
        self.assertIsInstance(declaration, VariableDeclaration)
        self.assertIsInstance(declaration.value, BinaryExpression)
        self.assertEqual(declaration.value.operator, "+")
        self.assertIsInstance(declaration.value.right, BinaryExpression)
        self.assertEqual(declaration.value.right.operator, "*")

    def test_raises_for_unterminated_block(self) -> None:
        with self.assertRaises(ParserError):
            _parse_program("scene main() {\n  dialogue(\"hi\")\n")


class InterpreterFoundationTests(unittest.TestCase):
    def test_executes_recursive_function(self) -> None:
        source = """
scene fib(n) {
  nodona (n <= 1) {
    packup n
  }
  packup fib(n - 1) + fib(n - 2)
}
scene main() {
  dialogue(fib(6))
}
"""
        output = io.StringIO()
        with redirect_stdout(output):
            Interpreter().interpret(_parse_program(source))
        self.assertEqual(output.getvalue().strip(), "8")

    def test_executes_elif_branch(self) -> None:
        source = """
scene main() {
  idhu n = 2
  nodona (n == 1) {
    dialogue("one")
  }
  illandre (n == 2) {
    dialogue("two")
  }
  climax {
    dialogue("other")
  }
}
"""
        output = io.StringIO()
        with redirect_stdout(output):
            Interpreter().interpret(_parse_program(source))
        self.assertEqual(output.getvalue().strip(), "two")

    def test_supports_size_builtin(self) -> None:
        source = """
scene main() {
  dialogue(size("abcd"))
}
"""
        output = io.StringIO()
        with redirect_stdout(output):
            Interpreter().interpret(_parse_program(source))
        self.assertEqual(output.getvalue().strip(), "4")

    def test_concatenates_strings_and_numbers_in_dialogue(self) -> None:
        source = """
scene main() {
  idhu n = 3
  dialogue("Move disk " + n + " from A to B")
}
"""
        output = io.StringIO()
        with redirect_stdout(output):
            Interpreter().interpret(_parse_program(source))
        self.assertEqual(output.getvalue().strip(), "Move disk 3 from A to B")

    def test_ignores_line_comments_and_keeps_floor_division(self) -> None:
        source = """
scene main() {
  // ignore this line
  dialogue(8 // 3)
}
"""
        output = io.StringIO()
        with redirect_stdout(output):
            Interpreter().interpret(_parse_program(source))
        self.assertEqual(output.getvalue().strip(), "2")

    def test_ignores_trailing_comment_after_statement(self) -> None:
        source = """
scene main() {
  dialogue("ok") // trailing comment
}
"""
        output = io.StringIO()
        with redirect_stdout(output):
            Interpreter().interpret(_parse_program(source))
        self.assertEqual(output.getvalue().strip(), "ok")

    def test_supports_array_literals_and_indexing(self) -> None:
        source = """
scene main() {
  idhu values = [1, 3, 5, 7, 9, 11]
  dialogue(values[3])
}
"""
        output = io.StringIO()
        with redirect_stdout(output):
            Interpreter().interpret(_parse_program(source))
        self.assertEqual(output.getvalue().strip(), "7")

    def test_short_circuit_or_does_not_evaluate_rhs(self) -> None:
        source = """
scene main() {
  nodona (blockbuster || missingName) {
    dialogue("ok")
  }
}
"""
        output = io.StringIO()
        with redirect_stdout(output):
            Interpreter().interpret(_parse_program(source))
        self.assertEqual(output.getvalue().strip(), "ok")

    def test_raises_for_unknown_function_call(self) -> None:
        source = """
scene main() {
  unknown()
}
"""
        with self.assertRaises(RuntimeSandalwoodError):
            Interpreter().interpret(_parse_program(source))


class CliFoundationTests(unittest.TestCase):
    def test_project_exposes_sandal_console_script(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(pyproject["project"]["scripts"]["sandal"], "sandalwood.cli.main:main")

    def test_cli_runs_hello_program(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "sandalwood.cli.main",
                str(repo_root / "examples" / "hello.sw"),
            ],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Namaskara Sandalwood!", result.stdout)
        self.assertIn("Parsed hello.sw", result.stdout)

    def test_cli_reports_invalid_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid.txt"
            file_path.write_text("scene main() {}", encoding="utf-8")
            with self.assertRaises(RuntimeSandalwoodError):
                run_file(file_path)

    def test_cli_reports_syntax_error(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "broken.sw"
            file_path.write_text("scene main() { nodona (blockbuster) { dialogue(\"x\") }", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "sandalwood.cli.main",
                    str(file_path),
                ],
                cwd=repo_root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("[SandalwoodError]", result.stdout)


if __name__ == "__main__":
    unittest.main()
