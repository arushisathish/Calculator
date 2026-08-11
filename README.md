# Command-Line Calculator

A keyboard-only calculator that runs directly in the terminal. Instead of
navigating menus, you type an expression the way you'd naturally think of
one — `8 + 3`, `sqrt(9)`, `log(100)` — and it handles both the math and
your mistakes gracefully.

## Why this is more than a basic calculator

Most beginner calculators assume the user always types something valid.
This one assumes they won't, and is built around three ideas instead:

1. **It never crashes.** Every risky operation — bad input, division by
   zero, invalid math — is caught and explained, not left to throw a raw
   Python error at the user.
2. **It understands common typos, not just correct syntax.** People
   naturally type `8x3` instead of `8*3`, or `2**3` out of habit from other
   languages. This calculator recognizes and handles those instead of
   rejecting them.
3. **It's usable without already knowing Python.** Every symbol and
   function is explained in plain English in the `help` menu — nothing
   assumes the user already knows what `%` or `^` means in code.

## How to run it

```
python calculator.py
```

A short welcome message and a quick usage example appear immediately —
you don't need to already know a `help` command exists to get started.
Type `help` any time afterward for the full guide.

## What you can type

| Input | Meaning |
|---|---|
| `8 + 3` | addition |
| `8 - 3` | subtraction |
| `8 * 3` (or `8x3`) | multiplication |
| `8 / 3` | division |
| `8 % 3` | modulo (remainder) |
| `2 ^ 3` (or `2**3`) | power / exponent |
| `sqrt(9)` | square root |
| `sqr(4)` | square (x × x) |
| `root(8, 3)` | nth root (cube root of 8, here) |
| `log(100)` | log base 10 |
| `log(8, 2)` | log base 2 of 8 |
| `ln(5)` | natural log |
| `5!` | factorial |
| `ans + 2` | reuse the last result |
| `history` | see everything calculated this session |
| `help` | show the full syntax guide |
| `exit` / `quit` | close the calculator |

## How input is understood (no `eval()` used)

Typed input is never passed through Python's `eval()` — that would let
anyone run arbitrary code through the calculator, which is a real risk even
in a small project. Instead, every line goes through auto-correct first,
then is checked against three patterns using regular expressions:

1. **Binary expression** — `number operator number` (e.g. `8 + 3`)
2. **Factorial** — `number!` (e.g. `5!`)
3. **Function call** — `name(args)` (e.g. `sqrt(9)`, `log(8, 2)`)

If nothing matches, the calculator says so directly and points to `help`
instead of guessing.

## Auto-correct: three different rules for three different mistakes

Not every "wrong" input gets treated the same way:

- **Unambiguous typos → fixed silently.** `8++3` and `8x3` have no other
  possible meaning, so they're just corrected with no message.
- **Ambiguous syntax → fixed *and* explained.** `2**3` is valid in Python
  but not here, so it's auto-corrected to `2^3` with a short note — so the
  user learns the calculator's actual syntax instead of wondering why it
  worked.
- **Valid but risky to mistype → left as-is, gently flagged.** `8--3` is
  mathematically correct (a double negative, equal to `8 + 3`), so it's
  computed correctly — but a note is shown in case it wasn't intentional.

## Math edge cases handled

- Division and modulo by zero
- Non-numeric input anywhere a number is expected
- Square/nth root of a negative number — **except** odd roots, which are
  real numbers and are correctly computed (`root(-8, 3) = -2`)
- A negative number raised to a fractional power (e.g. `-8 ^ 0.5`) is
  blocked with an explanation, instead of silently returning a complex
  number that would confuse anyone reading the result
- Logarithm or natural log of zero or a negative number
- Factorial of a negative or non-whole number
- Wrong number of arguments to a function (e.g. `root(8)` missing the
  second number)
- Unknown function names
- Unbalanced or malformed parentheses
- Ctrl+C exits cleanly instead of crashing with a traceback

## About AI integration (why it isn't in this version, and why it could matter)

AI integration wasn't added to this version because it's a first project,
and adding it properly would mean a real jump in complexity — calling an
external API, handling an API key, an internet connection, and a cost per
request, on top of new failure modes (no internet, invalid key, slow or
failed requests) that deserve their own error handling separate from the
math error handling already in this file.

That said, the idea is worth explaining, because it's a fair question to
ask: why would a calculator need AI at all?

The honest answer is that most people today don't reach for a calculator
to actually learn how to solve something — they Google the question or ask
an AI directly, get the answer, and move on, without practicing the
calculation themselves. If a calculator like this one had AI built in, the
goal wouldn't be to hand over answers. It would be to help someone who
knows *what* they want to calculate but isn't sure *how* to type it — for
example, someone who wants the cube root of 7, or a logarithm with a
specific base, but doesn't know the correct syntax for expressing that.
The AI's role there would be entirely about translating intent into correct
input, not solving the problem for them.

This kind of assistance could be genuinely useful in two settings:

- **Learning apps**, where the point is to still do the calculation
  yourself, but not get stuck on syntax you've never seen before.
- **Exam software**, where the AI would never be allowed to answer the
  actual question — but could still help a student correctly express what
  they're trying to calculate, the same way this calculator's `help` menu
  already does, just more conversationally.

If this is added later, it should live in its own optional module that this
program only uses if it's present and configured — so the calculator keeps
working with zero dependencies and zero cost if that module is missing or
disabled.
