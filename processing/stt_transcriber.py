import os, wave, json, yaml
from vosk import Model, KaldiRecognizer

cfg = yaml.safe_load(open('config.yaml','r'))
MODEL_PATH = cfg.get('VOSK_MODEL_PATH', 'models/vosk-model-small')

# Lazy load model
_model = None
def _get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Vosk model not found at {MODEL_PATH}. Please download and set path in config.yaml")
        _model = Model(MODEL_PATH)
    return _model

def transcribe_audio_file(wav_path):
    try:
        wf = wave.open(wav_path, 'rb')
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in (8000,16000,32000,44100,48000):
            # try to read but Vosk expects PCM WAV; best to match 16000 mono
            pass
        rec = KaldiRecognizer(_get_model(), wf.getframerate())
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                results.append(res.get('text',''))
        # final partial
        final = json.loads(rec.FinalResult())
        results.append(final.get('text',''))
        txt = ' '.join([r for r in results if r])
        return txt.strip()
    except Exception as e:
        print('[stt] error', e)
        return ''
