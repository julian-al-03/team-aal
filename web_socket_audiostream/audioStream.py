import os
import wave
import ssl
from aiohttp import web
import speech_recognition as sr
from pydub import AudioSegment
import io
import traceback

# Ensure the audio_files directory exists
os.makedirs('audio_files', exist_ok=True)

def wav_to_text(wav_path):
    # Your existing wav_to_text function here
    pass

async def upload_audio(request):
    try:
        data = await request.read()
        filename = f"audio_files/audio_{len(os.listdir('audio_files'))}.wav"
        
        print(f"Attempting to save file: {filename}")
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(44100)
            wav_file.writeframes(data)
        print(f"Saved audio file: {filename}")
        
        # Perform speech-to-text conversion
        try:
            print("Starting speech-to-text conversion")
            text = wav_to_text(filename)
            print(f"Speech-to-text result: {text}")
            return web.json_response({"message": f"Audio saved as {filename}", "transcription": text})
        except Exception as e:
            print(f"Error in speech-to-text conversion: {e}")
            traceback.print_exc()
            return web.json_response({"error": f"Error in speech-to-text conversion: {str(e)}"}, status=500)
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