import os, argparse, time, threading, json, uuid
from datetime import datetime
from capture.screen_recorder import ScreenRecorder
from capture.audio_recorder import AudioRecorder
from processing.ocr_extractor import extract_ocr_from_image
from processing.stt_transcriber import transcribe_audio_file
from processing.summarizer import summarize_session
import yaml

cfg = yaml.safe_load(open("config.yaml","r"))

def timestamp(): return datetime.now().strftime("%Y%m%d-%H%M%S")

def run_session(duration=60):
    out = cfg.get('OUTPUT_FOLDER','data')
    os.makedirs(out, exist_ok=True)
    os.makedirs(os.path.join(out,"screenshots"), exist_ok=True)
    os.makedirs(os.path.join(out,"audio"), exist_ok=True)
    os.makedirs(os.path.join(out,"transcripts"), exist_ok=True)
    os.makedirs("output", exist_ok=True)

    sr = ScreenRecorder(interval=cfg.get('SCREENSHOT_INTERVAL_SEC',2), outdir=os.path.join(out,"screenshots"))
    ar = AudioRecorder(segment_seconds=cfg.get('AUDIO_SEGMENT_SEC',4), outdir=os.path.join(out,"audio"))

    print("[+] Starting screen recorder and audio recorder...")
    sr.start()
    ar.start()

    start_ts = datetime.now().isoformat()
    time.sleep(duration)
    print("[+] Stopping recorders...")
    sr.stop()
    ar.stop()

    # Process captured files into timeline
    timeline = {
        'session_id': str(uuid.uuid4()),
        'start_time': start_ts,
        'end_time': datetime.now().isoformat(),
        'events': [],
        'transcript': []
    }

    # OCR each screenshot
    print("[+] Running OCR on screenshots...")
    for fname in sorted(os.listdir(os.path.join(out,'screenshots'))):
        path = os.path.join(out,'screenshots', fname)
        text = extract_ocr_from_image(path)
        timeline['events'].append({
            'ts': fname.replace('screenshot-','').replace('.png',''),
            'type': 'screenshot',
            'file': path,
            'ocr_text': text
        })

    # Transcribe each audio segment
    print("[+] Transcribing audio segments (Vosk)...")
    for fname in sorted(os.listdir(os.path.join(out,'audio'))):
        path = os.path.join(out,'audio', fname)
        txt = transcribe_audio_file(path)
        t = fname.replace('segment-','').replace('.wav','')
        timeline['transcript'].append({'ts': t, 'text': txt})

    # Summarize / produce suggestions
    print("[+] Summarizing session...")
    summary, suggestions = summarize_session(timeline)
    timeline['summary'] = summary
    timeline['automations_suggested'] = suggestions

    outfname = os.path.join('output', f"session_{timestamp()}_{timeline['session_id'][:8]}.json")
    with open(outfname,'w', encoding='utf-8') as f:
        json.dump(timeline, f, indent=2)
    print(f"[+] Session JSON written: {outfname}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--duration', type=int, default=60, help='record duration in seconds')
    args = p.parse_args()
    run_session(duration=args.duration)
