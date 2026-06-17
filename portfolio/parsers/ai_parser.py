"""Future AI-powered parser — built, but inert by default.

This implements the same :class:`ResumeParser` interface as the others, so the
generator already knows how to use it. It is intentionally disabled: enabling it
later requires no architectural change, only:

    1. pip install anthropic   (also uncomment it in requirements.txt)
    2. export ANTHROPIC_API_KEY=...
    3. python generate.py --parser ai --source resume/resume.pdf

The implementation below is wired but guarded so it never runs accidentally and
never adds a hard dependency today.
"""

from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path

from .base import ResumeData, ResumeParser

# Flip to True (and install/configure anthropic) to actually call the API.
AI_PARSER_ENABLED = False

# Latest Claude model at time of writing; update when migrating.
DEFAULT_MODEL = "claude-opus-4-8"


class AiParser(ResumeParser):
    name = "ai"

    def parse(self) -> ResumeData:
        if not AI_PARSER_ENABLED:
            raise RuntimeError(
                "The AI parser is not enabled yet.\n"
                "It is built for the future but intentionally inert. To turn it "
                "on:\n"
                "  1. Uncomment `anthropic` in requirements.txt and "
                "`pip install anthropic`\n"
                "  2. Set ANTHROPIC_API_KEY in your environment\n"
                "  3. Set AI_PARSER_ENABLED = True in portfolio/parsers/ai_parser.py\n"
                "Until then, use --parser yaml (default) or --parser pdf."
            )

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set.")

        try:
            import anthropic  # noqa: F401
            import fitz  # PyMuPDF
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "AI parser needs `anthropic` and `pymupdf` installed."
            ) from exc

        # Extract raw text from the source PDF.
        with fitz.open(self.source) as doc:
            resume_text = "\n".join(page.get_text() for page in doc)

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=4096,
            system=self._system_prompt(),
            messages=[{"role": "user", "content": resume_text}],
        )
        payload = "".join(
            block.text for block in message.content if block.type == "text"
        )
        raw = json.loads(payload)
        return ResumeData.from_dict(raw)

    @staticmethod
    def _system_prompt() -> str:
        return textwrap.dedent(
            """
            You convert resume text into structured JSON for a portfolio site.
            Return ONLY a JSON object (no prose, no code fences) matching this
            shape, omitting unknown fields:
            {
              "meta": {"title": "", "description": ""},
              "brand": "", "name": {"first": "", "last": ""},
              "hero": {"eyebrow": "", "availability": "", "summary": "",
                       "rotatingRoles": []},
              "metrics": [{"value": 0, "suffix": "", "label": ""}],
              "about": {"heading": "", "paragraphs": []},
              "experience": [{"date": "", "title": "", "meta": "",
                              "description": ""}],
              "projects": [{"kicker": "", "title": "", "description": "",
                            "tags": []}],
              "skillBars": [{"name": "", "level": 0}],
              "skillCards": [{"title": "", "description": ""}],
              "education": [{"line": "", "title": ""}],
              "contact": {"email": "", "phone": "", "linkedin": ""}
            }
            For skillBars.level, estimate 0-100 proficiency. Keep summaries
            concise and professional.
            """
        ).strip()
