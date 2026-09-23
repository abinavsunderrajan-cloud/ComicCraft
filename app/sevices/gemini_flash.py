from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_FLASH_MODEL
)

from app.schemas import (
    ComicOutline
)


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    story_tone: str,
    art_style: str,
    number_of_panels: int
) -> ComicOutline:

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is missing."
        )


    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


    prompt = f"""
You are an expert comic book story planner.

Create a structured comic outline.

Story prompt:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Story tone:
{story_tone}

Art style:
{art_style}

Number of panels:
{number_of_panels}

Requirements:

1. Create a suitable comic title.
2. Create exactly {number_of_panels} panels.
3. Every panel must move the story forward.
4. Give every panel a short title.
5. Give every panel a visual description.
6. Keep the main character consistent.
7. Make the story suitable for a comic.
"""


    response = client.models.generate_content(

        model=GEMINI_FLASH_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=ComicOutline
        )
    )


    if not response.parsed:

        raise RuntimeError(
            "Gemini Flash did not return a valid outline."
        )


    return response.parsed