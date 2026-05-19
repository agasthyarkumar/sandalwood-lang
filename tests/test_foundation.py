from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import unittest

from sandalwood.lexer.lexer import Lexer
from sandalwood.lexer.token import TokenType


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


class CliFoundationTests(unittest.TestCase):
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
        self.assertIn("Parsed hello.sw", result.stdout)


if __name__ == "__main__":
    unittest.main()
