import uuid
from normalize import normalize_phone, extract_skills_from_text
from confidence import compute_overall_confidence

# Priority order when two sources disagree — structured sources trusted more.
SOURCE_PRIORITY = {
    "recruiter_csv": 3,
    "ats_json": 3,
    "github": 2,
    "linkedin": 2,
    "resume": 2,
    "recruiter_notes": 1,
}


def _pick_best(values_with_sources):
    """values_with_sources: list of (value, source). Pick highest-priority non-null value."""
    candidates = [(v, s) for v, s in values_with_sources if v]
    if not candidates:
        return None, None
    candidates.sort(key=lambda x: SOURCE_PRIORITY.get(x[1], 0), reverse=True)
    return candidates[0]


def merge_records(csv_records, notes_records):
    """Merge CSV rows + notes records into ONE canonical profile.
    Assumption: all records here belong to the same candidate (we're not
    doing cross-candidate deduplication in this minimal version)."""

    provenance = []
    skills = {}  # name -> {"sources": set()}

    # --- full_name: pick best across all records ---
    name_candidates = [(r.get("full_name"), r["source"]) for r in csv_records + notes_records]
    full_name, name_source = _pick_best(name_candidates)
    if full_name:
        provenance.append({"field": "full_name", "source": name_source, "method": "priority_pick"})

    # --- emails: collect all unique, non-null ---
    emails = []
    for r in csv_records + notes_records:
        e = r.get("email")
        if e and e not in emails:
            emails.append(e)
            provenance.append({"field": "emails", "source": r["source"], "method": "collected"})

    # --- phones: normalize then dedupe ---
    phones = []
    for r in csv_records:
        p = normalize_phone(r.get("phone"))
        if p and p not in phones:
            phones.append(p)
            provenance.append({"field": "phones", "source": r["source"], "method": "normalized_e164"})

    # --- company / title: pick best from CSV (most structured) ---
    company_candidates = [(r.get("company"), r["source"]) for r in csv_records]
    title_candidates = [(r.get("title"), r["source"]) for r in csv_records]
    company, company_source = _pick_best(company_candidates)
    title, title_source = _pick_best(title_candidates)

    experience = []
    if company or title:
        experience.append({"company": company, "title": title, "start": None, "end": None, "summary": None})
        provenance.append({"field": "experience", "source": company_source or title_source, "method": "priority_pick"})

    # --- skills: extract from free text, tag sources ---
    for r in notes_records:
        found = extract_skills_from_text(r.get("skills_text"))
        for s in found:
            skills.setdefault(s, {"sources": set()})
            skills[s]["sources"].add(r["source"])
            provenance.append({"field": f"skills.{s}", "source": r["source"], "method": "keyword_match"})

    skills_list = [
        {"name": name, "confidence": 0.6 if len(info["sources"]) == 1 else 0.9, "sources": list(info["sources"])}
        for name, info in skills.items()
    ]

    # --- links: github from notes ---
    github = None
    for r in notes_records:
        if r.get("github"):
            github = "https://" + r["github"] if not r["github"].startswith("http") else r["github"]
            provenance.append({"field": "links.github", "source": r["source"], "method": "keyword_match"})

    # --- location: city from notes ---
    city = None
    for r in notes_records:
        if r.get("city"):
            city = r["city"]
            provenance.append({"field": "location.city", "source": r["source"], "method": "keyword_match"})

    canonical = {
        "candidate_id": str(uuid.uuid4()),
        "full_name": full_name,
        "emails": emails,
        "phones": phones,
        "location": {"city": city, "region": None, "country": "IN" if city else None},
        "links": {"linkedin": None, "github": github, "portfolio": None, "other": []},
        "headline": title,
        "years_experience": None,
        "skills": skills_list,
        "experience": experience,
        "education": [],
        "provenance": provenance,
    }
    canonical["overall_confidence"] = compute_overall_confidence(canonical)
    return canonical
    