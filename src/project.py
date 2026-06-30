def _get_path(record, path):
    """Resolve a simple path like 'emails[0]' or 'skills[].name' against the canonical record."""
    if "[]." in path:
        # e.g. "skills[].name" -> get list, pull 'name' from each item
        list_key, sub_field = path.split("[].")
        items = record.get(list_key, [])
        return [item.get(sub_field) for item in items if item.get(sub_field)]

    if "[" in path and "]" in path:
        # e.g. "emails[0]"
        key = path.split("[")[0]
        idx = int(path.split("[")[1].split("]")[0])
        values = record.get(key, [])
        return values[idx] if idx < len(values) else None

    # plain field, e.g. "full_name"
    return record.get(path)


def project(canonical, config):
    """Apply a runtime config to reshape the canonical record into a custom output."""
    output = {}
    on_missing = config.get("on_missing", "null")

    for field_def in config.get("fields", []):
        out_path = field_def["path"]
        source_path = field_def.get("from", out_path)
        required = field_def.get("required", False)

        value = _get_path(canonical, source_path)

        if value is None or value == []:
            if required and on_missing == "error":
                raise ValueError(f"Required field '{out_path}' is missing.")
            if on_missing == "omit":
                continue
            output[out_path] = None  # default: "null"
        else:
            output[out_path] = value

    if config.get("include_confidence", False):
        output["overall_confidence"] = canonical.get("overall_confidence")

    return output