from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


app = FastAPI(
    title="ComicCraft",
    description="AI Comic Story Creator using Gemini and Stable Diffusion",
    version="1.0.0"
)


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

app.include_router(router)


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "ComicCraft"
    }