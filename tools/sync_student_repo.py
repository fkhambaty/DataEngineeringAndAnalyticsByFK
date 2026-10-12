#!/usr/bin/env python3
"""Copy the public Meridian project into the nested student repository.

The instructor root is the parent of this tools directory, unless
MERIDIAN_INSTRUCTOR_ROOT or --source names another directory that contains
01_source_postgres and study/STUDENT_README.md.

The student root defaults to <instructor>/snowflake_dbt_airflow_python_byFK.
MERIDIAN_STUDENT_ROOT or --dest overrides it. An explicit destination inside
the instructor tree is accepted only when it is that nested repository.

--check prints the plan and exits 1 when the destination would change.
It does not create, modify, or delete anything.
--apply performs that plan. It never deletes the destination .git directory,
and it never removes local secrets or build artifacts.

The public README installed at the destination root is study/STUDENT_README.md.
The instructor README is not copied. The instructor-only gitignore line that
names the nested clone is dropped so the public ignore file stays portable.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

PUBLIC_DIRECTORIES = (
    "setup",
    "01_source_postgres",
    "02_ingestion_python",
    "03_snowflake",
    "04_dbt_meridian_dw",
    "05_airflow",
    "06_performance_lab",
    "07_data_modelling",
    "09_decisioning_python",
    "10_semantic_app",
    "11_platform_terraform",
    "12_case_studies",
    "tests",
    ".github",
    "study",
)

ARCHITECTURE_PATHS = (
    "00_architecture/DESIGN_DOC.md",
    "00_architecture/ARCHITECTURE_PROCESS.md",
    "00_architecture/OPERATIONS_RUNBOOK.md",
    "00_architecture/DR_RUNBOOK.md",
    "00_architecture/adr",
    "00_architecture/diagrams",
)

ROOT_FILES = (
    "requirements.txt",
    ".env.example",
    ".gitignore",
)

NESTED_NAME = "snowflake_dbt_airflow_python_byFK"
GITIGNORE_DROPPED_LINES = {f"{NESTED_NAME}/"}

EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".venv",
    "venv",
    "Videos",
    "Printouts",
    "include",
    "target",
    "dbt_packages",
    ".terraform",
    "__pycache__",
    ".pytest_cache",
    ".astro",
    "logs",
}

EXCLUDED_FILE_NAMES = {
    ".env",
    "profiles.yml",
    "airflow_settings.yaml",
    "test_course_release.py",
    ".user.yml",
    "credentials",
    "credentials.json",
    "credentials.yml",
    "credentials.yaml",
    ".DS_Store",
}

SENSITIVE_NAME_TOKENS = ("credential", "secret", "id_rsa", "id_ed25519")


def is_excluded(relative: Path) -> bool:
    """Return True when a relative path must never be copied or deleted."""
    if any(part in EXCLUDED_DIRECTORY_NAMES for part in relative.parts):
        return True
    name = relative.name
    lowered = name.lower()
    if name in EXCLUDED_FILE_NAMES:
        return True
    if lowered.startswith(".env") and "example" not in lowered:
        return True
    if ".tfstate" in lowered:
        return True
    if lowered.endswith((".pem", ".p8", ".pyc")):
        return True
    return any(token in lowered for token in SENSITIVE_NAME_TOKENS)


def is_git_metadata(relative: Path) -> bool:
    return ".git" in relative.parts


def assert_exclusion_rules() -> None:
    """Fail closed if a protected path would ever enter the copy plan."""
    excluded = (
        Path(".env"),
        Path("nested/.env"),
        Path(".env.local"),
        Path("secrets/credentials.json"),
        Path("04_dbt_meridian_dw/profiles.yml"),
        Path("05_airflow/airflow_settings.yaml"),
        Path("05_airflow/include/dbt/dbt_project.yml"),
        Path("04_dbt_meridian_dw/target/manifest.json"),
        Path("04_dbt_meridian_dw/dbt_packages/dbt_utils/dbt_project.yml"),
        Path("11_platform_terraform/.terraform/providers/x"),
        Path("11_platform_terraform/terraform.tfstate"),
        Path("11_platform_terraform/terraform.tfstate.backup"),
        Path("Videos/episode.mp4"),
        Path("Printouts/slide.pdf"),
        Path(".venv/bin/python"),
        Path("keys/account.pem"),
        Path("keys/snowflake.p8"),
        Path(".git/config"),
        Path("study/.git/HEAD"),
        Path("tests/test_course_release.py"),
    )
    allowed = (
        Path(".env.example"),
        Path("04_dbt_meridian_dw/profiles.yml.example"),
        Path("05_airflow/airflow_settings.yaml.example"),
        Path("study/index.html"),
        Path("00_architecture/DESIGN_DOC.md"),
        Path("requirements.txt"),
    )
    failures = [str(path) for path in excluded if not is_excluded(path)]
    failures += [str(path) for path in allowed if is_excluded(path)]
    if failures:
        raise SystemExit("exclusion self-test failed: " + ", ".join(failures))


def resolve_instructor_root(explicit: str | None) -> Path:
    if explicit:
        root = Path(explicit).expanduser().resolve()
    elif os.environ.get("MERIDIAN_INSTRUCTOR_ROOT"):
        root = Path(os.environ["MERIDIAN_INSTRUCTOR_ROOT"]).expanduser().resolve()
    else:
        root = Path(__file__).resolve().parent.parent
    if not (root / "01_source_postgres").is_dir():
        raise SystemExit(f"instructor root has no 01_source_postgres: {root}")
    template = root / "study" / "STUDENT_README.md"
    if not template.is_file():
        raise SystemExit(f"public README template missing: {template}")
    return root


def resolve_student_root(instructor: Path, explicit: str | None) -> Path:
    if explicit:
        dest = Path(explicit).expanduser().resolve()
    elif os.environ.get("MERIDIAN_STUDENT_ROOT"):
        dest = Path(os.environ["MERIDIAN_STUDENT_ROOT"]).expanduser().resolve()
    else:
        dest = (instructor / NESTED_NAME).resolve()
    if dest == instructor or instructor in dest.parents and dest != instructor / NESTED_NAME:
        try:
            relative = dest.relative_to(instructor)
        except ValueError:
            relative = None
        if relative != Path(NESTED_NAME):
            raise SystemExit(
                "destination inside the instructor tree must be "
                f"{instructor / NESTED_NAME}"
            )
    if dest in instructor.parents:
        raise SystemExit("destination contains the instructor root")
    return dest


def public_bytes(source: Path, relative: Path) -> bytes:
    data = (source / relative).read_bytes()
    if relative.as_posix() != ".gitignore":
        return data
    text = data.decode("utf-8")
    kept = [
        line
        for line in text.splitlines(keepends=True)
        if line.strip() not in GITIGNORE_DROPPED_LINES
    ]
    rendered = "".join(kept)
    if rendered and not rendered.endswith("\n"):
        rendered += "\n"
    return rendered.encode("utf-8")


def iter_source_files(source: Path, relative_root: Path):
    candidate = source / relative_root
    if not candidate.exists():
        return
    if candidate.is_file():
        if not candidate.is_symlink() and not is_excluded(relative_root):
            yield relative_root
        return
    for directory, dirnames, filenames in os.walk(candidate, followlinks=False):
        current = Path(directory)
        relative_dir = current.relative_to(source)
        dirnames[:] = [
            name
            for name in dirnames
            if not is_excluded(relative_dir / name) and not (current / name).is_symlink()
        ]
        for filename in filenames:
            relative = relative_dir / filename
            path = source / relative
            if path.is_symlink() or is_excluded(relative) or is_git_metadata(relative):
                continue
            yield relative


def desired_payload(source: Path) -> dict[str, bytes]:
    relative_paths: list[Path] = []
    for directory in PUBLIC_DIRECTORIES:
        relative_paths.extend(iter_source_files(source, Path(directory)))
    for architecture in ARCHITECTURE_PATHS:
        relative_paths.extend(iter_source_files(source, Path(architecture)))
    for filename in ROOT_FILES:
        relative_paths.extend(iter_source_files(source, Path(filename)))
    payload = {
        relative.as_posix(): public_bytes(source, relative) for relative in relative_paths
    }
    payload["README.md"] = (source / "study" / "STUDENT_README.md").read_bytes()
    illegal = [path for path in payload if is_excluded(Path(path)) or is_git_metadata(Path(path))]
    if illegal:
        raise SystemExit("plan included a protected path: " + ", ".join(illegal))
    return payload


def destination_files(dest: Path, managed: set[str]) -> dict[str, Path]:
    """Files already inside managed prefixes, ignoring secrets and .git."""
    found: dict[str, Path] = {}
    if not dest.is_dir():
        return found
    prefixes = {path.split("/", 1)[0] for path in managed}
    prefixes.update(path for path in managed if "/" not in path)
    for prefix in sorted(prefixes):
        current = dest / prefix
        if not current.exists() or current.is_symlink():
            continue
        if current.is_file():
            relative = Path(prefix)
            if not is_excluded(relative) and not is_git_metadata(relative):
                found[prefix] = current
            continue
        for directory, dirnames, filenames in os.walk(current, followlinks=False):
            relative_dir = Path(directory).relative_to(dest)
            dirnames[:] = [
                name
                for name in dirnames
                if name != ".git" and not is_excluded(relative_dir / name)
            ]
            for filename in filenames:
                relative = relative_dir / filename
                path = dest / relative
                if path.is_symlink() or is_excluded(relative) or is_git_metadata(relative):
                    continue
                found[relative.as_posix()] = path
    return found


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_plan(source: Path, dest: Path) -> tuple[list[str], list[str], list[str], int]:
    desired = desired_payload(source)
    existing = destination_files(dest, set(desired))
    adds: list[str] = []
    updates: list[str] = []
    unchanged = 0
    for relative, data in sorted(desired.items()):
        target = dest / relative
        if relative not in existing:
            adds.append(relative)
            continue
        if digest(target.read_bytes()) == digest(data):
            unchanged += 1
        else:
            updates.append(relative)
    deletes = sorted(set(existing) - set(desired))
    protected = [path for path in deletes if is_excluded(Path(path)) or is_git_metadata(Path(path))]
    if protected:
        raise SystemExit("refusing to delete protected paths: " + ", ".join(protected))
    return adds, updates, deletes, unchanged


def print_paths(label: str, paths: list[str], limit: int) -> None:
    if not paths:
        return
    print(f"{label} ({len(paths)}):")
    for path in paths[:limit]:
        print(f"  {path}")
    remaining = len(paths) - limit
    if remaining > 0:
        print(f"  ... {remaining} more")


def git_dir_status(dest: Path) -> str:
    git_dir = dest / ".git"
    if git_dir.is_dir():
        return f"nested .git present at {git_dir} (preserved)"
    if not dest.exists():
        return "destination is absent; .git will not be created or deleted by this tool"
    return "destination has no .git directory; this tool will not create or delete one"


def apply_plan(source: Path, dest: Path, adds: list[str], updates: list[str], deletes: list[str]) -> None:
    git_dir = (dest / ".git").resolve()
    desired = desired_payload(source)
    dest.mkdir(parents=True, exist_ok=True)
    for relative in deletes:
        target = (dest / relative).resolve()
        if target == git_dir or git_dir in target.parents:
            raise SystemExit(f"refusing to delete nested git metadata: {target}")
        if is_excluded(Path(relative)) or is_git_metadata(Path(relative)):
            raise SystemExit(f"refusing to delete protected path: {relative}")
        target.unlink()
    for relative in adds + updates:
        target = dest / relative
        resolved = target.resolve() if target.exists() else target
        if target.exists() and (resolved == git_dir or git_dir in resolved.parents):
            raise SystemExit(f"refusing to write inside nested git metadata: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".sync-tmp")
        temporary.write_bytes(desired[relative])
        temporary.replace(target)
    for relative in deletes:
        directory = (dest / relative).parent
        while directory != dest and directory.is_dir():
            try:
                directory.rmdir()
            except OSError:
                break
            directory = directory.parent


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="print the plan and modify nothing")
    mode.add_argument("--apply", action="store_true", help="copy the plan; never delete .git")
    parser.add_argument("--source", help="instructor root (default: parent of tools/)")
    parser.add_argument("--dest", help="student repository root")
    parser.add_argument("--limit", type=int, default=40, help="paths to print per action")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    assert_exclusion_rules()
    source = resolve_instructor_root(args.source)
    dest = resolve_student_root(source, args.dest)
    adds, updates, deletes, unchanged = build_plan(source, dest)
    mode = "apply" if args.apply else "check"
    print("Meridian student sync")
    print(f"  instructor: {source}")
    print(f"  student:    {dest}")
    print(f"  mode:       {mode}")
    print("exclusion self-test: ok")
    print(git_dir_status(dest))
    print(
        f"plan: {len(adds)} add, {len(updates)} update, "
        f"{len(deletes)} delete, {unchanged} unchanged"
    )
    print("README.md source: study/STUDENT_README.md")
    print_paths("would add", adds, args.limit)
    print_paths("would update", updates, args.limit)
    print_paths("would delete", deletes, args.limit)
    print(
        "omitted from every plan: .git .env credentials .venv Videos Printouts "
        "include/ profiles.yml airflow_settings.yaml target dbt_packages "
        ".terraform tfstate"
    )
    if args.check:
        print("check only: destination was not modified")
        return 0 if not adds and not updates and not deletes else 1
    apply_plan(source, dest, adds, updates, deletes)
    print("apply complete; nested .git was not deleted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
