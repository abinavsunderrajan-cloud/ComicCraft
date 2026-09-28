import re

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request
)
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import APP_DIR
from app.schemas import ComicRequest
from app.services.comic_service import generate_comic


router = APIRouter()

templates = Jinja2Templates(
    directory=str(APP_DIR / "templates")
)


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"title": "Home"}
)

@router.post("/generate")
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

        result = generate_comic(comic_request)

        return templates.TemplateResponse(
    request=request,
    name="comic_preview.html",
    context={
        "comic": result["comic"],
        "pdf_url": result["pdf_url"]
    }
)
    except Exception as exc:
        import traceback
        traceback.print_exc()

        return templates.TemplateResponse(
    request=request,
    name="error.html",
    context={
        "error": str(exc)
    },
    status_code=500
)


@router.post("/generate-comic/json")
async def generate_comic_json(
    comic_request: ComicRequest
):
    try:
        result = generate_comic(comic_request)

        return JSONResponse(
            content=result
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.get("/test-image")
async def test_image():
    try:
        from app.services.image_generator import generate_image

        image_url = generate_image(
            "A colorful comic book illustration "
            "of a young hero standing in a magical forest"
        )

        return {
            "status": "success",
            "image_url": image_url
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.get("/export-success")
async def export_success(
    request: Request,
    pdf_url: str = ""
):
    return templates.TemplateResponse(
    request=request,
    name="export_success.html",
    context={
        "pdf_url": pdf_url
    }
)


@router.get("/download/{filename}")
async def download_file(filename: str):
    safe_filename = re.sub(
        r"[^a-zA-Z0-9_.-]",
        "",
        filename
    )

    return RedirectResponse(
        url=f"/static/exports/{safe_filename}"
    )