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

from resume_source import PHONE, load_resume, redact_emails, redact_phone_numbers

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.davidcreason.com"
RESUME_PDF = os.path.join(ROOT, "assets", "David_Creason_Resume.pdf")

# ---- Source of truth: the resume PDF --------------------------------------
_removed = redact_phone_numbers(RESUME_PDF)
if _removed:
    print(f"Removed {_removed} phone number(s) from the resume PDF.")
_removed = redact_emails(RESUME_PDF)
if _removed:
    print(f"Removed {_removed} email address(es) from the resume PDF.")
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
        "title": "Hearth Venting Planner",
        "status": "active",
        "badge": "Live · in development",
        "year": "2026",
        "summary": "Enter your home's measurements, pick a manufacturer and venting system (DuraVent DuraTech, ICC EXCEL), and get a complete parts list that follows the manufacturer's installation rules and NFPA 211.",
        "tags": ["NFPA 211 checked", "Multi-manufacturer", "Part numbers & quantities", "Flags problems early", "CSV export"],
        "image": "/assets/projects/chimney-planner.jpg",
        "image_alt": "Screenshot of the Hearth Venting Planner form and generated parts list",
        "links": [
            ("Launch the planner", "https://project-creason.github.io/chimney_planner/", True),
        ],
    },
    {
        "slug": "scopeout",
        "title": "ScopeOut: Guided Deal Scoping",
        "status": "active",
        "badge": "Live demo",
        "year": "2026",
        "summary": "A rules-based configurator that turns discovery answers into a validated software deal scope. Editable rules, price books, discount approvals, and branded buyer summaries, all driven by one catalog file.",
        "tags": ["Sales engineering", "Rules engine", "Catalog-driven", "Approval workflow", "Vercel serverless", "Vanilla JS"],
        "image": "/assets/projects/cards/scopeout.jpg",
        "image_alt": "Discovery, rules, scope: scope it right the first time",
        "links": [
            ("Read the case study", "/projects/scopeout/", True),
            ("Try the live demo", "/scopeout/", False),
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
        "title": "Louisville Crime: 2024 vs. 2025",
        "status": "past",
        "badge": "Completed",
        "year": "2025\u20132026",
        "summary": "Two-year analysis of 140,212 reported offenses in Louisville, KY across weather, moon phase, offense categories, geography, holidays, and timing. Hot days drive crime up (r = 0.51 in both years); full moons still don't.",
        "tags": ["Tableau", "Python", "Public data", "Correlation analysis", "Year-over-year"],
        "image": "https://public.tableau.com/static/images/Lo/Louisville_KY_Crime_Stats/LouisvilleCrime/1.png",
        "image_alt": "Louisville crime Tableau dashboard preview",
        "links": [("Explore 2024 vs. 2025", "/projects/louisville-crime/", True)],
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


SITEMAP = []  # pages search engines should index; filled by page(), written to sitemap.xml at the end


def page(path, title, desc, section, body, extra_foot="", noindex=False):
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if label == section else ""}>{label}</a>'
        for label, href in NAV
    )
    full_title = PROFILE["name"] if title == "Home" else f"{title} · {PROFILE['name']}"
    canonical = SITE + path
    if not noindex:
        SITEMAP.append(path)
    robots = '\n  <meta name="robots" content="noindex, nofollow, noarchive">' if noindex else ""
    out = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">{robots}
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
  "Planning a wood-stove or fireplace chimney means cross-referencing a thick manufacturer catalog, clearance rules, and NFPA 211. This planner does it for you: pick a manufacturer and venting system, describe the installation, and it returns every part you need, with quantities and part numbers.",
  """      <img class="hero-shot" src="/assets/projects/chimney-planner.jpg" alt="The planner's form and generated parts list">
      <div class="cols">
        <section>
          <h2>What it does</h2>
          <ul>
            <li>Lets you choose a manufacturer and venting system (currently DuraVent DuraTech and ICC EXCEL, 5&Prime;&ndash;8&Prime;) and switches rules and parts automatically while keeping your measurements.</li>
            <li>Walks you through the appliance, ceiling, attic, and roof measurements, or loads a worked example to start from.</li>
            <li>Applies the strictest rule among the manufacturer&rsquo;s installation manual, NFPA 211, and your appliance manual&rsquo;s own limits.</li>
            <li>Builds the parts list by location (ceiling, chimney pipe, attic, roof, top), flags anything to double-check, and exports to CSV or a priced dealer order.</li>
          </ul>
        </section>
        <section>
          <h2>Why it matters</h2>
          <ul>
            <li>Turns hours of cross-checking a catalog, a code book, and an appliance manual into a few minutes of measurements.</li>
            <li>Never shorts a requirement: heights and clearances can be exceeded but never undercut, and pipe lengths always round up.</li>
            <li>Catches problems before anything is bought, like an offset that won&rsquo;t fit in the attic or a chase too wide for stock flashing.</li>
            <li>Gets the order right the first time, with exact part numbers, quantities, and optional retailer/distributor SKU and price mapping.</li>
            <li>Works for any stove or fireplace: you enter what its manual requires, so the planner never falls behind new models.</li>
          </ul>
        </section>
        <section>
          <h2>Built for</h2>
          <ul>
            <li><strong>Homeowners</strong> planning an install and wanting to know what it takes before they start.</li>
            <li><strong>Installers and sweeps</strong> quoting jobs quickly and consistently.</li>
            <li><strong>Hearth retailers and distributors</strong> building a complete, priced order with their own SKUs at the counter.</li>
          </ul>
        </section>
        <section>
          <h2>Coming next</h2>
          <ul>
            <li>Offsets on through-the-wall installations</li>
            <li>Free-standing stove placement and stovepipe</li>
            <li>Additional residential chimney, pellet, and direct-vent product lines</li>
            <li>AI that reads an appliance manual and fills in its requirements</li>
          </ul>
        </section>
      </div>
      <p class="note">A planning aid, not an installation approval. Follow local code and have the finished system inspected by a certified professional.</p>""")

# Portfolio AI Assistant detail

