# Sandalwood Language

Sandalwood is a modular interpreted language project (`.sw`) built on Python.

## Architecture

The foundation follows a clean pipeline:

`Lexer -> Parser -> AST -> Interpreter`

Project goals:
- Beginner-friendly implementation
- Extensible parser and runtime
- Config-driven lexer keywords/operators
- Single-source syntax spec in `config/syntax.json`

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
sandal examples/hello.sw
```

## Syntax Configuration

All language syntax is defined in:

`config/syntax.json`

This file contains Sandalwood language metadata, keywords, operators, delimiters, builtins, collection method names, and runtime mappings.
