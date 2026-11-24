#!/usr/bin/env python3
"""Convert a photo (PNG/JPEG, transparency kept) to a web-ready WebP.

Why: the old site shipped 7 MB of PNG cut-outs; WebP at quality 82 is ~85% smaller
with no visible loss. Needs Pillow (pip install pillow); the site build does not.

Usage:
  python3 tools/optimize_images.py SOURCE.png static/img/menu/new-dish.webp [--max 640]
"""
import argparse
from pathlib import Path

from PIL import Image


def optimize(src: Path, dst: Path, max_width: int = 640, quality: int = 82) -> tuple[int, int]:
    im = Image.open(src)
    im = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") or "transparency" in im.info else im.convert("RGB")
    bbox = im.getbbox() if im.mode == "RGBA" else None
    if bbox:  # trim fully transparent margins so plates fill their frame
        im = im.crop(bbox)
    if im.width > max_width:
        im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "WEBP", quality=quality, method=6)
    return im.size


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("source", type=Path)
    p.add_argument("dest", type=Path)
    p.add_argument("--max", type=int, default=640, help="max width in px (default 640)")
    a = p.parse_args()
    w, h = optimize(a.source, a.dest, a.max)
    print(f"{a.dest} {w}x{h} {a.dest.stat().st_size // 1024} KB")
