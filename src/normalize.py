import phonenumbers

# A small canonical skill lookup — maps messy variants to one clean name.
SKILL_CANON = {
    "python": "Python",
    "react": "React",
    "reactjs": "React",
    "docker": "Docker",
    "aws": "AWS",
    "node": "Node.js",
    "nodejs": "Node.js",
}


def normalize_phone(raw, default_region="IN"):
    """Convert a messy phone string to E.164 format (+91...). Returns None if invalid."""
    if not raw:
        return None
    try:
        parsed = phonenumbers.parse(raw, default_region)
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        pass
    return None


def normalize_skill(raw):
    """Map a raw skill word to its canonical name. Returns None if unrecognized."""
    if not raw:
        return None
    key = raw.strip().lower()
    return SKILL_CANON.get(key)


def extract_skills_from_text(text):
    """Scan free text for known skill keywords and return canonical names found."""
    if not text:
        return []
    found = []
    lower = text.lower()
    for variant, canon in SKILL_CANON.items():
        if variant in lower and canon not in found:
            found.append(canon)
    return found


def normalize_date(raw):
    """Placeholder for now — we'll extend this once we add resume parsing with real dates."""
    return raw