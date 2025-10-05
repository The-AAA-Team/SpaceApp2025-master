#!/usr/bin/env python3
"""Resumable one-shot pipeline

Usage: python run_full_once.py [--limit N] [--dry-run] [--summarize-only] [--batch-size N] [--retry-count N]

This script will:
 - Read the CSV URL from main.CSV_URL
 - With --summarize-only:
   - Skip scraping, just process existing items in data.json
   - For items without summaries, call summarize_text in batches
   - Handle API quota limits with retries and exponential backoff
   - Log failed items to failed.json for later retry
 - Without --summarize-only (default):
   - Ensure scraped metadata for each URL is present in data.json
   - For scraped items not yet summarized, call summarize_text
   - Append results to processed_data.json

The script saves progress after each successful batch so it can be safely resumed.
"""
import argparse
import time
import json
import os
import random
from pathlib import Path

from main import CSV_URL
from scraper import read_urls_from_csv, scrape_article
from geminiSummarizer import summarize_text
from storage import save_json, DATA_PATH, PROCESSED_PATH

# Constants for retry logic
MAX_RETRY_COUNT = 3
MIN_DELAY_BETWEEN_REQUESTS = 31  # seconds (for 2 requests/min quota)
INITIAL_RETRY_DELAY = 31  # seconds
MAX_RETRY_DELAY = 120    # seconds
BATCH_SIZE = 10
last_request_time = 0  # Track timing between requests

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_progress(path, data, backup=True):
    """Save data with optional backup of existing file."""
    if backup and os.path.exists(path):
        backup_path = f"{path}.bak"
        os.rename(path, backup_path)
        print(f"[INFO] Backed up existing file to {backup_path}")
    save_json(path, data, append=False)

def save_failed(failed_items, error_info):
    """Save failed items to failed.json with error info for later retry."""
    failed_path = Path(DATA_PATH).parent / 'failed.json'
    existing_failed = load_json(failed_path)
    
    # Add timestamp and error info
    failed_entry = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'error': str(error_info),
        'items': failed_items
    }
    existing_failed.append(failed_entry)
    save_json(failed_path, existing_failed)
    print(f"[WARN] Saved {len(failed_items)} failed items to {failed_path}")

def retry_with_backoff(func, *args, max_retries=MAX_RETRY_COUNT):
    """Retry a function with exponential backoff and rate limiting."""
    global last_request_time
    
    for attempt in range(max_retries):
        try:
            # Ensure minimum delay between requests
            now = time.time()
            time_since_last = now - last_request_time
            if time_since_last < MIN_DELAY_BETWEEN_REQUESTS:
                sleep_time = MIN_DELAY_BETWEEN_REQUESTS - time_since_last
                print(f"[INFO] Rate limiting - waiting {sleep_time:.1f}s before next request...")
                time.sleep(sleep_time)
            
            result = func(*args)
            last_request_time = time.time()
            return result
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Re-raise the last exception if all retries failed
            
            # Use longer delays for quota errors
            if "429" in str(e) or "quota" in str(e).lower():
                delay = max(MIN_DELAY_BETWEEN_REQUESTS, INITIAL_RETRY_DELAY * (2 ** attempt))
            else:
                delay = min(INITIAL_RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1), MAX_RETRY_DELAY)
                
            print(f"[WARN] Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay:.1f}s...")
            time.sleep(delay)

def process_batch(items, batch_size=BATCH_SIZE, summarize_only=False):
    """Process a batch of items, either summarizing or full pipeline."""
    results = []
    failed = []
    
    for i, item in enumerate(items):
        try:
            if summarize_only:
                # Only summarize if no summary exists
                if isinstance(item, dict) and not item.get('summary'):
                    print(f"[INFO] Summarizing {i+1}/{len(items)}: {item.get('url', 'Unknown URL')}")
                    summary = retry_with_backoff(summarize_text, item['content'])
                    item['summary'] = summary
                    results.append(item)
                else:
                    results.append(item)  # Keep existing item
            else:
                # Full pipeline
                if isinstance(item, dict) and 'content' in item:
                    summary = retry_with_backoff(summarize_text, item['content'])
                    results.append({'url': item['url'], 'summary': summary})
                else:
                    results.append(item)  # Keep legacy format
                    
        except Exception as e:
            print(f"[ERROR] Failed to process item {i+1}: {str(e)}")
            failed.append(item)
            
        # Save progress after each batch
        if (i + 1) % batch_size == 0:
            print(f"[INFO] Completed batch ending at {i+1}/{len(items)}")
            save_progress(DATA_PATH, results)
            
    return results, failed

