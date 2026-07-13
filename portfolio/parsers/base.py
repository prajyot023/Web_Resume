"""Resume data model and the parser interface.

``ResumeData`` mirrors the structure of ``resume/resume.yaml`` and is the single
shape consumed by the templates. Parsers are responsible for producing one of
these from whatever source they understand.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass
class Meta:
    siteUrl: str = ""
    title: str = ""
    description: str = ""
    ogImage: str = ""
    canonical: str = ""
    author: str = ""
    themeColor: str = "#000000"


@dataclass
class Name:
    first: str = ""
    last: str = ""

    @property
    def full(self) -> str:
        return f"{self.first} {self.last}".strip()


@dataclass
class Hero:
    eyebrow: str = ""
    availability: str = ""
    summary: str = ""
    rotatingRoles: list[str] = field(default_factory=list)


@dataclass
class Metric:
    value: int = 0
    suffix: str = ""
    label: str = ""


@dataclass
class About:
    heading: str = ""
    paragraphs: list[str] = field(default_factory=list)


@dataclass
class Experience:
    date: str = ""
    title: str = ""
    meta: str = ""
    description: str = ""


@dataclass
class Project:
    kicker: str = ""
    title: str = ""
    description: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class SkillBar:
    name: str = ""
    level: int = 0


@dataclass
class SkillCard:
    title: str = ""
    description: str = ""


@dataclass
class Education:
    line: str = ""
    title: str = ""


@dataclass
class Contact:
    copy: str = ""
    resumeUrl: str = ""
    email: str = ""
    phone: str = ""          # display form, e.g. "+91 70587 74113"
    phoneRaw: str = ""       # dial form, e.g. "+917058774113"
    whatsapp: str = ""       # number for wa.me, digits only
    linkedin: str = ""


@dataclass
class DearVisitor:
    kicker: str = "Dear visitor,"
    message: str = ""
    closing: str = "Sincerely,"


@dataclass
class Footer:
    credit: str = ""


@dataclass
class Integrations:
    gaId: str = ""
    clarityId: str = ""
    web3formsKey: str = ""
    githubUsername: str = ""
    buttondownUsername: str = ""
    calUrl: str = ""


@dataclass
class ResumeData:
    meta: Meta = field(default_factory=Meta)
    brand: str = ""
    name: Name = field(default_factory=Name)
    hero: Hero = field(default_factory=Hero)
    metrics: list[Metric] = field(default_factory=list)
    about: About = field(default_factory=About)
    experience: list[Experience] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    skillBars: list[SkillBar] = field(default_factory=list)
    skillCards: list[SkillCard] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    contact: Contact = field(default_factory=Contact)
    dearVisitor: DearVisitor = field(default_factory=DearVisitor)
    footer: Footer = field(default_factory=Footer)
    integrations: Integrations = field(default_factory=Integrations)

    # ------------------------------------------------------------------ #
    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "ResumeData":
        """Build a ResumeData from a plain (YAML/JSON) dict, tolerating
        missing keys so partially-filled resumes still render."""
        raw = raw or {}

        def build(klass, value):
            value = value or {}
            known = {f.name for f in klass.__dataclass_fields__.values()}
            return klass(**{k: v for k, v in value.items() if k in known})

        def build_list(klass, values):
            return [build(klass, v) for v in (values or [])]

        return cls(
            meta=build(Meta, raw.get("meta")),
            brand=raw.get("brand", ""),
            name=build(Name, raw.get("name")),
            hero=build(Hero, raw.get("hero")),
            metrics=build_list(Metric, raw.get("metrics")),
            about=build(About, raw.get("about")),
            experience=build_list(Experience, raw.get("experience")),
            projects=build_list(Project, raw.get("projects")),
            skillBars=build_list(SkillBar, raw.get("skillBars")),
            skillCards=build_list(SkillCard, raw.get("skillCards")),
            education=build_list(Education, raw.get("education")),
            contact=build(Contact, raw.get("contact")),
            dearVisitor=build(DearVisitor, raw.get("dearVisitor")),
            footer=build(Footer, raw.get("footer")),
            integrations=build(Integrations, raw.get("integrations")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# --------------------------------------------------------------------------- #
# Parser interface
# --------------------------------------------------------------------------- #

class ResumeParser(ABC):
    """Turns a resume source into :class:`ResumeData`."""

    #: human-friendly name used in CLI/--parser
    name: str = "base"

    def __init__(self, source: Path):
        self.source = Path(source)

    @abstractmethod
    def parse(self) -> ResumeData:
        """Return structured resume data."""
        raise NotImplementedError


def get_parser(kind: str, source: Path) -> ResumeParser:
    """Factory: resolve a ``--parser`` choice to a concrete parser.

    Imports are local so an unused parser's optional deps (PyMuPDF, anthropic)
    are never required.
    """
    kind = (kind or "yaml").lower()
    if kind == "yaml":
        from .yaml_parser import YamlParser
        return YamlParser(source)
    if kind == "pdf":
        from .pdf_parser import PdfParser
        return PdfParser(source)
    if kind == "ai":
        from .ai_parser import AiParser
        return AiParser(source)
    raise ValueError(f"Unknown parser: {kind!r} (expected yaml | pdf | ai)")
