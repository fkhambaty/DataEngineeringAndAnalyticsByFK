"""``python -m tools.course_qa`` runs the offline gate. ``shoot`` captures slides."""

from __future__ import annotations

import sys

from tools.course_qa.checks import main as check_main
from tools.course_qa.screenshots import main as shoot_main


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "shoot":
        return shoot_main(args[1:])
    if args and args[0] == "check":
        args = args[1:]
    return check_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
