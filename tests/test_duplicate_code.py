"""
Tests for analyzer.duplicate_code

This checker looks for lines of code that appear more than once in the
file. Blank lines and comment-only lines are ignored, because it is
completely normal for those to repeat (e.g. many blank lines, or the
same short comment used in different places).

This is a simple, line-based duplicate checker. It does not understand
that two pieces of code do the "same thing" written differently -
it only detects exact, identical lines. This is stated as a limitation
in the report.
"""

import pytest
from analyzer.duplicate_code import find_duplicate_lines


def test_no_duplicates_in_unique_code():
    """Normal case: every line is different, nothing should be flagged."""
    source = (
        "a = 1\n"
        "b = 2\n"
        "c = 3\n"
    )
    result = find_duplicate_lines(source)
    assert result == []


def test_duplicate_line_is_detected():
    """Normal case: the same line of code appears twice."""
    source = (
        "print('hello')\n"
        "x = 1\n"
        "print('hello')\n"
    )
    result = find_duplicate_lines(source)

    assert len(result) == 1
    assert result[0]["line_text"] == "print('hello')"
    assert result[0]["line_numbers"] == [1, 3]


def test_blank_lines_are_not_flagged_as_duplicates():
    """Boundary case: many blank lines should not be treated as
    duplicate code, since that is normal and not a real code smell."""
    source = "a = 1\n\n\n\nb = 2\n"
    result = find_duplicate_lines(source)
    assert result == []


def test_repeated_comments_are_not_flagged():
    """Boundary case: the same short comment used multiple times is
    normal and should not be reported as duplicate code."""
    source = (
        "# TODO: fix this\n"
        "a = 1\n"
        "# TODO: fix this\n"
        "b = 2\n"
    )
    result = find_duplicate_lines(source)
    assert result == []


def test_line_repeated_three_times_lists_all_line_numbers():
    """Normal case: a line duplicated more than twice should list
    every occurrence, not just the first two."""
    source = (
        "count = count + 1\n"
        "a = 1\n"
        "count = count + 1\n"
        "b = 2\n"
        "count = count + 1\n"
    )
    result = find_duplicate_lines(source)

    assert len(result) == 1
    assert result[0]["line_numbers"] == [1, 3, 5]


def test_empty_file_has_no_duplicates():
    """Boundary case: nothing to compare in an empty file."""
    result = find_duplicate_lines("")
    assert result == []


def test_leading_whitespace_differences_still_count_as_duplicate():
    """Edge case: the same statement indented differently (e.g. inside
    two different functions) is still the same logical line, so it
    should be counted as a duplicate."""
    source = (
        "def a():\n"
        "    return None\n"
        "def b():\n"
        "    return None\n"
    )
    result = find_duplicate_lines(source)

    assert len(result) == 1
    assert result[0]["line_text"] == "return None"
