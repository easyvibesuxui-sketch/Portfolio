"""Portfolio PDF — 16:9 pages in the site's own look, built from the site's data.

    python3 tools/resume/build_portfolio.py OUT_DIR [HERO_PNG]
    node tools/resume/render.mjs OUT_DIR/portfolio.html OUT.pdf

Text comes from build.py (PROJECTS, SERVICES, STEPS), cases.py and lab.py,
so nothing is retyped and nothing is invented. Images are resized into
OUT_DIR/img so the PDF stays small. HERO_PNG is a 1920x1080 grab of the
home-page creature canvas; without it the cover runs type-only.
"""
import html, os, re, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
import build                      # noqa: E402  (PROJECTS, SERVICES, STEPS, SITE …)
from cases import CASES           # noqa: E402
from lab import LAB               # noqa: E402

OUT = os.path.abspath(sys.argv[1])
HERO = sys.argv[2] if len(sys.argv) > 2 else None
IMG = os.path.join(OUT, "img")
os.makedirs(IMG, exist_ok=True)

SITE = "khomeriki.design"

# the eight that carry the story: platform depth, banking, data, consumer
FEATURED = [
    ("syniotec-sam", "B2B SaaS · Construction",
     ["syniotec-sam-wide.jpg", "syniotec-sam-mobile.jpg", "syniotec-sam.jpg"]),
    ("syniotec-ram", "B2B SaaS · Equipment rental",
     ["syniotec-ram-wide.jpg", "syniotec-ram-mobile.jpg", "syniotec-ram.jpg"]),
    ("seu-admin", "Enterprise · Higher education", None),
    ("seu-student", "Student portal · EdTech", None),
    ("halyk-onboarding", "Fintech · Mobile onboarding", None),
    ("halyk-open-banking", "Fintech · Open banking", None),
    ("deutsche-bank", "Data visualisation · Banking", None),
    ("ioka", "Real estate · Search", None),
]


def img(rel, w=1600, q=82):
    """Resize assets/<rel> into OUT/img and return the local file name."""
    src = os.path.join(ROOT, "assets", rel)
    if not os.path.exists(src):
        return None
    name = rel.replace("/", "_").rsplit(".", 1)[0] + f"_{w}.jpg"
    dst = os.path.join(IMG, name)
    if not os.path.exists(dst):
        im = Image.open(src).convert("RGB")
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(dst, quality=q, optimize=True, progressive=True)
    return "img/" + name


def case_images(slug, explicit):
    if explicit:
        files = [f"projects/{f}" for f in explicit]
    else:
        d = os.path.join(ROOT, "assets", "projects", slug)
        files = [f"projects/{slug}.jpg"]
        if os.path.isdir(d):
            files += [f"projects/{slug}/{f}" for f in sorted(os.listdir(d)) if f.endswith(".jpg")]
    # the main picture fills ~1000px of a 1600px page, thumbs ~470px
    out = [img(f, w=1300 if i == 0 else 760, q=76) for i, f in enumerate(files)]
    return [o for o in out if o]


def plain(s):
    """Case text carries entities and the odd tag; keep it as-is for HTML
    but drop tags so a lead never opens an element it does not close."""
    return re.sub(r"<[^>]+>", "", s or "")


def first_sentence(body):
    t = plain(body[0]) if body else ""
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    return m.group(1) if m else t


def project_title(slug):
    for p in build.PROJECTS:
        if p[0] == slug:
            return p[1]
    return slug


# ------------------------------------------------------------------ pages
pages = []
TOTAL = None  # filled after assembly


def page(body, cls="", n=True):
    pages.append((cls, body, n))


# 1 · cover
hero = ""
if HERO and os.path.exists(HERO):
    im = Image.open(HERO).convert("RGB")
    # keep the central creature and the two on the right; the left one
    # would sit under the name
    im = im.crop((560, 0, 1920, 1080))
    im.save(os.path.join(IMG, "hero.jpg"), quality=86, optimize=True)
    hero = '<img class="cover-hero" src="img/hero.jpg" alt="">'
