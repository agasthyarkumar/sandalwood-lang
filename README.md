# Sandalwood Language

Sandalwood is a modular interpreted language project (`.sw`) built on Python.

## Architecture

The foundation follows a clean pipeline:

`Lexer -> Parser -> AST -> Interpreter`

Project goals:
- Beginner-friendly implementation
- Extensible parser and runtime
- Config-driven lexer keywords/operators

## Project Structure

```text
sandalwood-lang/
├── config/
├── sandalwood/
│   ├── lexer/
│   ├── parser/
│   ├── ast/
│   ├── interpreter/
│   ├── runtime/
│   ├── errors/
│   ├── cli/
│   └── utils/
├── examples/
└── tests/
```

## Quick Start

```bash
python -m sandalwood.cli.main examples/hello.sw
```
