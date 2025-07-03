import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import requests
import time


# --- Configuration ---
# Load the pre-trained model
# Make sure the path to your model file is correct
try:
    model = load_model("/home/lightning/Downloads/eggs/mobilenetv2_egg_classifier_stage1.h5")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please ensure the file 'mobilenetv2_egg_classifier_stage1.h5' is in the same directory.")
    exit()

# Backend API endpoint
API_ENDPOINT = "https://avibot-dashboard-api-nh7v.onrender.com/record"

# Image size expected by the model
IMG_SIZE = (224, 224)

# --- Main Application Logic ---

def send_prediction_to_api(prediction_value):
    """Sends the prediction (0 or 1) to the backend API."""
    try:
        r = requests.post(API_ENDPOINT, json={"value": prediction_value}, timeout=5)
        if r.status_code == 200:
            print(f"API Call Success: Sent value {prediction_value}. Counts: {r.json()}")
        else:
            print(f"API Call Error: Status {r.status_code}, Response: {r.text}")
    except requests.exceptions.RequestException as e:
        print(f"API connection error: {e}")

def main():
    """Starts the webcam, performs live classification, and sends data."""
    # Start video capture from the default webcam (usually index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam opened successfully. Press 'q' to quit.")
    
    last_sent_prediction = -1 # Initialize with a value that won't match 0 or 1

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # 1. Preprocess the frame for the model
        # Convert the captured frame from BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Resize the frame to the model's expected input size
        resized_frame = cv2.resize(rgb_frame, IMG_SIZE)
        # Convert the frame to a numpy array and expand dimensions for batching
        img_array = np.expand_dims(resized_frame, axis=0)
        # Preprocess the image using MobileNetV2's specific function
        processed_frame = preprocess_input(img_array)

        # 2. Make a prediction
        prediction = model.predict(processed_frame)[0][0]
        
        # 3. Determine label and confidence
        is_cracked = prediction < 0.5
        label = "Cracked" if is_cracked else "Uncracked"
        confidence = 1 - prediction if is_cracked else prediction
        
        # 4. Send data to API only if the prediction changes
        current_prediction_value = 0 if is_cracked else 1
        if current_prediction_value != last_sent_prediction:
            send_prediction_to_api(current_prediction_value)
            last_sent_prediction = current_prediction_value

        # 5. Display the results on the frame
        # Set text color based on prediction
        text_color = (0, 0, 255) if is_cracked else (0, 255, 0) # Red for cracked, Green for uncracked
        display_text = f"{label} ({confidence*100:.2f}%)"
        
        # Put the text on the frame
        cv2.putText(frame, display_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)

        # Display the resulting frame in a window
        cv2.imshow('Live Egg Classifier', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture and destroy windows
    cap.release()
    cv2.destroyAllWindows()
    print("Application terminated.")

if __name__ == "__main__":
    main()