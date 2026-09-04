"""
naming.py

Checks Python source code against basic PEP8 naming conventions:
- functions and variables should be written in snake_case
- classes should be written in PascalCase

We use "re" (regular expressions) to check the shape of each name,
and "ast" to find where each name is defined in the code.
"""

import ast
import re

# A snake_case name is all lowercase letters/digits/underscores,
# and must start with a letter or underscore (not a digit).
SNAKE_CASE_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*$")

# A PascalCase name starts with an uppercase letter, and contains only
# letters and digits after that (no underscores).
PASCAL_CASE_PATTERN = re.compile(r"^[A-Z][a-zA-Z0-9]*$")

# Very short names (1-2 characters) are common and accepted in Python
# for things like loop counters (i, j, x, dx) so we do not flag these.
SHORT_NAME_MAX_LENGTH = 2


def check_naming(source_code):
    """
    Check a string of Python source code for naming convention violations.

    Args:
        source_code (str): the full text of a Python file.

    Returns:
        list[dict]: one dict per violation, each with keys:
            "name" (the bad name), "type" ("function"/"class"/"variable"),
            "line" (line number where it was defined).

    Raises:
        SyntaxError: if source_code is not valid Python code.
    """
    tree = ast.parse(source_code)
    violations = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _check_function_name(node, violations)
        elif isinstance(node, ast.ClassDef):
            _check_class_name(node, violations)
        elif isinstance(node, ast.Assign):
            _check_assigned_variable_names(node, violations)
        elif isinstance(node, ast.AnnAssign):
            _check_annotated_variable_name(node, violations)

    return violations


def _check_function_name(node, violations):
    """Add a violation if the function name is not snake_case."""
    name = node.name
    if _is_short_name(name):
        return
    if not SNAKE_CASE_PATTERN.match(name):
        violations.append({"name": name, "type": "function", "line": node.lineno})


def _check_class_name(node, violations):
    """Add a violation if the class name is not PascalCase."""
    name = node.name
    if not PASCAL_CASE_PATTERN.match(name):
        violations.append({"name": name, "type": "class", "line": node.lineno})


def _check_assigned_variable_names(node, violations):
    """
    Add a violation for each variable being assigned that is not
    snake_case, e.g. "totalAmount = 10".

    An assignment can target more than one name at once
    (for example: a = b = 5), so we loop over node.targets.
    """
    for target in node.targets:
        if isinstance(target, ast.Name):
            name = target.id
            if _is_short_name(name):
                continue
            if not SNAKE_CASE_PATTERN.match(name):
                violations.append(
                    {"name": name, "type": "variable", "line": node.lineno}
                )


def _check_annotated_variable_name(node, violations):
    """
    Add a violation for a type-annotated assignment that is not
    snake_case, e.g. "totalAmount: int = 10".

    Python represents this as ast.AnnAssign, a different node type
    from a plain assignment (ast.Assign), so it needs its own check.
    Without this, a type-annotated variable could break naming rules
    and never be flagged, even though "totalAmount = 10" (no type
    hint) would be caught by _check_assigned_variable_names above.
    """
    if isinstance(node.target, ast.Name):
        name = node.target.id
        if _is_short_name(name):
            return
        if not SNAKE_CASE_PATTERN.match(name):
            violations.append({"name": name, "type": "variable", "line": node.lineno})


def _is_short_name(name):
    """Return True if the name is short enough to be exempt (e.g. 'i', 'x')."""
    return len(name) <= SHORT_NAME_MAX_LENGTH