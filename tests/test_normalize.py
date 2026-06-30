import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from normalize import normalize_phone, extract_skills_from_text

def test_normalize_phone_plain():
    assert normalize_phone("9876543210") == "+919876543210"

def test_normalize_phone_with_country_code():
    assert normalize_phone("+91 98765 43210") == "+919876543210"

def test_normalize_phone_invalid():
    assert normalize_phone("123") is None

def test_normalize_phone_empty():
    assert normalize_phone(None) is None

def test_extract_skills():
    text = "I know Python and ReactJS"
    skills = extract_skills_from_text(text)
    assert "Python" in skills