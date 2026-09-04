"""
complexity.py

Calculates a simplified version of "cyclomatic complexity" for each
function in a piece of Python source code.

Cyclomatic complexity = 1 + number of decision points in the function.

Decision points we count:
- if / elif
- for
- while
- except (each "except" block is an extra path)
- boolean operators "and" / "or" (each one adds another possible path)

A higher number means the function has more independent paths through
it, which usually means it is harder to test and understand.
"""

import ast


def calculate_complexity(source_code):
    """
    Calculate cyclomatic complexity for every function in the source code.

    Args:
        source_code (str): the full text of a Python file.

    Returns:
        dict: maps function name -> complexity score (int).

    Raises:
        SyntaxError: if source_code is not valid Python code.
    """
    tree = ast.parse(source_code)
    results = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            results[node.name] = _complexity_of_function(node)

    return results


def _complexity_of_function(function_node):
    """
    Walk through a single function's body and count decision points.

    We start at 1 (one path through the function with no branching at all)
    and add 1 for every decision point we find inside it.
    """
    complexity = 1

    for node in ast.walk(function_node):
        if isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While)):
            complexity += 1
        elif isinstance(node, ast.ExceptHandler):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            # A BoolOp like "a and b and c" has (number of values - 1)
            # boolean operators joining them, so it adds that many paths.
            complexity += len(node.values) - 1

    return complexity
