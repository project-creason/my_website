# Resume page content. Loaded by build.py (shares its helpers: page, e, PROFILE).
# When the resume changes, update this file AND replace assets/David_Creason_Resume.pdf.

RESUME = {
    "headline": "Enterprise Applications & Systems Integration Lead | Business Systems Architect",
    "location": "Greater Louisville Area",
    "summary": (
        "Business Systems Leader and Enterprise Applications Manager with over 15 years of experience leading "
        "cross-functional teams, platform roadmaps, and M&A integrations. Proven background bridging corporate "
        "strategy with technical execution to automate mission-critical operations across enterprise ERP platforms, "
        "finance workflows, and customer data systems. Combines P&L ownership acumen with deep governance expertise "
        "across SOX compliance, ITIL 4 service delivery, and vendor management to eliminate operational friction "
        "and scale organizational capacity."
    ),
    "skills": [
        ("Leadership & Strategy", ["Enterprise Application Management", "Cross-Functional Team Leadership",
                                   "M&A Systems Onboarding", "P&L Accountability", "Vendor Management & RFPs"]),
        ("Governance & Risk", ["SOX Compliance", "Separation of Duties (SoD)", "Role-Based Access Control (RBAC)",
                               "ITIL 4 Change Enablement", "Audit Readiness"]),
        ("Business Operations", ["Quote-to-Cash Optimization", "Process Automation", "Financial Close Enablement",
                                 "Operational Scaling", "KPI & SLA Governance"]),
        ("Enterprise Ecosystems", ["Yardi Voyager ERP", "SAP Concur", "Microsoft Dataverse", "Longview Reporting",
                                   "Jira", "Lightspeed POS", "Jobber CRM"]),
    ],
    "experience": [
        {
            "org": "Ventas, Inc.", "place": "Louisville, KY",
            "title": "Applications Systems Analyst", "dates": "April 2025 – Present",
            "bullets": [
                "Directed enterprise system administration and data governance for corporate Yardi ERP, overseeing a core technical team responsible for maintaining 8,000+ active property entities, multi-platform integrations, and month/quarter-end close readiness.",
                "Engineered internal SOX controls and release governance, establishing a dual-custody deployment model (segregated staging and execution roles) that eliminated a critical production audit gap and ensured 100% audit compliance.",
                "Drove operational efficiency across M&A asset transitions, automating cross-departmental onboarding workflows to reduce property setup cycle times by over 80% while standardizing data integrity between Accounting and IT.",
                "Spearheaded software vendor partnerships and technical roadmaps, championing automated audit systems (Detect by Oversight in Concur), resolving critical SLA deficiencies with reporting vendors (Longview), and advising executive leadership on enterprise procurement evaluations.",
            ],
        },
        {
            "org": "The Fire Place", "place": "Crestwood, KY",
            "title": "Division Manager (Operational & Business Integration)", "dates": "August 2021 – May 2024",
            "bullets": [
                "Directly managed post-acquisition division integration, consolidating field operations, warehouse logistics, and dedicated sales teams to scale regional division revenue past $1M in the first year post-merger.",
                "Spearheaded the launch and systems rollout of a 5,400 sq. ft. commercial service and retail showroom, leading vendor procurement, inventory imports via Lightspeed POS, and technical facility infrastructure.",
                "Trained and mentored dedicated sales specialists and technical installation crews, establishing operational performance benchmarks, job scheduling protocols, and client service delivery standards.",
                "Directed omnichannel brand outreach and marketing campaigns, collaborating with regional agencies to execute television commercials, live radio broadcasts, and targeted digital advertising to expand customer acquisition.",
            ],
        },
        {
            "org": "Crestwood Home & Hearth", "place": "Crestwood, KY",
            "title": "Founder & Managing Director", "dates": "August 2018 – August 2021",
            "bullets": [
                "Bootstrapped, owned, and directed all facets of an independent field service enterprise, holding complete P&L accountability and scaling annual top-line revenue from $50K to nearly $300K (~500% growth) over three fiscal years.",
                "Optimized the quote-to-cash lifecycle and field resource scheduling, managing a high-velocity client service engine supporting 16 to 20 customer touchpoints weekly across residential and commercial accounts.",
                "Established enterprise-grade safety and regulatory compliance protocols, leveraging master-level industry certifications (NFI, CSIA) to minimize client liability and deliver authoritative expert testimony in formal legal disputes.",
                "Negotiated and executed the strategic acquisition and asset sale of the enterprise, transferring vehicle fleets, specialized equipment, inventory, and customer contracts while securing an executive post-merger integration leadership role.",
            ],
        },
        {
            "org": "Tealium", "place": "San Diego, CA (Remote)",
            "title": "Solutions Consultant | Senior Deployment Engineer", "dates": "March 2016 – August 2018",
            "bullets": [
                "Governed enterprise client onboarding lifecycles, partnering with Technical Project Managers to drive 45- to 60-day implementation sprints across diverse Fortune 500 consumer brands.",
                "Designed and deployed a digital customer intake portal (PHP, SQL, HTML) to replace legacy spreadsheet questionnaires, standardizing technical requirements gathering and reducing onboarding cycle times.",
                "Led technical discovery and alignment sessions across cross-functional client teams, translating tracking goals into technical specs for marketing directors, enterprise developers, and executive leaders (CIO/CTO).",
                "Managed defect tracking and resolution workflows via Jira, collaborating with core product engineering to remediate platform bugs and establish standard operating procedures that elevated implementation success rates.",
            ],
        },
        {
            "org": "Neustar, Inc.", "place": "Louisville, KY",
            "title": "Senior Professional Services Engineer | Solutions Specialist", "dates": "January 2010 – March 2016",
            "bullets": [
                "Led Professional Services delivery operations across global enterprise accounts, governing client kickoffs, technical testing milestones, risk mitigation schedules, and executive briefings for high-profile retail brands (including Ann Taylor, Toys “R” Us, and Harris Teeter).",
                "Earned rapid promotion from Tier-2 Support to Senior Professional Services Engineer, serving as the senior technical escalation authority across proprietary and acquired SaaS monitoring platforms (BrowserMob).",
                "Delivered consultative, data-driven executive performance reviews to client leadership, translating complex system telemetry, failure thresholds, and global traffic latency into actionable remediation roadmaps.",
                "Streamlined technical operations and support escalation paths, establishing standardized operational procedures and building custom internal tools (PHP, SQL) that enhanced team productivity.",
                "Recognized with the Neustar CEO Award and multiple Spot Bonus Awards for exceptional technical problem resolution, cross-functional delivery, and enterprise client retention.",
            ],
        },
        {
            "org": "Kentucky Higher Education Student Loan Corporation", "place": "Louisville, KY",
            "title": "Technical Support Analyst | Network Technician", "dates": "June 2003 – January 2010",
            "bullets": [
                "Delivered Tier-1 and Tier-2 systems and network infrastructure administration across desktops, servers, and VPN connections for 250+ enterprise users.",
                "Managed application user provisioning, access permissions, and data security protocols in strict compliance with state and organizational security standards.",
            ],
        },
    ],
    "education": [
        ("Master of Business Administration (MBA) in Project Management", "Amberton University (In Progress)"),
        ("Master of Science (MS) in Applied Information Technology", "Bellarmine University"),
        ("Bachelor of Science (BS) in Information Technology (Honors)", "University of Phoenix"),
        ("ITIL 4 Foundation", "PeopleCert"),
        ("Google Data Analytics Professional Certificate", "Coursera / Google"),
    ],
    "community": [
        {
            "org": "i.c.stars", "place": "Louisville, KY",
            "title": "Volunteer Technical & Career Mentor", "dates": "2025",
            "bullets": [
                "Provide executive and technical mentorship to aspiring IT professionals from underserved backgrounds, conducting coaching in data modeling, systems troubleshooting, and career progression.",
                "Facilitate workshops on corporate IT navigation, ITIL service frameworks, and structured problem-solving methodologies.",
            ],
        },
    ],
}


