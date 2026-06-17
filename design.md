# Animated Resume Design

## Direction
- Build the resume as the first screen, not as a marketing landing page.
- Lead with the candidate name, automation role, proof points, and contact actions.
- Use a full-bleed editorial workspace image as the hero visual, with readable text layered directly over the image.
- Keep the tone polished, energetic, and practical for a QA automation engineering profile.

## Visual System
- Palette: ink black, warm white, coral, mint, amber, and a restrained blue accent.
- Cards: 8px radius maximum, used only for repeated resume items such as projects, metrics, skills, and timeline entries.
- Typography: system sans-serif, high contrast, compact headings inside panels, no viewport-scaled font sizes.
- Motion: reveal sections on scroll, rotate the role line, animate metrics, use subtle hover tilt, and respect reduced-motion preferences.

## Layout
- Sticky top navigation with compact contact and utility actions.
- Hero height stays below a full viewport so the next resume band is visible.
- Sections: snapshot, about, experience, automation experience, projects, skills, education, contact.
- Print styles convert the page into a clean resume document.

## Asset
- Hero visual: `resume/photo.jpg`, auto-optimized into `dist/assets/hero-portrait.jpg`.

## Content source
- All page content is generated from `resume/resume.yaml` via the Python generator
  (`python generate.py`). Edit the YAML (or swap in a new resume) and rebuild — the
  templates in `templates/` and the data drive everything. See `README.md`.