page(f"""
  {hero}
  <div class="cover-top mono"><span>Portfolio 2026</span><span>{SITE}</span></div>
  <div class="cover-text">
    <div class="eyebrow mono">Everyone’s watching</div>
    <h1>Nodari Khomeriki</h1>
    <p class="cover-role">Senior Product Designer — UX/UI</p>
    <p class="cover-sub">B2B SaaS, fintech and data-heavy interfaces.<br>Design systems, research and shipped product.</p>
  </div>
  <div class="cover-foot mono"><span>Tbilisi, Georgia · Remote worldwide</span><span>contact@khomeriki.design</span><span>+995 99 460466</span></div>
""", "cover", n=False)

# 2 · about
clients = ["syniotec", "Halyk Bank", "Deutsche Bank", "Barclays", "VEON", "SEU University",
           "IOKA", "Miniso Georgia", "Marketcolor", "MVB Club", "Mult Georgia", "Assorti"]
page(f"""
  <div class="kicker mono">About</div>
  <div class="about">
    <div>
      <h2 class="big">Clarity first. Craft always. <em>Built to scale.</em></h2>
      <p class="lead">Senior product designer with 8+ years on B2B SaaS platforms, banking products and
      data-heavy interfaces — for teams in Bremen, London, Amsterdam, Almaty, Dubai and Tbilisi.</p>
      <p>Today I lead UX/UI for syniotec’s construction and equipment-rental platforms, web and iOS/Android,
      used by firms including STRABAG, Kurt König and HOCH. I own work end to end: research, information
      architecture, interaction design, prototyping, design systems and design QA with engineering.</p>
      <p>A finance degree and ACCA papers make fintech and analytics familiar ground, and I build:
      hand-written front-end and AI-assisted products shipped with Claude and Claude Code.</p>
    </div>
    <div>
      <div class="stats">
        <div><b>8+</b><span class="mono">Years in design</span></div>
        <div><b>32</b><span class="mono">Products shipped</span></div>
        <div><b>45</b><span class="mono">Certifications</span></div>
        <div><b>26</b><span class="mono">AI Lab builds</span></div>
      </div>
      <div class="kicker mono" style="margin-top:34px">Selected clients &amp; employers</div>
      <div class="clients">{''.join(f'<span>{c}</span>' for c in clients)}</div>
    </div>
  </div>
""")

# 3 · services + process
svc = "".join(
    f'<div class="svc"><span class="mono n">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>'
    for i, (t, d) in enumerate(build.SERVICES))
steps = "".join(
    f'<li><span class="mono n">0{i+1}</span><b>{t}</b><span>{s}</span></li>'
    for i, (t, s, _) in enumerate(build.STEPS))
page(f"""
  <div class="kicker mono">What I do · How the work happens</div>
  <div class="two">
    <div class="svcs">{svc}</div>
    <div>
      <h2 class="mid">Five moves, every time.</h2>
      <p class="muted">Same shape on a six-week engagement and a two-year platform. Only the length of each move changes.</p>
      <ol class="steps">{steps}</ol>
    </div>
  </div>
""")

