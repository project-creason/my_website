# Renders /resume/ from the parsed resume PDF (RESUME, built in build.py).
# Do not hand-edit resume content here: replace assets/David_Creason_Resume.pdf and rebuild.
# Loaded by build.py and shares its helpers: page, e, PROFILE, RESUME, PHONE.


def _jobs(items):
    out = []
    for j in items:
        bullets = "".join(f"<li>{e(b)}</li>" for b in j["bullets"])
        place = f" &middot; {e(j['place'])}" if j.get("place") else ""
        out.append(f"""        <article class="job">
          <header>
            <div><h3>{e(j['title'])}</h3><p class="org">{e(j['org'])}{place}</p></div>
            <p class="dates">{e(j['dates'])}</p>
          </header>
          <ul>{bullets}</ul>
        </article>""")
    return "\n".join(out)


def _contact_html(parts):
    out = []
    for p in parts:
        if "@" in p:
            # Email stays in the downloadable PDF only; the page links to the contact form.
            out.append('<a href="/contact/#form">Send a message</a>')
        elif "linkedin" in p.lower() or p.startswith("http") or "github.com" in p.lower():
            href = p if p.startswith("http") else "https://" + p
            out.append(f'<a href="{e(href)}" rel="noopener" target="_blank">{e(p)}</a>')
        else:
            out.append(e(p))
    return " &middot; ".join(out)


def _section(title, body):
    return f"""      <section class="r-section">
        <h2>{title}</h2>
{body}
      </section>"""


_sections = []
if RESUME["summary"]:
    _sections.append(_section("Professional summary", f'        <p class="lede">{e(RESUME["summary"])}</p>'))
if RESUME["skills"]:
    _skills = "\n".join(
        f"""          <div>{f'<h3>{e(cat)}</h3>' if cat else ''}<ul class="tags">{''.join(f'<li>{e(x)}</li>' for x in items)}</ul></div>"""
        for cat, items in RESUME["skills"]
    )
    _sections.append(_section("Core competencies &amp; technical skills", f'        <div class="skill-grid">\n{_skills}\n        </div>'))
if RESUME["experience"]:
    _sections.append(_section("Professional experience", _jobs(RESUME["experience"])))
if RESUME["education"]:
    _edu = "".join(f"<li><strong>{e(d)}</strong><span>{e(s)}</span></li>" for d, s in RESUME["education"])
    _sections.append(_section("Education &amp; certifications", f'        <ul class="edu">{_edu}</ul>'))
for _o in RESUME["other"]:
    _body = []
    if _o["paragraph"]:
        _body.append(f'        <p>{e(_o["paragraph"])}</p>')
    if _o["entries"]:
        _body.append(_jobs(_o["entries"]))
    if _o["bullets"]:
        _body.append('        <ul class="plain">' + "".join(f"<li>{e(b)}</li>" for b in _o["bullets"]) + "</ul>")
    if _body:
        _sections.append(_section(e(_o["title"]), "\n".join(_body)))

_specialties = f'\n          <p class="specialties">{e(RESUME["specialties"])}</p>' if RESUME.get("specialties") else ""

_html = f"""  <main id="main" class="resume">
    <div class="wrap">
      <header class="resume-head">
        <div>
          <p class="eyebrow">Resume</p>
          <h1 class="page-title">{e(RESUME['name'])}</h1>
          <p class="headline">{e(RESUME['headline'])}</p>
          <p class="contact-line">{_contact_html(RESUME['contact'])}</p>{_specialties}
        </div>
        <div class="actions no-print">
          <a class="btn" href="{PROFILE['resume']}" download>Download PDF</a>
          <button class="btn ghost" type="button" onclick="window.print()">Print</button>
        </div>
      </header>

{chr(10).join(_sections)}
    </div>
  </main>"""

# Last line of defense: never publish a phone number on the page.
assert not PHONE.search(_html), "A phone number made it into the resume page; refusing to build."
assert "@" not in _html, "An email address made it into the resume page; refusing to build."

page("/resume/", "Resume", (RESUME["summary"] or RESUME["headline"])[:155], "Resume", _html)
