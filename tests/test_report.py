"""
Tests for analyzer.report

This module ties all the individual checks together into one report,
and is responsible for handling real-world problems gracefully:
- a file path that does not exist
- a file that is not valid Python

These are the "invalid input" scenarios from the assignment's
requirements analysis (Task 1).
"""

import pytest
from analyzer.report import analyze_file, analyze_source


def test_analyze_source_combines_all_checks():
    """Normal case: analyzing a valid piece of source code returns a
    report containing results from every checker."""
    source = (
        "def calculateTotal(items):\n"
        "    unused = 0\n"
        "    total = 0\n"
        "    for item in items:\n"
        "        total = total + item\n"
        "    return total\n"
    )
    report = analyze_source(source)

    assert "metrics" in report
    assert "complexity" in report
    assert "unused_variables" in report
    assert "duplicate_lines" in report
    assert "naming_violations" in report

    # Spot-check that each checker actually ran and found what we expect.
    assert report["metrics"]["function_count"] == 1
    assert report["complexity"]["calculateTotal"] == 2
    assert any(v["name"] == "unused" for v in report["unused_variables"])
    assert any(v["name"] == "calculateTotal" for v in report["naming_violations"])


def test_analyze_source_with_invalid_python_returns_error():
    """Invalid input: broken Python should not crash the whole program.
    Instead the report should clearly say there was a syntax error."""
    report = analyze_source("def broken(:\n    pass\n")

    assert report["error"] is not None
    assert "syntax" in report["error"].lower()


def test_analyze_file_with_missing_file_returns_error():
    """Invalid input: a file path that does not exist should be handled
    with a clear error message, not an unhandled exception."""
    report = analyze_file("this_file_does_not_exist.py")

    assert report["error"] is not None
    assert "not found" in report["error"].lower()


def test_analyze_file_reads_and_analyzes_real_file(tmp_path):
    """Normal case: analyzing an actual file on disk works end-to-end."""
    file_path = tmp_path / "sample.py"
    file_path.write_text("def add(a, b):\n    return a + b\n")

    report = analyze_file(str(file_path))

    assert report["error"] is None
    assert report["metrics"]["function_count"] == 1


def test_empty_source_produces_a_clean_empty_report():
    """Boundary case: an empty file should produce a valid report with
    all-zero/empty results, not an error."""
    report = analyze_source("")

    assert report["error"] is None
    assert report["metrics"]["total_lines"] == 0
    assert report["complexity"] == {}
    assert report["unused_variables"] == []
    assert report["duplicate_lines"] == []
    assert report["naming_violations"] == []
