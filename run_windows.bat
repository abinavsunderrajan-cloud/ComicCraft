@echo off

echo ==========================================
echo        ComicCraft AI Comic Creator
echo ==========================================

echo.

if not exist ".venv" (

    echo Creating virtual environment...

    python -m venv .venv

)


echo.

echo Activating virtual environment...

call .venv\Scripts\activate


echo.

echo Installing requirements...

python -m pip install --upgrade pip

pip install -r requirements.txt


echo.

echo Starting ComicCraft...

uvicorn app.main:app --reload

pause