#!/usr/bin/env python3
"""Builds davidcreason.com into plain static HTML.

The resume PDF (assets/David_Creason_Resume.pdf) is the source of truth: your name,
headline, summary, current role, education, and the whole /resume/ page are read
from it on every build, and any phone number is removed from both the pages and
the PDF. To update, replace the PDF and run the build.

Projects and links are edited in the PROJECTS / PROFILE data below. Then run:

    python3 build.py

and commit the generated .html files. GitHub Pages serves them as-is.
"""
import html
import os
import re

from resume_source import PHONE, load_resume, redact_phone_numbers

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.davidcreason.com"
RESUME_PDF = os.path.join(ROOT, "assets", "David_Creason_Resume.pdf")

# ---- Source of truth: the resume PDF --------------------------------------
_removed = redact_phone_numbers(RESUME_PDF)
if _removed:
    print(f"Removed {_removed} phone number(s) from the resume PDF.")
RESUME = load_resume(RESUME_PDF)
_current = RESUME["experience"][0] if RESUME["experience"] else None
_first_sentence = re.split(r"(?<=[.!?])\s", RESUME["summary"], maxsplit=1)[0]

PROFILE = {
    "name": RESUME["name"],
    "role": RESUME["headline"],
    "tagline": _first_sentence,
    "current": f"{_current['title']} at {_current['org']}" if _current else "",
    "linkedin": "https://www.linkedin.com/in/dcreason/",
    "github": "https://github.com/project-creason",
    "resume": "/assets/David_Creason_Resume.pdf",
}

# status: "active" or "past". Order here is display order within each group.
PROJECTS = [
    {
        "slug": "chimney-planner",
        "title": "DuraTech Chimney Planner",
        "status": "active",
        "badge": "Live · in development",
        "year": "2026",
        "summary": "Enter your home's measurements and get a complete DuraVent DuraTech chimney parts list that follows the manufacturer's installation rules and NFPA 211.",
        "tags": ["JavaScript", "Rules engine", "CSV → JSON catalog", "GitHub Pages"],
        "image": "/assets/projects/chimney-planner.jpg",
        "image_alt": "Screenshot of the DuraTech Chimney Planner form and generated parts list",
        "links": [
            ("Launch the planner", "https://project-creason.github.io/chimney_planner/", True),
            ("Source on GitHub", "https://github.com/project-creason/chimney_planner", False),
        ],
    },
    {
        "slug": "resume-assistant",
        "title": "AI Resume Assistant",
        "status": "active",
        "badge": "Live",
        "year": "2025",
        "summary": "A chat assistant grounded in my work history that answers recruiters' questions about my experience, skills, and education, with streamed responses from a serverless API.",
        "tags": ["LLM", "Vercel serverless", "Streaming", "Vanilla JS"],
        "image": "/assets/projects/resume-assistant.jpg",
        "image_alt": "The AI resume assistant chat window",
        "links": [("Try it", "/#ask", True)],
    },
    {
        "slug": "louisville-crime",
        "title": "Louisville Crime, 2024",
        "status": "past",
        "badge": "Completed",
        "year": "2025",
        "summary": "Analysis of a year of reported crime in Louisville, KY: weather, moon phase, geography, holidays, and timing. Hot days drive crime up; full moons don't.",
        "tags": ["Tableau", "Public data", "Correlation analysis"],
        "image": "https://public.tableau.com/static/images/Lo/Louisville_KY_Crime_Stats/LouisvilleCrime/1.png",
        "image_alt": "Louisville crime Tableau dashboard preview",
        "links": [("View dashboard", "/projects/louisville-crime/", True)],
    },
    {
        "slug": "crestwood-home-hearth",
        "title": "Crestwood Home & Hearth",
        "status": "past",
        "badge": "Completed",
        "year": "2025",
        "summary": "Mapped the zip codes and counties where a local hearth business sold and installed, to show where its customers really come from.",
        "tags": ["Tableau", "Geographic analysis", "Small business"],
        "image": "https://public.tableau.com/static/images/Cr/CrestwoodHomeHearth/CHHStory/1.png",
        "image_alt": "Crestwood Home and Hearth customer map preview",
        "links": [("View story", "/projects/crestwood-home-hearth/", True)],
    },
]

