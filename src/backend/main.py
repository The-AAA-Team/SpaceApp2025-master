# main.py
from scraper import scrape_all_from_csv
from geminiSummarizer import summarize_text
from storage import save_results

CSV_URL = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"

if __name__ == "__main__":
    data = scrape_all_from_csv(CSV_URL, limit=3)
    results = []

    for url, text in data.items():
        print(f"\n---- SUMMARY for {url} ----")
        summary_data = summarize_text(text)

        # Attach URL if not already included
        if isinstance(summary_data, dict):
            summary_data["url"] = url
        else:
            summary_data = {"url": url, "summary": str(summary_data)}

        if "error" not in summary_data:
            results.append(summary_data)
            print(f"[SUCCESS] Summary generated for {url}")
        else:
            print(f"[ERROR] Failed to summarize {url}: {summary_data['error']}")

    if results:
        save_results(results)
        print(f"\n[INFO] ✅ Saved {len(results)} results to data.json")
    else:
        print("[INFO] No successful summaries generated.")
