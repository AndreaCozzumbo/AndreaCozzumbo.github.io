#!/usr/bin/env python3
"""Put your photos on the Photography page.

    python3 scripts/prepare_photos.py                 # uses the folder "photos" next to AC_web
    python3 scripts/prepare_photos.py <other-folder>

In the catalogue the highest number comes first: number the photos 0001, 0002... to choose it.
(The gallery with the arrows is in random order.)
Each sub-folder (BnW, Color) makes a section of the page with its name; empty ones are not shown.
Photos outside the sub-folders are not used: the script lists them.

What it does
  * writes a web copy (long edge 2400 px) and a thumbnail (long edge 1200 px) of each
    photo in assets/photos/, as sRGB JPEG, without ANY metadata (EXIF, GPS, serial numbers)
  * writes _data/photos.yml, the list read by the page. Descriptions (alt:) that you add
    there are kept when you run the script again
  * removes from the site the photos that you removed from the folder

Originals are never modified. Keep them outside AC_web, so they are never uploaded.
Needs Pillow and PyYAML:  python3 -m pip install pillow pyyaml
HEIC and 16-bit scans are read with the macOS tool "sips".
"""
import argparse
import hashlib
import io
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from PIL import Image, ImageCms, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT.parent / "photos"
OUT = ROOT / "assets" / "photos"
DATA = ROOT / "_data" / "photos.yml"
FULL_EDGE, THUMB_EDGE = 2400, 1200
EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".heic"}
HEADER = (
    "# Photos of /photography/, written by scripts/prepare_photos.py.\n"
    "# You can add a description in alt: (read aloud to blind visitors); it is kept,\n"
    "# also when the photo is renamed (id identifies the original file).\n\n"
)


def slugify(name, fallback):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or fallback


def natural(path):
    """Sort key: 2 comes before 10."""
    return [(0, int(t), "") if t.isdigit() else (1, 0, t) for t in re.findall(r"[0-9]+|[^0-9]+", path.name.lower())]


def photos_in(folder):
    return sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in EXTS and not p.name.startswith(".")),
        key=natural,
        reverse=True,  # the highest number comes first
    )


def open_photo(path):
    """Return the photo as an upright sRGB image."""
    try:
        im = Image.open(path)
        im.load()
        if im.mode.startswith(("I", "F")):  # 16-bit scan: Pillow would clip it to white
            raise OSError("16-bit image")
    except OSError:
        with tempfile.TemporaryDirectory() as tmp:
            jpg = Path(tmp) / "photo.jpg"
            run = subprocess.run(
                ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "100", str(path), "--out", str(jpg)],
                capture_output=True,
            )
            if run.returncode or not jpg.exists():
                sys.exit(f"Cannot read {path}")
            im = Image.open(jpg)
            im.load()
    icc = im.info.get("icc_profile")
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGB")
    if icc:
        try:
            profile = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            im = ImageCms.profileToProfile(im, profile, ImageCms.createProfile("sRGB"), outputMode="RGB")
        except ImageCms.PyCMSError:
            pass  # profile not usable for this image: keep the pixel values
    return im.convert("RGB")


def save(im, edge, path):
    im = im.copy()
    im.thumbnail((edge, edge), Image.LANCZOS)
    im.info.clear()  # no metadata in the published file
    path.parent.mkdir(parents=True, exist_ok=True)
    # write aside and move: the local preview must never copy a half-written file
    part = path.with_name(f".{path.name}.part")
    im.save(part, "JPEG", quality=88, optimize=True, progressive=True)
    part.replace(path)
    return im.size


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, nargs="?", default=DEFAULT_SOURCE)
    source = ap.parse_args().source
    if not source.is_dir():
        sys.exit(f"Folder not found: {source}")

    folders = [
        (d, d.name, photos_in(d)) for d in sorted(source.iterdir(), key=natural) if d.is_dir() and not d.name.startswith(".")
    ]
    if not any(files for _, _, files in folders):
        sys.exit(f"No photos in the sub-folders of {source}: nothing changed")

    previous = (yaml.safe_load(DATA.read_text(encoding="utf-8")) if DATA.exists() else None) or []
    old = {p["file"]: p for series in previous for p in series["photos"]}
    alts = {p.get("id", p["file"]): p.get("alt", "") for p in old.values()}

    result, used = [], set()
    for folder, title, files in folders:
        if not files:
            continue
        prefix = slugify(title, "series") + "/"
        photos = []
        for src in files:
            stem = slugify(src.stem, "photo")
            name, n = f"{prefix}{stem}.jpg", 1
            while name in used:
                n += 1
                name = f"{prefix}{stem}-{n}.jpg"
            used.add(name)
            photo_id = "p" + hashlib.sha256(src.read_bytes()).hexdigest()[:10]
            before = old.get(name, {})
            if before.get("id") == photo_id and (OUT / name).exists() and (OUT / "thumbs" / name).exists():
                width, height = before["width"], before["height"]  # already done
            else:
                im = open_photo(src)
                width, height = save(im, FULL_EDGE, OUT / name)
                save(im, THUMB_EDGE, OUT / "thumbs" / name)
                print(f"  {src.name} -> {name} ({width}x{height})")
            alt = alts.get(photo_id, alts.get(name, ""))
            photos.append({"file": name, "id": photo_id, "width": width, "height": height, "alt": alt})
        shown = re.sub(r"^\d+[\s_-]+", "", title).replace("_", " ")
        result.append({"title": shown, "photos": photos})

    DATA.write_text(HEADER + yaml.safe_dump(result, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8")
    for name in set(old) - used:  # only files this script listed before
        for path in (OUT / name, OUT / "thumbs" / name):
            path.unlink(missing_ok=True)
    print(f"{len(used)} photos on the Photography page")
    for path in photos_in(source):
        print(f"  NOT used, move it to a sub-folder: {path.name}")


if __name__ == "__main__":
    main()
