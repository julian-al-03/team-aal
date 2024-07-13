import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import paho.mqtt.client as mqtt
import os

def detect_tone(audio_file_path):
    # Load audio file
    audio = AudioSegment.from_file(audio_file_path)

    # Convert to numpy array
    samples = np.array(audio.get_array_of_samples())

    # Perform Fourier Transform to get the frequencies
    fft_result = np.fft.fft(samples)
    freqs = np.fft.fftfreq(len(samples))

    # Find the peak frequency
    peak_freq = freqs[np.argmax(np.abs(fft_result))]

    # Assuming the peep tone is at a specific frequency, e.g., 1000 Hz
    tone_frequency = 1000
    tolerance = 50

    if abs(peak_freq - tone_frequency) < tolerance:
        return True
    return False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def send_signal_to_esp32():
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect("broker.hivemq.com", 1883, 60)
    client.publish("raspberry/command", "signal")

    client.loop_forever()

if __name__ == "__main__":
    audio_file = "path/to/your/audio/file.wav"
    if detect_tone(audio_file):
        print("Peep tone detected!")
        send_signal_to_esp32()
    else:
        print("No peep tone detected.")
