from app.config import GEMINI_API_KEY
from google import genai

if not GEMINI_API_KEY:
    print("API KEY NOT FOUND")
else:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Say hello"
        )

        print("API KEY WORKING!")
        print(response.text)

    except Exception as e:
        print("API ERROR:", type(e).__name__, e)