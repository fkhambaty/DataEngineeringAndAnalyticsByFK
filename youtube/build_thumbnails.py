#!/usr/bin/env python3
"""Draw the Meridian YouTube thumbnails from thumbnails/source.json.

Uses the local system fonts it can find and Pillow geometry only.
Nothing is downloaded.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE_PATH = ROOT / "thumbnails" / "source.json"
WIDTH = 1280
HEIGHT = 720

BOLD_FONTS = (
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
)
REGULAR_FONTS = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
)

PIPE = ("#336791", "#F5C542", "#29B5E8", "#FF694B", "#38BDF8", "#A78BFA")


def hex_rgb(value: str) -> tuple[int, int, int]:
    raw = value.removeprefix("#")
    return tuple(int(raw[i : i + 2], 16) for i in (0, 2, 4))


def find_font(candidates: tuple[str, ...]) -> Path:
    for candidate in candidates:
        path = Path(candidate)
        if path.is_file():
            return path
    raise SystemExit(
        "No local sans font found. Install Arial, Liberation Sans, or DejaVu "
        "and rerun. This script does not download fonts."
    )


def font(size: int, bold: bool) -> ImageFont.FreeTypeFont:
    path = find_font(BOLD_FONTS if bold else REGULAR_FONTS)
    return ImageFont.truetype(str(path), size)


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def gradient(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    top = (23, 36, 56)
    mid = (16, 22, 34)
    bottom = (22, 20, 40)
    for y in range(size[1]):
        t = y / (size[1] - 1)
        if t < 0.55:
            u = t / 0.55
            color = tuple(lerp(top[i], mid[i], u) for i in range(3))
        else:
            u = (t - 0.55) / 0.45
            color = tuple(lerp(mid[i], bottom[i], u) for i in range(3))
        draw.line([(0, y), (size[0], y)], fill=color + (255,))
    return image


def glow(base: Image.Image, center: tuple[int, int], radius: int, color: str, strength: int) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    rgb = hex_rgb(color)
    step = 10
    for radius_i in range(radius, 0, -step):
        fade = (1 - radius_i / radius) ** 2
        alpha = int(strength * fade)
        draw.ellipse(
            [center[0] - radius_i, center[1] - radius_i, center[0] + radius_i, center[1] + radius_i],
            fill=rgb + (alpha,),
        )
    composited = Image.alpha_composite(base, overlay)
    base.paste(composited)


def grid(base: Image.Image) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(0, WIDTH, 64):
        draw.line([(x, 0), (x, HEIGHT)], fill=(255, 255, 255, 16))
    for y in range(0, HEIGHT, 64):
        draw.line([(0, y), (WIDTH, y)], fill=(255, 255, 255, 16))
    composited = Image.alpha_composite(base, overlay)
    base.paste(composited)


def rel(box: tuple[int, int, int, int], fx: float, fy: float) -> tuple[int, int]:
    x, y, w, h = box
    return (int(x + w * fx), int(y + h * fy))


def node(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int, fill: tuple[int, int, int, int], outline) -> None:
    x, y = center
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill, outline=outline, width=3)


def connect(draw: ImageDraw.ImageDraw, a: tuple[int, int], b: tuple[int, int], color, width: int = 4) -> None:
    draw.line([a, b], fill=color, width=width)


def pipe(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x, y, w, h = box
    y_line = y + h - 36
    count = len(PIPE)
    gap = w / (count + 1)
    points = []
    for index, color in enumerate(PIPE):
        center = (int(x + gap * (index + 1)), y_line)
        points.append(center)
        if index:
            connect(draw, points[index - 1], center, (255, 255, 255, 70), 3)
    for center, color in zip(points, PIPE):
        node(draw, center, 9, hex_rgb(color) + (230,), (255, 255, 255, 180))


def motif_rooms(draw, box, accent):
    centers = [rel(box, fx, fy) for fy in (0.28, 0.62) for fx in (0.22, 0.5, 0.78)]
    for index, center in enumerate(centers):
        if index:
            connect(draw, centers[index - 1], center, accent + (140,), 3)
    for center in centers:
        x, y = center
        draw.rounded_rectangle([x - 28, y - 22, x + 28, y + 22], radius=8, outline=accent + (230,), width=3)


def motif_layers(draw, box, accent):
    colors = ((208, 139, 79, 230), (201, 211, 223, 230), accent + (230,))
    for index, color in enumerate(colors):
        top = box[1] + 36 + index * 78
        inset = 36 + index * 18
        draw.rounded_rectangle(
            [box[0] + inset, top, box[0] + box[2] - inset, top + 48],
            radius=14,
            fill=color,
        )


def motif_star(draw, box, accent):
    center = rel(box, 0.5, 0.42)
    satellites = [rel(box, fx, fy) for fx, fy in ((0.18, 0.22), (0.5, 0.12), (0.82, 0.22), (0.84, 0.58), (0.5, 0.7), (0.16, 0.58))]
    for point in satellites:
        connect(draw, center, point, (255, 255, 255, 120), 3)
        node(draw, point, 16, (255, 255, 255, 30), accent + (220,))
    node(draw, center, 28, accent + (210,), (255, 255, 255, 230))


def motif_shelves(draw, box, accent):
    for index in range(3):
        top = box[1] + 40 + index * 86
        draw.rounded_rectangle(
            [box[0] + 40, top, box[0] + box[2] - 90, top + 18],
            radius=6,
            fill=(255, 255, 255, 28),
            outline=accent + (200,),
            width=3,
        )
    lock = rel(box, 0.84, 0.22)
    draw.arc([lock[0] - 16, lock[1] - 28, lock[0] + 16, lock[1] + 4], 200, 340, fill=accent + (230,), width=4)
    draw.rounded_rectangle([lock[0] - 18, lock[1], lock[0] + 18, lock[1] + 28], radius=4, outline=accent + (230,), width=4)


def motif_python(draw, box, accent):
    left = box[0] + 70
    top = box[1] + 70
    for index in range(4):
        y = top + index * 52
        draw.rounded_rectangle([left, y, left + 220 - index * 24, y + 28], radius=8, fill=accent + (40,), outline=accent + (220,), width=3)
    draw.arc([box[0] + box[2] - 150, box[1] + 80, box[0] + box[2] - 40, box[1] + 190], 20, 320, fill=(255, 255, 255, 180), width=4)


def motif_delta(draw, box, accent):
    base_y = box[1] + 150
    for index in range(8):
        x = box[0] + 36 + index * 46
        filled = index >= 6
        color = accent + (230,) if filled else (255, 255, 255, 40)
        draw.rounded_rectangle([x, base_y, x + 32, base_y + 32], radius=6, fill=color, outline=accent + (180,), width=2)
    draw.line([(box[0] + 36 + 6 * 46, base_y - 24), (box[0] + 36 + 6 * 46, base_y + 70)], fill=accent + (180,), width=3)


def motif_inbox(draw, box, accent):
    draw.polygon(
        [
            rel(box, 0.12, 0.28),
            rel(box, 0.42, 0.28),
            rel(box, 0.48, 0.62),
            rel(box, 0.06, 0.62),
        ],
        outline=accent + (230,),
    )
    for index in range(3):
        y = box[1] + 90 + index * 48
        draw.rounded_rectangle([box[0] + 230, y, box[0] + box[2] - 36, y + 22], radius=6, fill=(255, 255, 255, 36), outline=accent + (200,), width=2)


def motif_fact(draw, box, accent):
    center = rel(box, 0.48, 0.4)
    draw.rounded_rectangle([center[0] - 46, center[1] - 28, center[0] + 46, center[1] + 28], radius=8, fill=accent + (220,))
    for point in (rel(box, 0.16, 0.22), rel(box, 0.78, 0.18), rel(box, 0.84, 0.55), rel(box, 0.22, 0.66)):
        connect(draw, center, point, (255, 255, 255, 110), 3)
        node(draw, point, 14, (255, 255, 255, 28), (255, 255, 255, 180))


def motif_clock(draw, box, accent):
    center = rel(box, 0.48, 0.4)
    radius = 78
    draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline=accent + (230,), width=4)
    draw.line([center, (center[0] + 36, center[1] - 20)], fill=(255, 255, 255, 230), width=5)
    draw.line([center, (center[0], center[1] - 52)], fill=accent + (230,), width=5)
    node(draw, center, 6, accent + (255,), accent + (255,))


def motif_measure(draw, box, accent):
    bars = (70, 110, 86, 40, 28)
    for index, height in enumerate(bars):
        x = box[0] + 48 + index * 70
        y = box[1] + 210 - height
        color = accent + (220,) if index >= 3 else (251, 113, 133, 200)
        draw.rounded_rectangle([x, y, x + 40, box[1] + 210], radius=6, fill=color)


def motif_checks(draw, box, accent):
    for index in range(4):
        center = rel(box, 0.28, 0.18 + index * 0.16)
        node(draw, center, 16, accent + (50,), accent + (230,))
        x, y = center
        draw.line([(x - 7, y), (x - 2, y + 6), (x + 8, y - 7)], fill=accent + (255,), width=3)
        draw.line([(x + 28, y), (box[0] + box[2] - 40, y)], fill=(255, 255, 255, 50), width=3)


def motif_gate(draw, box, accent):
    y_gate = box[1] + 120
    draw.line([(box[0] + 30, y_gate), (box[0] + box[2] - 30, y_gate)], fill=accent + (230,), width=4)
    for index, dy in enumerate((70, 96, 48, 130, 24)):
        color = (251, 113, 133, 220) if dy < 60 else accent + (180,)
        node(draw, (box[0] + 60 + index * 70, y_gate + dy), 10, color, (255, 255, 255, 160))


def motif_personas(draw, box, accent):
    origin = rel(box, 0.22, 0.42)
    node(draw, origin, 22, accent + (220,), (255, 255, 255, 220))
    for index, fy in enumerate((0.16, 0.34, 0.56, 0.76)):
        point = rel(box, 0.72, fy)
        connect(draw, origin, point, (255, 255, 255, 100), 3)
        node(draw, point, 14, (255, 255, 255, 30), accent + (220,))


def motif_rebuild(draw, box, accent):
    center = rel(box, 0.48, 0.38)
    draw.arc([center[0] - 90, center[1] - 70, center[0] + 90, center[1] + 70], 30, 330, fill=accent + (230,), width=5)
    draw.polygon([(center[0] + 78, center[1] - 8), (center[0] + 96, center[1] + 10), (center[0] + 64, center[1] + 6)], fill=accent + (230,))
    draw.rounded_rectangle([center[0] - 16, center[1] - 8, center[0] + 16, center[1] + 24], radius=4, outline=(255, 255, 255, 230), width=4)
    draw.arc([center[0] - 12, center[1] - 28, center[0] + 12, center[1] - 4], 200, 340, fill=(255, 255, 255, 230), width=4)


def motif_pitch(draw, box, accent):
    center = rel(box, 0.48, 0.4)
    radius = 86
    draw.arc([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], 0, 300, fill=(255, 255, 255, 80), width=8)
    draw.arc([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], 300, 360, fill=accent + (255,), width=8)
    node(draw, center, 8, accent + (255,), accent + (255,))


MOTIFS = {
    "rooms": motif_rooms,
    "layers": motif_layers,
    "star": motif_star,
    "shelves": motif_shelves,
    "python": motif_python,
    "delta": motif_delta,
    "inbox": motif_inbox,
    "fact": motif_fact,
    "clock": motif_clock,
    "measure": motif_measure,
    "checks": motif_checks,
    "gate": motif_gate,
    "personas": motif_personas,
    "rebuild": motif_rebuild,
    "pitch": motif_pitch,
}


def wrap_hook(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    if draw.textlength(text, font=face) <= max_width:
        return [text]
    words = text.split()
    best: tuple[int, list[str]] | None = None
    for split in range(1, len(words)):
        lines = [" ".join(words[:split]), " ".join(words[split:])]
        if all(draw.textlength(line, font=face) <= max_width for line in lines):
            score = abs(len(lines[0]) - len(lines[1]))
            if best is None or score < best[0]:
                best = (score, lines)
    if best:
        return best[1]
    return [text]


def fit_hook(draw: ImageDraw.ImageDraw, text: str, max_width: int) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(78, 41, -2):
        face = font(size, True)
        lines = wrap_hook(draw, text, face, max_width)
        if all(draw.textlength(line, font=face) <= max_width for line in lines):
            return face, lines
    face = font(42, True)
    return face, wrap_hook(draw, text, face, max_width)


def render(spec: dict, badge_override: str | None = None) -> Image.Image:
    if spec.get("canvas", {}).get("width", WIDTH) not in (None, WIDTH):
        raise ValueError("Thumbnail canvas width is fixed at 1280")
    accent = hex_rgb(spec["accent"])
    image = gradient((WIDTH, HEIGHT))
    glow(image, (180, 80), 420, spec["accent"], 90)
    glow(image, (1100, 640), 380, "#5B4BB5", 70)
    grid(image)
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, WIDTH, 8], fill=accent + (255,))

    brand = font(18, True)
    draw.polygon(
        [(78, 66), (90, 78), (78, 90), (66, 78)],
        fill=accent + (255,),
    )
    draw.text((104, 66), "MERIDIAN", font=brand, fill=accent + (255,))

    badge = badge_override if badge_override is not None else spec["badge"]
    if badge:
        badge_font = font(28, True)
        bbox = badge_font.getbbox(badge)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        pad_x, pad_y = 22, 14
        origin = (64, 108)
        pill = [origin[0], origin[1], origin[0] + pad_x * 2 + text_w, origin[1] + pad_y * 2 + text_h]
        red, green, blue = accent
        luminance = (0.2126 * red + 0.7152 * green + 0.0722 * blue) / 255
        label = (7, 19, 28) if luminance > 0.62 else (240, 245, 251)
        draw.rounded_rectangle(pill, radius=22, fill=accent + (255,))
        draw.text((origin[0] + pad_x - bbox[0], origin[1] + pad_y - bbox[1]), badge, font=badge_font, fill=label + (255,))

    hook_font, lines = fit_hook(draw, spec["hook"], 690)
    y = 210
    for line in lines:
        draw.text((64, y), line, font=hook_font, fill=(240, 245, 251, 255))
        y += hook_font.size + 8

    draw.rectangle([64, 548, 148, 552], fill=accent + (255,))
    draw.text((64, 570), spec["tech"], font=font(32, True), fill=accent + (255,))
    draw.text((64, 618), "DATA FLOW", font=font(16, True), fill=(163, 177, 199, 255))

    panel = (760, 120, 456, 500)
    draw.rounded_rectangle(
        [panel[0], panel[1], panel[0] + panel[2], panel[1] + panel[3]],
        radius=28,
        fill=(28, 37, 54, 210),
        outline=(53, 67, 94, 255),
        width=2,
    )
    inner = (panel[0] + 24, panel[1] + 24, panel[2] - 48, panel[3] - 88)
    painter = MOTIFS[spec["motif"]]
    painter(draw, inner, accent)
    pipe(draw, (panel[0] + 24, panel[1] + panel[3] - 78, panel[2] - 48, 54))
    return image.convert("RGB")


def load_source(path: Path = SOURCE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_pngs(source: dict | None = None) -> list[Path]:
    source = source if source is not None else load_source()
    if source["canvas"]["width"] != WIDTH or source["canvas"]["height"] != HEIGHT:
        raise SystemExit("source.json canvas must be 1280x720")
    written = []
    for spec in source["releases"]:
        image = render(spec)
        destination = ROOT / "thumbnails" / f"{spec['id']}.png"
        image.save(destination, format="PNG", optimize=True, compress_level=9)
        written.append(destination)
    return written


def write_contact_sheet(paths: list[Path]) -> Path:
    thumb_width, thumb_height = 320, 180
    label_height, columns = 30, 3
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), (8, 12, 22))
    draw = ImageDraw.Draw(sheet)
    label_font = font(18, True)
    for index, path in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        x = index % columns * thumb_width
        y = index // columns * (thumb_height + label_height)
        sheet.paste(image, (x, y))
        draw.text((x + 10, y + thumb_height + 4), path.stem, font=label_font, fill=(240, 244, 252))
    destination = ROOT / "thumbnails" / "contact-sheet.png"
    sheet.save(destination, format="PNG", optimize=True, compress_level=9)
    return destination


def main() -> int:
    written = write_pngs()
    for path in written:
        print(f"{path.relative_to(ROOT)} {path.stat().st_size} bytes")
    contact_sheet = write_contact_sheet(written)
    print(f"{contact_sheet.relative_to(ROOT)} {contact_sheet.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
