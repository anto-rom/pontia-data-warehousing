"""
Pytest conftest for Data Warehouse course activities.
"""
import pytest


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print a formatted grade summary table."""
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))

    terminalreporter.write_sep("=", "GRADE SUMMARY")
    terminalreporter.write_line(f"  Tests passed: {passed}")
    terminalreporter.write_line(f"  Tests failed: {failed}")
    terminalreporter.write_sep("=")
