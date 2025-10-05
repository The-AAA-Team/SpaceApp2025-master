# data_processor.py
import json
import re
from pathlib import Path
import os


def extract_sections(summary: str):
    """Extracts structured sections (Purpose, Methods, Findings, etc.) from the summary text."""
    sections = {}
    pattern = r"\*\*\s*(.*?)\s*\*\*[:：]?\s*(.*?)(?=\n\*{2,}|$)"
    matches = re.findall(pattern, summary, flags=re.DOTALL)

    for title, content in matches:
        title = title.strip().replace("*", "")
        content = content.strip().replace("\n", " ")
        sections[title] = content

    return sections or None


def infer_title(summary: str):
    """Heuristic: take first line or first sentence as title."""
    first_line = summary.split("\n")[0]
    first_sentence = re.split(r"[.!?]", first_line)[0]
    return first_sentence.strip()[:120]


def extract_author(summary: str):
    """Tries to find author mentions from phrases like 'by Smith et al.'."""
    match = re.search(r"\bby\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)(?:\s+et\s+al\.)?", summary)
    if match:
        return match.group(1).strip()
    return "Unknown"


def enrich_data(input_file="data.json", output_file="processed_data.json"):
    """Loads saved summaries, extracts title, author, and structured sections.

    By default, resolves files relative to this backend module so it reads/writes
    the same files used by other backend modules.
    """
    base_dir = Path(os.path.dirname(__file__))
    path = Path(input_file)
    if not path.is_absolute():
        path = base_dir.joinpath(input_file)

    if not path.exists():
        print(f"[ERROR] Could not find {path}")
        return

    with open(input_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("[ERROR] data.json is empty or malformed.")
            return

    enriched = []
    for i, record in enumerate(data):
        summary = record.get("summary", "") if isinstance(record, dict) else str(record)
        url = record.get("url", f"Unknown_{i}") if isinstance(record, dict) else f"Unknown_{i}"

        author = extract_author(summary)
        title = infer_title(summary)
        sections = extract_sections(summary)

        enriched.append({
            "id": i + 1,
            "url": url,
            "author": author,
            "title": title,
            "summary": summary,
            "sections": sections
        })

    out_path = Path(output_file)
    if not out_path.is_absolute():
        out_path = base_dir.joinpath(output_file)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)

    print(f"[INFO] ✅ Enriched {len(enriched)} summaries → {out_path}")


if __name__ == "__main__":
    enrich_data()
