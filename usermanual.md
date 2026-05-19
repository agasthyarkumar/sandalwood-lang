# Sandalwood User Manual

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
