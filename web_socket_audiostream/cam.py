import cv2
import numpy as np
from imageDetect import get_color_positions

async def capture_and_save_frame():
    url = 'http://172.16.25.102:81/stream'  # Replace with your ESP32-CAM's IP
    cap = cv2.VideoCapture(url)
    
    try:
        ret, frame = cap.read()
        if ret:
            frame_path = 'captured_frame.jpg'
            cv2.imwrite(frame_path, frame)
            return frame_path
        else:
            print("Failed to capture frame")
            return None
    finally:
        cap.release()