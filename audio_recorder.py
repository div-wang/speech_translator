import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import threading
import queue

class AudioRecorder:
    def __init__(self, rate=16000, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.audio_queue = queue.Queue()
        self.is_recording = False
        
    def start_recording(self):
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._record)
        self.recording_thread.start()

    def _record(self):
        with sd.InputStream(samplerate=self.rate, channels=1, dtype='int16',
                          blocksize=self.chunk, callback=self._audio_callback):
            while self.is_recording:
                sd.sleep(100)

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"状态: {status}")
        self.audio_queue.put(indata.copy())

    def stop_recording(self):
        self.is_recording = False
        if hasattr(self, 'recording_thread'):
            self.recording_thread.join()

    def get_audio_data(self):
        if self.audio_queue.empty():
            return None
        return self.audio_queue.get() 