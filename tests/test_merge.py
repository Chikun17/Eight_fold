import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from extract import extract_csv, extract_notes
from merge import merge_records

def test_merge_produces_candidate_id():
    csv_records = extract_csv("sample_inputs/recruiter.csv")
    notes_records = extract_notes("sample_inputs/recruiter_notes.txt")
    canonical = merge_records(csv_records, notes_records)
    assert canonical["candidate_id"]
    assert canonical["full_name"] == "Om Mohanty"
    assert "+919876543210" in canonical["phones"]

def test_merge_handles_missing_source():
    canonical = merge_records([], [])
    assert canonical["full_name"] is None
    assert canonical["emails"] == []