"""Portrait image pipeline.

Resolves a portrait for the site from one of (in priority order):
  1. the largest embedded image inside a source PDF (if a PDF was given), then
  2. a photo file dropped next to the resume (resume/photo.*), then
  3. an existing/default portrait already in assets/.

The chosen image is normalised to a web-friendly JPEG (cap longest edge, quality
~82) — the Python equivalent of the earlier one-off `sips` optimisation.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

from PIL import Image

MAX_EDGE = 1080            # cap longest side; portrait source is ~807x1074
JPEG_QUALITY = 82
PHOTO_STEMS = ("photo", "portrait", "headshot")
PHOTO_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def _log(msg: str) -> None:
    print(f"  [image] {msg}")


def _save_optimized(img: Image.Image, dest: Path) -> Path:
    img = img.convert("RGB")
    w, h = img.size
    scale = MAX_EDGE / max(w, h)
    if scale < 1:
        img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    kb = dest.stat().st_size / 1024
    _log(f"wrote {dest} ({img.width}x{img.height}, {kb:.0f} KB)")
    return dest


def _extract_from_pdf(pdf_path: Path) -> Image.Image | None:
    """Return the largest embedded raster image in the PDF, or None."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None

    best: tuple[int, bytes] | None = None
    with fitz.open(pdf_path) as doc:
        for page in doc:
            for xref, *_ in page.get_images(full=True):
                try:
                    raw = doc.extract_image(xref)
                except Exception:
                    continue
                data = raw.get("image")
                if not data:
                    continue
                area = raw.get("width", 0) * raw.get("height", 0)
                if best is None or area > best[0]:
                    best = (area, data)

    if best is None:
        return None
    try:
        img = Image.open(io.BytesIO(best[1]))
        img.load()
        # Reject tiny logos/icons that aren't a real portrait.
        if min(img.size) < 200:
            return None
        return img
    except Exception:
        return None


def _find_photo_file(resume_dir: Path) -> Path | None:
    for stem in PHOTO_STEMS:
        for ext in PHOTO_EXTS:
            candidate = resume_dir / f"{stem}{ext}"
            if candidate.exists():
                return candidate
    return None


def resolve_portrait(
    *,
    source: Path,
    resume_dir: Path,
    assets_dir: Path,
    dest: Path,
) -> Path | None:
    """Produce the optimised portrait at ``dest``. Returns the path or None."""
    source = Path(source)

    # 1. Embedded image from a PDF source.
    if source.suffix.lower() == ".pdf" and source.exists():
        img = _extract_from_pdf(source)
        if img is not None:
            _log(f"extracted portrait from {source.name}")
            return _save_optimized(img, dest)
        _log(f"no usable embedded image in {source.name}; trying a photo file")

    # 2. A dropped photo file.
    photo = _find_photo_file(Path(resume_dir))
    if photo is not None:
        _log(f"using {photo}")
        return _save_optimized(Image.open(photo), dest)

    # 3. Existing default portrait already in assets/.
    existing = Path(assets_dir) / dest.name
    if existing.exists():
        if existing.resolve() != dest.resolve():
            _save_optimized(Image.open(existing), dest)
        _log(f"keeping existing portrait {existing}")
        return existing

    print(
        "  [image] warning: no portrait found (no PDF image, no resume/photo.*, "
        "no existing asset). The portrait area will be empty.",
        file=sys.stderr,
    )
    return None
