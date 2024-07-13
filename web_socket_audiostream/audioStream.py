import asyncio
import os
import wave
from aiohttp import web
import aiohttp
from aiohttp import WSMsgType
from speechToText import wav_to_text

# Ensure the audio_files directory exists
os.makedirs('audio_files', exist_ok=True)

async def audio_stream(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    print("Client connected")
    try:
        audio_data = b''
        filename = None
        wav_file = None
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == "start":
                    print("Starting new recording")
                    filename = f"audio_files/audio_{len(os.listdir('audio_files'))}.wav"
                    wav_file = wave.open(filename, 'wb')
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(44100)
                elif msg.data == "stop":
                    print("Stopping recording")
                    if wav_file:
                        wav_file.close()
                        print(f"Saved audio file: {filename}")
                        await ws.send_str(f"Audio saved as {filename}")
                        
                        # Perform speech-to-text conversion
                        try:
                            text = wav_to_text(filename)
                            await ws.send_str(f"Transcription: {text}")
                        except Exception as e:
                            print(f"Error in speech-to-text conversion: {e}")
                            await ws.send_str(f"Error in speech-to-text conversion: {str(e)}")
            elif msg.type == WSMsgType.BINARY:
                if wav_file:
                    wav_file.writeframes(msg.data)
            elif msg.type == WSMsgType.ERROR:
                print('WebSocket connection closed with exception %s' % ws.exception())
    finally:
        print("Client disconnected")
        if wav_file:
            wav_file.close()
    
    return ws

async def serve_html(request):
    return web.FileResponse('index.html')

app = web.Application()
app.router.add_get('/ws', audio_stream)
app.router.add_get('/', serve_html)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8765)
