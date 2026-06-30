import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from extract import extract_csv, extract_notes

csv_data = extract_csv("sample_inputs/recruiter.csv")
notes_data = extract_notes("sample_inputs/recruiter_notes.txt")

print("CSV records:", csv_data)
print("Notes records:", notes_data)


from normalize import normalize_phone, extract_skills_from_text

print("Phone 1:", normalize_phone("9876543210"))
print("Phone 2:", normalize_phone("+91 98765 43210"))
print("Skills found:", extract_skills_from_text(notes_data[0]["skills_text"]))



from merge import merge_records

canonical = merge_records(csv_data, notes_data)
import json
print(json.dumps(canonical, indent=2))



import json as _json
from project import project

with open("config_example.json") as f:
    config = _json.load(f)

custom_output = project(canonical, config)
print(_json.dumps(custom_output, indent=2))