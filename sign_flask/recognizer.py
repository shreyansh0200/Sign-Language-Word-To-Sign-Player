import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import uuid
import os

TEMP_AUDIO = "temp_audio"
os.makedirs(TEMP_AUDIO, exist_ok=True)

def record_and_recognize(duration=4):
    """
    Records audio from the microphone and converts it to lowercase text.
    """
    fs = 44100
    print("🎤 Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("✔ Recording finished")

    filename = os.path.join(TEMP_AUDIO, f"{uuid.uuid4()}.wav")
    write(filename, fs, audio)

    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(data)
        print("Recognized:", text)
        return text.lower()
    except Exception as e:
        print("Speech recognition error:", e)
        return None
