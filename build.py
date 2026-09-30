#!/usr/bin/env python3
"""
NK · Glass — static site generator.

There is no framework here on purpose: the whole site is five HTML
documents that share one shell. Editing this file and re-running it is
the only way pages should be changed, so the nav, footer and meta can
never drift apart between pages.

    python3 build.py
"""
import os, json, re, shutil, struct, sys, glob
from cases import CASES
from cv import ROLES as CV_ROLES, EDUCATION, CERTS, LANGUAGES
from lab import LAB

ROOT = os.path.dirname(os.path.abspath(__file__))
V = "221"                       # cache-buster for css/js

SITE = "https://khomeriki.design"
EMAIL = "contact@khomeriki.design"
PHONE = "+995 99 460466"
PHONE_HREF = "+99599460466"

NAV = [
    ("work",       "/work/",       "Work"),
    ("lab",        "/lab/",        "AI Lab"),
    ("experience", "/experience/", "Experience"),
    ("contact",    "/contact/",    "Contact"),
]

# ---------------------------------------------------------------- projects
# (slug, title, badge, tags, note)
PROJECTS = [
 ("ioka","IOKA","Real estate","Brand &amp; Web|Data viz","Dubai property portal. Off-plan, resale and rental in one search."),
 ("seu","SEU","Education","Brand &amp; Web|SaaS","Georgian National University. Institutional site across faculties, admissions and research."),
 ("seu-student","SEU · Student","EdTech","SaaS","Student portal. Registration, credits, library and surveys behind one login."),
 ("seu-admin","SEU · Registry","EdTech","SaaS|Data viz","Staff console. One student record, thirty departments editing it."),
 ("syniotec-sam","Syniotec · SAM","SaaS","SaaS|Data viz","Platform for construction companies. Equipment and people planned as one crew."),
 ("syniotec-ram","Syniotec · RAM","SaaS","SaaS|AI","Platform for rental companies. Planning board, overuse alerts and AI-read handovers."),
 ("syniotec-sam-mobile","Syniotec · SAM Mobile","Field app","Mobile|SaaS","Software Asset Manager on site. Shifts, transport, workshop and equipment."),
 ("syniotec-ram-mobile","Syniotec · RAM Mobile","Field app","Mobile|SaaS","Rental Asset Manager on site. Fleet, contracts, tasks and handover in four tabs."),
 ("halyk-bank","Halyk Bank Georgia","Fintech","Fintech|Brand &amp; Web","Internet bank. The deposit-opening flow, rebuilt around the choice rather than the form."),
 ("halyk-onboarding","Halyk · Onboarding","Fintech","Fintech|Mobile","Mobile app registration. Three fields, two state lookups and seven ways it can end."),
 ("halyk-open-banking","Halyk · Open Banking","Fintech","Fintech|Brand &amp; Web","Consent portal for inter-bank access. Permission by scope, account and currency."),
 ("halyk-cards","Halyk · Cards","Brand","Fintech|Brand &amp; Web","Card family for Halyk Bank Georgia. Credit, debit, gold, platinum and business."),
 ("veon","VEON","Data viz","Data viz|Brand &amp; Web","Chart and table set for a seven-market telecom group. Four themes, one geometry."),
 ("deutsche-bank","Deutsche Bank","Data viz","Fintech|Data viz","One chart grammar for analysts reading forty a day."),
 ("barclays-bank","Barclays","Data viz","Fintech|Data viz","Charting tool for bank employees. Publishable output without a designer in the loop."),
 ("neuro-pilot","Neuro Pilot","Health","Mobile|Brand &amp; Web","Georgian-language mental wellbeing app. Psychoeducation, self-assessment and guided practice."),
 ("chat-bar","Chat Bar","Social","Mobile|Brand &amp; Web","Check in to a bar, see who else is there. Location-based social, without a map of people."),
 ("opla-delivery","Opla Delivery","Mobile","Mobile","Courier app. Two piles that empty, and the day&rsquo;s pay behind them."),
 ("opla-fulfilment","Opla Fulfilment","Mobile","Mobile|SaaS","In-store picking. A list that counts down and a receipt that admits shortfalls."),
 ("tichera","Tichera","Marketplace","SaaS|Brand &amp; Web","Tutoring marketplace plus both dashboards &mdash; calendar, classroom, notifications."),
 ("meetsland","Meetsland","Social","Brand &amp; Web|Mobile","Online dating platform. Profiles, matching, in-app video and the safety layer under it."),
 ("mvb-redesign","MVB Club","Web","Brand &amp; Web","London online-coaching business. One scrolling page that ends in an application."),
   ("mvb-quiz","MVB Club Quiz","Web","Brand &amp; Web","Four-question onboarding quiz for a coaching service. Campaign, not form."),
 ("marketcolor","Marketcolor","Web","Brand &amp; Web","London content agency. A thirteen-year commission log instead of a portfolio."),
 ("miniso","Miniso Georgia","Retail","E-commerce|Brand &amp; Web","1100 results a section. Curated entrances and a basket built to grow."),
 ("home-market","Home Market","Retail","E-commerce|Mobile","Android tablet grocery app. Reorder first, and a barcode scanner for the fridge."),
 ("asorti","Assorti","Retail","E-commerce","Confectionery e-commerce. Cakes, pastries and made-to-order."),
 ("villey","Villey","Product","SaaS|Brand &amp; Web","Virtual farms mapped onto real ones in Africa. The farm asks, the owner answers."),
 ("barlepie","Barlepie","Data viz","Data viz|SaaS","Chart templates you can fill, style and embed. No designer, no developer."),
 ("11-corners","11 Corners","Travel","Brand &amp; Web|E-commerce","Georgian tour marketplace. Sells a season first, a catalogue last."),
 ("tales","Tales with Tails","Editorial","Brand &amp; Web","Georgian myth archive. Found by map, by region or by word."),
 ("mult-georgia","Mult Georgia","Retail","E-commerce|Brand &amp; Web","Georgian multi-vendor marketplace. Groceries to smartphones, one shelf."),
]

SERVICES = [
 ("Product &amp; UX design","Discovery, flows, prototypes and the research to justify them. End-to-end ownership from problem to release."),
 ("Design systems","Token architecture, component libraries and the documentation that keeps a team consistent as it grows."),
 ("Fintech &amp; data visualisation","Dashboards, reporting and trading-grade density. Making high-stakes numbers readable at a glance."),
 ("AI product interfaces","Interaction patterns for models that are probabilistic — trust, transparency, correction and graceful failure."),
 ("Mobile &amp; web apps","iOS, Android and responsive web experiences built to survive real usage, not just the case study."),
 ("Brand &amp; front-end","Identity systems and hand-built front-end when the interface deserves to be executed exactly as designed."),
]

# (title, one-line summary, longer description)
# The summaries are written rather than derived: taking the first sentence
# gave "Explore — Wide and cheap.", which means nothing without the rest of
# the paragraph. Still one source of truth, so the two pages cannot drift.
STEPS = [
 ("Frame",
  "Who it is for, what they are trying to finish, and what failure costs them.",
  "Before anything is drawn: who is this for, what are they actually trying to finish, and what does failure cost them. Most of the value in a project is decided here."),
 ("Explore",
  "Wide and cheap — enough options that the choice is a decision, not the first idea.",
  "Wide and cheap. Flows, sketches, competing structures — enough options that the chosen one is a decision rather than the first idea that appeared."),
 ("Build the system",
  "Tokens, components and states, so screens become assemblies instead of drawings.",
  "Tokens, components, states. Once the vocabulary exists, screens stop being drawings and start being assemblies, and the team can move without me."),
 ("Ship",
  "In engineering's tooling, closing the gap between the file and the browser.",
  "Working with engineering in their tooling, reviewing the real build, fixing the gap between the file and the browser. Design that never ships isn't design."),
 ("Watch",
  "Session review, tickets and analytics — so the next pass is informed, not imagined.",
  "What people actually do with it. Session review, support tickets, analytics — then the next iteration is informed instead of imagined."),
]

CAPS = ["Figma","Design systems","Prototyping","User research","Usability testing","Information architecture",
        "Data visualisation","Design tokens","WCAG accessibility","HTML / CSS","JavaScript","GSAP",
        "Design ops","Workshop facilitation","Design QA","AI product patterns"]


