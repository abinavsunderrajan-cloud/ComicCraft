import json
import re
from pathlib import Path

from fastapi import (
    APIRouter,
    Form,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    RedirectResponse
)

from fastapi.templating import Jinja2Templates

from app.schemas import ComicRequest

from app.services.comic_service import (
    generate_comic
)


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------

@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# ---------------------------------------------------------
# Generate comic
# ---------------------------------------------------------

@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    story_tone: str = Form(...),

    art_style: str = Form(...),

    number_of_panels: int = Form(5)
):

    try:

        comic_request = ComicRequest(

            story_prompt=story_prompt,

            character_name=character_name,

            setting=setting,

            story_tone=story_tone,

            art_style=art_style,

            number_of_panels=number_of_panels
        )


        comic = generate_comic(
            comic_request
        )


        return templates.TemplateResponse(

            "comic_preview.html",

            {
                "request": request,

                "comic": comic["comic"],

                "pdf_url": comic["pdf_url"]
            }
        )


    except Exception as exc:

        return templates.TemplateResponse(

            "error.html",

            {
                "request": request,

                "error": str(exc)
            },

            status_code=500
        )


# ---------------------------------------------------------
# JSON API
# ---------------------------------------------------------

@router.post(
    "/generate-comic/json"
)
async def generate_comic_json(
    comic_request: ComicRequest
):

    try:

        result = generate_comic(
            comic_request
        )

        return JSONResponse(
            content=result
        )

    except Exception as exc:

        return JSONResponse(

            status_code=500,

            content={
                "error": str(exc)
            }
        )


# ---------------------------------------------------------
# Test image generation
# ---------------------------------------------------------

@router.get(
    "/test-image"
)
async def test_image():

    from app.services.image_generator import (
        generate_image
    )


    image_path = generate_image(

        prompt=(
            "A cute fox standing in an "
            "enchanted magical forest, "
            "fantasy comic illustration"
        ),

        panel_number=999
    )


    return {
        "message": "Image generated successfully",
        "image": image_path
    }


# ---------------------------------------------------------
# Export success
# ---------------------------------------------------------

@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(
    request: Request,
    pdf_url: str = ""
):

    return templates.TemplateResponse(

        "export_success.html",

        {
            "request": request,
            "pdf_url": pdf_url
        }
    )


# ---------------------------------------------------------
# Download PDF
# ---------------------------------------------------------

@router.get(
    "/download/{filename}"
)
async def download_pdf(
    filename: str
):

    safe_filename = re.sub(
        r"[^a-zA-Z0-9_.-]",
        "",
        filename
    )


    if not safe_filename.endswith(".pdf"):

        return JSONResponse(

            status_code=400,

            content={
                "error": "Invalid PDF filename"
            }
        )


    file_path = (
        Path("app/static/exports")
        / safe_filename
    )


    if not file_path.exists():

        return JSONResponse(

            status_code=404,

            content={
                "error": "PDF file not found"
            }
        )


    return RedirectResponse(
        url=f"/static/exports/{safe_filename}"
    )