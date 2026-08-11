import math 
import random
import re

ans: float = 0.0
history: list[str] = []

WELCOME_LINES = [
    "This calculator promises 100% accuracy and 0% judgment about your math skills.",
    "Warning: unlike your school calculator, this one won't die mid-exam. (You still can't use it in one though.)",
    "No batteries required. No mouse required. Just you, your numbers, and mild chaos.",
    "This calculator has never once said 'Syntax Error' and left you to figure it out yourself.",
]


def show_welcome() -> None:
    print("=== Command-Line Calculator ===")
    print(random.choice(WELCOME_LINES))
    print()
    print("Just type a sum and hit Enter — e.g. 8 + 3, or sqrt(9)")
    print("Any doubt or error? Just type: help")
    print()


def show_help() -> None:
    print("=== HELP ===\n")
    print("SYMBOLS FOR BASIC MATH:")
    print("  +   plus / addition          e.g. 8 + 3   = 11")
    print("  -   minus / subtraction      e.g. 8 - 3   = 5")
    print("  *   times / multiplication   e.g. 8 * 3   = 24   (typing 8x3 also works)") 
    print("  /   divided by / division    e.g. 8 / 3   = 2.666...")
    print("  %   modulo (remainder left over after dividing)  e.g. 8 % 3 = 2")
    print("  ^   power / exponent (a raised to the b)  e.g. 2 ^ 3 = 8   (typing ** also works)")
    print()
    print("WORDS FOR EVERYTHING ELSE (type the word, then the number in brackets):")
    print("  sqrt(x)     square root of x        e.g. sqrt(9)  = 3")
    print("  sqr(x)      square of x, i.e. x*x    e.g. sqr(4)  = 16")
    print("  root(x, n)  the nth root of x        e.g. root(8, 3) = 2  (cube root of 8)")
    print("                (odd roots of negative numbers work: root(-8, 3) = -2)")
    print("  log(x)      log base 10 of x         e.g. log(100) = 2")
    print("  log(x, n)   log base n of x          e.g. log(8, 2) = 3")
    print("  ln(x)       natural log of x         e.g. ln(5) = 1.609...")
    print("  x!          factorial of x           e.g. 5! = 120")
    print()
    print("A FEW THINGS TO KNOW:")
    print("  - Even roots (like sqrt) and even-numbered roots of negative numbers aren't")
    print("    real numbers, so those are blocked with an explanation.")
    print("  - A negative number raised to a fractional power (e.g. -8^0.5) isn't a")
    print("    real number either, so that's blocked too.")
    print("  - Note: parentheses only work around function arguments, like sqrt(9) —")
    print("    not around plain numbers like (-8)^2. Just type -8^2 directly instead.")
    print("  - Small typos like 8x3, 8++3, or 2**3 are automatically understood.")
    print()
    print("OTHER COMMANDS:")
    print("  history   - see everything you've calculated this session")
    print("  help      - show this guide again")
    print("  exit/quit - close the calculator")
    print("  ans       - reuse your last result, e.g. ans + 2")
    print()


def parse_number(text: str) -> float:
    text = text.strip()
    if text.lower() == "ans":
        return ans
    try:
        return float(text)
    except ValueError:
        raise ValueError(f"'{text}' is not a valid number.")


def record(entry: str, result: float) -> None:
    global ans
    ans = result
    history.append(f"{entry} = {result}")
    print(f"  = {result}")


def show_history() -> None:
    if not history:
        print("  (no calculations yet this session)")
        return
    for i, entry in enumerate(history, start=1):
        print(f"  {i}. {entry}")


def autocorrect(text: str) -> tuple[str, list[str]]:
    notices: list[str] = []
    corrected = text

    if "**" in corrected:
        corrected = corrected.replace("**", "^")
        notices.append("Used '**' for power? This calculator uses '^' instead — 2^3 also works directly.")

    corrected = re.sub(r"\+\+", "+", corrected)

    corrected = re.sub(r"(?<=[\d)])\s*[xX]\s*(?=[\d(])", " * ", corrected)

    if re.search(r"(?<!-)--(?!-)", text):
        notices.append("Note: '--' is read as a double negative (e.g. 8 - (-3) = 11). "
                        "If you meant something else, try again.")

    return corrected, notices


