from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_FLASH_MODEL
)
from app.schemas import ComicOutline


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    story_tone: str,
    art_style: str,
    number_of_panels: int
) -> ComicOutline:

    prompt = f"""
Create a comic story outline.

Story idea:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{story_tone}

Art style:
{art_style}

Number of panels:
{number_of_panels}

Create exactly {number_of_panels} panels.

For every panel provide:
- panel number
- title
- scene description
- detailed image prompt

The story should have a clear beginning,
middle, and ending.
Make the panels connected and suitable
for a comic.
"""

    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicOutline
        )
    )

    if response.parsed:
        return response.parsed

    raise RuntimeError(
        "Gemini Flash did not return a valid comic outline."
    )