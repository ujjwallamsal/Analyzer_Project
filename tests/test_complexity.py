"""
Tests for analyzer.complexity

Cyclomatic complexity roughly measures how many independent paths exist
through a function. We calculate it as:

    complexity = 1 + (number of decision points)

Decision points are things like: if, elif, for, while, except,
and boolean "and"/"or" operators (each one adds another possible path).

A simple function with no branching has complexity 1.
Every "if", "for", "while", "except", "and", "or" adds 1.
"""

import pytest
from analyzer.complexity import calculate_complexity


def test_function_with_no_branches_has_complexity_one():
    """Normal case: straight-line code, no decisions, complexity = 1."""
    source = (
        "def add(a, b):\n"
        "    return a + b\n"
    )
    result = calculate_complexity(source)
    assert result["add"] == 1


def test_function_with_one_if_has_complexity_two():
    """Normal case: one 'if' adds exactly one path."""
    source = (
        "def check(x):\n"
        "    if x > 0:\n"
        "        return 'positive'\n"
        "    return 'non-positive'\n"
    )
    result = calculate_complexity(source)
    assert result["check"] == 2


def test_function_with_if_elif_else_and_loop():
    """Normal case: multiple decision points should all be counted.
    1 (base) + if + elif + for = 4
    """
    source = (
        "def classify(numbers):\n"
        "    for n in numbers:\n"
        "        if n > 0:\n"
        "            print('positive')\n"
        "        elif n < 0:\n"
        "            print('negative')\n"
        "        else:\n"
        "            print('zero')\n"
    )
    result = calculate_complexity(source)
    assert result["classify"] == 4


def test_boolean_operators_increase_complexity():
    """Normal case: 'and'/'or' each represent an extra logical path."""
    source = (
        "def is_valid(x, y):\n"
        "    if x > 0 and y > 0:\n"
        "        return True\n"
        "    return False\n"
    )
    result = calculate_complexity(source)
    # base 1 + if (1) + and (1) = 3
    assert result["is_valid"] == 3


def test_multiple_functions_are_reported_separately():
    """Normal case: each function gets its own complexity score."""
    source = (
        "def simple():\n"
        "    return 1\n"
        "\n"
        "def branching(x):\n"
        "    if x:\n"
        "        return 1\n"
        "    return 0\n"
    )
    result = calculate_complexity(source)
    assert result["simple"] == 1
    assert result["branching"] == 2


def test_empty_file_returns_empty_dict():
    """Boundary case: no functions at all."""
    result = calculate_complexity("")
    assert result == {}


def test_invalid_python_raises_syntax_error():
    """Invalid input: broken code should raise SyntaxError."""
    with pytest.raises(SyntaxError):
        calculate_complexity("def broken(:\n")


def test_except_block_increases_complexity():
    """Normal case: each 'except' block represents an extra path
    through the function, so it should add 1 to the complexity."""
    source = (
        "def safe_divide(a, b):\n"
        "    try:\n"
        "        return a / b\n"
        "    except ZeroDivisionError:\n"
        "        return 0\n"
    )
    result = calculate_complexity(source)
    # base 1 + except (1) = 2
    assert result["safe_divide"] == 2


def test_async_function_is_supported():
    """Edge case: async functions should be analyzed the same way as
    regular functions."""
    source = (
        "async def fetch(x):\n"
        "    if x:\n"
        "        return 1\n"
        "    return 0\n"
    )
    result = calculate_complexity(source)
    assert result["fetch"] == 2
