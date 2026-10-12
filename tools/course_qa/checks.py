"""Offline release checks for the decks declared in ``course/show.html``."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path

from tools.course_qa.catalog import CatalogError, Deck, declared_episode, parse_catalog, slide_steps
from tools.course_qa.paths import repo_root

_PUBLIC_REPO_NAME = "snowflake_dbt_airflow_python_byFK"
_DBT_PREFIXES = ("models/", "macros/", "analyses/", "snapshots/", "seeds/")
_PLACEHOLDER_ACCOUNTS = {"xy12345", "xy12345.ap-south-1"}

# Uppercase org-account locators. CSS identifiers are lowercase, so they do not match.
_ACCOUNT_RE = re.compile(r"\b[A-Z][A-Z0-9]{5,12}-[A-Z][A-Z0-9]{4,12}\b")
# Locator plus cloud region, except the documented placeholder xy12345.ap-south-1.
_REGION_ACCOUNT_RE = re.compile(r"\b(?!xy12345\.)[A-Za-z][A-Za-z0-9]{5,10}\.[a-z]{2}-[a-z0-9]+-\d\b")
_ASSIGNMENT_RE = re.compile(r"SNOWFLAKE_ACCOUNT\s*=\s*([^\s'\"<>]+)")
_HOME_RE = re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\Users\\)[^\s'\"<>]+")
_PRIVATE_KEY_RE = re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")


@dataclass(frozen=True)
class Finding:
    code: str
    deck_id: str
    detail: str

    def format(self) -> str:
        where = self.deck_id or "course"
        return f"{where} {self.code}: {self.detail}"


def run_checks(repo: Path) -> list[Finding]:
    """Check every catalog deck. The result is empty when the gate passes."""
    repo = repo.resolve()
    show_path = repo / "course" / "show.html"
    if not show_path.is_file():
        return [Finding("catalog", "", f"missing {show_path}")]
    show_html = show_path.read_text(encoding="utf-8")
    try:
        decks = parse_catalog(show_html)
    except CatalogError as exc:
        return [Finding("catalog", "", str(exc))]

    findings: list[Finding] = []
    seen_ids: set[str] = set()
    for deck in decks:
        if deck.deck_id in seen_ids:
            findings.append(Finding("catalog", deck.deck_id, "duplicate episode id"))
        seen_ids.add(deck.deck_id)
        html_path = deck.html_path(repo)
        try:
            html_path.relative_to(repo)
        except ValueError:
            findings.append(Finding("missing-deck", deck.deck_id, f"{deck.relpath} escapes the repository"))
            continue
        if not html_path.is_file():
            findings.append(Finding("missing-deck", deck.deck_id, f"missing {deck.relpath}"))
            continue
        html = html_path.read_text(encoding="utf-8")
        findings.extend(_section_findings(deck, html))
        findings.extend(_episode_findings(deck, html))
        findings.extend(_path_findings(repo, deck.deck_id, html))
        findings.extend(_forbidden_findings(repo, deck.deck_id, html))
        findings.extend(_link_findings(repo, deck.deck_id, html_path, html))

    findings.extend(_forbidden_findings(repo, "show", show_html))
    findings.extend(_link_findings(repo, "show", show_path, show_html))
    for name in ("opening.html", "pictures.html", "code.html"):
        support_path = repo / "course" / "show" / name
        if not support_path.is_file():
            findings.append(Finding("missing-course-page", "show", f"missing show/{name}"))
            continue
        support_html = support_path.read_text(encoding="utf-8")
        findings.extend(_forbidden_findings(repo, f"show/{name}", support_html))
        findings.extend(_link_findings(repo, f"show/{name}", support_path, support_html))
    return findings


def _section_findings(deck: Deck, html: str) -> list[Finding]:
    actual = len(slide_steps(html))
    if actual == deck.scenes:
        return []
    return [
        Finding(
            "section-count",
            deck.deck_id,
            f"catalog scenes={deck.scenes} but {deck.relpath} has {actual} section.s slides",
        )
    ]


def _episode_findings(deck: Deck, html: str) -> list[Finding]:
    declared = declared_episode(html)
    if declared is None or declared == deck.deck_id:
        return []
    return [
        Finding(
            "episode-id",
            deck.deck_id,
            f'{deck.relpath} data-episode="{declared}" does not match catalog id "{deck.deck_id}"',
        )
    ]


def _project_roots(repo: Path) -> list[str]:
    roots: list[str] = []
    for child in sorted(repo.iterdir()):
        if child.is_dir() and re.fullmatch(r"\d{2}_[A-Za-z0-9_]+", child.name):
            roots.append(child.name)
    if (repo / "setup").is_dir():
        roots.append("setup")
    return roots


def _dbt_dir(repo: Path) -> Path | None:
    for child in sorted(repo.iterdir()):
        if child.is_dir() and (child / "dbt_project.yml").is_file():
            return child
    return None


def _path_pattern(roots: list[str]) -> re.Pattern[str] | None:
    if not roots:
        return None
    ordered = sorted(roots, key=len, reverse=True)
    return re.compile(r"(?<![\w./-])(?:" + "|".join(re.escape(root) for root in ordered) + r")(?:/[\w.+-]+)+")


_DBT_PATH_RE = re.compile(
    r"(?<![\w./-])(?:models|macros|analyses|snapshots|seeds)(?:/[\w.+-]+)+"
)


def _clean_ref(raw: str) -> str:
    ref = raw.strip().strip("`'\"")
    ref = ref.rstrip(".,);:\"'`")
    while ref.endswith("/"):
        ref = ref[:-1]
    return ref


def _is_generated_env(ref: str) -> bool:
    return Path(ref).name == ".env"


def _has_file_suffix(ref: str) -> bool:
    name = Path(ref).name
    if name.startswith(".") and name.count(".") == 1:
        return True
    return Path(name).suffix != ""


def _prefix_match(directory: Path, stem: str) -> bool:
    if len(stem) < 2 or not directory.is_dir():
        return False
    return any(child.name.startswith(stem) and child.name != stem and not child.name.startswith(".") for child in directory.iterdir())


def _resolve_reference(base: Path, ref: str, repo: Path) -> str | None:
    """Return a finding code when ``ref`` does not resolve under ``base``, else None."""
    candidate = (base / ref).resolve()
    try:
        candidate.relative_to(repo if base == repo else base.resolve())
    except ValueError:
        return "missing-project-path"
    if _is_generated_env(ref) and (repo / ".env.example").is_file():
        return None
    if candidate.exists():
        return None
    if not _has_file_suffix(ref) and _prefix_match(candidate.parent, candidate.name):
        return None
    if _has_file_suffix(ref):
        return "missing-student-file"
    return "missing-project-path"


def _path_findings(repo: Path, deck_id: str, html: str) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[str, str]] = set()
    pattern = _path_pattern(_project_roots(repo))
    refs: list[tuple[str, str]] = []
    if pattern is not None:
        refs.extend(("repo", match.group(0)) for match in pattern.finditer(html))
    dbt = _dbt_dir(repo)
    if dbt is not None:
        refs.extend(("dbt", match.group(0)) for match in _DBT_PATH_RE.finditer(html))
    for kind, raw in refs:
        ref = _clean_ref(raw)
        if not ref or (kind, ref) in seen:
            continue
        if kind == "dbt" and not ref.startswith(_DBT_PREFIXES):
            continue
        seen.add((kind, ref))
        base = dbt if kind == "dbt" and dbt is not None else repo
        code = _resolve_reference(base, ref, repo)
        if code is None:
            continue
        where = "dbt project" if kind == "dbt" else "repository"
        findings.append(Finding(code, deck_id, f"{ref} is not in the {where}"))
    return findings


def _forbidden_findings(repo: Path, deck_id: str, html: str) -> list[Finding]:
    findings: list[Finding] = []
    for match in _HOME_RE.finditer(html):
        findings.append(Finding("forbidden-identity", deck_id, f"local home path {match.group(0)}"))
    for match in _PRIVATE_KEY_RE.finditer(html):
        findings.append(Finding("forbidden-identity", deck_id, "private key block"))
    for match in _ACCOUNT_RE.finditer(html):
        token = match.group(0)
        if token.lower() not in _PLACEHOLDER_ACCOUNTS:
            findings.append(Finding("forbidden-identity", deck_id, f"account locator {token}"))
    for match in _REGION_ACCOUNT_RE.finditer(html):
        token = match.group(0)
        if token.lower() not in _PLACEHOLDER_ACCOUNTS:
            findings.append(Finding("forbidden-identity", deck_id, f"account locator {token}"))
    for match in _ASSIGNMENT_RE.finditer(html):
        token = match.group(1).strip().rstrip(".,);")
        if token.lower() not in _PLACEHOLDER_ACCOUNTS:
            findings.append(Finding("forbidden-identity", deck_id, f"SNOWFLAKE_ACCOUNT={token}"))
    checkout = repo.name
    if checkout and checkout not in {".", _PUBLIC_REPO_NAME} and checkout in html:
        findings.append(Finding("forbidden-identity", deck_id, f"local checkout name {checkout}"))
    return _unique(findings)


def _unique(findings: list[Finding]) -> list[Finding]:
    seen: set[Finding] = set()
    ordered: list[Finding] = []
    for finding in findings:
        if finding in seen:
            continue
        seen.add(finding)
        ordered.append(finding)
    return ordered


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        name = tag.lower()
        if name in {"script", "style"}:
            self._skip += 1
            if name != "script":
                return
        if self._skip and name != "script":
            return
        if self._skip and name == "script":
            self._collect(attrs)
            return
        self._collect(attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self._skip:
            self._skip -= 1

    def _collect(self, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key.lower() in {"href", "src"} and value:
                self.links.append(value)


def _local_url(url: str) -> str | None:
    raw = url.strip()
    if not raw or raw.startswith("#"):
        return None
    lowered = raw.lower()
    if lowered.startswith(("http://", "https://", "mailto:", "data:", "javascript:", "about:", "//")):
        return None
    if re.match(r"^[a-z][a-z0-9+.-]*:", lowered):
        return None
    return raw.split("#", 1)[0].split("?", 1)[0]


def _link_findings(repo: Path, deck_id: str, html_path: Path, html: str) -> list[Finding]:
    parser = _LinkParser()
    parser.feed(html)
    parser.close()
    findings: list[Finding] = []
    seen: set[str] = set()
    for url in parser.links:
        local = _local_url(url)
        if local is None or local in seen:
            continue
        seen.add(local)
        target = (html_path.parent / local).resolve()
        try:
            target.relative_to(repo)
        except ValueError:
            findings.append(Finding("html-link", deck_id, f"{local} escapes the repository"))
            continue
        if not target.exists():
            findings.append(Finding("html-link", deck_id, f"missing {local}"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="course_qa",
        description="Offline checks for the Meridian course decks declared in course/show.html.",
    )
    parser.add_argument("--root", type=Path, default=None, help="Repository root. Default: walk upward to course/show.html.")
    parser.add_argument("--json", action="store_true", help="Print findings as JSON.")
    args = parser.parse_args(argv)
    try:
        root = (args.root or repo_root()).resolve()
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    findings = run_checks(root)
    if args.json:
        json.dump([asdict(item) for item in findings], sys.stdout, indent=2)
        sys.stdout.write("\n")
    elif findings:
        print(f"course release: {len(findings)} finding{'s' if len(findings) != 1 else ''}")
        for item in findings:
            print(f"  {item.format()}")
    else:
        show = (root / "course" / "show.html").read_text(encoding="utf-8")
        count = len(parse_catalog(show))
        print(f"course release: {count} decks, 0 findings")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
