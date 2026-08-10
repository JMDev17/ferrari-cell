#!/usr/bin/env python3
"""Convert local images to AVIF and report sizes."""

import os
from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent
FOTOS = BASE / "fotos"

# (source_name, max_width, quality)
IMAGES = [
    ("troca de bateria.png",    1200, 55),
    ("caiu na água.jpeg",       1200, 55),
    ("iphone não carrega.jpeg", 1200, 55),
    ("bateria ruim.jpeg",       1200, 55),
]

def convert(src_name, max_width, quality):
    src = FOTOS / src_name
    if not src.exists():
        print(f"  SKIP (not found): {src_name}")
        return

    stem = src.stem.replace(" ", "-").lower()
    # normalise accented chars
    import unicodedata
    stem = unicodedata.normalize("NFD", stem)
    stem = "".join(c for c in stem if unicodedata.category(c) != "Mn")
    dest_name = stem + ".avif"
    dest = FOTOS / dest_name

    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        img = img.resize((max_width, int(h * ratio)), Image.LANCZOS)
        new_w, new_h = img.size
    else:
        new_w, new_h = w, h

    img.save(dest, format="AVIF", quality=quality)

    src_kb  = src.stat().st_size / 1024
    dest_kb = dest.stat().st_size / 1024
    saving  = (1 - dest_kb / src_kb) * 100
    print(f"  {src_name}")
    print(f"    {src_kb:,.0f} KB  ->  {dest_kb:,.0f} KB  (-{saving:.0f}%)  [{new_w}x{new_h}]  ->  {dest_name}")

print("\n=== Converting images to AVIF ===\n")
for item in IMAGES:
    convert(*item)
print("\nDone.\n")