EDUCATION = [f"{deg}, {school}" if school else deg for deg, school in RESUME["education"]]

# ---- Key numbers band: pulled from the resume text so it stays in sync ----
# Each stat is a regex run against the resume. If a future resume drops the phrase,
# that stat simply disappears (and the build says so) instead of showing a stale number.
_resume_text = " ".join(
    [RESUME["summary"]]
    + [b for j in RESUME["experience"] for b in j["bullets"]]
    + [b for o in RESUME["other"] for en in o["entries"] for b in en["bullets"]]
)
STAT_RULES = [
    (r"over (\d+)\+? years", "{0}+", "years leading teams, platforms & M&A integrations"),
    (r"([\d,]+)\+ active property entities", "{0}+", "property entities governed in Yardi ERP"),
    (r"cycle times by over (\d+)%", "{0}%+", "less property setup time in M&A onboarding"),
    (r"(\d+)% audit compliance", "{0}%", "audit compliance after new SOX release controls"),
    (r"revenue past \$(\d+M)", "${0}+", "division revenue in year one post-merger"),
    (r"~(\d+)% growth", "~{0}%", "revenue growth at the business I founded"),
]
STATS = []
for _rx, _fmt, _label in STAT_RULES:
    _m = re.search(_rx, _resume_text, re.I)
    if _m:
        STATS.append((_fmt.format(*_m.groups()), _label))
    else:
        print(f"Note: stat not found in resume, skipped: {_label}")

_DEGREE = re.compile(r"\b(master|bachelor|associate|doctor|mba|m\.?s\.?|b\.?s\.?|ph\.?d)\b", re.I)
CERTS = [(deg, school) for deg, school in RESUME["education"] if not _DEGREE.search(deg)]

# Facts from the resume used in project copy
_chh = next((j for j in RESUME["experience"] if "Crestwood Home" in j["org"]), None)
if _chh:
    for _p in PROJECTS:
        if _p["slug"] == "crestwood-home-hearth":
            _yrs = re.findall(r"\d{4}", _chh["dates"])
            _span = f" from {_yrs[0]} to {_yrs[-1]}" if len(_yrs) >= 2 else ""
            _p["summary"] = (f"Mapped the zip codes and counties served by Crestwood Home & Hearth, the field service "
                             f"business I founded and ran{_span}.")

# --------------------------------------------------------------------------- helpers
e = html.escape
LI_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>'
GH_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .5A11.5 11.5 0 0 0 .5 12a11.5 11.5 0 0 0 7.86 10.92c.58.1.79-.25.79-.56v-2c-3.2.7-3.87-1.37-3.87-1.37-.53-1.33-1.28-1.69-1.28-1.69-1.05-.71.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.09-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.8 1.19 1.83 1.19 3.09 0 4.42-2.7 5.39-5.26 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 23.5 12 11.5 11.5 0 0 0 12 .5z"/></svg>'

NAV = [("Home", "/"), ("Projects", "/projects/"), ("Resume", "/resume/"), ("Contact", "/contact/")]


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)


