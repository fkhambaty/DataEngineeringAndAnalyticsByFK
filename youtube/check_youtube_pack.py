#!/usr/bin/env python3
"""Check the instructor YouTube pack, and rewrite UPLOAD_PACK.md from catalog.json.

    python3 check_youtube_pack.py
    python3 check_youtube_pack.py --write-packs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "catalog.json"
SOURCE_PATH = ROOT / "thumbnails" / "source.json"
MAX_TITLE = 100
MAX_TAGS = 500
MAX_THUMB_BYTES = 2 * 1024 * 1024
REQUIRED_HEADINGS = (
    "Title",
    "Hook",
    "Description",
    "Student repository",
    "Prerequisites",
    "Files covered",
    "Chapters",
    "Hashtags",
    "Tags",
    "Pinned comment",
    "Community post",
    "Cards and end screen",
    "Upload settings",
    "Filename",
    "Thumbnail",
    "Pre-publish checks",
)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
TIMESTAMP_RE = re.compile(r"^(\d{2}):(\d{2})(?::(\d{2}))?$")
CHAPTER_WARNING = "Adjust these timestamps after the final edit."


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def seconds(stamp: str) -> int:
    match = TIMESTAMP_RE.fullmatch(stamp.strip())
    if not match:
        raise ValueError(stamp)
    hours = 0
    minutes = int(match.group(1))
    if match.group(3) is None:
        secs = int(match.group(2))
    else:
        hours = minutes
        minutes = int(match.group(2))
        secs = int(match.group(3))
    return hours * 3600 + minutes * 60 + secs


def chapter_block(chapters: list[dict]) -> str:
    return "\n".join(f"{chapter['at']} {chapter['title']}" for chapter in chapters)


def render_pack(release: dict, series: dict) -> str:
    files = "\n".join(f"- `{path}`" for path in release["files"])
    prerequisites = "\n".join(f"- {item}" for item in release["prerequisites"])
    checks = "\n".join(f"- [ ] {item}" for item in release["pre_publish_checks"])
    settings = release["settings"]
    thumb = release["thumbnail"]
    hook = "\n".join(release["hook"])
    position = f"{release['order']} of {len(series['canonical_order'])}"
    if release.get("published"):
        url = release.get("published_url") or "add the URL from YouTube Studio"
        status = f"Status: published ({url}). Title, description and tags below are exactly what is live."
    else:
        status = "Status: not published yet."
    return f"""# {release['id']} — {release['show_title']}

{status}
Planned length: {release['planned_minutes']} minutes. Playlist position: {position}.
Grounding: {release['grounding']}

## Title

{release['title']}

## Hook

{hook}

## Description

{release['description'].rstrip()}

## Student repository

{series['student_repo']}

## Prerequisites

{prerequisites}

## Files covered

{files}

## Chapters

{CHAPTER_WARNING} They are drafted to the planned {release['planned_minutes']}-minute cut, not to a finished timeline.

```
{chapter_block(release['chapters'])}
```

## Hashtags

{' '.join(release['hashtags'])}

## Tags

{release['tags']}

## Pinned comment

{release['pinned_comment'].rstrip()}

## Community post

{release['community_post'].rstrip()}

## Cards and end screen

{release['cards_end_screen'].rstrip()}

## Upload settings

- Category: {settings['category']}
- Language: {settings['language']}
- License: {settings['license']}
- Audience: {settings['audience']}
- Visibility: {settings['visibility']}

## Filename

{release['filename']}

## Thumbnail

- File: `{thumb['file']}`
- Red corner tag: {thumb['tag']}
- Headline: {thumb['headline']}
- Handwritten line: {thumb['sub']}

## Pre-publish checks

