import cv2
import threading
from inference_sdk import InferenceHTTPClient  # type: ignore


with open("crab/APIKEY.TXT", "r", encoding="utf-8") as file:
    api = file.read().strip()

client = InferenceHTTPClient(api_url="http://localhost:9001", api_key=api)
video = cv2.VideoCapture(0)


lastpredictions = []
is_processing = False

def do_inference(frame_to_process):
    global lastpredictions, is_processing
    
    result = client.infer(frame_to_process, model_id="crab-detector/5")
    lastpredictions = result['predictions']
    is_processing = False

print("Press 'q' to quit.")

while True:
    ret, frame = video.read()
    if not ret: break
    frame = cv2.resize(frame, (640, 640))

    
    if not is_processing:
        is_processing = True
        
        thread = threading.Thread(target=do_inference, args=(frame.copy(),))
        thread.start()

    
    evilometer = 0
    for pred in lastpredictions:
        x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
        label = pred['class']
        x1, y1 = int(x - w/2), int(y - h/2)
        x2, y2 = int(x + w/2), int(y + h/2)

        color = (0, 0, 255) if label == 'evil' else (0, 255, 0)
        if label == 'evil': evilometer += 1
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.putText(frame, "Evilometer:"+str(evilometer), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    
    cv2.imshow('Roboflow Crab Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
