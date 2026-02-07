import cv2
import supervision as sv
from rfdetr import RFDETRMedium
from rfdetr.util.coco_classes import COCO_CLASSES

model = RFDETRMedium()

video_capture = cv2.VideoCapture(<WEBCAM_INDEX>)
if not video_capture.isOpened():
    raise RuntimeError("Failed to open webcam: <WEBCAM_INDEX>")

while True:
    success, frame_bgr = video_capture.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    detections = model.predict(frame_rgb, threshold=0.5)

    labels = [
        COCO_CLASSES[class_id]
        for class_id in detections.class_id
    ]

    annotated_frame = sv.BoxAnnotator().annotate(frame_bgr, detections)
    annotated_frame = sv.LabelAnnotator().annotate(annotated_frame, detections, labels)

    cv2.imshow("RF-DETR Webcam", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()