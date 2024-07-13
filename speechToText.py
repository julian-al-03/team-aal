import speech_recognition as sr
from pydub import AudioSegment

def wav_to_text(wav_path):
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load WAV file
    audio = AudioSegment.from_wav(wav_path)
    audio.export("temp.wav", format="wav")

    # Read the audio file
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)

    # Recognize speech using Google Web Speech API (offline compatible)
    try:
        text = recognizer.recognize_google(audio_data)
        print("Text: " + text)
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")

    return text

# Example usage
wav_path = './test.wav'
text = wav_to_text(wav_path)
print(text)
