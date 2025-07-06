import json


def extract_json_objects(raw_chunks):
    json_objects = []

    for raw in raw_chunks:
        # Directly use if already parsed
        if isinstance(raw, dict):
            json_objects.append(raw)
            continue

        # Try parsing entire string as JSON
        try:
            json_obj = json.loads(raw)
            if isinstance(json_obj, dict):
                json_objects.append(json_obj)
                continue
        except json.JSONDecodeError:
            pass  # fallback to manual parsing below

        # If string contains multiple JSON blocks, try to extract each
        try:
            start = 0
            while start < len(raw):
                start = raw.find("{", start)
                if start == -1:
                    break
                end = raw.find("}", start)
                while end != -1:
                    try:
                        candidate = raw[start:end + 1]
                        obj = json.loads(candidate)
                        if isinstance(obj, dict) and "file_summary" in obj:
                            json_objects.append(obj)
                            break
                    except json.JSONDecodeError:
                        pass
                    end = raw.find("}", end + 1)
                start += 1
        except Exception:
            continue

    return json_objects
