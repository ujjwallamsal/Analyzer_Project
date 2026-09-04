"""
report.py

Ties together every individual check (metrics, complexity, unused
variables, duplicate code, naming) into one combined report.

This module is also responsible for handling things going wrong:
- the file the user asked for does not exist
- the file is not valid Python

Instead of letting the program crash with an unhandled exception, we
catch these problems and put a clear message in report["error"].
"""

import os

from analyzer.metrics import calculate_metrics
from analyzer.complexity import calculate_complexity
from analyzer.unused_variables import find_unused_variables
from analyzer.duplicate_code import find_duplicate_lines
from analyzer.naming import check_naming


def analyze_file(file_path):
    """
    Read a Python file from disk and analyze it.

    Args:
        file_path (str): path to a .py file.

    Returns:
        dict: a report dictionary (see analyze_source for its shape).
            If the file does not exist, the report will contain an
            "error" message and all other fields will be None/empty.
    """
    if not os.path.isfile(file_path):
        return _empty_report_with_error(f"File not found: {file_path}")

    with open(file_path, "r") as file_handle:
        source_code = file_handle.read()

    return analyze_source(source_code)


def analyze_source(source_code):
    """
    Analyze a string of Python source code and produce a combined report.

    Args:
        source_code (str): the full text of a Python file.

    Returns:
        dict: with keys:
            "error"              -> None, or a message if analysis failed
            "metrics"            -> dict from analyzer.metrics
            "complexity"         -> dict from analyzer.complexity
            "unused_variables"   -> list from analyzer.unused_variables
            "duplicate_lines"    -> list from analyzer.duplicate_code
            "naming_violations"  -> list from analyzer.naming
    """
    try:
        metrics = calculate_metrics(source_code)
        complexity = calculate_complexity(source_code)
        unused_variables = find_unused_variables(source_code)
        naming_violations = check_naming(source_code)
    except SyntaxError as error:
        return _empty_report_with_error(f"Syntax error in source code: {error}")

    # Duplicate line checking works on plain text, so it does not need
    # to run inside the same try/except as the ast-based checks above.
    duplicate_lines = find_duplicate_lines(source_code)

    return {
        "error": None,
        "metrics": metrics,
        "complexity": complexity,
        "unused_variables": unused_variables,
        "duplicate_lines": duplicate_lines,
        "naming_violations": naming_violations,
    }


def _empty_report_with_error(message):
    """Build a report dictionary that only contains an error message."""
    return {
        "error": message,
        "metrics": None,
        "complexity": None,
        "unused_variables": None,
        "duplicate_lines": None,
        "naming_violations": None,
    }


def print_report(report):
    """
    Print a report dictionary to the screen in a readable, human-friendly
    format. This is used by the command-line interface (see __main__.py).
    """
    if report["error"] is not None:
        print("Could not analyze file.")
        print("Error:", report["error"])
        return

    print("=== Code Metrics ===")
    for key, value in report["metrics"].items():
        print(f"{key}: {value}")

    print("\n=== Cyclomatic Complexity ===")
    if not report["complexity"]:
        print("No functions found.")
    for function_name, score in report["complexity"].items():
        print(f"{function_name}: {score}")

    print("\n=== Unused Variables ===")
    if not report["unused_variables"]:
        print("None found.")
    for item in report["unused_variables"]:
        print(f"Line {item['line']}: '{item['name']}' is assigned but never used.")

    print("\n=== Duplicate Lines ===")
    if not report["duplicate_lines"]:
        print("None found.")
    for item in report["duplicate_lines"]:
        line_list = ", ".join(str(n) for n in item["line_numbers"])
        print(f"'{item['line_text']}' appears on lines: {line_list}")

    print("\n=== Naming Violations ===")
    if not report["naming_violations"]:
        print("None found.")
    for item in report["naming_violations"]:
        print(f"Line {item['line']}: {item['type']} '{item['name']}' does not follow naming conventions.")
