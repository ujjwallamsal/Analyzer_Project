# Python Static Code Analyzer

A command-line tool that analyzes a single Python source file and reports on code quality issues:

- **Code metrics** — total lines, blank lines, comment lines, code lines, number of functions, number of classes
- **Cyclomatic complexity** — how many independent paths run through each function
- **Unused variables** — variables assigned a value but never read
- **Duplicate lines** — exact lines of code repeated elsewhere in the file
- **Naming violations** — functions/variables not written in `snake_case`, classes not written in `PascalCase`

## Requirements

- Python 3.9+
- No external libraries are required to run the analyzer itself — only the standard library `ast` and `re` modules are used
- `pytest` and `coverage` are required to run the automated test suite

## Installation

```bash
git clone https://github.com/ujjwallamsal/Analyzer_Project.git
cd Analyzer_Project
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the analyzer against any Python file:

```bash
python -m analyzer path/to/your_file.py
```

Two example files are included to demonstrate the tool:

```bash
python -m analyzer samples/clean_example.py    # well-written code, few/no issues
python -m analyzer samples/messy_example.py    # intentionally messy code, triggers every check
```

If the given file does not exist, or contains invalid Python syntax, the tool prints a clear error message instead of crashing:

```bash
python -m analyzer does_not_exist.py
```

## Project Structure

```
analyzer/
    __init__.py
    __main__.py            # command-line entry point
    metrics.py              # line/function/class counting
    complexity.py            # cyclomatic complexity per function
    unused_variables.py      # scope-aware unused variable detection
    duplicate_code.py        # duplicate line detection
    naming.py                # PEP8 naming convention checks
    report.py                 # combines every checker into one report
tests/
    test_metrics.py
    test_complexity.py
    test_unused_variables.py
    test_duplicate_code.py
    test_naming.py
    test_report.py
    test_print_report.py
samples/
    clean_example.py
    messy_example.py
```

## Running the Tests

```bash
pytest tests/ -v
```

## Running the Tests with Coverage

```bash
coverage run -m pytest tests/
coverage report -m --include="analyzer/*"
coverage html   # generates htmlcov/index.html for a browsable report
```

## Design Notes and Assumptions

- Analysis is performed on a single Python file at a time, not a whole project or directory.
- Unused-variable detection only tracks simple `name = value` assignments. Unused function parameters, unused imports, and unused loop variables are intentionally out of scope, to keep the checker simple and predictable.
- Duplicate-code detection compares exact, trimmed lines of text. It does not detect code that does the same thing but is written differently (e.g. `x = a + b` vs `x = b + a`). Blank lines and comment-only lines are ignored, since repeating those is normal.
- Naming checks skip very short identifiers (1–2 characters), since names like `i`, `x`, or `dx` are common and idiomatic in Python.
- Cyclomatic complexity is calculated as `1 + number of decision points` (if/elif, for, while, except, and/or), a simplified but standard approximation of McCabe complexity.

## Test Coverage

The `analyzer` package is covered by 50 automated tests, reaching 99% statement coverage.

| Module | Coverage |
|---|---|
| `metrics.py` | 100% |
| `complexity.py` | 100% |
| `duplicate_code.py` | 100% |
| `naming.py` | 100% |
| `unused_variables.py` | 100% |
| `report.py` | 98% |
| **Total** | **99%** |
