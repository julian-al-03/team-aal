import asyncio
import websockets
import os
import wave
from websockets.exceptions import ConnectionClosedOK

# Ensure the audio_files directory exists
os.makedirs('audio_files', exist_ok=True)

async def audio_stream(websocket, path):
    print("Client connected")
    try:
        audio_data = b''
        filename = None
        wav_file = None
        async for message in websocket:
            if message == "start":
                print("Starting new recording")
                filename = f"audio_files/audio_{len(os.listdir('audio_files'))}.wav"
                wav_file = wave.open(filename, 'wb')
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(44100)
            elif message == "stop":
                print("Stopping recording")
                if wav_file:
                    wav_file.close()
                    print(f"Saved audio file: {filename}")
                    try:
                        await websocket.send(f"Audio saved as {filename}")
                    except ConnectionClosedOK:
                        print("Connection closed by client before final message could be sent")
            else:
                # Write audio data directly to WAV file
                if wav_file:
                    wav_file.writeframes(message)
    except ConnectionClosedOK:
        print("Connection closed by client")
    finally:
        print("Client disconnected")
        if wav_file:
            wav_file.close()

start_server = websockets.serve(audio_stream, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()