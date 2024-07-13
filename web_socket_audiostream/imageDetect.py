import cv2
import numpy as np

def get_color_positions(image_path):
    coordinates = [
    [0, 50, 5, 5],  # Example coordinates for first area
    [160, 100, 5, 5],  # Example coordinates for second area
    [306, 53, 5, 5]   # Example coordinates for third area
    ]
    # Read the image
    img = cv2.imread(image_path)
    
    # Function to get average color of a region
    def get_avg_color(x, y, w, h):
        region = img[y:y+h, x:x+w]
        return np.mean(region, axis=(0,1))
    
    # Get colors for each coordinate set
    colors = []
    for x, y, w, h in coordinates:
        avg_color = get_avg_color(x, y, w, h)
        colors.append(avg_color)
    
    # Classify colors
    color_positions = {}
    for i, color in enumerate(colors):
        b, g, r = color
        print(f"Position {i}: R={r:.2f}, G={g:.2f}, B={b:.2f}")
        
        if r > b and r > g:
            color_positions['red'] = i
        elif b > r and b > g:
            color_positions['blue'] = i
        elif r > 200 and g > 200 and b > 200:  # High values for all channels indicate white
            color_positions['white'] = i
    
    return color_positions