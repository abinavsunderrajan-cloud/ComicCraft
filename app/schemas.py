from typing import List

from pydantic import BaseModel, Field


class ComicRequest(BaseModel):

    story_prompt: str = Field(
        min_length=3
    )

    character_name: str = Field(
        min_length=1
    )

    setting: str = Field(
        min_length=1
    )

    story_tone: str = Field(
        min_length=1
    )

    art_style: str = Field(
        min_length=1
    )

    number_of_panels: int = Field(
        default=5,
        ge=3,
        le=10
    )


class PanelOutline(BaseModel):

    panel_number: int

    title: str

    description: str


class ComicOutline(BaseModel):

    title: str

    panels: List[PanelOutline]


class PanelStory(BaseModel):

    panel_number: int

    title: str

    narration: str

    dialogue: str

    character: str


class ComicStory(BaseModel):

    title: str

    panels: List[PanelStory]