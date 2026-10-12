"""Repeatable QA for the Meridian course player."""

from tools.course_qa.checks import Finding, run_checks
from tools.course_qa.paths import repo_root

__all__ = ["Finding", "repo_root", "run_checks"]
