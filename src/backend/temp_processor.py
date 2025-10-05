"""Helper functions for extracting structured data from article summaries."""
import json
import re
from pathlib import Path
import os


def extract_sections(summary: str):
    """Extracts structured sections (Purpose, Methods, Findings, etc.) from the summary text."""
    if not isinstance(summary, str):
        print(f"[ERROR] Expected string for summary, got {type(summary)}")
        return None

    sections = {}
    pattern = r"\*\*\s*(.*?)\s*\*\*[：:]?\s*(.*?)(?=\n\*{2,}|$)"
    
    try:
        matches = re.findall(pattern, summary, flags=re.DOTALL)
        for title, content in matches:
            title = title.strip().replace("*", "")
            content = content.strip().replace("\n", " ")
            sections[title] = content
    except Exception as e:
        print(f"[WARN] Error extracting sections: {e}")
        return None

    return sections or None


def infer_title(summary: str):
    """Heuristic: take first line or first sentence as title."""
    if not isinstance(summary, str):
        return None
    try:
        first_line = summary.split("\n")[0]
        first_sentence = re.split(r"[.!?]", first_line)[0]
        return first_sentence.strip()[:120]
    except Exception as e:
        print(f"[WARN] Error inferring title: {e}")
        return None


def extract_author(summary: str):
    """Tries to find author mentions from phrases like 'by Smith et al.'."""
    if not isinstance(summary, str):
        return None
    try:
        match = re.search(r"\bby\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)(?:\s+et\s+al\.)?", summary)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"[WARN] Error extracting author: {e}")
        return None
    return None


def enrich_data(input_file="data.json", output_file="processed_data.json"):
    """Loads saved summaries, extracts title, author, and structured sections.
    
    By default, resolves files relative to this backend module so it reads/writes
    the same files used by other backend modules.
    """
    print("[DEBUG] Starting data enrichment...")

    base_dir = Path(os.path.dirname(__file__))
    path = Path(input_file)
    if not path.is_absolute():
        path = base_dir.joinpath(input_file)

    print(f"[DEBUG] Reading from {path}")

    if not path.exists():
        print(f"[ERROR] Could not find {path}")
        return

    try:
        with open(path, "r") as f:
            data = json.load(f)
            print(f"[DEBUG] Loaded {len(data)} records")
            print(f"[DEBUG] First record type: {type(data[0])}")
            if isinstance(data[0], str):
                print(f"[DEBUG] First string length: {len(data[0])}")
            else:
                print(f"[DEBUG] First record keys: {data[0].keys()}")
    except json.JSONDecodeError:
        print(f"[ERROR] {path} is empty or malformed.")
        return
    except Exception as e:
        print(f"[ERROR] Failed to read {path}: {e}")
        return

    enriched = []
    for i, record in enumerate(data):
        # Handle both string and dict records
        if isinstance(record, str):
            summary = record
            url = f"Unknown_{i}"
        elif isinstance(record, dict):
            summary = record.get("summary", "")
            url = record.get("url", f"Unknown_{i}")
        else:
            print(f"[WARN] Skipping record {i}: invalid type {type(record)}")
            continue

        # Skip empty summaries
        if not summary:
            print(f"[WARN] Skipping record {i}: empty summary")
            continue

        try:
            # Extract and validate metadata
            author = extract_author(summary) or "Unknown"
            title = infer_title(summary) or "Untitled"
            sections = extract_sections(summary) or {}

            enriched.append({
                "id": i + 1,
                "url": url,
                "author": author,
                "title": title,
                "summary": summary,
                "sections": sections
            })
            if (i + 1) % 10 == 0:
                print(f"[INFO] Processed {i + 1}/{len(data)} records...")
        except Exception as e:
            print(f"[WARN] Error enriching record {i}: {e}")
            continue

    if not enriched:
        print("[ERROR] No records were successfully enriched.")
        return

    out_path = Path(output_file)
    if not out_path.is_absolute():
        out_path = base_dir.joinpath(output_file)

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(enriched, f, indent=2)
            print(f"[INFO] ✅ Enriched {len(enriched)} summaries → {out_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save enriched data: {e}")


if __name__ == "__main__":
    enrich_data()