def evaluate_binary(text: str) -> bool:
    match = re.fullmatch(
        r"\s*(ans|-?\d+(?:\.\d+)?)\s*([+\-*/%^])\s*(ans|-?\d+(?:\.\d+)?)\s*", text
    )
    if not match:
        return False

    left_raw, operator, right_raw = match.groups()
    try:
        a = parse_number(left_raw)
        b = parse_number(right_raw)

        if operator == "+":
            record(f"{a} + {b}", a + b)
        elif operator == "-":
            record(f"{a} - {b}", a - b)
        elif operator == "*":
            record(f"{a} * {b}", a * b)
        elif operator == "/":
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            record(f"{a} / {b}", a / b)
        elif operator == "%":
            if b == 0:
                raise ZeroDivisionError("Cannot use modulo with zero as the divisor.")
            record(f"{a} % {b}", a % b)
        elif operator == "^":
            if a < 0 and b != int(b):
                raise ValueError(
                    "A negative number raised to a fractional power isn't a real number."
                )
            record(f"{a} ^ {b}", a ** b)
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        print(f"  ⚠ {e}")
    return True


def evaluate_factorial(text: str) -> bool:
    match = re.fullmatch(r"\s*(ans|-?\d+(?:\.\d+)?)\s*!\s*", text)
    if not match:
        return False

    raw = match.group(1)
    try:
        n = parse_number(raw)
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        if n != int(n):
            raise ValueError("Factorial is only defined for whole numbers.")
        record(f"{n}!", float(math.factorial(int(n))))
    except (ValueError, OverflowError) as e:
        print(f"  ⚠ {e}")
    return True


def evaluate_function(text: str) -> bool:
    match = re.fullmatch(r"\s*([a-zA-Z]+)\s*\((.*)\)\s*", text)
    if not match:
        if "(" in text or ")" in text:
            print("  ⚠ Unbalanced or malformed parentheses.")
            return True
        return False

    name, args_raw = match.groups()
    name = name.lower()
    args = [a.strip() for a in args_raw.split(",")] if args_raw.strip() != "" else []

    try:
        if name == "sqr":
            if len(args) != 1:
                raise ValueError("sqr(x) takes exactly 1 argument.")
            x = parse_number(args[0])
            record(f"sqr({x})", x * x)

        elif name == "sqrt":
            if len(args) != 1:
                raise ValueError("sqrt(x) takes exactly 1 argument.")
            x = parse_number(args[0])
            if x < 0:
                raise ValueError("Cannot take the square root of a negative number.")
            record(f"sqrt({x})", math.sqrt(x))

        elif name == "root":
            if len(args) != 2:
                raise ValueError("root(x, n) takes exactly 2 arguments.")
            x, n = parse_number(args[0]), parse_number(args[1])
            if n == 0:
                raise ValueError("Cannot take the 0th root of a number.")
            if x < 0:
                is_odd_whole_root = (n == int(n)) and (int(n) % 2 != 0)
                if not is_odd_whole_root:
                    raise ValueError(
                        "Cannot take an even root of a negative number (result would not be a real number)."
                    )
                result = -((-x) ** (1 / n))
            else:
                result = x ** (1 / n)
            record(f"root({x}, {n})", result)

        elif name == "log":
            if len(args) == 1:
                x = parse_number(args[0])
                if x <= 0:
                    raise ValueError("Logarithm is only defined for numbers greater than 0.")
                record(f"log({x})", math.log10(x))
            elif len(args) == 2:
                x, base = parse_number(args[0]), parse_number(args[1])
                if x <= 0:
                    raise ValueError("Logarithm is only defined for numbers greater than 0.")
                if base <= 0 or base == 1:
                    raise ValueError("Log base must be greater than 0 and not equal to 1 (base 1 is undefined).")
                record(f"log({x}, base {base})", math.log(x, base))
            else:
                raise ValueError("log(x) or log(x, base) — 1 or 2 arguments only.")

        elif name == "ln":
            if len(args) != 1:
                raise ValueError("ln(x) takes exactly 1 argument.")
            x = parse_number(args[0])
            if x <= 0:
                raise ValueError("Natural log is only defined for numbers greater than 0.")
            record(f"ln({x})", math.log(x))

        else:
            raise ValueError(f"Unknown function '{name}'. Type 'help' to see available functions.")

    except (ValueError, OverflowError) as e:
        print(f"  ⚠ {e}")
    return True


def evaluate(text: str) -> None:
    if evaluate_binary(text):
        return
    if evaluate_factorial(text):
        return
    if evaluate_function(text):
        return
    print(f"  ⚠ '{text}' wasn't understood. Type 'help' to see supported input formats.")


def main() -> None:
    show_welcome()
    try:
        while True:
            raw = input("> ").strip()
            if raw == "":
                continue

            lower = raw.lower()
            if lower in ("exit", "quit"):
                print("Goodbye!")
                break
            elif lower in ("help", "h"):
                show_help()
            elif lower == "history":
                show_history()
            else:
                corrected, notices = autocorrect(raw)
                for note in notices:
                    print(f"  ℹ {note}")
                evaluate(corrected)

    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")


if __name__ == "__main__":
    main()
