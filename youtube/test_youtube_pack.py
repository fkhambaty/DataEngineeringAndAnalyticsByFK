#!/usr/bin/env python3
"""Stdlib checks for the instructor YouTube pack."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from PIL import Image

import check_youtube_pack as pack

ROOT = Path(__file__).resolve().parent
ORDER = ["E0", "E1", "E2", "E3", "P0", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13"]


class YoutubePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        cls.source = json.loads((ROOT / "thumbnails" / "source.json").read_text(encoding="utf-8"))
        cls.errors = pack.collect_errors()

    def test_metadata_complete(self) -> None:
        self.assertEqual(self.errors, [], "\n".join(self.errors))

    def test_canonical_order(self) -> None:
        self.assertEqual([item["id"] for item in self.catalog["releases"]], ORDER)

    def test_title_and_tag_limits(self) -> None:
        for release in self.catalog["releases"]:
            self.assertLessEqual(len(release["title"]), 100, release["id"])
            self.assertLessEqual(len(release["tags"]), 500, release["id"])
            self.assertNotIn(",,", release["tags"], release["id"])

    def test_thumbnail_copy_is_unique_and_short(self) -> None:
        headlines = [item["thumbnail"]["headline"] for item in self.catalog["releases"]]
        self.assertEqual(len(headlines), len(set(headlines)))
        for headline in headlines:
            self.assertGreaterEqual(len(headline.split()), 2)
            self.assertLessEqual(len(headline.split()), 7)

    def test_chapters_start_at_zero(self) -> None:
        for release in self.catalog["releases"]:
            self.assertEqual(release["chapters"][0]["at"], "00:00", release["id"])
            if not release["published"]:
                self.assertIn(pack.CHAPTER_WARNING, release["description"])

    def test_published_releases_keep_their_live_copy(self) -> None:
        by_id = {item["id"]: item for item in self.catalog["releases"]}
        self.assertEqual(by_id["E0"]["title"], "Snowflake, dbt, Airflow Project | PostgreSQL, SQL, Data Engineering")
        self.assertEqual(by_id["E1"]["title"], "Build a Real Bank on Your Laptop | PostgreSQL + 5 Million Payments | Episode 1")
        sources = {item["id"]: item for item in self.source["releases"]}
        for release_id in ("E0", "E1"):
            self.assertTrue(by_id[release_id]["published"])
            original = ROOT / "thumbnails" / sources[release_id]["original"]
            self.assertEqual(original.read_bytes(), (ROOT / "thumbnails" / f"{release_id}.jpg").read_bytes())

    def test_corner_tags(self) -> None:
        tags = {item["id"]: item["thumbnail"]["tag"] for item in self.catalog["releases"]}
        self.assertEqual(tags["E0"], "INTRO VIDEO")
        self.assertEqual(tags["E1"], "EPISODE 1")
        self.assertEqual(tags["P0"], "PYTHON PRIMER")
        self.assertEqual(tags["E13"], "EPISODE 13")

    def test_jpg_dimensions_and_size(self) -> None:
        for release_id in ORDER:
            path = ROOT / "thumbnails" / f"{release_id}.jpg"
            self.assertLess(path.stat().st_size, 2 * 1024 * 1024, release_id)
            with Image.open(path) as image:
                self.assertEqual(image.size, (1280, 720), release_id)
                self.assertEqual(image.format, "JPEG", release_id)


if __name__ == "__main__":
    unittest.main()
