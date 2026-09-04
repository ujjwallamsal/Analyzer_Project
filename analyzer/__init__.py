"""
analyzer package

A simple static code analysis tool for Python source files.

This package is split into small modules, one per type of check:
- metrics.py            -> basic code metrics (lines, functions, classes)
- complexity.py          -> cyclomatic complexity per function
- unused_variables.py    -> variables that are assigned but never used
- duplicate_code.py      -> repeated lines / blocks of code
- naming.py              -> PEP8 style naming convention checks
- report.py              -> combines everything into one report
"""
