with open("crab/APIKEY.TXT", "r", encoding="utf-8") as file:
        api = file.read().strip()
# Initialize the client
import cv2
from inference_sdk import InferenceHTTPClient

# 1. Initialize the Client
client = InferenceHTTPClient(
    api_url="http://localhost:9001",
    api_key=api
)

# 2. Start the Webcam
video = cv2.VideoCapture(1) # '0' is usually the default webcam

print("Press 'q' to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = video.read()
    if not ret:
        break

    # 3. Run Inference
    # We pass the 'frame' (numpy array) directly to the client
    result = client.infer(frame, model_id="crab-detector/2")

    # 4. Simple Visualization (Draw boxes)
    for prediction in result['predictions']:

        x, y, w, h = prediction['x'], prediction['y'], prediction['width'], prediction['height']
        label = prediction['class']
        print(prediction)
        # Convert Roboflow center-xy to top-left corner for OpenCV
        x1, y1 = int(x - w/2), int(y - h/2)
        x2, y2 = int(x + w/2), int(y + h/2)

        # Draw the rectangle and label
        if label == 'good':
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        elif label == 'evil':
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('Roboflow Crab Detection', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video.release()
cv2.destroyAllWindows()