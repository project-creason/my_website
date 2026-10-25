"""The resume PDF is the source of truth for the site.

`load_resume(pdf_path)` reads the PDF and returns structured data (name, headline,
summary, skills, experience, education, other sections). Any phone number is
removed from the extracted text.

`redact_phone_numbers(pdf_path)` blacks out (whites out) any phone number in the
PDF itself, in place, so the downloadable copy never shows one either.

`redact_emails(pdf_path)` removes any email address from the PDF, in place, and
re-sets the line it sat on (same font, size and color, re-centered if it was centered)
so no gap is left behind.

Requires PyMuPDF:  pip install pymupdf
"""
import re
import shutil
import tempfile

import pymupdf

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?:\+?1[\s.-]?)?\(?\b\d{3}\)?[\s.-]?\d{3}[\s.-]\d{4}\b")
MONTH = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
DATE = rf"(?:{MONTH}\.?\s+)?\d{{4}}"
DATES = rf"{DATE}(?:\s*[-–—]\s*(?:Present|Current|{DATE}))?"
TITLE_DATES = re.compile(rf"^(?P<title>.+?)\s*(?::|\|)\s*(?P<dates>{DATES})\s*$")
BULLET = re.compile(r"^[●•▪◦\-\*]\s*")


def scrub(text):
    """Remove phone numbers and tidy separators left behind."""
    text = PHONE.sub("", text)
    text = EMAIL.sub("", text)
    text = re.sub(r"(\s*\|\s*){2,}", " | ", text)
    return re.sub(r"^\s*\|\s*|\s*\|\s*$", "", text).strip()


def _lines(pdf_path):
    doc = pymupdf.open(pdf_path)
    raw = "\n".join(page.get_text(sort=True) for page in doc)
    out = []
    for line in raw.splitlines():
        line = line.replace("​", "").replace("\xa0", " ").strip()
        line = re.sub(r"\s{2,}", " ", line)
        if line:
            out.append(scrub(line) if PHONE.search(line) or EMAIL.search(line) else line)
    return [l for l in out if l]


SECTION_WORDS = ("SUMMARY", "PROFILE", "SKILL", "COMPETENC", "EXPERIENCE", "EMPLOYMENT", "EDUCATION",
                 "CERTIFICATION", "COMMUNITY", "VOLUNTEER", "INVOLVEMENT", "AWARD", "PROJECT",
                 "PUBLICATION", "ACCOMPLISHMENT", "ACHIEVEMENT", "AFFILIATION", "LEADERSHIP")


def _is_heading(line):
    letters = re.sub(r"[^A-Za-z]", "", line)
    return (letters.isupper() and len(letters) >= 6 and "|" not in line and not line.endswith(".")
            and not BULLET.match(line) and any(w in line.upper() for w in SECTION_WORDS))


def _split_outside_parens(s, sep=","):
    parts, depth, cur = [], 0, ""
    for ch in s:
        depth += ch == "("
        depth -= ch == ")"
        if ch == sep and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def _parse_section(lines):
    """Return {"paragraph": str, "bullets": [...], "entries": [...]} for one section."""
    entries, bullets, para = [], [], []
    cur_entry, cur_bullet = None, None

    def close_bullet():
        nonlocal cur_bullet
        if cur_bullet is not None:
            (cur_entry["bullets"] if cur_entry else bullets).append(cur_bullet.strip())
            cur_bullet = None

    i = 0
    while i < len(lines):
        line = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        # "Org | Place" followed by "Title: dates" (or "Title | dates") starts an entry
        if "|" in line and not BULLET.match(line) and TITLE_DATES.match(nxt):
            close_bullet()
            org, _, place = line.rpartition("|")
            m = TITLE_DATES.match(nxt)
            cur_entry = {"org": org.strip(), "place": place.strip(),
                         "title": m["title"].strip(), "dates": re.sub(r"\s*[-–—]\s*", " – ", m["dates"].strip()),
                         "bullets": []}
            entries.append(cur_entry)
            i += 2
            continue
        if BULLET.match(line):
            close_bullet()
            rest = BULLET.sub("", line)
            cur_bullet = rest
        elif cur_bullet is not None:
            cur_bullet += " " + line
        else:
            para.append(line)
        i += 1
    close_bullet()
    return {"paragraph": " ".join(para).strip(), "bullets": bullets, "entries": entries}