# ---------------------------------------------------------------- gradients
# (first tag -> slab gradient). Kept inside the brand's warm/plum range:
# the reference component's neon pairs (#4dff03, #00d0ff, #ff0058) would
# have put seven unrelated hues on one page.
TAG_GRADIENT = {
    "Fintech":      ("#6e6c6a", "#2a2a2c"),
    "SaaS":         ("#7a7876", "#232325"),
    "AI":           ("#8a8785", "#2e2e30"),
    "Mobile":       ("#75736f", "#1f1f21"),
    "Data viz":     ("#66645f", "#26262a"),
    "E-commerce":   ("#807d78", "#2b2b2d"),
    "Brand &amp; Web": ("#95918c", "#333336"),
}
DEFAULT_GRADIENT = ("#7a7876", "#26262a")


def image_size(path):
    """(width, height) for a JPEG or PNG, using only the stdlib.

    build.py has no dependencies and should keep it that way, so this
    reads the dimensions out of the file header rather than pulling in
    Pillow just to decide which mockup a screen belongs in.
    """
    try:
        with open(path, "rb") as f:
            head = f.read(24)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                return struct.unpack(">II", head[16:24])
            if head[:2] != b"\xff\xd8":
                return None
            f.seek(2)
            while True:
                b = f.read(1)
                while b and b != b"\xff":
                    b = f.read(1)
                while b == b"\xff":
                    b = f.read(1)
                if not b:
                    return None
                marker = b[0]
                # SOF0..SOF15, minus the non-frame markers in that range
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    f.read(3)
                    h, w = struct.unpack(">HH", f.read(4))
                    return w, h
                seg = struct.unpack(">H", f.read(2))[0]
                f.seek(seg - 2, 1)
    except Exception:
        return None


def local_for(url):
    """The file on disk behind a /assets/... URL, version query stripped."""
    return os.path.join(ROOT, url.split("?")[0].lstrip("/"))


def flat_edge(path):
    """The colour of an image's left and right edges, if they are one flat
    colour (a presentation image on a plain ground); None otherwise."""
    try:
        from PIL import Image
        import numpy as np
        a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    except Exception:
        return None
    cols = np.concatenate([a[:, :6], a[:, -6:]], 1).reshape(-1, 3)
    if cols.std(0).max() > 6:
        return None
    r, g, b = cols.mean(0).round().astype(int)
    return f"rgb({r},{g},{b})"


