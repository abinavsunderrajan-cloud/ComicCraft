def build_comic_layout(
    comic_story,
    image_urls
):
    panels = []

    for panel, image_url in zip(
        comic_story.panels,
        image_urls
    ):
        panels.append(
            {
                "panel_number": panel.panel_number,
                "title": panel.title,
                "image_url": image_url,
                "narration": panel.narration,
                "dialogue": panel.dialogue,
                "character": panel.character,
                "image_prompt": panel.image_prompt
            }
        )

    return {
        "title": comic_story.title,
        "panels": panels
    }