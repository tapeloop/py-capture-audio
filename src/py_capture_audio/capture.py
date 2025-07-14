""" main capture functionality used in library """
from time import sleep

# import sounddevice
# import numpy as np
# import keyboard
# import wave
# import time
# import scipy.io.wavfile as wav
#
# # Load and play a WAV file
# def play_wav(filename):
#     samplerate, data = wav.read(filename)
#     sounddevice.play(data, samplerate)
#     sounddevice.wait()
#     print("▶️ Playback finished.")
#
# def get_input_device():
#     print("\nAvailable audio input devices:")
#     # look for Stereo Mix
#     for i, dev in enumerate(sounddevice.query_devices()):
#         if "Stereo Mix" in dev['name']:
#             return i
#
# fs = 44100  # Sample rate
# recording = []
# is_recording = False
#
# print("Press SPACE to start/stop recording. Press ESC to quit.")
#
# def toggle_recording():
#     global is_recording, recording
#     if not is_recording:
#         print("🔴 Recording...")
#         recording = []
#         is_recording = True
#     else:
#         print("⏹️ Stopped recording.")
#         is_recording = False
#         save_recording(np.concatenate(recording))
#
# def save_recording(audio):
#     filename = f"recording_{int(time.time())}.wav"
#     audio = (audio * 32767).astype(np.int16)  # Convert to 16-bit PCM
#     with wave.open(filename, 'wb') as wf:
#         wf.setnchannels(1)
#         wf.setsampwidth(2)
#         wf.setframerate(fs)
#         wf.writeframes(audio.tobytes())
#     print(f"💾 Saved to {filename}")
#
# # Continuously listen for keyboard input and audio input
# def audio_callback(indata, frames, time, status):
#     if is_recording:
#         recording.append(indata.copy())
#
# ## need to set the inputstream to use speciifc devie
# with sounddevice.InputStream(callback=audio_callback, channels=1, samplerate=fs):
#     while True:
#         if keyboard.is_pressed("space"):
#             toggle_recording()
#             while keyboard.is_pressed("space"):  # Wait for key release
#                 time.sleep(0.1)
#         elif keyboard.is_pressed("esc"):
#             print("Exiting.")
#             break
#         time.sleep(0.05)


import sounddevice
import soundfile
import scipy.io.wavfile as wav


def get_input_device():
    print("\nAvailable audio input devices:")
    # look for Stereo Mix
    for i, dev in enumerate(sounddevice.query_devices()):
        if "Stereo Mix" in dev['name']:
            return i

def play_wav(filename):
    samplerate, data = wav.read(filename)
    sounddevice.play(data, samplerate)
    sounddevice.wait()
    print("▶️ Playback finished.")


def record_audio(filename="output.wav", duration=5, samplerate=44100, channels=2):
    input_device = get_input_device()
    print(f"\n🎙️ Recording from device index {input_device}...")
    audio = sounddevice.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, device=input_device)
    sounddevice.wait()
    soundfile.write(filename, audio, samplerate)
    print(f"✅ Saved to '{filename}'")
    sleep(5)
    print(f"playing {filename}")
    play_wav(filename)


if __name__ == "__main__":
    record_audio()