#!/usr/bin/env python3
"""Build the Meridian YouTube thumbnails from thumbnails/source.json.

Every thumbnail follows the published intro and Episode 1 design: light
background, Fakhruddin on the right, four logo circles, a two-line condensed
headline with one blue phrase, a handwritten subline and a red corner tag.

- A release with "original" is copied byte for byte from thumbnails/assets/.
  E0 (the intro) and E1 are the files that are already on YouTube.
- Every other release is drawn by headless Chrome over thumbnails/assets/plate.jpg,
  which is the intro photo with its text removed, so the face is identical.

    python3 build_thumbnails.py            # all releases
    python3 build_thumbnails.py E5 E6      # selected releases
"""

from __future__ import annotations

import html
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
THUMBS = ROOT / "thumbnails"
ASSETS = THUMBS / "assets"
SOURCE_PATH = THUMBS / "source.json"
LOGOS_JS = ROOT.parent / "course" / "show" / "deck" / "logos.js"
WIDTH = 1280
HEIGHT = 720
JPEG_QUALITY = 90
CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
)

TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face {{ font-family: "Anton"; src: url("{anton}"); }}
@font-face {{ font-family: "Gochi"; src: url("{gochi}"); }}
html, body {{ margin: 0; width: 1280px; height: 720px; overflow: hidden; }}
body {{ background: url("{plate}") 0 0 / 1280px 720px no-repeat; }}
.logo {{
  position: absolute; top: 109px; width: 134px; height: 134px; border-radius: 50%;
  background: #fff; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 10px 26px rgba(24, 44, 76, .18), 0 2px 5px rgba(24, 44, 76, .10);
}}
.logo svg {{ width: 76px; height: 76px; display: block; }}
.logo.pg svg {{ width: 84px; height: 84px; }}
svg.type {{ position: absolute; left: 0; top: 0; }}
</style>
<script src="{logos}"></script>
</head><body>
{circles}
<svg class="type" width="1280" height="720" xmlns="http://www.w3.org/2000/svg">
  <text id="l1" x="61" y="382" font-family="Anton" font-size="114" fill="#0e121e">{line1}</text>
  <text id="l2" x="61" y="506" font-family="Anton" font-size="114" fill="#0e121e"><tspan fill="#0781c8">{blue}</tspan>{rest}</text>
  <text id="sub" x="62" y="578" font-family="Gochi" font-size="75" fill="#0b0d17">{sub}</text>
  <text id="t1" x="1148" y="83" text-anchor="middle" font-family="Anton" font-size="71" fill="#d52129">{tag1}</text>
  <text id="t2" x="1148" y="165" text-anchor="middle" font-family="Anton" font-size="{tag2_size}" fill="#d52129">{tag2}</text>
