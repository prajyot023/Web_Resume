"""Render the site from :class:`ResumeData` using Jinja2, and stage static
assets into the output directory.
"""

from __future__ import annotations

import shutil
from dataclasses import asdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .parsers.base import ResumeData

# Static files copied verbatim into the build output.
STATIC_FILES = (
    "styles.css",
    "script.js",
    "manifest.json",
    "sw.js",
    "sitemap.xml",
    "robots.txt",
    "privacy.html",
    "terms.html",
    "favicon.svg",
)

PORTRAIT_NAME = "hero-portrait.jpg"


def _build_jsonld(data: ResumeData) -> dict:
    job_title = (data.hero.eyebrow.split("·")[0].strip()
                 if data.hero.eyebrow else "")
    same_as = []
    if data.contact.linkedin:
        same_as.append(data.contact.linkedin)
    if data.integrations.githubUsername:
        same_as.append(f"https://github.com/{data.integrations.githubUsername}")

    jsonld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": data.name.full,
        "url": data.meta.siteUrl,
    }
    if job_title:
        jsonld["jobTitle"] = job_title
    if same_as:
        jsonld["sameAs"] = same_as
    if data.skillBars:
        jsonld["knowsAbout"] = [s.name for s in data.skillBars]
    return jsonld


def build_context(data: ResumeData) -> dict:
    return {
        "data": data,
        "integrations": asdict(data.integrations),
        "pfdata": {"rotatingRoles": data.hero.rotatingRoles},
        "jsonld": _build_jsonld(data),
    }


def render_site(
    data: ResumeData,
    *,
    templates_dir: Path,
    project_root: Path,
    out_dir: Path,
) -> Path:
    """Render index.html and copy static assets into ``out_dir``."""
    templates_dir = Path(templates_dir)
    project_root = Path(project_root)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("index.html.j2")
    html = template.render(**build_context(data))

    index_path = out_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")
    print(f"  [render] wrote {index_path}")

    # Copy static files that exist.
    for name in STATIC_FILES:
        src = project_root / name
        if src.exists():
            shutil.copy2(src, out_dir / name)
        else:
            print(f"  [render] note: {name} not found, skipping")

    # Seed assets/ (the portrait is (re)written afterwards by images.py).
    src_assets = project_root / "assets"
    out_assets = out_dir / "assets"
    out_assets.mkdir(parents=True, exist_ok=True)
    if src_assets.is_dir():
        for item in src_assets.iterdir():
            if item.is_file():
                shutil.copy2(item, out_assets / item.name)

    return index_path
