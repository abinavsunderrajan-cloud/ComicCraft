from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_PRO_MODEL
)
from app.schemas import (
    ComicOutline,
    ComicStory
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_story(
    outline: ComicOutline
) -> ComicStory:

    outline_json = outline.model_dump_json()

    prompt = f"""
Turn the following comic outline into a detailed
comic story.

Comic outline:
{outline_json}

For every panel provide:
- panel number
- title
- narration
- character dialogue
- character name
- image prompt

Keep the story coherent across all panels.

Narration should be concise enough for a comic page.
Dialogue should sound natural and engaging.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicStory
        )
    )

    if response.parsed:
        return response.parsed

    raise RuntimeError(
        "Gemini Pro did not return a valid comic story."
    )