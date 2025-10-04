from scraper import scrape_all_from_csv
from geminiSummarizer import summarize_text

CSV_URL = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"

if __name__ == "__main__":
    data = scrape_all_from_csv(CSV_URL, limit=3)
    for url, text in data.items():
        print(f"\n---- SUMMARY for {url} ----")
        summary = summarize_text(text)
        if summary:
            print(summary)
        else:
            print("[ERROR] Failed to generate summary.")