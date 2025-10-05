import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "nih_data.json")

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

    existing.extend(results)

    with open(DATA_PATH, "w") as f:
        json.dump(existing, f, indent=2)

    print(f"[INFO] Saved {len(results)} new entries to {DATA_PATH}")
    return DATA_PATH