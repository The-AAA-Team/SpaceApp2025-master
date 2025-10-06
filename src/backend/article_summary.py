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
from io import StringIO

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

CSV_URL = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"

@app.route("/summarize", methods=["POST"])
def summary():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'No title provided'}), 400
    article_title = data['title'].strip()
    print(f"Recieved article title: {article_title}")

    try:
        response = requests.get(CSV_URL, timeout=10)
        response.raise_for_status() # Raises an exception for bad status codes (4xx or 5xx)
        # Use StringIO to read the response text as a file
        df = pd.read_csv(StringIO(response.text))
        print(f"Successfully loaded CSV with columns: {df.columns.tolist()}")

    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to fetch CSV from URL: {e}"
        print(f"ERROR: {error_msg}")
        return jsonify({'error': error_msg}), 500
    
    print(article_title)
    print(df['Title'][0])

    for i in range(len(df['Title'])):
        test = df['Title'][i].lower()
        print(test)
        if (test == article_title.lower()):
            print('found')
            break
    
    # 3. CORRECT MATCHING LOGIC using Pandas filtering
    # Find all rows where the 'Title' column exactly matches the requested article_title
    matching_rows = df[df['Title'].str.lower() == article_title.lower()]
    print(matching_rows)

    if matching_rows.empty:
        print(f"ERROR: Article '{article_title}' URL not found in CSV.")
        return jsonify({'error': f"Article '{article_title}' URL not found in CSV."}), 404

    # Extract the 'Link' (URL) from the first matching row
    url = matching_rows['Link'].iloc[0].strip()

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