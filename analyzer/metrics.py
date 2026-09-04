"""
metrics.py

Calculates simple, easy-to-understand metrics about a piece of Python
source code:
- how many lines total
- how many are blank
- how many are comments
- how many are actual code
- how many functions and classes are defined

We use Python's built-in "ast" (Abstract Syntax Tree) module to safely
understand the structure of the code, instead of guessing with regular
expressions.
"""

import ast


def calculate_metrics(source_code):
    """
    Calculate basic code metrics for a string of Python source code.

    Args:
        source_code (str): the full text of a Python file.

    Returns:
        dict: a dictionary with the following keys:
            total_lines, blank_lines, comment_lines, code_lines,
            function_count, class_count

    Raises:
        SyntaxError: if source_code is not valid Python code.
    """
    # First, make sure the code is valid Python.
    # ast.parse() will raise SyntaxError automatically if it is not.
    tree = ast.parse(source_code)

    # Split the source into individual lines so we can count them.
    lines = source_code.splitlines()

    total_lines = len(lines)
    blank_lines = 0
    comment_lines = 0

    for line in lines:
        stripped_line = line.strip()

        if stripped_line == "":
            blank_lines += 1
        elif stripped_line.startswith("#"):
            comment_lines += 1

    # Any line that is not blank and not a comment counts as a code line.
    code_lines = total_lines - blank_lines - comment_lines

    # Walk through the whole syntax tree and count function/class definitions.
    # ast.walk() visits every node in the tree, including nested ones,
    # so a function defined inside another function is still counted.
    function_count = 0
    class_count = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_count += 1
        elif isinstance(node, ast.ClassDef):
            class_count += 1

    return {
        "total_lines": total_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "code_lines": code_lines,
        "function_count": function_count,
        "class_count": class_count,
    }
