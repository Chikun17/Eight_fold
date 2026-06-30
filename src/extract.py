import csv

def extract_csv(path, source_name="recruiter_csv"):
    """Read the recruiter CSV and return a list of raw candidate dicts."""
    records = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append({
                    "source": source_name,
                    "full_name": row.get("name", "").strip() or None,
                    "email": row.get("email", "").strip() or None,
                    "phone": row.get("phone", "").strip() or None,
                    "company": row.get("current_company", "").strip() or None,
                    "title": row.get("title", "").strip() or None,
                })
    except FileNotFoundError:
        print(f"[warn] CSV not found at {path}, skipping.")
    except Exception as e:
        print(f"[warn] CSV malformed ({e}), skipping bad rows.")
    return records


def extract_notes(path, source_name="recruiter_notes"):
    """Read free-text recruiter notes and pull out simple fields by keyword."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"[warn] Notes file not found at {path}, skipping.")
        return []

    record = {"source": source_name, "full_name": None, "email": None,
              "company": None, "title": None, "skills_text": text,
              "github": None, "city": None}

    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("candidate:"):
            record["full_name"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("email:"):
            record["email"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("github:"):
            record["github"] = line.split(":", 1)[1].strip()

    if "based in" in text.lower():
        # crude extraction: text after "Based in" up to the period
        idx = text.lower().find("based in")
        snippet = text[idx + len("based in"):].split(".")[0].strip()
        record["city"] = snippet

    return [record]