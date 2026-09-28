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

    outline = generate_outline(
        story_prompt=request.story_prompt,
        character_name=request.character_name,
        setting=request.setting,
        story_tone=request.story_tone,
        art_style=request.art_style,
        number_of_panels=request.number_of_panels
    )

    story = generate_story(
        outline
    )

    image_urls = []

    for panel in story.panels:

        image_url = generate_image(
            image_prompt=panel.image_prompt,
            panel_number=panel.panel_number
        )

        image_urls.append(
            image_url
        )

    comic = build_comic_layout(
        story,
        image_urls
    )

    pdf_url = save_pdf(
        comic
    )

    return {
        "comic": comic,
        "pdf_url": pdf_url
    }