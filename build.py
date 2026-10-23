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

# Cloudflare Turnstile on the contact form. Leave empty to keep it off. To turn it on, paste the
# widget's public site key here, push, and only then add TURNSTILE_SECRET_KEY in Vercel (see README).
TURNSTILE_SITE_KEY = "0x4AAAAAAFcITuj8hmNc4RBF"

# status: "active" or "past". Order here is display order within each group.
PROJECTS = [
    {
        "slug": "chimney-planner",
        "title": "DuraTech Chimney Planner",
        "status": "active",
        "badge": "Live · in development",
        "year": "2026",
        "summary": "Enter your home's measurements and get a complete DuraVent DuraTech chimney parts list that follows the manufacturer's installation rules and NFPA 211.",
        "tags": ["NFPA 211 checked", "Part numbers & quantities", "Flags problems early", "CSV export"],
        "image": "/assets/projects/chimney-planner.jpg",
        "image_alt": "Screenshot of the DuraTech Chimney Planner form and generated parts list",
        "links": [
            ("Launch the planner", "https://project-creason.github.io/chimney_planner/", True),
        ],
    },
    {
        "slug": "resume-assistant",
        "title": "Portfolio AI Assistant",
        "status": "active",
        "badge": "Live",
        "year": "2025",
        "summary": "A chat assistant grounded in my resume and project pages that answers visitors' questions about my experience, skills, education, and projects, with streamed responses from a serverless API.",
        "tags": ["LLM", "Vercel serverless", "Streaming", "Vanilla JS"],
        "image": "/assets/projects/cards/resume-assistant.jpg",
        "image_alt": "Ask, answer, link: answers about my work, any time",
        "links": [("Try it", "/#ask", True)],
    },
    {
        "slug": "jobber-import-etl",
        "title": "Vendor Price Sheet → Jobber Import ETL",
        "status": "active",
        "badge": "Live · in development",
        "year": "2019–2026",
        "summary": "A config-driven Python pipeline that turns any manufacturer's price sheet into a clean, validated Jobber product import, with every rejected row explained.",
        "tags": ["Python", "pandas", "ETL", "Data quality", "Jobber"],
        "image": "/assets/projects/cards/jobber-import-etl.jpg",
        "image_alt": "Price sheets, clean, Jobber: every rejected row explained",
        "links": [
            ("Launch the demo", "https://project-creason.github.io/jobber_import_etl/", True),
            ("Source on GitHub", "https://github.com/project-creason/jobber_import_etl", False),
        ],
    },
    {
        "slug": "property-etl-bench",
        "title": "Property ETL Bench",
        "status": "active",
        "badge": "In use · built for a REIT",
        "year": "2026",
        "summary": "A browser-based ETL tool that turns raw property spreadsheets into Yardi Voyager import files, setting up about 30 properties in a few minutes instead of 5+ hours by hand.",
        "tags": ["JavaScript", "HTML", "CSS", "ETL", "Yardi Voyager", "Batch processing", "AI-assisted development"],
        "image": "/assets/projects/cards/property-etl-bench.jpg",
        "image_alt": "Spreadsheet, validate, Yardi: about 30 properties in minutes",
        "links": [("Read the case study", "/projects/property-etl-bench/", True)],
    },
    {
        "slug": "buffalo-trace-tracker",
        "title": "Buffalo Trace Bourbon Availability Tracker",
        "status": "active",
        "badge": "Live · automated daily",
        "year": "2026",
        "summary": "Automated Python pipeline on GitHub Actions that polls Buffalo Trace Distillery during morning release hours, deduplicates lineup changes, sends instant mobile push and BCC email alerts, and streams live status to this site.",
        "tags": ["Python", "GitHub Actions", "Web scraping", "State deduplication", "Mobile push (ntfy)", "Live JSON feed"],
        "image": "/assets/projects/cards/buffalo-trace-tracker.svg",
        "image_alt": "Buffalo Trace Bourbon Availability Tracker live dashboard preview",
        "links": [
            ("View live tracker", "/projects/buffalo-trace-tracker/", True),
            ("Source on GitHub", "https://github.com/project-creason/buffalo-trace-tracker", False),
        ],
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
        "title": "Crestwood Home & Hearth: Systems, Growth & Exit Case Study",
        "status": "past",
        "badge": "Founded \u00b7 acquired",
        "year": "2018\u20132022",
        "summary": "Applied enterprise systems engineering, a 4,533-SKU vendor ETL pipeline, custom JavaScript/AJAX automation, 3D CAD modeling, and parametric quoting calculators to drive +740% annualized revenue expansion (63.6% peak gross margin) and a turnkey exit to a major local HVAC company.",
        "tags": ["Systems architecture", "Quote-to-cash", "ETL & automation", "Unit economics", "3D CAD & IoT", "Tableau", "M&A exit"],
        "image": "https://public.tableau.com/static/images/Cr/CrestwoodHomeHearth/CHHStory/1.png",
        "image_alt": "Crestwood Home and Hearth technical case study and customer map preview",
        "links": [("Read the case study", "/projects/crestwood-home-hearth/", True)],
    },
    {
        "slug": "meal-delivery-cms",
        "title": "Customer Management System for a Meal-Delivery Business",
        "status": "past",
        "badge": "Graduate capstone",
        "year": "2011",
        "summary": "Team capstone for my M.S. at Bellarmine: analyzed a local meal-delivery company's operations and delivered a working system for customers, orders, meal plans, allergies, and delivery scheduling, with process models and a user's guide.",
        "tags": ["Systems analysis & design", "BPMN process modeling", "Database application", "Technical documentation"],
        "image": "/assets/projects/cards/meal-delivery-cms.jpg",
        "image_alt": "Analyze, model, build: from process models to a working system",
        "links": [("Read more", "/projects/meal-delivery-cms/", True)],
    },
    {
        "slug": "itil-service-management",
        "title": "ITIL Service Management Assessments",
        "status": "past",
        "badge": "Graduate coursework",
        "year": "2011",
        "summary": "For my M.S. ITIL course, I assessed two fictional companies, a global resort operator and a mobile music service, and wrote recommendations to IT leadership on service portfolios, SLAs, supplier contracts, continuity, and change management.",
        "tags": ["ITIL service lifecycle", "Service level management", "IT service continuity", "Supplier management"],
        "image": "/assets/projects/cards/itil-service-management.jpg",
        "image_alt": "Assess, prioritize, advise: recovery tiers by business impact",
        "links": [("Read more", "/projects/itil-service-management/", True)],
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


def _short_degree(deg):
    # "Master of Science (MS) in Applied Information Technology" -> "M.S., Applied Information Technology"
    m = re.match(r"Master of [\w ]+?\((\w+)\)\s+in\s+(.+)", deg)
    if not m:
        return deg
    abbr = m.group(1) if len(m.group(1)) > 2 else ".".join(m.group(1)) + "."
    return f"{abbr}, {m.group(2)}"


# Homepage "Credentials" row: completed master's degrees, then certifications.
# An in-progress degree stays in the full education list until the resume shows it finished.
CREDENTIALS = [(_short_degree(deg), school) for deg, school in RESUME["education"]
               if re.search(r"\bmaster\b", deg, re.I) and "progress" not in f"{deg} {school}".lower()] + CERTS

# Facts from the resume used in project copy
# Crestwood summary is defined directly in PROJECTS above

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
  <meta property="og:image" content="{SITE}/assets/og-card.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(PROFILE['name'])}: {e(PROFILE['role'])}">
  <meta name="twitter:card" content="summary_large_image">
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
  <script data-goatcounter="https://davidcreason.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
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


CHAT = """      <div id="chat-container" aria-label="Chat with an AI assistant about David's experience and projects">
        <div id="chips-wrapper">
          <button class="chip" data-q="What is David's core skill set?">Core Skills</button>
          <button class="chip" data-q="What roles is David targeting?">Target Roles</button>
          <button class="chip" data-q="Tell me about David's work at Ventas.">Ventas Experience</button>
          <button class="chip" data-q="What is David's education background?">Education &amp; Certs</button>
        </div>
        <div id="chat-box" aria-live="polite">
          <div class="msg bot">Hi! I&rsquo;m David Creason&rsquo;s Portfolio AI Assistant. Ask me about his experience, skills, or projects, or pick a topic above!</div>
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
page("/", "Home", f"{PROFILE['name']}, {PROFILE['role']}. Projects, data visualizations, and an AI assistant that answers questions about my experience and projects.", "Home", f"""  <section class="hero" data-hero-bg="neural-constellation">
    <div class="hero-backdrop" aria-hidden="true">
      <canvas class="hero-canvas"></canvas>
      <div class="hero-spotlight"></div>
      <div class="hero-scrim"></div>
    </div>
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
        {f'<div class="certs"><p class="certs-label">Credentials</p><ul class="cert-list">' + "".join(f'<li class="cert" tabindex="0">{e(d)}<span class="cert-tip">{e(sc)}</span></li>' for d, sc in CREDENTIALS) + '</ul></div>' if CREDENTIALS else ''}
      </div>
    </section>
    <section class="band" id="ask">
      <div class="wrap grid-2">
        <div>
          <p class="eyebrow">Ask me anything</p>
          <h2>Talk to my Portfolio AI Assistant</h2>
          <p>Curious about my experience, technical skills, or projects? This assistant knows my resume and every project on this site, and can answer in seconds, any time of day.</p>
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
  </main>""", extra_foot='\n  <script src="/assets/hero.js"></script>\n  <script src="/assets/chat.js"></script>')

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
          <h2>Why it matters</h2>
          <ul>
            <li>Turns hours of cross-checking a catalog, a code book, and an appliance manual into a few minutes of measurements.</li>
            <li>Never shorts a requirement: heights and clearances can be exceeded but never undercut, and pipe lengths always round up.</li>
            <li>Catches problems before anything is bought, like an offset that won&rsquo;t fit in the attic or a chase too wide for stock flashing.</li>
            <li>Gets the order right the first time, with exact part numbers and quantities.</li>
            <li>Works for any stove or fireplace: you enter what its manual requires, so the planner never falls behind new models.</li>
          </ul>
        </section>
        <section>
          <h2>Built for</h2>
          <ul>
            <li><strong>Homeowners</strong> planning an install and wanting to know what it takes before they start.</li>
            <li><strong>Installers and sweeps</strong> quoting jobs quickly and consistently.</li>
            <li><strong>Hearth retailers</strong> building a complete, correct order with a customer at the counter.</li>
          </ul>
        </section>
        <section>
          <h2>Coming next</h2>
          <ul>
            <li>Offsets on through-the-wall installations</li>
            <li>Free-standing stove placement and stovepipe</li>
            <li>The rest of DuraVent&rsquo;s residential product lines</li>
            <li>AI that reads an appliance manual and fills in its requirements</li>
          </ul>
        </section>
      </div>
      <p class="note">A planning aid, not an installation approval. Follow local code and have the finished system inspected by a certified professional.</p>""")

# Portfolio AI Assistant detail

detail_page(by["resume-assistant"],
  "Recruiters ask the same questions about every candidate. I built an assistant that answers them about me, so anyone visiting this site can ask about my experience or projects and get an immediate answer.",
  f"""      <div class="cols">
        <section>
          <h2>How it works</h2>
          <ul>
            <li>A serverless function on Vercel calls a large language model, grounded in my resume and project pages.</li>
            <li>The site build publishes plain-text copies of both, so the assistant updates itself whenever I add a project or a new resume.</li>
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
CHH_SECTIONS = r'''      <style>
        .chh-stats { margin: 28px 0 36px; padding: 24px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); }
        .chh-tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 32px 0 20px; }
        .chh-tab {
          background: var(--card); color: var(--ink-soft); border: 1px solid var(--line);
          border-radius: 8px; padding: 9px 16px; font: 600 .84rem var(--head); cursor: pointer;
          transition: all .15s ease;
        }
        .chh-tab:hover { border-color: var(--accent); color: var(--ink); }
        .chh-tab.active { background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }
        .chh-panel { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; margin-bottom: 32px; }
        .chh-grid-2 { display: grid; grid-template-columns: 1.2fr 1fr; gap: 28px; align-items: start; }
        @media (max-width: 860px) { .chh-grid-2 { grid-template-columns: 1fr; } }
        .chh-bars {
          display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; align-items: end;
          height: 230px; padding: 20px 12px 12px; border-bottom: 1px solid var(--line);
        }
        .chh-bar-col {
          display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
          height: 100%; cursor: pointer; text-align: center;
        }
        .chh-bar-col .val { font: 700 .88rem var(--head); color: var(--ink); }
        .chh-bar-col .sub { font: 600 .72rem var(--head); color: var(--accent); margin-bottom: 6px; }
        .chh-bar-wrap {
          width: 100%; max-width: 68px; background: color-mix(in srgb, var(--line) 65%, var(--paper));
          border: 1px solid var(--line); border-radius: 8px 8px 0 0; overflow: hidden;
          display: flex; flex-direction: column; justify-content: flex-end; transition: transform .15s ease, border-color .15s ease;
        }
        .chh-bar-col:hover .chh-bar-wrap, .chh-bar-col.active .chh-bar-wrap {
          border-color: var(--accent); transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0,0,0,.08);
        }
        .chh-bar-gp { width: 100%; background: var(--accent); transition: height .2s ease; }
        .chh-bar-yr { font: 700 .82rem var(--head); margin-top: 8px; color: var(--ink); }
        .chh-legend { display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between; font: 600 .75rem var(--head); color: var(--ink-soft); margin-top: 10px; }
        .chh-swatch { display: inline-block; width: 11px; height: 11px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }
        .chh-detail-box { background: var(--paper); border: 1px solid var(--line); border-left: 4px solid var(--accent); border-radius: 8px; padding: 18px 20px; margin-top: 18px; }
        .chh-detail-head { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; padding-bottom: 10px; border-bottom: 1px solid var(--line); margin-bottom: 10px; }
        .chh-detail-head strong { font: 700 .98rem var(--head); color: var(--ink); }
        .chh-detail-metrics { display: flex; flex-wrap: wrap; gap: 14px; font: 600 .8rem var(--head); color: var(--ink-soft); }
        .chh-detail-metrics b { color: var(--ink); }
        .chh-arch-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-bottom: 20px; }
        .chh-node {
          text-align: left; background: var(--paper); border: 1px solid var(--line); border-radius: 8px;
          padding: 16px; cursor: pointer; transition: all .15s ease; font-family: inherit; color: inherit;
        }
        .chh-node:hover { border-color: var(--accent); }
        .chh-node.active { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent); background: var(--card); }
        .chh-node .step { font: 700 .72rem var(--head); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
        .chh-node h3 { font-size: 1.02rem; margin: 4px 0 6px; color: var(--ink); }
        .chh-node p { margin: 0; font-size: .9rem; color: var(--ink-soft); line-height: 1.45; }
        .chh-sim-controls { background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 18px; display: grid; gap: 14px; }
        .chh-sim-row label { display: flex; justify-content: space-between; font: 600 .82rem var(--head); color: var(--ink); margin-bottom: 4px; }
        .chh-sim-row input[type="range"] { width: 100%; accent-color: var(--accent); cursor: pointer; }
        .chh-kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-top: 16px; }
        .chh-kpi { background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 12px 14px; }
        .chh-kpi.highlight { border-left: 3px solid var(--accent); background: var(--card); }
        .chh-kpi .k-lbl { font: 600 .72rem var(--head); text-transform: uppercase; letter-spacing: .06em; color: var(--ink-soft); }
        .chh-kpi .k-val { font: 700 1.15rem var(--head); color: var(--ink); margin-top: 4px; }
        .chh-code {
          background: var(--paper); border: 1px solid var(--line); border-radius: 8px;
          padding: 16px; overflow-x: auto; font: .84rem/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
          color: var(--ink); margin: 14px 0;
        }
        /* CAD & 3D Viewer styles */
        .chh-cad-canvas-wrap {
          position: relative; background: #0f172a; border: 1px solid var(--line); border-radius: 8px;
          overflow: hidden; height: 340px; cursor: grab; user-select: none;
        }
        .chh-cad-canvas-wrap:active { cursor: grabbing; }
        .chh-cad-badge {
          position: absolute; top: 10px; left: 12px; background: rgba(15,23,42,.82); color: #e2e8f0;
          border: 1px solid rgba(255,255,255,.15); border-radius: 6px; padding: 5px 10px;
          font: 600 .72rem var(--head); pointer-events: none;
        }
        .chh-cad-telemetry {
          position: absolute; bottom: 10px; left: 12px; right: 12px; display: flex; flex-wrap: wrap;
          justify-content: space-between; gap: 8px; background: rgba(15,23,42,.82); color: #cbd5e1;
          border: 1px solid rgba(255,255,255,.14); border-radius: 6px; padding: 6px 10px;
          font: 600 .72rem ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; pointer-events: none;
        }
        .chh-cad-shot-wrap {
          background: var(--paper); border: 1px solid var(--line); border-radius: 8px; overflow: hidden;
          position: relative;
        }
        .chh-cad-shot-wrap img {
          width: 100%; height: 300px; object-fit: contain; background: #e5e7eb; display: block; cursor: zoom-in;
        }
        .chh-cad-thumbs {
          display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; margin-top: 10px;
        }
        @media (max-width: 600px) { .chh-cad-thumbs { grid-template-columns: repeat(3, 1fr); } }
        .chh-cad-thumb {
          border: 2px solid var(--line); border-radius: 6px; overflow: hidden; padding: 0;
          background: #e5e7eb; cursor: pointer; height: 54px; transition: border-color .15s ease;
        }
        .chh-cad-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
        .chh-cad-thumb.active, .chh-cad-thumb:hover { border-color: var(--accent); }
        .chh-lightbox {
          position: fixed; inset: 0; background: rgba(15,23,42,.88); z-index: 9999;
          display: none; align-items: center; justify-content: center; padding: 24px; cursor: zoom-out;
        }
        .chh-lightbox.open { display: flex; }
        .chh-lightbox img { max-width: 94vw; max-height: 88vh; border-radius: 8px; box-shadow: 0 20px 50px rgba(0,0,0,.5); background: #fff; }
      </style>

      <!-- KEY NUMBERS BAND (PERCENTAGE-DRIVEN) -->
      <div class="chh-stats" aria-label="Crestwood Home and Hearth key metrics">
        <ul class="stats">
          <li><strong>+740%</strong><span>annualized revenue expansion from Year 1 baseline to exit (8.4x)</span></li>
          <li><strong>+310%</strong><span>peak year-over-year revenue growth via counter-seasonal CAD expansion</span></li>
          <li><strong>54&ndash;64%</strong><span>gross profit margin across field services &amp; custom installations</span></li>
          <li><strong>+419%</strong><span>customer base expansion (1,215+ accounts &middot; +171% avg. ticket growth)</span></li>
          <li><strong>4,533</strong><span>manufacturer SKUs normalized across 15+ vendors via custom ETL</span></li>
          <li><strong>Acquired</strong><span>turnkey asset sale to a major local HVAC company</span></li>
        </ul>
      </div>

      <div class="cols">
        <section>
          <h2>The engineering approach to a trade business</h2>
          <p>After a decade in enterprise IT engineering (Neustar and Tealium), I founded Crestwood Home &amp; Hearth in 2018 and treated it as a systems architecture problem: standardize multi-vendor data, automate quote-to-cash, instrument field diagnostics, and engineer unit economics before scaling headcount.</p>
        </section>
        <section>
          <h2>Counter-seasonal product &amp; margin design</h2>
          <p>Traditional hearth businesses face steep warm-weather revenue drops. In Spring 2020, I expanded into 3D CAD-modeled automated pergolas, motorized smart screens, outdoor kitchens, and high-margin ceramic flue restoration&mdash;driving <strong>+310% year-over-year revenue growth</strong>, expanding average ticket size by <strong>+171%</strong>, and lifting peak gross margin to <strong>63.6%</strong>.</p>
        </section>
      </div>

      <!-- INTERACTIVE SECTION 1: PERCENTAGE GROWTH & MARGIN TELEMETRY -->
      <h2 style="margin-top:44px">1. Indexed revenue growth &amp; margin telemetry (2019&ndash;2022)</h2>
      <p>Click any year bar or button below to inspect the accrual-basis margin percentages, indexed growth multiples (<code>2019 Base = 100</code>), and technical milestones behind each phase.</p>

      <div class="chh-panel">
        <div class="chh-tabs" style="margin-top:0">
          <button type="button" class="chh-tab yr-tab" onclick="chhSelectYear(0)">2019 (Base = 100)</button>
          <button type="button" class="chh-tab yr-tab active" onclick="chhSelectYear(1)">2020 (+310% YoY)</button>
          <button type="button" class="chh-tab yr-tab" onclick="chhSelectYear(2)">2021 (+590% vs. Y1)</button>
          <button type="button" class="chh-tab yr-tab" onclick="chhSelectYear(3)">2022 (+740% Exit Run-Rate)</button>
        </div>

        <div class="chh-bars" role="region" aria-label="Annual indexed revenue and gross margin chart">
          <div class="chh-bar-col" onclick="chhSelectYear(0)">
            <span class="val">1.0x Base</span>
            <span class="sub">61.3% GM</span>
            <div class="chh-bar-wrap" style="height: 18%;">
              <div class="chh-bar-gp" style="height: 61.3%;" title="Gross Margin: 61.3%"></div>
            </div>
            <span class="chh-bar-yr">2019</span>
          </div>
          <div class="chh-bar-col active" onclick="chhSelectYear(1)">
            <span class="val">+310% YoY</span>
            <span class="sub">63.6% GM</span>
            <div class="chh-bar-wrap" style="height: 54%;">
              <div class="chh-bar-gp" style="height: 63.6%;" title="Gross Margin: 63.6% | Net Operating Margin: 24.7%"></div>
            </div>
            <span class="chh-bar-yr">2020 (4.1x)</span>
          </div>
          <div class="chh-bar-col" onclick="chhSelectYear(2)">
            <span class="val">+68% YoY</span>
            <span class="sub">53.6% GM</span>
            <div class="chh-bar-wrap" style="height: 84%;">
              <div class="chh-bar-gp" style="height: 53.6%;" title="Gross Margin: 53.6% | +590% vs. Year 1"></div>
            </div>
            <span class="chh-bar-yr">2021 (6.9x)</span>
          </div>
          <div class="chh-bar-col" onclick="chhSelectYear(3)">
            <span class="val">+740% vs. Y1*</span>
            <span class="sub">54.0% GM</span>
            <div class="chh-bar-wrap" style="height: 98%; border-style: dashed;">
              <div class="chh-bar-gp" style="height: 54.0%;" title="Gross Margin: 54.0% | 8.4x Year 1 Baseline"></div>
            </div>
            <span class="chh-bar-yr">2022* (8.4x)</span>
          </div>
        </div>

        <div class="chh-legend">
          <div>
            <span><i class="chh-swatch" style="background:var(--accent)"></i>Gross Profit Margin (% of Revenue)</span>
            <span style="margin-left:16px"><i class="chh-swatch" style="background:color-mix(in srgb, var(--line) 80%, var(--paper));border:1px solid var(--line)"></i>Direct Materials, Freight &amp; Subcontractor COGS (%)</span>
          </div>
          <span>*Annualized run-rate index at time of 2022 asset acquisition (2019 Base = 100 / 1.0x)</span>
        </div>

        <div id="chh-year-detail" class="chh-detail-box" aria-live="polite"></div>
      </div>

      <!-- INTERACTIVE SECTION 2: SYSTEMS & DATA ARCHITECTURE -->
      <h2 style="margin-top:44px">2. Enterprise IT &amp; quote-to-cash architecture</h2>
      <p>Click any component in the stack below to see the engineering problem, how it was built, and its operational impact.</p>

      <div class="chh-arch-grid" role="tablist" aria-label="System architecture components">
        <button type="button" class="chh-node active" onclick="chhSelectNode(0)">
          <span class="step">01 &middot; Data Ingestion &amp; ETL</span>
          <h3>Multi-Vendor SKU ETL Pipeline</h3>
          <p>Normalized 4,533 SKUs across 15+ manufacturers into Jobber CRM, QuickBooks Online, and Wix.</p>
        </button>
        <button type="button" class="chh-node" onclick="chhSelectNode(1)">
          <span class="step">02 &middot; Field CRM &amp; API Automation</span>
          <h3>Jobber Cloud + Custom JS/AJAX</h3>
          <p>Mobile dispatch, quote-to-cash automation, and custom DOM/REST scripts to bypass UI limits.</p>
        </button>
        <button type="button" class="chh-node" onclick="chhSelectNode(2)">
          <span class="step">03 &middot; Spatial CAD &amp; Smart IoT</span>
          <h3>3D SketchUp + Somfy/Wi-Fi IoT</h3>
          <p>3D architectural patio modeling and multi-zone RF/Wi-Fi motor &amp; weather-sensor commissioning.</p>
        </button>
        <button type="button" class="chh-node" onclick="chhSelectNode(3)">
          <span class="step">04 &middot; Algorithmic Quoting</span>
          <h3>Parametric Margin Calculators</h3>
          <p>Matrix pricing models enforcing target gross margin % and net operating yield after commission.</p>
        </button>
        <button type="button" class="chh-node" onclick="chhSelectNode(4)">
          <span class="step">05 &middot; Telemetry &amp; Diagnostics</span>
          <h3>Quantitative Field Protocols</h3>
          <p>33-point NFPA 211 checklists, Magnehelic pressure gauges, and millivolt ohmmeter SOPs.</p>
        </button>
        <button type="button" class="chh-node" onclick="chhSelectNode(5)">
          <span class="step">06 &middot; M&amp;A Data Room &amp; Exit</span>
          <h3>Turnkey Acquisition Packaging</h3>
          <p>Accrual financial telemetry, catalog exports, and operational runbooks for the acquiring company.</p>
        </button>
      </div>

      <div id="chh-node-detail" class="chh-panel" style="margin-top:0" aria-live="polite"></div>

      <!-- INTERACTIVE SECTION 3: PARAMETRIC PRICING & PERCENTAGE UNIT ECONOMICS -->
      <h2 style="margin-top:44px">3. Interactive pricing &amp; margin-percentage engine</h2>
      <p>Complex custom installations fail when field quotes miss freight, extrusion waste, labor hours, or sales commissions. Try the live calculator below (modeled directly on the production <code>Fixed Screen Calculator</code> and <code>Commission &amp; Profit Calculator</code> workbooks) to see how every quote was decomposed into exact cost, labor/commission, and net profit percentages.</p>

      <div class="chh-panel">
        <div class="chh-grid-2">
          <div>
            <p class="eyebrow">Live Margin Simulator</p>
            <h3 style="margin:0 0 8px">Custom Screen &amp; Commission Margin Allocation (%)</h3>
            <p class="small" style="margin:0 0 16px;color:var(--ink-soft)">Adjust project dimensions, openings, and commission tier to inspect how the parametric model protects gross and net margin percentages.</p>

            <div class="chh-sim-controls">
              <div class="chh-sim-row">
                <label for="chh-openings"><span>Number of Openings (Fixed Freight Amortization)</span><span id="chh-openings-lbl">4 openings</span></label>
                <input type="range" id="chh-openings" min="1" max="10" value="4" oninput="chhUpdateSim()">
              </div>
              <div class="chh-sim-row">
                <label for="chh-width"><span>Opening Width (inches)</span><span id="chh-width-lbl">72&quot;</span></label>
                <input type="range" id="chh-width" min="36" max="192" step="6" value="72" oninput="chhUpdateSim()">
              </div>
              <div class="chh-sim-row">
                <label for="chh-height"><span>Opening Height (inches)</span><span id="chh-height-lbl">99&quot;</span></label>
                <input type="range" id="chh-height" min="48" max="144" step="3" value="99" oninput="chhUpdateSim()">
              </div>
              <div>
                <div style="font:600 .82rem var(--head);margin-bottom:6px">Product Tier</div>
                <div style="display:flex;gap:8px;flex-wrap:wrap">
                  <button type="button" id="chh-tier-mot" class="chh-tab active" onclick="chhSetTier('motorized')">Motorized Smart Screen (Somfy/Alutech)</button>
                  <button type="button" id="chh-tier-fix" class="chh-tab" onclick="chhSetTier('fixed')">Fixed Architectural Extrusion</button>
                </div>
              </div>
            </div>

            <div id="chh-sim-kpis" class="chh-kpis"></div>
          </div>

          <div>
            <div style="display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap">
              <div>
                <p class="eyebrow">Standardized Labor Allocation</p>
                <h3 style="margin:0 0 8px">Service Catalog Margin &amp; Yield Index</h3>
              </div>
              <select id="chh-svc-filter" onchange="chhRenderServices()" aria-label="Filter service lines" style="font:600 .78rem var(--head);padding:6px 10px;border-radius:6px;border:1px solid var(--line);background:var(--paper);color:var(--ink)">
                <option value="all">All Featured Services (12)</option>
                <option value="high">High Hourly Yield (2.0x+ Base)</option>
                <option value="restoration">Technical Restoration &amp; Installs</option>
                <option value="diagnostics">Inspections &amp; Diagnostics</option>
              </select>
            </div>
            <p class="small" style="margin:0 0 12px;color:var(--ink-soft)">Every service line was benchmarked by estimated man-hours, target gross margin %, and hourly revenue yield index (<code>1.0x = baseline installation hour</code>) to optimize crew scheduling.</p>

            <div class="table-wrap" style="margin-top:0;max-height:380px;overflow-y:auto">
              <table class="tiers">
                <thead>
                  <tr>
                    <th scope="col">Service Line</th>
                    <th scope="col" style="text-align:right">Est. Hrs</th>
                    <th scope="col" style="text-align:right">Target GM %</th>
                    <th scope="col" style="text-align:right">Hourly Yield Index</th>
                  </tr>
                </thead>
                <tbody id="chh-svc-tbody"></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- SECTION 4: CUSTOM AUTOMATION & HARDWARE DIAGNOSTICS -->
      <h2 style="margin-top:44px">4. Custom DOM/AJAX automation &amp; quantitative diagnostics</h2>
      <div class="cols">
        <section>
          <h3>Bypassing SaaS UI limits with JavaScript</h3>
          <p>When supplier pricebooks updated, hundreds of obsolete SKUs in Jobber needed to be purged before importing the new catalog. Because Jobber&rsquo;s web interface lacked bulk deletion by vendor prefix, I wrote a browser-console jQuery/AJAX script (<code>jobber_quick_product_delete.js</code>) to scrape the internal item IDs from the DOM and fire asynchronous <code>DELETE</code> requests directly against Jobber&rsquo;s endpoint:</p>
          <pre class="chh-code"><code>// Production utility: Product Imports/jobber_quick_product_delete.js
var icc = $('a:contains("ICC")');
for (var i = 0; i &lt; icc.length; i++) {
  var item = icc[i].href.split('/')[4];
  $.ajax({
    url: 'https://secure.getjobber.com/work_items/' + item,
    type: 'DELETE',
    success: function() { console.log('Removed', item); }
  });
}</code></pre>
          <p class="small">This early catalog work directly inspired two standalone tools on this site: the <a href="/projects/jobber-import-etl/">Vendor Price Sheet &rarr; Jobber Import ETL</a> pipeline and the <a href="/projects/chimney-planner/">DuraTech Chimney Planner</a>.</p>
        </section>

        <section>
          <h3>Instrument-driven field diagnostics &amp; SOPs</h3>
          <ul>
            <li><strong>Millivolt gas valve ohmmeter testing:</strong> Authored technician training decks standardizing multimeter resistance checks across Robertshaw &amp; SIT Electromagnet Power Units (<code>0&ndash;13 &Omega;</code> specification between EPU lead and TP terminal) and preventative pilot/spill-switch replacement rules to eliminate repeat callbacks.</li>
            <li><strong>Magnehelic differential pressure &amp; airflow telemetry:</strong> Built CDET dryer exhaust evaluation forms recording pre- and post-cleaning backpressure (<code>&le; 0.6&quot; Water Column</code>) and anemometer airflow velocity (<code>MPH</code>) at the appliance and exterior termination.</li>
            <li><strong>Time-critical chemical &amp; refractory SOPs:</strong> Documented step-by-step field runbooks for ChamberGuard and FireGuard ceramic resurfacing equipment, including a strict 2-minute pump-blockage recovery decision tree before refractory material cures in the line.</li>
            <li><strong>M&amp;A transition to a major local HVAC company:</strong> In 2022, packaged the 1,215-customer book (+419% growth), brand assets, inventory/tooling assessments, and operational playbooks into a clean asset sale and 3-year management integration agreement with a major local HVAC company.</li>
          </ul>
        </section>
      </div>

      <!-- INTERACTIVE SECTION 5: 3D CAD & SPATIAL ENGINEERING VIEWER -->
      <h2 style="margin-top:44px">5. Interactive 3D CAD &amp; spatial engineering viewer</h2>
      <p>Every custom motorized louvered pergola and architectural screen project was modeled in 3D SketchUp prior to factory extrusion to verify structural beam spans, louver rotation clearances, fan beam chases, and gutter downspout math. Interact with the live 3D parametric rig on the left or inspect the anonymized production CAD blueprints on the right.</p>

      <div class="chh-panel">
        <div class="chh-grid-2">
          <!-- LEFT: LIVE INTERACTIVE 3D CANVAS RIG -->
          <div>
            <p class="eyebrow">Live 3D Parametric Rig (Drag to Orbit 360&deg;)</p>
            <h3 style="margin:0 0 8px">Motorized Dual-Bay Pergola &amp; Smart Screen Simulator</h3>
            <div class="chh-cad-canvas-wrap" id="chh-cad-wrap">
              <canvas id="chh-cad-canvas" width="540" height="340" style="width:100%;height:100%;display:block"></canvas>
              <div class="chh-cad-badge">3D Isometric CAD &middot; 21&apos;4&quot; &times; 19&apos;9&quot; Dual-Bay Rig</div>
              <div class="chh-cad-telemetry" id="chh-cad-telemetry">
                <span>Louver Pitch: 45&deg;</span>
                <span>Solar Shade: 71%</span>
                <span>ZIP Screens: 35% Deployed</span>
              </div>
            </div>
            <div class="chh-sim-controls" style="margin-top:12px">
              <div class="chh-sim-row">
                <label for="chh-louver-ang"><span>Somfy RTS Motorized Louver Pitch (0&deg;&ndash;135&deg;)</span><span id="chh-louver-lbl">45&deg; (71% Shade)</span></label>
                <input type="range" id="chh-louver-ang" min="0" max="135" value="45" oninput="chhUpdateCadRig()">
              </div>
              <div class="chh-sim-row">
                <label for="chh-screen-dep"><span>Hammerhead Motorized ZIP Screen Drop (0%&ndash;100%)</span><span id="chh-screen-lbl">35% Deployed</span></label>
                <input type="range" id="chh-screen-dep" min="0" max="100" value="35" oninput="chhUpdateCadRig()">
              </div>
              <div class="chh-sim-row">
                <label for="chh-cam-yaw"><span>3D Camera Orbit Angle (or drag model directly)</span><span id="chh-yaw-lbl">-38&deg; Azimuth</span></label>
                <input type="range" id="chh-cam-yaw" min="-180" max="180" value="-38" oninput="chhUpdateCadRig()">
              </div>
            </div>
          </div>

          <!-- RIGHT: ACTUAL SKETCHUP CAD BLUEPRINT & RENDER VIEWER -->
          <div>
            <p class="eyebrow">Production SketchUp (.skp) Engineering Exports</p>
            <h3 style="margin:0 0 8px" id="chh-bp-title">3D Perspective &mdash; Dual-Bay Louver &amp; Screen Assembly</h3>
            <div class="chh-cad-shot-wrap">
              <img id="chh-bp-img" src="/assets/cad/pergola-3d-perspective-1.jpg" alt="3D SketchUp CAD rendering of dual-bay motorized louvered pergola" onclick="chhOpenLightbox(this.src, this.alt)">
            </div>
            <div class="chh-cad-thumbs" role="tablist" aria-label="CAD blueprint sheets">
              <button type="button" class="chh-cad-thumb active" onclick="chhSelectBlueprint(0)" title="3D Perspective: Structural Gutter & Sidewall"><img src="/assets/cad/pergola-3d-perspective-1.jpg" alt="Thumbnail 1"></button>
              <button type="button" class="chh-cad-thumb" onclick="chhSelectBlueprint(1)" title="3D Perspective: 6x6 Posts & Motorized Screen Bay"><img src="/assets/cad/pergola-3d-perspective-2.jpg" alt="Thumbnail 2"></button>
              <button type="button" class="chh-cad-thumb" onclick="chhSelectBlueprint(2)" title="3D Overhead: Closed Interlocking Louver Deck"><img src="/assets/cad/pergola-3d-overhead-closed.jpg" alt="Thumbnail 3"></button>
              <button type="button" class="chh-cad-thumb" onclick="chhSelectBlueprint(3)" title="CAD Plan: 21'4 x 19'9 Dual-Bay & Fan Beam Clearances"><img src="/assets/cad/pergola-cad-overhead-plan.jpg" alt="Thumbnail 4"></button>
              <button type="button" class="chh-cad-thumb" onclick="chhSelectBlueprint(4)" title="CAD Engineering: 7.5-in Structural Gutter & Louver Math"><img src="/assets/cad/pergola-cad-gutter-math.jpg" alt="Thumbnail 5"></button>
              <button type="button" class="chh-cad-thumb" onclick="chhSelectBlueprint(5)" title="CAD Plan: 40-ft Multi-Zone Brick-Attached Beam Layout"><img src="/assets/cad/pergola-cad-40ft-span.jpg" alt="Thumbnail 6"></button>
            </div>
            <div id="chh-bp-desc" class="chh-detail-box" style="margin-top:12px;padding:12px 16px;font-size:.9rem"></div>
          </div>
        </div>
      </div>

      <div id="chh-lightbox" class="chh-lightbox" onclick="chhCloseLightbox()" role="dialog" aria-label="Expanded CAD blueprint view">
        <img id="chh-lightbox-img" src="" alt="">
      </div>

      <!-- SECTION 6: PRESERVED TABLEAU GEOGRAPHIC STORY -->
      <h2 style="margin-top:48px">6. Geographic customer reach (Tableau analysis)</h2>
      <p>Zip codes and counties across the Greater Louisville and Oldham County region where Crestwood Home &amp; Hearth sold, serviced, and installed.</p>
      <div style="margin-top:20px"></div>'''
CHH_SCRIPT = r'''  <script>
    (function () {
      var yearData = [
        {
          title: "2019 &middot; Foundation &amp; Credentialed Market Entry (Base Index = 100)",
          rev: "100 Index (1.0x Base)",
          gp: "61.3% Gross Margin",
          net: "12.8% Marketing Reinvestment",
          bullets: [
            "Entered the market as the county's only CSIA Certified Chimney Sweep and CDET Certified Dryer Exhaust Technician, establishing an immediate technical credential moat.",
            "Deployed the core cloud SaaS stack (Jobber CRM for field dispatch/quoting, QuickBooks Online for accrual accounting, Wix for web intake) and 33-point NFPA 211 digital inspection templates.",
            "Maintained a 61.3% gross profit margin (38.7% direct COGS) in Year 1 while reinvesting 100% of operating cash flow (including 12.8% of top-line revenue into digital customer acquisition)."
          ]
        },
        {
          title: "2020 &middot; +310% YoY Hyper-Growth &amp; Counter-Seasonal CAD Pivot",
          rev: "410 Index (+310% YoY / 4.1x)",
          gp: "63.6% Gross Margin (+230 bps)",
          net: "24.7% Net Operating Margin",
          bullets: [
            "Quadrupled top-line revenue (+310% YoY) while expanding gross profit margin by +230 bps to 63.6% and delivering a 24.7% audited net operating margin.",
            "Engineered a counter-seasonal product expansion in Spring 2020: onboarded StruXure automated louvered pergolas (3D SketchUp CAD workflows), motorized smart screens, and outdoor kitchens.",
            "Expanded active customer accounts by +238% YoY, normalized 4,533 SKUs across 15+ manufacturers, and onboarded the first W-2 field technician in Q4 2020."
          ]
        },
        {
          title: "2021 &middot; +68% YoY Scale-Up &amp; Multi-Crew Operations (+590% vs. Y1)",
          rev: "690 Index (+68% YoY / 6.9x)",
          gp: "53.6% Gross Margin",
          net: "20.3% Combined Owner SDE Margin",
          bullets: [
            "Scaled revenue to 6.9x Year 1 baseline (+590% cumulative 3-year growth; +68% YoY on top of 2020's 4.1x surge), with 87.6% driven by technical field services and 12.4% by direct hardware sales.",
            "Allocated 15.8% of revenue to W-2 technician payroll and 1099 contractors, funding national academy certifications and launching high-yield FireGuard ceramic flue resurfacing (2.25x hourly yield index).",
            "Expanded cumulative customer base past 1,200 accounts while increasing trailing 12-month average ticket value by +171% vs. Year 1."
          ]
        },
        {
          title: "2022 &middot; +740% Exit Run-Rate (8.4x) &amp; Turnkey Acquisition",
          rev: "840 Index (+740% vs. Y1 / 8.4x)",
          gp: "54.0% Gross Margin",
          net: "100% Turnkey Asset Transfer",
          bullets: [
            "Reached an 8.4x annualized revenue run-rate (+740% over Year 1 baseline) across 1,215 active customer accounts (+419% expansion) and 2,160+ historical digital invoices.",
            "Packaged accrual financial telemetry, margin-percentage rate cards, inventory/tooling schedules, and supplier onboarding runbooks into a formal M&A data room.",
            "Executed a turnkey asset sale and 3-year management integration agreement with a major local HVAC company."
          ]
        }
      ];

      window.chhSelectYear = function (idx) {
        var d = yearData[idx];
        var tabs = document.querySelectorAll(".yr-tab");
        var cols = document.querySelectorAll(".chh-bar-col");
        for (var i = 0; i < tabs.length; i++) {
          tabs[i].classList.toggle("active", i === idx);
          if (cols[i]) cols[i].classList.toggle("active", i === idx);
        }
        var box = document.getElementById("chh-year-detail");
        if (!box) return;
        var lis = d.bullets.map(function (b) { return "<li>" + b + "</li>"; }).join("");
        box.innerHTML =
          '<div class="chh-detail-head">' +
            '<strong>' + d.title + '</strong>' +
            '<div class="chh-detail-metrics">' +
              '<span>Growth Index: <b>' + d.rev + '</b></span>' +
              '<span>Gross Margin: <b>' + d.gp + '</b></span>' +
              '<span>Operating Metric: <b>' + d.net + '</b></span>' +
            '</div>' +
          '</div>' +
          '<ul style="margin:0;padding-left:20px;font-size:.96rem">' + lis + '</ul>';
      };

      /* --- 3D CAD BLUEPRINT GALLERY --- */
      var blueprints = [
        {
          title: "3D Perspective (SW) &mdash; Dual-Bay Louver &amp; Structural Gutter Integration",
          src: "/assets/cad/pergola-3d-perspective-1.jpg",
          desc: "<strong>Engineering Callout:</strong> 3D SketchUp model validating a <code>21&apos;4&quot; &times; 19&apos;9&quot;</code> dual-zone motorized louvered pergola tied into an existing <code>18&apos;</code> roofline via full-perimeter structural gutters, double outer beams, and <code>6&quot;&times;6&quot;</code> aluminum posts."
        },
        {
          title: "3D Perspective (NW) &mdash; Motorized ZIP Screen &amp; Outdoor Kitchen Clearances",
          src: "/assets/cad/pergola-3d-perspective-2.jpg",
          desc: "<strong>Engineering Callout:</strong> Verifies <code>10&apos;0&quot;</code> post height, <code>8&apos;10.5&quot;</code> &amp; <code>9&apos;8&quot;</code> column spacing around the outdoor kitchen island, and recessed track clearances for Somfy/Alutech motorized solar screens."
        },
        {
          title: "3D Overhead Render &mdash; Interlocking Louver Deck &amp; Center Mullion Beam",
          src: "/assets/cad/pergola-3d-overhead-closed.jpg",
          desc: "<strong>Engineering Callout:</strong> Top-down solar &amp; watershed simulation showing closed interlocking louvers pitching rainwater into the integrated <code>7.5&quot;</code> structural gutter channel."
        },
        {
          title: "CAD Plan View &mdash; Dual-Bay Louver Span &amp; Integrated Fan Beams",
          src: "/assets/cad/pergola-cad-overhead-plan.jpg",
          desc: "<strong>Engineering Callout:</strong> Shop fabrication layout specifying centered fan beams in both bays, double carrier beams per structural span request, and sidewalk/masonry tie-in tolerances."
        },
        {
          title: "CAD Drainage &amp; Louver Math &mdash; 20&apos; &times; 20&apos; Four-Quad Structural Plan",
          src: "/assets/cad/pergola-cad-gutter-math.jpg",
          desc: "<strong>Engineering Callout:</strong> Exact louver pitch spacing (<em>&ldquo;Good Louver Math&rdquo;</em> verification), dual <code>10&apos;</code> bay splits, <code>7.5&quot;</code> structural gutter sizing, and designated corner downspout discharges."
        },
        {
          title: "CAD Multi-Zone Elevation &mdash; 40&apos; &times; 12&apos; Brick-Attached Span",
          src: "/assets/cad/pergola-cad-40ft-span.jpg",
          desc: "<strong>Engineering Callout:</strong> Large-span <code>40&apos; &times; 12&apos;</code> commercial/residential ledger attachment to masonry brick, specifying intermediate post loads, double front beam, dual fan beams, and louver orientation."
        }
      ];

      window.chhSelectBlueprint = function (idx) {
        var b = blueprints[idx];
        var img = document.getElementById("chh-bp-img");
        var title = document.getElementById("chh-bp-title");
        var desc = document.getElementById("chh-bp-desc");
        var thumbs = document.querySelectorAll(".chh-cad-thumb");
        for (var i = 0; i < thumbs.length; i++) {
          thumbs[i].classList.toggle("active", i === idx);
        }
        if (img) { img.src = b.src; img.alt = b.title.replace(/&[^;]+;/g, ""); }
        if (title) title.innerHTML = b.title;
        if (desc) desc.innerHTML = b.desc;
      };

      window.chhOpenLightbox = function (src, alt) {
        var lb = document.getElementById("chh-lightbox");
        var img = document.getElementById("chh-lightbox-img");
        if (lb && img) {
          img.src = src;
          img.alt = alt || "Expanded CAD Blueprint";
          lb.classList.add("open");
        }
      };

      window.chhCloseLightbox = function () {
        var lb = document.getElementById("chh-lightbox");
        if (lb) lb.classList.remove("open");
      };

      /* --- INTERACTIVE 3D PARAMETRIC PERGOLA & SCREEN CANVAS RIG --- */
      var camPitch = 26;
      var isDragging = false;
      var lastX = 0, lastY = 0;

      function project3D(x, y, z, yawDeg, pitchDeg, w, h) {
        var yaw = yawDeg * Math.PI / 180;
        var pitch = pitchDeg * Math.PI / 180;
        var x1 = x * Math.cos(yaw) - z * Math.sin(yaw);
        var z1 = x * Math.sin(yaw) + z * Math.cos(yaw);
        var y2 = y * Math.cos(pitch) - z1 * Math.sin(pitch);
        var z2 = y * Math.sin(pitch) + z1 * Math.cos(pitch);
        var scale = 420 / (420 + z2 + 60);
        return { x: (w / 2) + x1 * scale, y: (h * 0.56) - y2 * scale, s: scale };
      }

      function drawLine3D(ctx, p1, p2, color, width) {
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.strokeStyle = color;
        ctx.lineWidth = width || 1.5;
        ctx.stroke();
      }

      function drawPoly3D(ctx, pts, fill, stroke, width) {
        ctx.beginPath();
        ctx.moveTo(pts[0].x, pts[0].y);
        for (var i = 1; i < pts.length; i++) ctx.lineTo(pts[i].x, pts[i].y);
        ctx.closePath();
        if (fill) { ctx.fillStyle = fill; ctx.fill(); }
        if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = width || 1; ctx.stroke(); }
      }

      window.chhUpdateCadRig = function () {
        var canvas = document.getElementById("chh-cad-canvas");
        if (!canvas) return;
        var ctx = canvas.getContext("2d");
        var w = canvas.width, h = canvas.height;

        var louverEl = document.getElementById("chh-louver-ang");
        var screenEl = document.getElementById("chh-screen-dep");
        var yawEl = document.getElementById("chh-cam-yaw");

        var louverAng = louverEl ? parseInt(louverEl.value, 10) : 45;
        var screenDep = screenEl ? parseInt(screenEl.value, 10) : 35;
        var yawDeg = yawEl ? parseInt(yawEl.value, 10) : -38;

        var shadePct = Math.round(Math.abs(Math.cos(louverAng * Math.PI / 180)) * 100);
        if (louverAng <= 5) shadePct = 100;

        document.getElementById("chh-louver-lbl").textContent = louverAng + "\u00b0 (" + shadePct + "% Shade)";
        document.getElementById("chh-screen-lbl").textContent = screenDep + "% Deployed";
        document.getElementById("chh-yaw-lbl").textContent = yawDeg + "\u00b0 Azimuth";
        document.getElementById("chh-cad-telemetry").innerHTML =
          "<span>Louver Pitch: " + louverAng + "\u00b0</span>" +
          "<span>Solar Shade: " + shadePct + "%</span>" +
          "<span>ZIP Screens: " + screenDep + "% Deployed</span>";

        ctx.clearRect(0, 0, w, h);

        // Background blueprint grid
        ctx.strokeStyle = "rgba(148, 163, 184, 0.12)";
        ctx.lineWidth = 1;
        for (var gx = -160; gx <= 160; gx += 40) {
          var g1 = project3D(gx, -70, -140, yawDeg, camPitch, w, h);
          var g2 = project3D(gx, -70, 140, yawDeg, camPitch, w, h);
          drawLine3D(ctx, g1, g2, "rgba(148,163,184,0.14)", 1);
        }
        for (var gz = -140; gz <= 140; gz += 40) {
          var g3 = project3D(-160, -70, gz, yawDeg, camPitch, w, h);
          var g4 = project3D(160, -70, gz, yawDeg, camPitch, w, h);
          drawLine3D(ctx, g3, g4, "rgba(148,163,184,0.14)", 1);
        }

        // Patio slab
        var slab = [
          project3D(-130, -70, -110, yawDeg, camPitch, w, h),
          project3D(130, -70, -110, yawDeg, camPitch, w, h),
          project3D(130, -70, 110, yawDeg, camPitch, w, h),
          project3D(-130, -70, 110, yawDeg, camPitch, w, h)
        ];
        drawPoly3D(ctx, slab, "rgba(30, 41, 59, 0.75)", "rgba(100, 116, 139, 0.5)", 1.5);

        // Existing house L-wall (tan/warm sandstone like SketchUp render)
        var backWall = [
          project3D(-130, -70, -110, yawDeg, camPitch, w, h),
          project3D(130, -70, -110, yawDeg, camPitch, w, h),
          project3D(130, 82, -110, yawDeg, camPitch, w, h),
          project3D(-130, 82, -110, yawDeg, camPitch, w, h)
        ];
        drawPoly3D(ctx, backWall, "rgba(214, 180, 138, 0.28)", "rgba(234, 179, 8, 0.65)", 1.5);

        var sideWall = [
          project3D(-130, -70, -110, yawDeg, camPitch, w, h),
          project3D(-130, -70, 40, yawDeg, camPitch, w, h),
          project3D(-130, 82, 40, yawDeg, camPitch, w, h),
          project3D(-130, 82, -110, yawDeg, camPitch, w, h)
        ];
        drawPoly3D(ctx, sideWall, "rgba(194, 155, 112, 0.32)", "rgba(234, 179, 8, 0.65)", 1.5);

        // Motorized ZIP screens (front & right sides)
        if (screenDep > 0) {
          var dropY = 68 - (138 * (screenDep / 100));
          // Front Bay 1 screen
          var scrF1 = [
            project3D(-125, 68, 105, yawDeg, camPitch, w, h),
            project3D(0, 68, 105, yawDeg, camPitch, w, h),
            project3D(0, dropY, 105, yawDeg, camPitch, w, h),
            project3D(-125, dropY, 105, yawDeg, camPitch, w, h)
          ];
          drawPoly3D(ctx, scrF1, "rgba(56, 189, 248, 0.18)", "rgba(56, 189, 248, 0.75)", 1.2);
          // Front Bay 2 screen
          var scrF2 = [
            project3D(0, 68, 105, yawDeg, camPitch, w, h),
            project3D(125, 68, 105, yawDeg, camPitch, w, h),
            project3D(125, dropY, 105, yawDeg, camPitch, w, h),
            project3D(0, dropY, 105, yawDeg, camPitch, w, h)
          ];
          drawPoly3D(ctx, scrF2, "rgba(56, 189, 248, 0.18)", "rgba(56, 189, 248, 0.75)", 1.2);
          // Right side screen
          var scrR = [
            project3D(125, 68, -105, yawDeg, camPitch, w, h),
            project3D(125, 68, 105, yawDeg, camPitch, w, h),
            project3D(125, dropY, 105, yawDeg, camPitch, w, h),
            project3D(125, dropY, -105, yawDeg, camPitch, w, h)
          ];
          drawPoly3D(ctx, scrR, "rgba(56, 189, 248, 0.22)", "rgba(56, 189, 248, 0.85)", 1.2);
        }

        // 6x6 Aluminum Posts
        var posts = [
          [-125, 105], [0, 105], [125, 105], [125, -105]
        ];
        for (var pi = 0; pi < posts.length; pi++) {
          var px = posts[pi][0], pz = posts[pi][1];
          var pTop = project3D(px, 72, pz, yawDeg, camPitch, w, h);
          var pBot = project3D(px, -70, pz, yawDeg, camPitch, w, h);
          drawLine3D(ctx, pTop, pBot, "#94a3b8", 4.5);
        }

        // Dual-bay Motorized Louvers
        var rad = louverAng * Math.PI / 180;
        var lHalf = 7.5;
        var dy = Math.sin(rad) * lHalf;
        var dz = Math.cos(rad) * lHalf;

        for (var z = -92; z <= 92; z += 16) {
          for (var bay = 0; bay < 2; bay++) {
            var xStart = bay === 0 ? -122 : 3;
            var xEnd = bay === 0 ? -3 : 122;
            var lPts = [
              project3D(xStart, 72 + dy, z - dz, yawDeg, camPitch, w, h),
              project3D(xEnd, 72 + dy, z - dz, yawDeg, camPitch, w, h),
              project3D(xEnd, 72 - dy, z + dz, yawDeg, camPitch, w, h),
              project3D(xStart, 72 - dy, z + dz, yawDeg, camPitch, w, h)
            ];
            drawPoly3D(ctx, lPts, "rgba(226, 232, 240, 0.55)", "#475569", 1);
          }
        }

        // Perimeter Double Beams & Center Mullion Beam
        var frameCorners = [
          [-125, -105], [125, -105], [125, 105], [-125, 105]
        ];
        for (var fi = 0; fi < 4; fi++) {
          var c1 = frameCorners[fi];
          var c2 = frameCorners[(fi + 1) % 4];
          drawLine3D(
            ctx,
            project3D(c1[0], 72, c1[1], yawDeg, camPitch, w, h),
            project3D(c2[0], 72, c2[1], yawDeg, camPitch, w, h),
            "#f8fafc",
            3.5
          );
        }
        // Center mullion beam
        drawLine3D(
          ctx,
          project3D(0, 72, -105, yawDeg, camPitch, w, h),
          project3D(0, 72, 105, yawDeg, camPitch, w, h),
          "#38bdf8",
          3.2
        );
        // Dimension callout lines in red (matching SketchUp CAD style)
        var d1 = project3D(-125, -70, 118, yawDeg, camPitch, w, h);
        var d2 = project3D(125, -70, 118, yawDeg, camPitch, w, h);
        drawLine3D(ctx, d1, d2, "#ef4444", 1.5);
        ctx.fillStyle = "#f87171";
        ctx.font = "600 11px sans-serif";
        ctx.fillText("21' 4\" Double Beam Span", (d1.x + d2.x) / 2 - 55, (d1.y + d2.y) / 2 + 14);
      };

      var cadWrap = document.getElementById("chh-cad-wrap");
      if (cadWrap) {
        cadWrap.addEventListener("mousedown", function (e) {
          isDragging = true;
          lastX = e.clientX;
          lastY = e.clientY;
        });
        window.addEventListener("mousemove", function (e) {
          if (!isDragging) return;
          var dx = e.clientX - lastX;
          var dy = e.clientY - lastY;
          lastX = e.clientX;
          lastY = e.clientY;
          var yawEl = document.getElementById("chh-cam-yaw");
          if (yawEl) {
            var nextYaw = parseInt(yawEl.value, 10) + Math.round(dx * 0.6);
            if (nextYaw > 180) nextYaw -= 360;
            if (nextYaw < -180) nextYaw += 360;
            yawEl.value = nextYaw;
          }
          camPitch = Math.max(8, Math.min(60, camPitch + dy * 0.3));
          window.chhUpdateCadRig();
        });
        window.addEventListener("mouseup", function () { isDragging = false; });
      }

      var nodeData = [
        {
          title: "01 &middot; Multi-Vendor SKU ETL Pipeline (4,533 SKUs)",
          stack: "Excel Power Query &middot; CSV Schema Mapping &middot; Jobber &middot; QuickBooks Online &middot; Wix",
          challenge: "15+ hearth, venting, skylight, and outdoor living manufacturers supplied unstructured dealer pricebooks with inconsistent part numbering, tiered dealer discounts (0.50x to 0.65x), and freight rules.",
          solution: "Engineered standardized import templates transforming raw vendor catalogs (1,969 RH Peterson SKUs, 1,218 ICC venting SKUs, 614 Majestic/HHT SKUs, 438 Archgard SKUs, 146 Bromic SKUs, 130 Velux SKUs) into clean Jobber and QuickBooks schemas.",
          impact: "Allowed technicians to build accurate multi-part quotes on an iPad in the field during an inspection, contributing to a +171% increase in average ticket value."
        },
        {
          title: "02 &middot; Field Service CRM &amp; Custom JS/AJAX Automation",
          stack: "Jobber Cloud CRM &middot; jQuery AJAX &middot; REST Endpoints &middot; Automated Client Comms",
          challenge: "Jobber streamlined dispatch, mobile invoicing, and card payments, but lacked bulk catalog lifecycle tools when hundreds of vendor SKUs needed to be deprecated or repriced.",
          solution: "Wrote custom client-side JavaScript (jobber_quick_product_delete.js) to query the authenticated DOM, extract internal work_item IDs, and fire asynchronous DELETE requests against Jobber's internal endpoint.",
          impact: "Cut catalog maintenance time by 99% (from days of manual clicking to seconds), keeping field pricing synchronized with supplier cost updates."
        },
        {
          title: "03 &middot; 3D Spatial CAD Modeling &amp; Smart-Home IoT Integration",
          stack: "SketchUp 3D (.skp) &middot; StruXure Somfy RTS/OS &middot; Alutech Hammerhead Wi-Fi SmartHub",
          challenge: "Custom motorized louvered pergolas and recessed patio screens required exact structural clearances, gutter drainage planning, and client visualization before custom factory extrusion.",
          solution: "Integrated 3D SketchUp spatial modeling (perspective renders, structural gutter math, and beam/post layouts) into proposals, paired with multi-zone Somfy RF/Wi-Fi motor commissioning and rain/wind sensor automation.",
          impact: "Unlocked counter-seasonal warm-weather revenue streams and propelled +310% year-over-year revenue growth in 2020."
        },
        {
          title: "04 &middot; Parametric Quoting &amp; Margin-Percentage Calculators",
          stack: "Multi-Zone Pricing Matrices &middot; Extrusion &amp; Spline Calculators &middot; Commission Models",
          challenge: "Custom screens and multi-zone pergolas involve nonlinear cost variables (linear feet of beams, extrusion cuts, mesh square footage, crating/freight, and sales commissions) that easily erode margins if misquoted.",
          solution: "Built parametric pricing workbooks (Pergola X Price Calculator 3.0, Fixed Screen Calculator, Commission &amp; Profit Calculator) that compute COGS %, freight amortization, labor hours, commission tiers, and net profit % before a quote is sent.",
          impact: "Protected ~29.2% net operating profit after commission on custom screen projects and 1.0x&ndash;3.5x hourly yield indexes across 26 standardized service lines."
        },
        {
          title: "05 &middot; Quantitative Field Diagnostics &amp; NFPA 211 Compliance",
          stack: "Digital Ohmmeter &middot; Magnehelic Pressure Gauge &middot; Anemometer &middot; Bore-Scope Video",
          challenge: "Residential service trades often rely on subjective technician opinions, leading to misdiagnosed gas valves, repeat callbacks, or unverifiable safety findings in real-estate transactions.",
          solution: "Created hardware troubleshooting SOPs (0&ndash;13 Ohm EPU safety magnet testing for millivolt gas valves, 2-minute pump-blockage recovery protocols) and digital inspection forms recording Magnehelic pressure (&le; 0.6\" W.C.) and MPH airflow.",
          impact: "Built high trust with homeowners and realtors while enabling structured onboarding for new technicians."
        },
        {
          title: "06 &middot; M&amp;A Data Room &amp; Turnkey Exit Architecture",
          stack: "QuickBooks Accrual Telemetry &middot; SDE Valuation Models &middot; Turnkey Onboarding Playbook",
          challenge: "Most small trade businesses are difficult to sell because operational knowledge is undocumented and financial/customer data is fragmented.",
          solution: "Maintained clean accrual-basis P&amp;L and Balance Sheet telemetry, documented all vendor accounts, inventory/tooling schedules, and service man-hour rates, and wrote a structured onboarding roadmap for the buyer.",
          impact: "Enabled a smooth 2022 asset acquisition by a major local HVAC company, paired with a 3-year management role to scale the combined division."
        }
      ];

      window.chhSelectNode = function (idx) {
        var nodes = document.querySelectorAll(".chh-node");
        for (var i = 0; i < nodes.length; i++) {
          nodes[i].classList.toggle("active", i === idx);
        }
        var d = nodeData[idx];
        var panel = document.getElementById("chh-node-detail");
        if (!panel) return;
        panel.innerHTML =
          '<div class="chh-detail-head">' +
            '<strong>' + d.title + '</strong>' +
            '<span style="font:600 .76rem var(--head);color:var(--accent)">' + d.stack + '</span>' +
          '</div>' +
          '<div class="cols" style="margin-top:12px;gap:20px">' +
            '<section><h3 style="font-size:.92rem;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft)">Engineering Challenge</h3><p style="margin:0;font-size:.95rem">' + d.challenge + '</p></section>' +
            '<section><h3 style="font-size:.92rem;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft)">Technical Implementation</h3><p style="margin:0;font-size:.95rem">' + d.solution + '</p></section>' +
            '<section><h3 style="font-size:.92rem;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft)">Business Impact</h3><p style="margin:0;font-size:.95rem">' + d.impact + '</p></section>' +
          '</div>';
      };

      var currentTier = "motorized";
      window.chhSetTier = function (tier) {
        currentTier = tier;
        var bMot = document.getElementById("chh-tier-mot");
        var bFix = document.getElementById("chh-tier-fix");
        if (bMot && bFix) {
          bMot.classList.toggle("active", tier === "motorized");
          bFix.classList.toggle("active", tier === "fixed");
        }
        window.chhUpdateSim();
      };

      window.chhUpdateSim = function () {
        var elO = document.getElementById("chh-openings");
        var elW = document.getElementById("chh-width");
        var elH = document.getElementById("chh-height");
        if (!elO || !elW || !elH) return;
        var openings = parseInt(elO.value, 10);
        var width = parseInt(elW.value, 10);
        var height = parseInt(elH.value, 10);

        document.getElementById("chh-openings-lbl").textContent = openings + (openings === 1 ? " opening" : " openings");
        document.getElementById("chh-width-lbl").textContent = width + '"';
        document.getElementById("chh-height-lbl").textContent = height + '"';

        var sqFt = (width * height) / 144;
        var retail, cogs, laborHrs, laborCost, comm;
        if (currentTier === "fixed") {
          var extrusion = 76;
          var laborPerOp = 100;
          var mesh = sqFt * 0.30;
          var spline = 45;
          var shipping = 175;
          var netPerOp = extrusion + laborPerOp + mesh;
          var retailPerOp = netPerOp * 2.18;
          retail = (retailPerOp * openings) + shipping;
          cogs = ((extrusion + mesh) * openings) + spline + shipping;
          laborHrs = openings * 2.5;
          laborCost = laborPerOp * openings;
          comm = retail * 0.08;
        } else {
          var unitCost = 1150 + (sqFt * 7.25);
          cogs = (unitCost * openings) + 75;
          retail = cogs * 1.986;
          laborHrs = openings * 4;
          laborCost = laborHrs * 30;
          comm = retail * 0.0971;
        }
        var grossMarginPct = ((retail - cogs) / retail) * 100;
        var cogsPct = (cogs / retail) * 100;
        var laborCommPct = ((laborCost + comm) / retail) * 100;
        var profit = retail - cogs - laborCost - comm;
        var netMarginPct = (profit / retail) * 100;
        var yieldIndex = (profit / laborHrs) / 100;

        var kpis = document.getElementById("chh-sim-kpis");
        if (kpis) {
          kpis.innerHTML =
            '<div class="chh-kpi"><div class="k-lbl">Gross Margin (%)</div><div class="k-val">' + grossMarginPct.toFixed(1) + '%</div></div>' +
            '<div class="chh-kpi"><div class="k-lbl">Hardware &amp; Freight COGS</div><div class="k-val">' + cogsPct.toFixed(1) + '%</div></div>' +
            '<div class="chh-kpi"><div class="k-lbl">Labor (' + laborHrs + 'h) + Comm.</div><div class="k-val">' + laborCommPct.toFixed(1) + '%</div></div>' +
            '<div class="chh-kpi highlight"><div class="k-lbl">Net Profit Margin (%)</div><div class="k-val">' + netMarginPct.toFixed(1) + '%</div></div>' +
            '<div class="chh-kpi highlight"><div class="k-lbl">Dealer Markup Ratio</div><div class="k-val">' + (retail / cogs).toFixed(2) + 'x</div></div>' +
            '<div class="chh-kpi highlight"><div class="k-lbl">Hourly Yield Index</div><div class="k-val">' + yieldIndex.toFixed(2) + 'x Base</div></div>';
        }
      };

      var services = [
        { name: "FireGuard Ceramic Liner Resurfacing", cat: "restoration", hrs: 16.0, gmPct: 68.5, yieldIdx: 2.25 },
        { name: "Direct Vent Fireplace Installation", cat: "restoration", hrs: 16.0, gmPct: 54.0, yieldIdx: 1.00 },
        { name: "Pellet Stove &amp; Venting System Install", cat: "restoration", hrs: 10.0, gmPct: 58.0, yieldIdx: 1.60 },
        { name: "Smoke Chamber Parging (ChamberGuard)", cat: "restoration", hrs: 10.0, gmPct: 64.0, yieldIdx: 1.30 },
        { name: "Siloxane Masonry Waterproofing", cat: "restoration", hrs: 4.5, gmPct: 72.0, yieldIdx: 2.00 },
        { name: "NFPA 211 Level 3 Invasive Inspection", cat: "diagnostics", hrs: 4.0, gmPct: 84.0, yieldIdx: 2.00 },
        { name: "CrownGuard Elastomeric Membrane", cat: "restoration", hrs: 1.0, gmPct: 76.0, yieldIdx: 3.49 },
        { name: "NFPA 211 Level 2 Real Estate Inspection", cat: "diagnostics", hrs: 1.5, gmPct: 88.0, yieldIdx: 2.00 },
        { name: "Stainless Chase Cover Replacement", cat: "restoration", hrs: 1.5, gmPct: 56.0, yieldIdx: 1.99 },
        { name: "Gas Fireplace Service &amp; Valve Diagnostic", cat: "diagnostics", hrs: 1.0, gmPct: 85.0, yieldIdx: 2.49 },
        { name: "Sweep + NFPA Level 1 Digital Report", cat: "diagnostics", hrs: 1.0, gmPct: 86.0, yieldIdx: 2.25 },
        { name: "Diagnostic &amp; System Evaluation Protocol", cat: "diagnostics", hrs: 0.5, gmPct: 90.0, yieldIdx: 3.50 }
      ];

      window.chhRenderServices = function () {
        var f = document.getElementById("chh-svc-filter");
        var val = f ? f.value : "all";
        var rows = services.filter(function (s) {
          if (val === "all") return true;
          if (val === "high") return s.yieldIdx >= 1.99;
          return s.cat === val;
        }).map(function (s) {
          return '<tr>' +
            '<th scope="row" style="white-space:normal">' + s.name + '</th>' +
            '<td style="text-align:right"><code>' + s.hrs + 'h</code></td>' +
            '<td style="text-align:right"><code>' + s.gmPct.toFixed(1) + '%</code></td>' +
            '<td style="text-align:right"><strong>' + s.yieldIdx.toFixed(2) + 'x</strong></td>' +
          '</tr>';
        }).join("");
        var tbody = document.getElementById("chh-svc-tbody");
        if (tbody) tbody.innerHTML = rows;
      };

      chhSelectYear(1);
      chhSelectBlueprint(0);
      chhUpdateCadRig();
      chhSelectNode(0);
      chhUpdateSim();
      chhRenderServices();
    })();
  </script>'''
detail_page(by["crestwood-home-hearth"],
  "How I applied enterprise systems integration, multi-vendor ETL pipelines (4,533 SKUs), custom JavaScript/AJAX automation, 3D SketchUp CAD modeling, and parametric unit-economics engines to drive +740% annualized revenue expansion (63.6% peak gross margin) and a turnkey acquisition exit to a major local HVAC company.",
  CHH_SECTIONS + "\n" + tableau("viz-chh", "CrestwoodHomeHearth/CHHStory", "Crestwood Home &amp; Hearth Customers"),
  extra_foot=CHH_SCRIPT + tableau_script("viz-chh"))

# Meal-delivery CMS (Bellarmine capstone)
detail_page(by["meal-delivery-cms"],
  "For the two-course IT Systems Project capstone in my M.S. in Applied Information Technology, our team analyzed the operations of a local meal-delivery company and built a customer management system around how it actually worked.",
  """      <figure class="shot-fig">
        <img class="hero-shot" src="/assets/projects/capstone-cms.jpg" alt="Swim-lane process model for creating and publishing a menu">
        <figcaption>One of the project's process models (menu creation), redrawn from the original 2011 diagram.</figcaption>
      </figure>
      <div class="cols">
        <section>
          <h2>What the business needed</h2>
          <ul>
            <li>Recurring meal-plan orders with start and end dates, quantities, and discounts.</li>
            <li>Customer allergies and food aversions tracked and checked against orders, since a miss is a safety issue.</li>
            <li>Vacation holds and multiple delivery locations, so each day's cooking and delivery list is right.</li>
          </ul>
        </section>
        <section>
          <h2>What we delivered</h2>
          <ul>
            <li>Business process models (BPMN swim lanes) of how the business ran, from creating menus to daily production and delivery.</li>
            <li>A database application to manage customers, orders, meal plans and pricing, discounts, delivery locations, and vacation holds.</li>
            <li>Allergies flagged separately from preferences, and carried through to the affected meal plans.</li>
            <li>Operational reports: daily orders, deliveries by meal plan and location, allergies and aversions, vacations, customer list, and billing.</li>
            <li>A step-by-step user's guide written for non-technical staff, including identity checks before account details are discussed.</li>
          </ul>
        </section>
        <section>
          <h2>Why it still matters</h2>
          <ul>
            <li>It's the same work I do today at enterprise scale: understand the business process first, model it, then build the system and the controls around it.</li>
            <li>Data quality, safety-critical rules, and documentation people actually use were part of the design from day one.</li>
          </ul>
        </section>
      </div>""")

# ITIL coursework (Bellarmine AIT 531)
_tiers = [
    ("Immediate recovery", ["Reservations", "Website", "Lodging", "Customer relationship management", "Club management"],
     "Revenue stops the moment these go down. Reservations and the website serve guests across time zones around the clock, and club members are the most loyal customers."),
    ("Fast recovery", ["Financial management", "Material management"],
     "Used by nearly every division, but guests can still check in and stay while they're down. Purchasing still matters: guests notice when the restaurant runs out of something."),
    ("Gradual recovery", ["Human resources"],
     "Not critical to daily operations, with paper records as a fallback. Restoring from backup is acceptable, and faster options would cost more than the downtime."),
    ("Manual workaround", ["Ski management", "Golf management"],
     "Each resort can take bookings by phone and in a daily planner until the system returns, the way it worked before computers."),
]
_tier_rows = "".join(
    f"<tr><th scope=\"row\">{e(t)}</th><td>{e(', '.join(svcs))}</td><td>{e(why)}</td></tr>" for t, svcs, why in _tiers
)
detail_page(by["itil-service-management"],
  "In my M.S. course on IT Planning &amp; Service Management Using ITIL, each assignment put me inside a fictional company with real-world IT problems and asked for recommendations to leadership. The companies were invented for the course; the analysis and recommendations below are mine.",
  f"""      <figure class="shot-fig">
        <img class="hero-shot" src="/assets/projects/itil-assessments.jpg" alt="Recovery tiers assigned to each IT service by business impact">
        <figcaption>From my continuity plan for the resort operator: every service assigned a recovery tier by business impact.</figcaption>
      </figure>

      <h2 style="margin-top:40px">Resort operator: an ITIL roadmap for the VP of IT</h2>
      <p>A global resort company with no defined list of IT services, weak service levels, and aging systems nobody had retired.</p>
      <div class="cols">
        <section>
          <h3>Service portfolio</h3>
          <ul>
            <li>Defined the portfolio: a pipeline, a catalog of 12 live services (from the service desk to reservations, lodging, ski, golf, and club management), and a retired list.</li>
            <li>Showed how never retiring services had left legacy systems in place.</li>
          </ul>
        </section>
        <section>
          <h3>Service levels &amp; suppliers</h3>
          <ul>
            <li>Replaced unmeasurable SLAs with the full set: service level requirements, measurable SLAs, internal OLAs, and a service improvement plan.</li>
            <li>Specified OLAs with every department, Finance, and HR.</li>
            <li>Identified six outside suppliers that needed underpinning contracts, including 24/7 support for the business-critical website.</li>
          </ul>
        </section>
        <section>
          <h3>Continuity</h3>
          <ul>
            <li>Assigned every service a recovery tier based on what an outage would cost the business (below).</li>
          </ul>
        </section>
      </div>
      <div class="table-wrap">
        <table class="tiers">
          <thead><tr><th scope="col">Tier</th><th scope="col">Services</th><th scope="col">Why</th></tr></thead>
          <tbody>{_tier_rows}</tbody>
        </table>
      </div>

      <h2 style="margin-top:44px">Mobile music service: fix the foundation before expanding</h2>
      <p>A fast-growing company weighing two new lines of business, a mobile game and a dating app, after a 48-hour outage.</p>
      <div class="cols">
        <section>
          <h3>Recommendation</h3>
          <ul>
            <li>Advised leadership to hold off on both launches until core IT service management was in place.</li>
            <li>In an earlier memo to leadership, explained what ITSM is and why it would align IT with the business: utility and warranty, clear ownership, and accountability.</li>
          </ul>
        </section>
        <section>
          <h3>Top three risks</h3>
          <ul>
            <li><strong>Availability:</strong> no formal service levels, and an implied 99.999% target already missed.</li>
            <li><strong>People and legacy tech:</strong> a COBOL finance and procurement system, a shrinking talent pool, and falling morale.</li>
            <li><strong>Change management:</strong> each office configured differently, no release management, and no known-error database.</li>
          </ul>
        </section>
        <section>
          <h3>Why it still matters</h3>
          <ul>
            <li>It's the same judgment I use today: tie IT decisions to business impact, standardize before you scale, and put controls around change.</li>
          </ul>
        </section>
      </div>
      <p class="note">LDI and Mobile Music are fictional companies created for the course. The case materials belong to their authors and aren't reproduced here.</p>""")

exec(open(os.path.join(ROOT, "resume.py")).read())

# Contact
page("/contact/", "Contact", "Get in touch with David Creason: technical solutions, data analysis, and operational leadership.", "Contact", f"""  <main id="main">
    <div class="wrap contact-card">
      <img src="/assets/headshot.jpg" alt="Photo of David Creason" width="225" height="400">
      <div>
        <p class="eyebrow">Contact</p>
        <h1 class="page-title">Get in Touch</h1>
        <p>I&rsquo;m David Creason, a results-driven professional with a background in technical solutions, data analysis, and operational leadership. Throughout my career, I&rsquo;ve worked across various industries, helping businesses optimize workflows, implement strategic solutions, and improve customer experiences.</p>
        <p>Whether you&rsquo;re hiring, looking to collaborate, or just want to connect, I&rsquo;d love to hear from you. If one of my <a href="/projects/">projects</a> caught your eye, like the chimney planner, my ETL tools, or the Portfolio AI Assistant, I&rsquo;m always glad to talk through how it was built and what I&rsquo;d do next.</p>
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
          {f'<div class="cf-turnstile" data-sitekey="{e(TURNSTILE_SITE_KEY)}" data-theme="auto" data-size="flexible"></div>' if TURNSTILE_SITE_KEY else ''}
          <div class="form-foot">
            <button class="btn" type="submit">Send message</button>
            <p class="form-status" role="status" aria-live="polite"></p>
          </div>
        </form>
      </div>
    </div>
  </main>""", extra_foot=('\n  <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>' if TURNSTILE_SITE_KEY else '')
    + '\n  <script src="/assets/contact.js"></script>')

# Old URLs (Google Sites + first rebuild) keep working
redirect("/home/", "/")
redirect("/data-viz/", "/projects/#past")
redirect("/data-viz/louisville-crime/", "/projects/louisville-crime/")
redirect("/data-viz/crestwood-home-hearth/", "/projects/crestwood-home-hearth/")

# 404
# Jobber import ETL (Crestwood Home & Hearth product catalog)
_fixes = [
    ("Prices stored as text", "List: \"6,022.00\"", "Cost: 6022"),
    ("SKU needs a vendor prefix", "017-01-H-SM-RBC", "AFD 017-01-H-SM-RBC"),
    ("Two apostrophes used as an inch mark", "9.69’’ (246MM) CEILING MOUNT POLE", "9.69\" (246MM) CEILING MOUNT POLE"),
    ("Hidden control character from a Windows export", "8\"␝ x 5.5\"␝", "8\" x 5.5\""),
    ("Escaped symbols", "COVER,AFD \\#435 BRDX LARGE", "COVER,AFD #435 BRDX LARGE"),
    ("$0 placeholder row", "STAND - TUNGSTEN PORTABLE - BOX 2 OF 2, 0", "Rejected: zero price"),
]
_fix_rows = "".join(
    f"<tr><th scope=\"row\">{e(what)}</th><td><code>{e(before)}</code></td><td><code>{e(after)}</code></td></tr>"
    for what, before, after in _fixes
)
detail_page(by["jobber-import-etl"],
  "Crestwood Home &amp; Hearth sold and installed products from many manufacturers, and Jobber, its field-service software, needed every one of them in its product list. Each manufacturer publishes its price sheet in its own layout, so each Jobber import file was built one vendor at a time. This pipeline replaces that with one repeatable run.",
  f"""      <figure class="shot-fig">
        <img class="hero-shot" src="/assets/projects/jobber-etl.jpg" alt="The four pipeline stages: extract, transform, validate, load">
        <figcaption>One command turns a folder of vendor price sheets into Jobber-ready imports.</figcaption>
      </figure>

      <div class="cols">
        <section>
          <h2>The problem</h2>
          <ul>
            <li>No two price sheets match. One manufacturer's sheet has part number, list, net, UPC, weight, and box dimensions; another has a model number and a single price.</li>
            <li>Jobber accepts exactly five columns: name, description, price, taxable, and category.</li>
            <li>The sheets carry small data problems that break an import or show up on a customer's quote: broken characters, inch marks, prices stored as text, placeholder rows, and duplicates.</li>
          </ul>
        </section>
        <section>
          <h2>The approach</h2>
          <ul>
            <li><strong>Extract:</strong> reads Excel or CSV, finds the header row under any title banner, detects the text encoding, and picks the right sheet.</li>
            <li><strong>Transform:</strong> maps each vendor's columns to Jobber's five, adds the vendor prefix to the SKU, parses prices, and cleans the text.</li>
            <li><strong>Validate:</strong> rows with no SKU, no price, or a $0 price, and duplicate SKUs, go to a rejects file with the reason.</li>
            <li><strong>Load:</strong> writes the Jobber CSV, the rejects file, and a run report.</li>
          </ul>
        </section>
      </div>

      <h2 style="margin-top:44px">What the cleanup actually fixes</h2>
      <p>Every example below is a real row from a manufacturer's catalog.</p>
      <div class="table-wrap">
        <table class="tiers">
          <thead><tr><th scope="col">Problem</th><th scope="col">In the price sheet</th><th scope="col">In the Jobber import</th></tr></thead>
          <tbody>{_fix_rows}</tbody>
        </table>
      </div>

      <div class="cols" style="margin-top:44px">
        <section>
          <h2>Design choices</h2>
          <ul>
            <li><strong>Configuration, not code.</strong> Each vendor is a short entry in a JSON file: which file names it matches, its SKU prefix, and which columns hold the SKU, description, and price. Adding a manufacturer takes a minute.</li>
            <li><strong>Nothing disappears silently.</strong> Every dropped row lands in a rejects file with the reason, so a person can fix the source instead of guessing.</li>
            <li><strong>Safe to re-run.</strong> Finished Jobber files are skipped, and SKUs that already carry a prefix don't get a second one.</li>
            <li><strong>Pricing is a setting.</strong> Use the list price as is, or start from dealer cost with a markup.</li>
          </ul>
        </section>
        <section>
          <h2>Results so far</h2>
          <ul>
            <li>Tested on real rows from three manufacturers, chosen because they contain the problems above.</li>
            <li>15 rows imported cleanly; 3 rejected, each with the correct reason: a missing price, a $0 item, and a duplicate part number.</li>
          </ul>
          <h2 style="margin-top:28px">Try it, and what's next</h2>
          <ul>
            <li><a href="https://project-creason.github.io/jobber_import_etl/" rel="noopener" target="_blank">Try the live demo</a>: run the sample price sheets or your own, right in the browser. It runs the same Python code as the repo, and files never leave your computer.</li>
            <li>Run it on every full price sheet in the catalog.</li>
            <li>Watch a shared Drive folder and convert new price sheets automatically when they arrive.</li>
          </ul>
        </section>
      </div>""")

detail_page(by["property-etl-bench"],
  "Every time a property joined the portfolio, its details arrived as a spreadsheet that someone reshaped by hand into the import files Yardi Voyager expects. I built a browser tool that does the whole batch in one pass.",
  """      <style>
        .flow-fig { margin: 32px 0 8px; padding: 20px 12px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); }
        .flow-fig svg { width: 100%; height: auto; display: block; }
        .flow-fig .n rect { fill: var(--paper); stroke: var(--line); stroke-width: 1.5; }
        .flow-fig .n.out rect { stroke: var(--accent); }
        .flow-fig .n.ext rect { fill: none; stroke: var(--ink-soft); stroke-dasharray: 6 4; }
        .flow-fig .n text { fill: var(--ink); font: 600 14px var(--head); text-anchor: middle; }
        .flow-fig .n .s { fill: var(--ink-soft); font: 400 12px var(--head); }
        .flow-fig .e { stroke: var(--ink-soft); stroke-width: 1.5; fill: none; }
        .flow-fig .dash { stroke-dasharray: 5 4; }
        .flow-fig .loop { stroke: var(--accent); stroke-dasharray: 5 4; }
        .flow-fig .lbl { fill: var(--accent); font: 600 12px var(--head); text-anchor: middle; }
        .flow-fig .arrow { fill: var(--ink-soft); }
        .flow-fig .mobile { display: none; }
        @media (max-width: 600px) { .flow-fig .desktop { display: none; } .flow-fig .mobile { display: block; } }
      </style>
      <figure class="shot-fig">
        <div class="flow-fig">
          <svg class="desktop" viewBox="0 0 820 290" role="img" aria-label="Data flow: a property spreadsheet is parsed, then validated and mapped. Errors loop back for correction. Clean data becomes Yardi import CSVs, with room for more target systems, then is reviewed and exported.">
            <defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="arrow" d="M0,0 L10,5 L0,10 z"/></marker></defs>
            <g class="n"><rect x="10" y="105" width="130" height="70" rx="10"/><text x="75" y="136">Source</text><text class="s" x="75" y="155">property spreadsheet</text></g>
            <g class="n"><rect x="175" y="105" width="140" height="70" rx="10"/><text x="245" y="136">Parse &amp; normalize</text><text class="s" x="245" y="155">clean headers, types</text></g>
            <g class="n"><rect x="350" y="105" width="140" height="70" rx="10"/><text x="420" y="136">Validate &amp; map</text><text class="s" x="420" y="155">rules → target fields</text></g>
            <g class="n out"><rect x="530" y="35" width="140" height="70" rx="10"/><text x="600" y="66">Yardi import CSVs</text><text class="s" x="600" y="85">whole batch at once</text></g>
            <g class="n ext"><rect x="530" y="175" width="140" height="70" rx="10"/><text x="600" y="206">Other systems</text><text class="s" x="600" y="225">add new outputs</text></g>
            <g class="n"><rect x="700" y="105" width="110" height="70" rx="10"/><text x="755" y="136">Review</text><text class="s" x="755" y="155">&amp; export</text></g>
            <path class="e" marker-end="url(#pa)" d="M140 140 H172"/>
            <path class="e" marker-end="url(#pa)" d="M315 140 H347"/>
            <path class="e" marker-end="url(#pa)" d="M490 130 C510 115, 505 75, 527 72"/>
            <path class="e dash" marker-end="url(#pa)" d="M490 150 C510 165, 505 205, 527 208"/>
            <path class="e" marker-end="url(#pa)" d="M670 72 C690 75, 685 115, 698 127"/>
            <path class="e dash" marker-end="url(#pa)" d="M670 208 C690 205, 685 165, 698 153"/>
            <path class="e loop" marker-end="url(#pa)" d="M420 177 C420 265, 75 265, 75 178"/>
            <text class="lbl" x="248" y="257">errors flagged for correction</text>
          </svg>
          <svg class="mobile" viewBox="0 0 320 540" role="img" aria-label="The same data flow, stacked vertically.">
            <defs><marker id="pm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="arrow" d="M0,0 L10,5 L0,10 z"/></marker></defs>
            <g class="n"><rect x="60" y="10" width="200" height="60" rx="10"/><text x="160" y="37">Source</text><text class="s" x="160" y="55">property spreadsheet</text></g>
            <g class="n"><rect x="60" y="110" width="200" height="60" rx="10"/><text x="160" y="137">Parse &amp; normalize</text><text class="s" x="160" y="155">clean headers, types</text></g>
            <g class="n"><rect x="60" y="210" width="200" height="60" rx="10"/><text x="160" y="237">Validate &amp; map</text><text class="s" x="160" y="255">rules → target fields</text></g>
            <g class="n out"><rect x="10" y="320" width="140" height="60" rx="10"/><text x="80" y="347">Yardi CSVs</text><text class="s" x="80" y="365">whole batch</text></g>
            <g class="n ext"><rect x="170" y="320" width="140" height="60" rx="10"/><text x="240" y="347">Other systems</text><text class="s" x="240" y="365">add new outputs</text></g>
            <g class="n"><rect x="60" y="430" width="200" height="60" rx="10"/><text x="160" y="457">Review &amp; export</text><text class="s" x="160" y="475">download files</text></g>
            <path class="e" marker-end="url(#pm)" d="M160 70 V107"/>
            <path class="e" marker-end="url(#pm)" d="M160 170 V207"/>
            <path class="e" marker-end="url(#pm)" d="M130 270 L90 317"/>
            <path class="e dash" marker-end="url(#pm)" d="M190 270 L230 317"/>
            <path class="e" marker-end="url(#pm)" d="M80 380 L130 427"/>
            <path class="e dash" marker-end="url(#pm)" d="M240 380 L190 427"/>
            <path class="e loop" marker-end="url(#pm)" d="M260 240 C305 240, 305 140, 263 140"/>
            <text class="lbl" x="160" y="525">Errors loop back for correction</text>
          </svg>
        </div>
        <figcaption>How data moves through the tool (simplified). Dashed paths show where new target systems plug in.</figcaption>
      </figure>

      <div class="cols">
        <section>
          <h2>The problem</h2>
          <ul>
            <li>New property details arrived as spreadsheets, but Yardi Voyager only accepts its own import layouts.</li>
            <li>Each property took 10 to 15 minutes of repetitive, careful reshaping by hand.</li>
            <li>A mistyped code or a missed column usually didn't surface until the import failed, or until bad data was already in the system.</li>
          </ul>
        </section>
        <section>
          <h2>The approach</h2>
          <ul>
            <li><strong>Parse &amp; normalize:</strong> reads the spreadsheet, standardizes headers, and trims and types every value.</li>
            <li><strong>Validate &amp; map:</strong> checks required fields and formats, then maps source columns to the target import layout. Problems are flagged inline before anything is generated.</li>
            <li><strong>Generate:</strong> writes the Yardi import CSVs for every property in the batch at once.</li>
            <li><strong>Review &amp; export:</strong> the user previews every output before downloading, so a person stays in the loop.</li>
          </ul>
        </section>
      </div>

      <h2 style="margin-top:44px">Results</h2>
      <ul class="stats">
        <li><strong>10–15 min</strong><span>per property, done by hand before</span></li>
        <li><strong>~30</strong><span>properties set up in the most recent run</span></li>
        <li><strong>Minutes</strong><span>for the entire batch, versus 5+ hours by hand</span></li>
      </ul>
      <p>Catching bad data at the validation step also means import errors get fixed in seconds by the person who has the context, instead of being discovered later in Yardi.</p>

      <div class="cols" style="margin-top:44px">
        <section>
          <h2>Built to extend</h2>
          <ul>
            <li>Parsing and validation are separate from output generation, so supporting another target system means adding a new mapping and output step. The front half stays the same.</li>
            <li>The pattern fits any organization that loads records from spreadsheets into one or more systems of record, well beyond real estate.</li>
            <li>Plain JavaScript, HTML, and CSS in a single page: no server to stand up or secure, and the data never leaves the user's computer.</li>
          </ul>
        </section>
        <section>
          <h2>What I'd highlight</h2>
          <ul>
            <li><strong>Business analysis first.</strong> The hard part was understanding the target system's import rules well enough to encode them, not writing the transformation.</li>
            <li><strong>AI-assisted development.</strong> I built it with an AI coding assistant, moving quickly from requirements to working software while I owned the design, the data rules, and the testing.</li>
            <li><strong>Designed for the operator.</strong> Inline validation and a review step make it safe for someone who isn't an engineer to run.</li>
          </ul>
        </section>
      </div>

      <p class="small" style="margin-top:44px">This tool was built for an employer, so the source code and real data aren't published here. The diagram and descriptions are simplified and contain no proprietary mappings or business rules.</p>""")

page("/404/", "Page not found", "Page not found.", "", """  <main id="main">
    <div class="wrap">
      <h1 class="page-title">Page not found</h1>
      <p class="lede">That page doesn&rsquo;t exist. Try the <a href="/">home page</a> or <a href="/projects/">my projects</a>.</p>
    </div>
  </main>""")
os.replace(os.path.join(ROOT, "404/index.html"), os.path.join(ROOT, "404.html"))
os.rmdir(os.path.join(ROOT, "404"))
print("Built", len(PROJECTS), "projects.")


# ---- Plain-text project notes for the AI assistant ----
# The Portfolio AI Assistant (resume-bot on Vercel) reads /assets/projects.txt (alongside resume.txt), so the
# assistant always knows exactly what the project pages say. Edit the pages, not this.
def _page_text(path):
    raw = open(os.path.join(ROOT, path.strip("/"), "index.html"), encoding="utf-8").read()
    m = re.search(r'<main id="main">(.*?)</main>', raw, re.S)
    t = m.group(1) if m else ""
    t = re.sub(r"<(style|script|svg|noscript|object|figure)\b.*?</\1>", " ", t, flags=re.S)
    # Drop what the header block below already states, and the live chat widget.
    t = re.sub(r'<nav class="breadcrumb">.*?</nav>', " ", t, flags=re.S)
    t = re.sub(r'<p class="meta">.*?</p>|<h1 class="page-title">.*?</h1>|<ul class="tags">.*?</ul>'
               r'|<div class="actions">.*?</div>', " ", t, flags=re.S)
    t = re.sub(r'<div id="chat-container".*?id="send-btn">.*?</button>\s*</div>\s*</div>', " ", t, flags=re.S)
    t = re.sub(r"<li[^>]*>", "\n- ", t)
    t = re.sub(r"<h[1-3][^>]*>", "\n\n", t)
    t = re.sub(r"</(h[1-3]|p|li|tr|section|div|ul|table)>", "\n", t)
    t = re.sub(r"<t[hd][^>]*>", " | ", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in t.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


_notes = ["DAVID CREASON'S PROJECTS (generated from davidcreason.com/projects; the project pages are the source of truth)\n"]
for _p in PROJECTS:
    _url = f"https://www.davidcreason.com/projects/{_p['slug']}/"
    _links = "; ".join(f"{label}: {href if ext(href) else 'https://www.davidcreason.com' + href}"
                       for label, href, _ in _p["links"])
    _notes.append(
        f"=== {_p['title']} ===\n"
        f"Status: {'Active / current' if _p['status'] == 'active' else 'Past'} ({_p['badge']}), {_p['year']}\n"
        f"Project page: {_url}\n"
        f"Links: {_links}\n"
        f"Tags: {', '.join(_p['tags'])}\n"
        f"Summary: {_p['summary']}\n\n"
        f"{_page_text('/projects/' + _p['slug'] + '/')}\n"
    )
write("assets/projects.txt", "\n".join(_notes))

# ---- Final safety check: no phone number or email address in any published page ----
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
for _dir, _, _files in os.walk(ROOT):
    if "/.git" in _dir:
        continue
    for _f in _files:
        if _f.endswith((".html", ".txt")):
            _txt = open(os.path.join(_dir, _f)).read()
            assert not PHONE.search(_txt), f"Phone number found in {_f}; refusing to publish."
            assert not EMAIL_RE.search(_txt), f"Email address found in {_f}; refusing to publish."
print("Checked: no phone numbers or email addresses in any page.")
