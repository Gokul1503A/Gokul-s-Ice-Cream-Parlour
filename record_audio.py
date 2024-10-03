import sounddevice as sd
import numpy as np
import wavio
import threading

# Global variables
rf = False
recorded_frames = []

def record_now():
    global rf, recorded_frames

    # Parameters
    samplerate = 44100
    duration = 5  # Duration of recording in seconds
    recorded_frames = []

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        if rf:
            recorded_frames.append(indata.copy())

    # Start recording
    with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
        while rf:
            sd.sleep(100)  # Sleep while recording

def start_recording():
    global rf
    rf = True
    recorded_frames.clear()
    threading.Thread(target=record_now, daemon=True).start()

def stop_save():
    global rf

    rf = False

    # Convert recorded frames to a single NumPy array
    if recorded_frames:
        data = np.concatenate(recorded_frames, axis=0)
        filename = 'audio.mp3'

        # Save to WAV file
        wavio.write(filename, data, 44100, sampwidth=2)
        print(f"Audio saved as {filename}")

