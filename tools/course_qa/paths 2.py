"""Resolve the course repository without a hardcoded home directory."""

from __future__ import annotations

from pathlib import Path


def repo_root(start: Path | None = None) -> Path:
    """Walk upward from this package until ``course/show.html`` is found.

    ``start`` may be a file or a directory. The default start is this file, so
    the checkout root is found whether the command is launched from the repo,
    from ``tools/course_qa``, or via ``python -m``.
    """
    here = (start or Path(__file__)).resolve()
    if here.is_file():
        here = here.parent
    for candidate in (here, *here.parents):
        if (candidate / "course" / "show.html").is_file():
            return candidate
    anchor = start or Path(__file__)
    raise FileNotFoundError(f"course/show.html not found above {anchor}")
