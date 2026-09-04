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
expressions. We also use "tokenize" to tell the difference between a
real comment (# ...) and a '#' character that just happens to appear
inside a multi-line string, such as a docstring with an example in it.
"""

import ast
import io
import tokenize


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

    # Lines that fall inside a multi-line string (e.g. a docstring)
    # should never be treated as comments, even if the text on that
    # line happens to start with '#'.
    lines_inside_multiline_string = _find_lines_inside_multiline_strings(source_code)

    blank_lines = 0
    comment_lines = 0

    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()

        if stripped_line == "":
            blank_lines += 1
        elif stripped_line.startswith("#") and line_number not in lines_inside_multiline_string:
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


def _find_lines_inside_multiline_strings(source_code):
    """
    Return the set of line numbers that fall inside a multi-line
    string literal (e.g. a triple-quoted docstring), not counting the
    line where the string starts.

    A '#' on one of these lines is part of the string's text, not a
    real Python comment, so calculate_metrics() uses this set to
    avoid miscounting it.
    """
    lines_inside = set()
    tokens = tokenize.generate_tokens(io.StringIO(source_code).readline)

    for token in tokens:
        if token.type == tokenize.STRING:
            start_row = token.start[0]
            end_row = token.end[0]
            if end_row > start_row:
                for line_number in range(start_row + 1, end_row + 1):
                    lines_inside.add(line_number)

    return lines_inside