def _jobs(items):
    out = []
    for j in items:
        bullets = "".join(f"<li>{e(b)}</li>" for b in j["bullets"])
        out.append(f"""        <article class="job">
          <header>
            <div><h3>{e(j['title'])}</h3><p class="org">{e(j['org'])} &middot; {e(j['place'])}</p></div>
            <p class="dates">{e(j['dates'])}</p>
          </header>
          <ul>{bullets}</ul>
        </article>""")
    return "\n".join(out)


_skills = "\n".join(
    f"""          <div><h3>{e(cat)}</h3><ul class="tags">{''.join(f'<li>{e(x)}</li>' for x in items)}</ul></div>"""
    for cat, items in RESUME["skills"]
)
_edu = "".join(f"<li><strong>{e(d)}</strong><span>{e(s)}</span></li>" for d, s in RESUME["education"])

page("/resume/", "Resume", RESUME["summary"][:155], "Resume", f"""  <main id="main" class="resume">
    <div class="wrap">
      <header class="resume-head">
        <div>
          <p class="eyebrow">Resume</p>
          <h1 class="page-title">{e(PROFILE['name'])}</h1>
          <p class="headline">{e(RESUME['headline'])}</p>
          <p class="contact-line">{e(RESUME['location'])} &middot; <a href="mailto:{PROFILE['email']}">{PROFILE['email']}</a> &middot; <a href="{PROFILE['linkedin']}" rel="noopener" target="_blank">linkedin.com/in/dcreason</a></p>
        </div>
        <div class="actions no-print">
          <a class="btn" href="{PROFILE['resume']}" download>Download PDF</a>
          <button class="btn ghost" type="button" onclick="window.print()">Print</button>
        </div>
      </header>

      <section class="r-section">
        <h2>Professional summary</h2>
        <p class="lede">{e(RESUME['summary'])}</p>
      </section>

      <section class="r-section">
        <h2>Core competencies &amp; technical skills</h2>
        <div class="skill-grid">
{_skills}
        </div>
      </section>

      <section class="r-section">
        <h2>Professional experience</h2>
{_jobs(RESUME['experience'])}
      </section>

      <section class="r-section">
        <h2>Education &amp; certifications</h2>
        <ul class="edu">{_edu}</ul>
      </section>

      <section class="r-section">
        <h2>Community involvement</h2>
{_jobs(RESUME['community'])}
      </section>
    </div>
  </main>""")
