import sounddevice
import soundfile
import numpy
import keyboard
from time import sleep
from .playback import play_audio
import logging

from .source import get_source

logging.basicConfig(level=logging.INFO, format="%(message)s")

# TODO - Add support for different audio inputs
def get_input_device():
    logging.info("\nPolling available audio input devices:")
    devices = sounddevice.query_devices()
    # look for Stereo Mix or similar device
    for i, dev in enumerate(devices):
        logging.info(f"{i}: {dev['name']}")
        if "Stereo Mix" in dev['name']:
            return i
    idx = int(input("Enter device index: "))
    return idx

def record_audio(filename="output.wav", samplerate=44100, channels=2):
    input_device = 16 #get_input_device()
    frames = []
    recording = [False]

    logging.info("Press SPACE to start recording...")
    keyboard.wait("space")
    logging.info("🔴 Recording... Press SPACE again to stop.")
    sleep(0.2)

    def callback(indata, frame_count, time_info, status):
        if recording[0]:
            frames.append(indata.copy())

    recording[0] = True
    with sounddevice.InputStream(samplerate=samplerate, channels=channels, device=input_device, callback=callback):
        while True:
            if keyboard.is_pressed("space"):
                logging.info("⏹️ Stopped recording.")
                recording[0] = False
                while keyboard.is_pressed("space"):
                    sleep(0.1)
                break
            sleep(0.05)

    logging.info(f"Frames recorded: {len(frames)}")
    if frames:
        audio = numpy.concatenate(frames)
        soundfile.write(filename, audio, samplerate)
        logging.info(f"✅ Saved to '{filename}'")
        return filename
    else:
        logging.info("No audio data recorded.")
        return None

def handle_keys():
    """
    Selects the appropriate audio input device and manages recording and playback.
    """

    source = get_source()

    last_sample = None
    logging.info("Press SPACE to record, P to play last sample, ESC to exit.")
    while True:
        if keyboard.is_pressed("space"):
            while keyboard.is_pressed("space"):
                sleep(0.1)
            last_sample = record_audio()
        elif keyboard.is_pressed("p"):
            if last_sample:
                logging.info("Playing last recorded sample...")
                play_audio(last_sample)
            else:
                logging.info("No sample recorded yet.")
            while keyboard.is_pressed("p"):
                sleep(0.1)
        elif keyboard.is_pressed("esc"):
            logging.info("Exiting.")
            break
        sleep(0.05)