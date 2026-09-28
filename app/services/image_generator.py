from pathlib import Path

from huggingface_hub import InferenceClient

from app.config import (
    HF_TOKEN,
    IMAGE_MODEL_ID,
    PANELS_DIR
)


def generate_image(
    image_prompt: str,
    panel_number: int = 1
) -> str:

    prompt = f"""
Comic book illustration.

{image_prompt}

Style:
clear comic illustration,
strong composition,
expressive characters,
detailed environment,
cinematic lighting,
high quality,
no text,
no watermark.
"""

    client = InferenceClient(
        api_key=HF_TOKEN,
        provider="auto"
    )

    image = client.text_to_image(
        prompt=prompt,
        model=IMAGE_MODEL_ID
    )

    filename = f"panel_{panel_number}.png"
    output_path: Path = PANELS_DIR / filename

    image.save(output_path)

    return f"/static/panels/{filename}"