import requests
import pandas as pd
from bs4 import BeautifulSoup
import time


def read_urls_from_csv(csv_url):
    """
    Reads a CSV from a GitHub raw link and extracts all URLs.
    It auto-detects which column contains the links.
    """
    try:
        df = pd.read_csv(csv_url)
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        return []

    # Try to find a column with 'url' or 'link' in its name
    possible_cols = [col for col in df.columns if 'url' in col.lower() or 'link' in col.lower()]
    if not possible_cols:
        print("[ERROR] No URL column found in CSV. Check column names.")
        print("Columns found:", df.columns.tolist())
        return []

    url_col = possible_cols[0]
    urls = df[url_col].dropna().tolist()
    print(f"[INFO] Found {len(urls)} URLs in column '{url_col}'.")
    return urls


def scrape_article(url):
    """
    Fetches and cleans all readable text from a single webpage using BeautifulSoup.
    Removes scripts, styles, navbars, etc.
    Returns plain text.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        # Remove unnecessary elements
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()

        # Try to extract title and author metadata
        title = None
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        if not title:
            og_title = soup.find('meta', attrs={'property': 'og:title'})
            if og_title and og_title.get('content'):
                title = og_title['content'].strip()

        # heuristic for author from meta tags
        author = None
        author_meta = soup.find('meta', attrs={'name': 'author'}) or soup.find('meta', attrs={'property': 'article:author'})
        if author_meta and author_meta.get('content'):
            author = author_meta['content'].strip()

        # Extract visible paragraph text
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        content = ' '.join(paragraphs).strip()

        return {
            'url': url,
            'title': title or '',
            'author': author or 'Unknown',
            'content': content,
        }

    except Exception as e:
        print(f"[ERROR] While scraping {url}: {e}")
        return None


def scrape_all_from_csv(csv_url, limit=None):
    """
    Loops through all URLs in the CSV and scrapes each.
    You can set a limit to test only a few.
    Returns a dictionary {url: text}.
    """
    urls = read_urls_from_csv(csv_url)
    if limit:
        urls = urls[:limit]

    results = []
    print(f"[INFO] Starting scrape for {len(urls)} URLs...")

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Scraping: {url}")
        data = scrape_article(url)
        if data and data.get('content'):
            results.append(data)
            print(f"[SUCCESS] Collected {len(data.get('content'))} characters for {url}.")
        else:
            print("[WARN] No text extracted.")
        time.sleep(2)  # delay to avoid rate limiting

    print(f"\n[INFO] Finished scraping {len(results)} successful URLs.")
    return results