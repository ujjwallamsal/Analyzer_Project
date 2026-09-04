# Python Static Code Analyzer

A simple command-line tool that analyzes a Python source file and reports:

- **Code metrics** — total lines, blank lines, comment lines, code lines, number of functions, number of classes
- **Cyclomatic complexity** — how many independent paths run through each function
- **Unused variables** — variables assigned but never read
- **Duplicate lines** — exact lines of code repeated elsewhere in the file
- **Naming violations** — functions/variables not in `snake_case`, classes not in `PascalCase`

Built using an AI-assisted Test-Driven Development (TDD) workflow: for every checker, the automated tests were written first, then the implementation was written to make them pass.

## Project structure

```
analyzer/
    __init__.py
    __main__.py          # command-line entry point
    metrics.py
    complexity.py
    unused_variables.py
    duplicate_code.py
    naming.py
    report.py             # combines every checker into one report
tests/
    test_metrics.py
    test_complexity.py
    test_unused_variables.py
    test_duplicate_code.py
    test_naming.py
    test_report.py
    test_print_report.py
samples/
    clean_example.py      # well-written example (few/no issues)
    messy_example.py       # intentionally messy example (triggers every check)
```

## Requirements

- Python 3.9+
- No external libraries needed to run the analyzer itself (only the standard library `ast` and `re` modules are used)
- `pytest` and `coverage` are needed to run the test suite

Install test dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the analyzer against any Python file:

```bash
python -m analyzer path/to/your_file.py
```

Try it on the included sample files:

```bash
python -m analyzer samples/clean_example.py
python -m analyzer samples/messy_example.py
```

## Running the tests

```bash
pytest tests/ -v
```

## Running the tests with coverage

```bash
coverage run -m pytest tests/
coverage report -m
coverage html   # generates htmlcov/index.html for a browsable report
```

## Design notes / assumptions

- Analysis is performed on a single Python file at a time (not a whole project/directory).
- Input is assumed to be a `.py` file; if the file does not exist, or contains invalid Python syntax, the tool reports a clear error instead of crashing.
- Unused-variable detection only tracks simple `name = value` assignments. Unused function parameters, unused imports, and unused loop variables are intentionally out of scope, to keep the checker simple and predictable.
- Duplicate-code detection compares exact, trimmed lines of text. It does not detect code that does the same thing but is written differently (e.g. `x = a + b` vs `x = b + a`). Blank lines and comment-only lines are ignored since repeating those is normal.
- Naming checks skip very short names (1–2 characters), since short names like `i`, `x`, or `dx` are common and idiomatic in Python.
- Cyclomatic complexity is calculated as `1 + number of decision points` (if/elif, for, while, except, and/or), which is a simplified but standard approximation.