# 4…n · featured case studies
for i, (slug, label, explicit) in enumerate(FEATURED):
    c = CASES[slug]
    ims = case_images(slug, explicit)
    main = ims[0] if ims else None
    thumbs = ims[1:3]
    decisions = c["solution"].get("decisions", [])[:3]
    dec = "".join(f"<li>{plain(d[0])}</li>" for d in decisions)
    thumb_html = "".join(f'<div class="th"><img src="{t}" alt=""></div>' for t in thumbs)
    page(f"""
  <div class="case">
    <div class="case-text">
      <div class="kicker mono"><span class="acc">{i+1:02d}</span> — {label}</div>
      <h2 class="case-h">{plain(c['headline'])}</h2>
      <p class="case-sub">{plain(c['sub'])}</p>
      <dl class="meta mono">
        <div><dt>Role</dt><dd>{c['role']}</dd></div>
        <div><dt>Timeline</dt><dd>{c['timeline']}</dd></div>
        <div class="wide"><dt>Team</dt><dd>{c['team']}</dd></div>
      </dl>
      <h4 class="mono">Challenge</h4><p>{plain(c['challenge']['lead'])}</p>
      <h4 class="mono">Key decisions</h4><ul class="dec">{dec}</ul>
      <h4 class="mono">Outcome</h4><p><b>{plain(c['outcome']['lead'])}</b> {first_sentence(c['outcome']['body'])}</p>
      <a class="more mono" href="https://www.{SITE}/work/{slug}/">Full case study → {SITE}/work/{slug}</a>
    </div>
    <div class="case-media">
      {f'<div class="main"><img src="{main}" alt="{project_title(slug)}"></div>' if main else ''}
      <div class="thumbs">{thumb_html}</div>
    </div>
  </div>
""")

# index of all projects
cells = []
for slug, title, badge, tags, note in build.PROJECTS:
    t = img(f"projects/{slug}.jpg", w=400, q=74)
    cells.append(f'<a class="ix" href="https://www.{SITE}/work/{slug}/"><div class="ixi"><img src="{t}" alt=""></div>'
                 f'<b>{title}</b><span class="mono">{badge}</span></a>')
page(f"""
  <div class="kicker mono">All work · {len(build.PROJECTS)} shipped products</div>
  <div class="index">{''.join(cells)}</div>
""", "tight")

# AI lab
lab = sorted(LAB, key=lambda e: e.get("added", ""), reverse=True)[:15]
lcells = []
for e in lab:
    t = img(f"lab/{e['slug']}.jpg", w=560, q=74)
    lcells.append(f'<a class="lb" href="{html.escape(e.get("live") or "")}"><div class="lbi"><img src="{t}" alt=""></div>'
                  f'<b>{e["title"]}</b><span class="mono">{e["kind"]}</span></a>')
page(f"""
  <div class="kicker mono">AI Lab · Built with AI, shipped anyway</div>
  <p class="lab-lead">A designer who can build changes what is worth proposing. {len(LAB)} interfaces, tools,
  games and sites taken from idea to a live URL with Claude and Claude Code — written up at {SITE}/lab.</p>
  <div class="labgrid">{''.join(lcells)}</div>
""", "tight")

# closing
page(f"""
  {hero}
  <div class="close-text">
    <div class="eyebrow mono">Everyone’s watching</div>
    <h2 class="big">They decide in a glance.<br><em>Let’s give them something worth seeing.</em></h2>
    <div class="contacts mono">
      <a href="mailto:contact@khomeriki.design">contact@khomeriki.design</a>
      <span>+995 99 460466</span>
      <a href="https://www.{SITE}">{SITE}</a>
      <a href="https://www.linkedin.com/in/nodari-khomeriki">linkedin.com/in/nodari-khomeriki</a>
      <a href="https://dribbble.com/SimpleVibes">dribbble.com/SimpleVibes</a>
    </div>
  </div>
""", "closing", n=False)

TOTAL = len(pages)
body = []
for k, (cls, inner, n) in enumerate(pages, 1):
    num = f'<div class="pnum mono">{k:02d} / {TOTAL:02d}</div><div class="pname mono">Nodari Khomeriki — Portfolio</div>' if n else ""
    body.append(f'<section class="page {cls}">{inner}{num}</section>')

FONT = os.path.join(HERE, "fonts")
css = open(os.path.join(HERE, "portfolio.css")).read().replace("FONTDIR", FONT)
doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Nodari Khomeriki — Product Design Portfolio</title>
<meta name="author" content="Nodari Khomeriki">
<style>{css}</style></head><body>{''.join(body)}</body></html>"""
with open(os.path.join(OUT, "portfolio.html"), "w") as f:
    f.write(doc)
print(f"{TOTAL} pages -> {OUT}/portfolio.html")
