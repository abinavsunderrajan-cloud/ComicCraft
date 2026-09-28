import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"

STATIC_DIR = APP_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"

PANELS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GEMINI_FLASH_MODEL = os.getenv(
    "GEMINI_FLASH_MODEL",
    "gemini-3.5-flash-lite"
)

GEMINI_PRO_MODEL = os.getenv(
    "GEMINI_PRO_MODEL",
    "gemini-3.1-pro-preview"
)

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

IMAGE_MODEL_ID = os.getenv(
    "IMAGE_MODEL_ID",
    "runwayml/stable-diffusion-v1-5"
)

IMAGE_DEVICE = os.getenv(
    "IMAGE_DEVICE",
    "auto"
)

IMAGE_STEPS = int(
    os.getenv("IMAGE_STEPS", "20")
)

IMAGE_WIDTH = int(
    os.getenv("IMAGE_WIDTH", "512")
)

IMAGE_HEIGHT = int(
    os.getenv("IMAGE_HEIGHT", "512")
)


def validate_settings():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add it to the .env file."
        )