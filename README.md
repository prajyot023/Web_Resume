# Resume-driven Portfolio (Python generator)

An animated portfolio site whose entire content is generated from a single
resume file. Edit one file, run one command, and the whole site — text, metrics,
experience, projects, skills, education, contact, signature, SEO meta, and the
portrait photo — regenerates. All front-end features (scroll-split hero, reveals,
tilt, metric counters, theme toggle, etc.) are preserved.

The published site is plain static **HTML/CSS/JS**. Python is only the build tool.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Build from resume/resume.yaml into dist/
.venv/bin/python generate.py

# Build and preview at http://localhost:8000
.venv/bin/python generate.py --serve
```

Deploy by serving the generated `dist/` directory on any static host.

## Change the content

1. Edit **`resume/resume.yaml`** — the single source of truth. Every field maps
   to a section of the site; arrays (experience, projects, skills, …) can have any
   number of entries.
2. Replace **`resume/photo.jpg`** (or `photo.png` / `portrait.*`) to change the
   portrait. It is auto-optimised to a web-friendly JPEG.
3. Re-run `python generate.py`.

Empty `integrations` keys are detected and the related UI (GitHub card, booking
buttons, newsletter, analytics) is removed cleanly — no broken links or scripts.

## Use a different resume

```bash
# Reliable: fill resume/resume.yaml from your resume, then:
.venv/bin/python generate.py

# Best-effort PDF (no AI): extracts name/title/contact + the embedded photo,
# and warns about fields it can't map. Fill the rest into resume.yaml.
.venv/bin/python generate.py --source resume/your-resume.pdf --parser pdf
```

## Architecture

```
resume/resume.yaml ─┐
(or resume.pdf)     │   parser ──► ResumeData ──► Jinja2 templates ──► dist/
resume/photo.jpg ───┘                              + optimised portrait
```

- `generate.py` — CLI orchestrator (parse → render → image → optional `--serve`).
- `portfolio/parsers/` — pluggable parsers behind one interface:
  - `YamlParser` (default, reliable)
  - `PdfParser` (heuristic, no AI, best-effort)
  - `AiParser` (built but inert — see below)
- `portfolio/render.py` — Jinja2 rendering + static asset staging.
- `portfolio/images.py` — portrait extraction/optimisation (Pillow + PyMuPDF).
- `templates/index.html.j2` — the page template (design unchanged from the
  original site; content comes from `ResumeData`).
- `styles.css`, `script.js`, `favicon.svg`, `manifest.json`, `sw.js`,
  `sitemap.xml`, `robots.txt`, `privacy.html`, `terms.html` — static assets copied
  verbatim into `dist/`.

## Enabling AI parsing later

The AI parser is wired to the same interface but disabled by default. To turn it
on:

1. Uncomment `anthropic` in `requirements.txt` and `pip install anthropic`.
2. `export ANTHROPIC_API_KEY=...`
3. Set `AI_PARSER_ENABLED = True` in `portfolio/parsers/ai_parser.py`.
4. `python generate.py --parser ai --source resume/your-resume.pdf`

No other changes are needed.
