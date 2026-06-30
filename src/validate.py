import jsonschema
from schema import CANONICAL_SCHEMA

def validate_canonical(record):
    """Validate the full canonical record against our fixed schema. Raises on failure."""
    jsonschema.validate(instance=record, schema=CANONICAL_SCHEMA)
    return True