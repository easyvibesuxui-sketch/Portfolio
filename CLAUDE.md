# CLAUDE.md — khomeriki.design

Portfolio of Nodari Khomeriki (product & UX designer). Reply to Nodari in **Georgian**, keep it concise.

## What this is

A hand-rolled **static site**. No framework, no bundler, no npm. Python generates the HTML; the generated HTML is committed, so the repo *is* the site.

- Repo: `github.com/easyvibesuxui-sketch/Portfolio` (branch `main`)
- Hosting: Vercel project **portfolio**, connected to this repo → every push to `main` deploys to production
- Domain: `khomeriki.design` (DNS at Wix, records point to Vercel; apex redirects to `www`)

## Golden rules

1. **Never lose content.** Project texts, case studies, lab entries, CV data and pages must survive every change. Only touch UI (sections, cards, layout, styling) unless explicitly asked to edit content.
2. **Never hand-edit generated HTML** (`index.html`, `work/**/index.html`, `lab/`, `experience/`, `contact/`, `404.html`). Change the Python source, then run `python3 build.py`.
3. **Bump `V` in `build.py`** whenever `assets/css` or `assets/js` change. CSS/JS are served `immutable` for a year, so without a bump visitors keep the old files.
4. Don't invent metrics or numbers in case studies (see the note at the top of `cases.py`).
5. Keep the palette (below). No new accent colours.

## Layout

```
build.py        generator: NAV, PROJECTS list, SERVICES, page_* functions, PAGES map, V (cache-buster)
cases.py        CASES — long-form case study per project slug
lab.py          LAB — AI Lab entries (sorted by `added`, newest first)
cv.py           ROLES, EDUCATION, CERTS, LANGUAGES for /experience
assets/css/glass.css   all styles (light-theme overrides near the end, ~line 2650)
assets/js/      glass.js (main), eyes.js (hero gaze), peek.js (small eyes around the site),
                nebula.js, + vendored gsap / ScrollTrigger / lenis
assets/home/    hero + preloader media, eyes/ layers + manifest.json
assets/projects/<slug>/   case-study images, filled in filename order (01.jpg, 02.jpg …)
assets/lab/<slug>.jpg     AI Lab card images
tools/          image/video pipelines (not deployed)
vercel.json     clean URLs, trailing slash, cache headers, redirects
.vercelignore   keeps *.py, tools/, README.md off the deployed site
_headers        legacy (Netlify-style), not used by Vercel
```

## Commands

```bash
python3 build.py                 # regenerate every page; prints page/byte counts
python3 -m http.server 8000      # preview locally at http://localhost:8000
```

`build.py` itself needs `Pillow` and `numpy` (`pip install Pillow numpy`). Without them it runs without errors but writes different cover markup for some case studies, so run `git status` after a build and check that no unexpected `work/*/index.html` changed.

Tools need `numpy`, `opencv-python`, `Pillow`, and `ffmpeg` for the video graders.

## Common tasks

- **Add/edit a project card:** `PROJECTS` in `build.py`. Its case study lives in `CASES[slug]` in `cases.py`.
- **Add an AI Lab entry:** copy a block in `lab.py`, add `assets/lab/<slug>.jpg`. Lab cards must show a **real screenshot of the project's live site** (1200×600 JPG).
- **Rename/move a page:** add a permanent redirect in `vercel.json`, don't break old URLs.
- **New page:** add a `page_*` function and register it in `PAGES`.

## Design system

| Token | Value | Use |
|---|---|---|
| ground | `#EBEBEB` | page background |
| text | `#3F3F3F` | body text |
| accent | `#FF005C` | the one hot accent |
| dark bands | `#212121` | inverted sections |
| footer | `#1A1A1A` | footer |

Brand direction: **"Everyone's watching"** (attention is the product). Photorealistic eyeball creatures (planets with hands and hair), generated with Kling, on the `#EBEBEB` ground. Small creepy eyes appear across the whole site as accents.

Hero/preloader constraints:
- Eyes follow the cursor.
- The preloader video's **last frame must equal the hero's first frame** (`tools/build_eyes.py` writes `stage.png` for this).
- The central creature follows scroll down to the middle of section two, then stops.
- Kling clips are graded onto exactly `#EBEBEB` with `tools/grade_kling.py` / `tools/grade_reveal.py`.

## Before you push

1. `python3 build.py` runs clean.
2. Diff shows no removed content in `cases.py`, `lab.py`, `cv.py`, `PROJECTS` (unless asked).
3. `V` bumped if CSS/JS changed.
4. Check pages locally (home, /work/, one case study, /lab/, /experience/, /contact/, 404) on desktop and mobile widths.
5. Commit with a short message, push to `main`. Vercel deploys automatically. Confirm on https://www.khomeriki.design.
