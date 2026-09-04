"""
Tests for analyzer.naming

Rules we are checking (standard PEP8 Python style):
- function and variable names should be snake_case (e.g. my_variable)
- class names should be PascalCase (e.g. MyClass)
"""

import pytest
from analyzer.naming import check_naming


def test_snake_case_function_name_is_fine():
    """Normal case: correctly named function should not be flagged."""
    source = "def calculate_total():\n    pass\n"
    violations = check_naming(source)
    assert violations == []


def test_camel_case_function_name_is_flagged():
    """Normal case: a camelCase function name breaks the naming rule."""
    source = "def calculateTotal():\n    pass\n"
    violations = check_naming(source)

    assert len(violations) == 1
    assert violations[0]["name"] == "calculateTotal"
    assert violations[0]["type"] == "function"


def test_pascal_case_class_name_is_fine():
    """Normal case: correctly named class should not be flagged."""
    source = "class BankAccount:\n    pass\n"
    violations = check_naming(source)
    assert violations == []


def test_lowercase_class_name_is_flagged():
    """Normal case: a lowercase class name breaks the naming rule."""
    source = "class bank_account:\n    pass\n"
    violations = check_naming(source)

    assert len(violations) == 1
    assert violations[0]["name"] == "bank_account"
    assert violations[0]["type"] == "class"


def test_snake_case_variable_is_fine():
    """Normal case: correctly named variable should not be flagged."""
    source = "total_amount = 10\n"
    violations = check_naming(source)
    assert violations == []


def test_camel_case_variable_is_flagged():
    """Normal case: camelCase variable name breaks the naming rule."""
    source = "totalAmount = 10\n"
    violations = check_naming(source)

    assert len(violations) == 1
    assert violations[0]["name"] == "totalAmount"
    assert violations[0]["type"] == "variable"


def test_single_letter_variable_names_are_allowed():
    """Boundary case: short names like 'i' or 'x' are common in loops
    and should not be flagged as violations."""
    source = "for i in range(10):\n    x = i\n"
    violations = check_naming(source)
    assert violations == []


def test_empty_file_has_no_violations():
    """Boundary case: an empty file has nothing to flag."""
    violations = check_naming("")
    assert violations == []


def test_invalid_python_raises_syntax_error():
    """Invalid input: broken Python code should raise SyntaxError."""
    with pytest.raises(SyntaxError):
        check_naming("def broken(:\n")


def test_violation_includes_line_number():
    """Each violation should tell the user which line to look at."""
    source = "\n\ndef badName():\n    pass\n"
    violations = check_naming(source)

    assert violations[0]["line"] == 3


def test_type_annotated_variable_is_checked():
    """Regression test: a type-annotated assignment (e.g. x: int = 5)
    is a different AST node (AnnAssign) from a plain assignment
    (Assign). An earlier version of this checker only looked at
    Assign nodes, so a badly-named annotated variable slipped through
    undetected even though the same name without a type hint was
    correctly flagged. This test locks in the fix."""
    source = "totalAmount: int = 10\n"
    violations = check_naming(source)

    assert len(violations) == 1
    assert violations[0]["name"] == "totalAmount"
    assert violations[0]["type"] == "variable"


def test_correctly_named_annotated_variable_is_not_flagged():
    """Normal case: a properly named annotated variable should not
    be flagged, same as a properly named plain assignment."""
    source = "total_amount: int = 10\n"
    violations = check_naming(source)
    assert violations == []


def test_short_annotated_variable_name_is_allowed():
    """Boundary case: the short-name exemption applies to annotated
    assignments too, e.g. 'x: int = 5' should not be flagged."""
    source = "x: int = 5\n"
    violations = check_naming(source)
    assert violations == []


def test_two_letter_function_name_is_allowed():
    """Boundary case: very short function names (like 'ok') are common
    and exempt, same rule as short variable names."""
    source = "def ok():\n    pass\n"
    violations = check_naming(source)
    assert violations == []
