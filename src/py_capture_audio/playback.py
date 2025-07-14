""" simple playback feature used when previewing sounds """

import sounddevice as sd
import scipy.io.wavfile as wav

# Load and play a WAV file
def play_wav(filename):
    samplerate, data = wav.read(filename)
    sd.play(data, samplerate)
    sd.wait()
    print("▶️ Playback finished.")
