import threading, time, os
from mss import mss
from datetime import datetime

class ScreenRecorder:
    def __init__(self, interval=2, outdir='data/screenshots'):
        self.interval = interval
        self.outdir = outdir
        os.makedirs(outdir, exist_ok=True)
        self._running = False
        self._thread = None

    def _take_loop(self):
        with mss() as sct:
            while self._running:
                ts = datetime.now().strftime('screenshot-%Y%m%d-%H%M%S-%f.png')
                filepath = os.path.join(self.outdir, ts)
                sct.shot(output=filepath)
                # print('[screen] saved', filepath)
                time.sleep(self.interval)

    def start(self):
        if self._running: return
        self._running = True
        self._thread = threading.Thread(target=self._take_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread: self._thread.join(timeout=2)
