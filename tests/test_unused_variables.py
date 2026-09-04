"""
Tests for analyzer.unused_variables

A variable is "unused" if it is assigned a value but that value is
never read again anywhere in the same function (or at module level).

We only check simple assignments like "x = 5". We do not try to track
unused function parameters, unused imports, or unused loop variables,
since those follow different rules and are out of scope for this
simple checker (see assumptions in the report).
"""

import pytest
from analyzer.unused_variables import find_unused_variables


def test_used_variable_is_not_flagged():
    """Normal case: variable is assigned and then used."""
    source = (
        "def total():\n"
        "    x = 5\n"
        "    return x\n"
    )
    result = find_unused_variables(source)
    assert result == []


def test_unused_variable_is_flagged():
    """Normal case: variable is assigned but never read."""
    source = (
        "def total():\n"
        "    x = 5\n"
        "    y = 10\n"
        "    return y\n"
    )
    result = find_unused_variables(source)

    assert len(result) == 1
    assert result[0]["name"] == "x"


def test_variable_used_only_in_another_function_is_still_flagged():
    """Normal case: each function has its own scope. A variable assigned
    in one function is not considered 'used' just because a
    same-named variable is used in a different function."""
    source = (
        "def first():\n"
        "    value = 1\n"
        "\n"
        "def second():\n"
        "    value = 2\n"
        "    return value\n"
    )
    result = find_unused_variables(source)

    assert len(result) == 1
    assert result[0]["name"] == "value"
    assert result[0]["line"] == 2


def test_reassigned_variable_used_after_is_not_flagged():
    """Normal case: variable is reassigned and the final value is used."""
    source = (
        "def total():\n"
        "    x = 5\n"
        "    x = x + 1\n"
        "    return x\n"
    )
    result = find_unused_variables(source)
    assert result == []


def test_module_level_unused_variable_is_flagged():
    """Normal case: unused variables at the top level of the file
    (outside any function) should also be detected."""
    source = "unused_value = 42\n"
    result = find_unused_variables(source)

    assert len(result) == 1
    assert result[0]["name"] == "unused_value"


def test_empty_file_has_no_unused_variables():
    """Boundary case: nothing to flag in an empty file."""
    result = find_unused_variables("")
    assert result == []


def test_invalid_python_raises_syntax_error():
    """Invalid input: broken code should raise SyntaxError."""
    with pytest.raises(SyntaxError):
        find_unused_variables("def broken(:\n")


def test_async_function_scope_is_checked_separately():
    """Edge case: async functions should get their own scope, just
    like regular functions."""
    source = (
        "async def fetch():\n"
        "    unused = 1\n"
        "    return 2\n"
    )
    result = find_unused_variables(source)

    assert len(result) == 1
    assert result[0]["name"] == "unused"
