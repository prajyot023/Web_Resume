#!/usr/bin/env python3
"""Generate the portfolio site from a resume file.

Usage:
    python generate.py                         # build from resume/resume.yaml
    python generate.py --source resume/r.pdf --parser pdf
    python generate.py --serve                 # build, then preview locally
    python generate.py --parser ai --source resume/r.pdf   # future (inert)

Pipeline:  parse resume -> ResumeData -> render templates + optimise photo -> dist/
The visible site stays plain HTML/CSS/JS, so every front-end feature is preserved.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from portfolio.images import resolve_portrait
from portfolio.parsers import get_parser
from portfolio.render import PORTRAIT_NAME, render_site

DEFAULT_SOURCE = ROOT / "resume" / "resume.yaml"
TEMPLATES_DIR = ROOT / "templates"
RESUME_DIR = ROOT / "resume"
ASSETS_DIR = ROOT / "assets"
OUT_DIR = ROOT / "dist"


def build(source: Path, parser_kind: str, out_dir: Path) -> Path:
    # Start from a clean output dir so stale files never linger.
    if out_dir.exists():
        import shutil
        shutil.rmtree(out_dir)

    print(f"→ Parsing {source} (parser: {parser_kind})")
    parser = get_parser(parser_kind, source)
    data = parser.parse()
    print(f"  parsed resume for: {data.name.full or '(unknown)'}")

    print("→ Rendering site")
    render_site(
        data,
        templates_dir=TEMPLATES_DIR,
        project_root=ROOT,
        out_dir=out_dir,
    )

    print("→ Preparing portrait")
    resolve_portrait(
        source=source,
        resume_dir=RESUME_DIR,
        assets_dir=ASSETS_DIR,
        dest=out_dir / "assets" / PORTRAIT_NAME,
    )

    print(f"✓ Built site → {out_dir}")
    return out_dir


def serve(directory: Path, port: int = 8000) -> None:
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(directory)
    )
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\nServing {directory} at http://localhost:{port}  (Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the portfolio site.")
    ap.add_argument(
        "--source", type=Path, default=DEFAULT_SOURCE,
        help="Resume source file (default: resume/resume.yaml).",
    )
    ap.add_argument(
        "--parser", choices=["yaml", "pdf", "ai"], default=None,
        help="Parser to use (default: inferred from the source extension).",
    )
    ap.add_argument(
        "--out", type=Path, default=OUT_DIR,
        help="Output directory (default: dist/).",
    )
    ap.add_argument(
        "--serve", action="store_true",
        help="Start a local preview server after building.",
    )
    ap.add_argument("--port", type=int, default=8000, help="Preview port.")
    args = ap.parse_args(argv)

    parser_kind = args.parser
    if parser_kind is None:
        parser_kind = "pdf" if args.source.suffix.lower() == ".pdf" else "yaml"

    try:
        build(args.source, parser_kind, args.out)
    except Exception as exc:  # surface a clean message, not a traceback wall
        print(f"\n✗ Build failed: {exc}", file=sys.stderr)
        return 1

    if args.serve:
        serve(args.out, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
