import os
import ssl
from aiohttp import web
import speech_recognition as sr
from pydub import AudioSegment
import io
import traceback
from configCrane import execute
from filterText import filterText
from cam import capture_and_save_frame
from imageDetect import get_color_positions

# Ensure the audio_files directory exists
os.makedirs('audio_files', exist_ok=True)

def get_color_index(color_positions, target_color):
    for color, index in color_positions.items():
        if color.lower() == target_color.lower():
            return index
    return None  # Return None if the color is not found

def webm_to_wav(webm_data):
    # Convert webm data to wav
    audio = AudioSegment.from_file(io.BytesIO(webm_data), format="webm")
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    return wav_io.getvalue()

def wav_to_text(wav_data):
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(wav_data)) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Speech Recognition service; {e}"

async def upload_audio(request):
    try:
        reader = await request.multipart()
        field = await reader.next()
        if field.name == 'audio':
            webm_data = await field.read()
            wav_data = webm_to_wav(webm_data)
            
            filename = f"audio_files/audio_{len(os.listdir('audio_files'))}.wav"
            with open(filename, 'wb') as f:
                f.write(wav_data)
            print(f"Saved audio file: {filename}")
            
            text = wav_to_text(wav_data)

            is_throw, color = filterText(text)

            path = await capture_and_save_frame()
            ml = get_color_positions(path)
            index = get_color_index(ml, color)

            execute(is_throw, index)

            return web.json_response({"message": f"Audio saved as {filename}", "transcription": text})
    except Exception as e:
        print(f"Error processing audio: {e}")
        traceback.print_exc()
        return web.json_response({"error": f"Error processing audio: {str(e)}"}, status=500)

async def serve_html(request):
    return web.FileResponse('index.html')

app = web.Application()
app.router.add_post('/upload', upload_audio)
app.router.add_get('/', serve_html)

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('cert.pem', 'key.pem')

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8765, ssl_context=ssl_context)