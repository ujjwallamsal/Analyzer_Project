"""
__main__.py

Lets the analyzer be run from the command line like this:

    python -m analyzer path/to/your_file.py

This file is intentionally very small - all the real logic lives in
report.py and the individual checker modules, so it can be unit tested
directly without needing to run the whole program.
"""

import sys

from analyzer.report import analyze_file, print_report


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m analyzer <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    report = analyze_file(file_path)
    print_report(report)

    if report["error"] is not None:
        sys.exit(1)


if __name__ == "__main__":
    main()