def ensure_scraped(urls, existing_data, delay=1):
    """Scrape any URL not present in existing_data (match by url) and return updated list."""
    # existing_data may contain legacy string entries; only collect urls from dict items
    existing_urls = set()
    for d in existing_data:
        if isinstance(d, dict):
            u = d.get('url')
            if u:
                existing_urls.add(u)
        else:
            # skip non-dict legacy entries
            continue
    
    to_add = []
    for url in urls:
        if url not in existing_urls:
            try:
                print(f"[SCRAPE] {url}")
                content = scrape_article(url)
                if content:
                    to_add.append({'url': url, 'content': content})
                    existing_urls.add(url)
                    time.sleep(delay)  # Be nice to servers
            except Exception as e:
                print(f"[ERROR] Failed to scrape {url}: {e}")
                continue
    
    return existing_data + to_add

def main(limit=None, dry_run=False, summarize_only=False, batch_size=BATCH_SIZE, retry_count=MAX_RETRY_COUNT):
    """Main pipeline with support for summarize-only mode and batching."""
    print("[INFO] Loading existing data...")
    existing_data = load_json(DATA_PATH) or []
    total_records = len(existing_data)
    print(f"[INFO] Found {total_records} existing records")
    
    if not summarize_only:
        # Normal pipeline - scrape first
        print("[INFO] Reading URLs from CSV...")
        urls = read_urls_from_csv(CSV_URL)
        if limit:
            urls = urls[:limit]
            
        print(f"[INFO] Found {len(urls)} URLs to process")
        if dry_run:
            return
            
        print("[INFO] Ensuring all URLs are scraped...")
        updated_data = ensure_scraped(urls, existing_data)
        if updated_data != existing_data:
            print("[INFO] Saving updated scraped data...")
            save_progress(DATA_PATH, updated_data)
        existing_data = updated_data
    
    # Process in batches
    if limit:
        existing_data = existing_data[:limit]
    
    batches = [existing_data[i:i + batch_size] for i in range(0, len(existing_data), batch_size)]
    print(f"[INFO] Processing {len(existing_data)} records in {len(batches)} batches of {batch_size}")
    
    all_results = []
    all_failed = []
    
    start_time = time.time()
    for i, batch in enumerate(batches, 1):
        batch_start = time.time()
        total_items = len(existing_data)
        items_done = (i-1) * batch_size
        
        # Calculate ETA
        if i > 1:
            avg_batch_time = (batch_start - start_time) / (i-1)
            eta_minutes = (len(batches) - i + 1) * avg_batch_time / 60
            eta_str = f", ETA: {eta_minutes:.1f} minutes"
        else:
            eta_str = ""
            
        print(f"[INFO] Processing batch {i}/{len(batches)} ({items_done}/{total_items} items{eta_str})...")
        results, failed = process_batch(batch, batch_size=batch_size, summarize_only=summarize_only)
        all_results.extend(results)
        
        if failed:
            all_failed.extend(failed)
            save_failed(failed, f"Failed in batch {i}")
    
    # Save final results
    save_progress(DATA_PATH, all_results)
    
    # Print summary
    print(f"\n[SUMMARY]")
    print(f"Total records processed: {len(all_results)}")
    print(f"Successfully summarized: {len([r for r in all_results if isinstance(r, dict) and r.get('summary')])}")
    print(f"Failed items: {len(all_failed)}")
    
    if all_failed:
        print(f"Failed items saved to failed.json")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, help='limit number of articles to process')
    parser.add_argument('--dry-run', action='store_true', help='print what would be done without doing it')
    parser.add_argument('--summarize-only', action='store_true', help='skip scraping, only generate summaries')
    parser.add_argument('--batch-size', type=int, default=BATCH_SIZE, help='number of items to process before saving')
    parser.add_argument('--retry-count', type=int, default=MAX_RETRY_COUNT, help='maximum number of retries per item')
    args = parser.parse_args()
    
    main(
        limit=args.limit,
        dry_run=args.dry_run,
        summarize_only=args.summarize_only,
        batch_size=args.batch_size,
        retry_count=args.retry_count
    )
