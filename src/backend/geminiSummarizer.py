# gemini_summarizer.py
import os
import google.generativeai as genai

# Configure Gemini API
os.environ["GOOGLE_API_KEY"] = "AIzaSyDaLPwCTqHAUh6wonNmvzQZ4gQeERgOrNA"  # replace with your real key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def summarize_text(text):
    """
    Sends text to Gemini and returns a concise summary.
    Automatically trims long input to stay under token limits.
    """
    if not text:
        return "No content provided."

    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Summarize the following scientific article in 5–7 concise bullet points.
    Focus on:
    - Research purpose
    - Key findings
    - Methods used
    - Conclusions
    - Any implications or future work

    Article Text:
    {text[:15000]}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Gemini summarization failed: {e}")
        return None
