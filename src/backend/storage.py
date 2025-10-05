import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")
PROCESSED_PATH = os.path.join(os.path.dirname(__file__), "processed_data.json")

def save_results(results):
    """Save list of results (dicts) to JSON file."""
    existing = []
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f) or []
        except (json.JSONDecodeError, ValueError):
            # If the file is empty or malformed, warn and start fresh
            print(f"[WARN] {DATA_PATH} is empty or malformed. Overwriting with new data.")
            existing = []
        except Exception as e:
            print(f"[WARN] Could not read existing data at {DATA_PATH}: {e}")
            existing = []

    existing += results

    with open(DATA_PATH, "w") as f:
        json.dump(existing, f, indent=2)

    print(f"[INFO] Saved {len(results)} new entries to {DATA_PATH}")
    return DATA_PATH

def save_json(path, data, append=False):
    """Write `data` (list or dict) to `path`. If append and path exists and contains a list, extend it.

    Path may be absolute or relative. If relative, it's interpreted as-is.
    """
    try:
        # if append and file exists and contains a JSON list, extend it
        if append and os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    existing = json.load(f) or []
            except Exception:
                existing = []

            if isinstance(existing, list) and isinstance(data, list):
                existing.extend(data)
                out = existing
            else:
                # If types mismatch or not list, overwrite
                out = data
        else:
            out = data

        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)

        print(f"[INFO] Wrote {len(data) if isinstance(data, list) else 1} entries to {path}")
        return path
    except Exception as e:
        print(f"[ERROR] Failed to write {path}: {e}")
        raise