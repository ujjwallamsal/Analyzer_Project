"""
duplicate_code.py

Finds lines of code that appear more than once in a file (exact,
line-by-line matches only).

Blank lines and comment-only lines are ignored on purpose, since it is
normal for those to repeat often and it would not be a useful warning.

Note: this is a simple line-based check, not a "semantic" duplicate
checker. Two lines that do the same thing but are written differently
(e.g. "x = a + b" vs "x = b + a") will NOT be detected as duplicates.
This limitation is intentional, to keep the tool easy to understand.
"""


def find_duplicate_lines(source_code):
    """
    Find lines that appear more than once in the source code.

    Args:
        source_code (str): the full text of a Python file. Does not
            need to be valid Python, since this check only looks at
            plain text lines rather than parsing the code.

    Returns:
        list[dict]: one dict per duplicated line, with keys:
            "line_text" (the line, with whitespace trimmed)
            "line_numbers" (list of every line number it appears on)
    """
    lines = source_code.splitlines()

    # Maps a cleaned-up line of code -> list of line numbers it appears on.
    line_occurrences = {}

    for line_number, raw_line in enumerate(lines, start=1):
        cleaned_line = raw_line.strip()

        # Skip blank lines and comment-only lines - repeating these
        # is normal and not a sign of duplicated code.
        if cleaned_line == "" or cleaned_line.startswith("#"):
            continue

        if cleaned_line not in line_occurrences:
            line_occurrences[cleaned_line] = []
        line_occurrences[cleaned_line].append(line_number)

    duplicates = []
    for line_text, line_numbers in line_occurrences.items():
        if len(line_numbers) > 1:
            duplicates.append({"line_text": line_text, "line_numbers": line_numbers})

    return duplicates
