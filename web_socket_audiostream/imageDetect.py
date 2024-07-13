import cv2
import numpy as np

def get_color_positions(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Define ROIs (you may need to adjust these based on the exact image dimensions)
    height, width = img.shape[:2]
    roi_width = width // 5
    roi_height = height // 3
    rois = [
        img[roi_height:2*roi_height, roi_width:2*roi_width],
        img[roi_height:2*roi_height, 2*roi_width:3*roi_width],
        img[roi_height:2*roi_height, 3*roi_width:4*roi_width]
    ]
    
    # Get average color for each ROI
    colors = []
    for roi in rois:
        avg_color = np.mean(roi, axis=(0,1))
        colors.append(avg_color)
    
    # Classify colors
    color_positions = {}
    for i, color in enumerate(colors):
        b, g, r = color
        if r > g and r > b:
            color_positions['red'] = i
        elif b > r and b > g:
            color_positions['blue'] = i
        else:
            color_positions['white'] = i
    
    return color_positions

# Use the function
positions = get_color_positions('path_to_your_image.jpg')
print(positions)