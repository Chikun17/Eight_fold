# Eightfold Multi-Source Candidate Data Transformer

## What it does
Merges candidate data from a recruiter CSV (structured) and recruiter notes .txt
(unstructured) into one canonical profile, with normalization, provenance, and
confidence scoring. Supports a runtime config to reshape the output.

## How to run

1. Setup:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Run the pipeline:
   cd src
   python pipeline.py --csv ../sample_inputs/recruiter.csv \
                       --notes ../sample_inputs/recruiter_notes.txt \
                       --config ../config_example.json \
                       --out ../sample_outputs/output.json

   This produces:
   - sample_outputs/output.json        (full canonical profile)
   - sample_outputs/output_custom.json (config-projected output)

3. Run tests:
   python -m pytest tests/ -v

## Assumptions
- All input records belong to the same candidate (no cross-candidate dedup).
- Default region for phone parsing is India ("IN").
- Skills are matched via a small canonical keyword lookup table (not NLP).
- Source priority for conflicts: structured (CSV/ATS) > unstructured (resume/notes).

## Descoped (not implemented, due to time)
- Live GitHub/LinkedIn API integration (would extend extract.py the same way as CSV/notes).
- Resume PDF/DOCX parsing (notes.txt used as the unstructured source instead).
- Fuzzy name matching across sources (exact key matching only).
- UI — CLI only, per assignment's "lower priority" note.

## Architecture
extract -> merge (normalize + provenance) -> confidence -> project (config) -> validate