""" simple playback feature used when previewing sounds """

import sounddevice
import scipy.io.wavfile as wav

import logging

def play_audio(filename):
    samplerate, data = wav.read(filename)
    sounddevice.play(data, samplerate)
    sounddevice.wait()
    logging.info("▶️ Playback finished.")
