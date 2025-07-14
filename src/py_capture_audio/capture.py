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

import logging
import sounddevice
import numpy as np
import keyboard
import wave
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fs = 44100  # Sample rate
recording = []
is_recording = False

def get_input_device():
    for i, dev in enumerate(sounddevice.query_devices()):
        if "Stereo Mix" in dev['name']:
            return i

def audio_callback(indata, frames, time_info, status):
    global recording, is_recording
    if is_recording:
        recording.append(indata.copy())

def save_recording(audio):
    filename = f"recording_{int(time.time())}.wav"
    audio = (audio * 32767).astype(np.int16)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
    logger.info(f"💾 Saved to {filename}")
    return filename

def play_audio(filename):
    import scipy.io.wavfile as wav
    samplerate, data = wav.read(filename)
    sounddevice.play(data, samplerate)
    sounddevice.wait()
    logger.info("▶️ Playback finished.")

def record_audio():
    global is_recording, recording
    input_device = get_input_device()
    logger.info("Press SPACE to start/stop recording. Press ESC to quit.")
    with sounddevice.InputStream(callback=audio_callback, channels=1, samplerate=fs, device=input_device):
        while True:
            if keyboard.is_pressed("space"):
                if not is_recording:
                    logger.info("🔴 Recording...")
                    # recording = []
                    is_recording = True
                else:
                    logger.info("⏹️ Stopped recording.")
                    is_recording = False
                    if recording:  # Only concatenate if not empty
                        audio = np.concatenate(recording)
                        filename = save_recording(audio)
                        play_audio(filename)
                    else:
                        logger.warning("No audio data recorded.")
                while keyboard.is_pressed("space"):
                    time.sleep(0.1)
            elif keyboard.is_pressed("esc"):
                logger.info("Exiting.")
                break
            time.sleep(0.05)

if __name__ == "__main__":
    record_audio()