# gemini_summarizer.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("[ERROR] Missing GOOGLE_API_KEY in environment or .env file.")
genai.configure(api_key=api_key)

def summarize_text(text: str):
    """
    Uses Gemini to produce a structured summary including title, author, and key sections.
    Returns a dictionary formatted for your data pipeline.
    """
    if not text or len(text.strip()) == 0:
        return {"error": "Empty input text"}

    # Choose best available model
    model = genai.GenerativeModel("gemini-2.5-pro")

    prompt = f"""
    You are a scientific summarization assistant for NASA bioscience research.
    Read the following article and output a JSON object with these fields:

    {{
      "title": "Concise, descriptive title",
      "author": "Main author name if identifiable, else Unknown",
      "summary": "Overall summary in 5–7 concise bullet points",
      "sections": {{
        "Research Purpose": "...",
        "Methods Used": "...",
        "Key Findings": "...",
        "Conclusions": "...",
        "Implications & Future Work": "..."
      }}
    }}

    Keep the output machine-readable JSON only — no commentary or extra text.
    Article:
    {text[:15000]}
    """

    try:
        response = model.generate_content(prompt)
        raw_output = response.text.strip()

        # Gemini sometimes outputs fenced JSON ```json ... ```
        import re, json
        raw_output = re.sub(r"^```json|```$", "", raw_output).strip()

        # Attempt to parse the JSON safely
        try:
            result = json.loads(raw_output)
        except json.JSONDecodeError:
            result = {"summary": raw_output}

        return result

    except Exception as e:
        print(f"[ERROR] Gemini summarization failed: {e}")
        return {"error": str(e)}
