from flask import Flask, request, jsonify
from google import genai
import json


app = Flask(__name__)
file_path = './publications.json'
with open(file_path, 'r') as f:
    data = json.load(f)

@app.route("/publications")
def members():
    return data

@app.route("/summarize", methods=["POST"])
def summary():
    data = request.json()
    title = data.get("title")

    prompt = f"Summarize the following text:\n\n"

    response = client.model.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    summary = response.text

    return jsonify({"summary", summary})

if __name__ == "__main__":
    app.run(debug=True)