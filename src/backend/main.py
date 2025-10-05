"""End-to-end pipeline:
1) Scrape all URLs listed in CSV_URL
2) Save raw scraped metadata (title, url, author, content) to data.json
3) Summarize each article via Gemini and collect structured summaries
4) Save final enriched summaries to processed_data.json
"""
import os
from scraper import scrape_all_from_csv
from geminiSummarizer import summarize_text
from storage import save_json, PROCESSED_PATH, DATA_PATH
from data_processor import enrich_data as enrich_helper

CSV_URL = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"


def run_pipeline(csv_url=CSV_URL, limit=None, delay=2, process_only=False):
    """Run the pipeline, optionally skipping scraping if data.json exists.
    
    Args:
        csv_url: URL to CSV containing article links
        limit: Optional max number of articles to process
        delay: Seconds to wait between scraping requests
        process_only: If True, skip scraping and only process existing data.json
    """
    # 1) scrape unless process_only is True
    if not process_only:
        print("[STEP] Starting scraping...")
        scraped = scrape_all_from_csv(csv_url, limit=limit)

        if not scraped:
            print("[ERROR] No scraped content. Exiting.")
            return

        # scraped is a list of dicts with keys: url, title, author, content
        print(f"[STEP] Saving {len(scraped)} scraped records to {DATA_PATH}")
        save_json(DATA_PATH, scraped, append=False)

    else:
        print("[STEP] Skipping scraping since --process-only was specified")
        if not os.path.exists(DATA_PATH):
            print(f"[ERROR] No {DATA_PATH} found. Please run without --process-only first.")
            return

    # 2) process without using Gemini API
    print("[STEP] Processing scraped data using local enrichment...")
    try:
        enrich_helper()  # This will read from DATA_PATH and write to PROCESSED_PATH
        print("[STEP] Pipeline finished. Data has been processed and saved to processed_data.json")
    except Exception as e:
        print(f"[ERROR] Processing failed: {e}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, help='Max number of articles to process')
    parser.add_argument('--process-only', action='store_true', 
                      help='Skip scraping and only process existing data.json')
    args = parser.parse_args()
    
    run_pipeline(limit=args.limit, process_only=args.process_only)
