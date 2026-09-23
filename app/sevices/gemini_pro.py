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


def generate_story(
    outline: ComicOutline,
    character_name: str,
    setting: str,
    story_tone: str
) -> ComicStory:

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is missing."
        )


    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


    outline_text = outline.model_dump_json(
        indent=2
    )


    prompt = f"""
You are an expert comic book writer.

Turn the following comic outline into
a complete panel-by-panel comic script.

Main character:
{character_name}

Setting:
{setting}

Tone:
{story_tone}

Comic outline:

{outline_text}


For every panel provide:

- panel number
- title
- narration
- dialogue
- character

Requirements:

1. Keep the character consistent.
2. Keep the story coherent.
3. Keep narration concise.
4. Make dialogue natural.
5. Make the content suitable for a comic.
6. Do not add extra panels.
"""


    response = client.models.generate_content(

        model=GEMINI_PRO_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=ComicStory
        )
    )


    if not response.parsed:

        raise RuntimeError(
            "Gemini Pro did not return a valid story."
        )


    return response.parsed