{checks}
"""


def write_packs(catalog: dict | None = None) -> list[Path]:
    catalog = catalog if catalog is not None else load_json(CATALOG_PATH)
    written = []
    for release in catalog["releases"]:
        folder = ROOT / release["id"]
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "UPLOAD_PACK.md"
        path.write_text(render_pack(release, catalog["series"]), encoding="utf-8")
        written.append(path)
    return written


def parse_pack(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def chapter_lines(section: str) -> list[str]:
    match = re.search(r"```\n(.*?)```", section, re.S)
    if not match:
        return []
    return [line.strip() for line in match.group(1).splitlines() if line.strip()]


def collect_errors() -> list[str]:
    errors: list[str] = []
    if not CATALOG_PATH.is_file():
        return ["catalog.json is missing"]
    if not SOURCE_PATH.is_file():
        return ["thumbnails/source.json is missing"]
    catalog = load_json(CATALOG_PATH)
    source = load_json(SOURCE_PATH)
    series = catalog.get("series", {})
    releases = catalog.get("releases", [])
    order = [item["id"] for item in releases]
    expected_order = ["E0", "E1", "E2", "E3", "P0", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13"]
    if order != expected_order:
        errors.append(f"canonical release order is {order}")
    if series.get("canonical_order") != expected_order:
        errors.append("series.canonical_order does not match E0 through E13")
    repo = series.get("student_repo", "")
    if repo != "https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK":
        errors.append("student repository URL is not the public course repo")

    source_by_id = {item["id"]: item for item in source.get("releases", [])}
    if [item["id"] for item in source.get("releases", [])] != expected_order:
        errors.append("thumbnail source order does not match the canonical order")
    if source.get("canvas") != {"width": 1280, "height": 720}:
        errors.append("thumbnail source canvas is not 1280x720")

    titles = []
    hooks = []
    for release in releases:
        identity = release["id"]
        prefix = identity
        title = release.get("title", "")
        titles.append(title)
        if not title or len(title) > MAX_TITLE:
            errors.append(f"{prefix} title length is {len(title)}")
        description = release.get("description", "")
        published = release.get("published") is True
        if "published" not in release:
            errors.append(f"{prefix} must say whether it is published")
        hook = release.get("hook", [])
        if not (isinstance(hook, list) and len(hook) == 2 and all(isinstance(line, str) and line.strip() for line in hook)):
            errors.append(f"{prefix} hook must be exactly two non-empty lines")
        elif not published and not description.startswith(f"{hook[0]}\n{hook[1]}"):
            errors.append(f"{prefix} description does not open with the two-line hook")
        if not published and re.search(r"\b(?:E\d+|P0)\b", description):
            errors.append(f"{prefix} description uses an internal episode code instead of the YouTube name")
        for field in ("summary", "honesty", "filename", "pinned_comment", "community_post", "cards_end_screen", "grounding"):
            if not str(release.get(field, "")).strip():
                errors.append(f"{prefix} is missing {field}")
        if not release.get("prerequisites") or not release.get("files") or not release.get("pre_publish_checks"):
            errors.append(f"{prefix} prerequisites, files, or pre-publish checks are empty")
        if not published and CHAPTER_WARNING not in description:
            errors.append(f"{prefix} description is missing the chapter warning")
        if repo not in release.get("pinned_comment", "") or (not published and repo not in description):
            errors.append(f"{prefix} description or pinned comment is missing the student repository")
        marker = release.get("honesty_marker", "")
        if not published and identity in {"E3", "E8", "E9", "E11", "E13"} and (not marker or marker not in description):
            errors.append(f"{prefix} description is missing its honesty marker")
        chapters = release.get("chapters", [])
        if len(chapters) < 3:
            errors.append(f"{prefix} needs at least three chapters")
        else:
            if chapters[0].get("at") != "00:00":
                errors.append(f"{prefix} first chapter is not 00:00")
            previous = -1
            limit = int(release["planned_minutes"]) * 60
            for chapter in chapters:
                try:
                    stamp = seconds(chapter["at"])
                except ValueError:
                    errors.append(f"{prefix} has an invalid timestamp {chapter.get('at')}")
                    continue
                if stamp <= previous:
                    errors.append(f"{prefix} chapters are not strictly increasing")
                if stamp >= limit:
                    errors.append(f"{prefix} chapter {chapter['at']} is outside the planned duration")
                previous = stamp
            if not published and chapter_block(chapters) not in description:
                errors.append(f"{prefix} description chapters differ from the chapter list")
        hashtags = release.get("hashtags", [])
        if not (3 <= len(hashtags) <= 5) or any(not tag.startswith("#") or " " in tag for tag in hashtags):
            errors.append(f"{prefix} hashtags must be 3 to 5 single tokens")
        tags = release.get("tags", "")
        if not tags or len(tags) > MAX_TAGS:
            errors.append(f"{prefix} tags length is {len(tags)}")
        if any(not part.strip() or "," in part.strip() for part in tags.split(",")):
            errors.append(f"{prefix} tags must be comma-separated values without nested commas")
        settings = release.get("settings", {})
        for key in ("category", "language", "license", "audience", "visibility"):
            if not settings.get(key):
                errors.append(f"{prefix} settings.{key} is empty")
        if settings.get("category") != "Education" or settings.get("language") != "English":
            errors.append(f"{prefix} category or language is unexpected")
        if settings.get("audience") != "Not made for kids":
            errors.append(f"{prefix} audience is unexpected")
        if not release.get("filename", "").endswith(".mp4"):
            errors.append(f"{prefix} filename must end in .mp4")
        thumb = release.get("thumbnail", {})
        words = thumb.get("headline", "").split()
        hooks.append(thumb.get("headline", ""))
        if not (2 <= len(words) <= 7):
            errors.append(f"{prefix} thumbnail headline must be 2 to 7 words")
        if thumb.get("file") != f"thumbnails/{identity}.jpg":
            errors.append(f"{prefix} thumbnail file is not thumbnails/{identity}.jpg")
        visual = source_by_id.get(identity)
        if visual is None:
            errors.append(f"{prefix} has no thumbnail source")
        else:
            expected = {
                "tag": " ".join(visual.get("tag", [])),
                "headline": " ".join(part for part in (visual.get("line1"), visual.get("blue"), visual.get("rest")) if part),
                "sub": visual.get("sub"),
            }
            for key, value in expected.items():
                if thumb.get(key) != value:
                    errors.append(f"{prefix} thumbnail {key} does not match source.json")
            if len(visual.get("logos", [])) not in (4, 6):
                errors.append(f"{prefix} thumbnail needs four logo circles")
            if published != ("original" in visual):
                errors.append(f"{prefix} published thumbnails must be the original files, and only those")
        expected_tag = "INTRO VIDEO" if identity == "E0" else "PYTHON PRIMER" if identity == "P0" else f"EPISODE {identity[1:]}"
        if thumb.get("tag") != expected_tag:
            errors.append(f"{prefix} tag is not {expected_tag}")
        blob = json.dumps(release)
        if EMAIL_RE.search(blob) or "BEGIN PRIVATE KEY" in blob or "snowflakecomputing.com" in blob:
            errors.append(f"{prefix} contains private account material")
        if "not in the repo yet" in blob.lower():
            errors.append(f"{prefix} contains stale missing-deck copy")

        pack_path = ROOT / identity / "UPLOAD_PACK.md"
        if not pack_path.is_file():
            errors.append(f"{prefix} UPLOAD_PACK.md is missing")
            continue
        parsed = parse_pack(pack_path.read_text(encoding="utf-8"))
        for heading in REQUIRED_HEADINGS:
            if heading not in parsed or not parsed[heading].strip():
                errors.append(f"{prefix} pack is missing {heading}")
        if parsed.get("Title") != title:
            errors.append(f"{prefix} pack title does not match catalog.json")
        if parsed.get("Description") != description.strip():
            errors.append(f"{prefix} pack description does not match catalog.json")
        if parsed.get("Tags") != tags:
            errors.append(f"{prefix} pack tags do not match catalog.json")
        lines = chapter_lines(parsed.get("Chapters", ""))
        if not lines or not lines[0].startswith("00:00 "):
            errors.append(f"{prefix} pack chapters do not start at 00:00")
        elif lines != [f"{chapter['at']} {chapter['title']}" for chapter in chapters]:
            errors.append(f"{prefix} pack chapters do not match catalog.json")
        if CHAPTER_WARNING not in parsed.get("Chapters", ""):
            errors.append(f"{prefix} pack chapters are missing the final-edit warning")
        if thumb.get("tag", "~") not in parsed.get("Thumbnail", ""):
            errors.append(f"{prefix} pack thumbnail section does not name the corner tag")

        thumb_path = ROOT / "thumbnails" / f"{identity}.jpg"
        if not thumb_path.is_file():
            errors.append(f"{prefix} thumbnail JPG is missing")
            continue
        size = thumb_path.stat().st_size
        if size >= MAX_THUMB_BYTES:
            errors.append(f"{prefix} thumbnail is {size} bytes")
        with Image.open(thumb_path) as image:
            if image.size != (1280, 720):
                errors.append(f"{prefix} thumbnail size is {image.size}")
            if image.format != "JPEG":
                errors.append(f"{prefix} thumbnail format is {image.format}")
        if visual is not None and "original" in visual:
            original = ROOT / "thumbnails" / visual["original"]
            if not original.is_file() or original.read_bytes() != thumb_path.read_bytes():
                errors.append(f"{prefix} thumbnail is not byte-identical to the published {visual['original']}")

    if len(set(hooks)) != len(hooks):
        errors.append("thumbnail headlines are not unique")
    if len(set(titles)) != len(titles):
        errors.append("titles are not unique")
    if not (ROOT / "thumbnails" / "assets" / "plate.jpg").is_file():
        errors.append("thumbnails/assets/plate.jpg is missing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the Meridian YouTube publishing kit")
    parser.add_argument("--write-packs", action="store_true", help="rewrite UPLOAD_PACK.md from catalog.json")
    args = parser.parse_args()
    if args.write_packs:
        for path in write_packs():
            print(f"wrote {path.relative_to(ROOT)}")
    errors = collect_errors()
    if errors:
        print(f"FAILED {len(errors)}")
        for error in errors:
            print(f"- {error}")
        return 1
    catalog = load_json(CATALOG_PATH)
    print(f"OK {len(catalog['releases'])} releases")
    for release in catalog["releases"]:
        thumb = ROOT / release["thumbnail"]["file"]
        print(
            f"OK {release['id']} title={len(release['title'])} chars "
            f"tags={len(release['tags'])} chars jpg={thumb.stat().st_size} bytes "
            f"chapters={release['chapters'][0]['at']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
