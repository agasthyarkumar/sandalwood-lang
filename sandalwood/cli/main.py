from __future__ import annotations

import argparse
from pathlib import Path

from sandalwood.errors.handler import format_error
from sandalwood.errors.exceptions import SandalwoodError
from sandalwood.interpreter.interpreter import Interpreter
from sandalwood.lexer.lexer import Lexer
from sandalwood.parser.parser import Parser


def run_file(path: Path, print_tokens: bool = False) -> int:
    source = path.read_text(encoding="utf-8")
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    Interpreter().interpret(program)

    if print_tokens:
        for token in tokens:
            print(f"{token.token_type.name:>10} {token.value}")

    print(f"Parsed {path.name}: {len(program.statements)} statement(s)")
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Sandalwood .sw programs")
    parser.add_argument("file", type=Path, help="Path to a .sw file")
    parser.add_argument("--tokens", action="store_true", help="Print token stream")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    try:
        return run_file(args.file, print_tokens=args.tokens)
    except FileNotFoundError:
        print(f"File not found: {args.file}")
        return 1
    except SandalwoodError as exc:
        print(format_error(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
