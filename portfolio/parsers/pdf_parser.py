"""Best-effort, no-AI PDF parser.

Extracts plain text from a PDF and applies simple heuristics to recover the
most common resume fields. Resume layouts vary wildly, so this is intentionally
conservative: it fills what it can confidently detect, warns about everything it
could not map, and leaves the rest blank for the user to complete in
``resume.yaml``. For reliable results, prefer the YAML parser (or enable the AI
parser in the future).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from .base import (
    About,
    Contact,
    Hero,
    Meta,
    Name,
    ResumeData,
    ResumeParser,
)

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\d\s\-]{7,}\d)")
LINKEDIN_RE = re.compile(r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+", re.I)


def _warn(msg: str) -> None:
    print(f"  [pdf] warning: {msg}", file=sys.stderr)


class PdfParser(ResumeParser):
    name = "pdf"

    def parse(self) -> ResumeData:
        try:
            import fitz  # PyMuPDF
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "PyMuPDF is required for --parser pdf. Install with "
                "`pip install -r requirements.txt`."
            ) from exc

        if not self.source.exists():
            raise FileNotFoundError(f"Resume PDF not found: {self.source}")

        with fitz.open(self.source) as doc:
            text = "\n".join(page.get_text() for page in doc)

        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        data = ResumeData()

        # --- Name: assume the first non-empty line is the candidate name ---
        if lines:
            parts = lines[0].split()
            if len(parts) >= 2:
                data.name = Name(first=parts[0], last=" ".join(parts[1:]))
            else:
                data.name = Name(first=lines[0], last="")
            data.brand = data.name.first
        else:
            _warn("no text extracted — is this a scanned/image-only PDF?")

        # --- Title / headline: the line after the name, if it looks like one --
        if len(lines) >= 2 and len(lines[1]) <= 80:
            data.hero = Hero(eyebrow=lines[1])
            data.meta = Meta(
                title=f"{data.name.full} | {lines[1]}".strip(" |"),
                author=data.name.full,
            )

        # --- Contact details via regex over the whole document ---
        contact = Contact()
        if m := EMAIL_RE.search(text):
            contact.email = m.group(0)
        if m := LINKEDIN_RE.search(text):
            contact.linkedin = m.group(0)
            if not contact.linkedin.startswith("http"):
                contact.linkedin = "https://" + contact.linkedin
        if m := PHONE_RE.search(text):
            raw = re.sub(r"[^\d+]", "", m.group(0))
            contact.phone = m.group(0).strip()
            contact.phoneRaw = raw
            contact.whatsapp = raw.lstrip("+")
        data.contact = contact

        # --- Summary: first longish paragraph after the headline ---
        summary = next((ln for ln in lines[2:] if len(ln) > 120), "")
        if summary:
            data.about = About(heading="About", paragraphs=[summary])
            if data.hero:
                data.hero.summary = summary

        # Heuristics can't reliably segment experience/projects/skills.
        _warn(
            "experience, projects, skills, education and metrics could not be "
            "auto-detected. Fill them into resume.yaml, then run with the "
            "default parser. PDF parsing is best-effort only."
        )
        return data
