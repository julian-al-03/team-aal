import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

# Load the TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path="your_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ESP32-CAM stream URL
url = 'http://172.16.25.102:81/stream'  # Replace with your ESP32-CAM's IP

# Open the stream
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to receive frame")
        break
    
    # Preprocess the frame for your model
    # This step depends on your model's requirements
    input_shape = input_details[0]['shape']
    processed_frame = cv2.resize(frame, (input_shape[1], input_shape[2]))
    processed_frame = processed_frame.astype(np.float32)  # Ensure float32 type
    processed_frame = np.expand_dims(processed_frame, axis=0)
    
    # Set the tensor to point to the input data to be inferred
    interpreter.set_tensor(input_details[0]['index'], processed_frame)

    # Run the inference
    interpreter.invoke()

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Process the prediction
    # This depends on your model's output format
    class_index = np.argmax(output_data[0])
    class_names = ['Your', 'Class', 'Names']  # Replace with your actual class names
    class_name = class_names[class_index]
    confidence = output_data[0][class_index]
    
    # Display result on the frame
    cv2.putText(frame, f"{class_name}: {confidence:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow('ESP32-CAM Classification', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()