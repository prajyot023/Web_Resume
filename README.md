# My Portfolio Website

A personal portfolio/resume website. All the content comes from **one file**
(`resume/resume.yaml`). Change that file, run one command, and the whole website
updates — text, photo, everything.

---

## How to run it

Open a terminal in this folder and run:

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

After running `generate.py`, upload the **`dist/`** folder to any web host
(Netlify, GitHub Pages, Vercel, etc.). No server needed — it's just files.

---

## Build only (no preview)

```bash
.venv/bin/python generate.py
```

This just creates/updates the `dist/` folder without opening a browser.
