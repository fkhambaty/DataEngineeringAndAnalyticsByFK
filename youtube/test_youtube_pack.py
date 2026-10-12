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
        hooks = [item["thumbnail"]["hook"] for item in self.catalog["releases"]]
        self.assertEqual(len(hooks), len(set(hooks)))
        for hook in hooks:
            self.assertGreaterEqual(len(hook.split()), 2)
            self.assertLessEqual(len(hook.split()), 5)

    def test_chapters_start_at_zero(self) -> None:
        for release in self.catalog["releases"]:
            self.assertEqual(release["chapters"][0]["at"], "00:00", release["id"])
            self.assertIn(pack.CHAPTER_WARNING, release["description"])

    def test_episode_one_badge(self) -> None:
        e1 = next(item for item in self.source["releases"] if item["id"] == "E1")
        self.assertEqual(e1["badge"], "EPISODE 1")
        painted = pack.build_thumbnails.render(e1)
        blank = pack.build_thumbnails.render(e1, badge_override="")
        self.assertIsNotNone(pack.ImageChops.difference(painted, blank).getbbox())

    def test_png_dimensions_and_size(self) -> None:
        for release_id in ORDER:
            path = ROOT / "thumbnails" / f"{release_id}.png"
            self.assertLess(path.stat().st_size, 2 * 1024 * 1024, release_id)
            with Image.open(path) as image:
                self.assertEqual(image.size, (1280, 720), release_id)
                self.assertEqual(image.format, "PNG", release_id)


if __name__ == "__main__":
    unittest.main()