def widened(slug, path):
    """Pad a presentation image out to 16:9 by repeating its edge pixels
    (softened), written once next to the source. Only for images whose side
    edges are light and calm — a photo edge repeated would streak."""
    try:
        from PIL import Image, ImageFilter
        import numpy as np
        im = Image.open(path).convert("RGB"); w, h = im.size
    except Exception:
        return None
    if w / h >= 16 / 9 - 0.02:
        return None
    a = np.asarray(im).astype(np.float32)
    edges = np.concatenate([a[:, :4], a[:, -4:]], 1)
    if edges.mean() < 150 or np.abs(np.diff(edges, axis=0)).mean() > 3:
        return None
    W = round(h * 16 / 9); pl = (W - w) // 2; pr = W - w - pl
    def ground(col):
        # a running median down the edge: keeps the ground's gradient but
        # drops anything thin that touches the edge (a laptop's base)
        k = 121; padc = np.pad(col, ((k // 2, k // 2), (0, 0)), mode="edge")
        win = np.lib.stride_tricks.sliding_window_view(padc, k, axis=0)
        return np.median(win, axis=-1)[:, None, :]
    left = np.repeat(ground(a[:, 0]), pl, 1); right = np.repeat(ground(a[:, -1]), pr, 1)
    # the image's own outer strip fades into that ground, so something the
    # original crop cut through (a laptop base running off the edge) fades
    # out instead of being carried on as a stripe
    fw = max(8, round(w * 0.02))
    t = np.linspace(0, 1, fw)[None, :, None]; t = t * t * (3 - 2 * t)
    a = a.copy()
    # only a thin thing is faded (under an eighth of the height touching
    # that edge); a device cut by the edge stays as it is
    def thin(col, g):
        return (np.abs(col - g[:, 0]).max(1) > 18).mean() < 0.125
    if thin(a[:, 0], left):
        a[:, :fw] = left[:, :1] * (1 - t) + a[:, :fw] * t
    if thin(a[:, -1], right):
        a[:, -fw:] = a[:, -fw:] * (1 - t[:, ::-1]) + right[:, :1] * t[:, ::-1]
    out = np.concatenate([left, a, right], 1).clip(0, 255).astype(np.uint8)
    o = Image.fromarray(out)
    # soften only the padding so the seam has no hard column
    blur = o.filter(ImageFilter.GaussianBlur(6))
    m = Image.new("L", o.size, 255); m.paste(0, (pl + 2, 0, pl + w - 2, h))
    o.paste(blur, (0, 0), m)
    rel = f"assets/projects/{slug}-wide.jpg"
    o.save(os.path.join(ROOT, rel), quality=90)
    return f"/{rel}?v={V}"


def device_for(url):
    """Portrait screens go in a phone, landscape ones in a laptop.

    Deciding on the file rather than on the project's tags means a case
    with both an app and a marketing site frames each screen correctly.
    """
    rel = url.split("?")[0].lstrip("/")
    size = image_size(os.path.join(ROOT, rel))
    if not size:
        return "laptop"
    w, h = size
    # 1000px and wider is a desktop capture, however tall: a long chart
    # page in a phone frame claimed it was a mobile app
    if w >= 1000:
        return "laptop"
    return "phone" if h > w * 1.15 else "laptop"


def first_sentence(text):
    """Trim a long description down to its first sentence."""
    return text.split(". ")[0].rstrip(".") + "."


def card_chips(badge, tags):
    """Tag chips for a project card.

    `tags` is the filter taxonomy; `badge` is a sector label. On 17 of 24
    projects the badge just repeats a tag ("SaaS" / "SaaS|Data viz"), but on
    the other 7 it carries something the taxonomy has no word for — EdTech,
    Social, Retail. So the badge is only rendered when it is not already
    covered, which keeps the chips informative instead of repetitive and
    needs no per-project bookkeeping.
    """
    tl = [t.strip() for t in tags.split("|") if t.strip()]
    parts = [b.strip() for b in badge.split("·") if b.strip()]
    covered = all(any(pt.lower() in t.lower() for t in tl) for pt in parts)
    out = "".join(f'<span class="wtag">{t}</span>' for t in tl)
    if not covered:
        out += f'<span class="wtag is-sector">{badge}</span>'
    return out


def gradient_for(tags):
    first = tags.split("|")[0].strip()
    return TAG_GRADIENT.get(first, DEFAULT_GRADIENT)


EYES = os.path.exists(os.path.join(ROOT, "assets", "home", "eyes", "manifest.json"))
REVEAL = os.path.exists(os.path.join(ROOT, "assets", "home", "preload-eyes.mp4"))
# the small creatures that live around the site (assets/js/peek.js)
try:
    PEEK_MAN = json.load(open(os.path.join(ROOT, "assets", "eyes", "manifest.json")))
except (OSError, ValueError):
    PEEK_MAN = {}
PEEK = bool(PEEK_MAN)


def eye(cid, cls="", reach=None):
    """One of the creatures, small, looking at the visitor. Decorative:
    hidden from assistive tech, never carries content."""
    if not PEEK:
        return ""
    g = PEEK_MAN[cid]["geom"]
    r = f' data-reach="{reach}"' if reach else ""
    return (f'<span class="eye {cls}" data-eye="{cid}"{r} '
            f'style="aspect-ratio:{g["w"]}/{g["h"]}" aria-hidden="true"></span>')


def peek_row():
    """Four of them peering over the top of the dark band below."""
    if not PEEK:
        return ""
    return (f'\n<div class="peek-row" aria-hidden="true">'
            f'{eye("d", "pk pk--1", 160)}{eye("c", "pk pk--2")}{eye("p1", "pk pk--3", 260)}{eye("b", "pk pk--4")}'
            f'</div>\n')

def preload_html():
    """The home page's first beat. A Kling loop when the file exists, the
    drawn star-dust otherwise — decided here, at build time, so the page
    never references a file that is not there."""
    if REVEAL and EYES:
        return f'''<div class="preload preload--reveal" id="preload" data-mode="reveal" aria-hidden="true">
  <video class="preload-reveal" src="/assets/home/preload-eyes.mp4?v={V}"
         muted playsinline autoplay preload="auto"></video>
  <span class="preload-skip mono">Click to skip</span>
</div>
'''
    vid = os.path.exists(os.path.join(ROOT, "assets", "home", "preload.mp4"))
    media = (f'<video class="preload-vid" src="/assets/home/preload.mp4?v={V}" '
             f'muted loop playsinline autoplay preload="auto"></video>'
             if vid else '<canvas class="preload-cv" id="preloadcv"></canvas>')
    return f'''<div class="preload" id="preload" aria-hidden="true">
  {media}
  <div class="preload-in">
    <span class="preload-mark">NK</span>
    <span class="preload-num mono"><i>0</i></span>
  </div>
  <span class="preload-bar" aria-hidden="true"><i></i></span>
</div>
'''


def hero_media():
    """Hero layers. With the Kling clip present: the video at the bottom in
    graphite (CSS grayscale), and a canvas above it that copies the same
    frame in full colour and is masked to a pool under the pointer. One
    clip, drawn twice — so the colour and the graphite can never drift
    apart the way two separately generated clips would. Without the clip,
    the drawn field stands in."""
    if EYES:
        return (f'<canvas class="s1-eyes" id="s1eyes" data-base="/assets/home/eyes/" '
                f'data-v="{V}" aria-hidden="true"></canvas>')
    vid = os.path.exists(os.path.join(ROOT, "assets", "home", "hero-space.mp4"))
    if not vid:
        return '<canvas class="s1-v" id="s1space" aria-hidden="true"></canvas>'
    # With the clip present the drawn field is left out entirely — running
    # it under a video nobody can see through would just burn a frame loop.
    return (f'<video class="s1-vid" id="s1vid" src="/assets/home/hero-space.mp4?v={V}" '
            f'poster="/assets/home/hero-space-poster.jpg?v={V}" '
            f'muted loop playsinline autoplay preload="auto" aria-hidden="true"></video>'
            f'\n  <canvas class="s1-hot" id="s1hot" aria-hidden="true"></canvas>')


def head(title, desc, path, page):
    canon = SITE + path
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>try{{if(sessionStorage.getItem('nk-seen')==='1')document.documentElement.classList.add('pre-seen')}}catch(e){{}}</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0a0a0b">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/favicon.svg?v={V}" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v={V}">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="/assets/css/glass.css?v={V}">
</head>

<body data-page="{page}">

{preload_html() if page == "home" else ""}
<div class="aurora" aria-hidden="true"><canvas id="fieldbg" class="fieldcv"></canvas><canvas id="nebula"></canvas><i class="a1"></i><i class="a2"></i><i class="a3"></i><i class="a4"></i><i class="a5"></i></div>
<div class="grain" aria-hidden="true"></div>
<div class="vignette" aria-hidden="true"></div>
<div class="marks" aria-hidden="true"><i class="tl"></i><i class="tr"></i><i class="bl"></i><i class="br"></i></div>
<div id="cur" aria-hidden="true"></div>
<div id="ring" aria-hidden="true"><b></b></div>
<div id="trans" aria-hidden="true"><span></span></div>
'''


def nav(page):
    links = ""
    for key, href, lab in NAV:
        # Contact is already the pill at the end of the bar, so listing it
        # here too gave the same destination twice, one word apart. The
        # burger menu below still carries it.
        if key == "contact":
            continue
        cur = ' aria-current="page"' if key == page else ''
        links += (f'      <a href="{href}"{cur} class="nav-hide" data-trans="{lab}">'
                  f'<span class="swap"><span>{lab}</span><span>{lab}</span></span></a>\n')
    mlinks = ""
    for key, href, lab in NAV:
        cur = ' aria-current="page"' if key == page else ''
        mlinks += f'    <a href="{href}"{cur} data-trans="{lab}">{lab}</a>\n'
    return f'''
<header class="nav">
  <div class="nav-in">
    <a class="brand" href="/" data-trans="Home">{eye("d", "eye--brand", 120) or "<em></em>"}Nodari&nbsp;<span>Khomeriki</span></a>
    <nav class="nav-links mono" aria-label="Primary">
{links}      <a href="/contact/" class="nav-cta mono nav-hide" data-mag=".25" data-trans="Contact">Let's create</a>
      <button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Open menu"><i></i><i></i></button>
    </nav>
  </div>
</header>

<div id="menu" aria-hidden="true">
  <div class="mlinks">
    <a href="/" data-trans="Home">Home</a>
{mlinks}  </div>
  <div class="mfoot mono">
    <span>{EMAIL}</span>
    <span>Tbilisi, Georgia</span>
  </div>
</div>
'''


def footer(peek=True):
    return (peek_row() if peek else "") + f'''
<footer class="foot">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <h4 class="mono">Navigate</h4>
        <ul class="mono">
          <li><a href="/">Home</a></li>
          <li><a href="/work/">Work</a></li>
          <li><a href="/lab/">AI Lab</a></li>
          <li><a href="/experience/">Experience</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4 class="mono">Enquiry</h4>
        <ul class="mono">
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="tel:{PHONE_HREF}">{PHONE}</a></li>
        </ul>
      </div>
      <div>
        <h4 class="mono">Elsewhere</h4>
        <ul class="mono">
          <li><a href="https://www.linkedin.com/in/nodari-khomeriki" target="_blank" rel="noopener">LinkedIn ↗</a></li>
          <li><a href="https://dribbble.com/SimpleVibes" target="_blank" rel="noopener">Dribbble ↗</a></li>
        </ul>
      </div>
      <div>
        <h4 class="mono">Based in</h4>
        <ul class="mono"><li>Tbilisi, Georgia</li><li>Working globally</li><li>Open to work</li></ul>
      </div>
    </div>
    <div class="fmark" aria-hidden="true">NK</div>
    <div class="fbar mono">
      <span>© 2026 Nodari Khomeriki</span>
      <span>Designed &amp; built in Tbilisi</span>
    </div>
  </div>
</footer>

<script src="/assets/js/gsap.min.js"></script>
<script src="/assets/js/ScrollTrigger.min.js"></script>
<script src="/assets/js/lenis.min.js"></script>
<script src="/assets/js/glass.js?v={V}"></script>
{'<script src="/assets/js/eyes.js?v=' + V + '" defer></script>' if EYES else ''}
<script src="/assets/js/nebula.js?v={V}" defer></script>
{'<script src="/assets/js/peek.js?v=' + V + '" defer></script>' if PEEK else ''}
</body>
</html>
'''


def cta(title="Let's build<br><em>something real.</em>"):
    return f'''
<section class="pane cta">
  <div class="wrap">
    <div class="slab mono tick" style="justify-content:center">Contact</div>
    <a class="big" href="/contact/" data-cur="write" data-trans="Contact">{title}</a>
    <div style="margin-top:44px; display:flex; gap:14px; justify-content:center; flex-wrap:wrap" data-rise=".1">
      <a class="btn mono" href="/contact/" data-mag=".25" data-trans="Contact">Start a project</a>
      <a class="btn ghost mono" href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
</section>
'''


PHEAD_EYE = {"Work": "c", "AI Lab": "b", "Experience": "p1", "Contact": "d"}


def phead(eyebrow, line1, line2, lead, crumb="Home"):
    return f'''
<section class="phead">
  {eye(PHEAD_EYE.get(eyebrow, "c"), "eye--phead", 320)}
  <div class="scrim" aria-hidden="true"></div>
  <div class="wrap">
    <div class="crumb mono"><a href="/" data-trans="Home" class="is-back">&larr;<span>{crumb}</span></a> <span>/</span> <span>{eyebrow}</span></div>
    <h1>
      <span data-chars style="display:block">{line1}</span>
      <span data-chars style="display:block" class="em">{line2}</span>
    </h1>
    <p class="lead" data-rise=".1">{lead}</p>
  </div>
</section>
'''


def cards(items, start=1, reveal=True):
    out = []
    for i, (slug, title, badge, tags, note) in enumerate(items, start=start):
        plain = re.sub("&amp;", "and", title)
        gf, gt = gradient_for(tags)
        rv = " data-glass-in" if reveal else ""
        # A project can be written up before its screens can be shown. Asking
        # for a file that is not there gives a broken-image icon; the card's
        # own gradient is a better empty state than that.
        has_shot = os.path.exists(os.path.join(ROOT, "assets", "projects", f"{slug}.jpg"))
        img = (f'<img src="/assets/projects/{slug}.jpg?v={V}" alt="{plain} — interface design"'
               f' loading="lazy" width="800" height="600">' if has_shot else '')
        out.append(f'''
        <a class="wcard glass hoverable" href="/work/{slug}/" data-cur="view" data-trans="{plain}" data-tags="{tags}" style="--gf:{gf};--gt:{gt}"{rv}>
          <i class="gslab" aria-hidden="true"></i>
          <div class="wshot"><span class="widx mono">{i:02d}</span>{img}<span class="wpeek" aria-hidden="true">{eye(("d","c","p1","b")[i % 4], "eye--card", 140)}</span></div>
          <div class="wmeta"><h3 class="h3">{title}</h3></div>
          <p class="wnote">{note}</p>
          <div class="wtags mono">{card_chips(badge, tags)}</div>
        </a>''')
    return "\n".join(out)


# ================================================================ HOME
def page_home():
    """Nine sections, in the order you specified.

    1 hero video + copy + CTA        6 what I do
    2 scroll word-colour             7 how the work happens (dark)
    3 big image, no frame            8 who I work with
    4 horizontal left-scroll         9 footer (dark)
    5 selected projects (dark)
    """
    svc_cells = "\n".join(
        f'''      <div class="scell" data-rise=".{i}">
        <span class="snum mono">{i:02d}</span>
        <h3>{t}</h3>
        <p>{first_sentence(d)}</p>
      </div>''' for i, (t, d) in enumerate(SERVICES, 1))

    step_rows = "\n".join(
        f'''      <li data-rise=".{i}"><span class="snum mono">{i:02d}</span><b>{t}</b><span class="d">{first_sentence(d)}</span></li>'''
        for i, (t, d, _full) in enumerate(STEPS, 1))

    # §4 — the strip that carries on to the left
    strip_items = ""
    for slug, title, badge, tags, note in PROJECTS[:5]:
        plain = re.sub("&amp;", "and", title)
        if os.path.exists(os.path.join(ROOT, "assets", "projects", f"{slug}.jpg")):
            strip_items += (f'<a class="hs-item" href="/work/{slug}/" data-cur="view" data-trans="{plain}">'
                            f'<img src="/assets/projects/{slug}.jpg?v={V}" alt="{plain}" loading="lazy">'
                            f'<span class="hs-cap mono">{title}</span></a>')

    # §5 — selected work, on dark
    sel = ""
    for i, (slug, title, badge, tags, note) in enumerate(PROJECTS[:6], 1):
        plain = re.sub("&amp;", "and", title)
        has = os.path.exists(os.path.join(ROOT, "assets", "projects", f"{slug}.jpg"))
        img = (f'<img src="/assets/projects/{slug}.jpg?v={V}" alt="{plain}" loading="lazy">' if has else '')
        sel += f'''
        <a class="selcard" href="/work/{slug}/" data-cur="view" data-trans="{plain}" data-rise=".{i}">
          <span class="selshot">{img}</span>
          <span class="selmeta"><span class="mono n">{i:02d}</span><span class="t">{title}</span></span>
          <span class="selnote">{note}</span>
        </a>'''

    clients = ["Deutsche Bank", "Barclays", "VEON", "Halyk Bank", "Syniotec",
               "Marketcolor", "Miniso"]
    client_cells = "\n".join(f'      <div class="ccell">{c}</div>' for c in clients)

    def wordfill(t):
        return "".join(f'<span class="w"><i>{w}</i></span> ' for w in t.split(" "))

    return head(
        "Nodari Khomeriki — Product &amp; UX Designer | Fintech, SaaS, AI",
        "Senior product and UX designer in Tbilisi, Georgia. 8+ years across fintech, SaaS, AI and mobile for Deutsche Bank, Barclays, Halyk Bank and Syniotec.",
        "/", "home") + f'''
''' + nav("home") + f'''

<main id="top"{' class="has-eyes"' if EYES else ''}>
{'<div class="dock-track" aria-hidden="true"><canvas class="dock-eye" id="dockeye"></canvas></div>' if EYES else ''}

<!-- 1 ────────────────────────────── hero: video, copy, CTA -->
<section class="s1">
  <!-- Space, drawn. The reference is a parallax starfield, which is an
       interactive thing: it answers the pointer. No video can do that, so
       generation was never the tool for it — and colour on hover is one
       variable here rather than a crossfade between two clips. -->
  {hero_media()}
  <div class="s1-in">
    <!-- The hero is the film, a label and two ways in. The headline and the
         summary that used to sit here were competing with the footage for
         the same screen; both sentences still exist in the page — one as the
         document h1 below, one in the footer — so nothing has been dropped,
         it has stopped being shouted. -->
    <h1 class="sr-only">Interfaces for money, data and machines. Eight years of product and UX design across banking, industrial SaaS and AI products — for teams in Bremen, London, Almaty and Tbilisi.</h1>
    <p class="mono eyebrow" data-rise>Product &amp; UX design — Tbilisi, working globally</p>
    <div class="s1-cta" data-rise=".1">
      <a class="btn btn--fill mono" href="/work/" data-mag=".28" data-trans="Work">See the work</a>
      <a class="btn mono" href="/contact/" data-mag=".28" data-trans="Contact">Start a project</a>
    </div>
  </div>
  <div class="s1-foot mono"><span>Est. 2018</span><span class="scrollcue">Scroll<i></i></span><span>{len(PROJECTS)} products shipped</span></div>
</section>

<!-- 2 ────────────────────────────── the words colour in on scroll -->
<section class="s2" id="about">
  <div class="s2-sticky">
    <p class="mono eyebrow">Senior product &amp; UX designer</p>
    <h2 class="s2-h" data-wordfill>{wordfill("Clarity first. Craft always. Built to scale.")}</h2>
  </div>
</section>

<!-- 3+4 ──────────────── one ribbon: the big image is its first frame -->
<section class="s34">
  <div class="hs-sticky">
    <div class="hs-track" data-hstrip>

      <figure class="hs-hero">
        <img src="/assets/home/atmos-2.webp?v={V}" loading="eager" width="1196" height="2030"
             alt="Three stacked CRT televisions, their screens reading: I work in the space between research and shipped code — flows, design systems, data visualisation, and the small decisions that make a complex product feel obvious.">
      </figure>

      <div class="hs-lead">
        <p class="mono eyebrow">What I do</p>
        <h2 class="s4-h">Banking platforms,<br>industrial SaaS,<br><em>AI tooling.</em>{eye("d", "eye--h")}</h2>
      </div>

{strip_items}
      <a class="hs-item hs-item--all" href="/work/" data-trans="Work">
        <span class="hs-allbox"><span class="hs-all">See all<br>{len(PROJECTS)} projects <i>&rarr;</i></span></span>
        <span class="hs-cap" aria-hidden="true">&nbsp;</span>
      </a>
    </div>
    <div class="hs-bar" aria-hidden="true"><i></i></div>
  </div>
</section>

<!-- 5 ────────────────────────────── six ways in, dark -->
<section class="s6 s6--dark">
  <div class="wrap">
    <p class="mono eyebrow">Services</p>
    <h2 class="s6-h">Six ways in.{eye("c", "eye--h")}</h2>
    <p class="lead s6-lead">Most engagements are one of these, or two of them stacked. The deeper version of each lives on the craft page.</p>
    <div class="scells" style="--n:{len(SERVICES)}">
{svc_cells}
    </div>
  </div>
</section>

<!-- 6 ────────────────────────────── how the work happens -->
<section class="s7 s7--light">
  <div class="wrap">
    <p class="mono eyebrow">How the work happens</p>
    <h2 class="s7-h">Five moves, every time.{eye("b", "eye--h")}</h2>
    <p class="lead s7-lead">Same shape on a six-week engagement and a two-year platform. Only the length of each move changes.</p>
    <ol class="ssteps">
{step_rows}
    </ol>
  </div>
</section>

<!-- 7 ────────────────────────────── who I work with -->
<section class="s8">
  <div class="wrap">
    <h2 class="s8-h" data-rise>Who I work with.{eye("p1", "eye--h")}</h2>
    <div class="ccells">
{client_cells}
    </div>
  </div>
</section>

<!-- 8 ────────────────────── footer, dark: they are peering over it -->
{peek_row()}
<section class="s9">
  <div class="s9-in">
    <div class="s9-top">
      <p class="mono eyebrow">Everyone's watching</p>
      <h2 class="s9-h">They decide in a glance.<br><em>Let's give them something worth seeing.</em></h2>
    </div>
    <div>
      <span class="s9-mark">NK.</span>
      <p>Interfaces for money, data and machines. Designed in Tbilisi, shipped globally.</p>
    </div>
    <div class="s9-r">
      <a class="s9-link" href="mailto:{EMAIL}">{EMAIL} <i>&#8599;</i></a>
      <a class="s9-link" href="tel:{PHONE_HREF}">{PHONE} <i>&#8599;</i></a>
      <nav class="s9-nav">
        <a href="/work/" data-trans="Work">Work</a>
        <a href="/lab/" data-trans="AI Lab">AI Lab</a>
        <a href="/experience/" data-trans="Experience">Experience</a>
        <a href="/contact/" data-trans="Contact">Contact</a>
      </nav>
    </div>
  </div>
</section>

</main>
''' + footer(peek=False)


# ================================================================ WORK
def page_work():
    tally = {}
    for _, _, _, tags, _ in PROJECTS:
        for t in tags.split("|"):
            tally[t] = tally.get(t, 0) + 1
    return head(
        "Work — Nodari Khomeriki",
        f"{len(PROJECTS)} shipped products across fintech, SaaS, AI, mobile and e-commerce. Filter by discipline.",
        "/work/", "work") + nav("work") + phead(
        "Work",
        "Products,", "not pages.",
        f"{len(PROJECTS)} shipped products across banking, industrial SaaS, AI tooling and consumer apps — for teams in Bremen, London, Almaty and Tbilisi. Filter by discipline below."
    ) + f'''
<main>
<section class="pane" style="padding-top:clamp(40px,6vh,80px)">
  <div class="wrap">
    <div class="tagbar" role="group" aria-label="Filter work by discipline" aria-controls="wgrid"></div>
    <p class="tagbar-note mono" role="status" aria-live="polite"></p>

    <div class="wgrid" id="wgrid" data-cards>
{cards(PROJECTS)}
    </div>
  </div>
</section>
''' + cta("Something similar<br><em>in mind?</em>") + '''
</main>
''' + footer()


# ================================================================ CRAFT
def page_lab():
    if not LAB:
        entries = '''    <p class="lead" data-rise>First builds are in progress. Check back shortly.</p>'''
    else:
        blocks = []
        # Newest first off the `added` date, so entries can be written into
        # lab.py in any order and the page still reads as a timeline — except
        # for anything marked pin="bottom", which is an editorial decision to
        # keep the ad-funded builds out of the way of the design work.
        ordered = sorted(
            LAB,
            key=lambda x: (1 if x.get("pin") == "bottom" else 0,
                           tuple(-int(n) for n in x.get("added", "0-0-0").split("-"))))
        for e in ordered:
            # Capped so every card keeps its chips on one line. Uneven wrapping
            # was the only thing making the rows different heights, and the
            # fifth tool listed was never the reason anybody read an entry.
            chips = "".join(f'<span class="wtag">{t}</span>' for t in e["stack"][:3])
            chips += "".join(f'<span class="wtag is-sector">{t}</span>' for t in e["ai"][:2])
            notes = "".join(f"<li>{n}</li>" for n in e["notes"])
            links = ""
            if e.get("live"):
                links += (f'<a class="btn mono" href="{e["live"]}" target="_blank" rel="noopener"'
                          f' data-mag=".26">Open it &rarr;</a>')
            if e.get("repo"):
                links += (f'<a class="btn ghost mono" href="{e["repo"]}" target="_blank" rel="noopener"'
                          f' data-mag=".26">Source</a>')
            # an entry can be written before its screenshot exists; the card's
            # own gradient is a better empty state than a broken image icon
            has_shot = os.path.exists(os.path.join(ROOT, "assets", "lab", f'{e["slug"]}.jpg'))
            # ?v= like every other asset: /assets is served immutable for a
            # year, so a replaced screenshot never reached a returning visitor
            img = (f'<img src="/assets/lab/{e["slug"]}.jpg?v={V}" alt="{e["title"]} — screenshot"'
                   f' loading="lazy" width="1200" height="600">' if has_shot else '')
            shot = f'<div class="labshot">{img}</div>' 
            # eleven entries at full height was a page nobody reaches the end
            # of. The card carries the summary; the writing is one tap away and
            # opens in place, so nothing is lost and nothing is scrolled past.
            added = e.get("added", "")
            nsum = f'{len(e["notes"])} notes' if len(e["notes"]) != 1 else "1 note"
            # A build can be worth showing before it is finished, but only if
            # the card says so — otherwise every rough edge reads as a mistake
            # rather than a work in progress.
            wip = ('<span class="labwip mono">In progress</span>'
                   if e.get("status") == "in-progress" else '')
            blocks.append(f'''
      <article class="labcard glass" data-glass-in>
        {shot}
        <div class="labbody">
          <div class="labtop">
            <h2 class="h3">{e["title"]}{wip}</h2>
          </div>
          <div class="labmeta mono">
            <span class="labyear">{e["kind"]}</span>
            <time datetime="{added}">{added}</time>
          </div>
          <p class="lablead">{e["blurb"]}</p>
          <div class="wtags mono">{chips}</div>
          <details class="labmore">
            <summary class="mono">{nsum}</summary>
            <ul class="labnotes">{notes}</ul>
          </details>
          <div class="lablinks">{links}</div>
        </div>
      </article>''')
        entries = "\n".join(blocks)

    n = len(LAB)
    count = "one build" if n == 1 else f"{n} builds"
    return head(
        "AI Lab — Nodari Khomeriki",
        "Things built with AI: interfaces, tools and experiments shipped end to end — what worked, what did not, and what it is actually made of.",
        "/lab/", "lab") + nav("lab") + phead(
        "AI Lab",
        "Built with AI.", "Shipped anyway.",
        "A designer who can build changes what is worth proposing. These are the ones that made it to a URL — with the parts that fought back written down."
    ) + f'''
<main>

<section class="pane" style="padding-top:clamp(20px,3vh,40px)">
  <div class="wrap">
    <div class="slab mono tick">{count}</div>
    <div class="labs">
{entries}
    </div>
  </div>
</section>
''' + cta("Want one<br><em>of these built?</em>") + '''
</main>
''' + footer()


# ================================================================ EXPERIENCE
def page_experience():
    rows = ""
    for i, (title, kind, co, place, dates, span, bullets) in enumerate(CV_ROLES):
        det = ""
        toggle = ""
        if bullets:
            det = ('<div class="xdetail"><ul>'
                   + "".join(f"<li>{b}</li>" for b in bullets) + "</ul></div>")
            toggle = '<span class="xtoggle" aria-hidden="true">+</span>'
        cls = "xrow has-detail" if bullets else "xrow"
        rows += f'''
      <div class="{cls}"{' data-expand' if bullets else ''}>
        <div class="xhead">
          <div>
            <div class="xrole">{title}<span class="chip mono">{kind}</span></div>
            <div class="xco mono">{co}</div>
            <div class="xmeta mono"><span>{place}</span><span>·</span><span>{span}</span></div>
          </div>
          <div class="xdate mono">{dates}{toggle}</div>
        </div>
        {det}
      </div>'''

    edu = "".join(
        f'<div class="glass" data-glass-in><div><h3>{school}</h3><div class="d">{deg}</div></div>'
        f'<div class="y mono">{yrs}</div></div>'
        for school, deg, yrs in EDUCATION)

    groups = []
    for _, _, _, g in CERTS:
        if g not in groups:
            groups.append(g)
    bar = f'<button type="button" data-cgroup="All" aria-pressed="true">All <i>{len(CERTS)}</i></button>'
    for g in groups:
        n = sum(1 for c in CERTS if c[3] == g)
        bar += f'<button type="button" data-cgroup="{g}" aria-pressed="false">{g} <i>{n}</i></button>'

    certs = "".join(
        f'<div class="cert glass hoverable" data-cgroup="{g}"><h4>{name}</h4>'
        f'<div class="by mono">{issuer}</div><div class="on mono">{date}</div></div>'
        for name, issuer, date, g in CERTS)

    words = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    n_lang = words.get(len(LANGUAGES), str(len(LANGUAGES)))

    langs = "".join(
        f'<div class="lang glass" data-glass-in><h3>{l}</h3><div class="lvl">{lvl}</div>'
        f'<div class="bar"><i data-fill="{pct}"></i></div></div>'
        for l, lvl, pct in LANGUAGES)

    return head(
        "Experience — Nodari Khomeriki",
        f"Eight years of design work across syniotec, Halyk Bank Georgia, Marketcolor London and LTD YIC Amsterdam, plus {len(CERTS)} certifications.",
        "/experience/", "experience") + nav("experience") + phead(
        "Experience",
        "Eight years", "of craft.",
        "From a finance degree and an accounting qualification to leading design on banking platforms and industrial SaaS used across three continents."
    ) + f'''
<main>

<section class="pane" style="padding-top:clamp(40px,6vh,80px)">
  <div class="wrap">
    <div class="stats" style="margin-top:0">
      <div class="stat glass" data-glass-in><div class="n"><span data-count="8" data-suffix="+">0</span></div><div class="k mono">Years in design</div></div>
      <div class="stat glass" data-glass-in><div class="n"><span data-count="{len(PROJECTS)}" data-suffix="+">0</span></div><div class="k mono">Products shipped</div></div>
      <div class="stat glass" data-glass-in><div class="n"><span data-count="{len(CERTS)}">0</span></div><div class="k mono">Certifications</div></div>
      <div class="stat glass" data-glass-in><div class="n"><span data-count="{len(LANGUAGES)}">0</span></div><div class="k mono">Languages</div></div>
    </div>

    <div class="slab mono tick" style="margin-top:clamp(56px,9vh,110px)">Roles</div>
    <p class="lead" data-rise style="margin-bottom:clamp(24px,4vh,44px)">Open a role to see what the work actually involved.</p>
    <div class="xp">
{rows}
    </div>
  </div>
</section>

<section class="pane pane--lift">
  <div class="wrap">
    <div class="slab mono tick">Education</div>
    <h2 class="h2" data-chars>Finance first, design second.</h2>
    <p class="lead" style="margin-top:20px" data-rise>A background in banking and accounting is an unusual route into product design — and the reason fintech interfaces feel like familiar territory rather than a new domain.</p>
    <div class="edu">{edu}</div>
  </div>
</section>

<section class="pane">
  <div class="wrap">
    <div class="slab mono tick">Licenses &amp; certifications</div>
    <h2 class="h2" data-chars>{len(CERTS)} certifications, and counting.</h2>
    <p class="lead" style="margin-top:20px" data-rise>Interaction Design Foundation for the fundamentals, Anthropic and Google for the AI work, ACCA from an earlier life in finance.</p>
    <div class="certbar" role="group" aria-label="Filter certifications by issuer">{bar}</div>
    <p class="tagbar-note mono" role="status" aria-live="polite"></p>
    <div class="certs">{certs}</div>
  </div>
</section>

<section class="pane pane--lift">
  <div class="wrap">
    <div class="slab mono tick">Languages</div>
    <h2 class="h2" data-chars>Working across {n_lang}.</h2>
    <div class="langs">{langs}</div>
  </div>
</section>

<section class="pane">
  <div class="wrap">
    <div class="slab mono tick">Sectors</div>
    <div class="grid">
      <div class="c5"><h2 class="h2" data-chars>Where the work has lived.</h2></div>
      <div class="c7">
        <div data-lines>
          <p class="lead">Regulated banking — where a misread number has a cost. Industrial SaaS — where the user is on a construction site, not at a desk. AI products — where the interface has to make an uncertain answer honest.</p>
          <p class="lead" style="margin-top:18px">The common thread is density: a lot of information, a user under time pressure, and no room for a decorative interface.</p>
        </div>
        <div style="margin-top:40px" data-rise=".1">
          <a class="btn mono" href="/work/" data-mag=".25" data-trans="Work">See the work</a>
        </div>
      </div>
    </div>
  </div>
</section>
''' + cta("Let's talk about<br><em>your team.</em>") + '''
</main>
''' + footer()


# ================================================================ CONTACT
def page_contact():
    return head(
        "Contact — Nodari Khomeriki",
        f"Get in touch about product design, design systems or fintech work. {EMAIL} · Tbilisi, Georgia.",
        "/contact/", "contact") + nav("contact") + phead(
        "Contact",
        "Let's build", "something real.",
        "Available for projects from Q3 2026. Tell me what you're building and what's currently in the way — I usually reply within a day."
    ) + f'''
<main>

<section class="pane" style="padding-top:clamp(40px,6vh,80px)">
  <div class="wrap">
    <div class="ccards">
      <a class="ccard glass hoverable" href="mailto:{EMAIL}" data-glass-in>
        <h4 class="mono">Email</h4>
        <div class="v">{EMAIL}</div>
        <div class="m mono">Best for project enquiries</div>
      </a>
      <a class="ccard glass hoverable" href="tel:{PHONE_HREF}" data-glass-in>
        <h4 class="mono">Phone</h4>
        <div class="v">{PHONE}</div>
        <div class="m mono">Tbilisi · GMT+4</div>
      </a>
      <a class="ccard glass hoverable" href="https://www.linkedin.com/in/nodari-khomeriki" target="_blank" rel="noopener" data-glass-in>
        <h4 class="mono">LinkedIn</h4>
        <div class="v">nodari-khomeriki ↗</div>
        <div class="m mono">Roles and referrals</div>
      </a>
      <a class="ccard glass hoverable" href="https://dribbble.com/SimpleVibes" target="_blank" rel="noopener" data-glass-in>
        <h4 class="mono">Dribbble</h4>
        <div class="v">SimpleVibes ↗</div>
        <div class="m mono">Explorations and shots</div>
      </a>
    </div>
  </div>
</section>

<section class="pane pane--lift">
  <div class="wrap">
    <div class="slab mono tick">Enquiry</div>
    <div class="grid">
      <div class="c5">
        <h2 class="h2" data-chars>Start here.</h2>
        <p class="lead" style="margin-top:22px" data-rise>The more you can say about the problem, the more useful my first reply will be.</p>
      </div>
      <div class="c7">
        <form class="form" id="enquiry" novalidate>
          <div class="field">
            <label for="f-name" class="mono">Your name *</label>
            <input id="f-name" name="name" type="text" autocomplete="name" placeholder="Jane Doe" required>
            <div class="err mono" data-err="name" aria-live="polite"></div>
          </div>
          <div class="field">
            <label for="f-email" class="mono">Email *</label>
            <input id="f-email" name="email" type="email" autocomplete="email" placeholder="jane@company.com" required>
            <div class="err mono" data-err="email" aria-live="polite"></div>
          </div>
          <div class="field">
            <label for="f-company" class="mono">Company</label>
            <input id="f-company" name="company" type="text" autocomplete="organization" placeholder="Optional">
          </div>
          <div class="field">
            <label for="f-budget" class="mono">Rough budget</label>
            <select id="f-budget" name="budget">
              <option value="">Prefer not to say</option>
              <option>Under €10k</option>
              <option>€10k — €30k</option>
              <option>€30k — €75k</option>
              <option>€75k+</option>
              <option>Full-time role</option>
            </select>
          </div>
          <div class="field">
            <label for="f-message" class="mono">What are you building? *</label>
            <textarea id="f-message" name="message" placeholder="The product, the stage it's at, and what's currently in the way." required></textarea>
            <div class="err mono" data-err="message" aria-live="polite"></div>
          </div>
          <div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap">
            <button class="btn mono" type="submit" data-mag=".2">Send enquiry</button>
            <span class="form-note mono">Opens your mail app with everything filled in.</span>
          </div>
        </form>
      </div>
    </div>
  </div>
</section>

</main>
''' + footer()


# ================================================================ 404
def page_404():
    return head("Page not found — Nodari Khomeriki",
                "That page doesn't exist. Head back to the portfolio.",
                "/404.html", "notfound") + nav("") + '''
<main class="nf">
  <div class="scrim" style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,8,9,.80),var(--ink))" aria-hidden="true"></div>
  <div class="inner glass">
    <div class="big" aria-label="404">4''' + (eye("d", "eye--o", 200) or "0") + '''4</div>
    <h1 class="h3" style="margin-top:16px">This page doesn't exist.</h1>
    <p class="lead" style="margin:16px auto 0">It may have moved, or the link may be wrong.</p>
    <div style="margin-top:36px;display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <a class="btn mono" href="/" data-mag=".25" data-trans="Home">Back home</a>
      <a class="btn ghost mono" href="/work/" data-trans="Work">See the work</a>
    </div>
  </div>
</main>
''' + footer()



# ================================================================ CASE STUDY
def shots_for(slug):
    """Screens you drop into assets/projects/<slug>/ fill the image slots."""
    d = os.path.join(ROOT, "assets", "projects", slug)
    if not os.path.isdir(d):
        return []
    return [f"/assets/projects/{slug}/{f}?v={V}"
            for f in sorted(os.listdir(d))
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]


def paras(items, cls="cbody"):
    return f'<div class="{cls}">' + "".join(f"<p>{p}</p>" for p in items) + "</div>"


def shot(url, alt, i, host=None, plain=False):
    """A screen, framed as the device it was designed for.

    Portrait screens get a phone, landscape ones a browser window. Both
    frames also cap the image near its native width: a screenshot can only
    be as sharp as the display it was captured on, and stretched across a
    1440px column it reads as a bad image rather than a small one.
    """
    if not url:
        # A grey "Screen 01" box is worse than no box: it reads as a broken
        # page rather than as a case study that leads with its writing.
        return ""

    if plain:
        # Not every project is screens. Product photography and print renders
        # already have their own composition, and a browser chrome around a
        # bank card claims it is a website.
        return (f'<figure class="shot is-plain" data-glass-in>'
                f'<img src="{url}" alt="{alt}" loading="lazy"></figure>')

    # A full-page capture is still a screenshot and belongs in the same window
    # as every other one. It is simply cropped to the window rather than given
    # its own scrolling container: a scroll region nested inside a page traps
    # the wheel and breaks the one reading rhythm the case study has.
    # 1000px is the line between a phone screen exported at 2x — which is
    # still a phone and belongs in one — and a desktop page captured whole.
    dim = image_size(local_for(url))
    if dim and dim[0] >= 1000 and dim[1] > dim[0] * 1.15:
        bar = ('<span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>'
               + (f'<span class="url mono">{host}</span>' if host else ''))
        return (f'<figure class="shot is-browser is-page" data-glass-in>'
                f'<span class="chrome" aria-hidden="true">{bar}</span>'
                f'<img src="{url}" alt="{alt}" loading="lazy"></figure>')

    if device_for(url) == "phone":
        return (f'<figure class="shot is-phone" data-glass-in>'
                f'<span class="phone">'
                f'<span class="notch" aria-hidden="true"></span>'
                f'<img src="{url}" alt="{alt}" loading="lazy">'
                f'</span></figure>')

    bar = ('<span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>'
           + (f'<span class="url mono">{host}</span>' if host else ''))
    return (f'<figure class="shot is-browser" data-glass-in>'
            f'<span class="chrome" aria-hidden="true">{bar}</span>'
            f'<img src="{url}" alt="{alt}" loading="lazy"></figure>')


def page_case(idx):
    slug, title, badge, tags, note = PROJECTS[idx]
    c = CASES.get(slug)
    if not c:
        return None
    plain = re.sub("&amp;", "and", title)
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    prv = PROJECTS[(idx - 1) % len(PROJECTS)]
    pics = shots_for(slug)
    pic = iter(pics)

    # a shipped project people can go and use is worth more than any
    # amount of case-study prose, so surface it right under the meta
    livebtn = ""
    # host only — the label is a brand, not a path. seu.edu.ge/ka read as
    # a broken URL; the link itself still goes to the full address.
    host = re.sub(r"^https?://(www\.)?", "", c["live"]).split("/")[0] if c.get("live") else None
    if c.get("live"):
        livebtn = (f'<div class="caselive" data-rise=".1">'
                   f'<a class="btn mono" href="{c["live"]}" target="_blank" rel="noopener"'
                   f' data-mag=".26">Visit {host} &rarr;</a></div>')

    def nextpic():
        return next(pic, None)

    # `shots="plain"` marks a case whose images are objects rather than
    # interfaces — cards, print, packaging. They are shown as they are.
    plain_shots = c.get("shots") == "plain"

    def framed(u, alt, i):
        return shot(u, alt, i, host, plain_shots)

    # A device makes the cover honest about scale: the screenshot renders
    # near its native width inside the lid instead of being stretched over
    # the full column, and the brand photograph sits behind it.
    cover_src = os.path.join(ROOT, "assets", "projects", f"{slug}.jpg")
    cover_dim = image_size(cover_src)
    cover_ok = bool(cover_dim) and cover_dim[0] >= 800
    cover_url = f"/assets/projects/{slug}.jpg?v={V}"

    def device(src, alt):
        """The house pattern for a cover: the project's own image thrown out
        of focus behind, and the interface sitting on it inside a device.
        The frame is picked from the file's shape — portrait is a phone,
        anything wider is a laptop — and it doubles as the sharpness fix,
        since the screen area lands near the image's native width instead
        of being stretched across the whole column."""
        if device_for(src) == "phone":
            inner = (f'<span class="phone"><span class="notch" aria-hidden="true"></span>'
                     f'<img src="{src}" alt="{alt}"></span>')
            kind = "phone"
        else:
            inner = (f'<span class="laptop"><span class="lid">'
                     f'<img src="{src}" alt="{alt}"></span>'
                     f'<span class="base"><i></i></span></span>')
            kind = "laptop"
        return (f'<figure class="cover is-device is-{kind}" data-glass-in>'
                f'<img class="cover-bg" src="{cover_url}" alt="" aria-hidden="true">'
                f'{inner}</figure>')

    if c.get("cover") == "card" and cover_ok:
        # the card image is already a composed presentation of the product;
        # a device over a blurred copy of it showed the same screens twice
        wide = widened(slug, cover_src)
        cover = (f'<figure class="cover is-fit is-flat" data-glass-in>'
                 f'<img class="cover-fg" src="{wide}" alt="{plain} — {badge}">'
                 f'</figure>') if wide else (
                 f'<figure class="cover is-fit" data-glass-in>'
                 f'<img class="cover-bg" src="{cover_url}" alt="" aria-hidden="true">'
                 f'<img class="cover-fg" src="{cover_url}" alt="{plain} — {badge}">'
                 f'</figure>')
    elif pics and plain_shots:
        # The object is the image. Show it whole on a wash of itself.
        cover = (f'<figure class="cover is-fit" data-glass-in>'
                 f'<img class="cover-bg" src="{pics[0]}" alt="" aria-hidden="true">'
                 f'<img class="cover-fg" src="{pics[0]}" alt="{plain} — {badge}">'
                 f'</figure>')
        if len(pics) > 1:
            next(pic, None)
    elif pics:
        # Gallery files are raw captures — a bare screen with nothing around
        # it — so they need a device to sit in.
        cover = device(pics[0], f"{plain} — {badge}")
        # the cover has shown this screen; the first decision starting on the
        # same picture a scroll later read as a duplicate
        if len(pics) > 1:
            next(pic, None)
    elif cover_ok:
        # Card thumbnails are presentation images that already have a laptop
        # or phone composed into them. Wrapping one in another frame put the
        # screen inside three nested bezels, so these are shown whole. When the
        # image's own edges are flat, the frame takes that colour and the image
        # simply continues into it; otherwise a blurred copy fills the frame.
        edge = flat_edge(cover_src)
        wide = widened(slug, cover_src) if not edge else None
        if wide:
            # the image carried out to 16:9 by continuing its own edge
            # pixels, so its ground and shadows run on to the frame's edge
            cover = (f'<figure class="cover is-fit is-flat" data-glass-in>'
                     f'<img class="cover-fg" src="{wide}" alt="{plain} — {badge}">'
                     f'</figure>')
        elif edge:
            cover = (f'<figure class="cover is-fit is-flat" data-glass-in style="background:{edge}">'
                     f'<img class="cover-fg" src="{cover_url}" alt="{plain} — {badge}">'
                     f'</figure>')
        else:
            cover = (f'<figure class="cover is-fit" data-glass-in>'
                     f'<img class="cover-bg" src="{cover_url}" alt="" aria-hidden="true">'
                     f'<img class="cover-fg" src="{cover_url}" alt="{plain} — {badge}">'
                     f'</figure>')
    else:
        # Under 800px there is nothing a device can rescue: a 220px file in a
        # laptop lid is still a 220px file. The thumbnail becomes an
        # out-of-focus wash and the project's name carries the space instead.
        # No thumbnail at all is a legitimate state — a project can be written
        # up before its screens can be shown. The gradient carries it alone
        # rather than requesting a file that is not there.
        gf, gt = gradient_for(tags)
        wash = (f'<img class="cover-bg" src="{cover_url}" alt="" aria-hidden="true">'
                if cover_dim else '')
        cover = (f'<figure class="cover is-plate" data-glass-in style="--gf:{gf};--gt:{gt}">'
                 f'{wash}'
                 f'<figcaption class="plate">'
                 f'<span class="mono">{badge}</span>'
                 f'<span class="pt">{title}</span>'
                 f'</figcaption></figure>')

    # ---- section nav ------------------------------------------------------
    secs = [("overview", "Case study"), ("challenge", "The challenge")]
    if c.get("discovery"): secs.append(("discovery", "Discovery &amp; research"))
    secs.append(("solution", "The solution"))
    secs.append(("outcome", "Outcome"))
    # The sticky bar was the only thing on screen for most of a long case
    # study and it had no way out of it — leaving meant scrolling to the top
    # crumb or all the way to the pager. It now starts with the way back.
    casenav = ('<a href="/work/" class="mono is-back" data-trans="Work"'
               ' aria-label="Back to all work">&larr;<span>Work</span></a>')
    casenav += "".join(f'<a href="#{i}" class="mono">{l}</a>' for i, l in secs)

    # ---- challenge --------------------------------------------------------
    ch = c["challenge"]
    callout = ""
    if ch.get("callout"):
        lab, t, txt = ch["callout"]
        callout = (f'<div class="callout glass" data-glass-in>'
                   f'<span class="pill mono">{lab}</span><h3>{t}</h3><p>{txt}</p></div>')
    challenge = f'''
<section class="csec" id="challenge">
  <div class="wrap">
    <div class="csec-label mono tick">The challenge</div>
    <h2 data-chars>{ch["lead"]}</h2>
    <div class="ctwo">
      <div class="body">{paras(ch["body"])}</div>
      <div class="side">{callout}</div>
    </div>
  </div>
</section>'''

    # ---- discovery --------------------------------------------------------
    discovery = ""
    d = c.get("discovery")
    if d:
        obs = "".join(f'<div class="glass" data-glass-in><h4>{t}</h4><p>{x}</p></div>'
                      for t, x in d.get("obs", []))
        finds = "".join(
            f'<div class="find"><div class="k mono">{k}</div>'
            f'<div class="t">{t}</div><div class="d">{x}</div></div>'
            for k, t, x in d.get("findings", []))
        discovery = f'''
<section class="csec" id="discovery">
  <div class="wrap">
    <div class="csec-label mono tick">Discovery &amp; research</div>
    <h2 data-chars>{d["lead"]}</h2>
    <div class="ctwo"><div class="body">{paras(d["body"])}</div></div>
    <div class="obs">{obs}</div>
    <div class="finds">{finds}</div>
  </div>
</section>'''

    # ---- insight ----------------------------------------------------------
    insight = ""
    ins = c.get("insight")
    if ins:
        insight = f'''
<section class="csec" style="padding-block:0">
  <div class="wrap">
    <div class="insight glass" data-glass-in>
      <div class="csec-label mono tick">Key insight</div>
      <blockquote>{ins["quote"]}</blockquote>
      <div class="after">{"".join(f"<p>{p}</p>" for p in ins["body"])}</div>
    </div>
  </div>
</section>'''

    # ---- solution ---------------------------------------------------------
    sol = c["solution"]
    decs = ""
    for i, (t, sub, body) in enumerate(sol["decisions"], 1):
        decs += (f'<div class="decision" data-rise>'
                 f'<span class="pill mono">Design decision</span>'
                 f'<h3>{t}</h3><p class="sub">{sub}</p>{paras(body)}'
                 f'{framed(nextpic(), plain + " — " + re.sub("&amp;", "and", t), i)}</div>')
    solution = f'''
<section class="csec" id="solution">
  <div class="wrap">
    <div class="csec-label mono tick">The solution</div>
    <h2 data-chars>{sol["lead"]}</h2>
    <div class="ctwo"><div class="body">{paras(sol["body"])}</div></div>
    {decs}
  </div>
</section>'''

    # ---- outcome + reflection --------------------------------------------
    out = c["outcome"]
    refl = ""
    r = c.get("reflection")
    if r:
        refl = (f'<div class="callout glass" data-glass-in style="margin-top:clamp(32px,5vh,60px)">'
                f'<span class="pill mono">Reflection</span><h3>{r["title"]}</h3>'
                + "".join(f"<p>{p}</p>" for p in r["body"]) + '</div>')
    outcome = f'''
<section class="csec" id="outcome">
  <div class="wrap">
    <div class="csec-label mono tick">Outcome</div>
    <h2 data-chars>{out["lead"]}</h2>
    <div class="ctwo"><div class="body">{paras(out["body"])}</div></div>
    {refl}
  </div>
</section>'''

    # ---- any remaining screens become a closing gallery -------------------
    rest = list(pic)
    gallery = ""
    if rest:
        # every leftover screen keeps its own frame, whole: phones in a row
        # of phones, desktop captures in windows two to a row. Cropping them
        # all to the same 4:3 tile cut phones in half and charts off mid-axis.
        if plain_shots:
            cells = "".join(
                f'<figure data-glass-in><img src="{u}" alt="{plain} screen" loading="lazy"></figure>'
                for u in rest)
            grid = f'<div class="gal">{cells}</div>'
        else:
            phones = [u for u in rest if device_for(u) == "phone"]
            wide = [u for u in rest if u not in phones]
            grid = ""
            if phones:
                grid += '<div class="galp">' + "".join(
                    framed(u, f"{plain} screen", 99) for u in phones) + '</div>'
            if len(wide) == 1:
                grid += framed(wide[0], f"{plain} screen", 99)
            elif wide:
                grid += '<div class="galb">' + "".join(
                    framed(u, f"{plain} screen", 99) for u in wide) + '</div>'
        gallery = f'''
<section class="csec" style="padding-top:0">
  <div class="wrap"><div class="csec-label mono tick">More screens</div>
  {grid}</div>
</section>'''

    meta = "".join(f'<div><dt class="mono">{k}</dt><dd>{v}</dd></div>' for k, v in
                   [("Role", c["role"]), ("Timeline", c["timeline"]), ("Team", c["team"])])

    return head(
        f"{plain} — case study | Nodari Khomeriki",
        re.sub("<[^>]+>|&amp;", " ", c["sub"])[:158].strip(),
        f"/work/{slug}/", "work") + nav("work") + f'''
<main>

<section class="case-hero" id="overview">
  <canvas class="fieldcv" aria-hidden="true"></canvas>
  <div class="scrim" aria-hidden="true"></div>
  <div class="wrap">
    <div class="crumb mono">
      <a href="/" data-trans="Home">Home</a> <span>/</span>
      <a href="/work/" data-trans="Work" class="is-back">&larr;<span>Work</span></a> <span>/</span>
      <span>{plain}</span>
    </div>
    <h1><span data-chars style="display:block">{c["headline"]}</span></h1>
    <p class="lead case-sum" data-rise=".08">{c["sub"]}</p>
    {cover}
    <dl class="meta">{meta}</dl>
    {livebtn}
  </div>
</section>

<nav class="casenav" aria-label="Case study sections">{casenav}</nav>
{challenge}
{discovery}
{insight}
{solution}
{outcome}
{gallery}

<nav class="pager" aria-label="Project navigation">
  <a class="glass hoverable prev" href="/work/{prv[0]}/" data-trans="{re.sub("&amp;", "and", prv[1])}">
    <span class="k mono">← Previous</span><span class="t">{prv[1]}</span>
  </a>
  <a class="pager-up mono" href="/work/" data-trans="Work">All {len(PROJECTS)} projects</a>
  <a class="glass hoverable next" href="/work/{nxt[0]}/" data-trans="{re.sub("&amp;", "and", nxt[1])}">
    <span class="k mono">Next →</span><span class="t">{nxt[1]}</span>
  </a>
</nav>

</main>
''' + footer()

# ---------------------------------------------------------------- write
PAGES = {
    "index.html":            page_home,
    "work/index.html":       page_work,
    "lab/index.html":        page_lab,
    "experience/index.html": page_experience,
    "contact/index.html":    page_contact,
    "404.html":              page_404,
}

def main():
    for i, (slug, *_rest) in enumerate(PROJECTS):
        if slug in CASES:
            PAGES[f"work/{slug}/index.html"] = (lambda i=i: page_case(i))

    for path, fn in PAGES.items():
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        html = fn()
        with open(full, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  {path:26} {len(html):>7,} bytes")
    print(f"\n{len(PAGES)} pages · {len(PROJECTS)} projects · {len(CASES)} case studies · assets v{V}")

if __name__ == "__main__":
    main()
