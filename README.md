# The AGI Assistant — MVP

A local, offline MVP that records screenshots and short audio segments, performs OCR (Tesseract) and STT (Vosk), and produces a structured JSON timeline + simple rule-based summary. This project is Windows-first and tailored for the hackathon Round 1 (Observe & Understand).

---
## What's included
- `main.py` — orchestrator (starts capture + processing and writes an output JSON)
- `capture/screen_recorder.py` — screenshot capture (mss)
- `capture/audio_recorder.py` — audio capture (sounddevice) saving short WAV segments
- `processing/ocr_extractor.py` — uses pytesseract on screenshots
- `processing/stt_transcriber.py` — uses Vosk model to transcribe WAV segments
- `processing/summarizer.py` — combines OCR + STT into a timeline JSON
- `requirements.txt` — pip dependencies
- `demo.bat` — Windows demo runner (runs main for ~60 seconds)
- `/data/` — folders created by runtime (screenshots, audio, transcripts, output)

---
## Prerequisites
1. Install Python 3.10+ from https://python.org and make sure `python` and `pip` are on PATH.
2. Install FFmpeg (optional for recording clips) and add to PATH: https://ffmpeg.org/download.html
3. Install Tesseract OCR (for `pytesseract`) — recommended Windows build: https://github.com/UB-Mannheim/tesseract/wiki
   - After install, add the Tesseract `tesseract.exe` folder to PATH (or update `TESSERACT_CMD` in `config.yaml`).
4. Download a Vosk model (small) and place it in `models/vosk-model-small`.
   - Example small English model: https://alphacephei.com/vosk/models (download and unzip to `models/vosk-model-small`)
   - Recommended: `vosk-model-small-en-us-0.15` (or similar).
5. (Optional) Create and activate a Python virtual environment.

---
## Quick setup & run (one-time)
Open PowerShell or CMD in the project folder and run:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Edit `config.yaml` if your Tesseract executable or Vosk model path differs.

Run the demo (records ~60 seconds and writes JSON):
```powershell
demo.bat
# or
python main.py --duration 60
```

Outputs will be under `data/` and a JSON under `output/`.
