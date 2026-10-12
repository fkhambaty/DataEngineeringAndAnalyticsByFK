#!/usr/bin/env python3
"""Capture final-step deck screenshots from any working directory."""

from __future__ import annotations

import sys
from pathlib import Path


def _put_repo_on_path() -> None:
    here = Path(__file__).resolve().parent
    for candidate in (here, *here.parents):
        if (candidate / "course" / "show.html").is_file():
            root = str(candidate)
            if root not in sys.path:
                sys.path.insert(0, root)
            return
    raise SystemExit("Could not resolve the repository root (course/show.html).")


if __name__ == "__main__":
    _put_repo_on_path()
    from tools.course_qa.screenshots import main

    raise SystemExit(main())
