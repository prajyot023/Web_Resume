"""Pluggable resume parsers.

Each parser turns a resume source into a :class:`ResumeData` object. The site
generator is parser-agnostic, so new sources (PDF, AI, ...) can be added without
touching rendering.
"""

from .base import ResumeData, ResumeParser, get_parser

__all__ = ["ResumeData", "ResumeParser", "get_parser"]
