# My Portfolio Website

A personal portfolio/resume website. All the content comes from **one file**
(`resume/resume.yaml`). Change that file, run one command, and the whole website
updates — text, photo, everything.

🌐 **Live site:** https://prajyot023.github.io/Web_Resume/

---

## How to run it

**Easiest way:** double-click **`start.command`** in Finder. It builds the site
and opens **http://localhost:8000** in your browser. Close the Terminal window to stop.

**Or from a terminal** in this folder:

```bash
.venv/bin/python generate.py --serve
```

Then open **http://localhost:8000** in your browser.
Press `Ctrl + C` to stop.

That's it. 🎉

---

## How to change my details

1. Open **`resume/resume.yaml`** and edit your name, jobs, skills, etc.
2. To change the photo, replace **`resume/photo.jpg`** with your own picture.
3. Run the command again:

```bash
.venv/bin/python generate.py --serve
```

Your changes show up instantly.

---

## First time setup (only once)

If the `.venv` folder is missing, create it first:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then use the run command above.

---

## Where things live

| File / Folder        | What it is                                  |
| -------------------- | ------------------------------------------- |
| `resume/resume.yaml` | **Your content** — edit this               |
| `resume/photo.jpg`   | **Your photo** — replace this              |
| `dist/`              | The finished website (created when you run) |
| `templates/`         | The page layout (you usually don't touch)   |
| `styles.css`         | The colors and design                       |
| `generate.py`        | The command that builds the site            |

---

## Putting it online

**It's already automatic.** Every time you push to the `main` branch, GitHub
Actions rebuilds the site and publishes it to GitHub Pages — no manual steps:

```bash
git add -A
git commit -m "Update my details"
git push
```

Your changes go live at https://prajyot023.github.io/Web_Resume/ within a minute
or two.

**Somewhere else?** Run `generate.py`, then upload the **`dist/`** folder to any
web host (Netlify, Vercel, etc.). No server needed — it's just files.

---

## Build only (no preview)

```bash
.venv/bin/python generate.py
```

This just creates/updates the `dist/` folder without opening a browser.
