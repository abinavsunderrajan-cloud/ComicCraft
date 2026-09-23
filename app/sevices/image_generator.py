from pathlib import Path

import torch

from diffusers import (
    StableDiffusionPipeline
)

from app.config import (
    HF_TOKEN,
    IMAGE_MODEL_ID,
    IMAGE_DEVICE,
    IMAGE_STEPS,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    PANELS_DIR
)


_pipeline = None


def get_pipeline():

    global _pipeline


    if _pipeline is not None:

        return _pipeline


    if torch.cuda.is_available():

        device = "cuda"

    else:

        device = "cpu"


    if IMAGE_DEVICE != "auto":

        device = IMAGE_DEVICE


    kwargs = {}


    if HF_TOKEN:

        kwargs["token"] = HF_TOKEN


    _pipeline = StableDiffusionPipeline.from_pretrained(

        IMAGE_MODEL_ID,

        **kwargs
    )


    _pipeline = _pipeline.to(
        device
    )


    return _pipeline


def generate_image(
    prompt: str,
    panel_number: int
) -> str:

    pipeline = get_pipeline()


    full_prompt = f"""
Comic book illustration.

{prompt}

High quality comic art,
clear composition,
strong storytelling,
consistent character,
detailed background,
cinematic lighting.
"""


    result = pipeline(

        prompt=full_prompt,

        num_inference_steps=IMAGE_STEPS,

        width=IMAGE_WIDTH,

        height=IMAGE_HEIGHT
    )


    image = result.images[0]


    filename = (
        f"panel_{panel_number}.png"
    )


    file_path = (
        Path(PANELS_DIR)
        / filename
    )


    image.save(
        file_path
    )


    return (
        f"/static/panels/{filename}"
    )