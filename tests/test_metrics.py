"""
Tests for analyzer.metrics

These tests are written BEFORE the implementation (Test-Driven Development).
We describe the behaviour we want first, then write metrics.py to make
these tests pass.
"""

import pytest
from analyzer.metrics import calculate_metrics


def test_counts_lines_in_simple_code():
    """Normal case: a small script with code, a blank line and a comment."""
    source = (
        "x = 1\n"
        "\n"
        "# this is a comment\n"
        "y = 2\n"
    )
    result = calculate_metrics(source)

    assert result["total_lines"] == 4
    assert result["blank_lines"] == 1
    assert result["comment_lines"] == 1
    assert result["code_lines"] == 2


def test_counts_functions_and_classes():
    """Normal case: file with one function and one class."""
    source = (
        "def greet():\n"
        "    return 'hi'\n"
        "\n"
        "class Animal:\n"
        "    pass\n"
    )
    result = calculate_metrics(source)

    assert result["function_count"] == 1
    assert result["class_count"] == 1


def test_empty_file_returns_zero_counts():
    """Boundary case: an empty file should not crash, everything is 0."""
    result = calculate_metrics("")

    assert result["total_lines"] == 0
    assert result["code_lines"] == 0
    assert result["function_count"] == 0
    assert result["class_count"] == 0


def test_file_with_only_comments_and_blank_lines():
    """Boundary case: no real code at all, only comments/blank lines."""
    source = (
        "# comment one\n"
        "\n"
        "# comment two\n"
    )
    result = calculate_metrics(source)

    assert result["code_lines"] == 0
    assert result["comment_lines"] == 2
    assert result["blank_lines"] == 1


def test_invalid_python_raises_syntax_error():
    """Invalid input: code that is not valid Python should raise SyntaxError,
    not silently return a wrong answer."""
    broken_source = "def broken(:\n    pass\n"

    with pytest.raises(SyntaxError):
        calculate_metrics(broken_source)


def test_nested_function_is_still_counted():
    """Edge case: a function defined inside another function should still
    be counted as a function."""
    source = (
        "def outer():\n"
        "    def inner():\n"
        "        pass\n"
        "    return inner\n"
    )
    result = calculate_metrics(source)

    assert result["function_count"] == 2
