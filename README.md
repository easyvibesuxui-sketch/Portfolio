# khomeriki.design

Portfolio of Nodari Khomeriki — product & UX designer.

Static site. `build.py` generates every page (`index.html`, `work/`, `lab/`,
`experience/`, `contact/`, `404.html`) from the data in `build.py`, `cases.py`,
`lab.py` and `cv.py`. The generated HTML is committed, so the repo is the site.

```
python3 build.py        # regenerate all pages (bump V in build.py to bust caches)
```

Deployed on Vercel (`vercel.json`: clean URLs, immutable asset caching,
redirects). `tools/` holds the image pipelines (hero creatures, preloader grading,
card composites); they are not deployed.
