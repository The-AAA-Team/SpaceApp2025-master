import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_article
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("[ERROR] Missing GOOGLE_API_KEY in environment or .env file.")
genai.configure(api_key=api_key)

app = Flask(__name__)
CORS(app)

file_path = './publications.json'
with open(file_path, 'r') as f:
    data = json.load(f)

@app.route("/publications")
def members():
    return data

@app.route("/summarize", methods=["POST"])
def summary():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'No title provided'}), 400
    article_title = data['title']
    print(f"Recieved article title: {article_title}")

    CSV_URL = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"
    df = pd.read_csv(CSV_URL)
    title_col = next((col for col in df.columns if 'title' in col.lower()), None)
    url_col = next((col for col in df.columns if 'link' in col.lower()), None)

    if not title_col or not url_col:
        missing_cols = []
        if not title_col: missing_cols.append("'title'")
        if not url_col: missing_cols.append("'url'")
        error_msg = f"Required columns ({', '.join(missing_cols)}) not found in the CSV headers."
        print(f"ERROR: {error_msg}")
        return jsonify({'error': error_msg}), 500
    print("got title")

    match = df[df[title_col] == article_title]

    if match.empty:
        return jsonify({'error': f"Article '{article_title}' URL not found in CSV."}), 404
    print("got match")
            
    url = match[url_col].iloc[0]
    print(f"Found URL: {url}")
    
    content = scrape_article(url)

    print("sending prompt")
    prompt = f"Summarize the following text:\n\nc{content}"

    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content(prompt)

    summary = response.text

    print(summary)

    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True, port=5000)