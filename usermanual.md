# Sandalwood User Manual

## Setup & Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Quick Setup

**Option 1: Automated Setup (Recommended)**

Run the automated setup script:

```bash
bash init.sh
```

This will:
- Verify Python version
- Install the Sandalwood package in development mode
- Verify the `sandal` command is available

**Option 2: Manual Setup**

```bash
# Navigate to project directory
cd /path/to/sandalwood-lang

# Install in development mode
pip install -e .

# Verify installation
sandal --help
```

### Running Sandalwood Programs

After setup, run any `.sw` file with:

```bash
sandal examples/hello.sw
```

### Example Programs

Try these included examples:
- `examples/hello.sw` - Hello world
- `examples/fibonacci.sw` - Fibonacci sequence
- `examples/binary_search.sw` - Binary search algorithm

## Language

- Name: Sandalwood
- Extension: `.sw`
- Version: `0.1`

## Source of Truth for Syntax

All Sandalwood syntax is defined in:

`/home/runner/work/sandalwood-lang/sandalwood-lang/config/syntax.json`

Update this file to evolve keywords, operators, delimiters, builtins, and runtime mappings.

## Keywords

- `idhu` (mutable variable)
- `pakka` (constant variable)
- `scene` (function definition)
- `packup` (return)
- `nodona` (if)
- `illandre` (else-if)
- `climax` (else)
- `retake` (while)
- `cut` (break)
- `mundhe` (continue)
- `blockbuster` (true)
- `flop` (false)
- `dialogue` (print)
- `kelu` (input)
- `banner` (class)
- `hosa` (new)
- `nanu` (self)
- `tharale` (import)
- `prayatna` (try)
- `thappu` (catch)
- `kone` (finally)

## Operators

- Arithmetic: `+`, `-`, `*`, `/`, `%`, `//`
- Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Logical: `&&`, `||`, `!`
- Assignment: `=`

## Delimiters

- `(` `)`
- `{` `}`
- `[` `]`
- `;` `,` `:`

## Collections

### Array methods

- `tallu` (append)
- `tegeyu` (pop)
- `ulta` (reverse)
- `jodisu` (sort)
- `size` (length)

### Map methods

- `haku` (insert)
- `siktha` (contains)
- `chavi` (keys)
- `bele` (values)

## Builtins

- `dialogue`, `kelu`, `size`
- `min`, `max`, `abs`, `pow`, `sqrt`
- `split`, `join`, `replace`, `upper`, `lower`

## Example

```sw
scene main() {
  idhu number = 42
  dialogue(number)
}
```
