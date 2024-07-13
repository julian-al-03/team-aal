import asyncio
import os
import wave
import ssl
from aiohttp import web
import aiohttp
from aiohttp import WSMsgType
from speechToText import wav_to_text

# Ensure the audio_files directory exists
os.makedirs('audio_files', exist_ok=True)

import traceback

async def audio_stream(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    print("Client connected")
    try:
        audio_data = b''
        filename = None
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == "start":
                    print("Starting new recording")
                    filename = f"audio_files/audio_{len(os.listdir('audio_files'))}.wav"
                elif msg.data == "stop":
                    print("Stopping recording")
                    if audio_data:
                        try:
                            print(f"Attempting to save file: {filename}")
                            with wave.open(filename, 'wb') as wav_file:
                                wav_file.setnchannels(1)
                                wav_file.setsampwidth(2)
                                wav_file.setframerate(44100)
                                wav_file.writeframes(audio_data)
                            print(f"Saved audio file: {filename}")
                            await ws.send_str(f"Audio saved as {filename}")
                            
                            # Perform speech-to-text conversion
                            try:
                                print("Starting speech-to-text conversion")
                                text = wav_to_text(filename)
                                print(f"Speech-to-text result: {text}")
                                await ws.send_str(f"Transcription: {text}")
                            except Exception as e:
                                print(f"Error in speech-to-text conversion: {e}")
                                traceback.print_exc()
                                await ws.send_str(f"Error in speech-to-text conversion: {str(e)}")
                        except Exception as e:
                            print(f"Error saving audio file: {e}")
                            traceback.print_exc()
                            await ws.send_str(f"Error saving audio file: {str(e)}")
                        finally:
                            audio_data = b''
                    else:
                        print("No audio data to save")
            elif msg.type == WSMsgType.BINARY:
                audio_data += msg.data
                print(f"Received {len(msg.data)} bytes of audio data")
            elif msg.type == WSMsgType.ERROR:
                print('WebSocket connection closed with exception %s' % ws.exception())
    except Exception as e:
        print(f"Unexpected error in audio_stream: {e}")
        traceback.print_exc()
    finally:
        print("Client disconnected")
    
    return ws
async def serve_html(request):
    return web.FileResponse('index.html')

app = web.Application()
app.router.add_get('/ws', audio_stream)
app.router.add_get('/', serve_html)

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('cert.pem', 'key.pem')

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8765, ssl_context=ssl_context)