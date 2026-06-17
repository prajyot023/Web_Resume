"""Reliable, default parser: reads a structured ``resume.yaml`` (or .json)."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from .base import ResumeData, ResumeParser


class YamlParser(ResumeParser):
    name = "yaml"

    def parse(self) -> ResumeData:
        if not self.source.exists():
            raise FileNotFoundError(f"Resume file not found: {self.source}")

        text = self.source.read_text(encoding="utf-8")
        if self.source.suffix.lower() == ".json":
            raw = json.loads(text)
        else:
            raw = yaml.safe_load(text)

        if not isinstance(raw, dict):
            raise ValueError(
                f"{self.source} must contain a mapping at the top level."
            )
        return ResumeData.from_dict(raw)
