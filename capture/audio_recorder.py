import sounddevice as sd
import wavio
import threading, time, os
from datetime import datetime

class AudioRecorder:
    def __init__(self, segment_seconds=4, samplerate=16000, channels=1, outdir='data/audio'):
        self.segment_seconds = segment_seconds
        self.samplerate = samplerate
        self.channels = channels
        self.outdir = outdir
        os.makedirs(outdir, exist_ok=True)
        self._running = False
        self._thread = None

    def _record_loop(self):
        while self._running:
            ts = datetime.now().strftime('segment-%Y%m%d-%H%M%S-%f.wav')
            filepath = os.path.join(self.outdir, ts)
            # record for segment_seconds
            print('[audio] recording segment', filepath)
            data = sd.rec(int(self.segment_seconds * self.samplerate), samplerate=self.samplerate, channels=self.channels, dtype='int16')
            sd.wait()
            wavio.write(filepath, data, self.samplerate, sampwidth=2)
            time.sleep(0.1)

    def start(self):
        if self._running: return
        self._running = True
        self._thread = threading.Thread(target=self._record_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread: self._thread.join(timeout=2)
