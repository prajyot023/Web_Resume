# Web Resume

A data-driven personal portfolio site. All content lives in a single YAML file;
a small Python build pipeline renders it into a fast, fully static website — no
runtime, no database, no framework lock-in.

**Live:** https://prajyot023.github.io/Web_Resume/

---

## Highlights

- **Single source of truth** — every word, metric, and link comes from
  [`resume/resume.yaml`](resume/resume.yaml). Edit one file, rebuild, done.
- **Static output** — the build emits plain HTML/CSS/JS into `dist/`, hostable
  anywhere with zero server-side code.
- **Pluggable parsers** — swap the content source (YAML today; PDF and an
  optional AI parser are built in) without touching the rendering layer.
- **Progressive Web App** — installable, offline-capable via a service worker
  and web app manifest.
- **SEO-ready** — generated `schema.org` JSON-LD, canonical URLs, sitemap,
  robots, and Open Graph metadata.
- **Continuous deployment** — every push to `main` builds and publishes to
  GitHub Pages automatically.

---

## Tech Stack

| Layer          | Tooling                                             |
| -------------- | --------------------------------------------------- |
| Build          | Python 3.12                                         |
| Templating     | Jinja2                                              |
| Content        | PyYAML                                               |
| Image pipeline | Pillow (portrait optimisation), PyMuPDF (PDF extract) |
| Front end      | Hand-authored HTML, CSS, and vanilla JavaScript     |
| Hosting        | GitHub Pages via GitHub Actions                     |

---

## Quick Start

**Prerequisite:** Python 3.10+.

```bash
# 1. Create the virtual environment and install dependencies (first time only)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Build and preview locally
.venv/bin/python generate.py --serve
```

Open **http://localhost:8000** and press `Ctrl + C` to stop.

> **macOS shortcut:** double-click `start.command` in Finder. It handles setup,
> builds the site, and opens it in your browser automatically.

---

## Usage

### Build only

```bash
.venv/bin/python generate.py
```

Produces the static site in `dist/` without starting a preview server.

### Build and preview

```bash
.venv/bin/python generate.py --serve [--port 8000]
```

### Alternative sources

```bash
# Parse a PDF resume with the heuristic parser
.venv/bin/python generate.py --source resume/resume.pdf --parser pdf

# Custom output directory
.venv/bin/python generate.py --out build/
```

The parser is inferred from the file extension when `--parser` is omitted.

---

## Editing Your Content

1. Edit [`resume/resume.yaml`](resume/resume.yaml) — name, roles, experience,
   projects, skills, contact details, and site metadata.
2. Replace `resume/photo.jpg` to change the portrait. It is automatically
   resized and compressed to a web-friendly JPEG during the build.
3. Rebuild with any command above; changes appear immediately.

---

## How It Works

```
resume.yaml ──▶ Parser ──▶ ResumeData ──▶ Jinja2 template ──▶ dist/index.html
photo.jpg ────▶ Pillow (resize + compress) ─────────────────▶ dist/assets/hero-portrait.jpg
                                                              + static assets copied verbatim
```

1. **Parse** — a parser reads the source and produces a typed `ResumeData`
   object. Missing fields are tolerated, so partial resumes still render.
2. **Render** — Jinja2 fills the template and generates SEO metadata (JSON-LD,
   canonical URL, Open Graph).
3. **Optimise** — the portrait is normalised to a capped, progressive JPEG.
4. **Emit** — everything is written to `dist/`, ready to deploy.

---

## Project Structure

| Path                    | Purpose                                          |
| ----------------------- | ------------------------------------------------ |
| `resume/resume.yaml`    | Content — the single source of truth             |
| `resume/photo.jpg`      | Portrait image                                   |
| `generate.py`           | Build entry point / CLI                          |
| `portfolio/`            | Parsers, renderer, and image pipeline            |
| `templates/`            | Jinja2 page templates                            |
| `styles.css`, `script.js` | Front-end design and interactivity             |
| `sw.js`, `manifest.json`  | Progressive Web App configuration              |
| `dist/`                 | Generated static site (build output)             |

---

## Deployment

Deployment is **automatic**. Every push to `main` triggers the
[GitHub Actions workflow](.github/workflows/deploy.yml), which builds the site
and publishes it to GitHub Pages:

```bash
git add -A
git commit -m "Update content"
git push
```

Changes go live at https://prajyot023.github.io/Web_Resume/ within a minute or two.

To host elsewhere, run `generate.py` and upload the `dist/` folder to any static
host (Netlify, Vercel, Cloudflare Pages, etc.).

---

## License

Personal project. All rights reserved unless stated otherwise.
