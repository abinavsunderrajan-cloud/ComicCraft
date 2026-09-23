from app.schemas import ComicRequest

from app.services.gemini_flash import (
    generate_outline
)

from app.services.gemini_pro import (
    generate_story
)

from app.services.image_generator import (
    generate_image
)

from app.services.layout_builder import (
    build_comic_layout
)

from app.services.exporters import (
    save_pdf
)


def generate_comic(
    request: ComicRequest
):

    # -----------------------------------------------------
    # STEP 1: Generate outline
    # -----------------------------------------------------

    outline = generate_outline(

        story_prompt=request.story_prompt,

        character_name=request.character_name,

        setting=request.setting,

        story_tone=request.story_tone,

        art_style=request.art_style,

        number_of_panels=request.number_of_panels
    )


    # -----------------------------------------------------
    # STEP 2: Generate detailed story
    # -----------------------------------------------------

    story = generate_story(

        outline=outline,

        character_name=request.character_name,

        setting=request.setting,

        story_tone=request.story_tone
    )


    # -----------------------------------------------------
    # STEP 3: Generate images
    # -----------------------------------------------------

    image_paths = []


    for panel in story.panels:

        image_prompt = f"""
Character:
{request.character_name}

Setting:
{request.setting}

Art style:
{request.art_style}

Story tone:
{request.story_tone}

Panel title:
{panel.title}

Narration:
{panel.narration}

Dialogue:
{panel.dialogue}

Create an illustration that visually represents
this comic panel.
"""


        image_url = generate_image(

            prompt=image_prompt,

            panel_number=panel.panel_number
        )


        image_paths.append(
            image_url
        )


    # -----------------------------------------------------
    # STEP 4: Build comic layout
    # -----------------------------------------------------

    comic = build_comic_layout(

        story=story,

        image_paths=image_paths
    )


    # -----------------------------------------------------
    # STEP 5: Export PDF
    # -----------------------------------------------------

    pdf_url = save_pdf(
        comic
    )


    return {

        "comic": comic,

        "pdf_url": pdf_url
    }