detail_page(by["scopeout"],
  "Scoping a software deal usually means a rep applying packaging rules from memory or a spreadsheet, and the mistakes show up later as a surprise re-scope, a discount fight, or an unhappy first renewal. I built ScopeOut to turn those rules into a guided discovery flow, so every rep scopes the same way and every decision shows its reason.",
  """      <figure class="shot-fig">
        <img class="hero-shot" src="/assets/projects/scopeout.jpg" alt="ScopeOut in seller view: discovery questions on the left, the recommended plan, usage squares and checks on the right">
        <figcaption>Seller view. Every answer updates the plan, the bill of scope, and the reasons behind them as you go.</figcaption>
      </figure>

      <div class="cols">
        <section>
          <h2>The problem</h2>
          <ul>
            <li>Packaging rules live in a rep&rsquo;s head or a pricing spreadsheet, so two reps can scope the same customer two different ways.</li>
            <li>Discovery answers rarely make it into the CRM in a usable form, so the reasoning behind a deal is lost by the time it reaches deal desk or delivery.</li>
            <li>Changing packaging means retraining every rep, and old rules linger for months.</li>
          </ul>
        </section>
        <section>
          <h2>The approach</h2>
          <ul>
            <li><strong>Discovery first:</strong> the rep answers plain-language questions from the call, and the scope builds itself as they go.</li>
            <li><strong>Rules, not guesses:</strong> rules can only raise the requirement, so the strictest one sets the plan, and every decision is shown with its reason.</li>
            <li><strong>One catalog file per product:</strong> questions, plans, rules, price books and outputs all live in data. Import a new file and the tool reconfigures with no code changes.</li>
            <li><strong>Built on a proven engine:</strong> the same rules engine runs my <a href="/projects/chimney-planner/">chimney planner</a>, which shows it isn&rsquo;t tied to one industry.</li>
          </ul>
        </section>
      </div>

      <figure class="shot-fig" style="margin-top:44px">
        <img class="hero-shot" src="/assets/projects/scopeout-buyer.jpg" alt="ScopeOut in buyer view, white-labeled as Quillmetrics with a Powered by ScopeOut badge">
        <figcaption>Buyer view, white-labeled for a fictional analytics vendor. Buyers see the vendor&rsquo;s brand and a self-serve version of the same questions.</figcaption>
      </figure>

      <div class="cols">
        <section>
          <h2>For the sales team</h2>
          <ul>
            <li>Example scenarios load a realistic customer in one click, for training or for a live call.</li>
            <li>A bill of scope, a plain-language summary, and a CRM-ready record come out of every session.</li>
            <li>Discounts above a rep&rsquo;s limit need a manager&rsquo;s approval, and buyers never see a price that hasn&rsquo;t been approved.</li>
            <li>Buyers can get a branded email summary, sent by a small serverless function protected by a CAPTCHA and rate limits.</li>
          </ul>
        </section>
        <section>
          <h2>For RevOps</h2>
          <ul>
            <li>Packaging, price books, discount limits and simple rules are edited in a draft, then published to every rep at once.</li>
            <li>A change log shows exactly what moved between versions, price by price.</li>
            <li>Catalog imports are validated line by line, so a broken rule or a typo in a formula is caught before it reaches a rep.</li>
          </ul>
        </section>
      </div>

      <h2 style="margin-top:44px">At a glance</h2>
      <ul class="stats">
        <li><strong>1</strong><span>catalog file per product: questions, plans, rules and prices</span></li>
        <li><strong>2</strong><span>industries on one engine: software deals and chimney systems</span></li>
        <li><strong>3</strong><span>roles: rep, sales manager, RevOps admin</span></li>
      </ul>

      <div class="cols" style="margin-top:44px">
        <section>
          <h2>Using it on a sales call</h2>
          <ul>
            <li>Start with discovery, not a feature tour, and let the prospect&rsquo;s answers decide what the scope needs.</li>
            <li>Load a scenario that matches their situation, so they watch their own deal get scoped.</li>
            <li>Switch to the buyer view to show what their own customers would see.</li>
            <li>Send a branded summary at the end, so the scope and its reasoning travel with the deal.</li>
          </ul>
        </section>
        <section>
          <h2>What I&rsquo;d highlight</h2>
          <ul>
            <li><strong>Solutions engineering end to end.</strong> Defining the buyer&rsquo;s problem, designing the rules model, and building the tool that solves it.</li>
            <li><strong>Configuration as data.</strong> Moving business rules out of code means the people who own the rules can change them.</li>
            <li><strong>AI-assisted development.</strong> Built quickly with an AI coding assistant, while I owned the product decisions, the rules, and the testing.</li>
          </ul>
        </section>
      </div>

      <h2 style="margin-top:44px">Try it yourself</h2>
      <ul>
        <li>Load an example scenario and watch the plan and the usage squares change as you edit answers.</li>
        <li>Switch to <strong>Buyer</strong> to see the self-serve versions for executives and project leads.</li>
        <li>On the <strong>Admin</strong> tab, choose the RevOps admin role, change a rule, and publish it.</li>
        <li>Import a catalog on the Admin tab: try the <a href="/scopeout/files/quillmetrics-catalog.json" download>clean catalog</a>, then the <a href="/scopeout/files/quillmetrics-catalog-with-errors.json" download>one with planted errors</a> to see validation catch them.</li>
      </ul>
      <div class="actions" style="margin-top:20px"><a class="btn" href="/scopeout/">Try the live demo</a></div>

      <p class="small" style="margin-top:44px">Quillmetrics is a fictional company, and all products, customers and prices in the demo are illustrative.</p>""")

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
LOU_SECTIONS = f"""      <style>
        .lou-stats {{ margin: 28px 0 36px; padding: 24px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); }}
        .lou-bar-top {{
          display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap;
          margin: 36px 0 18px;
        }}
        .lou-bar-top h2 {{ margin: 0; }}
        .lou-controls {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
        .lou-btn {{
          background: var(--card); color: var(--ink-soft); border: 1px solid var(--line);
          border-radius: 8px; padding: 7px 13px; font: 600 .8rem var(--head); cursor: pointer;
          transition: all .15s ease; display: inline-flex; align-items: center; gap: 6px;
        }}
        .lou-btn:hover {{ border-color: var(--accent); color: var(--ink); }}
        .lou-btn.active {{ background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }}
        .lou-legend {{ display: flex; flex-wrap: wrap; gap: 18px; align-items: center; font: 600 .8rem var(--head); color: var(--ink-soft); margin: 0 0 20px; }}
        .lou-swatch {{ display: inline-block; width: 12px; height: 12px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }}
        .lou-hint {{ margin-left: auto; font: 600 .76rem var(--head); color: var(--accent); }}
        @media (max-width: 720px) {{ .lou-hint {{ margin-left: 0; width: 100%; }} }}

        .lou-vgrid {{
          display: grid; grid-template-columns: repeat(2, 1fr); gap: 22px; margin: 16px 0 44px;
        }}
        .lou-vgrid.full-mode {{ grid-template-columns: 1fr; gap: 28px; }}
        @media (max-width: 860px) {{ .lou-vgrid {{ grid-template-columns: 1fr; }} }}

        .lou-vcard {{
          background: var(--card); border: 1px solid var(--line); border-radius: var(--radius);
          padding: 20px 22px 18px; display: flex; flex-direction: column; gap: 10px;
          transition: box-shadow .18s ease, border-color .18s ease, transform .18s ease;
        }}
        .lou-vcard:hover {{ border-color: color-mix(in srgb, var(--accent) 55%, var(--line)); box-shadow: 0 10px 28px rgba(0,0,0,.08); }}
        .lou-vcard.expanded {{
          grid-column: 1 / -1; border-color: var(--accent);
          box-shadow: 0 14px 36px rgba(0,0,0,.12); padding: 26px 28px 22px;
        }}
        .lou-vcard.expanded h3 {{ font-size: 1.35rem; }}
        .lou-vcard.expanded .lou-vsvg-wrap {{ padding: 18px 18px 12px; }}

        .lou-vcard-top {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; }}
        .lou-vkicker {{ font: 700 .72rem var(--head); text-transform: uppercase; letter-spacing: .09em; color: var(--accent); }}
        .lou-vtop-right {{ display: flex; align-items: center; gap: 8px; }}
        .lou-vpill {{ font: 700 .7rem var(--head); padding: 3px 9px; border-radius: 999px; }}
        .lou-vpill.same {{ background: color-mix(in srgb, var(--line) 70%, transparent); color: var(--ink-soft); }}
        .lou-vpill.shift {{ background: rgba(181,85,43,.14); color: var(--accent); }}
        .lou-vpill.low {{ background: rgba(47,163,86,.15); color: #2fa356; }}
        .lou-exp-btn {{
          background: var(--paper); color: var(--ink-soft); border: 1px solid var(--line);
          border-radius: 6px; padding: 3px 9px; font: 600 .72rem var(--head); cursor: pointer;
          transition: all .15s ease;
        }}
        .lou-exp-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
        .lou-vcard.expanded .lou-exp-btn {{ background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }}

        .lou-vcard h3 {{ font-size: 1.12rem; margin: 0; line-height: 1.25; }}
        .lou-vsvg-wrap {{
          background: var(--paper); border: 1px solid var(--line); border-radius: 8px;
          padding: 12px 10px 8px; margin-top: 2px; position: relative;
        }}
        .lou-vsvg {{ width: 100%; height: auto; display: block; overflow: visible; }}
        .lou-vsvg text {{ font-family: var(--head); fill: var(--ink); pointer-events: none; transition: opacity .15s ease; }}
        .lou-vsvg .muted {{ fill: var(--ink-soft); }}
        .lou-vsvg .acc {{ fill: var(--accent); }}
        .lou-vsvg .grn {{ fill: #2fa356; }}
        .lou-vsvg .axis {{ stroke: var(--line); stroke-width: 1; pointer-events: none; }}
        .lou-vsvg .dash-base {{ stroke: var(--ink-soft); stroke-width: 1.2; stroke-dasharray: 4 3; opacity: .65; pointer-events: none; }}
        .lou-vsvg .b24 {{ fill: color-mix(in srgb, var(--ink-soft) 48%, var(--paper)); stroke: var(--line); stroke-width: 1; transition: all .15s ease; }}
        .lou-vsvg .b25 {{ fill: var(--accent); transition: all .15s ease; }}
        .lou-vsvg .bgrn {{ fill: #2fa356; transition: all .15s ease; }}

        /* Year focus modes */
        .lou-vgrid.focus-2024 .b25, .lou-vgrid.focus-2024 .bgrn, .lou-vgrid.focus-2024 .line-25 {{ opacity: .18; }}
        .lou-vgrid.focus-2024 .b24 {{ fill: var(--accent); stroke: var(--accent); }}
        .lou-vgrid.focus-2025 .b24, .lou-vgrid.focus-2025 .line-24 {{ opacity: .18; }}

        /* Interactive SVG hover groups */
        .lou-hit {{ cursor: pointer; outline: none; transition: opacity .15s ease; }}
        .lou-hit .hit-bg {{ fill: transparent; rx: 5px; transition: fill .15s ease, stroke .15s ease; }}
        .lou-vsvg:has(.lou-hit:hover) .lou-hit:not(:hover),
        .lou-vsvg:has(.lou-hit:focus) .lou-hit:not(:focus) {{ opacity: .38; }}
        .lou-hit:hover .hit-bg, .lou-hit:focus .hit-bg {{
          fill: color-mix(in srgb, var(--accent) 9%, transparent);
          stroke: color-mix(in srgb, var(--accent) 45%, transparent);
          stroke-width: 1;
        }}
        .lou-hit:hover .b24, .lou-hit:focus .b24 {{ stroke: var(--ink); stroke-width: 1.5; filter: brightness(1.06); }}
        .lou-hit:hover .b25, .lou-hit:focus .b25,
        .lou-hit:hover .bgrn, .lou-hit:focus .bgrn {{ stroke: var(--ink); stroke-width: 1.5; filter: brightness(1.1); }}

        /* Live readout bar inside each card */
        .lou-readout {{
          display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap;
          background: color-mix(in srgb, var(--line) 28%, var(--paper)); border: 1px solid var(--line);
          border-left: 3px solid var(--accent); border-radius: 6px; padding: 8px 12px;
          font: .84rem/1.4 var(--head); color: var(--ink-soft); min-height: 38px;
        }}
        .lou-readout strong {{ color: var(--ink); font-weight: 700; }}
        .lou-readout .ro-badges {{ display: inline-flex; gap: 8px; align-items: center; flex-wrap: wrap; font-size: .78rem; font-weight: 700; }}
        .lou-readout .ro-24 {{ color: var(--ink-soft); }}
        .lou-readout .ro-25 {{ color: var(--accent); }}
        .lou-readout .ro-d {{ padding: 1px 7px; border-radius: 999px; background: color-mix(in srgb, var(--line) 75%, transparent); color: var(--ink); }}

        /* Floating cursor tooltip */
        #lou-tip {{
          position: fixed; z-index: 9999; pointer-events: none; opacity: 0; transform: translateY(4px);
          transition: opacity .12s ease, transform .12s ease;
          background: var(--navy); color: #fff; border: 1px solid rgba(255,255,255,.16);
          border-radius: 8px; padding: 10px 13px; box-shadow: 0 12px 28px rgba(0,0,0,.28);
          font: .78rem/1.45 var(--head); max-width: 280px;
        }}
        #lou-tip.show {{ opacity: 1; transform: translateY(0); }}
        #lou-tip .t-head {{ font-weight: 700; font-size: .84rem; color: #fff; margin-bottom: 4px; border-bottom: 1px solid rgba(255,255,255,.14); padding-bottom: 4px; }}
        #lou-tip .t-row {{ display: flex; justify-content: space-between; gap: 14px; color: #d9e0e8; }}
        #lou-tip .t-row b {{ color: #fff; }}
        #lou-tip .t-note {{ margin-top: 5px; color: #f0b597; font-size: .74rem; font-weight: 600; }}
      </style>

      <div class="lou-stats" aria-label="Louisville crime 2024 vs 2025 key metrics">
        <ul class="stats">
          <li><strong>140,212</strong><span>reported offenses analyzed (69,876 in 2024 &middot; 70,336 in 2025, +0.7% YoY)</span></li>
          <li><strong>r = 0.51</strong><span>daily high-temp correlation in both years (+0.73 to +0.76 offenses per &deg;F)</span></li>
          <li><strong>-20.1%</strong><span>drop in auto thefts in 2025 (-1,161), alongside homicide (-26.1%) &amp; robbery (-18.4%)</span></li>
          <li><strong>+28.5%</strong><span>surge in retail shoplifting (+912), with grocery store incidents up +73.6%</span></li>
          <li><strong>88</strong><span>offenses on Jan 6, 2025 (winter storm &amp; ice) &mdash; single lowest day across both years</span></li>
          <li><strong>-20.2%</strong><span>drop in Downtown (40202) offenses in 2025, while outer-ring ZIPs rose</span></li>
        </ul>
      </div>

      <div class="lou-bar-top">
        <h2>2024 vs. 2025 interactive visual comparison</h2>
        <div class="lou-controls" role="toolbar" aria-label="Chart display controls">
          <button type="button" class="lou-btn active" data-yr="both" onclick="louSetYear('both', this)">Both Years</button>
          <button type="button" class="lou-btn" data-yr="2024" onclick="louSetYear('2024', this)">2024 Only</button>
          <button type="button" class="lou-btn" data-yr="2025" onclick="louSetYear('2025', this)">2025 Only</button>
          <button type="button" class="lou-btn" id="lou-layout-btn" onclick="louToggleAllExpand()">&#x2922; Expand All Charts</button>
        </div>
      </div>

      <div class="lou-legend">
        <span><i class="lou-swatch" style="background:color-mix(in srgb, var(--ink-soft) 48%, var(--paper));border:1px solid var(--line)"></i>2024 Baseline (69,876 offenses)</span>
        <span><i class="lou-swatch" style="background:var(--accent)"></i>2025 Update / Increase (70,336 offenses)</span>
        <span><i class="lou-swatch" style="background:#2fa356"></i>2025 Decrease</span>
        <span class="lou-hint">Hover any bar or point to inspect &middot; Click &#x2922; Expand on any card for full-width view</span>
      </div>

      <div id="lou-tip" role="status" aria-hidden="true"></div>

      <div class="lou-vgrid" id="lou-vgrid">

        <!-- CARD 1: TEMPERATURE -->
        <article class="lou-vcard" id="lou-card-1">
          <div class="lou-vcard-top">
            <span class="lou-vkicker">01 &middot; Temperature vs. Crime</span>
            <div class="lou-vtop-right">
              <span class="lou-vpill same">Consistent &middot; r = 0.51</span>
              <button type="button" class="lou-exp-btn" onclick="louToggleCard(this)">&#x2922; Expand</button>
            </div>
          </div>
          <h3>Hot 85&deg;F+ days drive +39% more daily crime than freezing days</h3>
          <div class="lou-vsvg-wrap">
            <svg class="lou-vsvg" viewBox="0 0 440 195" role="img" aria-label="Interactive bar chart of average daily offenses across five NOAA temperature bands in 2024 and 2025.">
              <line class="axis" x1="36" y1="155" x2="428" y2="155"/>
              <line class="axis" x1="36" y1="116" x2="428" y2="116" stroke-dasharray="2 3"/>
              <line class="axis" x1="36" y1="77" x2="428" y2="77" stroke-dasharray="2 3"/>
              <line class="axis" x1="36" y1="38" x2="428" y2="38" stroke-dasharray="2 3"/>
              <text class="muted" x="30" y="158" font-size="10" text-anchor="end">120</text>
              <text class="muted" x="30" y="119" font-size="10" text-anchor="end">150</text>
              <text class="muted" x="30" y="80" font-size="10" text-anchor="end">180</text>
              <text class="muted" x="30" y="41" font-size="10" text-anchor="end">210</text>

              <g class="lou-hit" tabindex="0" data-lbl="Freezing Days (&lt;32&deg;F)" data-v24="154.2/day (9d)" data-v25="151.6/day (21d)" data-delta="-1.7% YoY" data-note="Coldest days consistently record the lowest daily crime volume.">
                <rect class="hit-bg" x="44" y="28" width="62" height="160"/>
                <rect class="b24" x="52" y="110.5" width="22" height="44.5" rx="3"/>
                <rect class="b25" x="76" y="113.9" width="22" height="41.1" rx="3"/>
                <text class="muted" x="63" y="105" font-size="9.5" font-weight="600" text-anchor="middle">154</text>
                <text class="acc" x="87" y="108" font-size="9.5" font-weight="700" text-anchor="middle">152</text>
                <text x="75" y="172" font-size="10.5" font-weight="700" text-anchor="middle">&lt;32&deg;F</text>
                <text class="muted" x="75" y="184" font-size="9" text-anchor="middle">Freezing</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Cold Days (32&ndash;49&deg;F)" data-v24="172.6/day (48d)" data-v25="174.9/day (56d)" data-delta="+1.3% YoY" data-note="Stepping above freezing adds ~20+ offenses per day in both years.">
                <rect class="hit-bg" x="120" y="28" width="62" height="160"/>
                <rect class="b24" x="128" y="86.6" width="22" height="68.4" rx="3"/>
                <rect class="b25" x="152" y="83.6" width="22" height="71.4" rx="3"/>
                <text class="muted" x="139" y="81" font-size="9.5" font-weight="600" text-anchor="middle">173</text>
                <text class="acc" x="163" y="78" font-size="9.5" font-weight="700" text-anchor="middle">175</text>
                <text x="151" y="172" font-size="10.5" font-weight="700" text-anchor="middle">32&ndash;49&deg;F</text>
                <text class="muted" x="151" y="184" font-size="9" text-anchor="middle">Cold</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Mild Days (50&ndash;69&deg;F)" data-v24="181.3/day (99d)" data-v25="190.8/day (91d)" data-delta="+5.2% YoY" data-note="Spring and autumn mild days hover near the ~191/day annual mean.">
                <rect class="hit-bg" x="196" y="28" width="62" height="160"/>
                <rect class="b24" x="204" y="75.3" width="22" height="79.7" rx="3"/>
                <rect class="b25" x="228" y="63.0" width="22" height="92.0" rx="3"/>
                <text class="muted" x="215" y="70" font-size="9.5" font-weight="600" text-anchor="middle">181</text>
                <text class="acc" x="239" y="57" font-size="9.5" font-weight="700" text-anchor="middle">191</text>
                <text x="227" y="172" font-size="10.5" font-weight="700" text-anchor="middle">50&ndash;69&deg;F</text>
                <text class="muted" x="227" y="184" font-size="9" text-anchor="middle">Mild</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Warm Days (70&ndash;84&deg;F)" data-v24="196.4/day (118d)" data-v25="196.5/day (109d)" data-delta="+0.1% YoY" data-note="Identical daily average (196.4 vs 196.5/day) across both years.">
                <rect class="hit-bg" x="272" y="28" width="62" height="160"/>
                <rect class="b24" x="280" y="55.7" width="22" height="99.3" rx="3"/>
                <rect class="b25" x="304" y="55.5" width="22" height="99.5" rx="3"/>
                <text class="muted" x="291" y="50" font-size="9.5" font-weight="600" text-anchor="middle">196</text>
                <text class="acc" x="315" y="50" font-size="9.5" font-weight="700" text-anchor="middle">197</text>
                <text x="303" y="172" font-size="10.5" font-weight="700" text-anchor="middle">70&ndash;84&deg;F</text>
                <text class="muted" x="303" y="184" font-size="9" text-anchor="middle">Warm</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Hot Days (85&deg;F+)" data-v24="207.4/day (92d)" data-v25="211.2/day (88d)" data-delta="+39.3% vs Freezing" data-note="Days reaching 85&deg;F+ averaged 211.2 offenses/day in 2025 vs 151.6 below freezing.">
                <rect class="hit-bg" x="348" y="28" width="62" height="160"/>
                <rect class="b24" x="356" y="41.4" width="22" height="113.6" rx="3"/>
                <rect class="b25" x="380" y="36.4" width="22" height="118.6" rx="3"/>
                <text class="muted" x="367" y="36" font-size="9.5" font-weight="600" text-anchor="middle">207</text>
                <text class="acc" x="391" y="31" font-size="9.5" font-weight="700" text-anchor="middle">211</text>
                <text x="379" y="172" font-size="10.5" font-weight="700" text-anchor="middle">85&deg;F+</text>
                <text class="muted" x="379" y="184" font-size="9" text-anchor="middle">Hot (+39%)</text>
              </g>

              <path d="M 75 112 L 379 38" fill="none" stroke="var(--ink)" stroke-width="1.6" stroke-dasharray="5 4" opacity=".65" pointer-events="none"/>
              <text class="acc" x="230" y="20" font-size="10.5" font-weight="700" text-anchor="middle">+0.73 to +0.76 offenses per +1&deg;F (r = 0.514 &amp; 0.511)</text>
            </svg>
          </div>
          <div class="lou-readout" data-default="NOAA daily high temperature explained ~26% of daily crime variance in both 2024 and 2025.">
            <span>NOAA daily high temperature explained ~26% of daily crime variance in both 2024 and 2025.</span>
          </div>
        </article>

        <!-- CARD 2: FULL MOON & RAIN MYTH -->
        <article class="lou-vcard" id="lou-card-2">
          <div class="lou-vcard-top">
            <span class="lou-vkicker">02 &middot; Lunar &amp; Rain Effect</span>
            <div class="lou-vtop-right">
              <span class="lou-vpill same">Myth Debunked</span>
              <button type="button" class="lou-exp-btn" onclick="louToggleCard(this)">&#x2922; Expand</button>
            </div>
          </div>
          <h3>Full moons (-5.9%) and rainy days (-4.7%) don&rsquo;t spike crime</h3>
          <div class="lou-vsvg-wrap">
            <svg class="lou-vsvg" viewBox="0 0 440 195" role="img" aria-label="Horizontal comparison chart showing full-moon days and rainy days sit near or slightly below the 192 offenses per day annual baseline.">
              <line class="dash-base" x1="375" y1="22" x2="375" y2="178"/>
              <text class="muted" x="375" y="15" font-size="9.5" font-weight="700" text-anchor="middle">~192/day avg</text>

              <g class="lou-hit" tabindex="0" data-lbl="2024 Full Moon Days (12 dates)" data-v24="193.7/day (Full Moon)" data-v25="190.8/day (Other 354d)" data-delta="+1.5% (Noise)" data-note="No statistically significant difference between full moons and normal days in 2024.">
                <rect class="hit-bg" x="8" y="27" width="426" height="34"/>
                <text x="138" y="44" font-size="10.5" font-weight="700" text-anchor="end">2024 Full Moon (12d)</text>
                <text class="muted" x="138" y="56" font-size="9" text-anchor="end">vs. 354 other days (190.8)</text>
                <rect class="b24" x="145" y="34" width="232.4" height="18" rx="3"/>
                <text x="383" y="47" font-size="10" font-weight="700">193.7/d (+1.5%)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="2025 Full Moon Days (12 dates)" data-v24="193.1/day (Other 353d)" data-v25="181.8/day (Full Moon)" data-delta="-5.9% Lower" data-note="In 2025, full-moon days actually averaged 11.3 fewer offenses per day than non-full-moon days.">
                <rect class="hit-bg" x="8" y="67" width="426" height="34"/>
                <text x="138" y="84" font-size="10.5" font-weight="700" text-anchor="end">2025 Full Moon (12d)</text>
                <text class="muted" x="138" y="96" font-size="9" text-anchor="end">vs. 353 other days (193.1)</text>
                <rect class="bgrn" x="145" y="74" width="218.1" height="18" rx="3"/>
                <text class="grn" x="369" y="87" font-size="10" font-weight="700">181.8/d (-5.9%)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Rainy Days (&ge;0.1&Prime; Precipitation)" data-v24="189.8/day (94 rainy d)" data-v25="185.8/day (90 rainy d)" data-delta="-4.7% vs Dry" data-note="Rain alone barely suppresses crime unless combined with sub-freezing ice or snow.">
                <rect class="hit-bg" x="8" y="107" width="426" height="34"/>
                <text x="138" y="124" font-size="10.5" font-weight="700" text-anchor="end">2025 Rainy (&ge;0.1&Prime;, 90d)</text>
                <text class="muted" x="138" y="136" font-size="9" text-anchor="end">vs. 275 dry days (195.0)</text>
                <rect class="b24" x="145" y="114" width="223.0" height="18" rx="3"/>
                <text class="muted" x="374" y="127" font-size="10" font-weight="700">185.8/d (-4.7%)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Hot Days (85&deg;F+ Contrast)" data-v24="207.4/day (92 hot d)" data-v25="211.2/day (88 hot d)" data-delta="+39.3% vs Freezing" data-note="Unlike moon phase or rain, high temperature strongly and reliably lifts daily crime.">
                <rect class="hit-bg" x="8" y="147" width="426" height="34"/>
                <text x="138" y="164" font-size="10.5" font-weight="700" text-anchor="end">2025 Hot (85&deg;F+, 88d)</text>
                <text class="muted" x="138" y="176" font-size="9" text-anchor="end">vs. 21 freezing days (151.6)</text>
                <rect class="b25" x="145" y="154" width="253.4" height="18" rx="3"/>
                <text class="acc" x="403" y="167" font-size="10" font-weight="700">211.2/d</text>
              </g>
            </svg>
          </div>
          <div class="lou-readout" data-default="Across all 24 full moons in 2024–2025, full-moon days averaged 187.7/day vs. 191.9/day on other days.">
            <span>Across all 24 full moons in 2024&ndash;2025, full-moon days averaged 187.7/day vs. 191.9/day on other days.</span>
          </div>
        </article>

        <!-- CARD 3: DIVERGING OFFENSE & VENUE SHIFTS -->
        <article class="lou-vcard" id="lou-card-3">
          <div class="lou-vcard-top">
            <span class="lou-vkicker">03 &middot; Offense &amp; Venue Mix</span>
            <div class="lou-vtop-right">
              <span class="lou-vpill shift">Major Structural Shift</span>
              <button type="button" class="lou-exp-btn" onclick="louToggleCard(this)">&#x2922; Expand</button>
            </div>
          </div>
          <h3>Auto theft &amp; homicide plunged; retail shoplifting surged</h3>
          <div class="lou-vsvg-wrap">
            <svg class="lou-vsvg" viewBox="0 0 440 205" role="img" aria-label="Diverging bar chart of 2024 to 2025 percentage changes across major crime and location categories.">
              <line class="axis" x1="215" y1="18" x2="215" y2="198" stroke-width="1.5"/>
              <text class="grn" x="145" y="13" font-size="9.5" font-weight="700" text-anchor="middle">&larr; 2025 Decreases</text>
              <text class="acc" x="295" y="13" font-size="9.5" font-weight="700" text-anchor="middle">2025 Increases &rarr;</text>

              <g class="lou-hit" tabindex="0" data-lbl="1 Homicide (Offense)" data-v24="153 offenses" data-v25="113 offenses" data-delta="-40 (-26.1%)" data-note="Criminal homicide offenses dropped 26.1% year over year in 2025.">
                <rect class="hit-bg" x="10" y="19" width="420" height="19"/>
                <rect class="bgrn" x="157" y="22" width="58" height="14" rx="2"/>
                <text x="152" y="33" font-size="9.5" font-weight="700" text-anchor="end">Homicide -26.1%</text>
                <text class="muted" x="221" y="33" font-size="9">153 &rarr; 113 (-40)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="14 Auto Theft (Offense)" data-v24="5,769 offenses" data-v25="4,608 offenses" data-delta="-1,161 (-20.1%)" data-note="Largest volume drop in 2025 as the 2023–2024 Kia/Hyundai theft wave cooled.">
                <rect class="hit-bg" x="10" y="39" width="420" height="19"/>
                <rect class="bgrn" x="170" y="42" width="45" height="14" rx="2"/>
                <text x="165" y="53" font-size="9.5" font-weight="700" text-anchor="end">Auto Theft -20.1%</text>
                <text class="muted" x="221" y="53" font-size="9">5,769 &rarr; 4,608 (-1,161)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="8 Robbery (Offense)" data-v24="971 offenses" data-v25="792 offenses" data-delta="-179 (-18.4%)" data-note="Street and commercial robberies declined by 179 offenses in 2025.">
                <rect class="hit-bg" x="10" y="59" width="420" height="19"/>
                <rect class="bgrn" x="174" y="62" width="41" height="14" rx="2"/>
                <text x="169" y="73" font-size="9.5" font-weight="700" text-anchor="end">Robbery -18.4%</text>
                <text class="muted" x="221" y="73" font-size="9">971 &rarr; 792 (-179)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Parking Lots &amp; Garages (Venue)" data-v24="7,900 offenses" data-v25="6,963 offenses" data-delta="-937 (-11.9%)" data-note="Mirrors the 20% drop in vehicle thefts and 20% drop in Downtown 40202.">
                <rect class="hit-bg" x="10" y="79" width="420" height="19"/>
                <rect class="bgrn" x="188" y="82" width="27" height="14" rx="2"/>
                <text x="183" y="93" font-size="9.5" font-weight="700" text-anchor="end">Parking Lots -11.9%</text>
                <text class="muted" x="221" y="93" font-size="9">7,900 &rarr; 6,963 (-937)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="13 Burglary (Offense)" data-v24="3,517 offenses" data-v25="3,113 offenses" data-delta="-404 (-11.5%)" data-note="Residential and commercial burglary reports dropped 11.5% in 2025.">
                <rect class="hit-bg" x="10" y="99" width="420" height="19"/>
                <rect class="bgrn" x="189" y="102" width="26" height="14" rx="2"/>
                <text x="184" y="113" font-size="9.5" font-weight="700" text-anchor="end">Burglary -11.5%</text>
                <text class="muted" x="221" y="113" font-size="9">3,517 &rarr; 3,113 (-404)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="34 Narcotics &amp; 35 Equip (Offense)" data-v24="3,658 offenses" data-v25="4,444 offenses" data-delta="+786 (+21.5%)" data-note="Reflects higher proactive drug enforcement and seizures in 2025.">
                <rect class="hit-bg" x="10" y="119" width="420" height="19"/>
                <rect class="b25" x="215" y="122" width="48" height="14" rx="2"/>
                <text class="muted" x="209" y="133" font-size="9" text-anchor="end">3,658 &rarr; 4,444 (+786)</text>
                <text class="acc" x="268" y="133" font-size="9.5" font-weight="700">Narcotics +21.5%</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="18 Shoplifting (Offense)" data-v24="3,200 offenses" data-v25="4,112 offenses" data-delta="+912 (+28.5%)" data-note="Largest single offense increase in 2025 (+912 retail theft reports).">
                <rect class="hit-bg" x="10" y="139" width="420" height="19"/>
                <rect class="b25" x="215" y="142" width="63" height="14" rx="2"/>
                <text class="muted" x="209" y="153" font-size="9" text-anchor="end">3,200 &rarr; 4,112 (+912)</text>
                <text class="acc" x="283" y="153" font-size="9.5" font-weight="700">Shoplifting +28.5%</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="55 Trespassing (Offense)" data-v24="584 offenses" data-v25="817 offenses" data-delta="+233 (+39.9%)" data-note="Increased commercial and multifamily trespassing enforcement.">
                <rect class="hit-bg" x="10" y="159" width="420" height="19"/>
                <rect class="b25" x="215" y="162" width="88" height="14" rx="2"/>
                <text class="muted" x="209" y="173" font-size="9" text-anchor="end">584 &rarr; 817 (+233)</text>
                <text class="acc" x="308" y="173" font-size="9.5" font-weight="700">Trespassing +39.9%</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Grocery &amp; Supermarkets (Venue)" data-v24="818 offenses" data-v25="1,420 offenses" data-delta="+602 (+73.6%)" data-note="Driven by retail shoplifting; department/discount stores also rose +19.6%.">
                <rect class="hit-bg" x="10" y="179" width="420" height="19"/>
                <rect class="b25" x="215" y="182" width="135" height="14" rx="2"/>
                <text class="muted" x="209" y="193" font-size="9" text-anchor="end">818 &rarr; 1,420 (+602)</text>
                <text class="acc" x="355" y="193" font-size="9.5" font-weight="700">Grocery +73.6%</text>
              </g>
            </svg>
          </div>
          <div class="lou-readout" data-default="Total volume was flat (+0.7%), but vehicle and violent crime fell while retail and drug reports rose.">
            <span>Total volume was flat (+0.7%), but vehicle and violent crime fell while retail and drug reports rose.</span>
          </div>
        </article>

        <!-- CARD 4: SEASONALITY & DAY OF WEEK -->
        <article class="lou-vcard" id="lou-card-4">
          <div class="lou-vcard-top">
            <span class="lou-vkicker">04 &middot; Seasonality &amp; Day of Week</span>
            <div class="lou-vtop-right">
              <span class="lou-vpill shift">Mon &rarr; Fri/Sat Shift</span>
              <button type="button" class="lou-exp-btn" onclick="louToggleCard(this)">&#x2922; Expand</button>
            </div>
          </div>
          <h3>Q3 summer peak held; busiest day shifted from Monday to weekend</h3>
          <div class="lou-vsvg-wrap">
            <svg class="lou-vsvg" viewBox="0 0 440 195" role="img" aria-label="Left: 12-month curve peaking in July and August in both years. Right: Day of week bars showing Monday #1 in 2024 shifting to Saturday #1 and Friday #2 in 2025.">
              <line class="axis" x1="224" y1="15" x2="224" y2="182"/>

              <text x="114" y="16" font-size="10" font-weight="700" text-anchor="middle">Monthly Curve (Q3 Peak)</text>
              <line class="axis" x1="18" y1="145" x2="210" y2="145"/>
              <polyline class="line-24" fill="none" stroke="var(--ink-soft)" stroke-width="2" stroke-dasharray="4 3" pointer-events="none"
                points="20,100 37,115 54,97 71,94 88,47 105,62 122,43 139,45 156,75 173,77 190,98 207,95"/>
              <polyline class="line-25" fill="none" stroke="var(--accent)" stroke-width="2.4" pointer-events="none"
                points="20,120 37,129 54,84 71,79 88,51 105,61 122,38 139,41 156,68 173,81 190,70 207,101"/>

              <g class="lou-hit" tabindex="0" data-lbl="Q1 (Jan&ndash;Mar) &amp; Feb Trough" data-v24="15,958 (Feb: 5,094)" data-v25="15,539 (Feb: 4,814)" data-delta="-2.6% in Q1" data-note="February was the lowest month of the year in both 2024 (5,094) and 2025 (4,814).">
                <rect class="hit-bg" x="14" y="24" width="48" height="138"/>
                <circle cx="37" cy="129" r="4" class="b25"/>
                <text class="muted" x="45" y="141" font-size="8.5" text-anchor="middle">Feb Low (4.8k)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Q2 (Apr&ndash;Jun) Spring Warmup" data-v24="18,141 (May: 6,456)" data-v25="18,376 (May: 6,381)" data-delta="+1.3% in Q2" data-note="Crime climbs sharply each May as daily highs cross 75°F.">
                <rect class="hit-bg" x="63" y="24" width="48" height="138"/>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Q3 (Jul&ndash;Sep) Summer Peak" data-v24="18,953 (Jul: 6,534)" data-v25="19,245 (Jul: 6,631)" data-delta="+1.5% in Q3" data-note="July (#1) and August (#2) were the top two months in both 2024 and 2025.">
                <rect class="hit-bg" x="112" y="24" width="50" height="138"/>
                <circle cx="122" cy="38" r="4" class="b25"/>
                <text class="acc" x="126" y="32" font-size="9" font-weight="700" text-anchor="middle">Jul Peak (6.6k)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Q4 (Oct&ndash;Dec) Autumn/Winter" data-v24="16,824 (Nov: 5,448)" data-v25="17,176 (Nov: 5,996)" data-delta="+2.1% in Q4" data-note="Q4 cools down from summer highs; December 2025 dipped to 5,390.">
                <rect class="hit-bg" x="163" y="24" width="50" height="138"/>
              </g>

              <text class="muted" x="20" y="158" font-size="8.5" text-anchor="middle">J</text>
              <text class="muted" x="54" y="158" font-size="8.5" text-anchor="middle">M</text>
              <text class="muted" x="88" y="158" font-size="8.5" text-anchor="middle">M</text>
              <text class="acc" x="122" y="158" font-size="8.5" font-weight="700" text-anchor="middle">J</text>
              <text class="muted" x="156" y="158" font-size="8.5" text-anchor="middle">S</text>
              <text class="muted" x="190" y="158" font-size="8.5" text-anchor="middle">N</text>
              <text class="muted" x="114" y="176" font-size="9" text-anchor="middle">Q3: 18,953 (&rsquo;24) &middot; 19,245 (&rsquo;25)</text>

              <text x="334" y="16" font-size="10" font-weight="700" text-anchor="middle">Day of Week (2024 vs. 2025)</text>
              <line class="axis" x1="234" y1="145" x2="434" y2="145"/>

              <g class="lou-hit" tabindex="0" data-lbl="Sunday" data-v24="10,055 (#3)" data-v25="10,309 (#3)" data-delta="+2.5% YoY" data-note="Sunday stayed the 3rd-busiest day of the week in both years.">
                <rect class="hit-bg" x="235" y="26" width="25" height="136"/>
                <rect class="b24" x="238" y="71" width="9" height="74" rx="2"/><rect class="b25" x="248" y="53" width="9" height="92" rx="2"/>
                <text class="muted" x="247" y="158" font-size="8.5" text-anchor="middle">Sun</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Monday (#1 in 2024 &rarr; #4 in 2025)" data-v24="10,519 (#1)" data-v25="9,984 (#4)" data-delta="-5.1% YoY" data-note="Monday led 2024 (helped by 53 leap-year Mondays) before dropping to #4 in 2025.">
                <rect class="hit-bg" x="263" y="26" width="25" height="136"/>
                <rect class="b24" x="266" y="39" width="9" height="106" rx="2"/><rect class="b25" x="276" y="76" width="9" height="69" rx="2"/>
                <text x="270" y="34" font-size="8" font-weight="700" text-anchor="middle">&rsquo;24 #1</text>
                <text x="275" y="158" font-size="8.5" font-weight="700" text-anchor="middle">Mon</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Tuesday" data-v24="9,803 (#5)" data-v25="9,790 (#6)" data-delta="-0.1% YoY" data-note="Tuesday volume was virtually identical across both years.">
                <rect class="hit-bg" x="291" y="26" width="25" height="136"/>
                <rect class="b24" x="294" y="89" width="9" height="56" rx="2"/><rect class="b25" x="304" y="90" width="9" height="55" rx="2"/>
                <text class="muted" x="303" y="158" font-size="8.5" text-anchor="middle">Tue</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Wednesday" data-v24="9,522 (#7 Lowest)" data-v25="9,900 (#5)" data-delta="+4.0% YoY" data-note="Wednesday was the quietest day in 2024 before edging up in 2025.">
                <rect class="hit-bg" x="319" y="26" width="25" height="136"/>
                <rect class="b24" x="322" y="108" width="9" height="37" rx="2"/><rect class="b25" x="332" y="82" width="9" height="63" rx="2"/>
                <text class="muted" x="331" y="158" font-size="8.5" text-anchor="middle">Wed</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Thursday" data-v24="9,660 (#6)" data-v25="9,509 (#7 Lowest)" data-delta="-1.6% YoY" data-note="Thursday was the quietest day of the week in 2025 (9,509 offenses).">
                <rect class="hit-bg" x="347" y="26" width="25" height="136"/>
                <rect class="b24" x="350" y="99" width="9" height="46" rx="2"/><rect class="b25" x="360" y="109" width="9" height="36" rx="2"/>
                <text class="muted" x="359" y="158" font-size="8.5" text-anchor="middle">Thu</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Friday (#4 in 2024 &rarr; #2 in 2025)" data-v24="9,941 (#4)" data-v25="10,398 (#2)" data-delta="+4.6% YoY" data-note="Friday jumped +457 offenses to become the #2 busiest day in 2025.">
                <rect class="hit-bg" x="375" y="26" width="25" height="136"/>
                <rect class="b24" x="378" y="79" width="9" height="66" rx="2"/><rect class="b25" x="388" y="47" width="9" height="98" rx="2"/>
                <text class="acc" x="387" y="158" font-size="8.5" font-weight="700" text-anchor="middle">Fri</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Saturday (#2 in 2024 &rarr; #1 in 2025)" data-v24="10,376 (#2)" data-v25="10,446 (#1)" data-delta="+0.7% YoY" data-note="Saturday took the #1 spot in 2025 with 10,446 offenses (200.9/day).">
                <rect class="hit-bg" x="403" y="26" width="25" height="136"/>
                <rect class="b24" x="406" y="49" width="9" height="96" rx="2"/><rect class="b25" x="416" y="44" width="9" height="101" rx="2"/>
                <text class="acc" x="415" y="38" font-size="8" font-weight="700" text-anchor="middle">&rsquo;25 #1&ndash;2</text>
                <text class="acc" x="415" y="158" font-size="8.5" font-weight="700" text-anchor="middle">Sat</text>
              </g>

              <text class="muted" x="334" y="176" font-size="9" text-anchor="middle">Sat (10,446) &amp; Fri (10,398) led 2025</text>
            </svg>
          </div>
          <div class="lou-readout" data-default="July and August were #1 and #2 in both years, while 2025 volume shifted from Monday (-5.1%) to Friday/Saturday.">
            <span>July and August were #1 and #2 in both years, while 2025 volume shifted from Monday (-5.1%) to Friday/Saturday.</span>
          </div>
        </article>

        <!-- CARD 5: GEOGRAPHY (ZIPS & DIVISIONS) -->
        <article class="lou-vcard" id="lou-card-5">
          <div class="lou-vcard-top">
            <span class="lou-vkicker">05 &middot; Geography &amp; ZIP Codes</span>
            <div class="lou-vtop-right">
              <span class="lou-vpill low">Downtown -20.2%</span>
              <button type="button" class="lou-exp-btn" onclick="louToggleCard(this)">&#x2922; Expand</button>
            </div>
          </div>
          <h3>Top 4 ZIPs held steady; Downtown dropped -20.2% while outer ring grew</h3>
          <div class="lou-vsvg-wrap">
            <svg class="lou-vsvg" viewBox="0 0 440 195" role="img" aria-label="Horizontal bar comparison of top Louisville ZIP codes and LMPD 8th Division.">
              <g class="lou-hit" tabindex="0" data-lbl="ZIP 40203 (Old Louisville / Russell)" data-v24="4,933 (#1)" data-v25="4,929 (#1)" data-delta="-4 (-0.1%)" data-note="Highest-volume ZIP code in both 2024 and 2025, virtually unchanged.">
                <rect class="hit-bg" x="8" y="14" width="424" height="20"/>
                <text x="136" y="28" font-size="9.5" font-weight="700" text-anchor="end">40203 (Old Lou / West)</text>
                <rect class="b25" x="142" y="17" width="197" height="14" rx="2"/>
                <text x="345" y="28" font-size="9" font-weight="600">4,929 (-0.1%)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="ZIP 40211 (Shawnee / Chickasaw)" data-v24="4,772 (#2)" data-v25="4,889 (#2)" data-delta="+117 (+2.5%)" data-note="Second-highest ZIP code in both years, located in West Louisville.">
                <rect class="hit-bg" x="8" y="36" width="424" height="20"/>
                <text x="136" y="50" font-size="9.5" font-weight="700" text-anchor="end">40211 (Shawnee / West)</text>
                <rect class="b25" x="142" y="39" width="196" height="14" rx="2"/>
                <text x="344" y="50" font-size="9" font-weight="600">4,889 (+2.5%)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="ZIP 40214 (Iroquois / Beechmont)" data-v24="4,623 (#3)" data-v25="4,866 (#3)" data-delta="+243 (+5.3%)" data-note="Held #3 rank in both years; part of LMPD 3rd &amp; 4th Divisions.">
                <rect class="hit-bg" x="8" y="58" width="424" height="20"/>
                <text x="136" y="72" font-size="9.5" font-weight="700" text-anchor="end">40214 (Iroquois / South)</text>
                <rect class="b25" x="142" y="61" width="195" height="14" rx="2"/>
                <text x="343" y="72" font-size="9" font-weight="600">4,866 (+5.3%)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="ZIP 40219 (Okolona / Highview)" data-v24="4,618 (#4)" data-v25="4,796 (#4)" data-delta="+178 (+3.9%)" data-note="Held #4 rank in both years; top 4 ZIPs account for 27% of all Louisville crime.">
                <rect class="hit-bg" x="8" y="80" width="424" height="20"/>
                <text x="136" y="94" font-size="9.5" font-weight="700" text-anchor="end">40219 (Okolona / South)</text>
                <rect class="b25" x="142" y="83" width="192" height="14" rx="2"/>
                <text x="340" y="94" font-size="9" font-weight="600">4,796 (+3.9%)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="ZIP 40215 (Taylor Berry / Jacobs)" data-v24="3,798 (#7)" data-v25="4,040 (#5)" data-delta="+242 (+6.4%)" data-note="Rose from #7 in 2024 to #5 in 2025 as Downtown 40202 dropped.">
                <rect class="hit-bg" x="8" y="102" width="424" height="20"/>
                <text x="136" y="116" font-size="9.5" font-weight="700" text-anchor="end">40215 (Taylor Berry)</text>
                <rect class="b25" x="142" y="105" width="162" height="14" rx="2"/>
                <text class="acc" x="310" y="116" font-size="9" font-weight="700">4,040 (+6.4%)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="ZIP 40202 (Downtown / Central Business District)" data-v24="4,078 (#5)" data-v25="3,256 (#7)" data-delta="-822 (-20.2%)" data-note="Largest geographic drop in the city (-822 offenses), falling from #5 to #7.">
                <rect class="hit-bg" x="8" y="124" width="424" height="20"/>
                <text x="136" y="138" font-size="9.5" font-weight="700" text-anchor="end">40202 (Downtown CBD)</text>
                <rect class="b24" x="142" y="127" width="163" height="14" rx="2"/>
                <rect class="bgrn" x="142" y="127" width="130" height="14" rx="2"/>
                <text class="grn" x="311" y="138" font-size="9" font-weight="700">3,256 (-20.2% / -822)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="ZIP 40272 (Valley Station)" data-v24="2,900 (#10)" data-v25="3,234 (#8)" data-delta="+334 (+11.5%)" data-note="Fastest-growing top-10 ZIP code (+11.5% YoY) in Southwest Jefferson County.">
                <rect class="hit-bg" x="8" y="146" width="424" height="20"/>
                <text x="136" y="160" font-size="9.5" font-weight="700" text-anchor="end">40272 (Valley Station)</text>
                <rect class="b25" x="142" y="149" width="129" height="14" rx="2"/>
                <text class="acc" x="277" y="160" font-size="9" font-weight="700">3,234 (+11.5% / +334)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="LMPD 8th Division (East End / Middletown)" data-v24="4,632 offenses" data-v25="5,191 offenses" data-delta="+559 (+12.1%)" data-note="Largest percentage increase among all 8 LMPD patrol divisions.">
                <rect class="hit-bg" x="8" y="168" width="424" height="20"/>
                <text x="136" y="182" font-size="9.5" font-weight="700" text-anchor="end">LMPD 8th Div (East End)</text>
                <rect class="b25" x="142" y="171" width="208" height="14" rx="2"/>
                <text class="acc" x="355" y="182" font-size="9" font-weight="700">5,191 (+12.1%)</text>
              </g>
            </svg>
          </div>
          <div class="lou-readout" data-default="The top 4 ZIPs kept 27% of all crime in the exact same order, while Downtown fell from #5 to #7.">
            <span>The top 4 ZIPs kept 27% of all crime in the exact same order, while Downtown fell from #5 to #7.</span>
          </div>
        </article>

        <!-- CARD 6: EXTREME LOWS & 1ST-OF-MONTH SPIKE -->
        <article class="lou-vcard" id="lou-card-6">
          <div class="lou-vcard-top">
            <span class="lou-vkicker">06 &middot; Daily Extremes &amp; Lag</span>
            <div class="lou-vtop-right">
              <span class="lou-vpill low">Jan 6 Blizzard: 88</span>
              <button type="button" class="lou-exp-btn" onclick="louToggleCard(this)">&#x2922; Expand</button>
            </div>
          </div>
          <h3>Blizzard set a 2-year low (88); delayed reports spike the 1st of month</h3>
          <div class="lou-vsvg-wrap">
            <svg class="lou-vsvg" viewBox="0 0 440 195" role="img" aria-label="Comparison of extreme low and high days against the 192 per day average.">
              <line class="dash-base" x1="316" y1="18" x2="316" y2="188"/>
              <text class="muted" x="316" y="13" font-size="9" font-weight="700" text-anchor="middle">192/day avg</text>

              <g class="lou-hit" tabindex="0" data-lbl="Jan 6, 2025 Winter Storm &amp; Ice" data-v24="182 (Jan 15 '24 storm)" data-v25="88 offenses (Jan 6 '25)" data-delta="-54% vs Avg" data-note="7+ inches of snow and ice shut down Louisville, setting the single lowest day of 2024–2025.">
                <rect class="hit-bg" x="8" y="19" width="424" height="21"/>
                <text x="144" y="34" font-size="9.5" font-weight="700" text-anchor="end">Jan 6, 2025 (7&Prime;+ Snow/Ice)</text>
                <rect class="bgrn" x="150" y="23" width="76" height="14" rx="2"/>
                <text class="grn" x="232" y="34" font-size="9.5" font-weight="700">88 (-54% &middot; 2-yr low)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Thanksgiving Day (Nov 28 '24 / Nov 27 '25)" data-v24="112 offenses (#1 low '24)" data-v25="150 offenses" data-delta="-41% / -22% vs Avg" data-note="Lowest single day of 2024 (112) and well below average again in 2025 (150).">
                <rect class="hit-bg" x="8" y="43" width="424" height="21"/>
                <text x="144" y="58" font-size="9.5" font-weight="700" text-anchor="end">Thanksgiving &rsquo;24 / &rsquo;25</text>
                <rect class="bgrn" x="150" y="47" width="97" height="14" rx="2"/>
                <text class="grn" x="253" y="58" font-size="9.5" font-weight="700">112 (&rsquo;24) &middot; 150 (&rsquo;25)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Christmas Day (Dec 25)" data-v24="184 offenses" data-v25="133 offenses (#5 low '25)" data-delta="-31% vs '25 Avg" data-note="Christmas Day 2025 dropped to 133 offenses (104 unique incidents).">
                <rect class="hit-bg" x="8" y="67" width="424" height="21"/>
                <text x="144" y="82" font-size="9.5" font-weight="700" text-anchor="end">Christmas Day &rsquo;25 / &rsquo;24</text>
                <rect class="bgrn" x="150" y="71" width="115" height="14" rx="2"/>
                <text class="grn" x="271" y="82" font-size="9.5" font-weight="700">133 (&rsquo;25) &middot; 184 (&rsquo;24)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Days 2&ndash;31 Daily Average" data-v24="189.9/day (3.5% &gt;7d lag)" data-v25="191.1/day (3.9% &gt;7d lag)" data-delta="+0.6% YoY" data-note="Normal calendar days (excluding the 1st of the month) average ~190–191 offenses/day.">
                <rect class="hit-bg" x="8" y="93" width="424" height="21"/>
                <text x="144" y="108" font-size="9.5" font-weight="700" text-anchor="end">Days 2&ndash;31 Avg (2025)</text>
                <rect class="b24" x="150" y="97" width="166" height="14" rx="2"/>
                <text class="muted" x="322" y="108" font-size="9" font-weight="600">191.1/d (3.9% &gt;7d lag)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="1st of the Month Average (12 dates/yr)" data-v24="221.2/day (10.6% &gt;7d lag)" data-v25="241.1/day (13.0% &gt;7d lag)" data-delta="+26.2% vs Days 2-31" data-note="Long-window crimes (fraud, identity theft) default to the 1st of the month when reported later.">
                <rect class="hit-bg" x="8" y="119" width="424" height="21"/>
                <text x="144" y="134" font-size="9.5" font-weight="700" text-anchor="end">1st of Month Avg (2025)</text>
                <rect class="b25" x="150" y="123" width="209" height="14" rx="2"/>
                <text class="acc" x="364" y="134" font-size="9" font-weight="700">241.1/d (+26%)</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="Highest Non-1st Days (Jul 22 '24 / May 30 '25)" data-v24="269 (July 22, 2024)" data-v25="272 (May 30, 2025)" data-delta="+42% vs Avg" data-note="Peak single days not falling on the 1st of a month in 2024 and 2025.">
                <rect class="hit-bg" x="8" y="143" width="424" height="21"/>
                <text x="144" y="158" font-size="9.5" font-weight="700" text-anchor="end">Jul 22 &rsquo;24 / May 30 &rsquo;25</text>
                <rect class="b25" x="150" y="147" width="236" height="14" rx="2"/>
                <text class="acc" x="391" y="158" font-size="9" font-weight="700">269 / 272</text>
              </g>

              <g class="lou-hit" tabindex="0" data-lbl="2025 Summer 1st-of-Month Peaks" data-v24="253 (May 1) / 250 (Jun 1)" data-v25="276 (Jul 1) / 274 (Aug 1)" data-delta="Top Raw Dates" data-note="Combines summer heat with 1st-of-the-month retroactive reporting.">
                <rect class="hit-bg" x="8" y="167" width="424" height="21"/>
                <text x="144" y="182" font-size="9.5" font-weight="700" text-anchor="end">Jul 1 / Aug 1 / Jun 1 &rsquo;25</text>
                <rect class="b25" x="150" y="171" width="239" height="14" rx="2"/>
                <text class="acc" x="394" y="182" font-size="9" font-weight="700">276 / 274 / 273</text>
              </g>
            </svg>
          </div>
          <div class="lou-readout" data-default="13.0% of offenses dated on the 1st were reported >7 days later (vs. 3.9% on other days), inflating 1st-of-month counts.">
            <span>13.0% of offenses dated on the 1st were reported &gt;7 days later (vs. 3.9% on other days), inflating 1st-of-month counts.</span>
          </div>
        </article>

      </div>

      <h2 style="margin-top:44px">2024 interactive Tableau workbook</h2>
      <p>Explore the original 2024 Tableau Public story and ZIP-code heat map below.</p>
{tableau("viz-lou", "Louisville_KY_Crime_Stats/LouisvilleCrime", "Louisville, KY Crime Info")}"""

