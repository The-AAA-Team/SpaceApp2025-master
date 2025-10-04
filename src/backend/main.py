from scraper import scrape_all_from_csv
from geminiSummarizer import summarize_text
from storage import save_results
from data_processor import enrich_data



CSV_URL = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"

if __name__ == "__main__":
    data = scrape_all_from_csv(CSV_URL, limit=3)
    results = []

    for url, text in data.items():
        print(f"\n---- SUMMARY for {url} ----")
        summary = summarize_text(text)
        if summary:
            # print(summary)
            results.append({
                "url": url,
                "summary": summary
            })
        else:
            print("[ERROR] Failed to generate summary.")
if results:
    save_results(results)
    print("RESULTS: is true")
    # print(results)
    enrich_data()  # NEW LINE — runs the enrichment step
    print("[INFO] Enriched data saved to processed_results.json")
else:
    print("No results to save.")