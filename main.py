import os
import threading
from enum import Enum
import keyboard
import numpy as np
import pyperclip
import sounddevice as sd
import whisper
from scipy.io.wavfile import write
import winsound


class WhisperModels(Enum):
    TINY_EN = "tiny.en"
    TINY = "tiny"
    BASE_EN = "base.en"
    BASE = "base"
    SMALL_EN = "small.en"
    SMALL = "small"
    MEDIUM_EN = "medium.en"
    MEDIUM = "medium"
    LARGE_V1 = "large-v1"
    LARGE_V2 = "large-v2"
    LARGE_V3 = "large-v3"
    LARGE = "large"


class AudioRecorder:
    def __init__(self, model_name=WhisperModels.MEDIUM_EN, hotkey="ctrl+shift+r"):
        self.output_folder = "output"
        self.hotkey = hotkey

        self.is_recording = False
        self.record_thread = None
        self.recordings = []

        # Load Whisper Model
        self.transcriber = whisper.load_model(model_name.value)

    def transcribe(self, audio_path: str) -> str:
        result = self.transcriber.transcribe(audio_path)
        return result["text"]

    def toggle_recording(self):
        self.start_recording() if not self.is_recording else self.stop_recording()

    def start_recording(self):
        print("*** Start Recording...")
        winsound.PlaySound("./assets/recording.wav", winsound.SND_FILENAME)

        self.is_recording = True
        self.record_thread = threading.Thread(target=self.record_audio)
        self.record_thread.start()

    def stop_recording(self):
        print("*** Stop Recording")

        self.is_recording = False

        # Stop soundDevice and join thread
        sd.stop()
        self.record_thread.join()

        if not self.recordings:
            print("No audio data recorded. Please check your audio input device.")
            exit(1)

        print("*** Creating Audio file...")

        # Concatenate and scale and convert to 16 bit PCM audio
        audio_data = np.concatenate(self.recordings)
        audio_data = (audio_data * 32767).astype(np.int16)

        # Create output directory if necessary
        os.makedirs(self.output_folder, exist_ok=True)
        filename = f"{self.output_folder}/audio.wav"

        # Write as .wav file
        write(filename, 44100, audio_data)
        print("*** Audio file created")

        # Re-initialize recordings list
        self.recordings = []

        # Start transcription
        self.process_transcription(filename)

    def record_audio(self):
        with sd.InputStream(callback=self.audio_callback):
            while self.is_recording:
                sd.sleep(1000)

    # noinspection PyUnusedLocal
    def audio_callback(self, indata, frames, time, status):
        self.recordings.append(indata.copy())

    def process_transcription(self, filename: str):
        print("*** Transcribing using Whisper...")
        transcription = self.transcribe(filename)
        print(f"*** Transcription done")

        # Add transcription to copy
        pyperclip.copy(transcription)
        winsound.PlaySound("./assets/clipboard.wav", winsound.SND_FILENAME)

        print("*** Transcription copied to clipboard")
        print("------------------------------------------------------------------")
        print(f"*** Waiting for recording ({self.hotkey})...")


def main():
    # Add ffmpeg to Windows PATH
    os.environ["PATH"] += os.pathsep + r"C:\\ffmpeg\\bin"

    hotkey = "ctrl+alt+space"
    model_name = WhisperModels.MEDIUM_EN

    # Load Instance
    app = AudioRecorder(model_name=model_name, hotkey=hotkey)

    print(f"*** Waiting for recording ({hotkey})...")

    # Registering hotkey combination
    keyboard.add_hotkey(hotkey, app.toggle_recording)

    # Running keyboard listener in loop
    keyboard.wait()


if __name__ == "__main__":
    main()
