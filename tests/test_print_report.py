"""
Tests for analyzer.report.print_report

print_report() only prints to the screen, it does not return anything
useful to check. So instead of checking a return value, we capture
what gets printed (using pytest's built-in "capsys" fixture) and check
that the important information shows up in the output.
"""

from analyzer.report import analyze_source, print_report


def test_print_report_shows_error_message(capsys):
    """When the report contains an error, print_report should show it
    clearly instead of trying to print metrics that don't exist."""
    report = analyze_source("def broken(:\n")
    print_report(report)

    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "syntax" in captured.out.lower()


def test_print_report_shows_all_sections_for_valid_code(capsys):
    """Normal case: a valid file should print every section of the
    report, including cases where a section has no findings."""
    source = (
        "def calculateTotal(items):\n"
        "    unused = 0\n"
        "    total = 0\n"
        "    for item in items:\n"
        "        total = total + item\n"
        "    return total\n"
    )
    report = analyze_source(source)
    print_report(report)

    captured = capsys.readouterr()
    assert "Code Metrics" in captured.out
    assert "Cyclomatic Complexity" in captured.out
    assert "Unused Variables" in captured.out
    assert "Duplicate Lines" in captured.out
    assert "Naming Violations" in captured.out
    assert "unused" in captured.out
    assert "calculateTotal" in captured.out


def test_print_report_shows_unused_variable_and_duplicate_line_details(capsys):
    """Normal case: when findings DO exist, the printed report should
    include the actual details (not just the section heading)."""
    source = (
        "print('hi')\n"
        "unused_here = 5\n"
        "print('hi')\n"
    )
    report = analyze_source(source)
    print_report(report)

    captured = capsys.readouterr()
    assert "unused_here" in captured.out
    assert "print('hi')" in captured.out
    assert "appears on lines" in captured.out


def test_print_report_handles_empty_findings(capsys):
    """Boundary case: when there are no functions and nothing to flag,
    print_report should say so instead of printing nothing / crashing."""
    report = analyze_source("x = 1\n")
    print_report(report)

    captured = capsys.readouterr()
    assert "No functions found." in captured.out
    assert "None found." in captured.out
