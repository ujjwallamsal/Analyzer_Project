"""
unused_variables.py

Finds variables that are assigned a value but never read afterwards,
within the same scope (either a function, or the top level of the file).

Scope note: each function has its own separate scope. A variable named
"value" in one function has nothing to do with a variable also named
"value" in a different function.

Out of scope (kept simple on purpose - see report assumptions):
- unused function parameters
- unused imports
- unused loop variables (e.g. "for i in range(10)")
"""

import ast


def find_unused_variables(source_code):
    """
    Find variables that are assigned but never used.

    Args:
        source_code (str): the full text of a Python file.

    Returns:
        list[dict]: one dict per unused variable, with keys
            "name" and "line" (the line of its first assignment).

    Raises:
        SyntaxError: if source_code is not valid Python code.
    """
    tree = ast.parse(source_code)
    violations = []

    # Start checking from the top level of the file (module scope).
    # This function will recursively check every function scope too.
    _check_scope(tree, violations)

    return violations


class _NameCollector(ast.NodeVisitor):
    """
    Walks through the statements of ONE scope (one function, or the
    module top level) and records:
    - every variable name that gets assigned to (and the line it
      first appears on)
    - every variable name that gets read

    It stops at the boundary of any nested function/class, because
    those are separate scopes and are handled separately.
    """

    def __init__(self):
        self.assigned = {}  # name -> line number of first assignment
        self.used = set()
        self.nested_functions = []

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            if node.id not in self.assigned:
                self.assigned[node.id] = node.lineno
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Remember this nested function so we can check it separately,
        # but do NOT recurse into it now (that would mix its variables
        # with the current scope's variables).
        self.nested_functions.append(node)

    def visit_AsyncFunctionDef(self, node):
        self.nested_functions.append(node)


def _check_scope(scope_node, violations):
    """
    Check one scope (a Module or a FunctionDef) for unused variables,
    then recursively check every function defined inside it.
    """
    collector = _NameCollector()

    for statement in scope_node.body:
        collector.visit(statement)

    for name, line in collector.assigned.items():
        if name not in collector.used:
            violations.append({"name": name, "line": line})

    for nested_function in collector.nested_functions:
        _check_scope(nested_function, violations)
