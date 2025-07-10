import sounddevice as sd
import scipy.io.wavfile as wav

# Load and play a WAV file
def play_wav(filename):
    samplerate, data = wav.read(filename)
    sd.play(data, samplerate)
    sd.wait()
    print("▶️ Playback finished.")

play_wav("recording_1752168199.wav")