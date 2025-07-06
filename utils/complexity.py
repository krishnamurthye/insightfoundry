from radon.complexity import cc_visit


def get_complexity_metrics(code, language):
    if language.lower() != "python":
        return []
    try:
        return [{"name": f.name, "complexity": f.complexity} for f in cc_visit(code)]
    except Exception:
        return []


def merge_complexity_estimates(json_blocks):
    values = []
    for j in json_blocks:
        val = j.get("file_complexity_estimate", "")
        if isinstance(val, (int, float)) and val >= 0:
            values.append(val)
        elif isinstance(val, str):
            try:
                parsed = float(val)
                if parsed >= 0:
                    values.append(parsed)
            except:
                continue
    if values:
        return round(sum(values) / len(values), 2)  # or `max(values)` or `min(values)`
    return None  # or "unknown"