LOU_SCRIPT = r"""
  <script>
    function louToggleCard(btn) {
      var card = btn.closest(".lou-vcard");
      var exp = card.classList.toggle("expanded");
      btn.innerHTML = exp ? "&#x2921; Collapse" : "&#x2922; Expand";
      if (exp) card.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
    function louToggleAllExpand() {
      var grid = document.getElementById("lou-vgrid");
      var btn = document.getElementById("lou-layout-btn");
      var full = grid.classList.toggle("full-mode");
      btn.classList.toggle("active", full);
      btn.innerHTML = full ? "&#x229E; 2-Column Grid" : "&#x2922; Expand All Charts";
      document.querySelectorAll(".lou-vcard").forEach(function (c) {
        c.classList.remove("expanded");
        var b = c.querySelector(".lou-exp-btn");
        if (b) b.innerHTML = "&#x2922; Expand";
      });
    }
    function louSetYear(yr, btn) {
      var grid = document.getElementById("lou-vgrid");
      grid.classList.remove("focus-2024", "focus-2025");
      if (yr === "2024") grid.classList.add("focus-2024");
      if (yr === "2025") grid.classList.add("focus-2025");
      document.querySelectorAll(".lou-controls [data-yr]").forEach(function (b) {
        b.classList.toggle("active", b === btn);
      });
    }
    (function () {
      var tip = document.getElementById("lou-tip");
      if (!tip) return;
      function showHit(hit, e) {
        var lbl = hit.getAttribute("data-lbl") || "";
        var v24 = hit.getAttribute("data-v24") || "";
        var v25 = hit.getAttribute("data-v25") || "";
        var dlt = hit.getAttribute("data-delta") || "";
        var note = hit.getAttribute("data-note") || "";
        tip.innerHTML =
          '<div class="t-head">' + lbl + '</div>' +
          '<div class="t-row"><span>2024:</span><b>' + v24 + '</b></div>' +
          '<div class="t-row"><span>2025:</span><b>' + v25 + '</b></div>' +
          '<div class="t-row"><span>Difference:</span><b>' + dlt + '</b></div>' +
          (note ? '<div class="t-note">' + note + '</div>' : '');
        tip.classList.add("show");
        var card = hit.closest(".lou-vcard");
        var ro = card ? card.querySelector(".lou-readout") : null;
        if (ro) {
          ro.innerHTML =
            '<strong>' + lbl + '</strong>' +
            '<span class="ro-badges">' +
              '<span class="ro-24">2024: ' + v24 + '</span>' +
              '<span class="ro-25">2025: ' + v25 + '</span>' +
              '<span class="ro-d">' + dlt + '</span>' +
            '</span>';
        }
        if (e && e.clientX) moveTip(e);
      }
      function moveTip(e) {
        var x = e.clientX + 16;
        var y = e.clientY + 16;
        if (x + 290 > window.innerWidth) x = e.clientX - 295;
        if (y + 140 > window.innerHeight) y = e.clientY - 140;
        tip.style.left = Math.max(8, x) + "px";
        tip.style.top = Math.max(8, y) + "px";
      }
      function hideHit(hit) {
        tip.classList.remove("show");
        var card = hit.closest(".lou-vcard");
        var ro = card ? card.querySelector(".lou-readout") : null;
        if (ro) {
          ro.innerHTML = '<span>' + (ro.getAttribute("data-default") || "") + '</span>';
        }
      }
      document.querySelectorAll(".lou-hit").forEach(function (hit) {
        hit.addEventListener("mouseenter", function (e) { showHit(hit, e); });
        hit.addEventListener("mousemove", moveTip);
        hit.addEventListener("mouseleave", function () { hideHit(hit); });
        hit.addEventListener("focus", function (e) { showHit(hit, e); });
        hit.addEventListener("blur", function () { hideHit(hit); });
      });
    })();
  </script>"""

