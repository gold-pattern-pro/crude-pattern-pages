#!/usr/bin/env python3
"""Regenerate PNG favicons for a site (full-bleed, no dark outer ring).

Usage:
  python scripts/gen-site-icons.py gold
  python scripts/gen-site-icons.py crude
  python scripts/gen-site-icons.py forex
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("pip install pillow") from None

ROOT = Path(__file__).resolve().parent.parent

THEMES = {
    "gold": {
        "dir": ROOT / "assets" / "images",
        "label": "Au",
        "top": (245, 230, 179, 255),
        "bot": (201, 162, 39, 255),
        "text": (26, 18, 4, 255),
    },
    "crude": {
        "dir": ROOT / "_crude" / "assets" / "images",
        "label": "CP",
        "top": (94, 234, 212, 255),
        "bot": (234, 88, 12, 255),
        "text": (255, 255, 255, 255),
    },
    "forex": {
        "dir": ROOT / "_forex" / "assets" / "images",
        "label": "FX",
        "top": (96, 165, 250, 255),
        "bot": (29, 78, 216, 255),
        "text": (255, 255, 255, 255),
    },
}


def draw_icon(size: int, theme: dict) -> Image.Image:
    radius = max(8, size // 5)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=theme["bot"])
    d.rounded_rectangle([0, 0, size - 1, size // 2], radius=radius, fill=theme["top"])
    font_size = max(12, size // 3)
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("Arial Bold.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()
    text = theme["label"]
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(
        ((size - tw) / 2, (size - th) / 2 - size * 0.04),
        text,
        fill=theme["text"],
        font=font,
    )
    return img


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in THEMES:
        print("Usage: gen-site-icons.py", "|".join(THEMES))
        sys.exit(1)
    theme = THEMES[sys.argv[1]]
    out = theme["dir"]
    out.mkdir(parents=True, exist_ok=True)
    for name, px in (("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)):
        path = out / name
        draw_icon(px, theme).save(path, "PNG")
        print("wrote", path)


if __name__ == "__main__":
    main()
