#Knowledge graph

import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from storage import save_results
from scraper import scrape_article, read_urls_from_csv
import google.generativeai as genai
from dotenv import load_dotenv

CSV_URL = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"

# from scraper import scrape_all_from_csv
from geminiSummarizer import summarize_text
# from storage import save_results

def nih_scrape(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(page.text, 'html.parser')
    classes = soup.find(class_='cg p')
    title = soup.find('hgroup').text
    if (classes):
        authors = classes.find_all('h3')
        authors = classes.find_all('h3')
        author_names = [author.get_text() for author in authors]
        authorsParsed = ", ".join(author_names)
    else:
        authorsParsed = "unknown"

    #Scraping div with text I want
    temp = soup.find(class_='pmc-layout__citation')
    #Now scraping the actual date
    date_text = (temp.find('div')).text

    date = date_text[date_text.index(".")+2 : date_text.index(".")+6]

    text = scrape_article(url)
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    model = genai.GenerativeModel("gemini-2.5-pro")
    prompt=f"You are a scientific summarization assistant for NASA bioscience research. Read the following article and highlights all relevant keywords. Only put the relevant keywords in the response, separated by commas, and dont include more than 50 keywords. Article: {text[:15000]}"

    try:
        response = model.generate_content(prompt)
        raw_output = response.text.strip()

    except Exception as e:
        print(f"[ERROR] Gemini summarization failed: {e}")
        raw_output = ""

    summary_data = {"url": url, "title": title, "authors": authorsParsed, "date": date, "keywords": raw_output}
    # result.append(summary_data)
    
    # return result
    return summary_data

# save_results(nih_scrape("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4136787"))

urls = read_urls_from_csv(CSV_URL)
urls = urls[:49]

result = []
for url in urls:
    result.append(nih_scrape(url))
    print(f"Finished URL: {url}")
save_results(result)