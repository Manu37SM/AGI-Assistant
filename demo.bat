\
@echo off
REM Demo runner for Windows: records for 60 seconds and exits
python -m venv .venv 2>nul
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
) else (
    echo "Activate your python environment manually before running demo.bat"
)
pip install -r requirements.txt
echo Running demo for 60 seconds...
python main.py --duration 60
pause
