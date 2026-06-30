def compute_overall_confidence(canonical):
    """Simple, explainable scoring: average of per-field confidence signals."""
    scores = []

    # Core identity fields: full credit if present, since CSV is reliable
    scores.append(1.0 if canonical.get("full_name") else 0.0)
    scores.append(1.0 if canonical.get("emails") else 0.0)
    scores.append(1.0 if canonical.get("phones") else 0.0)

    # Skills: average of individual skill confidences (0 if no skills found)
    skills = canonical.get("skills", [])
    if skills:
        scores.append(sum(s["confidence"] for s in skills) / len(skills))
    else:
        scores.append(0.0)

    # Experience: full credit if at least one entry present
    scores.append(1.0 if canonical.get("experience") else 0.0)

    return round(sum(scores) / len(scores), 2)