"""Read the episode catalog and the slide list inside each deck."""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


class CatalogError(Exception):
    """``course/show.html`` has no parseable ``EPISODES`` array."""


@dataclass(frozen=True)
class Deck:
    """One cinematic deck declared in the player catalog."""

    deck_id: str
    code: str
    title: str
    scenes: int
    relpath: str

    def html_path(self, repo: Path) -> Path:
        return (repo / "course" / self.relpath).resolve()


_EPISODES_RE = re.compile(r"const\s+EPISODES\s*=\s*\[(.*?)]\s*;", re.S)
_OBJECT_RE = re.compile(r"\{[^{}]*\}", re.S)
_SCENES_RE = re.compile(r"scenes\s*:\s*(\d+)")
_BODY_RE = re.compile(r"<body\b([^>]*)>", re.I)
_EPISODE_ATTR_RE = re.compile(r"""data-episode\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)


def parse_catalog(show_html: str) -> list[Deck]:
    """Return decks in catalog order.

    Each object must name ``id``, ``deck``, and ``scenes``. Nested braces are
    not used by the player catalog.
    """
    found = _EPISODES_RE.search(show_html)
    if found is None:
        raise CatalogError("const EPISODES was not found in course/show.html")
    decks: list[Deck] = []
    for obj in _OBJECT_RE.findall(found.group(1)):
        if "id" not in obj or "deck" not in obj:
            continue
        deck_id = _string_field(obj, "id")
        relpath = _string_field(obj, "deck")
        scenes_match = _SCENES_RE.search(obj)
        if not deck_id or not relpath or scenes_match is None:
            raise CatalogError(f"episode object is missing id, deck, or scenes: {obj[:120]}")
        decks.append(
            Deck(
                deck_id=deck_id,
                code=_string_field(obj, "code") or deck_id,
                title=_string_field(obj, "title") or deck_id,
                scenes=int(scenes_match.group(1)),
                relpath=relpath,
            )
        )
    if not decks:
        raise CatalogError("EPISODES listed no decks")
    return decks


def _string_field(obj: str, name: str) -> str:
    found = re.search(
        r'(?<![A-Za-z0-9_])' + re.escape(name) + r'\s*:\s*"((?:\\.|[^"\\])*)"',
        obj,
    )
    return found.group(1) if found else ""


class _SlideParser(HTMLParser):
    """Count ``<section class="s">`` slides, ignoring scripts, styles, and comments."""

    def __init__(self) -> None:
        super().__init__()
        self.steps: list[int] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        name = tag.lower()
        if name in {"script", "style"}:
            self._skip += 1
        if self._skip:
            return
        if name != "section":
            return
        attr = {key.lower(): (value or "") for key, value in attrs}
        classes = attr.get("class", "").split()
        if "s" not in classes:
            return
        raw_steps = attr.get("data-steps", "")
        self.steps.append(int(raw_steps) if raw_steps.isdigit() else 0)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self._skip:
            self._skip -= 1


def slide_steps(html: str) -> list[int]:
    """Final click-step of each slide. ``0`` means the slide has no ``data-steps``."""
    parser = _SlideParser()
    parser.feed(html)
    parser.close()
    return parser.steps


def final_hash(index: int, steps: int) -> str:
    """Hash the deck engine reads: ``#3`` or ``#3.2`` (1-based slide, final step)."""
    if index < 1:
        raise ValueError(f"slide index must be 1-based, got {index}")
    if steps < 0:
        raise ValueError(f"data-steps cannot be negative, got {steps}")
    if steps:
        return f"{index}.{steps}"
    return str(index)


def final_hashes(html: str) -> list[str]:
    return [final_hash(index, steps) for index, steps in enumerate(slide_steps(html), start=1)]


def declared_episode(html: str) -> str | None:
    """``data-episode`` on ``<body>``, or None when the deck does not set it."""
    match = _BODY_RE.search(html)
    if match is None:
        return None
    found = _EPISODE_ATTR_RE.search(match.group(1))
    if found is None:
        return None
    return found.group(1) if found.group(1) is not None else found.group(2)