detail_page(by["louisville-crime"],
  "Two-year comparison of 140,212 Louisville Metro Police Department (LMPD) incident reports (69,876 offenses in 2024 vs. 70,336 in 2025) paired with daily NOAA weather observations and lunar phases.",
  LOU_SECTIONS,
  extra_foot=LOU_SCRIPT + tableau_script("viz-lou"))

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
          <li><strong>+419%</strong><span>customer base expansion (+171% avg. ticket growth)</span></li>
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
          <p class="small">This early catalog work directly inspired two standalone tools on this site: the <a href="/projects/jobber-import-etl/">Vendor Price Sheet &rarr; Jobber Import ETL</a> pipeline and the <a href="/projects/chimney-planner/">Hearth Venting Planner</a>.</p>
        </section>

        <section>
          <h3>Instrument-driven field diagnostics &amp; SOPs</h3>
          <ul>
            <li><strong>Millivolt gas valve ohmmeter testing:</strong> Authored technician training decks standardizing multimeter resistance checks across Robertshaw &amp; SIT Electromagnet Power Units (<code>0&ndash;13 &Omega;</code> specification between EPU lead and TP terminal) and preventative pilot/spill-switch replacement rules to eliminate repeat callbacks.</li>
            <li><strong>Magnehelic differential pressure &amp; airflow telemetry:</strong> Built CDET dryer exhaust evaluation forms recording pre- and post-cleaning backpressure (<code>&le; 0.6&quot; Water Column</code>) and anemometer airflow velocity (<code>MPH</code>) at the appliance and exterior termination.</li>
            <li><strong>Time-critical chemical &amp; refractory SOPs:</strong> Documented step-by-step field runbooks for ChamberGuard and FireGuard ceramic resurfacing equipment, including a strict 2-minute pump-blockage recovery decision tree before refractory material cures in the line.</li>
            <li><strong>M&amp;A transition to a major local HVAC company:</strong> In 2022, packaged the customer book (+419% growth), brand assets, inventory/tooling assessments, and operational playbooks into a clean asset sale and 3-year management integration agreement with a major local HVAC company.</li>
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
            "Continued expanding the customer base while increasing trailing 12-month average ticket value by +171% vs. Year 1."
          ]
        },
        {
          title: "2022 &middot; +740% Exit Run-Rate (8.4x) &amp; Turnkey Acquisition",
          rev: "840 Index (+740% vs. Y1 / 8.4x)",
          gp: "54.0% Gross Margin",
          net: "100% Turnkey Asset Transfer",
          bullets: [
            "Reached an 8.4x annualized revenue run-rate (+740% over Year 1 baseline) with +419% customer base expansion over Year 1.",
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
  </main>""", noindex=True)
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


# Hand-curated notes for projects whose pages are mostly interactive widgets, where the text pulled from
# the page would be noisy. These replace the page text below for the assistant; keep them in step with
# the project page when its facts change.
NOTES_OVERRIDE = {
    'buffalo-trace-tracker': "Buffalo Trace Distillery rotates allocated bourbons (Blanton's, E.H. Taylor, Eagle Rare, Weller) at its Frankfort, KY Gift Shop each morning. I built a zero-dependency Python pipeline on GitHub Actions that polls the distillery during morning release windows, deduplicates state changes, dispatches instant mobile push and BCC email alerts, and streams the live JSON feed directly into the dashboard on davidcreason.com/projects/buffalo-trace-tracker/.",
    'louisville-crime': "Two-year comparison of 140,212 Louisville Metro Police Department (LMPD) incident reports (69,876 offenses across 57,246 unique incidents in 2024 vs. 70,336 offenses across 56,453 unique incidents in 2025, +0.7% YoY) paired with daily NOAA weather observations (station USC00154958) and lunar phases.\n\nKey 2024 vs. 2025 Findings:\n- Temperature Correlation (Consistent): r = 0.514 in 2024 (+0.73 offenses per +1°F) and r = 0.511 in 2025 (+0.76 offenses per +1°F). In 2025, daily offenses rose from 151.6/day below 32°F (154.2 in 2024) to 174.9/day at 32–49°F, 190.8/day at 50–69°F, 196.5/day at 70–84°F, and 211.2/day at 85°F+ (+39.3% over freezing).\n- Lunar & Rain Effect (Consistent — Myth Debunked): The 12 full-moon days averaged 193.7/day vs. 190.8/day in 2024 (+1.5%) and 181.8/day vs. 193.1/day in 2025 (-5.9%). Rainy days (>=0.1 in.) averaged 185.8/day vs. 195.0/day on dry days in 2025 (-4.7%).\n- Offense & Venue Mix (Major Shift): Auto theft fell -20.1% (5,769 → 4,608, -1,161), homicide fell -26.1% (153 → 113, -40), robbery fell -18.4% (971 → 792), burglary fell -11.5% (3,517 → 3,113), and parking lot/garage offenses fell -11.9% (7,900 → 6,963). Meanwhile, retail shoplifting surged +28.5% (3,200 → 4,112, +912), grocery/supermarket incidents rose +73.6% (818 → 1,420), narcotics rose +21.5% (3,658 → 4,444), and trespassing rose +39.9% (584 → 817).\n- Seasonality & Day of Week: Q3 led both years (18,953 in 2024; 19,245 in 2025), with July #1 (6,534 and 6,631) and February lowest (5,094 and 4,814). Busiest day of the week shifted from Monday in 2024 (10,519) to Saturday (10,446) and Friday (10,398) in 2025.\n- Geography: Top 4 ZIPs held steady in both years: 40203 (4,933 → 4,929), 40211 (4,772 → 4,889), 40214 (4,623 → 4,866), and 40219 (4,618 → 4,796). Downtown 40202 dropped -20.2% (4,078 → 3,256, #5 to #7), while outer-ring 40272 (+11.5%, 2,900 → 3,234) and LMPD 8th Division (+12.1%, 4,632 → 5,191) grew.\n- Daily Extremes & 1st-of-Month Lag: Jan 6, 2025 (7+ inch snow and ice storm) set a two-year low of 88 offenses (-54%), beating Thanksgiving (112 in 2024; 150 in 2025) and Christmas (133 in 2025). Raw peak dates in 2025 fell on July 1 (276), Aug 1 (274), and June 1 (273), followed by May 30 (272) — reflecting delayed reports that default to the 1st of the month (241.1/day avg on the 1st vs. 191.1/day on days 2–31; 13.0% reported >7 days later vs. 3.9%).",
    'crestwood-home-hearth': 'How I applied enterprise systems integration, multi-vendor ETL pipelines (4,533 SKUs), custom JavaScript/AJAX automation, 3D SketchUp CAD modeling, and parametric unit-economics engines to drive +740% annualized revenue expansion (63.6% peak gross margin) and a turnkey acquisition exit to a major local HVAC company.\n\nKey Growth & Percentage Highlights:\n- Revenue Expansion: +310% YoY growth in Year 2 (4.1x baseline), +68% YoY in Year 3 (+590% cumulative 3-year growth / 6.9x), reaching +740% (8.4x Year 1 baseline) annualized run-rate at acquisition exit in 2022.\n- Margin Performance: 61.3% Gross Margin in Year 1, 63.6% Peak Gross Margin and 24.7% Net Operating Margin in Year 2, and 53.6%-54.0% Gross Margin during multi-crew scaling in 2021-2022.\n- Customer & Ticket Velocity: +419% customer base expansion and +171% expansion in trailing 12-month average ticket value.\n- Interactive 3D CAD & Spatial Engineering Viewer: Includes a live 360-degree rotatable 3D parametric rig simulating Somfy RTS motorized louver pitch (0-135 deg) and Hammerhead motorized ZIP screen deployment (0-100%), paired with 6 production SketchUp (.skp) engineering blueprint exports.\n- 4,533-SKU Multi-Vendor ETL & Custom JS/AJAX Automation: Normalized 15+ manufacturer catalogs into Jobber CRM, QuickBooks Online, and Wix, and authored browser-console AJAX scripts (DELETE /work_items/{id}) to purge obsolete catalog items in seconds.\n- Parametric Margin Calculators: Enforced ~29.2% net operating margin after sales commission on custom screens and 1.0x-3.5x hourly yield indexes across 26 standardized service lines.\n\nOpen full screen on Tableau Public →',
}


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
        f"{NOTES_OVERRIDE.get(_p['slug']) or _page_text('/projects/' + _p['slug'] + '/')}\n"
    )
write("assets/projects.txt", "\n".join(_notes))

# ---- Search engines: sitemap.xml and robots.txt ----
# Every page built with page() is listed unless it was built with noindex=True. The ScopeOut demo is a
# standalone app outside build.py, and so is the Buffalo Trace tracker page, so they're added by hand. Old Google Sites redirects stay out.
_urls = SITEMAP + ["/projects/buffalo-trace-tracker/", "/scopeout/"]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in _urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nDisallow: /scopeout-mailer/\n\nSitemap: {SITE}/sitemap.xml\n")

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