def load_resume(pdf_path):
    lines = _lines(pdf_path)
    name = lines[0].title() if lines[0].isupper() else lines[0]
    header, sections, order, current = [], {}, [], None
    for line in lines[1:]:
        if _is_heading(line):
            current = line.strip()
            sections[current] = []
            order.append(current)
        elif current is None:
            header.append(line)
        else:
            sections[current].append(line)

    headline = header[0] if header else ""
    contact_line = next((l for l in header if "@" in l or "linkedin" in l.lower()), "")
    contact = [p.strip() for p in contact_line.split("|") if p.strip()]
    # Text between the contact line and the first heading: an all-caps specialties banner
    # and/or an unlabeled summary paragraph.
    rest = header[header.index(contact_line) + 1:] if contact_line in header else header[1:]
    banner = [l for l in rest if re.sub(r"[^A-Za-z]", "", l).isupper()]
    intro = " ".join(l for l in rest if l not in banner)
    location = next((p for p in contact if "@" not in p and "linkedin" not in p.lower() and "http" not in p), "")

    r = {"name": name, "headline": headline, "location": location, "contact": contact,
         "specialties": " ".join(banner), "summary": intro, "skills": [], "experience": [], "education": [], "other": []}

    for title in order:
        parsed = _parse_section(sections[title])
        t = title.lower()
        if "summary" in t or "profile" in t:
            r["summary"] = parsed["paragraph"] or " ".join(parsed["bullets"])
        elif ("skill" in t or "competenc" in t) and not parsed["entries"]:
            for b in parsed["bullets"]:
                cat, sep, items = b.partition(":")
                r["skills"].append((cat.strip(), _split_outside_parens(items)) if sep else ("", [b]))
        elif "experience" in t or "employment" in t:
            r["experience"] = parsed["entries"]
        elif ("education" in t or "certification" in t) and not parsed["entries"]:
            for b in parsed["bullets"]:
                deg, _, school = b.rpartition("|") if "|" in b else b.rpartition(":")
                r["education"].append((deg.strip(), school.strip()) if deg else (b, ""))
        else:
            r["other"].append({"title": title.title(), **parsed})
    return r


def redact_phone_numbers(pdf_path):
    """White out any phone number in the PDF, in place. Returns how many were removed."""
    doc = pymupdf.open(pdf_path)
    found = 0
    for page in doc:
        for match in set(m.group(0) for m in PHONE.finditer(page.get_text())):
            for rect in page.search_for(match):
                page.add_redact_annot(rect, fill=(1, 1, 1))
                found += 1
        page.apply_redactions()
    if found:
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
        doc.save(tmp, garbage=4, deflate=True)
        doc.close()
        shutil.move(tmp, pdf_path)
    else:
        doc.close()
    return found


def redact_emails(pdf_path):
    """Remove any email address from the PDF, in place, re-setting its line. Returns how many were removed."""
    doc = pymupdf.open(pdf_path)
    found = 0
    for page in doc:
        fonts = {f[3].split("+")[-1]: f[0] for f in page.get_fonts()}
        redo = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                spans = line["spans"]
                text = "".join(sp["text"] for sp in spans)
                if not EMAIL.search(text):
                    continue
                found += len(EMAIL.findall(text))
                first = spans[0]
                left, right = min(sp["bbox"][0] for sp in spans), max(sp["bbox"][2] for sp in spans)
                centered = abs((left + right) / 2 - page.rect.width / 2) < 4
                redo.append((scrub(text), first, left, right, centered))
                for sp in spans:
                    page.add_redact_annot(pymupdf.Rect(sp["bbox"]), fill=(1, 1, 1))
        if not redo:
            continue
        page.apply_redactions()
        for new_text, sp, left, right, centered in redo:
            if not new_text:
                continue
            buf = doc.extract_font(fonts[sp["font"]])[3]
            font = pymupdf.Font(fontbuffer=buf)
            width = font.text_length(new_text, sp["size"])
            x = (left + right) / 2 - width / 2 if centered else left
            c = sp["color"]
            alias = "redo" + re.sub(r"[^A-Za-z]", "", sp["font"])[:12]
            page.insert_font(fontname=alias, fontbuffer=buf)
            page.insert_text((x, sp["origin"][1]), new_text, fontsize=sp["size"], fontname=alias,
                             color=((c >> 16) / 255, (c >> 8 & 255) / 255, (c & 255) / 255))
    if found:
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
        doc.save(tmp, garbage=4, deflate=True)
        doc.close()
        shutil.move(tmp, pdf_path)
    else:
        doc.close()
    return found
