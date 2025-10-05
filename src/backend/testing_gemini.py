import google.generativeai as genai

genai.configure(api_key="AIzaSyBsQbvaYpqmABR7tGqgH9t_-k6GawjMlys")

print("Available models:")
for m in genai.list_models():
    print(" -", m.name)

model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content("Summarize this: Gemini is a Google AI model.")
print("\nGemini response:\n", response.text)
