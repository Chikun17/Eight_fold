import argparse
import json
import sys

from extract import extract_csv, extract_notes
from merge import merge_records
from project import project
from validate import validate_canonical


def run_pipeline(csv_path, notes_path, config_path, out_path):
    # 1. Extract
    csv_records = extract_csv(csv_path) if csv_path else []
    notes_records = extract_notes(notes_path) if notes_path else []

    if not csv_records and not notes_records:
        print("[error] No usable input sources found. Exiting.")
        sys.exit(1)

    # 2. Merge (normalize happens inside merge.py via normalize.py calls)
    canonical = merge_records(csv_records, notes_records)

    # 3. Validate canonical record
    try:
        validate_canonical(canonical)
    except Exception as e:
        print(f"[error] Canonical record failed validation: {e}")
        sys.exit(1)

    # 4. Default output = canonical record itself
    default_output = canonical

    # 5. If a config was given, also produce a custom projected output
    custom_output = None
    if config_path:
        with open(config_path) as f:
            config = json.load(f)
        custom_output = project(canonical, config)

    # 6. Write results
    with open(out_path, "w") as f:
        json.dump(default_output, f, indent=2)
    print(f"[ok] Default canonical output written to {out_path}")

    if custom_output:
        custom_out_path = out_path.replace(".json", "_custom.json")
        with open(custom_out_path, "w") as f:
            json.dump(custom_output, f, indent=2)
        print(f"[ok] Custom config output written to {custom_out_path}")


def main():
    parser = argparse.ArgumentParser(description="Eightfold Multi-Source Candidate Data Transformer")
    parser.add_argument("--csv", help="Path to recruiter CSV file")
    parser.add_argument("--notes", help="Path to recruiter notes .txt file")
    parser.add_argument("--config", help="Path to runtime projection config JSON")
    parser.add_argument("--out", default="sample_outputs/output.json", help="Output file path")
    args = parser.parse_args()

    run_pipeline(args.csv, args.notes, args.config, args.out)


if __name__ == "__main__":
    main()