</svg>
<script>
const ICON_BLUE = "#1f6fd1";
function logoSvg(key) {{
  if (key === "pg") {{
    return '<svg viewBox="-20 -20 472 486"><defs><linearGradient id="pgbody" x1="0" y1="0" x2=".9" y2="1">'
      + '<stop offset="0" stop-color="#6fa0e6"/><stop offset=".5" stop-color="#336791"/><stop offset="1" stop-color="#1f4470"/></linearGradient></defs>'
      + '<path d="' + PG_OFFICIAL.sil + '" fill="#0e2a47" stroke="#0e2a47" stroke-width="37.4"/>'
      + '<g style="fill:none;stroke:#FFFFFF;stroke-width:12.4651;stroke-linecap:round;stroke-linejoin:round">' + PG_OFFICIAL.front + '</g></svg>';
  }}
  let svg = LOGO[key];
  if (key === "gh") svg = svg.replace('fill="#ffffff"', 'fill="#181717"');
  if (key.startsWith("i-")) svg = svg.replace(/stroke="#[0-9a-fA-F]{{3,6}}"/, 'stroke="' + ICON_BLUE + '"').replace('stroke-width="1.8"', 'stroke-width="2"');
  return svg;
}}
document.querySelectorAll(".logo").forEach(el => {{ el.innerHTML = logoSvg(el.dataset.key); }});
document.fonts.ready.then(() => {{
  const l1 = document.getElementById("l1"), l2 = document.getElementById("l2");
  const widest = Math.max(l1.getComputedTextLength(), l2.getComputedTextLength());
  if (widest > 760) {{ const size = 114 * 760 / widest; l1.setAttribute("font-size", size); l2.setAttribute("font-size", size); }}
  const sub = document.getElementById("sub");
  if (sub.getComputedTextLength() > 735) sub.setAttribute("font-size", 75 * 735 / sub.getComputedTextLength());
  const t1 = document.getElementById("t1"), t2 = document.getElementById("t2");
  const tagWidth = Math.max(t1.getComputedTextLength(), t2.getComputedTextLength());
  const centre = 1254 - tagWidth / 2;
  t1.setAttribute("x", centre); t2.setAttribute("x", centre);
  document.title = "ready";
}});
</script>
</body></html>
"""


def load_source(path: Path = SOURCE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_chrome() -> str:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    raise SystemExit("Google Chrome or Chromium is required to draw the thumbnails.")


def headline(spec: dict) -> str:
    return " ".join(part for part in (spec["line1"], spec["blue"], spec["rest"]) if part)


def page(spec: dict) -> str:
    keys = spec["logos"]
    circles = "\n".join(
        f'<div class="logo{" pg" if key == "pg" else ""}" data-key="{html.escape(key)}" style="left:{112 + 168 * index}px"></div>'
        for index, key in enumerate(keys)
    )
    tag1, tag2 = spec["tag"]
    rest = f" {spec['rest']}" if spec["rest"] else ""
    return TEMPLATE.format(
        anton=(ASSETS / "fonts" / "Anton-Regular.ttf").as_uri(),
        gochi=(ASSETS / "fonts" / "GochiHand-Regular.ttf").as_uri(),
        plate=(ASSETS / "plate.jpg").as_uri(),
        logos=LOGOS_JS.as_uri(),
        circles=circles,
        line1=html.escape(spec["line1"]),
        blue=html.escape(spec["blue"]),
        rest=html.escape(rest),
        sub=html.escape(spec["sub"]),
        tag1=html.escape(tag1),
        tag2=html.escape(tag2),
        tag2_size=79 if tag2.isdigit() else 71,
    )


def draw(spec: dict, destination: Path, chrome: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        page_path = Path(tmp) / f"{spec['id']}.html"
        shot = Path(tmp) / f"{spec['id']}.png"
        page_path.write_text(page(spec), encoding="utf-8")
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--allow-file-access-from-files",
                "--force-device-scale-factor=1",
                f"--window-size={WIDTH},{HEIGHT}",
                "--virtual-time-budget=4000",
                f"--screenshot={shot}",
                page_path.as_uri(),
            ],
            check=True,
            capture_output=True,
        )
        with Image.open(shot) as image:
            image.convert("RGB").crop((0, 0, WIDTH, HEIGHT)).save(destination, "JPEG", quality=JPEG_QUALITY, optimize=True)


def build(ids: list[str] | None = None) -> list[Path]:
    source = load_source()
    chrome = None
    written = []
    for spec in source["releases"]:
        if ids and spec["id"] not in ids:
            continue
        destination = THUMBS / f"{spec['id']}.jpg"
        if "original" in spec:
            shutil.copyfile(THUMBS / spec["original"], destination)
        else:
            chrome = chrome or find_chrome()
            draw(spec, destination, chrome)
        written.append(destination)
    return written


def write_contact_sheet(source: dict | None = None) -> Path:
    source = source if source is not None else load_source()
    paths = [path for spec in source["releases"] if (path := THUMBS / f"{spec['id']}.jpg").is_file()]
    thumb_width, thumb_height, label_height, columns = 426, 240, 34, 3
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), (16, 20, 28))
    draw_sheet = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype(str(ASSETS / "fonts" / "Anton-Regular.ttf"), 22)
    for index, path in enumerate(paths):
        with Image.open(path) as image:
            small = image.convert("RGB").resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        x = index % columns * thumb_width
        y = index // columns * (thumb_height + label_height)
        sheet.paste(small, (x, y))
        draw_sheet.text((x + 10, y + thumb_height + 4), path.stem, font=label_font, fill=(240, 244, 252))
    destination = THUMBS / "contact-sheet.jpg"
    sheet.save(destination, "JPEG", quality=85, optimize=True)
    return destination


def main(argv: list[str]) -> int:
    for path in build(argv or None):
        print(f"{path.relative_to(ROOT)} {path.stat().st_size} bytes")
    sheet = write_contact_sheet()
    print(f"{sheet.relative_to(ROOT)} {sheet.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
