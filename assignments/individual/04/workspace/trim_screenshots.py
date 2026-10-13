#!/usr/bin/env python3
"""Crop the empty white area below the content of full-page UI screenshots."""
from pathlib import Path
from PIL import Image, ImageChops

for png in sorted((Path(__file__).parent / "screenshots").glob("*.png")):
    im = Image.open(png).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bbox = ImageChops.difference(im, bg).getbbox()
    if bbox:
        bottom = min(im.height, bbox[3] + 24)
        if bottom < im.height - 10:
            im.crop((0, 0, im.width, bottom)).save(png)
            print(f"{png.name}: {im.height} -> {bottom}px")
