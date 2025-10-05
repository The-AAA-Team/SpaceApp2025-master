# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# from scraper import scrape_all_from_csv
from geminiSummarizer import summarize_text
# from storage import save_results

def osdr_scrape_web(url):
        # headers = {'User-Agent': 'Mozilla/5.0'}
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(30)

        driver.get(url)
        time.sleep(5)
        print(driver.find_element(By.TAG_NAME, "p").is_displayed())
        element = driver.find_element(By.CLASS_NAME, "ws-pre-line")
        
        return element.text
    
print(summarize_text(osdr_scrape_web("https://osdr.nasa.gov/bio/repo/data/studies/OSD-772")))