def page(path, title, desc, section, body, extra_foot=""):
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if label == section else ""}>{label}</a>'
        for label, href in NAV
    )
    full_title = PROFILE["name"] if title == "Home" else f"{title} · {PROFILE['name']}"
    canonical = SITE + path
    out = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>{e(full_title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{e(full_title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE}/assets/headshot.jpg">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/">DavidCreason.com</a>
      <nav class="nav" aria-label="Main">{nav}</nav>
    </div>
  </header>
{body}
  <footer class="site-footer">
    <div class="wrap">
      <span>&copy; <span id="yr"></span> {e(PROFILE['name'])}</span>
      <span><a href="{PROFILE['linkedin']}" rel="noopener">LinkedIn</a> &middot; <a href="{PROFILE['github']}" rel="noopener">GitHub</a> &middot; <a href="/contact/">Contact</a> &middot; <a href="/resume/">Resume</a></span>
    </div>
  </footer>
  <script>document.getElementById("yr").textContent = new Date().getFullYear();</script>{extra_foot}
</body>
</html>
"""
    write(path.strip("/") + "/index.html" if path != "/" else "index.html", out)


def redirect(path, to):
    write(path.strip("/") + "/index.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title>
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{SITE}{to}">
<meta http-equiv="refresh" content="0; url={to}">
</head><body><a href="{to}">This page moved. Continue &rarr;</a></body></html>
""")


def ext(href):
    return href.startswith("http")


def link_attrs(href):
    return ' rel="noopener" target="_blank"' if ext(href) else ""


def project_card(p, featured=False):
    tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
    links = "".join(
        f'<a class="btn{"" if primary else " ghost"} sm" href="{e(href)}"{link_attrs(href)}>{e(label)}</a>'
        for label, href, primary in p["links"]
    )
    detail = f"/projects/{p['slug']}/"
    cls = "project featured" if featured else "project"
    return f"""        <article class="{cls}">
          <a class="shot" href="{detail}"><img src="{e(p['image'])}" alt="{e(p['image_alt'])}" loading="lazy"></a>
          <div class="body">
            <p class="meta"><span class="badge {p['status']}">{e(p['badge'])}</span><span>{e(p['year'])}</span></p>
            <h3><a href="{detail}">{e(p['title'])}</a></h3>
            <p>{e(p['summary'])}</p>
            <ul class="tags">{tags}</ul>
            <div class="links">{links}</div>
          </div>
        </article>"""


def tableau(div_id, name, alt):
    img = f"https://public.tableau.com/static/images/{name[:2]}/{name}/1.png"
    params = {
        "host_url": "https%3A%2F%2Fpublic.tableau.com%2F", "embed_code_version": "3", "site_root": "",
        "name": name, "tabs": "no", "toolbar": "yes", "static_image": img, "animate_transition": "yes",
        "display_static_image": "yes", "display_spinner": "yes", "display_overlay": "yes",
        "display_count": "yes", "language": "en-US",
    }
    ps = "\n".join(f'            <param name="{k}" value="{v}">' for k, v in params.items())
    return f"""      <div class="viz-frame">
        <div class="tableauPlaceholder" id="{div_id}" style="position: relative">
          <noscript><a href="https://public.tableau.com/views/{name}"><img alt="{alt}" src="{img}" style="border:none"></a></noscript>
          <object class="tableauViz" style="display:none;">
{ps}
          </object>
        </div>
      </div>
      <p class="small"><a href="https://public.tableau.com/views/{name}" rel="noopener" target="_blank">Open full screen on Tableau Public &rarr;</a></p>"""


def tableau_script(div_id):
    return f"""
  <script>
    (function () {{
      var div = document.getElementById("{div_id}");
      var viz = div.getElementsByTagName("object")[0];
      function size() {{
        var w = div.offsetWidth;
        viz.style.width = "100%";
        viz.style.height = (w > 800 ? Math.round(w * 0.75) : w > 500 ? Math.round(w * 0.9) : 900) + "px";
      }}
      size(); window.addEventListener("resize", size);
      var s = document.createElement("script");
      s.src = "https://public.tableau.com/javascripts/api/viz_v1.js";
      viz.parentNode.insertBefore(s, viz);
    }})();
  </script>"""


def detail_page(p, lede, sections, extra_foot=""):
    tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
    links = "".join(
        f'<a class="btn{"" if primary else " ghost"}" href="{e(href)}"{link_attrs(href)}>{e(label)}</a>'
        for label, href, primary in p["links"] if href != f"/projects/{p['slug']}/"
    )
    page(f"/projects/{p['slug']}/", p["title"], p["summary"], "Projects", f"""  <main id="main">
    <div class="wrap">
      <nav class="breadcrumb"><a href="/projects/">&larr; All projects</a></nav>
      <p class="meta"><span class="badge {p['status']}">{e(p['badge'])}</span><span>{e(p['year'])}</span></p>
      <h1 class="page-title">{e(p['title'])}</h1>
      <p class="lede">{lede}</p>
      <ul class="tags">{tags}</ul>
      {f'<div class="actions">{links}</div>' if links else ''}
{sections}
    </div>
  </main>""", extra_foot)


CHAT = """      <div id="chat-container" aria-label="Chat with an AI assistant about David's experience">
        <div id="chips-wrapper">
          <button class="chip" data-q="What is David's core skill set?">Core Skills</button>
          <button class="chip" data-q="What roles is David targeting?">Target Roles</button>
          <button class="chip" data-q="Tell me about David's work at Ventas.">Ventas Experience</button>
          <button class="chip" data-q="What is David's education background?">Education &amp; Certs</button>
        </div>
        <div id="chat-box" aria-live="polite">
          <div class="msg bot">Hi! I&rsquo;m an AI assistant trained on David Creason&rsquo;s professional experience. Ask me anything or select a topic above!</div>
        </div>
        <div id="input-area">
          <input type="text" id="user-input" placeholder="Ask a question..." aria-label="Your question">
          <button id="send-btn">Send</button>
        </div>
      </div>"""

# --------------------------------------------------------------------------- pages
active = [p for p in PROJECTS if p["status"] == "active"]
past = [p for p in PROJECTS if p["status"] == "past"]
by = {p["slug"]: p for p in PROJECTS}

# Home
edu = "".join(f"<li>{e(x)}</li>" for x in EDUCATION)
page("/", "Home", f"{PROFILE['name']}, {PROFILE['role']}. Projects, data visualizations, and an AI assistant that answers questions about my experience.", "Home", f"""  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="role">{e(PROFILE['role'])}</p>
        <h1>{e(PROFILE['name'])}</h1>
        <p class="tagline">{e(PROFILE['tagline'])}</p>
        <div class="hero-actions">
          <a class="btn" href="/projects/">See my projects</a>
          <a class="btn light" href="#ask">Ask my AI assistant</a>
        </div>
        <div class="social">
          <a href="{PROFILE['linkedin']}" rel="noopener" target="_blank">{LI_SVG} LinkedIn</a>
          <a href="{PROFILE['github']}" rel="noopener" target="_blank">{GH_SVG} GitHub</a>
          <a href="/resume/">Resume</a>
        </div>
      </div>
    </div>
  </section>
  <main id="main">
    <section class="band stats-band" aria-label="Career highlights">
      <div class="wrap">
        <ul class="stats">
{"".join(f'          <li><strong>{e(v)}</strong><span>{e(l)}</span></li>\n' for v, l in STATS)}        </ul>
        {f'<p class="certs"><span class="certs-label">Certified</span>' + "".join(f'<span class="cert">{e(d)}<small>{e(sc)}</small></span>' for d, sc in CERTS) + '</p>' if CERTS else ''}
      </div>
    </section>
    <section class="band" id="ask">
      <div class="wrap grid-2">
        <div>
          <p class="eyebrow">Ask me anything</p>
          <h2>Talk to my AI resume assistant</h2>
          <p>Curious about my experience, leadership, or technical skills? This assistant is trained on my professional background and can answer in seconds, any time of day.</p>
          <p>Prefer a person? <a href="/contact/">Reach out directly</a>.</p>
          <div class="facts">
            <div><h3>Today</h3><p>{e(PROFILE['current'])}</p></div>
            <div><h3>Education &amp; certifications</h3><ul>{edu}</ul></div>
          </div>
        </div>
{CHAT}
      </div>
    </section>
    <section class="band alt">
      <div class="wrap">
        <div class="section-head">
          <div><p class="eyebrow">Now building</p><h2>Active projects</h2></div>
          <a class="more" href="/projects/">All projects &rarr;</a>
        </div>
        <div class="projects">
{project_card(active[0], featured=True)}
{chr(10).join(project_card(p) for p in active[1:])}
        </div>
      </div>
    </section>
    <section class="band">
      <div class="wrap">
        <div class="section-head">
          <div><p class="eyebrow">Selected work</p><h2>Past projects</h2></div>
        </div>
        <div class="projects">
{chr(10).join(project_card(p) for p in past)}
        </div>
      </div>
    </section>
    <section class="band cta">
      <div class="wrap">
        <h2>Let&rsquo;s work together</h2>
        <p>Open to conversations about analytics, systems, and automation work.</p>
        <div class="actions center"><a class="btn" href="/contact/#form">Send me a message</a><a class="btn ghost" href="/resume/">View resume</a></div>
      </div>
    </section>
  </main>""", extra_foot='\n  <script src="/assets/chat.js"></script>')

# Projects index
page("/projects/", "Projects", "Active and past projects by David Creason: web tools, AI, and data visualization.", "Projects", f"""  <main id="main">
    <div class="wrap">
      <p class="eyebrow">Portfolio</p>
      <h1 class="page-title">Projects</h1>
      <p class="lede">What I&rsquo;m building now and what I&rsquo;ve shipped. Every data visualization was developed with permission from the relevant parties.</p>
      <h2 class="group" id="active">Active</h2>
      <div class="projects">
{chr(10).join(project_card(p) for p in active)}
      </div>
      <h2 class="group" id="past">Past</h2>
      <div class="projects">
{chr(10).join(project_card(p) for p in past)}
      </div>
    </div>
  </main>""")

# Chimney planner detail
detail_page(by["chimney-planner"],
  "Planning a wood-stove or fireplace chimney means cross-referencing a thick manufacturer catalog, clearance rules, and NFPA 211. This planner does it for you: describe the installation and it returns every part you need, with quantities and part numbers.",
  """      <img class="hero-shot" src="/assets/projects/chimney-planner.jpg" alt="The planner's form and generated parts list">
      <div class="cols">
        <section>
          <h2>What it does</h2>
          <ul>
            <li>Walks you through the appliance, ceiling, attic, and roof measurements, or loads a worked example to start from.</li>
            <li>Applies the strictest rule among the DuraVent guideline, NFPA 211, and your appliance manual&rsquo;s own limits.</li>
            <li>Builds the parts list by location (ceiling, chimney pipe, attic, roof, top) and flags anything to double-check.</li>
            <li>Exports the list to CSV for ordering.</li>
          </ul>
        </section>
        <section>
          <h2>How it&rsquo;s built</h2>
          <ul>
            <li>The DuraVent catalog is kept as editable CSV files, compiled to JSON for the site.</li>
            <li>All the logic runs in the browser in plain JavaScript, with no server or database.</li>
            <li>Hosted free on GitHub Pages.</li>
            <li>Instead of a stove database that would always be out of date, users enter their appliance&rsquo;s own requirements.</li>
          </ul>
        </section>
        <section>
          <h2>Roadmap</h2>
          <ul>
            <li>Offsets on through-the-wall installations</li>
            <li>Free-standing stove placement and stovepipe</li>
            <li>The rest of DuraVent&rsquo;s residential product lines</li>
            <li>AI that reads an appliance manual and fills in its requirements</li>
          </ul>
        </section>
      </div>
      <p class="note">A planning aid, not an installation approval. Follow local code and have the finished system inspected by a certified professional.</p>""")

# Resume assistant detail
detail_page(by["resume-assistant"],
  "Recruiters ask the same questions about every candidate. I built an assistant that answers them about me, so anyone visiting this site can ask about my experience and get an immediate answer.",
  f"""      <div class="cols">
        <section>
          <h2>How it works</h2>
          <ul>
            <li>A serverless function on Vercel holds my professional background and calls a large language model.</li>
            <li>Answers stream back word by word, so there&rsquo;s no waiting on a full response.</li>
            <li>The chat window is about 100 lines of dependency-free JavaScript that drops into any page.</li>
            <li>Quick-question chips cover what people ask most.</li>
          </ul>
        </section>
      </div>
      <h2 style="margin-top:40px">Try it</h2>
      <div class="chat-demo">
{CHAT}
      </div>""", extra_foot='\n  <script src="/assets/chat.js"></script>')

# Louisville
findings = [
    ("Lunar influence", "No statistically significant relationship between full moons and higher crime rates."),
    ("Temperature", "A positive correlation: as daily temperatures rise, so does the number of crimes."),
    ("Geography", "The west side of the city sees a higher incidence of criminal activity than other areas."),
    ("Holidays", "Thanksgiving Day recorded the fewest crimes, suggesting holidays may influence crime patterns."),
    ("Seasonality", "Q3 had the highest average monthly crime counts."),
    ("Day of week", "Mondays registered more crimes than any other day."),
    ("Peak day", "July 22 had the single highest crime count of the year."),
]
items = "\n".join(f"        <li><strong>{h}</strong><span>{t}</span></li>" for h, t in findings)
detail_page(by["louisville-crime"],
  "This workbook contains information about reported crimes in 2024 in Louisville, KY.",
  f"""      <h2 style="margin-top:40px">Key findings</h2>
      <ul class="findings">
{items}
      </ul>
{tableau("viz-lou", "Louisville_KY_Crime_Stats/LouisvilleCrime", "Louisville, KY Crime Info")}""",
  extra_foot=tableau_script("viz-lou"))

# Crestwood
detail_page(by["crestwood-home-hearth"],
  "Zip codes and counties where Crestwood Home &amp; Hearth did business.",
  f"""      <div style="margin-top:32px"></div>
{tableau("viz-chh", "CrestwoodHomeHearth/CHHStory", "Crestwood Home &amp; Hearth Customers")}""",
  extra_foot=tableau_script("viz-chh"))

exec(open(os.path.join(ROOT, "resume.py")).read())

# Contact
page("/contact/", "Contact", "Get in touch with David Creason: technical solutions, data analysis, and operational leadership.", "Contact", f"""  <main id="main">
    <div class="wrap contact-card">
      <img src="/assets/headshot.jpg" alt="Photo of David Creason" width="225" height="400">
      <div>
        <p class="eyebrow">Contact</p>
        <h1 class="page-title">Get in Touch</h1>
        <p>I&rsquo;m David Creason, a results-driven professional with a background in technical solutions, data analysis, and operational leadership. Throughout my career, I&rsquo;ve worked across various industries, helping businesses optimize workflows, implement strategic solutions, and improve customer experiences.</p>
        <p>Whether you&rsquo;re looking to collaborate, discuss a potential opportunity, or just connect, I&rsquo;d love to hear from you. Feel free to reach out with any questions about my experience, skills, or how I can contribute to your team.</p>
        <div class="actions">
          <a class="btn ghost" href="/resume/">View my resume</a>
          <a class="btn ghost" href="{PROFILE['linkedin']}" rel="noopener" target="_blank">LinkedIn</a>
        </div>

        <form id="form" class="contact-form" novalidate>
          <h2>Let&rsquo;s start the conversation</h2>
          <div class="field-row">
            <label>Your name<input name="name" autocomplete="name" maxlength="100" required></label>
            <label>Your email<input name="email" type="email" autocomplete="email" maxlength="200" required></label>
          </div>
          <label><span>Subject <span class="opt">(optional)</span></span><input name="subject" maxlength="150"></label>
          <label>Message<textarea name="message" rows="6" maxlength="5000" required></textarea></label>
          <div class="hp" aria-hidden="true"><label>Company<input name="company" tabindex="-1" autocomplete="off"></label></div>
          <div class="form-foot">
            <button class="btn" type="submit">Send message</button>
            <p class="form-status" role="status" aria-live="polite"></p>
          </div>
        </form>
      </div>
    </div>
  </main>""", extra_foot='\n  <script src="/assets/contact.js"></script>')

# Old URLs (Google Sites + first rebuild) keep working
redirect("/home/", "/")
redirect("/data-viz/", "/projects/#past")
redirect("/data-viz/louisville-crime/", "/projects/louisville-crime/")
redirect("/data-viz/crestwood-home-hearth/", "/projects/crestwood-home-hearth/")

# 404
page("/404/", "Page not found", "Page not found.", "", """  <main id="main">
    <div class="wrap">
      <h1 class="page-title">Page not found</h1>
      <p class="lede">That page doesn&rsquo;t exist. Try the <a href="/">home page</a> or <a href="/projects/">my projects</a>.</p>
    </div>
  </main>""")
os.replace(os.path.join(ROOT, "404/index.html"), os.path.join(ROOT, "404.html"))
os.rmdir(os.path.join(ROOT, "404"))
print("Built", len(PROJECTS), "projects.")

# ---- Final safety check: no phone number or email address in any published page ----
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
for _dir, _, _files in os.walk(ROOT):
    if "/.git" in _dir:
        continue
    for _f in _files:
        if _f.endswith(".html"):
            _txt = open(os.path.join(_dir, _f)).read()
            assert not PHONE.search(_txt), f"Phone number found in {_f}; refusing to publish."
            assert not EMAIL_RE.search(_txt), f"Email address found in {_f}; refusing to publish."
print("Checked: no phone numbers or email addresses in any page.")
