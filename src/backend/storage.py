import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "test_data.json")

def save_results(results):
    """Save list of results (dicts) to JSON file."""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.extend(results)

    with open(DATA_PATH, "w") as f:
        json.dump(existing, f, indent=2)

    print(f"[INFO] Saved {len(results)} new entries to {DATA_PATH}")
    return DATA_PATH